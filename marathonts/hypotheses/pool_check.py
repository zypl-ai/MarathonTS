"""Supplementary check of the window pools (not pre-specified): replaced values, range and flat windows.

    python -m marathonts.hypotheses.pool_check --artifacts-dir artifacts/run_l4 [--out-dir <dir>] [--flat 0.01]

Reads every pool `<artifacts>/pools/<dataset>/<generator>/seed<k>.parquet` (array `pool`, shape
(N, T, 3), channels in [0, 1]; the value is channel 0) and writes, per (dataset, generator, seed):

* `exact_half` — values of the value channel exactly equal to 0.5. The VAE replaces a NaN of the
  decoder by 0.5 (`TsgmVAE.sample`); its decoder ends with a sigmoid, which in float32 returns exactly
  0.5 only for an input within about 3e-8 of zero, so such values are the upper bound of replaced NaN;
* `nan_windows` — windows whose every value of every channel is exactly 0.5 (a whole window decoded
  as NaN);
* `at_0`, `at_1` — shares of values exactly at the bounds (the sigmoid saturates in float32; the
  clipping to [0, 1] does not change a sigmoid output);
* `min`, `q0001`, `q9999`, `max` — range of the value channel; train is [0, 1] after scaling;
* `window_std_median`, `flat_share` — median standard deviation of a window's value and the share of
  windows with a standard deviation below `--flat`.

Output: `<out>/pool_check.parquet` and `<out>/POOL_CHECK.md` (default `<artifacts>/supplementary/pool_check`).
CPU only; the pools of a run are published with it (Hugging Face: every dataset but ETT and PJM).
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from marathonts.bench.storage import read_arrays, write_table


def check_pool(pool: np.ndarray, flat: float) -> dict:
    v = pool[..., 0].astype(np.float64)
    std = v.std(axis=1)
    return dict(n_windows=pool.shape[0], exact_half=int((pool[..., 0] == np.float32(0.5)).sum()),
                nan_windows=int((pool == np.float32(0.5)).all(axis=(1, 2)).sum()),
                at_0=float((v == 0).mean()), at_1=float((v == 1).mean()),
                min=float(v.min()), q0001=float(np.quantile(v, 1e-4)), q9999=float(np.quantile(v, 1 - 1e-4)),
                max=float(v.max()), window_std_median=float(np.median(std)), flat_share=float((std < flat).mean()))


def run(artifacts: Path, flat: float = 0.01) -> pd.DataFrame:
    rows = []
    for f in sorted((artifacts / "pools").glob("*/*/seed*.parquet")):
        if f.name.endswith(".record.parquet"):
            continue
        rows.append(dict(dataset=f.parent.parent.name, generator=f.parent.name, seed=int(f.stem[4:]),
                         **check_pool(read_arrays(f)["pool"], flat)))
    if not rows:
        raise SystemExit(f"no pools under {artifacts / 'pools'}")
    return pd.DataFrame(rows)


def report(df: pd.DataFrame, artifacts: Path, flat: float) -> str:
    g = df.groupby(["generator", "dataset"]).agg(
        seeds=("seed", "nunique"), windows=("n_windows", "sum"), exact_half=("exact_half", "sum"),
        nan_windows=("nan_windows", "sum"), at_0=("at_0", "mean"), at_1=("at_1", "mean"), min=("min", "min"),
        max=("max", "max"), window_std_median=("window_std_median", "median"), flat_share=("flat_share", "mean"))
    lines = [f"# Pool check — {artifacts.name}", "",
             "Supplementary, not pre-specified (`python -m marathonts.hypotheses.pool_check`). Value channel, scaled with the "
             "bounds of train ([0, 1]). `exact_half`: values exactly 0.5 (upper bound of NaN replaced by 0.5); "
             "`nan_windows`: windows that are 0.5 everywhere; `at_0`, `at_1`: shares at the bounds; "
             f"`flat_share`: share of windows with a standard deviation below {flat}.", "",
             g.to_markdown(floatfmt=".4g"), ""]
    return "\n".join(lines)


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--artifacts-dir", required=True)
    ap.add_argument("--out-dir", help="default: <artifacts>/supplementary/pool_check")
    ap.add_argument("--flat", type=float, default=0.01, help="window standard deviation below which a window is flat")
    a = ap.parse_args(argv)
    art = Path(a.artifacts_dir)
    out = Path(a.out_dir) if a.out_dir else art / "supplementary" / "pool_check"
    df = run(art, a.flat)
    out.mkdir(parents=True, exist_ok=True)
    write_table(df, out / "pool_check.parquet", keep64=[c for c in df.columns if df[c].dtype.kind == "f"])
    (out / "POOL_CHECK.md").write_text(report(df, art, a.flat))
    print(report(df, art, a.flat))


if __name__ == "__main__":
    main()
