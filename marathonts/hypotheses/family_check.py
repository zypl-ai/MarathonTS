"""Supplementary check of the fidelity-utility associations of RQ4 by generator family (not pre-specified).

    python -m marathonts.hypotheses.family_check --artifacts-dir artifacts/run_h200 \\
        [--restrict-to artifacts/run_l4] [--out-dir <dir>]

RQ4 correlates, within a dataset, a fidelity metric with the transfer ratio of a utility criterion across the
methods of a run, and tests the correlations over datasets (Wilcoxon, Benjamini-Hochberg over every pair of a
metric and a criterion). Several methods share a generator (every assembler of a pool, the seam-processing
variants of an assembler), so they are not independent observations. A family is the generator a method's
series come from (`overall.generator`); the zEDGE pool and the two zEDGE_TS long-series paths come from one
generator and form one family (`MERGE`). Three checks:

* leave one family out — RQ4 recomputed without each family in turn: how many pairs are predictive, and how
  many of the pre-specified predictive pairs stay predictive whatever family is left out;
* selection outside the family — for each criterion and each held-out family, the metric with the largest
  median correlation on the other families is chosen; on each dataset, the share of the pairs (a method of the
  held-out family, a method of another family) that this metric orders as the transfer ratio does (ties count
  one half; 0.5 is chance) is computed. Median over datasets, a 95 % bootstrap interval over datasets and a
  one-sided Wilcoxon test against 0.5;
* `--restrict-to <run>` — RQ4 on the methods that the other run also has (the main run on the methods of the
  replication run separates the set of methods from the hardware).

Written to `<out>/` (default `<artifacts>/supplementary/family_check`): `lofo.parquet`, `selection.parquet`,
`restricted.parquet` (with `--restrict-to`) and `FAMILY_CHECK.md`. CPU only, from the tables of the run.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from marathonts.bench import registry as R
from marathonts.bench.storage import write_table

MERGE = {"zedge_ts": "zedge", "zedge_ts_long": "zedge", "zedge_ts_ar": "zedge"}
N_BOOT = 2000


def family(m: str) -> str:
    from marathonts.hypotheses.overall import generator

    g = generator(m)
    return MERGE.get(g, g)


def inputs(T, cfg, methods):
    """The oriented fidelity table and the transfer ratios of RQ4 (`questions.rq4_fidelity_predicts_utility`)."""
    from marathonts.bench.fidelity import ORIENT
    from marathonts.hypotheses import questions as Q
    from marathonts.hypotheses.catalog import fidelity_long

    Ub = Q.utility_by_criterion(T, methods)
    F = fidelity_long(T["fidelity"])
    F = F[F["method"].isin(methods) & F["unit"].isin(Q.fid_units(("train", "val", "oot"), cfg.fidelity_ref))]
    Fm = F.groupby(["dataset", "method", "unit"])["value"].mean().unstack("unit")
    Fm = Fm * pd.Series(ORIENT).reindex(Fm.columns).to_numpy()
    return Fm, Ub


def rq4(Fm: pd.DataFrame, Ub: pd.DataFrame, methods, alpha: float) -> pd.DataFrame:
    """RQ4 on a subset of methods, as in the pre-specified analysis."""
    from marathonts.hypotheses import stats as S

    J = Fm.join(Ub, how="inner")
    J = J[J.index.get_level_values("method").isin(methods)]
    per = []
    for ds, g in J.groupby(level="dataset"):
        if len(g) < 5:
            continue
        for crit in Ub.columns:
            for u in Fm.columns:
                j = g[[u, crit]].dropna().rank()
                if len(j) >= 5 and j[u].nunique() > 1:
                    per.append((u, crit, float(j[u].corr(j[crit]))))
    P = pd.DataFrame(per, columns=["unit", "criterion", "rho"])
    rows = []
    for (u, crit), g in P.groupby(["unit", "criterion"]):
        r = g["rho"].dropna().to_numpy()
        if len(r) < 3:
            continue
        rows.append(dict(unit=u, criterion=crit, n_datasets=len(r), median_rho=float(np.median(r)),
                         p_two_sided=S.wilcoxon(r)))
    G = pd.DataFrame(rows, columns=["unit", "criterion", "n_datasets", "median_rho", "p_two_sided"])
    if not len(G):                       # fewer than five methods left on every dataset: nothing to test
        return G.assign(p_bh=pd.Series(dtype=float), predictive=pd.Series(dtype=bool))
    G["p_bh"] = S.bh(G["p_two_sided"].to_numpy())
    G["predictive"] = (G["p_bh"] < alpha) & (G["median_rho"] > 0)
    return G


def concordance(x: np.ndarray, y: np.ndarray, inside: np.ndarray) -> float:
    """Share of the pairs (inside, outside) ordered alike by x and y; ties in x count one half."""
    i, o = np.where(inside)[0], np.where(~inside)[0]
    if not len(i) or not len(o):
        return np.nan
    dx = np.sign(x[i][:, None] - x[o][None, :])
    dy = np.sign(y[i][:, None] - y[o][None, :])
    ok = dy != 0
    if not ok.any():
        return np.nan
    s = np.where(dx == 0, 0.5, (dx == dy).astype(float))
    return float(s[ok].mean())


def selection(Fm, Ub, methods, fam: dict, alpha: float, rng) -> pd.DataFrame:
    from marathonts.hypotheses import stats as S

    J = Fm.join(Ub, how="inner")
    J = J[J.index.get_level_values("method").isin(methods)]
    rows = []
    for F in sorted(set(fam.values())):
        rest = [m for m in methods if fam[m] != F]
        G = rq4(Fm, Ub, rest, alpha)
        for crit, g in G.groupby("criterion"):
            best = g.sort_values(["median_rho", "unit"], ascending=[False, True], kind="stable").iloc[0]
            u = best["unit"]
            per = []
            for ds, d in J.groupby(level="dataset"):
                d = d[[u, crit]].dropna()
                ms = d.index.get_level_values("method")
                c = concordance(d[u].to_numpy(float), d[crit].to_numpy(float),
                                np.array([fam[m] == F for m in ms]))
                if not np.isnan(c):
                    per.append(c)
            per = np.array(per)
            if not len(per):
                continue
            boot = np.median(per[rng.integers(0, len(per), (N_BOOT, len(per)))], axis=1)
            rows.append(dict(held_out=F, n_methods=sum(fam[m] == F for m in methods), criterion=crit,
                             metric=u, rho_on_rest=float(best["median_rho"]), n_datasets=len(per),
                             concordance=float(np.median(per)), ci_lo=float(np.quantile(boot, 0.025)),
                             ci_hi=float(np.quantile(boot, 0.975)),
                             p_above_chance=S.wilcoxon(per - 0.5, "greater") if np.any(per != 0.5) else 1.0))
    return pd.DataFrame(rows)


def run(art: Path, restrict: Path | None):
    from marathonts.hypotheses.leaderboard import ranked_methods
    from marathonts.hypotheses.tie_check import load

    R.load_builtins()
    T, cfg = load(art)
    methods = ranked_methods(T, cfg)
    fam = {m: family(m) for m in methods}
    Fm, Ub = inputs(T, cfg, methods)
    main = rq4(Fm, Ub, methods, cfg.alpha)
    key = ["unit", "criterion"]
    pred = main.loc[main["predictive"], key]
    lofo = []
    keep = pd.Series(True, index=pd.MultiIndex.from_frame(pred))
    for F in sorted(set(fam.values())):
        G = rq4(Fm, Ub, [m for m in methods if fam[m] != F], cfg.alpha)
        still = pred.merge(G[key + ["predictive"]], on=key, how="left")["predictive"].fillna(False).to_numpy(bool)
        keep &= still
        lofo.append(dict(left_out=F, n_methods_left_out=sum(fam[m] == F for m in methods),
                         methods_left=sum(fam[m] != F for m in methods), predictive=int(G["predictive"].sum()),
                         of_prespecified_still=int(still.sum()),
                         median_rho=float(G["median_rho"].median())))
    lofo = pd.DataFrame(lofo)
    sel = selection(Fm, Ub, methods, fam, cfg.alpha, np.random.default_rng(0))
    res = None
    if restrict is not None:
        T2, cfg2 = load(restrict)
        common = sorted(set(methods) & set(ranked_methods(T2, cfg2)))
        G = rq4(Fm, Ub, common, cfg.alpha)
        res = G.assign(restricted_to=restrict.name)
        rinfo = dict(n=len(common), predictive=int(G["predictive"].sum()), median_rho=float(G["median_rho"].median()),
                     at_min_p=int((G["p_two_sided"] <= G["p_two_sided"].min() + 1e-12).sum()),
                     min_p=float(G["p_two_sided"].min()), families=len({fam[m] for m in common}))
    T, cfg = load(art)  # restore the configuration of this run
    info = dict(methods=len(methods), families=len(set(fam.values())),
                family_sizes={F: sum(v == F for v in fam.values()) for F in sorted(set(fam.values()))},
                pairs=len(main), predictive=int(main["predictive"].sum()), stable=int(keep.sum()),
                median_rho=float(main["median_rho"].median()), restricted=rinfo if restrict is not None else None)
    return lofo, sel, res, info


def report(lofo, sel, res, info, art: Path) -> str:
    s = sel.assign(above_chance=sel["ci_lo"] > 0.5)
    by_f = s.groupby("held_out").agg(criteria=("criterion", "size"), median_concordance=("concordance", "median"),
                                     interval_above_chance=("above_chance", "sum"))
    out = [f"# Family check — {art.name}", "",
           "Supplementary, not pre-specified (`python -m marathonts.hypotheses.family_check`). RQ4 by generator "
           "family (see the module docstring); the zEDGE pool and the zEDGE_TS paths form one family.", "",
           f"Methods: {info['methods']}; families: {info['families']} "
           f"({', '.join(f'{k}: {v}' for k, v in info['family_sizes'].items())}). Pairs of a metric and a "
           f"criterion: {info['pairs']}; predictive (pre-specified): {info['predictive']}; median of the median "
           f"correlations: {info['median_rho']:.2f}.", "",
           "## Leave one family out", "",
           f"Pre-specified predictive pairs that stay predictive whatever family is left out: {info['stable']} of "
           f"{info['predictive']}.", "", lofo.to_markdown(index=False, floatfmt=".2f"), "",
           "## Selection outside the family", "",
           "For each criterion and held-out family: the metric with the largest median correlation on the other "
           "families, and on the held-out family the share of the pairs (held-out method, other method) ordered "
           "as by the transfer ratio (median over datasets; 95 % bootstrap interval over datasets; one-sided "
           "Wilcoxon against 0.5).", "",
           "By held-out family (`interval_above_chance`: criteria whose interval lies above 0.5):", "",
           by_f.to_markdown(floatfmt=".2f"), "", "All:", "", sel.to_markdown(index=False, floatfmt=".3g"), ""]
    if info["restricted"]:
        r = info["restricted"]
        out += ["## Methods of the other run", "",
                f"RQ4 on the {r['n']} methods ({r['families']} families) that `{res['restricted_to'].iloc[0]}` also "
                f"has: {r['predictive']} predictive pairs; median of the median correlations {r['median_rho']:.2f}; "
                f"{r['at_min_p']} pairs at the smallest p ({r['min_p']:.4f}).", ""]
    return "\n".join(out)


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--artifacts-dir", required=True)
    ap.add_argument("--restrict-to", help="artifacts of another run: RQ4 also on the methods both runs have")
    ap.add_argument("--out-dir")
    a = ap.parse_args(argv)
    art = Path(a.artifacts_dir)
    out = Path(a.out_dir) if a.out_dir else art / "supplementary" / "family_check"
    lofo, sel, res, info = run(art, Path(a.restrict_to) if a.restrict_to else None)
    out.mkdir(parents=True, exist_ok=True)
    write_table(lofo, out / "lofo.parquet", keep64=["median_rho"])
    write_table(sel, out / "selection.parquet", keep64=["concordance", "ci_lo", "ci_hi", "rho_on_rest"])
    if res is not None:
        write_table(res, out / "restricted.parquet", keep64=["median_rho"])
    text = report(lofo, sel, res, info, art)
    (out / "FAMILY_CHECK.md").write_text(text)
    print(text)


if __name__ == "__main__":
    main()
