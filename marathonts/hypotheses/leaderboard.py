"""Leaderboard: every method ranked in every slice of the benchmark, then aggregated.

    python -m marathonts.hypotheses.leaderboard [--artifacts-dir artifacts/min] [--profile min] [--out DIR]

Slices (leaves):
* fidelity — one metric against one real reference: train / val / OOT (`@<part>` suffix, see
  `bench.fidelity`); groups computed once (F10, distance to train) form the slice "—";
* utility — TSTR of one task × model × test split (val / OOT) × metric;
* cost — slices `COST_SLICES`: total wall time of a series, training of its generator, generation of
  a new series by a trained model (sampling + assembly), peak memory (GPU, resident).

Within a leaf the methods are ranked per (dataset, seed): methods of one seed share the pool and the
test rows, so they form a block. Rank 1 = best, ties get the mean rank; a method missing in a block
is left out and the ranks of the others are rescaled to 1…k (k = number of ranked methods). A TSTR
cell a method's series could not train is not missing: `load_tables` enters it as a model that
learned nothing (`Config.utility_fail_penalty`, `catalog.impute_failed_utility`). Ranks are
averaged up a fixed hierarchy with equal weight at every level, so a group with many metrics does not
outweigh a group with few:

    leaf (metric | task × model × metric) → group (F-group | task type) → criterion (per reference / split)

Utility criteria use the primary metric of each task type (`PRIMARY_METRIC`) and the models fitted on
every task of the criterion; the other metrics and models are kept as separate leaves.

Rankings (`RANKINGS`): four, each the mean of two domains with equal weight — fidelity (the mean of its
criteria, each averaged over its references) and utility of one task type:

    fidelity against val + OOT  × utility classification     (`holdout_clf`)
    fidelity against val + OOT  × utility regression         (`holdout_reg`)
    fidelity against train      × utility classification     (`train_clf`)
    fidelity against train      × utility regression         (`train_reg`)

Core rankings (`CORE_RANKINGS`, `core_<ranking>`): the same four with the fidelity domain restricted
to `CORE_METRICS` — one or two canonical metrics per criterion, fixed in advance. Next to them: normalised scores of the core metrics (random assembly = 0, real data = 1,
`normalized_scores`) and the anchor check of every metric (`anchor_check`: does it tell real data from
a random assembly beyond the noise; on all, even and odd seeds).

Utility: TSTR tested on val and OOT. Not part of the rankings: groups computed once (slice "—": F10,
privacy — ranked on its own as the criterion `fidelity:privacy@—`) and cost (time, memory — ranked by
the cost slices; `with_cost:<ranking>` adds cost to a ranking as a third domain of equal weight).
Domain-level ranks (`DOMAINS`: fidelity or utility alone, per slice) are reported next to the criteria.
Thematic slices (`THEMES`: class balance, extremes) rank the leaves of one property across groups;
they are reported next to the criteria and are not part of the rankings.

Uncertainty: two-level bootstrap (datasets, then seeds within a dataset) of the averaged ranks → CI of
each method's rank and the probability of being first / in the top 3; Friedman test with blocks =
datasets and the Nemenyi critical difference; the top tier = the best method and every method not
significantly worse than it (one-sided Wilcoxon over datasets, Holm; Benavoli et al., 2016 — the
Nemenyi CD grows with the number of methods and is reported only for reference). Stability: Kendall τ
between the rankings of different criteria and slices (train vs val vs OOT, fidelity vs utility,
linear vs boosting). The second path of the noise pair (`noise_pair[1]`) and the pseudo-methods `real`, `<m>@len` are
not ranked; it is reported as a sanity check — ranked together with every method, it must not
differ from its pair (two-sided Wilcoxon over datasets).
"""
from __future__ import annotations

import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats as sps

from . import stats as S

from marathonts.bench import registry as R  # noqa: E402
from marathonts.bench.fidelity import GROUP_OF, ORIENT, PRIMARY_ONLY, split_ref  # noqa: E402

from .catalog import CALENDAR_VALIDITY, PRIMARY_METRIC, utility_long  # noqa: E402

# fidelity group → criterion (a custom group is its own criterion)
FID_CRITERIA = {
    "F1_marginal": "distribution", "F2_increments": "distribution",
    "F3_dependence": "dependence", "F4_seasonality": "dependence",
    "F6_windows": "windows", "F9_coverage": "windows",
    "F7_long_structure": "long_structure", "F8_target": "target",
    "F5_seams": "seams", "F10_memorisation": "privacy",
    "F11_class_balance": "target", "F12_extremes": "distribution",
}
# task type → utility criterion
UT_CRITERIA = {"clf": "classification", "mc": "classification",
               "reg": "regression", "qreg": "regression", "ms": "regression", "vol": "regression"}
# the rankings: domain prefix → slices averaged (a criterion belongs to its longest matching prefix);
# the domains of a ranking have equal weight, a domain is the mean of its criteria. Fidelity: every
# criterion except those computed once (slice "—": privacy); utility: one criterion, TSTR on val and OOT
FIDELITY_REFS = {"holdout": ("val", "oot"), "train": ("train",)}
UTILITY_PARTS = {"clf": "classification", "reg": "regression"}
_REF_TEXT = {"holdout": "val and OOT (each criterion is the mean of the two)", "train": "train"}
_UT_TEXT = {"clf": "classification (binary and multiclass tasks)",
            "reg": "regression (point, quantile, multi-step and volatility tasks)"}
_FID_LIST = ("distribution (F1, F2, F12), dependence (F3, F4), windows (F6, F9), long structure (F7), "
             "target (F8, F11), seams (F5)")
RANKINGS = {
    f"{r}_{u}": dict(
        title=f"Fidelity: {'val + OOT' if r == 'holdout' else 'train'}; utility: {UTILITY_PARTS[u]}",
        domains={"fidelity:": refs, f"utility:{UTILITY_PARTS[u]}": ("val", "oot")},
        text=(f"Fidelity domain — the criteria {_FID_LIST}, each against {_REF_TEXT[r]}. Utility domain — "
              f"TSTR {_UT_TEXT[u]}, primary metric of each task type, tested on val and OOT. Rank = mean of "
              "the two domains with equal weight. Not included: privacy (F10), time, memory."))
    for r, refs in FIDELITY_REFS.items() for u in UTILITY_PARTS}
# core metric set: one or two canonical fidelity metrics per criterion, fixed in advance by what they
# measure (not by how well they separated the methods in a run — that would select on the data the
# conclusions are drawn from). Utility is the same
# as in the full rankings (TSTR, primary metric of every task type, every task)
CORE_METRICS = {
    "distribution": ("F1.2_w1", "F2.1_ks_d24"),                  # Wasserstein of values; KS of 24 h changes
    "dependence": ("F3.5_log_psd", "F4.1_how_mean"),             # spectrum (every lag); weekly profile
    "windows": ("F6.1_disc_score", "F6.4_mmd"),                  # discriminative score; MMD of windows
    "long_structure": ("F7.1_roll_mean_ks", "F7.2_roll_std_ks"),  # rolling mean and spread
    "target": ("F11.1_class_share_logratio",),                   # class shares of every classification task
    "seams": ("F5.7_seam_detect_auc_dev",),                      # can a classifier find the seams
}
CORE_FIDELITY: set = set()
CORE_RANKINGS: dict = {}
_CORE_LIST = ""



def places(x: np.ndarray, axis: int) -> np.ndarray:
    """0-based place of every entry along `axis` (lower is better): the number of entries strictly better.
    Tied entries share a place, so P(first) and P(top 3) do not depend on the order of the methods or on how
    a sort breaks ties on a given CPU."""
    x = np.moveaxis(np.asarray(x, float), axis, -1)
    out = (x[..., None, :] < x[..., :, None]).sum(-1)
    return np.moveaxis(out, -1, axis)

def core_changed() -> None:
    """Derive the core set, its text and the core rankings from `CORE_METRICS` (in place: other modules hold
    references); `Config.core_metrics` replaces `CORE_METRICS` through `catalog.configure`."""
    global _CORE_LIST
    CORE_FIDELITY.clear()
    CORE_FIDELITY.update(m for ms in CORE_METRICS.values() for m in ms)
    _CORE_LIST = "; ".join(f"{c.replace('_', ' ')} ({', '.join(ms)})" for c, ms in CORE_METRICS.items())
    CORE_RANKINGS.clear()
    CORE_RANKINGS.update({
        f"core_{k}": dict(title=f"Core metrics. {d['title']}", domains=d["domains"],
                          text=(f"As `{k}`, with the fidelity domain restricted to the core metrics: {_CORE_LIST}. "
                                "Utility domain unchanged."))
        for k, d in RANKINGS.items()})


core_changed()
# cost as a third domain of equal weight next to a ranking (Pareto front and `with_cost:<ranking>`)
COST_DOMAIN = {"cost": ("total", "memory")}
# domain-level ranks: the fidelity / utility domain alone, per slice and over all its slices (reported
# next to the criteria; not part of the rankings; fidelity without privacy)
DOMAINS = {
    "fidelity@train": {"fidelity:": ("train",)}, "fidelity@val": {"fidelity:": ("val",)},
    "fidelity@oot": {"fidelity:": ("oot",)}, "fidelity@all": {"fidelity:": ("train", "val", "oot")},
    "utility@val": {"utility:": ("val",)}, "utility@oot": {"utility:": ("oot",)},
    "utility@all": {"utility:": ("val", "oot")},
}

# thematic slices: leaves across groups, ranked like the criteria but not part of the rankings.
# fidelity: base metric ids (every reference); utility: (task, task type, metric) → in the theme
EXTREME_METRICS = {"F1.5_q01_err", "F1.5_q99_err", "F1.6_kurt_err", "F1.10_hill_err", "F2.4_big_jump_share_err",
                   "F7.4_excursion_ks"}


def _rare_task(task: str) -> bool:
    from marathonts.bench.fidelity import _is_rare

    return task in R.tasks and _is_rare(R.tasks.get(task))


THEMES = {
    # class shares of every classification task; a prior shift shows in TSTR as miscalibration (ECE)
    "class_balance": dict(fidelity=lambda b: b == "F8.1_class_tvd" or b.startswith("F11."),
                          utility=lambda task, kind, metric: kind in ("clf", "mc") and metric == "ece"),
    # tails, outliers and extremes; TSTR error on the extreme 10% of targets and PR AUC of rare events
    "extremes": dict(fidelity=lambda b: b in EXTREME_METRICS or b.startswith("F12."),
                     utility=lambda task, kind, metric: (kind in ("reg", "vol") and metric == "mae_extreme")
                     or (kind == "clf" and metric == "pr_auc" and _rare_task(task))),
}
KEYS = ["dataset", "seed", "method"]


# ─────────────────────── method families ───────────────────────────────────
def family(method: str) -> str:
    """Long-series generator / random selection / optimised selection / seam processing (from the method spec).
    Seam processing is a joiner applied to a stitcher that also runs without it; a method whose assembler
    never runs without its joiner (`vae_quilting`: patch choice and boundary cut are one method) belongs to
    the family of its selection, as in `not_ranked`."""
    import marathonts.bench.methods  # noqa: F401  (registers the built-in methods)

    if method not in R.methods:
        return "custom"
    s = R.methods.get(method)
    if s.long:
        return "long-series generator"
    if s.joiner and any(not o.joiner and (o.pool, o.assembler) == (s.pool, s.assembler)
                        for o in (R.methods.get(m) for m in R.methods.names())):
        return f"seam processing ({s.joiner})"
    return "random selection" if s.assembler in ("random", "random_b") else "optimised selection"


# ─────────────────────── long rows: one oriented score per leaf ────────────
def fidelity_rows(fid: pd.DataFrame, methods, primary_ref: str = "val") -> pd.DataFrame:
    cols = [c for c in fid.columns if c in ORIENT and split_ref(c, primary_ref)[0] not in CALENDAR_VALIDITY]
    L = fid[fid["method"].isin(methods)].melt(id_vars=KEYS, value_vars=cols, var_name="leaf", value_name="value")
    L = L.dropna(subset=["value"])
    L["group"] = L["leaf"].map(GROUP_OF)
    L["slice"] = ["—" if g in PRIMARY_ONLY else split_ref(u, primary_ref)[1] for u, g in zip(L["leaf"], L["group"])]
    L["criterion"] = "fidelity:" + L["group"].map(lambda g: FID_CRITERIA.get(g, g))
    L["score"] = L["value"] * L["leaf"].map(ORIENT)
    L["model"], L["agg"] = "", True
    return L


def utility_rows(ut: pd.DataFrame, methods) -> pd.DataFrame:
    L = utility_long(ut, all_metrics=True)
    L = L[(L["regime"] == "S") & L["method"].isin(methods)].dropna(subset=["value"]).copy()
    if not len(L):
        return L
    kind = dict(zip(ut["task"], ut["task_kind"]))
    L["group"] = L["task"].map(kind)
    L["slice"] = L["split"].astype(str)
    L["criterion"] = "utility:" + L["group"].map(lambda k: UT_CRITERIA.get(k, k))
    L["leaf"] = L["task"] + "|" + L["model"] + "|" + L["metric"]
    from .catalog import HIGHER_BETTER

    L["score"] = np.where(L["metric"].isin(HIGHER_BETTER), L["value"], -L["value"])
    # aggregated: the primary metric of the task type, on the models fitted on every task of the criterion
    prim = L["metric"] == L["group"].map(PRIMARY_METRIC)
    cover = L[prim].groupby(["criterion", "model"])["task"].nunique()
    need = L[prim].groupby("criterion")["task"].nunique()
    common = {(c, m) for (c, m), n in cover.items() if n == need[c]}
    from .catalog import _warn_once

    for c in need.index:
        out = sorted(m for (c2, m) in cover.index if c2 == c and (c, m) not in common)
        if not any(c2 == c for c2, _ in common):
            _warn_once(f"{c}: no model is fitted on every task of the criterion — it has no aggregated rank "
                       f"(models: {', '.join(out)}; Config.model_tasks)")
        elif out:
            _warn_once(f"{c}: models not fitted on every task of the criterion are left out of its aggregated rank "
                       f"(kept as leaves): {', '.join(out)}")
    L["agg"] = prim & np.array([(c, m) in common for c, m in zip(L["criterion"], L["model"])], bool)
    return L


# cost slices: slice → {leaf: (columns of the timing table, reduction)}; lower is better. Training of a
# shared generator (one VAE per pool, Diffusion-TS in min / mid) is charged to every seed and method using it
COST_SLICES = {
    "total": {"wall_time": (["total_wall_s"], "sum")},
    "training": {"wall_time": (["fit_wall_s"], "sum")},
    "generation": {"wall_time": (["sample_wall_s", "assemble_wall_s"], "sum")},
    "memory": {"gpu_peak_mb": (["fit_gpu_peak_mb", "fit_tf_gpu_peak_mb", "sample_gpu_peak_mb", "assemble_gpu_peak_mb"], "max"),
               "rss_delta_mb": (["fit_rss_delta_mb", "sample_rss_delta_mb", "assemble_rss_delta_mb"], "max")},
}


def cost_rows(timing: pd.DataFrame, methods) -> pd.DataFrame:
    """One row per (dataset, seed, method) and cost leaf (`COST_SLICES`); a leaf whose columns are
    missing from the timing table is skipped. Group = the leaf, so time and memory weigh the same."""
    if timing is None or not len(timing):
        return pd.DataFrame()
    t = timing[timing["method"].isin(methods)]
    out = []
    for sl, leaves in COST_SLICES.items():
        for leaf, (cols, how) in leaves.items():
            cols = [c for c in cols if c in t]
            if not cols:
                continue
            v = t[cols].astype(float)
            v = v.fillna(0.0).sum(axis=1) if how == "sum" else v.max(axis=1)
            v = v.where(t[cols].notna().any(axis=1))
            d = t[KEYS].assign(leaf=f"cost:{leaf}", group=leaf, slice=sl, criterion="cost", model="",
                               value=v.to_numpy(), score=-v.to_numpy(), agg=True).dropna(subset=["value"])
            out.append(d)
    return pd.concat(out, ignore_index=True) if out else pd.DataFrame()


def rank_rows(L: pd.DataFrame, k: int) -> pd.DataFrame:
    """Rank per (dataset, seed, leaf, slice), 1 = best, rescaled to 1…k when methods are missing."""
    g = L.groupby(["dataset", "seed", "leaf", "slice"])["score"]
    r, n = g.rank(ascending=False, method="average"), g.transform("count")
    return L.assign(rank=np.where(n > 1, 1 + (r - 1) * (k - 1) / (n - 1).clip(lower=1), np.nan))


# ─────────────────────── aggregation ───────────────────────────────────────
def column(criterion: str, sl: str) -> str:
    return f"{criterion}@{sl}"


def aggregate(L: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """(groups, criteria): mean rank per (dataset, seed, method) — columns `<group>@<slice>` and
    `<criterion>@<slice>` (cost: `cost`). Leaves → groups → criteria, equal weights."""
    A = L[L["agg"]]
    G = A.groupby(["criterion", "group", "slice", *KEYS])["rank"].mean()
    C = G.groupby(["criterion", "slice", *KEYS]).mean().reset_index()
    C["col"] = [column(c, s) for c, s in zip(C["criterion"], C["slice"])]
    G = G.reset_index()
    G["col"] = [f"{c}/{g}@{s}" for c, g, s in zip(G["criterion"], G["group"], G["slice"])]
    wide = lambda t: t.pivot_table(index=KEYS, columns="col", values="rank").sort_index(axis=1)
    return wide(G), wide(C)


def rank_of(C: pd.DataFrame, domains: dict, weights: dict | None = None) -> pd.Series:
    """Rank of a ranking per (dataset, seed, method): each criterion averaged over its slices in
    `domains`, the criteria of a domain averaged (weighted), then the domains averaged."""
    crit = criterion_means(C, domains)
    w = pd.Series({k: (weights or {}).get(k, 1.0) for k in crit.columns}, dtype=float)
    dom = {}
    for pref in domains:
        cols = [c for c in crit.columns if _domain(c, domains) == pref]
        if cols:
            sub, ww = crit[cols], w[cols]
            dom[pref] = (sub * ww).sum(axis=1, min_count=1) / sub.notna().mul(ww).sum(axis=1)
    if not dom:                                      # no criterion of `domains` in this run (e.g. no utility)
        return pd.Series(dtype=float)
    return pd.DataFrame(dom).mean(axis=1)


def criterion_means(C: pd.DataFrame, domains: dict) -> pd.DataFrame:
    """Criterion means per (dataset, seed, method): the criteria of `domains`, each averaged over its
    slices."""
    parts = {}
    for c in C.columns:
        crit, _, sl = c.partition("@")
        pref = _domain(crit, domains)
        if pref is not None and (sl or "—") in domains[pref]:
            parts.setdefault(crit, []).append(c)
    return pd.DataFrame({k: C[v].mean(axis=1) for k, v in parts.items()})


def _domain(crit: str, domains: dict) -> str | None:
    """The domain of a criterion: its longest matching prefix (`fidelity:privacy` before `fidelity:`)."""
    m = [p for p in domains if crit.startswith(p)]
    return max(m, key=len) if m else None


# ─────────────────────── uncertainty ───────────────────────────────────────
def theme_rows(L: pd.DataFrame, primary_ref: str = "val") -> pd.DataFrame:
    """Rows of the thematic slices (`THEMES`), ranks kept: criterion `theme:<name>:fidelity` (group =
    the metric, every metric weighs the same) and `theme:<name>:utility` (group = task type, the
    models fitted on every task of the theme)."""
    out = []
    F = L[L["criterion"].str.startswith("fidelity:")]
    U = L[L["criterion"].str.startswith("utility:")]
    fb = F["leaf"].map(lambda u: split_ref(u, primary_ref)[0])
    for th, sel in THEMES.items():
        f = F[fb.map(sel["fidelity"]).astype(bool)].assign(group=fb)
        if len(U):
            met = U["leaf"].str.rsplit("|", n=1).str[-1]
            m = np.array([bool(sel["utility"](t, k, me)) for t, k, me in zip(U["task"], U["group"], met)], bool)
            u = U[m]
            if len(u):
                cover = u.groupby("model")["task"].nunique()
                u = u[u["model"].isin(cover[cover == u["task"].nunique()].index)]
        else:
            u = U
        for part, d in (("fidelity", f), ("utility", u)):
            if len(d):
                out.append(d.assign(criterion=f"theme:{th}:{part}", agg=True))
    return pd.concat(out, ignore_index=True) if out else pd.DataFrame()


def summarize(x: pd.Series, n_boot: int = 1000, seed: int = 0, alpha: float = 0.05) -> pd.DataFrame:
    """`x`: rank indexed by (dataset, seed, method). Per method: mean rank over datasets (seeds
    averaged within a dataset), bootstrap CI and P(first), P(top 3); Friedman p and Nemenyi CD
    (reference only: `top_tier` = Friedman rank within CD of the best); the tier used in the report —
    the best method and every method not significantly worse than it (Wilcoxon, Holm)."""
    if not len(x) or "method" not in x.index.names:
        return pd.DataFrame()
    W = x.unstack("method")
    D = W.groupby(level="dataset").mean()
    D = D.loc[:, D.notna().sum() >= max(3, len(D) // 2)]
    if D.shape[1] < 2 or len(D) < 2:
        return pd.DataFrame()
    W = W[D.columns]
    rng = np.random.default_rng(seed)
    # datasets × seeds × methods, padded with NaN; resample datasets, then seeds within them
    blocks = [W.xs(d, level="dataset").to_numpy(float) for d in D.index]
    sizes = np.array([len(a) for a in blocks])
    T = np.full((len(blocks), sizes.max(), D.shape[1]), np.nan)
    for i, a in enumerate(blocks):
        T[i, : len(a)] = a
    B = []
    with warnings.catch_warnings():                  # a method missing in every resampled block → NaN
        warnings.simplefilter("ignore", RuntimeWarning)
        for pick, idx, valid in S.resample_groups(rng, sizes, n_boot, D.shape[1]):
            v = np.where(valid[..., None], T[pick[..., None], idx], np.nan)
            B.append(np.nanmean(np.nanmean(v, axis=2), axis=1))
    B = np.concatenate(B)
    B = np.where(np.isnan(B), np.inf, B)
    place = places(B, axis=1)
    out = pd.DataFrame({"avg_rank": D.mean(), "ci_lo": np.quantile(B, alpha / 2, axis=0),
                        "ci_hi": np.quantile(B, 1 - alpha / 2, axis=0), "p_first": (place == 0).mean(0),
                        "p_top3": (place < 3).mean(0), "n_datasets": D.notna().sum()}, index=D.columns)
    p, fr, cd = S.friedman_nemenyi(-D)
    out["friedman_rank"] = fr.reindex(out.index) if fr is not None else np.nan
    best = out["friedman_rank"].min()
    out["top_tier"] = out["friedman_rank"] <= best + cd if np.isfinite(cd) else False
    out = out.sort_values("avg_rank")
    # every method against the best one: one-sided Wilcoxon over datasets (worse than the best?), Holm;
    # the tier = the best and every method not significantly worse (Benavoli et al., 2016)
    best = out.index[0]
    pw = {m: S.wilcoxon((D[m] - D[best]).dropna().to_numpy(), "greater") for m in out.index[1:]}
    adj = dict(zip(pw, S.holm(np.array(list(pw.values()), float)))) if pw else {}
    out["p_worse_than_best_holm"] = pd.Series(adj)
    out["tier_wilcoxon"] = out["p_worse_than_best_holm"].fillna(1.0) >= alpha
    used = S.complete_blocks(-D, 1)                  # what the Friedman test ran on (see `stats.complete_blocks`)
    out.attrs.update(p_friedman=p, nemenyi_cd=cd, n_blocks=len(used), n_methods_friedman=used.shape[1])
    return out


def kendall_matrix(avg: pd.DataFrame) -> pd.DataFrame:
    """Kendall τ between the method rankings of every pair of columns (methods present in both)."""
    cols = list(avg.columns)
    M = pd.DataFrame(np.nan, index=cols, columns=cols)
    for i, a in enumerate(cols):
        for b in cols[i:]:
            j = avg[[a, b]].dropna()
            t = sps.kendalltau(j[a], j[b]).statistic if len(j) > 2 else np.nan
            M.loc[a, b] = M.loc[b, a] = t
    return M


MODEL_ORDER = ("linear", "gbdt", "mlp")             # order of the built-in models in the model comparisons
SLICE_COMPARISONS = {"train ↔ val", "val ↔ oot", "train ↔ oot", "fidelity ↔ utility"}


def stability_pairs(avg: pd.DataFrame) -> pd.DataFrame:
    """Kendall τ of the pre-defined comparisons: train ↔ val ↔ OOT for every fidelity criterion,
    val ↔ OOT for every utility criterion, every pair of models (linear ↔ gbdt, …), fidelity ↔ utility."""
    def tau(a, b):
        j = avg[[a, b]].dropna()
        return sps.kendalltau(j[a], j[b]).statistic if len(j) > 2 else np.nan

    rows = []
    crits = sorted({c.partition("@")[0] for c in avg.columns
                    if not c.startswith(("domain:", "ranking:", "with_cost:"))})   # criteria only
    for c in crits:
        sl = {c2.partition("@")[2]: c2 for c2 in avg.columns if c2.partition("@")[0] == c}
        for a, b in (("train", "val"), ("val", "oot"), ("train", "oot")):
            if a in sl and b in sl:
                rows.append(dict(comparison=f"{a} ↔ {b}", criterion=c, tau=tau(sl[a], sl[b])))
    by_base: dict = {}                              # every pair of models of a utility criterion (linear ↔ gbdt, …)
    for c in [c for c in avg.columns if c.startswith("utility:") and "|" in c]:
        base, _, m = c.rpartition("|")
        by_base.setdefault(base, []).append(m)
    for base, ms in by_base.items():
        ms = sorted(ms, key=lambda m: (MODEL_ORDER.index(m) if m in MODEL_ORDER else len(MODEL_ORDER), m))
        for i, a in enumerate(ms):
            for b in ms[i + 1:]:
                rows.append(dict(comparison=f"{a} ↔ {b}", criterion=base, tau=tau(f"{base}|{a}", f"{base}|{b}")))
    for f in [c for c in avg.columns if c.startswith("fidelity:") and c.endswith("@val")]:
        for u in [c for c in avg.columns if c.startswith("utility:") and "|" not in c]:
            rows.append(dict(comparison="fidelity ↔ utility", criterion=f"{f} ↔ {u}", tau=tau(f, u)))
    return pd.DataFrame(rows)


def weight_sensitivity(Cm: pd.DataFrame, domains: dict, n: int = 2000, seed: int = 0) -> pd.DataFrame:
    """A ranking under random criterion weights (Dirichlet(1) within each domain, the domains
    averaged as in `rank_of`): share of draws where a method is first / in the top 3, and
    Kendall τ with the equal-weight ranking."""
    D = Cm.groupby(level="dataset").mean() if "dataset" in Cm.index.names else Cm
    M = D.groupby(level="method").mean() if "method" in D.index.names else D
    M = M.dropna(how="all")
    if M.shape[1] < 2 or len(M) < 3:
        return pd.DataFrame()
    rng = np.random.default_rng(seed)
    A = np.nan_to_num(M.to_numpy(), nan=np.nanmean(M.to_numpy()))
    doms = [[i for i, c in enumerate(M.columns) if _domain(c, domains) == p] for p in domains]
    doms = [d for d in doms if d]

    def score(ws):                                   # ws: one weight vector per domain → methods
        return np.mean([A[:, d] @ w for d, w in zip(doms, ws)], axis=0)

    eq = pd.Series(score([np.full(len(d), 1 / len(d)) for d in doms]), index=M.index)
    sc = np.stack([score([rng.dirichlet(np.ones(len(d))) for d in doms]) for _ in range(n)], axis=1)
    place = places(sc, axis=0)
    taus = [sps.kendalltau(eq.to_numpy(), sc[:, i]).statistic for i in range(min(n, 500))]
    out = pd.DataFrame({"equal_weights_rank": eq, "p_first": (place == 0).mean(1), "p_top3": (place < 3).mean(1)},
                       index=M.index).sort_values("equal_weights_rank")
    out.attrs["median_tau_vs_equal"] = float(np.median(taus))
    return out


# ─────────────────────── anchors: random assembly = 0, real data = 1 ───────
ANCHOR_REFS = ("val", "train")      # fidelity references with a real anchor (`real` is a piece of OOT)


def _anchor_long(T: dict, cfg) -> pd.DataFrame:
    """One value per (dataset, seed, method, leaf): fidelity against val and train (privacy and calendar
    checks excluded), utility — primary metric of every task × model × split, TSTR (the TRTR of `real`
    kept as the method `real`). Columns: dataset, seed, method, leaf, kind, criterion, core, value."""
    out = []
    fid = T.get("fidelity", pd.DataFrame())
    if len(fid):
        cols = [c for c in fid.columns if c in ORIENT and GROUP_OF.get(c) not in PRIMARY_ONLY
                and split_ref(c, cfg.fidelity_ref)[1] in ANCHOR_REFS
                and split_ref(c, cfg.fidelity_ref)[0] not in CALENDAR_VALIDITY]
        F = fid.melt(id_vars=KEYS, value_vars=cols, var_name="leaf", value_name="value").dropna(subset=["value"])
        F["kind"] = "fidelity"
        F["criterion"] = "fidelity:" + F["leaf"].map(GROUP_OF).map(lambda g: FID_CRITERIA.get(g, g))
        F["core"] = F["leaf"].map(lambda u: split_ref(u, cfg.fidelity_ref)[0] in CORE_FIDELITY)
        out.append(F)
    ut = T.get("utility", pd.DataFrame())
    if len(ut):
        U = utility_long(ut)
        U = U[((U["regime"] == "S") & (U["method"] != "real")) | ((U["regime"] == "R") & (U["method"] == "real"))]
        kind = dict(zip(ut["task"], ut["task_kind"]))
        U = U.assign(leaf=U["task"] + "|" + U["model"] + "|" + U["metric"] + "@" + U["split"].astype(str),
                     kind="utility", core=True,
                     criterion="utility:" + U["task"].map(kind).map(lambda k: UT_CRITERIA.get(k, k)))
        out.append(U[KEYS + ["leaf", "kind", "criterion", "core", "value"]].dropna(subset=["value"]))
    return pd.concat(out, ignore_index=True) if out else pd.DataFrame()


def _pair_noise(w: pd.DataFrame, a: str, b: str) -> pd.Series:
    """Per (dataset, leaf): median over seeds of |random − twin|; without the twin (min) — median of
    |random(seed k) − random(next seed)|, the between-seed spread of the random path."""
    if b in w:
        return (w[a] - w[b]).abs().groupby(level=["dataset", "leaf"]).median()
    s = w[a].sort_index()
    return s.groupby(level=["dataset", "leaf"]).diff().abs().groupby(level=["dataset", "leaf"]).median()


def anchor_check(T: dict, cfg) -> pd.DataFrame:
    """Does a metric separate the anchors beyond the noise? Per (dataset, leaf): gap = |real − random
    assembly| (the random assembly averaged over seeds), noise = median over seeds of |random − its twin|
    (`noise_pair`; without the twin — the between-seed spread of the random path, `_pair_noise`); ratio = gap / noise, median over datasets; separated = ratio > 1. The competing
    methods are not looked at, so the check does not select on who wins. Computed on all seeds and
    separately on even and odd seeds: `flip` — the verdict differs between the two halves.
    Fidelity: `real` is a piece of OOT, shorter than the synthetic series; for distance metrics its
    estimation noise is larger, so the gap is underestimated and the check is conservative."""
    L = _anchor_long(T, cfg)
    a, b = tuple(cfg.noise_pair)
    if not len(L) or a not in set(L["method"]):
        return pd.DataFrame()
    W = L[L["method"].isin([a, b, "real"])].pivot_table(index=["dataset", "leaf", "seed"], columns="method",
                                                        values="value")
    if "real" not in W:
        return pd.DataFrame()
    meta = L.drop_duplicates("leaf").set_index("leaf")[["kind", "criterion", "core"]]
    real = W["real"].groupby(level=["dataset", "leaf"]).mean()       # fidelity: one value; utility: TRTR
    out = {}
    for name, sel in (("all", lambda s: np.ones(len(s), bool)), ("even", lambda s: s % 2 == 0),
                      ("odd", lambda s: s % 2 == 1)):
        w = W[sel(W.index.get_level_values("seed").to_numpy())]
        g = w.groupby(level=["dataset", "leaf"])
        noise = _pair_noise(w, a, b)
        gap = (real.reindex(noise.index) - g[a].mean()).abs()
        ratio = (gap / noise.where(noise > 0)).groupby(level="leaf").median()
        out[f"ratio_{name}"] = ratio
        out[f"separated_{name}"] = ratio > 1
    res = pd.DataFrame(out).join(meta)
    res["n_datasets"] = real.groupby(level="leaf").count()
    res["flip"] = res["separated_even"] != res["separated_odd"]
    return res.reset_index()[["leaf", "kind", "criterion", "core", "n_datasets", "ratio_all", "separated_all",
                              "ratio_even", "ratio_odd", "separated_even", "separated_odd", "flip"]]


def normalized_scores(T: dict, cfg, methods) -> tuple[pd.DataFrame, pd.DataFrame]:
    """(per leaf, summary): the value of a method on the scale random assembly = 0, real data = 1,
    (x − x_random) / (x_real − x_random), on the core metrics. Fidelity: against val and train, on the
    series cut to the length of the real reference (`<method>@len`, seed 0) — the same length as `real`;
    utility: TSTR vs TRTR, seeds averaged within a dataset, models fitted on every task. A dataset is
    left out of a leaf when its anchors are not separated beyond the noise (|x_real − x_random| ≤ median
    |random − twin| over seeds, or the between-seed spread of the random path without the twin). Summary: per method and criterion, median over leaves within a dataset,
    then median over datasets; `fidelity` / `utility` — the same over all leaves of the domain."""
    L = _anchor_long(T, cfg)
    a, b = tuple(cfg.noise_pair)
    if not len(L):
        return pd.DataFrame(), pd.DataFrame()
    L = L[L["core"]]
    seeds = L[L["method"].isin([a, b])].pivot_table(index=["dataset", "leaf", "seed"], columns="method", values="value")
    noise = _pair_noise(seeds, a, b) if a in seeds else pd.Series(dtype=float)
    U = L[L["kind"] == "utility"]
    if len(U):                                        # models fitted on every task of the criterion (as in the ranks)
        cover = U.assign(model=U["leaf"].str.split("|").str[1], task=U["leaf"].str.split("|").str[0])
        n = cover.groupby(["criterion", "model"])["task"].nunique()
        need = cover.groupby("criterion")["task"].nunique()
        keep = {(c, m) for (c, m), k in n.items() if k == need[c]}
        U = U[[(c, m) in keep for c, m in zip(cover["criterion"], cover["model"])]]
    F = L[L["kind"] == "fidelity"]
    F = F[F["method"].str.endswith("@len") | (F["method"] == "real")].assign(
        method=lambda d: d["method"].str.removesuffix("@len"))
    M = pd.concat([F, U]).groupby(["dataset", "leaf", "method"])["value"].mean().unstack("method")
    if a not in M or "real" not in M:
        return pd.DataFrame(), pd.DataFrame()
    # zero point of a method: the random assembly of its own pool (another pool generator has its own); a
    # long-series generator and a pool without a random path: the noise pair's one
    def anchor(m):
        s = R.methods.get(m) if m in R.methods else None
        if s is not None and s.pool:
            r = [x for x in M.columns if x in R.methods and R.methods.get(x).pool == s.pool
                 and R.methods.get(x).assembler == "random"]
            if r:
                return r[0]
        return a

    def zero(x):                                     # gap to real and where it exceeds the noise, per anchor
        if x == a:
            nz = noise
        else:
            px = R.methods.get(x).pool
            tw = [y for y in set(L["method"]) if y in R.methods and R.methods.get(y).pool == px
                  and R.methods.get(y).assembler == "random_b"]
            sd = L[L["method"].isin([x, *tw])].pivot_table(index=["dataset", "leaf", "seed"], columns="method",
                                                          values="value")
            nz = _pair_noise(sd, x, tw[0] if tw else "") if x in sd else pd.Series(dtype=float)
        g = M["real"] - M[x]
        return g, g.abs() > nz.reindex(g.index).fillna(0)

    zeros = {}
    meta = L.drop_duplicates("leaf").set_index("leaf")[["kind", "criterion"]]
    rows = []
    for m in [m for m in methods if m in M]:
        x = anchor(m)
        if x not in zeros:
            zeros[x] = zero(x)
        gap, ok = zeros[x]
        s = ((M[m] - M[x]) / gap.where(ok)).rename("score").reset_index().dropna(subset=["score"])
        rows.append(s.assign(method=m))
    per = pd.concat(rows, ignore_index=True).join(meta, on="leaf") if rows else pd.DataFrame()
    if not len(per):
        return per, pd.DataFrame()
    crit = (per.groupby(["method", "criterion", "dataset"])["score"].median()
            .groupby(["method", "criterion"]).median().unstack("criterion"))
    dom = (per.groupby(["method", "kind", "dataset"])["score"].median()
           .groupby(["method", "kind"]).median().unstack("kind"))
    crit.columns = [c.replace("fidelity:", "").replace("utility:", "") for c in crit.columns]
    summ = dom.join(crit).reindex(sorted(per["method"].unique(), key=lambda m: (family(m), m)))
    summ.index.name = "method"
    return per, summ


# ─────────────────────── build ─────────────────────────────────────────────
def ranked_methods(T: dict, cfg) -> list[str]:
    fid = T.get("fidelity", pd.DataFrame())
    present = set(fid["method"]) if len(fid) else set()
    if len(T.get("utility", pd.DataFrame())):
        present |= set(T["utility"]["method"])
    twin = tuple(cfg.noise_pair)[1]
    return sorted(m for m in present if m != "real" and "@" not in m and m != twin)


def not_ranked(cfg, methods) -> list[str]:
    """Methods left out of the rankings (`Config.rank_exclude`; None → the seam-processing variants unless
    every stitcher has them, `smooth_paths="all"`: with joiners on some stitchers only, those would enter the
    ranking several times and every other stitcher once). A method whose assembler never runs without its joiner (`vae_quilting`: choice and
    boundary cut are one method) is not a variant and is ranked."""
    ex = getattr(cfg, "rank_exclude", None)
    if ex is None:
        import marathonts.bench.methods  # noqa: F401  (registers the built-in methods)

        spec = {m: R.methods.get(m) for m in methods if m in R.methods}
        ex = []
        if not getattr(cfg, "smooth_everywhere", False):
            plain = {(s.pool, s.assembler) for s in spec.values() if not s.joiner}
            ex += [m for m, s in spec.items() if s.joiner and (s.pool, s.assembler) in plain]
    return [m for m in methods if m in set(ex)]


def leaderboard_methods(T: dict, cfg) -> list[str]:
    """The ranked methods: every method of the tables (`ranked_methods`) except `not_ranked`."""
    methods = ranked_methods(T, cfg)
    out = set(not_ranked(cfg, methods))
    return [m for m in methods if m not in out]


def build(T: dict, cfg, methods=None, n_boot: int = 1000) -> dict:
    """Every table of the leaderboard (see the module docstring)."""
    R.load_builtins()
    methods = methods or leaderboard_methods(T, cfg)
    k = len(methods)
    parts = [fidelity_rows(T["fidelity"], methods, cfg.fidelity_ref) if len(T.get("fidelity", [])) else None,
             utility_rows(T["utility"], methods) if len(T.get("utility", [])) else None,
             cost_rows(T.get("timing"), methods)]
    L = pd.concat([p for p in parts if p is not None and len(p)], ignore_index=True)
    L = rank_rows(L, k)
    G, C = aggregate(L)
    TH = theme_rows(L, cfg.fidelity_ref)
    if len(TH):
        _, Cth = aggregate(TH)
        C = C.join(Cth, how="outer")
    # utility per model (stability between models only)
    U = L[L["agg"] & L["criterion"].str.startswith("utility:")]
    Cm = (U.groupby(["criterion", "slice", "model", "group", *KEYS])["rank"].mean()
          .groupby(["criterion", "slice", "model", *KEYS]).mean().reset_index()) if len(U) else pd.DataFrame()
    if len(Cm):
        Cm["col"] = Cm["criterion"] + "@" + Cm["slice"] + "|" + Cm["model"]
        Cm = Cm.pivot_table(index=KEYS, columns="col", values="rank")
    summ = {}
    for k, d in RANKINGS.items():
        summ[f"ranking:{k}"] = summarize(rank_of(C, d["domains"]), n_boot)
        summ[f"with_cost:{k}"] = summarize(rank_of(C, {**d["domains"], **COST_DOMAIN}), n_boot)
    # core rankings: the same leaves and ranks, fidelity restricted to the core metrics
    core = L["agg"] & (~L["criterion"].str.startswith("fidelity:")
                       | L["leaf"].map(lambda u: split_ref(u, cfg.fidelity_ref)[0] in CORE_FIDELITY))
    _, C_core = aggregate(L[core])
    for k, d in CORE_RANKINGS.items():
        summ[f"ranking:{k}"] = summarize(rank_of(C_core, d["domains"]), n_boot)
    for name, d in DOMAINS.items():
        summ[f"domain:{name}"] = summarize(rank_of(C, d), n_boot)
    for c in C.columns:
        summ[c] = summarize(C[c].dropna(), n_boot)
    tests = pd.DataFrame([dict(column=c, p_friedman=s.attrs.get("p_friedman"), nemenyi_cd=s.attrs.get("nemenyi_cd"),
                               n_blocks=s.attrs.get("n_blocks"), n_methods_friedman=s.attrs.get("n_methods_friedman"),
                               best=s.index[0] if len(s) else None)
                          for c, s in summ.items() if len(s)])
    rankings = {k: t.assign(family=[family(m) for m in t.index])[["family", *t.columns]]
                for k in RANKINGS if len(t := summ[f"ranking:{k}"])}
    main = ranking_table(rankings, methods)
    rankings_core = {k: t.assign(family=[family(m) for m in t.index])[["family", *t.columns]]
                     for k in CORE_RANKINGS if len(t := summ[f"ranking:{k}"])}
    main_core = ranking_table(rankings_core, methods)
    avg = pd.DataFrame({c: s["avg_rank"] for c, s in summ.items() if len(s)})
    avg_g = G.groupby(level=["dataset", "method"]).mean().groupby(level="method").mean()
    avg_all = pd.concat([avg, Cm.groupby(level=["dataset", "method"]).mean().groupby(level="method").mean()]
                        if len(Cm) else [avg], axis=1)
    leaves = (L.groupby(["criterion", "group", "slice", "leaf", "dataset", "method"])["rank"].mean()
              .groupby(["criterion", "group", "slice", "leaf", "method"]).agg(["mean", "count"])
              .rename(columns={"mean": "avg_rank", "count": "n_datasets"}).reset_index())
    # magnitudes next to the ranks: median transfer ratio (utility), median raw value (cost)
    from .catalog import transfer_ratio

    tr = pd.DataFrame()
    if len(T.get("utility", [])):
        Rt = transfer_ratio(utility_long(T["utility"]))
        Rt = Rt[Rt["method"].isin(methods)]
        Rt["criterion"] = "utility:" + Rt["task"].map(dict(zip(T["utility"]["task"], T["utility"]["task_kind"]))).map(
            lambda k_: UT_CRITERIA.get(k_, k_))
        common = set(map(tuple, L.loc[L["agg"] & L["criterion"].str.startswith("utility:"), ["criterion", "model"]]
                         .drop_duplicates().to_numpy()))       # the models of the criteria, as in the ranks
        Rt = Rt[[(c, m) in common for c, m in zip(Rt["criterion"], Rt["model"])]]
        tr = Rt.groupby(["method", "criterion", "split"])["ratio"].median().unstack(["criterion", "split"])
        tr.columns = [f"{c}@{s}" for c, s in tr.columns]
    cost = (T["timing"][T["timing"]["method"].isin(methods)].groupby("method")["total_wall_s"].median()
            if len(T.get("timing", [])) and "total_wall_s" in T["timing"] else pd.Series(dtype=float))
    with_cost = {}
    for k, t in rankings.items():                    # quality rank, rank with cost, time, Pareto front
        w = t[["family", "avg_rank"]].copy()
        if len(summ[f"with_cost:{k}"]):
            w["rank_with_cost"] = summ[f"with_cost:{k}"]["avg_rank"].reindex(w.index)
        w["median_time_s"] = cost.reindex(w.index)
        w["pareto"] = pareto_front(w["avg_rank"], w["median_time_s"])
        with_cost[k] = w.sort_values("median_time_s")
    weights = {k: weight_sensitivity(criterion_means(C, d["domains"]).groupby(level=["dataset", "method"]).mean()
                                     .groupby(level="method").mean(), d["domains"]) for k, d in RANKINGS.items()}
    out = dict(rows=L, groups=G, criteria=C, main=main, rankings=rankings, with_cost=with_cost, summaries=summ,
               tests=tests, avg_by_column=avg, avg_by_group=avg_g, leaves=leaves, transfer_ratio=tr,
               kendall=kendall_matrix(avg), stability=stability_pairs(avg_all), weights=weights,
               main_core=main_core, rankings_core=rankings_core)
    out["not_ranked"] = [m for m in ranked_methods(T, cfg) if m not in methods]
    out["anchors"] = anchor_check(T, cfg)
    out["normalized"], out["normalized_summary"] = normalized_scores(T, cfg, methods)
    out["twin"] = twin_check(T, cfg, methods, n_boot)
    out["n_boot"] = n_boot
    return out


def pareto_front(rank: pd.Series, time: pd.Series) -> pd.Series:
    """True: no other method has a time and a rank both lower or equal, one of them strictly lower;
    a method without timing is not on the front."""
    ok = time.notna()
    r, t = rank[ok], time[ok]
    on = {m: not ((t <= t[m]) & (r <= r[m]) & ((t < t[m]) | (r < r[m]))).any() for m in r.index}
    return pd.Series(on, dtype=bool).reindex(rank.index, fill_value=False)


def ranking_table(rankings: dict, methods) -> pd.DataFrame:
    """Methods × rankings: average rank, P(first) and tier in each ranking (`RANKINGS`), methods in the
    order of family, then name; `first_in` — the rankings a method is first in."""
    cols = {}
    for k, t in rankings.items():
        cols[f"{k}:rank"] = t["avg_rank"]
        cols[f"{k}:p_first"] = t["p_first"]
        cols[f"{k}:tier"] = t["tier_wilcoxon"]
    idx = sorted({m for t in rankings.values() for m in t.index} or set(methods), key=lambda m: (family(m), m))
    out = pd.DataFrame(cols, index=idx) if cols else pd.DataFrame(index=idx)
    out.insert(0, "family", [family(m) for m in idx])
    best = {k: t.index[0] for k, t in rankings.items()}
    out["first_in"] = [", ".join(k for k, b in best.items() if b == m) for m in out.index]
    return out


def twin_check(T: dict, cfg, methods, n_boot: int) -> pd.DataFrame:
    """The noise pair ranked together with every method: in every criterion the two random paths
    must not differ — two-sided Wilcoxon over datasets of their rank difference, Holm over the
    criteria (the Nemenyi CD, much wider, only for reference)."""
    a, b = tuple(cfg.noise_pair)
    if a not in methods:
        return pd.DataFrame()
    m2 = list(methods) + [b]
    parts = [fidelity_rows(T["fidelity"], m2, cfg.fidelity_ref) if len(T.get("fidelity", [])) else None,
             utility_rows(T["utility"], m2) if len(T.get("utility", [])) else None]
    L = pd.concat([p for p in parts if p is not None and len(p)], ignore_index=True)
    if b not in set(L["method"]):
        return pd.DataFrame()
    _, C = aggregate(rank_rows(L, len(m2)))
    rows = []
    for c in C.columns:
        D = C[c].dropna().unstack("method").groupby(level="dataset").mean()
        if a not in D or b not in D:
            continue
        d = (D[a] - D[b]).dropna()
        _, _, cd = S.friedman_nemenyi(-D)
        rows.append(dict(column=c, rank_a=float(D[a].mean()), rank_b=float(D[b].mean()), n_datasets=len(d),
                         mean_diff=float(d.mean()) if len(d) else np.nan, p_two_sided=S.wilcoxon(d.to_numpy()),
                         nemenyi_cd=cd))
    t = pd.DataFrame(rows)
    if len(t):
        t["p_holm"] = S.holm(t["p_two_sided"].to_numpy())
        t["indistinguishable"] = t["p_holm"].fillna(1.0) >= cfg.alpha
    return t


# ─────────────────────── output ────────────────────────────────────────────
def _fmt(x, nd=2):
    return "" if pd.isna(x) else (f"{x:.{nd}f}" if isinstance(x, (float, np.floating)) else str(x))


def _md(df: pd.DataFrame, index_name: str = "method", nd: int = 2) -> str:
    if df is None or not len(df):
        return "_no data_\n"
    d = df.reset_index().rename(columns={"index": index_name})
    esc = lambda x: str(x).replace("|", "\\|")      # column ids `…|linear` would split the cells
    head = "| " + " | ".join(map(esc, d.columns)) + " |\n|" + "---|" * d.shape[1] + "\n"
    return head + "\n".join("| " + " | ".join(esc(_fmt(v, nd)) for v in r) + " |" for r in d.itertuples(index=False)) + "\n"


# what every column of the leaderboard tables means (`column_doc`)
COLUMN_DOC = {
    "method": "method id",
    "family": "method family: long-series generator, random selection, optimised selection, seam processing "
              "(a joiner on a stitcher that also runs without it; joiner in brackets)",
    "avg_rank": "mean rank over datasets (seeds averaged within a dataset); 1 = best",
    "ci_lo": "lower bound of the 95% bootstrap interval of avg_rank",
    "ci_hi": "upper bound of the 95% bootstrap interval of avg_rank",
    "p_first": "share of bootstrap samples in which the method has the lowest avg_rank",
    "p_top3": "share of bootstrap samples in which the method is among the three lowest",
    "n_datasets": "number of datasets in which the method is ranked",
    "friedman_rank": "mean Friedman rank over datasets",
    "top_tier": "True — Friedman rank within the Nemenyi critical difference of the best (reference only)",
    "p_worse_than_best_holm": "p-value of the one-sided Wilcoxon test over datasets \"worse than the first "
                              "method\", Holm correction; empty for the first method",
    "tier_wilcoxon": "True — not significantly worse than the first method (p_worse_than_best_holm ≥ 0.05)",
    "rank_with_cost": "avg_rank of the same ranking with cost (total time, peak memory) as a third domain of "
                      "equal weight",
    "median_time_s": "median total wall time of one series (training + generation), seconds",
    "pareto": "True — no other method has both a lower-or-equal avg_rank and a lower-or-equal median_time_s "
              "(one of them strictly lower); False otherwise or without timing",
    "column": "the ranked column (ranking, domain, criterion@slice)",
    "p_friedman": "p-value of the Friedman test (blocks = datasets)",
    "nemenyi_cd": "Nemenyi critical difference of Friedman ranks",
    "n_blocks": "number of datasets in the Friedman test (complete blocks; a method missing on a dataset is left "
                "out of the test, or the dataset is — whichever keeps more cells)",
    "n_methods_friedman": "number of methods in the Friedman test",
    "best": "method with the lowest avg_rank in the column",
    "count": "number of compared pairs of rankings",
    "mean": "mean Kendall τ (1 — the same order, 0 — unrelated, −1 — reversed)",
    "min": "lowest Kendall τ", "max": "highest Kendall τ",
    "comparison": "the two kinds of slices compared",
    "criterion": "the criterion whose two slices are compared",
    "tau": "Kendall τ between the method orders of the two slices",
    "equal_weights_rank": "score of the method with equal criterion weights (lower = better)",
    "rank_a": "mean rank of the first path", "rank_b": "mean rank of the second path",
    "mean_diff": "mean rank difference first − second over datasets",
    "p_two_sided": "p-value of the two-sided Wilcoxon test of the difference",
    "p_holm": "p_two_sided after Holm correction over the criteria",
    "indistinguishable": "True — p_holm ≥ α (the two paths do not differ)",
    "leaf": "metric (fidelity: `<metric>@<reference>`, val without suffix; utility: `task|model|metric@split`)",
    "kind": "fidelity or utility",
    "core": "True — the leaf belongs to the core metric set",
    "ratio_all": "median over datasets of |real − random assembly| / noise (median |random − twin| over seeds, or the "
                 "between-seed spread of the random path where the twin is not run); "
                 "all seeds",
    "separated_all": "True — ratio_all > 1: the metric tells real data from a random assembly beyond the noise",
    "ratio_even": "ratio on the even seeds", "ratio_odd": "ratio on the odd seeds",
    "separated_even": "ratio_even > 1", "separated_odd": "ratio_odd > 1",
    "flip": "True — the verdict differs between even and odd seeds",
}


def column_doc(df: pd.DataFrame, patterns: dict | None = None) -> str:
    """\"Columns:\" list for a table: the columns of `COLUMN_DOC` present in it (with its index name), then
    `patterns` — {name or name pattern: meaning}, for the columns named by data (criteria, rankings) and
    for a column whose meaning differs in this table."""
    if df is None or not len(df):
        return ""
    doc = {**COLUMN_DOC, **(patterns or {})}
    idx = [df.index.name] if df.index.name else [] if isinstance(df.index, pd.RangeIndex) else ["method"]
    names = list(dict.fromkeys(idx + [str(c) for c in df.columns]))
    items = [f"`{c}` — {doc[c]}" for c in names if c in doc]
    items += [f"`{k}` — {v}" for k, v in (patterns or {}).items() if k not in names]
    return "Columns: " + "; ".join(items) + ".\n" if items else ""


def core_section(res: dict, folder: str = "leaderboard") -> list[str]:
    """LEADERBOARD.md: the core-metric rankings, the normalised scores and the anchor check."""
    rank_cols = ["family", "avg_rank", "ci_lo", "ci_hi", "p_first", "p_top3", "p_worse_than_best_holm", "tier_wilcoxon"]
    L = []
    if len(res.get("main_core", [])):
        L += ["## Core-metric rankings", "",
              "The four rankings with the fidelity domain restricted to the core metric set — one or two canonical "
              "metrics per criterion, fixed in advance by what they measure: "
              f"{_CORE_LIST}. Utility is the same as in the four rankings. The full rankings above use every metric.", "",
              column_doc(res["main_core"], {"<ranking>:rank": "avg_rank of the method in that core ranking (1 = best)",
                                            "<ranking>:p_first": "share of bootstrap samples in which the method is first",
                                            "<ranking>:tier": "True — not significantly worse than the first method "
                                                              "(one-sided Wilcoxon over datasets, Holm, α = 0.05)",
                                            "first_in": "the core rankings in which the method has the lowest avg_rank"}),
              "Rows: methods ordered by family, then name.", "", _md(res["main_core"]), ""]
        for k, d in CORE_RANKINGS.items():
            t = res["rankings_core"].get(k)
            if t is None or not len(t):
                continue
            a_ = res["summaries"][f"ranking:{k}"].attrs
            L += [f"### {d['title']} (`{k}`)", "",
                  f"Friedman p = {_fmt(a_.get('p_friedman'), 3)}, Nemenyi CD = {_fmt(a_.get('nemenyi_cd'))}, "
                  f"datasets × methods in the test = {a_.get('n_blocks')} × {a_.get('n_methods_friedman')}. Rows: sorted by avg_rank.", "", _md(t[rank_cols]), ""]
    ns = res.get("normalized_summary", pd.DataFrame())
    if len(ns):
        t = ns.copy()
        t.insert(0, "family", [family(m) for m in t.index])
        L += ["## Normalised scores on the core metrics", "",
              "Composition: every core metric on the scale random assembly (`noise_pair[0]`) = 0, real data = 1: "
              "(x − x_random) / (x_real − x_random); above 1 — closer to the reference than the real data, below 0 — "
              "worse than a random assembly. Fidelity against val and train, on the series cut to the length of the "
              "real reference (seed 0); utility — TSTR against TRTR, seeds averaged, models fitted on every task. "
              "A dataset is left out of a metric when its anchors differ by no more than the noise. Median over the "
              "metrics of a criterion within a dataset, then over datasets. Not used in the rankings: the size of "
              f"the effect next to them. Per metric and dataset — `{folder}/normalized.parquet`.", "",
              column_doc(t, {"fidelity": "median normalised score over every core fidelity metric",
                             "utility": "median normalised score over every utility cell",
                             "<criterion>": "median normalised score over the core metrics of the criterion"}),
              "Rows: methods ordered by family, then name.", "", _md(t), ""]
    an = res.get("anchors", pd.DataFrame())
    if len(an):
        def counts(d):
            return dict(n=len(d), separated=int(d["separated_all"].sum()),
                        separated_even=int(d["separated_even"].sum()), separated_odd=int(d["separated_odd"].sum()),
                        flips=int(d["flip"].sum()))
        s = pd.DataFrame({"every fidelity metric": counts(an[an["kind"] == "fidelity"]),
                          "core fidelity metrics": counts(an[(an["kind"] == "fidelity") & an["core"]]),
                          "utility cells": counts(an[an["kind"] == "utility"])}).T
        core = an[(an["kind"] == "fidelity") & an["core"]].set_index("leaf").drop(columns=["kind", "core"])
        L += ["## Anchor check: does a metric tell real data from a random assembly", "",
              "Composition: per dataset, gap = |real − random assembly| (assembly averaged over seeds) and noise = "
              "median over seeds of |random − its twin| (without the twin, as in min: the between-seed spread of the "
              "random path); ratio = gap / noise, median over datasets; separated — "
              "ratio > 1. The competing methods are not used, so the check does not depend on who wins. Computed on "
              "all seeds and separately on even and odd seeds: a flip — the verdict differs between the two halves. "
              "Fidelity against val and train; `real` is a piece of OOT, shorter than the synthetic series, so for "
              f"distance metrics the gap is underestimated (conservative). Every leaf — `{folder}/anchor_check.parquet`.", "",
              "Columns: `n` — number of leaves; `separated` — separated on all seeds; `separated_even`, "
              "`separated_odd` — on each half; `flips` — leaves whose verdict differs between the halves.", "",
              _md(s, "leaves"), "", "### Core fidelity metrics", "", column_doc(core), _md(core, "leaf"), ""]
    return L


def write(res: dict, cfg, out: Path, report_dir: Path | None = None) -> Path:
    """Parquet tables to `out`, `LEADERBOARD.md` to `report_dir` (default `<out>/../reports`)."""
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    report_dir = Path(report_dir) if report_dir else out.parent / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    folder = out.name
    from marathonts.bench.storage import write_table

    def save(df, name, index=True):
        if df is None or not len(df):
            return
        d = df.reset_index() if index else df.copy()
        d.columns = [str(c) for c in d.columns]
        for c in d.columns:
            if d[c].dtype == object:
                d[c] = d[c].map(lambda v: v if v is None or isinstance(v, (str, float, int, bool)) else str(v))
        write_table(d, out / f"{name}.parquet")

    save(res["main"], "rankings_summary")
    save(pd.concat(res["rankings"], names=["ranking", "method"]) if res["rankings"] else None, "rankings")
    save(pd.concat(res["with_cost"], names=["ranking", "method"]) if res["with_cost"] else None, "rankings_cost")
    save(pd.concat({c: s for c, s in res["summaries"].items() if len(s)}, names=["column", "method"]), "by_column")
    save(res["avg_by_group"], "by_group")
    save(res["leaves"], "leaves", index=False)
    save(res["tests"], "tests", index=False)
    save(res["kendall"], "kendall")
    save(res["stability"], "stability", index=False)
    w = {k: v for k, v in res["weights"].items() if len(v)}
    save(pd.concat(w, names=["ranking", "method"]) if w else None, "weights")
    save(res["transfer_ratio"], "transfer_ratio")
    save(res["twin"], "twin", index=False)
    save(res["main_core"], "rankings_core_summary")
    save(pd.concat(res["rankings_core"], names=["ranking", "method"]) if res["rankings_core"] else None,
         "rankings_core")
    save(res["normalized"], "normalized", index=False)
    save(res["normalized_summary"], "normalized_summary")
    save(res["anchors"], "anchor_check", index=False)

    main, avg = res["main"], res["avg_by_column"]
    order = main.index
    ds = sorted(res["rows"]["dataset"].unique())
    seeds = sorted(res["rows"]["seed"].unique())
    rank_cols = ["family", "avg_rank", "ci_lo", "ci_hi", "p_first", "p_top3", "p_worse_than_best_holm", "tier_wilcoxon"]
    L = ["# Method ranking", "",
         f"Methods: {len(main)}. Datasets ({len(ds)}): {', '.join(ds)}. Seeds: {len(seeds)}.", "",
         *([f"Not ranked (they take part in every research question and in the case study): "
            f"{', '.join(f'`{m}`' for m in res['not_ranked'])}"
            + ("" if getattr(cfg, "rank_exclude", None) is not None else
               ("" if getattr(cfg, "smooth_everywhere", False) else
               " — the seam-processing variants: they exist for some stitchers only (`smooth_paths`), "
               "so those would enter the ranking several times and every other stitcher once"))
            + " (`Config.rank_exclude`, `--rank-exclude`; `smooth_paths=\"all\"` runs every seam processing over "
              "every stitcher and ranks them).", ""] if res.get("not_ranked") else []),
         *(["Left out of the analysis: " + "; ".join("`%s` on %s" % (m, ", ".join(ds)) for m, ds in cfg.leaked.items()) + " "
            "— the dataset, or the same object at other stations, years or resolution, is in the method's "
            "training corpus, so its results there are not out-of-sample "
            "(`Config.leaked`; DATASETS.md).", ""] if getattr(cfg, "leaked", None) else []),
         "Procedure. Within every leaf (one fidelity metric against one real reference, or one utility task × "
         "model × test split × metric) the methods are ranked per (dataset, seed); rank 1 = the best value. "
         "Ranks are averaged leaf → metric group → criterion → domain with equal weights at every level; a "
         "ranking is the mean of its domains with equal weights. The rank of a method in a ranking is the mean "
         "over datasets (seeds averaged within a dataset). Uncertainty: two-level bootstrap (datasets, then "
         f"seeds within a dataset), {res.get('n_boot', 1000)} samples.", "",
         "## The four rankings", "",
         "Fidelity criteria in every ranking: " + _FID_LIST + ". Not part of any of the four rankings: privacy "
         "(F10; its own table below), time and memory (cost tables below), the thematic slices.", "",
         *[f"- `{k}` — **{d['title']}**. {d['text']}" for k, d in RANKINGS.items()], "",
         "### Summary of the four rankings", "",
         column_doc(main, {"<ranking>:rank": "avg_rank of the method in that ranking (1 = best)",
                        "<ranking>:p_first": "share of bootstrap samples in which the method is first in that ranking",
                        "<ranking>:tier": "True — not significantly worse than the first method of that ranking "
                                          "(one-sided Wilcoxon over datasets, Holm, α = 0.05)",
                        "first_in": "the rankings in which the method has the lowest avg_rank"}),
         "Rows: methods ordered by family, then name.", "",
         _md(main), ""]
    for i, (k, d) in enumerate(RANKINGS.items(), 1):
        t = res["rankings"].get(k)
        if t is None or not len(t):
            continue
        a_ = res["summaries"][f"ranking:{k}"].attrs
        L += [f"## Ranking {i}. {d['title']} (`{k}`)", "", f"Composition: {d['text']}", "",
              f"Friedman p = {_fmt(a_.get('p_friedman'), 3)}, Nemenyi CD = {_fmt(a_.get('nemenyi_cd'))}, "
              f"datasets × methods in the test = {a_.get('n_blocks')} × {a_.get('n_methods_friedman')}.", "",
              column_doc(t[rank_cols]), "Rows: sorted by avg_rank.", "", _md(t[rank_cols]), ""]
    L += core_section(res, folder)
    pv = res["summaries"].get("fidelity:privacy@—", pd.DataFrame())
    if len(pv):
        cols = [c for c in rank_cols if c in pv]
        L += ["## Privacy (F10, memorisation)", "",
              "Composition: F10.1 DCR — distance from a synthetic window to the nearest train window, relative to "
              "the same distance for held-out windows (|log ratio|); F10.2 — share of synthetic windows closer to "
              "train than the 5th percentile of real-to-real distances. Computed once, against train. Not part of "
              "the four rankings.", "",
              column_doc(pv[[c for c in cols if c != "family"]]), "Rows: sorted by avg_rank.", "",
              _md(pv[[c for c in cols if c != "family"]]), ""]
    if res["with_cost"]:
        L += ["## Cost next to the rankings", "",
              "Composition: for each of the four rankings, its quality rank, the same ranking with cost added as a "
              "third domain of equal weight (cost: total wall time of a series and peak memory), and the median "
              "total time. Times from different hardware are not comparable.", ""]
        for k, t in res["with_cost"].items():
            L += [f"### `{k}` — {RANKINGS[k]['title']}", "", column_doc(t), "Rows: sorted by median_time_s.", "",
                  _md(t), ""]
    L += ["## Ranks by criterion and slice", "",
          "Composition: the mean rank of every method in one criterion against one reference or on one test "
          "split. The four rankings are built from the fidelity columns against train / val / oot and the utility "
          "columns; `@—` (privacy) and cost are not part of them.", ""]
    cols = [c for c in avg.columns if c.startswith("domain:")]
    if cols:
        t = avg.reindex(order)[cols].rename(columns=lambda c: c.replace("domain:", ""))
        L += ["### Domains", "",
              "Composition: one domain alone, the mean of its criteria (fidelity without privacy).", "",
              column_doc(t, {"fidelity@<ref>": "mean rank over the fidelity criteria against train / val / oot; "
                                            "@all — against all three",
                          "utility@<split>": "mean rank over the utility criteria tested on val / oot; @all — both"}),
              _md(t), ""]
    for pref, title, desc in (
            ("fidelity:", "Fidelity", "fidelity criterion against train / val / oot; `@—` — computed once "
                                      "(privacy)"),
            ("utility:", "Utility", "TSTR utility criterion (classification, regression) tested on val / oot"),
            ("cost", "Cost", "cost slice: total — total wall time of a series, training — training of the "
                             "generator (a shared generator is charged to every method and seed using it), "
                             "generation — sampling + assembly of a new series, memory — peak GPU memory and RSS "
                             "increase; lower = better rank")):
        cols = [c for c in avg.columns if c.startswith(pref)]
        if cols:
            t = avg.reindex(order)[cols].rename(columns=lambda c: c.replace("fidelity:", "").replace("utility:", ""))
            L += [f"### {title}", "", column_doc(t, {"<criterion>@<slice>": f"mean rank of the method: {desc}"}),
                  _md(t), ""]
    for th in THEMES:
        cols = [c for c in avg.columns if c.startswith(f"theme:{th}:")]
        if cols:
            title = {"class_balance": "Class balance", "extremes": "Outliers and extremes"}.get(th, th)
            t = avg.reindex(order)[cols].rename(columns=lambda c: c.replace(f"theme:{th}:", ""))
            L += [f"### Theme: {title}", "",
                  "Composition. " + {
                      "class_balance": "Fidelity: F8.1 and F11 (class shares of every classification task, rare "
                                       "events separately, multiclass, loss of the minority class). Utility: ECE "
                                       "of the classifiers.",
                      "extremes": "Fidelity: tail quantiles and the Hill index (F1.5, F1.10), kurtosis (F1.6), "
                                  "large jumps (F2.4), excursion durations (F7.4), F12 (frequency and size of "
                                  "exceedances of the real 0.5/99.5%, local spikes, block maxima and minima). "
                                  "Utility: regression error on the extreme 10% of the target and PR AUC of rare "
                                  "events."}.get(th, "") + " Not part of the rankings.", "",
                  column_doc(t, {"fidelity@<ref>": "mean rank over the theme's fidelity metrics against that reference",
                              "utility@<split>": "mean rank over the theme's utility metrics on that test split"}),
                  _md(t), ""]
    L += ["### Tests by column", "", column_doc(res["tests"]), _md(res["tests"].set_index("column"), "column", 3), ""]
    if len(res["transfer_ratio"]):
        t = res["transfer_ratio"].reindex(order)
        L += ["## Effect size: median transfer ratio", "",
              column_doc(t, {"<criterion>@<split>": "median over datasets, seeds, tasks and models of TSTR / TRTR "
                                                 "(quality of a model trained on synthetic data / trained on real "
                                                 "data, both tested on real data); 1 = as on real data"}),
              _md(t), ""]
    st = res["stability"]
    if len(st):
        d1 = st.groupby("comparison")["tau"].describe()[["count", "mean", "min", "max"]]
        d2 = st[st["comparison"] != "fidelity ↔ utility"]
        L += ["## Ranking stability (Kendall τ between the rankings of slices)", "",
              column_doc(d1, {"comparison": "pair of slice types compared (e.g. train ↔ val)"}),
              _md(d1, "comparison"), "", column_doc(d2), _md(d2.set_index("comparison"), "comparison"), ""]
    for k, w in res["weights"].items():
        if len(w):
            L += [f"## Sensitivity to the criterion weights: `{k}`", "",
                  f"Composition: the ranking `{k}` under 2000 random criterion weights (Dirichlet(1) within each "
                  f"domain). Median Kendall τ with equal weighting: {_fmt(w.attrs.get('median_tau_vs_equal'))}.", "",
                  column_doc(w, {"p_first": "share of the weight draws in which the method is first",
                              "p_top3": "share of the weight draws in which the method is among the three first"}),
                  _md(w), ""]
    if len(res["twin"]):
        L += [f"## Noise check: {cfg.noise_pair[0]} vs {cfg.noise_pair[1]}", "",
              "Composition: two equally random paths on the same pool, ranked together with every method; "
              "two-sided Wilcoxon over datasets of their rank difference, Holm correction over the criteria.", "",
              column_doc(res["twin"]), _md(res["twin"].set_index("column"), "column", 3), ""]
    L += ["## Details", "", f"Tables in `{folder}/`: ranks by metric group and task — `by_group.parquet`, by every "
          "leaf — `leaves.parquet`, full summaries by column with CI — `by_column.parquet` (`ranking:<name>` — the "
          "four rankings, `with_cost:<name>` — with cost, `domain:<name>`, criteria), the rankings — "
          "`rankings.parquet`, their summary — `rankings_summary.parquet`, cost next to them — `rankings_cost.parquet`; "
          "core-metric rankings — `rankings_core.parquet`, `rankings_core_summary.parquet`; normalised scores — "
          "`normalized.parquet`, `normalized_summary.parquet`; anchor check — `anchor_check.parquet`.", ""]
    f = report_dir / "LEADERBOARD.md"
    f.write_text("\n".join(L))
    return f


def main(argv=None):
    import argparse
    import dataclasses

    from .run import _run_config, add_analysis_args, apply_analysis_args, check_tables, load_tables

    ap = argparse.ArgumentParser()
    ap.add_argument("--artifacts-dir")
    ap.add_argument("--profile", choices=["min", "mid", "max"], default="min")
    ap.add_argument("--out", help="default: <artifacts>/leaderboard (report: <artifacts>/reports)")
    ap.add_argument("--n-boot", type=int, default=1000)
    ap.add_argument("--rank-exclude", nargs="*", metavar="METHOD",
                    help="methods left out of the rankings (default: Config.rank_exclude — the seam-processing variants, unless every stitcher has them); no names — rank every method")
    add_analysis_args(ap)
    a = ap.parse_args(argv)
    a.case_method = a.noise_pair = None
    cfg = apply_analysis_args(_run_config(a), a)
    if a.artifacts_dir:
        cfg = dataclasses.replace(cfg, artifacts_dir=Path(a.artifacts_dir))
    if a.rank_exclude is not None:                   # [] → rank every method
        cfg = dataclasses.replace(cfg, rank_exclude=list(a.rank_exclude))
    T = load_tables(cfg)
    check_tables(T, cfg)
    res = build(T, cfg, n_boot=a.n_boot)
    out = Path(a.out) if a.out else Path(cfg.artifacts_dir) / "leaderboard"
    print(f"leaderboard → {write(res, cfg, out)}")


if __name__ == "__main__":
    main()
