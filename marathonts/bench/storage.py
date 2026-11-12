"""Parquet storage: every table, series, pool and set of weights is a zstd-compressed Parquet file.

* `write_table / read_table` — DataFrames (floats downcast to float32 unless listed in `keep64`).
* `write_arrow` — a pyarrow Table as is (vector predictions / labels as native list columns).
* `write_arrays / read_arrays` — named numpy arrays of any shape (pools, model weights, opaque
  blobs): one row per array with its dtype, shape and raw bytes; zstd compresses the bytes.
* `write_record / read_record` — a dict as a one-row table (timings, run info).
* `is_valid` / `check_done` — a unit counts as done only if its file reads back; a file truncated
  by an interrupted run is renamed `*.bad` and the unit is redone.
* A Git LFS pointer in place of a file (the repository cloned without Git LFS) stops the run with
  `LfsPointerError` instead: it is neither read nor renamed.

Writes are atomic: data go to a hidden temp file (`.<name>.tmp`) that is renamed at the end, so
an interruption never leaves a half-written `*.parquet` and globs never see temp files.
"""
from __future__ import annotations

import io
import json
import pickle
from pathlib import Path
from typing import Iterable, Mapping

import numpy as np
import pandas as pd

COMPRESSION = "zstd"
LEVEL = 9
# arrays kept in float32 whatever `weights_dtype` is (normalisation statistics: float16 under-
# and overflows them — a std of 1e-8 becomes 0, a mean above 65504 becomes inf)
FLOAT32_SUFFIXES = ("x_mean", "x_std", "y_mean_std")


LFS_POINTER = b"version https://git-lfs.github.com/spec/"


class LfsPointerError(RuntimeError):
    """A Git LFS pointer where a Parquet file should be."""


def _check_lfs(path: Path) -> None:
    with open(path, "rb") as f:
        if f.read(len(LFS_POINTER)) == LFS_POINTER:
            raise LfsPointerError(
                f"{path} is a Git LFS pointer, not the file: the repository was cloned without Git LFS. "
                "Run `git lfs install && git lfs pull` (or download the artifacts, README) and start again; "
                "nothing was changed.")


def _tmp(path: Path) -> Path:
    return path.with_name(f".{path.name}.tmp")


def _prepare(df: pd.DataFrame, keep64: Iterable[str] = ()) -> pd.DataFrame:
    keep64 = set(keep64)
    out = df.copy()
    for c in out.columns:
        if c in keep64:
            continue
        if out[c].dtype == np.float64:
            out[c] = out[c].astype(np.float32)
        elif out[c].dtype == object:
            first = out[c].dropna().head(1)
            if len(first) and isinstance(first.iloc[0], dict):          # dicts → JSON; lists stay lists
                out[c] = out[c].map(lambda v: json.dumps(v, default=float) if isinstance(v, dict) else v)
    return out


def write_table(df: pd.DataFrame, path: Path, keep64: Iterable[str] = ()) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = _tmp(path)
    _prepare(df, keep64).to_parquet(tmp, compression=COMPRESSION, compression_level=LEVEL, index=False)
    tmp.replace(path)
    return path


def write_arrow(table, path: Path) -> Path:
    import pyarrow.parquet as pq

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = _tmp(path)
    pq.write_table(table, tmp, compression=COMPRESSION, compression_level=LEVEL)
    tmp.replace(path)
    return path


def read_table(path: Path) -> pd.DataFrame:
    _check_lfs(path)
    return pd.read_parquet(path)


def is_valid(path: Path) -> bool:
    """The file exists and its Parquet footer reads; a Git LFS pointer raises `LfsPointerError`."""
    path = Path(path)
    if not path.exists():
        return False
    _check_lfs(path)
    try:
        import pyarrow.parquet as pq

        pq.read_metadata(path)
        return True
    except Exception:
        return False


def check_done(*paths: Path) -> bool:
    """All files exist and read; an unreadable one (truncated by an interruption) is renamed
    `<name>.bad` so the unit is redone instead of blocking the later stages."""
    ok = True
    for p in map(Path, paths):
        if not p.exists():
            ok = False
        elif not is_valid(p):
            p.replace(p.with_name(p.name + ".bad"))
            ok = False
    return ok


def write_record(rec: Mapping, path: Path) -> Path:
    flat = {k: (json.dumps(v, default=float) if isinstance(v, (list, dict, tuple)) else v) for k, v in rec.items()}
    return write_table(pd.DataFrame([flat]), path, keep64=[k for k, v in flat.items() if isinstance(v, float)])


def read_record(path: Path) -> dict:
    return read_table(path).iloc[0].to_dict()


def write_arrays(arrays: Mapping[str, np.ndarray], path: Path, dtype: str | None = "float32") -> Path:
    """Named arrays → Parquet. Floating arrays are cast to `dtype` (None keeps them), except the
    normalisation statistics (`FLOAT32_SUFFIXES`), which stay float32."""
    rows = []
    for name, a in arrays.items():
        a = np.asarray(a)
        if dtype and a.dtype.kind == "f":
            a = a.astype(np.float32 if name.endswith(FLOAT32_SUFFIXES) and dtype == "float16" else dtype)
        a = np.ascontiguousarray(a)
        rows.append({"name": name, "dtype": a.dtype.str, "shape": json.dumps(list(a.shape)), "data": a.tobytes()})
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = _tmp(path)
    pd.DataFrame(rows, columns=["name", "dtype", "shape", "data"]).to_parquet(
        tmp, compression=COMPRESSION, compression_level=LEVEL, index=False)
    tmp.replace(path)
    return path


def read_arrays(path: Path) -> dict[str, np.ndarray]:
    _check_lfs(path)
    df = pd.read_parquet(path)
    return {r.name: np.frombuffer(r.data, dtype=np.dtype(r.dtype)).reshape(json.loads(r.shape)).copy()
            for r in df.itertuples()}


def blob(obj) -> np.ndarray:
    """Any picklable object as a uint8 array (stored with `write_arrays`; zstd compresses it)."""
    buf = io.BytesIO()
    pickle.dump(obj, buf, protocol=pickle.HIGHEST_PROTOCOL)
    return np.frombuffer(buf.getvalue(), dtype=np.uint8)


def unblob(a: np.ndarray):
    return pickle.loads(np.asarray(a, dtype=np.uint8).tobytes())


def torch_state(module, prefix: str = "") -> dict[str, np.ndarray]:
    """A torch module's state_dict as named numpy arrays."""
    return {prefix + k: v.detach().cpu().numpy() for k, v in module.state_dict().items()}


def list_array(mat: np.ndarray):
    """(n, k) numpy → pyarrow list<float32> column without Python lists."""
    import pyarrow as pa

    mat = np.ascontiguousarray(np.asarray(mat, np.float32))
    n, k = mat.shape
    return pa.ListArray.from_arrays(pa.array(np.arange(0, n * k + 1, k, dtype=np.int32)), pa.array(mat.ravel()))
