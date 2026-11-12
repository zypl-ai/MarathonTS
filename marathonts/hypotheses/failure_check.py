"""Supplementary check of the utility cells a synthetic series could not train (not pre-specified): how many
there are, where, and why.

    python -m marathonts.hypotheses.failure_check --artifacts-dir artifacts/run_h200 --series-dir <run>/series \\
        [--out-dir <dir>]

The missing TSTR cells are found as in the analysis (`catalog.impute_failed_utility`: every task × model ×
split fitted on real train, for every method with a unit on that dataset and seed). For each of them the labels
of the synthetic series are rebuilt with the thresholds of the task (`bench.tasks.make_xy`), and the reason is:

* `one_class` — the labels of the synthetic series have one class: the series cannot train the task, whatever
  the model (an intrinsic property of the series, e.g. a smooth median forecast that never crosses the
  threshold);
* `no_rows` — the series gives no usable rows;
* `other` — the labels have two or more classes, so the fit itself failed or was not run (a recoverable
  failure of training or infrastructure).

Output: `<out>/failure_check.parquet` (one row per missing cell) and `<out>/FAILURE_CHECK.md`
(default `<artifacts>/supplementary/failure_check`). CPU only; the series of a run are published with it
(Hugging Face: every dataset but ETT and PJM).
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from marathonts.bench import registry as R
from marathonts.bench.config import Config
from marathonts.bench.storage import write_table
from marathonts.bench.tasks import make_xy, target_params
from marathonts.hypotheses.catalog import impute_failed_utility


def reason(series: pd.DataFrame, task, prm: dict) -> str:
    _, y, _ = make_xy(series["value"].to_numpy(float), series["how"].to_numpy(int), task, prm)
    if len(y) == 0:
        return "no_rows"
    return "one_class" if len(np.unique(y)) < 2 else "other"


def run(artifacts: Path, series_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    import marathonts.bench.tasks  # noqa: F401  (registers the tasks)

    cfg = Config()
    ut = pd.read_parquet(artifacts / "tables" / "utility.parquet")
    full = impute_failed_utility(ut)
    S = full[(full["regime"] == "S") & ~full["method"].astype(str).str.contains("@")
             & ~full["task_kind"].isin(["grid", "threshold"])]
    miss = S[S["imputed"] == True][["dataset", "seed", "method", "task", "task_kind", "model", "split"]]  # noqa: E712
    why = {}
    for (ds, m, sd, tn), _ in miss.groupby(["dataset", "method", "seed", "task"]):
        f = series_dir / ds / m / f"seed{int(sd)}.parquet"
        if not f.exists():
            why[(ds, m, sd, tn)] = "series_unavailable"
            continue
        task = R.tasks.get(tn)
        why[(ds, m, sd, tn)] = reason(pd.read_parquet(f, columns=["value", "how"]), task, target_params(cfg, ds, task))
    miss = miss.assign(reason=[why[(r.dataset, r.method, r.seed, r.task)] for r in miss.itertuples()])
    cells = S.assign(missing=S["imputed"] == True).groupby(["method", "task_kind"]).agg(  # noqa: E712
        cells=("missing", "size"), missing=("missing", "sum")).reset_index()
    return miss, cells


def report(miss: pd.DataFrame, cells: pd.DataFrame, artifacts: Path) -> str:
    tot, nm = int(cells["cells"].sum()), int(cells["missing"].sum())
    by_m = miss.groupby(["method", "reason"]).size().unstack(fill_value=0)
    by_m["cells"] = cells.groupby("method")["cells"].sum().reindex(by_m.index)
    by_t = miss.groupby(["task", "reason"]).size().unstack(fill_value=0)
    by_k = cells.groupby("task_kind")[["cells", "missing"]].sum()
    return "\n".join([
        f"# Failure check — {artifacts.name}", "",
        "Supplementary, not pre-specified (`python -m marathonts.hypotheses.failure_check`). Missing TSTR cells "
        "(task × model × split that a method's series could not train) and their reason: `one_class` — the labels "
        "of the synthetic series have one class (intrinsic); `no_rows` — no usable rows; `other` — two or more "
        "classes, the fit failed or was not run (recoverable).", "",
        f"Missing: {nm} of {tot} TSTR cells ({nm / tot:.2%}).", "",
        "By task kind:", "", by_k.to_markdown(), "",
        "By method and reason (`cells`: all TSTR cells of the method):", "", by_m.to_markdown(), "",
        "By task and reason:", "", by_t.to_markdown(), ""])


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--artifacts-dir", required=True)
    ap.add_argument("--series-dir", help="default: <artifacts>/series")
    ap.add_argument("--out-dir", help="default: <artifacts>/supplementary/failure_check")
    a = ap.parse_args(argv)
    art = Path(a.artifacts_dir)
    out = Path(a.out_dir) if a.out_dir else art / "supplementary" / "failure_check"
    miss, cells = run(art, Path(a.series_dir) if a.series_dir else art / "series")
    out.mkdir(parents=True, exist_ok=True)
    write_table(miss, out / "failure_check.parquet")
    text = report(miss, cells, art)
    (out / "FAILURE_CHECK.md").write_text(text)
    print(text)


if __name__ == "__main__":
    main()
