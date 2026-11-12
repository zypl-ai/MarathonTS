"""Supplementary check of the confirmatory test C1 (not pre-specified): the method-by-dataset eligibility mask,
a permutation calibration of the Friedman test and its sensitivity to the design.

    python -m marathonts.hypotheses.c1_check --artifacts-dir artifacts/run_h200 \\
        [--restrict-to artifacts/run_l4] [--n-perm 100000] [--out-dir <dir>]

C1 (`questions.confirmatory_rq`) is a Friedman test over the ranked methods of the default ranking with the
datasets as blocks, in each confirmatory cell. The design is made complete by `stats.complete_blocks`: a
method without a value on some dataset (a pretrained model left out on a dataset of its training data,
`Config.leaked`) drops out of the test and every dataset stays (or the incomplete datasets drop out, whichever
keeps more cells). Here, for each cell:

* the mask — every ranked method × dataset: whether the cell has a value, whether it is left out for leakage,
  and whether it enters C1;
* the pre-specified test (chi-square approximation) and its permutation p: the values are permuted within each
  dataset (the null of exchangeable methods within a block), the statistic is the sum of squared rank sums
  (equivalent to Friedman's under the permutation), p = (1 + #{perm >= obs}) / (1 + n_perm);
* sensitivity: (a) every ranked method with the incomplete datasets kept, Skillings-Mack test (Skillings and
  Mack, 1981; equals Friedman's statistic on a complete design), permutation within the observed cells of
  each dataset; (b) every ranked method on the datasets where all of them have a value; (c) with
  `--restrict-to`, the methods that the other run also ranks;
* the Holm correction of the ten confirmatory tests recomputed with the permutation p of C1.

Written to `<out>/` (default `<artifacts>/supplementary/c1_check`): `mask.parquet`, `tests.parquet` and
`C1_CHECK.md`. CPU only, from the tables of the run.
"""
from __future__ import annotations

import argparse
import dataclasses
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats as sps

from marathonts.bench import registry as R
from marathonts.bench.storage import write_table


def _ranks(X: np.ndarray) -> np.ndarray:
    """Average ranks within each row over the observed (non-NaN) cells; NaN stays NaN."""
    out = np.full(X.shape, np.nan)
    for i, row in enumerate(X):
        ok = ~np.isnan(row)
        out[i, ok] = sps.rankdata(row[ok])
    return out


def skillings_mack(X: np.ndarray) -> float:
    """Skillings-Mack statistic of a blocks × treatments table with missing cells (NaN)."""
    Rk = _ranks(X)
    k_i = (~np.isnan(X)).sum(axis=1)
    w = np.sqrt(12.0 / (k_i + 1.0))
    A = np.nansum(w[:, None] * (Rk - (k_i[:, None] + 1.0) / 2.0), axis=0)
    obs = (~np.isnan(X)).astype(float)
    lam = obs.T @ obs
    np.fill_diagonal(lam, 0.0)
    Sig = -lam
    np.fill_diagonal(Sig, lam.sum(axis=1))
    return float(A @ np.linalg.pinv(Sig) @ A)


def _sum_sq(Rk: np.ndarray) -> float:
    return float((np.nansum(Rk, axis=0) ** 2).sum())


def permutation_p(X: np.ndarray, stat, n_perm: int, rng) -> float:
    """Permutation p: the observed values are permuted within each block (missing cells stay missing)."""
    obs = stat(X)
    ge, Y = 0, X.copy()
    idx = [np.where(~np.isnan(r))[0] for r in X]
    for _ in range(n_perm):
        for i, ix in enumerate(idx):
            Y[i, ix] = X[i, rng.permutation(ix)]
        ge += stat(Y) >= obs - 1e-9 * abs(obs)
    return (1 + ge) / (1 + n_perm)


def friedman_perm(X: np.ndarray, n_perm: int, rng) -> float:
    """Permutation p of Friedman's test on a complete table, vectorised over permutations."""
    Rk = _ranks(X)
    n, k = Rk.shape
    obs = _sum_sq(Rk)
    ge, done, chunk = 0, 0, 5000
    while done < n_perm:
        m = min(chunk, n_perm - done)
        order = np.argsort(rng.random((m, n, k)), axis=2)
        P = np.take_along_axis(np.broadcast_to(Rk, (m, n, k)), order, axis=2)
        ge += int(((P.sum(axis=1) ** 2).sum(axis=1) >= obs - 1e-9 * obs).sum())
        done += m
    return (1 + ge) / (1 + n_perm)


def cell_tables(T, cfg):
    from marathonts.hypotheses import leaderboard as LB
    from marathonts.hypotheses import questions as Q

    cm = LB.leaderboard_methods(T, dataclasses.replace(cfg, rank_exclude=None))
    U = Q.tstr_primary(T)
    out = {}
    for task, model, split in Q.CONFIRMATORY_CELLS:
        kind = R.tasks.get(task).kind if task in R.tasks else "clf"
        unit = f"{task}|{model}|S|{split}|{Q.PRIMARY_METRIC[kind]}"
        L = U[U["unit"] == unit]
        out[f"{task}|{model}|{split}"] = L[L["method"].isin(cm)].groupby(["dataset", "method"])["value"].mean().unstack()
    return cm, out


def run(art: Path, restrict: Path | None, n_perm: int):
    from marathonts.hypotheses import stats as S
    from marathonts.hypotheses.leaderboard import leaderboard_methods
    from marathonts.hypotheses.tie_check import load

    R.load_builtins()
    other = None
    if restrict is not None:
        T2, cfg2 = load(restrict)
        other = set(leaderboard_methods(T2, dataclasses.replace(cfg2, rank_exclude=None)))
    T, cfg = load(art)
    cm, cells = cell_tables(T, cfg)
    datasets = sorted(set(T["fidelity"]["dataset"]))
    leaked = {m: set(v) for m, v in (cfg.leaked or {}).items()}
    rng = np.random.default_rng(0)
    conf = pd.read_parquet(art / "hypotheses" / "confirmatory.parquet")
    masks, tests = [], []
    for cell, D0 in cells.items():
        D0 = D0.reindex(index=datasets, columns=sorted(cm))
        D = S.complete_blocks(D0)
        for m in D0.columns:
            for ds in D0.index:
                masks.append(dict(cell=cell, method=m, dataset=ds, has_value=bool(pd.notna(D0.at[ds, m])),
                                  leaked=ds in leaked.get(m, set()), in_c1=bool(m in D.columns and ds in D.index)))
        variants = [("pre-specified: complete methods", D, "friedman")]
        variants.append(("(a) every ranked method, incomplete blocks", D0.dropna(axis=1, how="all"), "skillings_mack"))
        variants.append(("(b) every ranked method, complete datasets", D0.dropna(), "friedman"))
        if other is not None:
            Dc = D0[[m for m in D0.columns if m in other]]
            variants.append((f"(c) methods of {restrict.name}", S.complete_blocks(Dc), "friedman"))
        for name, X, kind in variants:
            A = X.to_numpy(float)
            n, k = A.shape
            if kind == "friedman":
                chi = float(sps.friedmanchisquare(*A.T).statistic) if n >= 3 and k >= 3 else np.nan
                p_chi = float(sps.friedmanchisquare(*A.T).pvalue) if n >= 3 and k >= 3 else np.nan
                p_perm = friedman_perm(A, n_perm, rng) if n >= 3 and k >= 3 else np.nan
            else:
                chi = skillings_mack(A)
                p_chi = float(sps.chi2.sf(chi, k - 1))
                p_perm = permutation_p(A, skillings_mack, max(n_perm // 20, 2000), rng)
            tests.append(dict(cell=cell, variant=name, test=kind, n_datasets=n, n_methods=k,
                              missing_cells=int(np.isnan(A).sum()), statistic=chi, p_chi2=p_chi, p_perm=p_perm,
                              methods=", ".join(X.columns)))
    tests = pd.DataFrame(tests)
    # Holm over the ten confirmatory tests with the permutation p of C1
    c = conf.copy()
    pre = tests[tests["variant"].str.startswith("pre-specified")].set_index("cell")["p_perm"]
    is_c1 = c["test"].str.startswith("C1")
    c.loc[is_c1, "p_two_sided"] = c.loc[is_c1, "cell"].map(pre).to_numpy()
    c["p_holm_perm"] = S.holm(c["p_two_sided"].fillna(1.0).to_numpy())
    holm = c[["test", "cell", "comparison", "p_holm", "p_holm_perm", "verdict"]]
    # a complete design must give Skillings-Mack = Friedman
    A = cells[next(iter(cells))].dropna().to_numpy(float)
    n, k = A.shape
    fr = 12.0 / (n * k * (k + 1)) * _sum_sq(_ranks(A)) - 3.0 * n * (k + 1)   # Friedman without the tie correction
    check = abs(skillings_mack(A) - fr)
    return pd.DataFrame(masks), tests, holm, dict(sm_vs_friedman=check, n_perm=n_perm)


def report(mask, tests, holm, info, art: Path) -> str:
    ex = mask[~mask["in_c1"]]
    drop = ex.groupby(["cell", "method"]).agg(datasets_without_value=("has_value", lambda s: int((~s).sum())),
                                             leaked=("leaked", "sum")).reset_index()
    t = tests.drop(columns="methods")
    return "\n".join([
        f"# C1 check — {art.name}", "",
        "Supplementary, not pre-specified (`python -m marathonts.hypotheses.c1_check`). See the module docstring.",
        "", "## Eligibility", "",
        "Ranked methods that do not enter C1 (every one of their cells is out; `leaked`: datasets left out for "
        "leakage):", "", drop.to_markdown(index=False), "",
        "Methods of each test:", "",
        tests[["cell", "variant", "methods"]].to_markdown(index=False), "",
        "## Tests", "",
        f"Permutations: {info['n_perm']} (Skillings-Mack: {max(info['n_perm'] // 20, 2000)}). Check: on a complete "
        f"design Skillings-Mack equals Friedman without the tie correction (difference {info['sm_vs_friedman']:.2g}).", "",
        t.to_markdown(index=False, floatfmt=".3g"), "",
        "## Holm over the confirmatory family with the permutation p of C1", "",
        holm.to_markdown(index=False, floatfmt=".3g"), ""])


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--artifacts-dir", required=True)
    ap.add_argument("--restrict-to", help="artifacts of another run: C1 also on the methods both runs rank")
    ap.add_argument("--n-perm", type=int, default=100000)
    ap.add_argument("--out-dir")
    a = ap.parse_args(argv)
    art = Path(a.artifacts_dir)
    out = Path(a.out_dir) if a.out_dir else art / "supplementary" / "c1_check"
    mask, tests, holm, info = run(art, Path(a.restrict_to) if a.restrict_to else None, a.n_perm)
    out.mkdir(parents=True, exist_ok=True)
    write_table(mask, out / "mask.parquet")
    write_table(tests, out / "tests.parquet", keep64=["statistic", "p_chi2", "p_perm"])
    text = report(mask, tests, holm, info, art)
    (out / "C1_CHECK.md").write_text(text)
    print(text)


if __name__ == "__main__":
    main()
