"""Supplementary check of the noise margins (not pre-specified): the margins themselves, their zero and
near-zero values, and how the verdicts change when the margin is estimated otherwise.

    python -m marathonts.hypotheses.noise_check --analysis-dir artifacts/run_h200 \\
        [--variant pairs=<dir> perm1=<dir> … scale0.5=<dir> scale2=<dir>] [--out-dir <dir>]

`--analysis-dir` is the output of the pre-specified analysis (`hypotheses/`); each `--variant` is the output of
the same analysis run with `--noise-estimator` ("pairs": every pair of seeds; "perm:<n>": neighbouring seeds
after a random reordering of the seeds) or `--noise-scale` (a factor on every margin). Written to
`<out>/` (default `<analysis-dir>/supplementary/noise_check`):

* `margins.parquet` — the margin of every (question, comparison, dataset, unit) of RQ2 and RQ3 with the number
  of seeds behind it (`n`; the pre-specified estimator uses the n − 1 differences of neighbouring seeds);
* `verdicts.parquet` — the global verdicts of RQ2, RQ3 and C1–C4 under every variant, side by side;
* `NOISE_CHECK.md` — the summary: margins, zero and near-zero margins (below 1 % of the median margin of
  the unit over datasets), the per-dataset verdicts that rest on them, and the verdicts that change.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from marathonts.bench.storage import write_table

QUESTIONS = ("RQ2", "RQ3")
NEAR_ZERO = 0.01


def _key(df: pd.DataFrame) -> pd.Series:
    return df["comparison"].astype(str) + " | " + df["unit"].astype(str) + " | " + df["kind"].astype(str)


def margins(hyp: Path) -> pd.DataFrame:
    rows = []
    for q in QUESTIONS:
        f = hyp / f"{q}_per_dataset.parquet"
        if f.exists():
            p = pd.read_parquet(f)
            rows.append(p.assign(question=q)[["question", "comparison", "kind", "dataset", "unit", "n", "margin",
                                              "verdict"]])
    m = pd.concat(rows, ignore_index=True)
    med = m.groupby(["question", "comparison", "unit"])["margin"].transform(lambda s: s[s > 0].median())
    # a zero margin is stored as NaN (the smallest effect is undefined; the dataset leaves the global test)
    return m.assign(zero=m["margin"].isna() | (m["margin"] == 0),
                    near_zero=(m["margin"] > 0) & (m["margin"] < NEAR_ZERO * med))


def verdicts(hyp: Path, name: str) -> pd.DataFrame:
    rows = []
    for q in QUESTIONS:
        f = hyp / f"{q}_global.parquet"
        if f.exists():
            g = pd.read_parquet(f)
            rows.append(pd.DataFrame({"question": q, "key": _key(g), name: g["verdict"].to_numpy()}))
    f = hyp / "confirmatory.parquet"
    if f.exists():
        c = pd.read_parquet(f)
        rows.append(pd.DataFrame({"question": "C1-C4", "key": (c["test"] + " | " + c["cell"] + " | " + c["comparison"]),
                                  name: c["verdict"].to_numpy()}))
    return pd.concat(rows, ignore_index=True).set_index(["question", "key"])


def report(M: pd.DataFrame, V: pd.DataFrame, names: list[str]) -> str:
    out = ["# Noise check — supplementary, not pre-specified", "",
           "Margins of RQ2 and RQ3 (one row per question, comparison, dataset and unit). `n`: seeds behind a margin; "
           "the pre-specified estimator uses the n − 1 differences of neighbouring seeds. Zero: every difference is "
           "zero (a discrete or a constant metric), the margin is undefined. Near zero: above zero and "
           f"below {NEAR_ZERO:.0%} of the median margin of the unit over datasets.", ""]
    s = M.groupby("question").agg(margins=("margin", "size"), seeds_median=("n", "median"), seeds_min=("n", "min"),
                                  zero=("zero", "sum"), near_zero=("near_zero", "sum"))
    out += [s.to_markdown(), ""]
    d = M[M["verdict"].isin(["better", "worse", "same"])]
    t = d.groupby(["question", "verdict"]).agg(per_dataset=("margin", "size"), on_zero=("zero", "sum"),
                                               on_near_zero=("near_zero", "sum"))
    out += ["Per-dataset verdicts and the margins they rest on (a zero margin is undefined: the per-dataset verdict is inconclusive and the dataset leaves the global test):", "",
            t.to_markdown(), ""]
    counts = pd.concat({n: V[n].groupby(level="question").value_counts().unstack(fill_value=0) for n in names},
                       names=["variant"]).fillna(0).astype(int)
    out += ["Global verdicts under every variant (`main` = pre-specified):", "", counts.to_markdown(), ""]
    var = [n for n in names if n != "main"]
    if not var:
        return "\n".join(out)
    both = {n: V[n].notna() & V["main"].notna() for n in var}
    ch = pd.DataFrame({n: (both[n] & (V[n] != V["main"])).groupby(level="question").sum() for n in var})
    gone = pd.DataFrame({n: (V["main"].notna() & V[n].isna()).groupby(level="question").sum() for n in var})
    new = pd.DataFrame({n: (V["main"].isna() & V[n].notna()).groupby(level="question").sum() for n in var})
    out += ["Global verdicts that differ from `main` (units tested in both):", "", ch.to_markdown(), "",
            "Units tested in `main` but not in the variant (every dataset with a zero margin) and the reverse:", "",
            gone.add_suffix(" lost").join(new.add_suffix(" new")).T.to_markdown(), ""]
    changed = pd.concat([both[n] & (V[n] != V["main"]) for n in var], axis=1).any(axis=1)
    diff = V[changed]
    if len(diff):
        out += ["The verdicts that differ under any variant:", "", diff.reset_index().to_markdown(index=False), ""]
    return "\n".join(out)


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--analysis-dir", required=True, help="output of the pre-specified analysis (with hypotheses/)")
    ap.add_argument("--variant", nargs="*", default=[], metavar="NAME=DIR", help="outputs of the variant analyses")
    ap.add_argument("--out-dir")
    a = ap.parse_args(argv)
    base = Path(a.analysis_dir)
    out = Path(a.out_dir) if a.out_dir else base / "supplementary" / "noise_check"
    M = margins(base / "hypotheses")
    V = [verdicts(base / "hypotheses", "main")]
    names = ["main"]
    for v in a.variant:
        n, d = v.split("=", 1)
        V.append(verdicts(Path(d) / "hypotheses", n))
        names.append(n)
    V = pd.concat(V, axis=1)
    out.mkdir(parents=True, exist_ok=True)
    write_table(M, out / "margins.parquet", keep64=["margin"])
    write_table(V.reset_index(), out / "verdicts.parquet")
    text = report(M, V, names)
    (out / "NOISE_CHECK.md").write_text(text)
    print(text)


if __name__ == "__main__":
    main()
