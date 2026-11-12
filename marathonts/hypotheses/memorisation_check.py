"""Supplementary check of the memorisation diagnostics F10 (not pre-specified): the signed DCR ratio, the
near copies with their uncertainty, and controls with exact and near copies of train.

    python -m marathonts.hypotheses.memorisation_check --artifacts-dir artifacts/run_h200 \\
        --series-dir <run>/series [--data-dir data/processed/min] [--n-boot 2000] [--jobs 8] [--out-dir <dir>]

F10 (`fidelity.F10_memorisation`) cuts windows of length T from the synthetic series, the real val series and
train (z-scored with val) and takes, for every synthetic and every val window, the distance to the closest
training window (DCR). F10.1 is |log(median DCR of the synthetic windows / median DCR of the val windows)|;
F10.2 is the share of synthetic windows whose DCR is below the 5th percentile of the val windows' DCR (near
copies). The absolute value of F10.1 does not tell a series closer to train than val (copying) from one
farther from it (off-distribution). Here the same windows are recomputed for every series of the run and for
the real OOT piece (`real`, as in the run), and:

* `units.parquet` — one row per series: `signed_log_ratio` (< 0: closer to train than val), its absolute value
  (equal to the published F10.1), `near_copies` / `windows` (`near_copy_share`, equal to the published F10.2),
  `exact_copies` (DCR below 0.05 in z units: float32 distances of identical windows are not exactly 0);
* `methods.parquet` — per method: the median over datasets (mean over seeds within a dataset) of the signed
  log ratio and of the near-copy share, each with a two-level bootstrap interval (datasets, then seeds;
  `n_boot`), the total counts, the median ratio of the near-copy share to the real one and the memorisation
  flag of the analysis (`overall.memorisation`: ratio >= 2 and a significant excess, one-sided Wilcoxon over
  datasets, Holm);
* controls, scored in the same way on every dataset and seed and flagged by the same rule: `copy` — the first
  points of train (every window an exact copy); `copy+noise s` — the same with Gaussian noise of s standard
  deviations of train; `partial f` — the real OOT piece with its first share f replaced by train.

Written to `<out>/` (default `<artifacts>/supplementary/memorisation_check`), with `MEMORISATION_CHECK.md`. CPU
only; needs the series of the run (Hugging Face: every dataset but ETT and PJM) and the prepared data.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import pandas as pd

from marathonts.bench.storage import write_table

EXACT = 0.05            # float32 distances of exact copies are not exactly 0
NOISE = (0.05, 0.1, 0.25, 0.5)
PARTIAL = (0.1, 0.25, 0.5)
CONTROLS = ["copy", *[f"copy+noise {s}" for s in NOISE], *[f"partial {f}" for f in PARTIAL]]


def _frame(data_dir: Path, ds: str):
    f = pd.read_parquet(data_dir / f"{ds}.parquet")
    f["split"] = f["split"].astype(str)
    meta = pd.read_parquet(data_dir / f"{ds}.meta.parquet").iloc[0].to_dict()
    part = {s: (g["value"].to_numpy(float), g["how"].to_numpy(int)) for s, g in f.groupby("split")}
    return part, int(meta["T"]), int(meta["K"])


def _series(kind: str, part, T: int, K: int, seed: int, series_file: str | None):
    """(values, how) of one unit: a stored series, `real` or a control."""
    tr, tr_how = part["train"]
    oot, oot_how = part["oot"]
    L = K * T
    if series_file is not None:
        s = pd.read_parquet(series_file, columns=["value", "how"])
        return s["value"].to_numpy(float), s["how"].to_numpy(int)
    if kind == "real":
        return oot[:L], oot_how[:L]
    rng = np.random.default_rng([seed, 7])
    n = min(L, len(tr))
    if kind == "copy":
        return tr[:n].copy(), tr_how[:n]
    if kind.startswith("copy+noise"):
        s = float(kind.split()[-1])
        return tr[:n] + s * np.nanstd(tr) * rng.standard_normal(n), tr_how[:n]
    if kind.startswith("partial"):
        f = float(kind.split()[-1])
        x, h = oot[:L].copy(), oot_how[:L].copy()
        m = int(round(f * len(x)))
        start = int(rng.integers(0, max(1, len(tr) - m)))
        x[:m], h[:m] = tr[start:start + m], tr_how[start:start + m]
        return x, h
    raise ValueError(kind)


def one(args) -> dict:
    import torch

    from marathonts.bench.fidelity import FidelityContext, _nn_min, _windows, _zscore

    torch.set_num_threads(1)
    data_dir, ds, method, seed, series_file = args
    part, T, K = _frame(data_dir, ds)
    x, how = _series(method, part, T, K, seed, series_file)
    ref, ref_how = part["val"]
    tr, tr_how = part["train"]
    ctx = FidelityContext(x, how, np.array([], int), ref, ref_how, tr, tr_how, T, seed)
    Wx, Wr = ctx.windows[:2]
    rng = np.random.default_rng(seed + 2)                   # as in fidelity.F10_memorisation
    Wt = _windows(_zscore(tr, ref), T, rng=rng)
    row = dict(dataset=ds, method=method, seed=seed, windows=len(Wx))
    if not (len(Wt) > 10 and len(Wx) > 10 and len(Wr) > 10):
        return {**row, "signed_log_ratio": np.nan, "abs_log_ratio": np.nan, "near_copies": 0,
                "near_copy_share": np.nan, "exact_copies": 0, "dcr_syn": np.nan, "dcr_val": np.nan}
    dcr_x = _nn_min(Wx[:, ::2], Wt[:, ::2])
    dcr_r = _nn_min(Wr[:, ::2], Wt[:, ::2])
    sl = float(np.log(np.median(dcr_x) / (np.median(dcr_r) + 1e-12) + 1e-12))
    near = dcr_x < np.percentile(dcr_r, 5)
    return {**row, "signed_log_ratio": sl, "abs_log_ratio": abs(sl), "near_copies": int(near.sum()),
            "near_copy_share": float(near.mean()), "exact_copies": int((dcr_x < EXACT).sum()),
            "dcr_syn": float(np.median(dcr_x)), "dcr_val": float(np.median(dcr_r))}


def _boot(P: pd.DataFrame, col: str, n_boot: int, rng) -> tuple[float, float, float]:
    """Median over datasets of the mean over seeds, and a two-level bootstrap interval (datasets, then seeds)."""
    by = {ds: g[col].dropna().to_numpy() for ds, g in P.groupby("dataset")}
    by = {k: v for k, v in by.items() if len(v)}
    if not by:
        return np.nan, np.nan, np.nan
    est = float(np.median([v.mean() for v in by.values()]))
    keys = list(by)
    stats = []
    for _ in range(n_boot):
        ks = rng.choice(len(keys), len(keys))
        stats.append(np.median([rng.choice(by[keys[i]], len(by[keys[i]])).mean() for i in ks]))
    lo, hi = np.percentile(stats, [2.5, 97.5])
    return est, float(lo), float(hi)


def summarise(U: pd.DataFrame, methods, n_boot: int, alpha: float, ratio: float) -> pd.DataFrame:
    from marathonts.hypotheses import stats as S

    rng = np.random.default_rng(0)
    real = U[U["method"] == "real"].groupby("dataset")["near_copy_share"].median()
    rows, p = [], []
    for m in methods:
        P = U[U["method"] == m]
        if not len(P):
            continue
        sl, sl_lo, sl_hi = _boot(P, "signed_log_ratio", n_boot, rng)
        nc, nc_lo, nc_hi = _boot(P, "near_copy_share", n_boot, rng)
        per = P.groupby("dataset")["near_copy_share"].median()
        rr = (per / real.reindex(per.index)).replace([np.inf, -np.inf], np.nan)
        p.append(S.wilcoxon((per - real.reindex(per.index)).dropna().to_numpy(), "greater"))
        rows.append(dict(method=m, series=len(P), signed_log_ratio=sl, slr_lo=sl_lo, slr_hi=sl_hi,
                         closer_than_val=int((P["signed_log_ratio"] < 0).sum()),
                         near_copy_share=nc, ncs_lo=nc_lo, ncs_hi=nc_hi, near_copies=int(P["near_copies"].sum()),
                         windows=int(P["windows"].sum()), exact_copies=int(P["exact_copies"].sum()),
                         near_copy_ratio=float(rr.median())))
    out = pd.DataFrame(rows)
    out["p_more_copies_holm"] = S.holm(np.array(p, float)) if len(p) else []
    out["memorisation_flag"] = (out["near_copy_ratio"] >= ratio) & (out["p_more_copies_holm"] < alpha)
    return out


def run(art: Path, series_dir: Path, data_dir: Path, n_boot: int, jobs: int):
    from marathonts.hypotheses.leaderboard import ranked_methods
    from marathonts.hypotheses.overall import NEAR_COPY_RATIO
    from marathonts.hypotheses.tie_check import load

    T, cfg = load(art)
    methods = ranked_methods(T, cfg)
    datasets = sorted(set(T["fidelity"]["dataset"]))
    tasks = [(data_dir, f.parts[-3], f.parts[-2], int(f.stem[4:]), str(f))
             for m in methods for f in sorted(series_dir.glob(f"*/{m}/seed*.parquet")) if f.parts[-3] in datasets]
    tasks += [(data_dir, ds, "real", cfg.seeds[0], None) for ds in datasets]
    tasks += [(data_dir, ds, c, s, None) for c in CONTROLS for ds in datasets for s in cfg.seeds]
    with ProcessPoolExecutor(jobs) as ex:
        U = pd.DataFrame(list(ex.map(one, tasks, chunksize=4)))
    pub = T["fidelity"].set_index(["dataset", "method", "seed"])
    for col, src in (("f101_published", "F10.1_dcr_logratio"), ("f102_published", "F10.2_near_copy_share")):
        U[col] = [pub[src].get((r.dataset, r.method, r.seed), np.nan) for r in U.itertuples()]
    ratio = getattr(cfg, "near_copy_ratio", None) or NEAR_COPY_RATIO
    M = summarise(U, methods, n_boot, cfg.alpha, ratio)
    C = summarise(U, CONTROLS, n_boot, cfg.alpha, ratio)
    return U, M, C


def report(U, M, C, art: Path) -> str:
    def agree(a, b):
        both = U[a].notna() & U[b].notna()
        d = (U[a] - U[b]).abs()[both]
        return f"{int((d < 1e-4).sum())} of {int(both.sum())} (largest difference {d.max():.2g})"

    per_ds = U[U["f101_published"].notna()].assign(d=lambda d: (d["abs_log_ratio"] - d["f101_published"]).abs())
    off = per_ds[per_ds["d"] >= 1e-4].groupby("dataset").size()
    real = U[U["method"] == "real"]["near_copy_share"]
    return "\n".join([
        f"# Memorisation check — {art.name}", "",
        "Supplementary, not pre-specified (`python -m marathonts.hypotheses.memorisation_check`). See the module "
        "docstring. Medians over datasets of the mean over seeds, 95 % two-level bootstrap intervals.", "",
        f"Recomputed |signed log ratio| equals the published F10.1 in {agree('abs_log_ratio', 'f101_published')}; "
        f"the near-copy share equals F10.2 in {agree('near_copy_share', 'f102_published')}."
        + (f" Differences by dataset: {off.to_dict()}." if len(off) else ""), "",
        f"Real OOT piece: near-copy share median {real.median():.3f} (range {real.min():.3f}-{real.max():.3f}).", "",
        "## Methods", "", M.to_markdown(index=False, floatfmt=".3g"), "",
        "## Controls", "", C.to_markdown(index=False, floatfmt=".3g"), ""])


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--artifacts-dir", required=True)
    ap.add_argument("--series-dir", help="default: <artifacts>/series")
    ap.add_argument("--data-dir", default="data/processed/min")
    ap.add_argument("--n-boot", type=int, default=2000)
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--out-dir")
    a = ap.parse_args(argv)
    art = Path(a.artifacts_dir)
    out = Path(a.out_dir) if a.out_dir else art / "supplementary" / "memorisation_check"
    U, M, C = run(art, Path(a.series_dir) if a.series_dir else art / "series", Path(a.data_dir), a.n_boot, a.jobs)
    out.mkdir(parents=True, exist_ok=True)
    write_table(U, out / "units.parquet", keep64=["signed_log_ratio", "abs_log_ratio", "near_copy_share"])
    write_table(pd.concat([M.assign(kind="method"), C.assign(kind="control")]), out / "methods.parquet",
                keep64=["signed_log_ratio", "near_copy_share"])
    text = report(U, M, C, art)
    (out / "MEMORISATION_CHECK.md").write_text(text)
    print(text)


if __name__ == "__main__":
    main()
