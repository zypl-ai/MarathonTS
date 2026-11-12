"""Supplementary check of the gap to real data, RQ5 (a) (not pre-specified): absolute TSTR and TRTR scores, the
utility cells where the transfer ratio is undefined, and a summary of the tests by criterion.

    python -m marathonts.hypotheses.rq5_check --artifacts-dir artifacts/run_h200 [--out-dir <dir>]

RQ5 (a) (`questions.rq5_gap_and_stability`) tests, for each method and criterion, whether the median transfer
ratio over datasets is below 1 (one-sided Wilcoxon over datasets, Benjamini-Hochberg). The transfer ratio
(`catalog.transfer_ratio`) is TSTR / TRTR for higher-is-better scores, TRTR / TSTR for losses and, for ROC AUC,
(TSTR - 0.5) / (TRTR - 0.5), undefined when TRTR is within 0.02 of chance. Here:

* `absolute.parquet` — for every task, downstream model and test split, the primary metric of TRTR (the real
  series; mean over seeds, median over datasets), the median over the methods of their TSTR (mean over seeds,
  median over datasets) and the best method by that TSTR;
* `undefined.parquet` — the ROC AUC cells (dataset, seed, task, model, split) whose ratio is undefined;
* `RQ5_CHECK.md` — the tests of RQ5 (a) by criterion and the tables above.

Written to `<out>/` (default `<artifacts>/supplementary/rq5_check`). CPU only, from the tables of the run.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from marathonts.bench.storage import write_table


def run(art: Path):
    from marathonts.hypotheses.catalog import HIGHER_BETTER, transfer_ratio, utility_long
    from marathonts.hypotheses.leaderboard import ranked_methods
    from marathonts.hypotheses.tie_check import load

    T, cfg = load(art)
    methods = ranked_methods(T, cfg)
    L = utility_long(T["utility"])
    R = transfer_ratio(L)
    R = R[R["method"].isin(methods)]
    cells = R[R["metric"] == "auc"].drop_duplicates(["dataset", "seed", "task", "model", "split"])
    undefined = cells.loc[(cells["trtr"] - 0.5) <= 0.02, ["dataset", "seed", "task", "model", "split", "trtr"]]
    key = ["task", "model", "split", "metric"]
    real = L[(L["method"] == "real") & (L["regime"] == "R")]
    trtr = real.groupby(key + ["dataset"])["value"].mean().groupby(key).median().rename("trtr")
    syn = L[(L["regime"] == "S") & L["method"].isin(methods)]
    per = syn.groupby(key + ["method", "dataset"])["value"].mean().groupby(key + ["method"]).median()
    rows = []
    for k, g in per.groupby(level=key):
        g = g.droplevel(key)
        higher = k[3] in HIGHER_BETTER or k[3] == "auc"
        best = g.idxmax() if higher else g.idxmin()
        rows.append(dict(zip(key, k), trtr=float(trtr.get(k, np.nan)), tstr_median=float(g.median()),
                         tstr_best=float(g[best]), best_method=best, n_methods=len(g),
                         higher_is_better=bool(higher)))
    absolute = pd.DataFrame(rows)
    G = pd.read_parquet(art / "hypotheses" / "RQ5_global.parquet")
    summary = G.groupby("unit").agg(tests=("method", "size"), rejected=("verdict", lambda s: int((s == "worse than real").sum())),
                                    median_ratio_min=("median_ratio", "min"), median_ratio_max=("median_ratio", "max"),
                                    ci_hi_max=("ci_hi", "max"), p_bh_max=("p_below_real_bh", "max"),
                                    datasets_min=("n_datasets", "min"), datasets_max=("n_datasets", "max"))
    info = dict(auc_cells=len(cells), undefined=len(undefined))
    return absolute, undefined, summary, info


def report(absolute, undefined, summary, info, art: Path) -> str:
    by = undefined.groupby(["dataset", "task"]).size().rename("cells").reset_index().sort_values("cells", ascending=False)
    return "\n".join([
        f"# RQ5 check — {art.name}", "",
        "Supplementary, not pre-specified (`python -m marathonts.hypotheses.rq5_check`). See the module docstring.",
        "", "## Tests of RQ5 (a) by criterion", "", summary.to_markdown(floatfmt=".3g"), "",
        "## ROC AUC cells with an undefined ratio", "",
        f"{info['undefined']} of {info['auc_cells']} cells (dataset × seed × task × model × split; "
        f"{info['undefined'] / info['auc_cells']:.1%}): the real series is within 0.02 of chance.", "",
        by.to_markdown(index=False), "",
        "## Absolute scores", "",
        "Primary metric; TRTR: the real series; TSTR: median over the methods, and the best method.", "",
        absolute.to_markdown(index=False, floatfmt=".3g"), ""])


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--artifacts-dir", required=True)
    ap.add_argument("--out-dir")
    a = ap.parse_args(argv)
    art = Path(a.artifacts_dir)
    out = Path(a.out_dir) if a.out_dir else art / "supplementary" / "rq5_check"
    absolute, undefined, summary, info = run(art)
    out.mkdir(parents=True, exist_ok=True)
    write_table(absolute, out / "absolute.parquet", keep64=["trtr", "tstr_median", "tstr_best"])
    write_table(undefined, out / "undefined.parquet")
    text = report(absolute, undefined, summary, info, art)
    (out / "RQ5_CHECK.md").write_text(text)
    print(text)


if __name__ == "__main__":
    main()
