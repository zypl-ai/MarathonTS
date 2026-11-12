"""Supplementary check of the confirmatory test C3 without the task-aware assembler zseries (not pre-specified).

    python -m marathonts.hypotheses.c3_check --artifacts-dir artifacts/run_h200 [--out-dir <dir>]

C3 (`questions.confirmatory_rq`) is the main effect of window selection: the mean of every ranked selection
strategy of the pool against its random path, in each confirmatory cell. zseries uses the thresholds of task
U2.1, the classification cell of the family; no open assembler does. Here C3 is recomputed exactly as in the
pre-specified analysis, once with every selection strategy (it reproduces the published test) and once without
the zseries assembler (the open assemblers only), and the Holm correction of the ten confirmatory tests is
recomputed with the second C3. C4 cannot be checked in this way: in profile `min` the joiners are applied to the
path of zseries only.

Written to `<out>/` (default `<artifacts>/supplementary/c3_check`): `c3.parquet` and `C3_CHECK.md`. CPU only,
from the tables of the run.
"""
from __future__ import annotations

import argparse
import dataclasses
from pathlib import Path

import numpy as np
import pandas as pd

from marathonts.bench import registry as R
from marathonts.bench.storage import write_table

EXCLUDED_ASSEMBLERS = ("zseries",)


def run(art: Path):
    from marathonts.hypotheses import leaderboard as LB
    from marathonts.hypotheses import questions as Q
    from marathonts.hypotheses import stats as S
    from marathonts.hypotheses.catalog import _ut_orient
    from marathonts.hypotheses.tie_check import load

    R.load_builtins()
    T, cfg = load(art)
    methods = LB.ranked_methods(T, cfg)
    U = Q.tstr_primary(T)
    grid = Q.pool_grid(methods)
    cm = set(LB.leaderboard_methods(T, dataclasses.replace(cfg, rank_exclude=None)))
    rand = grid.get(("random", None))
    rows = []
    for task, model, split in Q.CONFIRMATORY_CELLS:
        kind = R.tasks.get(task).kind if task in R.tasks else "clf"
        unit = f"{task}|{model}|S|{split}|{Q.PRIMARY_METRIC[kind]}"
        L = U[U["unit"] == unit]
        cell = f"{task}|{model}|{split}"
        o = _ut_orient(L)
        W = Q._wide(L)
        A = [m for m in Q.selection_methods(grid) if m in cm and m in W.columns]
        open_ = [m for m in A if not (m in R.methods and R.methods.get(m).assembler in EXCLUDED_ASSEMBLERS)]
        for name, cols in (("pre-specified: every selection strategy", A), ("without zseries", open_)):
            gl = [Q._contrast(L, o, cfg, Q._d(W, o, cols, [rand]), "selection")[1]] if cols and rand in W.columns else []
            r = Q._conf_row("C3 selection", cell, "optimised selection (mean) vs random", gl)
            rows.append(dict(cell=cell, variant=name, n_assemblers=len(cols), assemblers=", ".join(cols),
                             **{k: r.get(k) for k in ("n_datasets", "median_z", "p_two_sided", "p_equiv")}))
    C = pd.DataFrame(rows)
    conf = pd.read_parquet(art / "hypotheses" / "confirmatory.parquet")
    pre = C[C["variant"].str.startswith("pre")].set_index("cell")["p_two_sided"]
    reproduces = bool(np.allclose(conf.loc[conf["test"].str.startswith("C3"), "p_two_sided"].to_numpy(float),
                                  conf.loc[conf["test"].str.startswith("C3"), "cell"].map(pre).to_numpy(float)))
    c = conf.copy()
    alt = C[C["variant"] == "without zseries"].set_index("cell")
    is3 = c["test"].str.startswith("C3")
    for col in ("p_two_sided", "p_equiv", "median_z"):
        c.loc[is3, col] = c.loc[is3, "cell"].map(alt[col]).to_numpy()
    c["p_holm"] = S.holm(c["p_two_sided"].fillna(1.0).to_numpy())
    c["p_equiv_holm"] = S.holm(c["p_equiv"].where(c["directional"]).fillna(1.0).to_numpy())
    verdict = []
    for r in c.itertuples():
        if pd.isna(r.p_two_sided):
            verdict.append("missing")
        elif not r.directional:
            verdict.append("differ" if r.p_holm < cfg.alpha else "inconclusive")
        elif r.p_holm < cfg.alpha and abs(r.median_z) > 1:
            verdict.append("better" if r.median_z > 0 else "worse")
        elif r.p_equiv_holm < cfg.alpha:
            verdict.append("same")
        else:
            verdict.append("inconclusive")
    c["verdict_without_zseries"] = verdict
    holm = c[["test", "cell", "comparison", "p_holm", "p_equiv_holm", "verdict", "verdict_without_zseries"]]
    return C, holm, dict(reproduces=reproduces)


def report(C, holm, info, art: Path) -> str:
    return "\n".join([
        f"# C3 check — {art.name}", "",
        "Supplementary, not pre-specified (`python -m marathonts.hypotheses.c3_check`). C3 with every selection "
        "strategy and without the zseries assembler (see the module docstring). `median_z`: the median effect "
        "over datasets in noise units (> 0: selection better than the random path).", "",
        f"The pre-specified variant reproduces the published C3: {info['reproduces']}.", "",
        C.to_markdown(index=False, floatfmt=".3g"), "",
        "Holm over the ten confirmatory tests with C3 without zseries (`verdict`: published):", "",
        holm.to_markdown(index=False, floatfmt=".3g"), ""])


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--artifacts-dir", required=True)
    ap.add_argument("--out-dir")
    a = ap.parse_args(argv)
    art = Path(a.artifacts_dir)
    out = Path(a.out_dir) if a.out_dir else art / "supplementary" / "c3_check"
    C, holm, info = run(art)
    out.mkdir(parents=True, exist_ok=True)
    write_table(C, out / "c3.parquet", keep64=["median_z", "p_two_sided", "p_equiv"])
    text = report(C, holm, info, art)
    (out / "C3_CHECK.md").write_text(text)
    print(text)


if __name__ == "__main__":
    main()
