"""Stage 1 — a registered dataset (bench.datasets) → splits and window parameters.

Every dataset becomes the same object: an hourly `value` series (NaN where unknown), its
hour of week `how`, and a `split` label (train / val / oot, embargo rows dropped). Window
parameters follow BENCHMARK.md, Protocol: data and are computed on train only. Stored as Parquet:
`data/processed/<profile>/<name>.parquet` (series) and `<name>.meta.parquet` (one-row meta).
"""
from __future__ import annotations

import hashlib
import json
import warnings
from dataclasses import dataclass

import numpy as np
import pandas as pd
from numpy.lib.stride_tricks import sliding_window_view

from . import registry as R
from .config import PKG, ROOT, Config
from .storage import read_record, write_record, write_table

HOURS_PER_WEEK = 168
# content hashes of the prepared series of the published results, {data_key: {dataset: hash}}; not part of any
# fingerprint (adding or changing an entry redoes nothing) — only checked, so that data that differ from the
# published ones (a re-uploaded source, a revised history) do not pass unnoticed
DATA_HASHES_FILE = PKG / "data_hashes.json"
_warned: set = set()


# ─────────────────────── prepared dataset ──────────────────────────────────
@dataclass
class Prepared:
    name: str
    frame: pd.DataFrame          # index time; columns value, how, split
    meta: dict

    def part(self, split: str) -> tuple[np.ndarray, np.ndarray]:
        f = self.frame[self.frame["split"] == split]
        return f["value"].to_numpy(float), f["how"].to_numpy(int)

    @property
    def lo(self) -> float:
        return self.meta["lo"]

    @property
    def hi(self) -> float:
        return self.meta["hi"]


def to_channels(values, how, lo, hi) -> np.ndarray:
    a = 2 * np.pi * np.asarray(how) / HOURS_PER_WEEK
    return np.column_stack([(np.asarray(values) - lo) / (hi - lo),
                            (np.sin(a) + 1) / 2, (np.cos(a) + 1) / 2]).astype(np.float32)


def from_channels(X, lo, hi) -> tuple[np.ndarray, np.ndarray]:
    X = np.asarray(X)
    values = X[:, 0].astype(np.float64) * (hi - lo) + lo
    a = np.arctan2(2 * X[:, 1] - 1, 2 * X[:, 2] - 1)
    how = np.mod(np.rint(a / (2 * np.pi) * HOURS_PER_WEEK), HOURS_PER_WEEK).astype(int)
    return values, how


def slide(X: np.ndarray, T: int, s: int) -> np.ndarray:
    if len(X) < T:
        return np.zeros((0, T, X.shape[1]), np.float32)
    W = sliding_window_view(X, (T, X.shape[1]))[::s, 0]
    return np.ascontiguousarray(W[~np.isnan(W).any(axis=(1, 2))], dtype=np.float32)


def _interp_short_gaps(s: pd.Series, max_gap: int) -> pd.Series:
    isna = s.isna()
    run = isna.groupby((~isna).cumsum()).transform("sum")
    filled = s.interpolate(limit_area="inside")
    return filled.where(~isna | (run <= max_gap))


def prepare(name: str, cfg: Config) -> Prepared:
    R.load_builtins()
    raw = R.datasets.get(name).load(cfg)
    if not isinstance(raw.index, pd.DatetimeIndex):
        raise TypeError(f"dataset {name}: load() must return a series with a DatetimeIndex")
    s = _interp_short_gaps(raw.asfreq("h"), cfg.max_gap_interp)
    s = s.loc[s.first_valid_index(): s.last_valid_index()]
    if cfg.max_points:
        s = s.iloc[-cfg.max_points:]                    # the most recent part of the series
        s = s.loc[s.first_valid_index(): s.last_valid_index()]
    n = len(s)
    n_tr, n_va = int(cfg.split[0] * n), int(cfg.split[1] * n)
    n_te = n - n_tr - n_va
    if n_tr < 4 * cfg.T or min(n_va, n_te) - cfg.embargo < 2 * cfg.T:
        raise ValueError(f"dataset {name}: {n} hourly points after cleaning are too few for T = {cfg.T}: train needs "
                         f"≥ {4 * cfg.T} points and val / OOT ≥ {2 * cfg.T + cfg.embargo} each (split {cfg.split}, "
                         f"embargo {cfg.embargo})")
    split = np.full(n, "", dtype=object)
    split[:n_tr] = "train"
    split[n_tr + cfg.embargo: n_tr + n_va] = "val"
    split[n_tr + n_va + cfg.embargo:] = "oot"
    how = (s.index.dayofweek * 24 + s.index.hour).to_numpy()
    frame = pd.DataFrame({"value": s.to_numpy(float), "how": how, "split": split}, index=s.index)
    frame = frame[frame["split"] != ""]
    frame.index.name = "time"

    train = frame.loc[frame["split"] == "train", "value"].to_numpy(float)
    T = cfg.T
    lo, hi = float(np.nanmin(train)), float(np.nanmax(train))
    K = int(round(n_tr / T))
    meta = dict(name=name, n=int(len(frame)), n_train=int(n_tr), lo=lo, hi=hi, T=T, K=K,
                start=str(frame.index[0]), end=str(frame.index[-1]),
                nan_share_train=float(np.isnan(train).mean()),
                data_key=cfg.data_key(name), split_key=cfg.split_key(name))
    return Prepared(name, frame, meta)


def window_layout(meta: dict, cfg: Config) -> dict:
    """Windows of a prepared series from the config — not stored with the data, so changing them
    never re-prepares the series (BENCHMARK.md, Protocol: data): pool size N = max(pool_size, pool_mult · K), slicing
    step s (≈ max_windows windows), end of the core part and start of the holdout part of train
    (the last `holdout_frac`, embargo between them)."""
    n_tr, T, K = int(meta["n_train"]), int(meta["T"]), int(meta["K"])
    hold_len = int(cfg.holdout_frac * n_tr)
    return dict(N=int(max(cfg.pool_size, cfg.pool_mult * K)), s=int(max(1, (n_tr - T) // cfg.max_windows)),
                core_end=int(n_tr - hold_len - cfg.embargo), hold_start=int(n_tr - hold_len))


def save_prepared(p: Prepared, cfg: Config) -> None:
    f = p.frame.reset_index()
    f["how"] = f["how"].astype(np.int16)
    f["split"] = f["split"].astype("category")
    write_table(f, cfg.processed_dir / f"{p.name}.parquet", keep64=["value"])
    write_record(p.meta, cfg.processed_dir / f"{p.name}.meta.parquet")


def prepared_exists(name: str, cfg: Config) -> bool:
    """Prepared with the current data settings (split, points, T); stale data is redone."""
    f = cfg.processed_dir / f"{name}.meta.parquet"
    return f.exists() and (cfg.processed_dir / f"{name}.parquet").exists() \
        and read_record(f).get("data_key") == cfg.data_key(name)


def load_prepared(name: str, cfg: Config) -> Prepared:
    frame = pd.read_parquet(cfg.processed_dir / f"{name}.parquet").set_index("time")
    frame["split"] = frame["split"].astype(str)
    meta = read_record(cfg.processed_dir / f"{name}.meta.parquet")
    meta = {k: (v.item() if hasattr(v, "item") else v) for k, v in meta.items()}
    if meta.get("data_key") != cfg.data_key(name):
        raise RuntimeError(f"{cfg.processed_dir / name}: prepared with other data settings (split, max_points, "
                           f"T …) than this config — run the `prepare` stage first")
    p = Prepared(name, frame, meta)
    check_data_hash(p, cfg)
    return p


# ─────────────────────── content hashes ────────────────────────────────────
def content_hash(p: Prepared) -> str:
    """Hash of the prepared series itself (time, value, hour of week, split), independent of the
    Parquet writer: the same numbers give the same hash on any machine and library version."""
    f = p.frame
    h = hashlib.sha256()
    h.update(f.index.to_numpy().astype("datetime64[ns]").view(np.int64).tobytes())
    v = f["value"].to_numpy(np.float64)
    h.update(np.where(np.isnan(v), np.nan, v).tobytes())      # one NaN bit pattern
    h.update(f["how"].to_numpy(np.int64).tobytes())
    h.update("\n".join(f["split"].astype(str)).encode())
    return h.hexdigest()[:16]


def _read_hashes() -> dict:
    return json.loads(DATA_HASHES_FILE.read_text()) if DATA_HASHES_FILE.exists() else {}


def check_data_hash(p: Prepared, cfg: Config) -> bool | None:
    """Compare the prepared series with the published hash: None — no published hash (custom dataset
    or other data settings), True — the same data, False — different data (warned once per dataset).
    Never an error: the run goes on, but its results are not comparable with the published ones."""
    want = _read_hashes().get(cfg.data_key(p.name), {}).get(p.name)
    if want is None:
        return None
    got = content_hash(p)
    if got != want and (p.name, cfg.data_key(p.name)) not in _warned:
        _warned.add((p.name, cfg.data_key(p.name)))
        warnings.warn(f"dataset {p.name}: the prepared series differ from the published ones (hash {got}, "
                      f"published {want} in {DATA_HASHES_FILE.name}) — the source data have changed; "
                      f"results are not comparable with the published run", stacklevel=2)
    return got == want


def record_data_hashes(cfg: Config, names) -> dict:
    """Write the hashes of prepared datasets still missing from DATA_HASHES_FILE for these data settings;
    existing entries are never overwritten. Returns {dataset: hash} of what was added."""
    allh = _read_hashes()
    added = {}
    for name in names:
        # per-dataset key (`Config.data_key`): datasets of the same settings share an entry
        entry = allh.setdefault(cfg.data_key(name), {"_settings": cfg._key_values(cfg.DATA_KEYS, name)})
        if name in entry or not prepared_exists(name, cfg):
            continue
        frame = pd.read_parquet(cfg.processed_dir / f"{name}.parquet").set_index("time")
        added[name] = entry[name] = content_hash(Prepared(name, frame, {}))
    if added:
        DATA_HASHES_FILE.write_text(json.dumps(allh, indent=2, default=str) + "\n")
    return added


def train_windows(p: Prepared, cfg: Config) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Train in channels, core windows and holdout windows (BENCHMARK.md, Protocol: data)."""
    v, h = p.part("train")
    X = to_channels(v, h, p.lo, p.hi)
    w, T = window_layout(p.meta, cfg), p.meta["T"]
    return X, slide(X[: w["core_end"]], T, w["s"]), slide(X[w["hold_start"]:], T, w["s"])


DESCRIPTOR_TABLE = "descriptors.parquet"         # in tables/: the dataset descriptors of RQ7 and CS15 (written by collect)


def descriptors(cfg: Config) -> pd.DataFrame:
    """Descriptors of the train part of every prepared dataset (RQ7 and CS15): K, autocorrelation at 24 and 168,
    kurtosis of the 24-step differences, volatility clustering, trend relative to the spread, share of gaps."""
    rows = []
    for ds in cfg.datasets:
        p = load_prepared(ds, cfg)
        v, _ = p.part("train")
        s = pd.Series(v)
        d1, d24 = s.diff(), s.diff(24)
        rows.append(dict(dataset=ds, K=p.meta["K"], acf24=s.autocorr(24), acf168=s.autocorr(168),
                         kurt_d24=float(d24.kurt()), volclust=float(d1.abs().autocorr(1)),
                         trend=float(abs(np.polyfit(np.arange(len(s.dropna())), s.dropna(), 1)[0]) * len(s) / s.std()),
                         nan_share=float(s.isna().mean())))
    return pd.DataFrame(rows)
