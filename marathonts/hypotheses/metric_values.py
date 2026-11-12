"""Metric values by slice: the measured values behind the rankings → `reports/METRIC_VALUES.md` and
`artifacts/<profile>/metric_values/*.parquet`.

The rankings and tests (LEADERBOARD.md, OVERALL.md, REPORT.md) report ranks, effect sizes and verdicts; this
report gives the values of the metrics themselves.

* Fidelity — the core metrics (`leaderboard.CORE_METRICS`): per real reference (val, train, OOT) a table method ×
  metric, the median over datasets of the median over seeds; against the primary reference, per metric a table
  method × dataset. The row `real` is the real OOT part scored as a series (seed 0): the value a method would have
  if it reproduced held-out real data; against OOT it is compared with itself and is left out.
* Utility — the primary metric of each task (`catalog.PRIMARY_METRIC`): per model and test split a table method ×
  task with TRTR (`real`, trained on real train) as the first row, the median over datasets of the median over
  seeds; the pre-specified cells (`questions.CONFIRMATORY_CELLS`) per dataset. Values are measured cells only:
  cells a method's series could not train (imputed in the rankings, `Config.utility_fail_penalty`) are left out
  and counted in a separate table.

Every value of every metric, reference, task, model and split (median and interquartile range over seeds) is in
`fidelity.parquet` and `utility.parquet` of `metric_values/`. Pairs left out for leakage (`Config.leaked`) are
empty cells.

    python -m marathonts.hypotheses.metric_values --profile min
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from marathonts.bench.fidelity import ORIENT, split_ref

from . import catalog as C
from . import leaderboard as LB

REAL = "real"


def _arrow(orient: int) -> str:
    return "↑" if orient > 0 else "↓"


def _seed_stats(df: pd.DataFrame, keys: list[str], cols: list[str]) -> pd.DataFrame:
    """Median and interquartile range over seeds of `cols` per `keys`."""
    g = df.groupby(keys)[cols]
    med, q1, q3 = g.median(), g.quantile(0.25), g.quantile(0.75)
    return pd.concat({"median": med, "iqr": q3 - q1}, axis=1)


def _methods(present, cfg) -> list[str]:
    """Methods of the tables, without the length-matched variants; `real` first."""
    ms = sorted(m for m in set(present) if m != REAL and "@" not in str(m))
    return ([REAL] if REAL in set(present) else []) + ms


def fidelity_values(fid: pd.DataFrame, cfg) -> dict:
    """{"long": per (dataset, method, metric, reference) median / IQR over seeds of every fidelity metric,
    "by_ref": {reference: method × core metric}, "by_dataset": {core metric: method × dataset}}."""
    if fid is None or not len(fid):
        return {"long": pd.DataFrame(), "by_ref": {}, "by_dataset": {}}
    primary = cfg.fidelity_ref
    cols = [c for c in fid.columns if c in ORIENT]
    df = fid[~fid["method"].astype(str).str.contains("@")]
    st = _seed_stats(df, ["dataset", "method"], cols)
    long = (st.stack(level=1, future_stack=True).rename_axis(["dataset", "method", "column"]).reset_index())
    long[["metric", "reference"]] = [split_ref(c, primary) for c in long["column"]]
    long = long.drop(columns="column")[["dataset", "method", "metric", "reference", "median", "iqr"]]
    core = [m for ms in LB.CORE_METRICS.values() for m in ms]
    methods = _methods(df["method"], cfg)
    refs = [primary] + [r for r in cfg.fidelity_extra_refs if r != primary]
    by_ref = {}
    for r in refs:
        sub = long[(long["reference"] == r) & long["metric"].isin(core)]
        if not len(sub):
            continue
        t = sub.groupby(["method", "metric"])["median"].median().unstack()
        t = t.reindex(index=[m for m in methods if not (m == REAL and r == "oot")],
                      columns=[m for m in core if m in t.columns])
        t.columns = [f"{m} {_arrow(ORIENT.get(m, -1))}" for m in t.columns]
        by_ref[r] = t
    by_ds = {}
    for m in core:
        sub = long[(long["reference"] == primary) & (long["metric"] == m)]
        if len(sub):
            by_ds[m] = sub.pivot_table(index="method", columns="dataset", values="median").reindex(methods)
    return {"long": long, "by_ref": by_ref, "by_dataset": by_ds}


def utility_values(ut: pd.DataFrame, cfg) -> dict:
    """{"long": per (dataset, method, regime, task, model, split, metric) median / IQR over seeds of every
    measured utility metric, "by_task": {(model, split): method × task, primary metric}, "cells": {(task, model,
    split): method × dataset}, "failed": method × task, number of cells left out}."""
    if ut is None or not len(ut):
        return {"long": pd.DataFrame(), "by_task": {}, "cells": {}, "failed": pd.DataFrame()}
    plain = ut[~ut["task_kind"].isin(["grid", "threshold"]) & ~ut["method"].astype(str).str.contains("@")]
    imputed = plain["imputed"].fillna(False).astype(bool) if "imputed" in plain else pd.Series(False, index=plain.index)
    failed = plain[imputed]
    meas = plain[~imputed].copy()
    meas.loc[meas["regime"] == "R", "method"] = REAL
    metrics = [m for m in C.UT_ORIENT if m in meas.columns]
    keys = ["dataset", "method", "task", "task_kind", "model", "split"]
    st = _seed_stats(meas, keys, metrics)
    long = st.stack(level=1, future_stack=True).rename_axis(keys + ["metric"]).reset_index().dropna(subset=["median"])
    prim = long[[m == C.PRIMARY_METRIC.get(k) for m, k in zip(long["metric"], long["task_kind"])]]
    methods = _methods(prim["method"], cfg)
    kind_of = dict(prim[["task", "task_kind"]].drop_duplicates().itertuples(index=False))
    order = list(LB.UT_CRITERIA)                     # classification kinds first, then regression
    tasks = sorted(kind_of, key=lambda t: (order.index(kind_of[t]) if kind_of[t] in order else len(order), t))
    label = {t: f"{t} ({C.PRIMARY_METRIC[k]} {_arrow(C.UT_ORIENT.get(C.PRIMARY_METRIC[k], -1))})"
             for t, k in prim[["task", "task_kind"]].drop_duplicates().itertuples(index=False)}
    by_task = {}
    for (model, split), g in prim.groupby(["model", "split"]):
        t = g.groupby(["method", "task"])["median"].median().unstack()
        t = t.reindex(index=methods, columns=[x for x in tasks if x in t.columns]).dropna(how="all")
        by_task[(model, split)] = t.rename(columns=label)
    cells = {}
    for task, model, split in _confirmatory_cells():
        g = prim[(prim["task"] == task) & (prim["model"] == model) & (prim["split"] == split)]
        if len(g):
            cells[(task, model, split)] = g.pivot_table(index="method", columns="dataset", values="median").reindex(methods)
    fail = (failed.groupby(["method", "task"]).size().unstack(fill_value=0) if len(failed) else pd.DataFrame())
    return {"long": long, "by_task": by_task, "cells": cells, "failed": fail}


def _confirmatory_cells():
    from .questions import CONFIRMATORY_CELLS

    return CONFIRMATORY_CELLS


def build(T: dict, cfg) -> dict:
    C.configure(cfg)
    return {"fidelity": fidelity_values(T.get("fidelity"), cfg), "utility": utility_values(T.get("utility"), cfg)}


def _nd(df: pd.DataFrame) -> int:
    """Decimals for a table: three, four for values below 0.01."""
    v = df.abs().stack()
    v = v[v > 0]
    return 4 if len(v) and float(v.median()) < 0.01 else 3


def write(res: dict, cfg, out: Path, report_dir: Path | None = None) -> Path:
    """Parquet tables to `out`, the report `METRIC_VALUES.md` to `report_dir` (default `<out>/../reports`)."""
    from marathonts.bench.storage import write_table

    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    report_dir = Path(report_dir) if report_dir else out.parent / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    F, U = res["fidelity"], res["utility"]
    if len(F["long"]):
        write_table(F["long"], out / "fidelity.parquet")
    if len(U["long"]):
        write_table(U["long"], out / "utility.parquet")
    folder = out.name
    L = ["# Metric values", "",
         "Values of the metrics behind the rankings: median over seeds within a dataset; over datasets — the median "
         "of those. ↑ — higher is better, ↓ — lower is better. Empty cell — no value (a pair left out for leakage, "
         "a metric a method has no value of, a model not run on the task). Every metric, reference, task, model "
         f"and split with the interquartile range over seeds — `{folder}/fidelity.parquet`, `{folder}/utility.parquet`; "
         "definitions — METRICS.md.", ""]
    if F["by_ref"]:
        L += ["## Fidelity: core metrics by real reference", "",
              "Median over datasets. `real` — the real OOT part scored as a series (seed 0); against OOT it is "
              "compared with itself and is left out.", ""]
        for r, t in F["by_ref"].items():
            L += [f"### Against {r}", "", LB._md(t, nd=_nd(t)), ""]
    if F["by_dataset"]:
        L += [f"## Fidelity: core metrics by dataset (against {cfg.fidelity_ref})", ""]
        for m, t in F["by_dataset"].items():
            L += [f"### {m} {_arrow(ORIENT.get(m, -1))}", "", LB._md(t, nd=_nd(t)), ""]
    if U["by_task"]:
        L += ["## Utility: primary metric by task", "",
              "TSTR — a model trained on the method's synthetic series only; `real` — TRTR, the same model trained "
              "on real train. Both are tested on the same real rows. Median over datasets of measured cells.", ""]
        mo = {m: i for i, m in enumerate(cfg.models)}
        so = {x: i for i, x in enumerate(cfg.test_splits)}
        for (model, split), t in sorted(U["by_task"].items(), key=lambda kv: (mo.get(kv[0][0], 99), so.get(kv[0][1], 99))):
            L += [f"### Model `{model}`, test split {split}", "", LB._md(t, nd=3), ""]
    if U["cells"]:
        L += ["## Utility: pre-specified cells by dataset", ""]
        for (task, model, split), t in U["cells"].items():
            met = C.PRIMARY_METRIC.get(_task_kind(task), "")
            L += [f"### `{task}`, model `{model}`, test split {split} ({met})", "", LB._md(t, nd=3), ""]
    if len(U["failed"]):
        L += ["## Utility: cells a method's series could not train", "",
              "Number of (dataset, seed, model, split) cells without a measured value — one class in the labels of "
              "the series, no rows or a failed fit; left out above, imputed in the rankings "
              "(HYPOTHESES.md §2).", "", LB._md(U["failed"], nd=0), ""]
    f = report_dir / "METRIC_VALUES.md"
    f.write_text("\n".join(L))
    return f


def _task_kind(task: str) -> str:
    from marathonts.bench import registry as R

    R.load_builtins()
    return R.tasks.get(task).kind


def main(argv=None) -> dict:
    import argparse
    import dataclasses

    from .run import _run_config, add_analysis_args, apply_analysis_args, load_tables

    ap = argparse.ArgumentParser()
    ap.add_argument("--artifacts-dir")
    ap.add_argument("--profile", choices=["min", "mid", "max"], default="min")
    ap.add_argument("--out", help="default: <artifacts>/metric_values (report: <artifacts>/reports)")
    add_analysis_args(ap)
    a = ap.parse_args(argv)
    a.case_method = a.noise_pair = None
    cfg = apply_analysis_args(_run_config(a), a)
    if a.artifacts_dir:
        cfg = dataclasses.replace(cfg, artifacts_dir=Path(a.artifacts_dir))
    res = build(load_tables(cfg), cfg)
    out = Path(a.out) if a.out else Path(cfg.artifacts_dir) / "metric_values"
    f = write(res, cfg, out)
    print(f"metric values → {f}")
    return res


if __name__ == "__main__":
    main()
