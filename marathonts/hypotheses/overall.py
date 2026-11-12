"""One overall leaderboard: fidelity on the core metrics and utility; no privacy, no cost.

    python -m marathonts.hypotheses.overall [--artifacts-dir artifacts/min] [--profile min] [--out DIR]

Composition (fixed in advance):
* fidelity — the core criteria (`leaderboard.CORE_METRICS`), each the mean of its ranks against train, val and
  OOT with equal weights: the aim is synthetic data close to the real series, and train / val / OOT are three
  pieces of it (train — the longest and most precise, val and OOT — not seen by the generator);
* utility — TSTR classification and regression with equal weights, each tested on val and OOT;
* overall = the mean of the two domains with equal weights. Privacy (F10) is not ranked: a memorisation flag is
  reported next to the rank (`memorisation`).

Ranks are noise-aware: within a leaf (dataset, seed, metric × reference or task × model × metric × split) two
methods whose scores differ by no more than the noise of the leaf tie. Rank of a method = 1 + #{methods better
beyond the noise} + ½ #{other methods within the noise}; with zero noise it is the ordinary average rank
(`leaderboard.rank_rows`). Noise of a (dataset, leaf) = median over seeds of |random − twin| (`noise_pair`), or of
|random(seed k) − random(next seed)| without the twin — the estimate of the anchor check. Between seeds the pool
changes too, so it bounds the within-seed noise from above and the ties are conservative. Ranks are then
averaged leaf → group → criterion → domain with equal weights (`leaderboard.aggregate`, `rank_of`), uncertainty
and tiers as in the leaderboard (`leaderboard.summarize`).

Next to the rank: fidelity and utility ranks alone and their Pareto front; normalised scores (random assembly
= 0, real data = 1, `leaderboard.normalized_scores`, criteria and domains averaged with the same equal weights);
the memorisation flag. Robustness: the sensitivity variants (`VARIANTS`), a field with one method per generator
(`field_check`: do near-identical variants of one generator move the others), leave-one-dataset-out and random
criterion weights.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats as sps

from . import stats as S
from .leaderboard import (CORE_FIDELITY, CORE_METRICS, _md, aggregate, column_doc, criterion_means, family,
                          fidelity_rows, leaderboard_methods, normalized_scores, pareto_front, rank_of, summarize,
                          utility_rows, weight_sensitivity)

from marathonts.bench import registry as R  # noqa: E402
from marathonts.bench.fidelity import split_ref  # noqa: E402

REFS = ("train", "val", "oot")
UT_SPLITS = ("val", "oot")
DOMAINS = {"fidelity:": REFS, "utility:": UT_SPLITS}
# metrics without a check against the anchors: seams (real data has none) and the discriminative score against
# val (not separated from the noise in the anchor check); left out in the variant `no_unchecked`
UNCHECKED = (("F5.7_seam_detect_auc_dev", None), ("F6.1_disc_score", "val"))
# sensitivity variants; `main` is the leaderboard
VARIANTS = {
    "main": dict(text="the leaderboard: core metrics, fidelity against train + val + OOT, noise-aware ranks"),
    "plain_ranks": dict(noise=False, text="ordinary average ranks (no ties within the noise)"),
    "fidelity_train": dict(refs=("train",), text="fidelity against train only"),
    "fidelity_holdout": dict(refs=("val", "oot"), text="fidelity against val + OOT only"),
    "no_unchecked": dict(drop=UNCHECKED, text="without F5.7 (seams, no anchor) and F6.1 against val (noise)"),
    "all_metrics": dict(core=False, text="every fidelity metric instead of the core set"),
    "common_datasets": dict(common=True, text="only the datasets where every method is ranked"),
}
# memorisation flag: share of synthetic windows closer to train than the 5th percentile of real-to-real
# distances (F10.2) against the same share of the real OOT piece; flagged when the method's median over
# datasets is at least `Config.near_copy_ratio` (default NEAR_COPY_RATIO) times the real one and the excess is significant (one-sided Wilcoxon over
# datasets, Holm over the methods)
NEAR_COPY = "F10.2_near_copy_share"
NEAR_COPY_RATIO = 2.0


# ─────────────────────── noise-aware ranks ─────────────────────────────────
def rows(T: dict, cfg, methods) -> pd.DataFrame:
    """Fidelity and utility leaves of `methods` (`leaderboard.fidelity_rows`, `utility_rows`), aggregated ones only."""
    parts = [fidelity_rows(T["fidelity"], methods, cfg.fidelity_ref) if len(T.get("fidelity", [])) else None,
             utility_rows(T["utility"], methods) if len(T.get("utility", [])) else None]
    L = pd.concat([p for p in parts if p is not None and len(p)], ignore_index=True)
    return L[L["agg"]].reset_index(drop=True)


def leaf_noise(T: dict, cfg) -> pd.Series:
    """Noise of every (dataset, leaf, slice): median over seeds of |random − twin|, or of the between-seed
    difference of the random path without the twin (`leaderboard._pair_noise`)."""
    a, b = tuple(cfg.noise_pair)
    L = rows(T, cfg, [a, b])
    g = ["dataset", "leaf", "slice"]
    W = L.pivot_table(index=[*g, "seed"], columns="method", values="score")
    if a not in W:
        return pd.Series(dtype=float)
    d = (W[a] - W[b]).abs() if b in W else W[a].sort_index().groupby(level=g).diff().abs()
    return d.groupby(level=g).median()


def rank_noise(L: pd.DataFrame, k: int, noise: pd.Series | None = None, cells: int = 5_000_000) -> pd.DataFrame:
    """`leaderboard.rank_rows` with ties within the noise of the leaf (module docstring); `noise` None → the
    ordinary average ranks. Ranks rescaled to 1…k when methods are missing in a block. The blocks are compared
    in chunks of about `cells` method pairs (memory ∝ chunk × methods²)."""
    idx = ["dataset", "seed", "leaf", "slice"]
    W = L.pivot_table(index=idx, columns="method", values="score")
    S_ = W.to_numpy(float)
    if noise is not None and len(noise):
        key = pd.MultiIndex.from_arrays([W.index.get_level_values(n) for n in ("dataset", "leaf", "slice")])
        eps = noise.reindex(key).fillna(0.0).to_numpy()
    else:
        eps = np.zeros(len(W))
    out = np.full_like(S_, np.nan)
    chunk = max(1, cells // max(1, S_.shape[1]) ** 2)
    for i in range(0, len(S_), chunk):
        s, e = S_[i:i + chunk], eps[i:i + chunk, None, None]
        ok = ~np.isnan(s)
        D = s[:, None, :] - s[:, :, None]              # D[n, i, j] = score_j − score_i
        better = ((D > e) & ok[:, None, :]).sum(2)
        tie = ((np.abs(D) <= e) & ok[:, None, :]).sum(2) - 1
        r = 1 + better + 0.5 * tie
        n = ok.sum(1, keepdims=True)
        out[i:i + chunk] = np.where(ok & (n > 1), 1 + (r - 1) * (k - 1) / np.clip(n - 1, 1, None), np.nan)
    rk = pd.DataFrame(out, index=W.index, columns=W.columns).stack().rename("rank")
    return L.join(rk, on=[*idx, "method"])


def select(L: pd.DataFrame, cfg, core: bool = True, drop=()) -> pd.DataFrame:
    """Leaves of a variant: utility, and fidelity on the core metrics (`core`) without the (metric, reference)
    pairs of `drop` (reference None — every reference)."""
    fid = L["criterion"].str.startswith("fidelity:")
    parts = {u: split_ref(u, cfg.fidelity_ref) for u in L["leaf"].unique()}       # once per leaf, not per row
    base, ref = L["leaf"].map(lambda u: parts[u][0]), L["leaf"].map(lambda u: parts[u][1])
    keep = ~fid | base.isin(CORE_FIDELITY) if core else pd.Series(True, index=L.index)
    for m, r in drop:
        keep &= ~(fid & (base == m) & ((ref == r) if r else True))
    return L[keep]


def overall_rank(C: pd.DataFrame, refs=REFS) -> pd.Series:
    """Rank per (dataset, seed, method): fidelity against `refs` and utility, equal weights."""
    return rank_of(C, {"fidelity:": refs, "utility:": UT_SPLITS})


# ─────────────────────── next to the rank ──────────────────────────────────
def memorisation(T: dict, methods, alpha: float = 0.05, ratio: float = NEAR_COPY_RATIO) -> pd.DataFrame:
    """Near-copy share (F10.2) of every method against the real OOT piece (`NEAR_COPY_RATIO`, module header).
    Medians over seeds within a dataset, then over datasets."""
    f = T.get("fidelity", pd.DataFrame())
    if not len(f) or NEAR_COPY not in f:
        return pd.DataFrame()
    D = f[f["method"].isin([*methods, "real"])].groupby(["dataset", "method"])[NEAR_COPY].median().unstack("method")
    if "real" not in D:
        return pd.DataFrame()
    ms = [m for m in methods if m in D]
    p = [S.wilcoxon((D[m] - D["real"]).dropna().to_numpy(), "greater") for m in ms]
    out = pd.DataFrame({"near_copy_share": D[ms].median(), "near_copy_real": float(D["real"].median()),
                        "near_copy_ratio": (D[ms].div(D["real"], axis=0)).median(),
                        "p_more_copies_holm": S.holm(np.array(p, float))}, index=ms)
    out["memorisation_flag"] = (out["near_copy_ratio"] >= ratio) & (out["p_more_copies_holm"] < alpha)
    return out


def normalized(T: dict, cfg, methods) -> pd.DataFrame:
    """Normalised scores (random assembly = 0, real = 1) with the hierarchy of the ranks: per criterion median
    over the leaves of a dataset, then over datasets; a domain = the mean of its criteria; overall = the mean of
    the two domains. Fidelity against val and train only (`real` is a piece of OOT)."""
    per, _ = normalized_scores(T, cfg, methods)
    if not len(per):
        return pd.DataFrame()
    crit = (per.groupby(["method", "kind", "criterion", "dataset"])["score"].median()
            .groupby(["method", "kind", "criterion"]).median())
    dom = crit.groupby(["method", "kind"]).mean().unstack("kind").add_prefix("norm_")
    dom["norm_overall"] = dom.mean(axis=1, skipna=False)
    return dom


def generator(method: str) -> str:
    """The generator a method's series come from (a pool generator or a long-series generator)."""
    if method not in R.methods:
        return method
    s = R.methods.get(method)
    return s.pool or s.long


def representative(group: list[str], cfg) -> str:
    """One method per generator, fixed without the results: the random assembly of the pool, else the first by name."""
    a = tuple(cfg.noise_pair)[0]
    if a in group:
        return a
    rnd = [m for m in group if m in R.methods and R.methods.get(m).assembler in ("random", "random_b")]
    return sorted(rnd or group)[0]


def field_check(L: pd.DataFrame, cfg, methods, noise, main: pd.DataFrame, n_boot: int) -> tuple[pd.DataFrame, float]:
    """Each method ranked in a field of one method per generator (`representative`; its own generator
    represented by the method itself). Kendall τ between the order of the representatives in that field and
    in the leaderboard. Shows whether near-identical variants of one generator move the others."""
    groups: dict[str, list[str]] = {}
    for m in methods:
        groups.setdefault(generator(m), []).append(m)
    reps = {g: representative(ms, cfg) for g, ms in groups.items()}
    rows_, cache = [], {}
    for m in methods:
        fld = tuple(sorted({**reps, generator(m): m}.values()))
        if fld not in cache:
            Lf = rank_noise(L[L["method"].isin(fld)], len(fld), noise)
            cache[fld] = summarize(overall_rank(aggregate(Lf)[1]), n_boot)
        t = cache[fld]
        if m in t.index:
            rows_.append(dict(method=m, generator=generator(m), field=", ".join(fld), rank_in_field=t.loc[m, "avg_rank"],
                              place_in_field=int(t.index.get_loc(m)) + 1, field_size=len(t),
                              tier_in_field=bool(t.loc[m, "tier_wilcoxon"])))
    out = pd.DataFrame(rows_).set_index("method") if rows_ else pd.DataFrame()
    base = cache.get(tuple(sorted(reps.values())), pd.DataFrame())
    common = [m for m in base.index if m in main.index]
    tau = sps.kendalltau(base.loc[common, "avg_rank"], main.loc[common, "avg_rank"]).statistic if len(common) > 2 else np.nan
    return out, float(tau)


def leave_one_dataset_out(x: pd.Series) -> pd.DataFrame:
    """Place of every method with each dataset left out in turn (seeds averaged within a dataset)."""
    D = x.unstack("method").groupby(level="dataset").mean()
    place = lambda m: m.rank(method="min")
    full = place(D.mean())
    P = pd.DataFrame({d: place(D.drop(index=d).mean()) for d in D.index})
    return pd.DataFrame({"place": full, "place_best": P.min(axis=1), "place_worst": P.max(axis=1),
                         "n_first": (P == 1).sum(axis=1), "n_left_out": P.shape[1]}).sort_values("place")


# ─────────────────────── build ─────────────────────────────────────────────
def build(T: dict, cfg, methods=None, n_boot: int = 1000) -> dict:
    """Every table of the overall leaderboard (module docstring)."""
    R.load_builtins()
    methods = methods or leaderboard_methods(T, cfg)
    k = len(methods)
    noise = leaf_noise(T, cfg)
    L_all = rows(T, cfg, methods)
    L = select(L_all, cfg)
    C = aggregate(rank_noise(L, k, noise))[1]
    x = overall_rank(C)
    main = summarize(x, n_boot)
    tests = dict(main.attrs)
    main.insert(0, "family", [family(m) for m in main.index])
    main.insert(1, "generator", [generator(m) for m in main.index])
    fid = summarize(rank_of(C, {"fidelity:": REFS}), n_boot)["avg_rank"]
    ut = summarize(rank_of(C, {"utility:": UT_SPLITS}), n_boot)["avg_rank"]
    main["fidelity_rank"], main["utility_rank"] = fid.reindex(main.index), ut.reindex(main.index)
    main["pareto_fid_ut"] = pareto_front(main["fidelity_rank"], main["utility_rank"])
    main = main.join(normalized(T, cfg, methods)).join(
        memorisation(T, methods, cfg.alpha, getattr(cfg, "near_copy_ratio", NEAR_COPY_RATIO)))
    # sensitivity variants
    var, info = {"main": main["avg_rank"]}, []
    for name, v in VARIANTS.items():
        if name != "main":
            Lv = select(L_all, cfg, v.get("core", True), v.get("drop", ()))
            Cv = aggregate(rank_noise(Lv, k, noise if v.get("noise", True) else None))[1]
            xv = overall_rank(Cv, v.get("refs", REFS))
            if v.get("common"):
                W = xv.unstack("method").groupby(level="dataset").mean()
                xv = xv[xv.index.get_level_values("dataset").isin(W.dropna().index)]
            sv = summarize(xv, n_boot)
            var[name] = sv["avg_rank"] if len(sv) else pd.Series(dtype=float)
        s = var[name]
        common = s.index.intersection(main.index)
        info.append(dict(variant=name, text=VARIANTS[name]["text"], first=s.idxmin() if len(s) else None,
                         tau_vs_main=sps.kendalltau(s[common], main.loc[common, "avg_rank"]).statistic
                         if len(common) > 2 else np.nan,
                         main_first_place=int(s.rank(method="min").get(main.index[0], np.nan))
                         if main.index[0] in s.index else None))
    sens = pd.DataFrame(var).reindex(main.index)
    field, field_tau = field_check(L, cfg, methods, noise, main, n_boot)
    weights = weight_sensitivity(criterion_means(C, DOMAINS).groupby(level=["dataset", "method"]).mean()
                                 .groupby(level="method").mean(), DOMAINS)
    crit = criterion_means(C, DOMAINS).groupby(level=["dataset", "method"]).mean().groupby(level="method").mean()
    return dict(main=main, criteria=crit.reindex(main.index), sensitivity=sens,
                variants=pd.DataFrame(info).set_index("variant"), field=field.reindex(main.index), field_tau=field_tau,
                lodo=leave_one_dataset_out(x), weights=weights, noise=noise,
                attrs=tests, methods=methods, datasets=sorted(L["dataset"].unique()),
                seeds=sorted(L["seed"].unique()))


# ─────────────────────── output ────────────────────────────────────────────
DOC = {
    "generator": "the generator the method's series come from (pool or long-series generator)",
    "fidelity_rank": "avg_rank in the fidelity domain alone (core criteria against train + val + OOT)",
    "utility_rank": "avg_rank in the utility domain alone (TSTR classification + regression, val + OOT)",
    "pareto_fid_ut": "True — no other method is at least as good in both fidelity_rank and utility_rank and "
                     "strictly better in one",
    "norm_fidelity": "normalised fidelity: mean over the core criteria of the median normalised score "
                     "(random assembly = 0, real = 1; against val and train)",
    "norm_utility": "normalised utility: mean of classification and regression (TSTR, random = 0, TRTR = 1)",
    "norm_overall": "mean of norm_fidelity and norm_utility",
    "near_copy_share": "median over datasets of F10.2: share of synthetic windows closer to train than the 5th "
                       "percentile of real-to-real distances",
    "near_copy_real": "the same share for the real OOT piece",
    "near_copy_ratio": "median over datasets of near_copy_share / near_copy_real",
    "p_more_copies_holm": "one-sided Wilcoxon over datasets \"more near copies than real\", Holm over the methods",
    "memorisation_flag": "True — near_copy_ratio ≥ Config.near_copy_ratio (default 2) and p_more_copies_holm < α; reported, "
                         "does not change the rank",
    "text": "what the variant changes", "first": "the method with the lowest avg_rank in the variant",
    "tau_vs_main": "Kendall τ between the method order of the variant and of the leaderboard",
    "main_first_place": "place of the leaderboard's first method in the variant",
    "field": "the methods of the field (one per generator)",
    "rank_in_field": "avg_rank of the method in its field", "place_in_field": "place in its field",
    "field_size": "number of methods in the field",
    "tier_in_field": "True — not significantly worse than the first method of the field",
    "place": "place in the leaderboard (seeds averaged within a dataset, then the mean over datasets)",
    "place_best": "best place with one dataset left out", "place_worst": "worst place with one dataset left out",
    "n_first": "number of the leave-one-dataset-out rankings in which the method is first",
    "n_left_out": "number of leave-one-dataset-out rankings (one per dataset)",
}


def doc(df: pd.DataFrame, extra: dict | None = None) -> str:
    """`leaderboard.column_doc` with the meanings of `DOC` for the columns of `df` only."""
    return column_doc(df, {k: v for k, v in {**DOC, **(extra or {})}.items() if k in df.columns})


def write(res: dict, cfg, out: Path, report_dir: Path | None = None) -> Path:
    """Parquet tables to `out`, `OVERALL.md` to `report_dir` (default `<out>/../reports`)."""
    from marathonts.bench.storage import write_table

    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    report_dir = Path(report_dir) if report_dir else out.parent / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)

    def save(df, name, index=True):
        if df is None or not len(df):
            return
        d = df.reset_index() if index else df.copy()
        d.columns = [str(c) for c in d.columns]
        write_table(d, out / f"{name}.parquet")

    for name in ("main", "criteria", "sensitivity", "variants", "field", "lodo", "weights"):
        save(res[name], "overall" if name == "main" else name)
    main = res["main"]
    rank_cols = ["family", "avg_rank", "ci_lo", "ci_hi", "p_first", "p_top3", "p_worse_than_best_holm",
                 "tier_wilcoxon", "n_datasets"]
    side = [c for c in ("fidelity_rank", "utility_rank", "pareto_fid_ut", "norm_fidelity", "norm_utility",
                        "norm_overall", "near_copy_share", "near_copy_ratio", "memorisation_flag") if c in main]
    core = "; ".join(f"{c.replace('_', ' ')} ({', '.join(ms)})" for c, ms in CORE_METRICS.items())
    a_ = res["attrs"]
    L = ["# Overall leaderboard: fidelity and utility", "",
         f"Methods: {len(main)}. Datasets ({len(res['datasets'])}): {', '.join(res['datasets'])}. "
         f"Seeds: {len(res['seeds'])}.", "",
         "Composition (fixed in advance). Fidelity — the core criteria " + core + "; each criterion the mean of "
         "its ranks against train, val and OOT. Utility — TSTR classification and regression with equal weights, "
         "each tested on val and OOT. Overall = mean of the two domains. Not included: privacy (memorisation flag "
         "next to the rank), time, memory.", "",
         "Ranks are noise-aware: within a leaf two methods whose scores differ by no more than the noise of the "
         "leaf (median over seeds of |random − twin|, or the between-seed spread of the random path where the "
         "twin is not run) tie. Uncertainty: two-level bootstrap (datasets, then seeds), "
         f"{len(res['seeds'])} seeds; tier — not significantly worse than the first method (one-sided Wilcoxon over "
         "datasets, Holm).", "",
         f"Friedman p = {a_.get('p_friedman', np.nan):.3g}, datasets × methods in the test = {a_.get('n_blocks')} × {a_.get('n_methods_friedman')}.", "",
         "## Leaderboard", "", column_doc(main[rank_cols]), "Rows: sorted by avg_rank.", "", _md(main[rank_cols]), "",
         "## Next to the rank", "", doc(main[side]), _md(main[side]), "",
         "## Criteria", "", "Mean rank of every method in each criterion (references / splits averaged).", "",
         _md(res["criteria"]), "",
         "## Sensitivity", "", doc(res["variants"]), _md(res["variants"], "variant"), "",
         "avg_rank of every method in every variant.", "", _md(res["sensitivity"]), "",
         "## One method per generator", "",
         f"Kendall τ between the order of the representatives in their field and in the leaderboard: "
         f"{res['field_tau']:.2f}.", "", doc(res["field"]), _md(res["field"]), "",
         "## Leave one dataset out", "", doc(res["lodo"]), _md(res["lodo"]), ""]
    w = res["weights"]
    if len(w):
        L += ["## Random criterion weights", "",
              f"Dirichlet(1) weights within each domain, 2000 draws; median Kendall τ with equal weights: "
              f"{w.attrs.get('median_tau_vs_equal', np.nan):.2f}.", "",
              column_doc(w, {"p_first": "share of the draws in which the method is first",
                             "p_top3": "share of the draws in which the method is among the three first"}), _md(w), ""]
    f = report_dir / "OVERALL.md"
    f.write_text("\n".join(L))
    return f


def main(argv=None) -> dict:
    import argparse
    import dataclasses

    from .run import _run_config, add_analysis_args, apply_analysis_args, check_tables, load_tables

    ap = argparse.ArgumentParser()
    ap.add_argument("--artifacts-dir")
    ap.add_argument("--profile", choices=["min", "mid", "max"], default="min")
    ap.add_argument("--out", help="default: <artifacts>/overall (report: <artifacts>/reports)")
    ap.add_argument("--n-boot", type=int, default=1000)
    ap.add_argument("--rank-exclude", nargs="*", metavar="METHOD",
                    help="methods left out (default: Config.rank_exclude, as in the leaderboard); no names — every method")
    add_analysis_args(ap)
    a = ap.parse_args(argv)
    a.case_method = a.noise_pair = None
    cfg = apply_analysis_args(_run_config(a), a)
    if a.artifacts_dir:
        cfg = dataclasses.replace(cfg, artifacts_dir=Path(a.artifacts_dir))
    if a.rank_exclude is not None:
        cfg = dataclasses.replace(cfg, rank_exclude=list(a.rank_exclude))
    T = load_tables(cfg)
    check_tables(T, cfg)
    res = build(T, cfg, n_boot=a.n_boot)
    out = Path(a.out) if a.out else Path(cfg.artifacts_dir) / "overall"
    print(f"overall leaderboard → {write(res, cfg, out)}")
    return res


if __name__ == "__main__":
    main()
