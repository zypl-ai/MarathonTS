"""Research questions RQ0–RQ9 of the benchmark (HYPOTHESES.md §3), posed about every method. The case study of one method (`--case-method`, CS1–CS15) is in `catalog.py`.

RQ0  validity: noise, real-data ceiling, which metrics discriminate methods, redundancy
RQ1  ranking of every method in every slice (`leaderboard.py`)
RQ2  assembly from a window pool vs generators of long series
RQ3  inside assembly: window selection × seam processing (same pool → shared noise)
RQ4  does fidelity predict utility (which metrics, against which reference)
RQ5  gap to real data (TSTR / TRTR), stability over time and model class, decision transfer
RQ6  cost and the quality–cost Pareto front
RQ7  dataset moderators (exploratory)
RQ8  class balance: class shares of every classification task, rare events, their cost in TSTR
RQ9  extremes: tails, outliers, block maxima / minima, their cost for predicting extremes

Each `rq*` function takes the benchmark tables and the config and returns
`{"global": DataFrame, "per_dataset": DataFrame, "extra": dict}` like the case-study functions.
`confirmatory_rq` is the pre-specified family (Holm): `CONFIRMATORY_CELLS`, `CONFIRMATORY_GENERATORS`.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats as sps

from . import engine as E
from . import leaderboard as LB
from . import stats as S
from .catalog import (CALENDAR_VALIDITY, PRIMARY_METRIC, _tstr, _ut_orient, dataset_descriptors,
                      fidelity_long, h0_noise, transfer_ratio, utility_long)

from marathonts.bench import registry as R  # noqa: E402
from marathonts.bench.fidelity import GROUP_OF, ORIENT, split_ref  # noqa: E402

# pre-specified confirmatory cells: (task, model, test split) — one classification, one regression task
CONFIRMATORY_CELLS = (("clf_up_h24_q90", "linear", "oot"), ("reg_h24", "linear", "oot"))
# pre-specified long-series generators of C2: fixed, so a custom long method (compared in RQ2) does not grow the family
from marathonts.bench.config import PRESPECIFIED_LONG as CONFIRMATORY_GENERATORS  # noqa: E402
_LB: dict = {}                       # leaderboard of the current run (built once, shared by RQ1 / RQ5 / RQ6)


# ─────────────────────── shared pieces ─────────────────────────────────────
def leaderboard(T, cfg) -> dict:
    key = id(T)
    if key not in _LB:
        _LB.clear()
        _LB[key] = LB.build(T, cfg, n_boot=max(200, cfg.n_boot // 2))
    return _LB[key]


def _methods(T, cfg) -> list[str]:
    return LB.ranked_methods(T, cfg)


def _empty(**extra):
    return {"global": pd.DataFrame(), "per_dataset": pd.DataFrame(), "extra": dict(extra)}


def fid_units(refs=("val", "oot"), primary="val"):
    """Fidelity units against the given references (calendar validity metrics excluded)."""
    return [u for u in ORIENT if split_ref(u, primary)[1] in refs and split_ref(u, primary)[0] not in CALENDAR_VALIDITY]


def tstr_primary(T) -> pd.DataFrame:
    """TSTR rows of the primary metric of every task (unit = task|model|S|split|metric)."""
    return _tstr(utility_long(T["utility"]))


def pool_grid(methods) -> dict:
    """{(assembler, joiner): method} of the methods sharing the noise pair's pool."""
    import marathonts.bench.methods  # noqa: F401

    a = E.NOISE[0]
    if a not in R.methods:
        return {}
    pool = R.methods.get(a).pool
    out = {}
    for m in methods:
        if m in R.methods:
            s = R.methods.get(m)
            if s.pool == pool and s.assembler not in ("random_b",):
                out[(s.assembler, s.joiner)] = m
    return out


def selection_methods(grid: dict) -> list[str]:
    """Every selection strategy of the pool but the random path: the assemblers run without a joiner, and
    those that only run with one (`quilt_sel` + `quilt`: choice and boundary cut are one method)."""
    plain = {a for (a, j) in grid if j is None}
    return [m for (a, j), m in grid.items() if a != "random" and (j is None or a not in plain)]


def long_methods(methods) -> list[str]:
    import marathonts.bench.methods  # noqa: F401

    return [m for m in methods if m in R.methods and R.methods.get(m).long]


def _compare(long, orient, a, comparators, cfg, margin="pool", adjust="bh", units=None, label=None):
    """`a` against each comparator (d > 0: `a` better) — per dataset over seeds and across datasets,
    the engine's tests and verdicts; margin "pool" = rand vs rand_b (without the twin: seed spread of rand),
    "seed" = the larger of the between-seed spreads of `a` and of the comparator (a generator without
    sampling — TimesFM, Timestral — has none, so its own spread alone would give a zero margin)."""
    if units is not None:
        long = long[long["unit"].isin(units)]
    q = cfg.equivalence_margin_q
    margins = E.seed_margins(long, q, method=a) if margin == "seed" else E.noise_margins(long, q)
    per_all, glob_all = [], []
    for c in comparators:
        pairs = E.paired(long, orient, c, method=a)
        if not len(pairs):
            continue
        if margin == "seed":
            m = margins.merge(E.seed_margins(long, q, method=c), on=["dataset", "unit"], how="outer",
                              suffixes=("_a", "_c"))
            margins_c = m.assign(margin=np.fmax(m["margin_a"], m["margin_c"]))[["dataset", "unit", "margin"]]
        else:
            margins_c = margins
        per, glob = E.summarize(pairs, margins_c, cfg.alpha, cfg.n_boot)
        tag = label or f"{a} vs {c}"
        per["comparison"] = glob["comparison"] = tag
        per["comparator"] = glob["comparator"] = c
        per["method"] = glob["method"] = a
        per_all.append(per)
        glob_all.append(glob)
    return per_all, glob_all


def _contrast(long, orient, cfg, d_rows: pd.DataFrame, label: str):
    """Engine summary of a ready-made contrast `d_rows` (dataset, unit, seed, d — oriented, > 0 = first
    term better) with the pool noise margin."""
    margins = E.noise_margins(long, cfg.equivalence_margin_q)
    per, glob = E.summarize(d_rows, margins, cfg.alpha, cfg.n_boot)
    per["comparison"] = glob["comparison"] = label
    per["comparator"] = glob["comparator"] = label
    return per, glob


def _finish(per_all, glob_all, adjust, cfg):
    gl, pr = [g for g in glob_all if len(g)], [p for p in per_all if len(p)]
    glob = pd.concat(gl, ignore_index=True) if gl else pd.DataFrame()
    per = pd.concat(pr, ignore_index=True) if pr else pd.DataFrame()
    if len(glob):
        glob = E.finalize(glob, adjust, cfg.alpha)
    if len(per) and len(glob):
        per, glob = _per_dataset_adjust(per, glob, adjust, cfg)
    return glob, per


def _per_dataset_adjust(per, glob, adjust, cfg):
    """As `engine.finalize_per_dataset`, keyed by comparison (several methods share a comparator)."""
    per = per.assign(comparator=per["comparison"])
    glob = glob.assign(_c=glob["comparator"], comparator=glob["comparison"])
    per, glob = E.finalize_per_dataset(per, glob, adjust, cfg.alpha)
    return per, glob.assign(comparator=glob.pop("_c"))


def _seed_means(long) -> pd.DataFrame:
    return long.groupby(["dataset", "unit", "method"])["value"].mean().reset_index()


# ─────────────────────── RQ0 validity ──────────────────────────────────────
def rq0_validity(T, cfg):
    """(a) noise: the two random paths are equivalent; (b) ceiling: real OOT against the methods;
    (c) discriminability: does a metric separate the methods (Friedman over methods, blocks =
    datasets, BH) by more than the noise; (d) redundancy: rank correlation between metrics
    and between the references of one metric."""
    base = h0_noise(T, cfg)
    ceiling = base["extra"].get("ceiling_share_real_better", pd.DataFrame())
    flagged = sorted(ceiling.index[ceiling.median(axis=1) < 0.5]) if len(ceiling) else []
    methods = _methods(T, cfg)
    F = fidelity_long(T["fidelity"])
    F = F[F["unit"].isin(fid_units(("train", "val", "oot"), cfg.fidelity_ref)) | F["unit"].map(GROUP_OF).eq("F10_memorisation")]
    U = tstr_primary(T)
    rows = []
    for kind, L in (("fidelity", F), ("utility", U)):
        if not len(L):
            continue
        margins = E.noise_margins(L, cfg.equivalence_margin_q).set_index(["dataset", "unit"])["margin"]
        M = _seed_means(L[L["method"].isin(methods)])
        for u, g in M.groupby("unit"):
            D = S.complete_blocks(g.pivot_table(index="dataset", columns="method", values="value"))
            if len(D) < 3 or D.shape[1] < 3:
                continue
            p = float(sps.friedmanchisquare(*[D[c] for c in D.columns]).pvalue)
            iqr = (D.quantile(0.75, axis=1) - D.quantile(0.25, axis=1))
            mg = margins.reindex(pd.MultiIndex.from_product([D.index, [u]])).to_numpy()
            ratio = np.nanmedian(np.where(mg > 0, iqr.to_numpy() / mg, np.nan)) if np.isfinite(mg).any() else np.nan
            rows.append(dict(unit=u, kind=kind, group=GROUP_OF.get(u, u.split("|")[0]),
                             reference=split_ref(u, cfg.fidelity_ref)[1] if kind == "fidelity" else u.split("|")[3],
                             n_datasets=len(D), n_methods=D.shape[1], p_friedman=p, spread_over_noise=ratio))
    disc = pd.DataFrame(rows)
    if len(disc):
        disc["p_friedman_bh"] = S.bh(disc["p_friedman"].to_numpy())
        disc["discriminative"] = (disc["p_friedman_bh"] < cfg.alpha) & (disc["spread_over_noise"] > 1)
    red, refs = redundancy(F[F["method"].isin(methods)], cfg)
    noise = base["global"]
    return {"global": disc, "per_dataset": base["per_dataset"],
            "extra": {"noise_floor": noise, "ceiling_share_real_better": ceiling,
                      "uninformative_metrics": ", ".join(flagged),
                      "discriminative_share_by_group": disc.groupby(["kind", "group", "reference"])["discriminative"]
                      .mean().unstack("reference").round(2) if len(disc) else pd.DataFrame(),
                      "redundant_pairs": red, "reference_agreement": refs}}


def redundancy(F: pd.DataFrame, cfg, thr: float = 0.9):
    """Spearman ρ between metrics over (dataset, method) after ranking the methods within a dataset:
    metric pairs at the primary reference with |ρ| ≥ thr, and per metric ρ between its references."""
    M = _seed_means(F)
    M["r"] = M.groupby(["dataset", "unit"])["value"].rank() * M["unit"].map(ORIENT)
    W = M.pivot_table(index=["dataset", "method"], columns="unit", values="r")
    prim = [u for u in W.columns if "@" not in u]
    C = W[prim].corr(method="spearman")
    iu = np.triu_indices(len(prim), 1)
    pairs = pd.DataFrame({"metric_a": np.array(prim)[iu[0]], "metric_b": np.array(prim)[iu[1]],
                          "rho": C.to_numpy()[iu]}).dropna()
    pairs = pairs[pairs["rho"].abs() >= thr].sort_values("rho", key=np.abs, ascending=False)
    rows = []
    for u in prim:
        r = dict(metric=u)
        for ref in ("train", "oot"):
            v = f"{u}@{ref}"
            if v in W:
                j = W[[u, v]].dropna()
                r[f"rho_val_{ref}"] = float(j[u].corr(j[v], method="spearman")) if len(j) > 3 else np.nan
        rows.append(r)
    return pairs.reset_index(drop=True), pd.DataFrame(rows)


# ─────────────────────── RQ1 ranking ───────────────────────────────────────
def rq1_ranking(T, cfg):
    lb = leaderboard(T, cfg)
    cols = ["family", "avg_rank", "ci_lo", "ci_hi", "p_first", "p_top3", "p_worse_than_best_holm", "tier_wilcoxon"]
    # the leaderboard of each of the four rankings (`leaderboard.RANKINGS`) and their summary
    rk = {f"ranking_{k}": t[cols] for k, t in lb["rankings"].items()}
    rk.update({f"ranking_{k}": t[cols] for k, t in lb["rankings_core"].items()})
    return {"global": lb["tests"], "per_dataset": pd.DataFrame(),
            "extra": {**rk, "rankings": lb["main"], "rankings_core": lb["main_core"],
                      "normalized_scores": lb["normalized_summary"], "anchor_check": lb["anchors"],
                      "note": "full ranking by slice — reports/LEADERBOARD.md"}}


# ─────────────────────── RQ2 assembly vs long-series generators ────────────
ASSEMBLY_MEDIAN = "assembly_median"


def _with_assembly_median(L, methods):
    grid = pool_grid(methods)
    asm = [m for m in grid.values()]
    med = L[L["method"].isin(asm)].groupby(["dataset", "seed", "unit"])["value"].median().reset_index()
    return pd.concat([L, med.assign(method=ASSEMBLY_MEDIAN)], ignore_index=True)


def rq2_assembly_vs_long(T, cfg):
    """Each generator of long series against the window-pool assembly: the simplest assembly (the
    random path, `noise_pair[0]`) and the median of every assembly method of the pool, per seed.
    Utility: TSTR, primary metric of every task × model × split; fidelity: every metric against val
    and OOT. Margin: the larger of the between-seed spreads of the long-series generator (independently
    trained) and of the assembly it is compared with. d > 0:
    the long-series generator is better."""
    methods = _methods(T, cfg)
    gens = long_methods(methods)
    if not gens:
        return _empty(note="no long-series generators in the tables")
    per_all, glob_all = [], []
    for kind, L, orient in (("utility", tstr_primary(T), None), ("fidelity", fidelity_long(T["fidelity"]), ORIENT)):
        if kind == "fidelity":
            L = L[L["unit"].isin(fid_units(("val", "oot"), cfg.fidelity_ref))]
        if not len(L):
            continue
        L = _with_assembly_median(L, methods)
        o = orient or _ut_orient(L)
        for g in gens:
            p, gl = _compare(L, o, g, [E.NOISE[0], ASSEMBLY_MEDIAN], cfg, margin="seed")
            for x in (*p, *gl):
                x["kind"] = kind
            per_all += p
            glob_all += gl
    glob, per = _finish(per_all, glob_all, "bh", cfg)
    return {"global": glob, "per_dataset": per, "extra": {}}


# ─────────────────────── RQ3 selection × seam processing ───────────────────
def _wide(L):
    return L.pivot_table(index=["dataset", "seed", "unit"], columns="method", values="value")


def _d(W, orient, a_cols, b_cols):
    """Oriented mean(a) − mean(b) per (dataset, seed, unit)."""
    d = W[a_cols].mean(axis=1, skipna=False) - W[b_cols].mean(axis=1, skipna=False)
    d = d * d.index.get_level_values("unit").map(lambda u: orient.get(u, 1.0)).to_numpy()
    return d.dropna().rename("d").reset_index()


def rq3_assembly_factors(T, cfg):
    """On one pool (shared noise): (a) every selection strategy against the random path;
    (b) every seam processing against no processing, on each path; (c) main effect of each joiner,
    averaged over the assemblers run with every joiner (min, mid: the zseries stitcher; max: every
    stitcher but the random path, which has no seam processing). d > 0: the first term is better."""
    methods = _methods(T, cfg)
    grid = pool_grid(methods)
    if not grid:
        return _empty(note="no pool methods")
    rand = grid.get(("random", None))
    joiners = sorted({j for (_, j) in grid if j})
    full = [a for a in sorted({a for (a, _) in grid}) if all((a, j) in grid for j in [None, *joiners])]
    per_all, glob_all = [], []
    for kind, L, orient in (("utility", tstr_primary(T), None), ("fidelity", fidelity_long(T["fidelity"]), ORIENT)):
        if kind == "fidelity":
            L = L[L["unit"].isin(fid_units(("val", "oot"), cfg.fidelity_ref))]
        if not len(L):
            continue
        o = orient or _ut_orient(L)
        parts_p, parts_g = [], []
        # (a) selection strategies vs random
        for m in selection_methods(grid):
            p, g = _compare(L, o, m, [rand], cfg, label=f"selection: {m} vs {rand}")
            parts_p += p
            parts_g += g
        # (b) seam processing vs none, on each path
        for (a, j), m in grid.items():
            if j and (a, None) in grid:
                p, g = _compare(L, o, m, [grid[(a, None)]], cfg, label=f"seams: {m} vs {grid[(a, None)]}")
                parts_p += p
                parts_g += g
        # (c) main effect of each joiner over the assemblers that have every joiner
        if full and joiners:
            W = _wide(L)
            for j in joiners:
                A = [grid[(a, j)] for a in full]
                B = [grid[(a, None)] for a in full]
                if set(A + B) <= set(W.columns):
                    p, g = _contrast(L, o, cfg, _d(W, o, A, B), f"main effect: seams {j} vs none")
                    parts_p.append(p)
                    parts_g.append(g)
        for x in (*parts_p, *parts_g):
            x["kind"] = kind
        per_all += parts_p
        glob_all += parts_g
    glob, per = _finish(per_all, glob_all, "bh", cfg)
    return {"global": glob, "per_dataset": per,
            "extra": {"grid": pd.DataFrame([dict(assembler=a, joiner=j or "none", method=m)
                                            for (a, j), m in sorted(grid.items(), key=str)])}}


# ─────────────────────── RQ4 fidelity → utility ────────────────────────────
def utility_by_criterion(T, methods) -> pd.DataFrame:
    """Transfer ratio per (dataset, method, criterion@split): median over seeds, tasks of the
    criterion (primary metric) and the models fitted on every one of them."""
    L = utility_long(T["utility"])
    Rt = transfer_ratio(L)
    Rt = Rt[Rt["method"].isin(methods)].dropna(subset=["ratio"])
    kind = dict(zip(T["utility"]["task"], T["utility"]["task_kind"]))
    Rt["criterion"] = Rt["task"].map(kind).map(lambda k: LB.UT_CRITERIA.get(k, k))
    cover = Rt.groupby(["criterion", "model"])["task"].nunique()
    need = Rt.groupby("criterion")["task"].nunique()
    ok = {(c, m) for (c, m), n in cover.items() if n == need[c]}
    Rt = Rt[[(c, m) in ok for c, m in zip(Rt["criterion"], Rt["model"])]]
    Rt["col"] = Rt["criterion"] + "@" + Rt["split"].astype(str)
    return Rt.groupby(["dataset", "method", "col"])["ratio"].median().unstack("col")


def rq4_fidelity_predicts_utility(T, cfg):
    """Per dataset, Spearman ρ across methods between a fidelity metric (oriented: higher = better)
    and the transfer ratio of a utility criterion; across datasets: median ρ, share of datasets with
    ρ > 0, Wilcoxon of ρ against 0, BH over every (metric, criterion). Which metrics — and which
    reference (train / val / OOT) — tell which synthetic data will train better models."""
    methods = _methods(T, cfg)
    if not len(T.get("utility", [])):
        return _empty()
    Ub = utility_by_criterion(T, methods)
    F = fidelity_long(T["fidelity"])
    F = F[F["method"].isin(methods) & F["unit"].isin(fid_units(("train", "val", "oot"), cfg.fidelity_ref))]
    Fm = F.groupby(["dataset", "method", "unit"])["value"].mean().unstack("unit")
    Fm = Fm * pd.Series(ORIENT).reindex(Fm.columns).to_numpy()
    J = Fm.join(Ub, how="inner")
    rows, per = [], []
    for ds, g in J.groupby(level="dataset"):
        if len(g) < 5:
            continue
        for crit in Ub.columns:
            for u in Fm.columns:
                j = g[[u, crit]].dropna().rank()          # Spearman: ranks of the methods present in both
                if len(j) >= 5 and j[u].nunique() > 1:
                    per.append(dict(dataset=ds, unit=u, criterion=crit, rho=float(j[u].corr(j[crit]))))
    P = pd.DataFrame(per)
    if not len(P):
        return _empty()
    for (u, crit), g in P.groupby(["unit", "criterion"]):
        r = g["rho"].dropna().to_numpy()
        if len(r) < 3:
            continue
        base, ref = split_ref(u, cfg.fidelity_ref)
        rows.append(dict(unit=u, metric=base, reference=ref, group=GROUP_OF.get(u), criterion=crit,
                         n_datasets=len(r), median_rho=float(np.median(r)), share_positive=float((r > 0).mean()),
                         p_two_sided=S.wilcoxon(r)))
    G = pd.DataFrame(rows)
    G["p_bh"] = S.bh(G["p_two_sided"].to_numpy())
    G["predictive"] = (G["p_bh"] < cfg.alpha) & (G["median_rho"] > 0)
    by_ref = G.groupby(["criterion", "reference"]).agg(median_rho=("median_rho", "median"),
                                                       share_predictive=("predictive", "mean")).round(3)
    by_group = G.groupby(["group", "reference", "criterion"])["median_rho"].median().unstack("criterion").round(3)
    return {"global": G.sort_values("median_rho", ascending=False), "per_dataset": P,
            "extra": {"by_reference": by_ref, "by_group": by_group,
                      # ties of median_rho broken by unit name: the same five on every platform
                      "top_predictors": G.sort_values(["median_rho", "unit"], ascending=[False, True], kind="stable")
                                         .groupby("criterion").head(5)}}


# ─────────────────────── RQ5 gap to real data, stability ───────────────────
def rq5_gap_and_stability(T, cfg):
    """(a) gap: transfer ratio per method × criterion@split — median over datasets, bootstrap CI over
    datasets, one-sided Wilcoxon of (ratio − 1) < 0 over datasets, BH; (b) stability of the ranking:
    Kendall τ val ↔ OOT and linear ↔ boosting (leaderboard); (c) decisions made on synthetic data
    (grid of models, threshold) — profile max."""
    methods = _methods(T, cfg)
    if not len(T.get("utility", [])):
        return _empty()
    Ub = utility_by_criterion(T, methods)
    rows = []
    rng = np.random.default_rng(0)
    for m, g in Ub.groupby(level="method"):
        for c in Ub.columns:
            r = g[c].dropna().to_numpy()
            if len(r) < 3:
                continue
            bs = [np.median(r[rng.integers(0, len(r), len(r))]) for _ in range(1000)]
            rows.append(dict(method=m, unit=c, n_datasets=len(r), median_ratio=float(np.median(r)),
                             ci_lo=float(np.quantile(bs, 0.025)), ci_hi=float(np.quantile(bs, 0.975)),
                             p_below_real=S.wilcoxon(r - 1.0, "less")))
    G = pd.DataFrame(rows)
    if len(G):
        G["p_below_real_bh"] = S.bh(G["p_below_real"].to_numpy())
        G["verdict"] = np.where(G["p_below_real_bh"] < cfg.alpha, "worse than real", "inconclusive")
    lb = leaderboard(T, cfg)
    st = lb["stability"]
    from .leaderboard import SLICE_COMPARISONS

    # val ↔ OOT and every pair of models (linear ↔ gbdt, and custom models)
    st = st[(st["comparison"] == "val ↔ oot") | ~st["comparison"].isin(SLICE_COMPARISONS)] if len(st) else st
    avg = lb["avg_by_column"]
    shift = pd.DataFrame({c.replace("@val", ""): avg[c.replace("@val", "@oot")] - avg[c]
                          for c in avg.columns if c.startswith("utility:") and c.endswith("@val")
                          and c.replace("@val", "@oot") in avg})
    extra = {"rank_stability": st, "rank_shift_oot_minus_val": shift.round(2)}
    u = T["utility"]
    if "task_kind" in u and (u["task_kind"] == "grid").any():
        grid = u[u["task_kind"] == "grid"]
        dt = []
        for (ds, m, seed), g in grid.groupby(["dataset", "method", "seed"]):
            w = g.pivot_table(index="grid_id", columns="regime", values="auc")
            if {"R", "S"} <= set(w.columns) and len(w) > 2:
                dt.append(dict(dataset=ds, method=m, rho=float(w["R"].corr(w["S"], method="spearman"))))
        if dt:
            extra["decision_transfer_rank_agreement"] = (pd.DataFrame(dt).groupby(["method", "dataset"])["rho"].median()
                                                         .groupby("method").median().sort_values(ascending=False)
                                                         .to_frame("median_spearman"))
    else:
        extra["decision_transfer"] = "no model grid: profile max (decision_transfer=True)"
    return {"global": G, "per_dataset": Ub.reset_index(), "extra": extra}


# ─────────────────────── RQ6 cost ──────────────────────────────────────────
def rq6_cost(T, cfg):
    """Per method: median wall time (dataset medians, bootstrap CI over datasets), time relative to
    the fastest method, scaling of log time with log K (bootstrap over datasets); the parts of the cost
    (training, generation of a new series, peak memory); the cost ranks of the leaderboard per slice;
    for each of the four rankings the quality–cost Pareto front and the rank with cost as a third domain."""
    t = T.get("timing", pd.DataFrame())
    if not len(t) or "total_wall_s" not in t:
        return _empty()
    methods = _methods(T, cfg)
    t = t[t["method"].isin(methods)]
    med = t.groupby(["method", "dataset"]).agg(total=("total_wall_s", "median"), K=("K", "first")).reset_index()
    rng = np.random.default_rng(0)
    rows = []
    for m, g in med.groupby("method"):
        x = g["total"].to_numpy(float)
        bs = [np.median(x[rng.integers(0, len(x), len(x))]) for _ in range(1000)]
        row = dict(method=m, median_time_s=float(np.median(x)), ci_lo=float(np.quantile(bs, 0.025)),
                   ci_hi=float(np.quantile(bs, 0.975)), n_datasets=len(x))
        lx, ly = np.log(g["K"].to_numpy(float)), np.log(np.clip(x, 1e-3, None))
        if len(lx) >= 3 and np.ptp(lx) > 0:
            row["slope_logT_logK"] = float(np.polyfit(lx, ly, 1)[0])
            sl = [np.polyfit(lx[i], ly[i], 1)[0] for i in (rng.integers(0, len(lx), len(lx)) for _ in range(500))
                  if np.ptp(lx[i]) > 0]
            row["slope_ci_lo"], row["slope_ci_hi"] = float(np.quantile(sl, 0.025)), float(np.quantile(sl, 0.975))
        rows.append(row)
    G = pd.DataFrame(rows).sort_values("median_time_s")
    G["x_fastest"] = G["median_time_s"] / G["median_time_s"].min()
    # parts of the cost: medians over datasets of the per-dataset medians
    parts = {}
    for sl, leaves in LB.COST_SLICES.items():
        for leaf, (cols, how) in leaves.items():
            cols = [c for c in cols if c in t]
            if cols:
                v = t[cols].astype(float)
                v = v.fillna(0.0).sum(axis=1) if how == "sum" else v.max(axis=1)
                parts[f"{sl}:{leaf}"] = (t.assign(_v=v).groupby(["method", "dataset"])["_v"].median()
                                         .groupby("method").median())
    lb = leaderboard(T, cfg)
    ranks = lb["avg_by_column"][[c for c in lb["avg_by_column"].columns if c.startswith("cost@")]]
    hw = sorted(t["gpu"].fillna("none").unique()) if "gpu" in t else []
    return {"global": G, "per_dataset": med,
            "extra": {"cost_parts": pd.DataFrame(parts).reindex(G["method"]).round(1),
                      "cost_ranks": ranks.reindex(G["method"]).round(2),
                      "pareto": (pd.concat(lb["with_cost"], names=["ranking", "method"]).reset_index()
                                 if lb["with_cost"] else pd.DataFrame()),
                      "hardware": hw,
                      "warning": "times on different hardware are not comparable" if len(hw) > 1 else ""}}


# ─────────────────────── RQ8 / RQ9 thematic questions ──────────────────────
def _theme_units(T, cfg, theme):
    """(fidelity long, utility long) of a theme (`leaderboard.THEMES`): fidelity metrics against val
    and OOT; TSTR utility cells whose (task, kind, metric) the theme selects."""
    sel = LB.THEMES[theme]
    F = fidelity_long(T["fidelity"])
    F = F[F["unit"].isin([u for u in fid_units(("val", "oot"), cfg.fidelity_ref)
                          if sel["fidelity"](split_ref(u, cfg.fidelity_ref)[0])])]
    U = pd.DataFrame()
    if len(T.get("utility", [])):
        Ua = _tstr(utility_long(T["utility"], all_metrics=True))
        kind = dict(zip(T["utility"]["task"], T["utility"]["task_kind"]))
        m = np.array([bool(sel["utility"](t, kind.get(t), me)) for t, me in zip(Ua["task"], Ua["metric"])], bool)
        U = Ua[m]
    return F, U


def _theme_link(T, cfg, F, U, methods):
    """Per dataset, Spearman ρ across methods between each fidelity metric of the theme (oriented,
    seed mean) and the theme's utility score (mean within-cell rank of the oriented TSTR metric,
    higher = better); across datasets: median ρ, Wilcoxon against 0, BH."""
    if not len(F) or not len(U):
        return pd.DataFrame()
    U = U[U["method"].isin(methods)]
    o = _ut_orient(U)
    um = U.groupby(["dataset", "unit", "method"])["value"].mean().reset_index()
    um["s"] = um["value"] * um["unit"].map(o)
    um["r"] = um.groupby(["dataset", "unit"])["s"].rank()
    us = um.groupby(["dataset", "method"])["r"].mean().rename("utility")
    fm = F[F["method"].isin(methods)].groupby(["dataset", "unit", "method"])["value"].mean().reset_index()
    fm["s"] = fm["value"] * fm["unit"].map(ORIENT)
    rows = []
    for u, g in fm.groupby("unit"):
        j = g.set_index(["dataset", "method"])["s"].to_frame("f").join(us, how="inner")
        rho = [float(sps.spearmanr(d["f"], d["utility"]).statistic) for _, d in j.groupby(level="dataset")
               if len(d) >= 5 and d["f"].nunique() > 1]
        rho = np.array([r for r in rho if np.isfinite(r)])
        if len(rho) >= 3:
            rows.append(dict(unit=u, reference=split_ref(u, cfg.fidelity_ref)[1], n_datasets=len(rho),
                             median_rho=float(np.median(rho)), share_positive=float((rho > 0).mean()),
                             p_two_sided=S.wilcoxon(rho)))
    g = pd.DataFrame(rows)
    if len(g):
        g["p_bh"] = S.bh(g["p_two_sided"].to_numpy())
    return g.sort_values("median_rho", ascending=False) if len(g) else g


def _theme_question(T, cfg, theme):
    """Families compared on the theme's units — every pool method against the random path (pool
    margin), every long-series generator against the assembly median (between-seed spread), BH over the question —
    the theme's ranking (leaderboard) and the link of its fidelity metrics to its utility metrics."""
    methods = _methods(T, cfg)
    F, U = _theme_units(T, cfg, theme)
    grid = pool_grid(methods)
    rand = grid.get(("random", None))
    gens = long_methods(methods)
    per_all, glob_all = [], []
    for kind, L, orient in (("fidelity", F, ORIENT), ("utility", U, None)):
        if not len(L):
            continue
        o = orient or _ut_orient(L)
        parts_p, parts_g = [], []
        for m in [m for m in grid.values() if m != rand]:
            p, g = _compare(L, o, m, [rand], cfg, label=f"{m} vs {rand}")
            parts_p += p
            parts_g += g
        if gens:
            LA = _with_assembly_median(L, methods)
            for gname in gens:
                p, g = _compare(LA, o, gname, [ASSEMBLY_MEDIAN], cfg, margin="seed",
                                label=f"{gname} vs {ASSEMBLY_MEDIAN}")
                parts_p += p
                parts_g += g
        for x in (*parts_p, *parts_g):
            x["kind"] = kind
        per_all += parts_p
        glob_all += parts_g
    glob, per = _finish(per_all, glob_all, "bh", cfg)
    lb = leaderboard(T, cfg)
    cols = [c for c in lb["avg_by_column"].columns if c.startswith(f"theme:{theme}:")]
    rank = lb["avg_by_column"].reindex(lb["main"].index)[cols] if cols else pd.DataFrame()
    tests = lb["tests"][lb["tests"]["column"].isin(cols)] if len(lb["tests"]) else pd.DataFrame()
    summary = (glob.groupby(["kind", "comparison"])["verdict"].value_counts().unstack(fill_value=0)
               if len(glob) else pd.DataFrame())
    return {"global": glob, "per_dataset": per,
            "extra": {"ranking": rank.round(2), "ranking_tests": tests, "verdicts_by_comparison": summary,
                      "fidelity_predicts_utility": _theme_link(T, cfg, F, U, methods)}}


def rq8_class_balance(T, cfg):
    """Do methods keep the class shares of every classification task — rare events above all — and
    does a wrong share cost TSTR quality? Units: F8.1, F11 (val, OOT); TSTR ECE of binary tasks."""
    return _theme_question(T, cfg, "class_balance")


def rq9_extremes(T, cfg):
    """Do methods keep the tails, outliers and extremes of the real series, and does that matter for
    models that must predict extremes? Units: tail metrics of F1, F2.4, F7.4, F12 (val, OOT); TSTR
    error on the extreme 10% of regression targets, PR AUC of rare events."""
    return _theme_question(T, cfg, "extremes")


# ─────────────────────── RQ7 moderators ────────────────────────────────────
def rq7_moderators(results: dict, cfg) -> dict:
    """Exploratory: Spearman between dataset descriptors and the per-dataset effects of RQ2 and of the
    RQ3 main effects (median effect in noise units over the units of a comparison), BH."""
    desc = dataset_descriptors(cfg)
    eff = {}
    for rq, pat in (("RQ2", None), ("RQ3", "main effect")):
        per = results.get(rq, {}).get("per_dataset")
        if per is None or not len(per) or "effect_noise_units" not in per:
            continue
        for (comp, kind), g in per.groupby(["comparison", "kind"]):
            if pat and not str(comp).startswith(pat):
                continue
            eff[f"{rq}:{kind}:{comp}"] = g.groupby("dataset")["effect_noise_units"].median()
    rows = []
    for name, e in eff.items():
        j = desc.set_index("dataset").join(e.rename("effect")).dropna()
        for c in desc.columns.drop("dataset"):
            if len(j) >= 4 and j[c].nunique() > 1:
                r, p = sps.spearmanr(j[c], j["effect"])
                rows.append(dict(effect=name, descriptor=c, spearman=float(r), p=float(p), n=len(j)))
    g = pd.DataFrame(rows)
    if len(g):
        g["p_bh"] = S.bh(g["p"].to_numpy())
    return {"global": g, "per_dataset": desc, "extra": {}}


# ─────────────────────── confirmatory family ───────────────────────────────
def confirmatory_rq(T, cfg) -> pd.DataFrame:
    """The pre-specified family, Holm over every test together; cells `CONFIRMATORY_CELLS` (TSTR,
    primary metric of the task):
    C1  do the methods differ at all — Friedman over every method of the default ranking, blocks = datasets
        (`stats.complete_blocks`: a method left out on a dataset drops out of the test, not the dataset);
    C2  each long-series generator vs the median of the pool assembly (between-seed spread);
    C3  main effect of window selection (mean of every ranked selection strategy vs the random path);
    C4  main effect of seam processing (mean of every joiner vs none, averaged over the paths that have
        every joiner).
    Verdict: Holm on the two-sided p; a directional test is better / worse when significant and
    |median z| > 1, same when TOST (Holm) is significant; a missing test enters with p = 1."""
    methods = _methods(T, cfg)
    U = tstr_primary(T)
    grid = pool_grid(methods)
    joiners = sorted({j for (_, j) in grid if j})
    full = [a for a in sorted({a for (a, _) in grid}) if all((a, j) in grid for j in [None, *joiners])]
    gens = list(CONFIRMATORY_GENERATORS)            # a missing one enters with p = 1
    # C1 and C3: the ranked methods of the default ranking (not the reporting flag --rank-exclude)
    import dataclasses

    cmethods = LB.leaderboard_methods(T, dataclasses.replace(cfg, rank_exclude=None))
    rows = []
    for task, model, split in CONFIRMATORY_CELLS:
        kind = R.tasks.get(task).kind if task in R.tasks else "clf"
        unit = f"{task}|{model}|S|{split}|{PRIMARY_METRIC[kind]}"
        L = U[U["unit"] == unit]
        cell = f"{task}|{model}|{split}"
        # C1
        D = S.complete_blocks(L[L["method"].isin(cmethods)].groupby(["dataset", "method"])["value"].mean().unstack())
        p = float(sps.friedmanchisquare(*[D[c] for c in D.columns]).pvalue) if len(D) >= 3 and D.shape[1] >= 3 else np.nan
        rows.append(dict(test="C1 methods differ", cell=cell, comparison="Friedman, all methods", n_datasets=len(D),
                         p_two_sided=p, directional=False))
        if not len(L):
            for g in gens:
                rows.append(dict(test="C2 long vs assembly", cell=cell, comparison=f"{g} vs {ASSEMBLY_MEDIAN}",
                                 directional=True))
            rows += [dict(test="C3 selection", cell=cell, comparison="optimised selection (mean) vs random", directional=True),
                     dict(test="C4 seam processing", cell=cell, comparison="any vs none", directional=True)]
            continue
        o = _ut_orient(L)
        LA = _with_assembly_median(L, methods)
        for g in gens:
            _, gl = _compare(LA, o, g, [ASSEMBLY_MEDIAN], cfg, margin="seed") if g in methods else (None, [])
            rows.append(_conf_row("C2 long vs assembly", cell, f"{g} vs {ASSEMBLY_MEDIAN}", gl))
        W = _wide(L)
        rand = grid.get(("random", None))
        ranked = set(cmethods)
        A = [m for m in selection_methods(grid) if m in ranked and m in W.columns]
        gl = [_contrast(L, o, cfg, _d(W, o, A, [rand]), "selection")[1]] if A and rand in W.columns else []
        rows.append(_conf_row("C3 selection", cell, "optimised selection (mean) vs random", gl))
        if joiners and full:
            A = [grid[(a, j)] for a in full for j in joiners]
            B = [grid[(a, None)] for a in full for _ in joiners]
            ok = set(A + B) <= set(W.columns)
            gl = [_contrast(L, o, cfg, _d(W, o, A, B), "seams")[1]] if ok else []
        else:
            gl = []
        rows.append(_conf_row("C4 seam processing", cell, "any joiner vs none (all paths)", gl))
    c = pd.DataFrame(rows)
    for col in ("p_two_sided", "p_equiv"):
        if col not in c:
            c[col] = np.nan
    c["p_holm"] = S.holm(c["p_two_sided"].fillna(1.0).to_numpy())
    pe = c["p_equiv"].where(c["directional"]).fillna(1.0).to_numpy()
    c["p_equiv_holm"] = S.holm(pe)
    out = []
    for r in c.itertuples():
        if pd.isna(r.p_two_sided):
            out.append("missing")
        elif not r.directional:
            out.append("differ" if r.p_holm < cfg.alpha else "inconclusive")
        elif r.p_holm < cfg.alpha and abs(r.median_z) > 1:
            out.append("better" if r.median_z > 0 else "worse")
        elif r.p_equiv_holm < cfg.alpha:
            out.append("same")
        else:
            out.append("inconclusive")
    c["verdict"] = out
    return c


def _conf_row(test, cell, comparison, glob_list):
    g = [x for x in glob_list if len(x)]
    if not g:
        return dict(test=test, cell=cell, comparison=comparison, directional=True)
    r = g[0].iloc[0]
    return dict(test=test, cell=cell, comparison=comparison, directional=True, n_datasets=r.n_datasets,
                median_z=r.median_z, ci_lo=r.ci_lo, ci_hi=r.ci_hi,
                p_two_sided=min(1.0, 2 * min(r.p_better, r.p_worse)), p_equiv=r.p_equiv, p_sign=r.p_sign,
                n_better=r.n_better, n_worse=r.n_worse)


QUESTIONS = {
    "RQ0": rq0_validity, "RQ1": rq1_ranking, "RQ2": rq2_assembly_vs_long, "RQ3": rq3_assembly_factors,
    "RQ4": rq4_fidelity_predicts_utility, "RQ5": rq5_gap_and_stability, "RQ6": rq6_cost,
    "RQ8": rq8_class_balance, "RQ9": rq9_extremes,
}
QUESTION_TITLES = {
    "RQ0": "Benchmark validity: noise, real-data ceiling, discriminative power and redundancy of the metrics",
    "RQ1": "Ranking of every method in every slice",
    "RQ2": "Assembly from a window pool vs long-series generators",
    "RQ3": "Within assembly: window selection × seam processing",
    "RQ4": "Does fidelity predict utility (which metrics, against which reference)",
    "RQ5": "Gap to real data (TSTR / TRTR), stability over time and across models",
    "RQ6": "Speed and cost: training and generation time, memory, Pareto front \"quality × time\"",
    "RQ7": "Moderators: dataset descriptors and the effects of RQ2 / RQ3 (exploratory)",
    "RQ8": "Class balance: do methods preserve class shares (rare events especially) and what does an error cost",
    "RQ9": "Outliers and extremes: do methods preserve tails and outliers, and does it matter to the models",
}
