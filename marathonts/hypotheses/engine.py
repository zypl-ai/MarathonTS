"""Paired-effect engine: the method under study vs a comparator, per dataset (over seeds) and across datasets.

Input: a long table with columns `dataset, seed, unit, method, value` (unit = a metric or a
(task, model, regime, split, metric) cell; in utility the regime is S — TSTR — or, for the
pseudo-method `real`, R — TRTR) and an orientation per unit (+1 higher is better).

For every (unit, comparator):
* per dataset — d = orient · (method − comparator) over seeds (d > 0: the method better); Wilcoxon
  one-sided both ways, TOST against the noise margin, Hodges–Lehmann effect, verdict;
* across datasets — d in noise units (d / margin of its dataset); Wilcoxon, sign test and a
  one-sample t-test on dataset means, hierarchical bootstrap CI, TOST at ±1 noise unit.

The margin of a (dataset, unit) — the smallest effect of interest — is the `q`-quantile (median by
default) of |vae_rand − vae_rand_b| over seeds: what two random stitches of one pool
differ by in a single run. Without the twin (profile min) it is the between-seed spread of vae_rand
(the pool is resampled on every seed, so this margin is wider). Against independently trained
baselines the margin is the between-seed spread of the case-study method instead (`seed_margins`).
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from . import stats as S

CASE_METHOD = "vae_zseries"
NOISE = ("vae_rand", "vae_rand_b")


def has_twin(long: pd.DataFrame) -> bool:
    """Is the second random path of the noise pair in the table (not run in min)?"""
    return bool(NOISE[1]) and bool((long["method"] == NOISE[1]).any())


NOISE_ESTIMATOR = "neighbours"    # Config.noise_estimator: "neighbours" (pre-specified), "pairs", "perm:<n>"
NOISE_SCALE = 1.0                 # Config.noise_scale: factor on every margin (supplementary sensitivity)


def _abs_diffs(t: pd.DataFrame) -> pd.DataFrame:
    """Between-seed absolute differences of one method per (dataset, unit), by `NOISE_ESTIMATOR`:
    neighbouring seeds (k, k+1) in seed order, every pair of seeds, or neighbours after a random reordering
    of the seeds ("perm:<n>", the same order for every dataset and unit)."""
    est = NOISE_ESTIMATOR
    if est == "neighbours" or est.startswith("perm:"):
        if est.startswith("perm:"):
            seeds = np.sort(t["seed"].unique())
            order = dict(zip(np.random.default_rng(int(est.split(":", 1)[1])).permutation(seeds), range(len(seeds))))
            t = t.assign(_o=t["seed"].map(order)).sort_values("_o").drop(columns="_o")
        else:
            t = t.sort_values("seed")
        return t.assign(absd=t.groupby(["dataset", "unit"])["value"].diff().abs())[["dataset", "unit", "absd"]]
    if est == "pairs":
        W = t.pivot_table(index=["dataset", "unit"], columns="seed", values="value")
        v = W.to_numpy(float)
        i, j = np.triu_indices(v.shape[1], k=1)
        d = np.abs(v[:, i] - v[:, j])
        out = pd.DataFrame(d, index=W.index).stack(future_stack=True).rename("absd").reset_index()
        return out[["dataset", "unit", "absd"]]
    raise ValueError(f"noise_estimator {est!r}: use 'neighbours', 'pairs' or 'perm:<n>'")


def noise_margins(long: pd.DataFrame, q: float = 0.5) -> pd.DataFrame:
    """Pool margin: |random − twin| over seeds; without the twin — the between-seed spread of the random path."""
    if not has_twin(long):
        return seed_margins(long, q, method=NOISE[0])
    a = long[long["method"] == NOISE[0]].set_index(["dataset", "unit", "seed"])["value"]
    b = long[long["method"] == NOISE[1]].set_index(["dataset", "unit", "seed"])["value"]
    j = pd.concat([a.rename("a"), b.rename("b")], axis=1).dropna()
    j["absd"] = (j["a"] - j["b"]).abs()
    m = j.groupby(level=["dataset", "unit"])["absd"].quantile(q).rename("margin").reset_index()
    return m.assign(margin=m["margin"] * NOISE_SCALE)


def seed_margins(long: pd.DataFrame, q: float = 0.5, method: str | None = None) -> pd.DataFrame:
    """Margin from the between-seed spread of one method: q-quantile of |value(seed k) − value(seed k+1)|.
    Used against independently trained baselines, where the pool-sharing noise of rand vs rand_b
    misses the generator-training variance."""
    t = _abs_diffs(long[long["method"] == (method or CASE_METHOD)])
    m = t.groupby(["dataset", "unit"])["absd"].quantile(q).rename("margin").reset_index()
    return m.assign(margin=m["margin"] * NOISE_SCALE)


BASELINES = ("diffusion_ts", "chronos")
CONFIRMATORY_BASELINES = ("diffusion_ts", "chronos")   # case-study pre-specified cell (CS10), even if a baseline is missing
ALTERNATIVES: tuple = ()          # other stitchers on the pool of the method under study (BASELINES.md A–B)
RUN_CFG = None                    # the config the units were made with (before --case-method / --case-task overrides)
CASE_TASK = "clf_up_h24_q90"


def configure(cfg) -> None:
    """Roles of the hypotheses from the config: the method under test (`case_method`), the noise pair (two
    random paths on its pool; the twin only where it is run), the alternative stitchers on the same pool
    (every other method of `cfg.methods` with the same pool generator), the long-series baselines and the
    task of the case-study cells (`stitch_task`)."""
    global CASE_METHOD, NOISE, BASELINES, ALTERNATIVES, CASE_TASK, CONFIRMATORY_BASELINES, NOISE_ESTIMATOR, NOISE_SCALE
    CASE_METHOD, NOISE = cfg.case_method, tuple(cfg.noise_pair)
    NOISE_ESTIMATOR = getattr(cfg, "noise_estimator", "neighbours") or "neighbours"
    NOISE_SCALE = float(getattr(cfg, "noise_scale", 1.0) or 1.0)
    S.CI_STAT = getattr(cfg, "ci_stat", "mean") or "mean"
    BASELINES, CASE_TASK = tuple(cfg.baselines), cfg.stitch_task
    # the confirmatory family: the pre-specified baselines among the config's (hypotheses.run passes the
    # run's planned ones, present in the tables or not)
    from marathonts.bench.config import PRESPECIFIED_LONG

    CONFIRMATORY_BASELINES = tuple(b for b in dict.fromkeys(cfg.baselines) if b in PRESPECIFIED_LONG)
    from marathonts.bench import registry as R

    pool = R.methods.get(CASE_METHOD).pool if CASE_METHOD in R.methods else None
    ALTERNATIVES = tuple(m for m in cfg.methods if m in R.methods and pool and R.methods.get(m).pool == pool
                         and m not in (CASE_METHOD, *NOISE))


def paired(long: pd.DataFrame, orient: dict, comparator: str, method: str | None = None,
           method_override: pd.DataFrame | None = None) -> pd.DataFrame:
    """dataset, seed, unit, d (oriented: > 0 means the method under study is better)."""
    method = method or CASE_METHOD
    a = (method_override if method_override is not None else long[long["method"] == method])
    a = a.set_index(["dataset", "unit", "seed"])["value"]
    b = long[long["method"] == comparator].set_index(["dataset", "unit", "seed"])["value"]
    j = pd.concat([a.rename("a"), b.rename("comp")], axis=1).dropna().reset_index()
    j["d"] = j["unit"].map(orient).fillna(1.0) * (j["a"] - j["comp"])
    return j


def summarize(pairs: pd.DataFrame, margins: pd.DataFrame, alpha=0.05, n_boot=2000) -> tuple[pd.DataFrame, pd.DataFrame]:
    """(per-dataset table, global table) for one comparator."""
    p = pairs.merge(margins, on=["dataset", "unit"], how="left")
    # per dataset: the tests of every (dataset, unit) at once — rows of one length go to scipy as a matrix
    keys, rows = _groups(p, ["dataset", "unit"])
    d_all, mg_all = p["d"].to_numpy(float), p["margin"].to_numpy(float)
    ds_ = [d_all[r] for r in rows]
    mgs = np.array([mg_all[r[0]] for r in rows], float)
    mgs[~(mgs > 0)] = np.nan                # zero noise (discrete / tied metric): no SESOI → no verdict
    hl = S.by_rows(ds_, S.hodges_lehmann_rows, S.hodges_lehmann)
    pbs = S.by_rows(ds_, lambda D: S.wilcoxon_rows(D, "greater"), lambda d: S.wilcoxon(d, "greater"))
    pws = S.by_rows(ds_, lambda D: S.wilcoxon_rows(D, "less"), lambda d: S.wilcoxon(d, "less"))
    pes = S.by_rows(ds_, S.tost_rows, S.tost, mgs)
    per = []
    for (ds, unit), d, mg, eff, pb, pw, pe in zip(keys, ds_, mgs, hl, pbs, pws, pes):
        per.append(dict(dataset=ds, unit=unit, n=len(d), mean_d=float(np.mean(d)), hl=eff, margin=mg,
                        effect_noise_units=eff / mg if mg and mg > 0 else np.nan,
                        p_better=pb, p_worse=pw, p_equiv=pe, rank_biserial=S.rank_biserial(d),
                        verdict=S.verdict(pb, pw, pe, eff, mg, alpha), **S.run_tests(S.DATASET_TESTS, d, mg)))
    per = pd.DataFrame(per)

    glob = []
    p["z"] = np.where(p["margin"] > 0, p["d"] / p["margin"], np.nan)
    zm = p.groupby(["unit", "dataset"])["z"].mean()
    zero = p.groupby(["unit", "dataset"])["margin"].first().le(0).groupby(level="unit").sum()
    counts = per.groupby(["unit", "verdict"]).size().unstack(fill_value=0) if len(per) else pd.DataFrame()
    units, dms = [], []
    for unit, z in zm.groupby(level="unit"):
        dm = z.dropna()
        if len(dm) >= 3:                    # global tests need ≥ 3 datasets
            units.append(unit)
            dms.append(dm.to_numpy())
    pbs = S.by_rows(dms, lambda D: S.wilcoxon_rows(D, "greater"), lambda d: S.wilcoxon(d, "greater"))
    pws = S.by_rows(dms, lambda D: S.wilcoxon_rows(D, "less"), lambda d: S.wilcoxon(d, "less"))
    pes = S.by_rows(dms, S.tost_rows, S.tost, np.ones(len(dms)))
    zrows = dict(zip(*_groups(p, ["unit"])))
    for unit, dm, pb, pw, pe in zip(units, dms, pbs, pws, pes):
        g = p.iloc[zrows[(unit,)]]
        lo, hi = S.hier_bootstrap_ci(pd.DataFrame({"dataset": g["dataset"], "d": g["z"]}), n_boot=n_boot)
        v = counts.loc[unit] if unit in counts.index else pd.Series(dtype=int)
        glob.append(dict(unit=unit, n_datasets=len(dm), n_datasets_zero_margin=int(zero.get(unit, 0)),
                         mean_z=float(pd.Series(dm).mean()), median_z=float(np.median(dm)),
                         ci_lo=lo, ci_hi=hi, p_better=pb, p_worse=pw, p_equiv=pe, p_sign=S.sign_test(dm),
                         p_ttest=S.ttest_1samp(dm),
                         n_better=int(v.get("better", 0)), n_worse=int(v.get("worse", 0)),
                         n_same=int(v.get("same", 0)), n_inconclusive=int(v.get("inconclusive", 0)),
                         **S.run_tests(S.GLOBAL_TESTS, dm)))
    return per, pd.DataFrame(glob)


def _groups(df: pd.DataFrame, keys: list) -> tuple[list, list]:
    """(key tuples, row positions) of the groups of `df` by `keys`, in groupby's sorted order."""
    if not len(df):
        return [], []
    gid = df.groupby(keys, sort=True).ngroup().to_numpy()
    pos = np.flatnonzero(gid >= 0)
    pos = pos[np.argsort(gid[pos], kind="stable")]
    rows = np.split(pos, np.flatnonzero(np.diff(gid[pos])) + 1)
    first = df.iloc[[r[0] for r in rows]][keys]
    return list(first.itertuples(index=False, name=None)), rows


def finalize(glob: pd.DataFrame, family_adjust: str = "holm", alpha=0.05) -> pd.DataFrame:
    """Adjust the global p-values within one hypothesis and give the global verdict."""
    if not len(glob):
        return glob
    adj = S.holm if family_adjust == "holm" else S.bh
    g = glob.copy()
    for c in ("p_better", "p_worse", "p_equiv"):
        g[c + "_adj"] = adj(g[c].to_numpy())
    g["verdict"] = [S.verdict(r.p_better_adj, r.p_worse_adj, r.p_equiv_adj, r.median_z, 1.0, alpha)
                    for r in g.itertuples()]
    return g


def finalize_per_dataset(per: pd.DataFrame, glob: pd.DataFrame, family_adjust: str = "bh", alpha=0.05):
    """Adjust per-dataset p-values within (hypothesis, dataset) — all units and comparators of the
    hypothesis on that dataset form one family — recompute the verdicts and the verdict counts
    of the global table."""
    if not len(per):
        return per, glob
    adj = S.holm if family_adjust == "holm" else S.bh
    per = per.copy()
    for c in ("p_better", "p_worse", "p_equiv"):
        per[c + "_adj"] = np.nan
        for ds, idx in per.groupby("dataset").groups.items():
            per.loc[idx, c + "_adj"] = adj(per.loc[idx, c].to_numpy())
    per["verdict"] = [S.verdict(r.p_better_adj, r.p_worse_adj, r.p_equiv_adj, r.hl, r.margin, alpha)
                      for r in per.itertuples()]
    if len(glob):
        cnt = per.groupby(["unit", "comparator"])["verdict"].value_counts().unstack(fill_value=0)
        glob = glob.copy()
        for v in ("better", "worse", "same", "inconclusive"):
            m = cnt[v] if v in cnt else pd.Series(dtype=int)
            glob[f"n_{v}"] = [int(m.get((u, c), 0)) for u, c in zip(glob["unit"], glob["comparator"])]
    return per, glob
