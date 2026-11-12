"""Supplementary check of F5.6, the share of change points at seams, against the density of the seams (not
pre-specified).

    python -m marathonts.hypotheses.seam_check --artifacts-dir artifacts/run_h200 --series-dir <run>/series \\
        [--n-perm 200] [--jobs 8] [--out-dir <dir>]

F5.6 (`fidelity.F5_seams`) is the share of the change points of a series (PELT on 2-hour means,
`fidelity._cp_rate`) that lie within three points of a seam. If the change points had nothing to do with the
seams, this share would be about the share of positions within three points of a seam, which grows with the
density of the seams (about 4 % with a seam every 168 points, 11 % every 64). For every series of the run:

* `seams` and `exposed` — the number of seams and the share of positions within three points of one;
* `f56` — F5.6 recomputed from the series (equal to the published value);
* `f56_null` — the mean of the same share over `n_perm` circular shifts of the seam positions by a random
  offset (the spacing of the seams is kept, their placement relative to the change points is not);
* `f56_lift` = `f56` / `f56_null` — 1: the change points fall on the seams as often as by chance; above 1: more
  often.

Written to `<out>/` (default `<artifacts>/supplementary/seam_check`): `seams.parquet` (one row per series) and
`SEAM_CHECK.md` (medians per method). CPU only; needs `ruptures` and the series of the run (Hugging Face: every
dataset but ETT and PJM).
"""
from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import pandas as pd

from marathonts.bench.storage import write_table

WINDOW = 3


def _share(sv: np.ndarray, bk: np.ndarray) -> float:
    if not len(sv) or not len(bk):
        return np.nan
    return float(np.mean([np.min(np.abs(sv - b)) <= WINDOW for b in bk]))


def one(args) -> dict:
    from marathonts.bench.fidelity import _cp_rate

    f, ds, m, seed, n_perm = args
    s = pd.read_parquet(f, columns=["value", "seam"])
    x = s["value"].to_numpy(float)
    n = len(x)
    sv = np.where(s["seam"].to_numpy(bool))[0]
    sv = sv[(sv > 0) & (sv < n)]
    exposed = np.zeros(n, bool)
    for d in range(-WINDOW, WINDOW + 1):
        i = sv + d
        exposed[i[(i >= 0) & (i < n)]] = True
    _, bk = _cp_rate(x)
    obs = _share(sv, bk)
    rng = np.random.default_rng(seed)
    null = np.nan
    if len(sv) and len(bk):
        null = float(np.mean([_share(np.sort((sv + rng.integers(0, n)) % n), bk) for _ in range(n_perm)]))
    return dict(dataset=ds, method=m, seed=seed, length=n, seams=len(sv), exposed=float(exposed.mean()),
                change_points=len(bk), f56=obs, f56_null=null,
                f56_lift=obs / null if np.isfinite(obs) and np.isfinite(null) and null > 0 else np.nan)


def run(art: Path, series_dir: Path, n_perm: int, jobs: int) -> pd.DataFrame:
    from marathonts.hypotheses.leaderboard import ranked_methods
    from marathonts.hypotheses.tie_check import load

    T, cfg = load(art)
    methods = ranked_methods(T, cfg)
    tasks = [(f, f.parts[-3], f.parts[-2], int(f.stem[4:]), n_perm)
             for m in methods for f in sorted(series_dir.glob(f"*/{m}/seed*.parquet"))]
    with ProcessPoolExecutor(jobs) as ex:
        rows = list(ex.map(one, tasks, chunksize=8))
    out = pd.DataFrame(rows)
    pub = T["fidelity"].set_index(["dataset", "method", "seed"])["F5.6_cp_at_seams"]
    out["f56_published"] = [pub.get((r.dataset, r.method, r.seed), np.nan) for r in out.itertuples()]
    return out


def report(D: pd.DataFrame, art: Path) -> str:
    agree = (D["f56"] - D["f56_published"]).abs()
    both = D["f56"].notna() & D["f56_published"].notna()
    g = D.groupby("method").agg(series=("seams", "size"), seams=("seams", "median"), exposed=("exposed", "median"),
                                change_points=("change_points", "median"), f56=("f56", "median"),
                                f56_null=("f56_null", "median"), f56_lift=("f56_lift", "median"),
                                lift_defined=("f56_lift", lambda s: int(s.notna().sum())))
    g = g.sort_values("f56")
    rho_raw = g["f56"].corr(g["exposed"], method="spearman")
    t = g.dropna(subset=["f56_lift"])
    tau = t["f56"].rank().corr(t["f56_lift"].rank(), method="kendall")
    return "\n".join([
        f"# Seam check — {art.name}", "",
        "Supplementary, not pre-specified (`python -m marathonts.hypotheses.seam_check`). See the module docstring.",
        "", f"Series: {len(D)}; F5.6 recomputed equals the published value in {int((agree[both] < 1e-6).sum())} of "
        f"{int(both.sum())} series with both defined (largest difference {agree[both].max():.2g}).", "",
        f"Across methods, Spearman correlation between the median F5.6 and the median exposed share: {rho_raw:.2f}. "
        f"Kendall's tau between the order of the methods by F5.6 and by the chance-adjusted lift: {tau:.2f}.", "",
        "Medians per method (sorted by F5.6; `lift_defined`: series with a seam and a change point):", "",
        g.to_markdown(floatfmt=".3g"), ""])


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--artifacts-dir", required=True)
    ap.add_argument("--series-dir", help="default: <artifacts>/series")
    ap.add_argument("--n-perm", type=int, default=200)
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--out-dir")
    a = ap.parse_args(argv)
    art = Path(a.artifacts_dir)
    out = Path(a.out_dir) if a.out_dir else art / "supplementary" / "seam_check"
    D = run(art, Path(a.series_dir) if a.series_dir else art / "series", a.n_perm, a.jobs)
    out.mkdir(parents=True, exist_ok=True)
    write_table(D, out / "seams.parquet", keep64=["f56", "f56_null", "f56_lift", "exposed"])
    text = report(D, art)
    (out / "SEAM_CHECK.md").write_text(text)
    print(text)


if __name__ == "__main__":
    main()
