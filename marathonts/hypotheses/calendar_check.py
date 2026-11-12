"""Supplementary check of the calendar of the synthetic series (not pre-specified): how far the hour of the
week of each series is from a valid calendar.

    python -m marathonts.hypotheses.calendar_check --artifacts-dir artifacts/run_l4 [--out-dir <dir>]

Reads every series `<artifacts>/series/<dataset>/<method>/seed<k>.parquet` (columns `how`, the hour of the
week, and `piece`, the stretch between two seams) and writes, per (dataset, method, seed):

* `step_one` — share of steps at which the hour of the week advances by exactly one (as fidelity F4.4);
* `err_median`, `err_p90`, `err_max`, `share_err_ge3` — the error of the calendar inside a piece, in hours:
  for every piece, the valid calendar `(c + i) mod 168` with the offset `c` closest to the series is
  found, and the error of a step is the circular distance between its hour and that calendar. A jump at a
  seam is not an error here (a new piece may start at any hour); a calendar that jitters by an hour inside
  a window is.

Output: `<out>/calendar_check.parquet` and `<out>/CALENDAR_CHECK.md` (default
`<artifacts>/supplementary/calendar_check`). CPU only; the series of a run are published with it (Hugging
Face: every dataset but ETT and PJM).
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from marathonts.bench.storage import write_table

H = 168
OFFSETS = np.arange(H)


def piece_errors(how: np.ndarray) -> np.ndarray:
    """Circular error (hours) of each step of one piece against its closest valid calendar."""
    i = np.arange(len(how))
    d = np.abs((how[None, :] - (OFFSETS[:, None] + i[None, :])) % H)
    d = np.minimum(d, H - d)                                   # (offset, step)
    return d[np.argmin(d.sum(axis=1))]


def check_series(how: np.ndarray, piece: np.ndarray) -> dict:
    how, piece = np.asarray(how, int), np.asarray(piece)
    err = np.concatenate([piece_errors(how[piece == p]) for p in pd.unique(piece)])
    return dict(n=len(how), pieces=int(len(pd.unique(piece))), step_one=float(((np.diff(how) % H) == 1).mean()),
                err_median=float(np.median(err)), err_p90=float(np.quantile(err, 0.9)), err_max=int(err.max()),
                share_err_ge3=float((err >= 3).mean()))


def run(artifacts: Path, length_matched: bool = False) -> pd.DataFrame:
    rows = []
    for f in sorted((artifacts / "series").glob("*/*/seed*.parquet")):
        method = f.parent.name
        if "@" in method and not length_matched:
            continue
        S = pd.read_parquet(f, columns=["how", "piece"])
        rows.append(dict(dataset=f.parent.parent.name, method=method, seed=int(f.stem[4:]),
                         **check_series(S["how"].to_numpy(), S["piece"].to_numpy())))
    if not rows:
        raise SystemExit(f"no series under {artifacts / 'series'}")
    return pd.DataFrame(rows)


def report(df: pd.DataFrame, artifacts: Path) -> str:
    g = df.groupby("method").agg(datasets=("dataset", "nunique"), series=("seed", "size"),
                                 step_one=("step_one", "median"), err_median=("err_median", "median"),
                                 err_p90=("err_p90", "median"), err_max=("err_max", "max"),
                                 share_err_ge3=("share_err_ge3", "median")).sort_values("step_one")
    lines = [f"# Calendar check — {artifacts.name}", "",
             "Supplementary, not pre-specified (`python -m marathonts.hypotheses.calendar_check`). Medians over datasets and "
             "seeds. `step_one`: share of steps at which the hour of the week advances by exactly one (F4.4). "
             "`err_*`: error of the hour of the week inside a piece (between two seams) against the closest valid "
             "calendar, in hours (`err_max`: the largest over all series); `share_err_ge3`: share of steps with an "
             "error of 3 hours or more.", "", g.to_markdown(floatfmt=".3g"), ""]
    return "\n".join(lines)


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--artifacts-dir", required=True)
    ap.add_argument("--out-dir", help="default: <artifacts>/supplementary/calendar_check")
    ap.add_argument("--length-matched", action="store_true", help="also the length-matched variants <method>@len")
    a = ap.parse_args(argv)
    art = Path(a.artifacts_dir)
    out = Path(a.out_dir) if a.out_dir else art / "supplementary" / "calendar_check"
    df = run(art, a.length_matched)
    out.mkdir(parents=True, exist_ok=True)
    write_table(df, out / "calendar_check.parquet", keep64=[c for c in df.columns if df[c].dtype.kind == "f"])
    (out / "CALENDAR_CHECK.md").write_text(report(df, art))
    print(report(df, art))


if __name__ == "__main__":
    main()
