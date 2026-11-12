"""Wall-clock, CPU time and peak memory of a block, plus the hardware it ran on.

Every timing record carries the hardware fingerprint, so the analysis can flag times measured on
different runtimes (T4 vs A100 vs CPU).
"""
from __future__ import annotations

import os
import platform
import resource
import time
from contextlib import contextmanager


def hardware(use_torch: bool = True) -> dict:
    info = {"platform": platform.platform(), "cpu_count": os.cpu_count(), "gpu": "none"}
    try:
        if not use_torch:
            raise ImportError
        import torch

        if torch.cuda.is_available():
            info["gpu"] = torch.cuda.get_device_name(0)
            info["gpu_mem_gb"] = round(torch.cuda.get_device_properties(0).total_memory / 2**30, 1)
    except Exception:
        pass
    if info["gpu"] == "none":                        # env without torch (tsgm / TensorFlow): ask the driver
        try:
            import subprocess

            out = subprocess.run(["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"],
                                 capture_output=True, text=True, timeout=10).stdout.strip().splitlines()
            if out:
                info["gpu"] = out[0].strip()
        except Exception:
            pass
    try:
        with open("/proc/meminfo") as f:
            info["ram_gb"] = round(int(f.readline().split()[1]) / 2**20, 1)
    except Exception:
        pass
    info.update(library_versions())
    return info


LIBRARIES = ("numpy", "pandas", "scipy", "torch", "scikit-learn", "xgboost", "statsmodels", "pyarrow",
             "tensorflow", "keras", "tsgm", "chronos-forecasting", "timesfm", "timestral", "sdv", "ruptures", "hmmlearn")


def library_versions() -> dict:
    """Installed versions of the libraries the benchmark uses (`v_<name>`; absent ones skipped)."""
    from importlib import metadata

    out = {}
    for lib in LIBRARIES:
        try:
            out[f"v_{lib}"] = metadata.version(lib)
        except metadata.PackageNotFoundError:
            pass
    return out


def _rss_mb() -> float:
    """Current resident memory of the process (psutil); falls back to the lifetime peak."""
    try:
        import psutil

        return psutil.Process().memory_info().rss / 2**20
    except Exception:
        r = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        return r / 2**20 if platform.system() == "Darwin" else r / 2**10   # bytes on macOS, KiB on Linux


@contextmanager
def timed(record: dict, key: str):
    """Adds `<key>_wall_s`, `<key>_cpu_s`, `<key>_gpu_peak_mb` (torch, reset per block) and
    `<key>_rss_delta_mb` (resident memory after − before the block) to `record`."""
    import sys

    torch = None
    try:
        if "tensorflow" in sys.modules and "torch" not in sys.modules:   # TF process (pools): no torch CUDA context
            raise ImportError
        import torch as _t

        if _t.cuda.is_available():
            torch = _t
            torch.cuda.synchronize()
            torch.cuda.reset_peak_memory_stats()
    except Exception:
        pass
    rss0 = _rss_mb()
    w0, c0 = time.perf_counter(), time.process_time()
    try:
        yield
    finally:
        if torch is not None:
            torch.cuda.synchronize()
            record[f"{key}_gpu_peak_mb"] = torch.cuda.max_memory_allocated() / 2**20
        record[f"{key}_wall_s"] = time.perf_counter() - w0
        record[f"{key}_cpu_s"] = time.process_time() - c0
        record[f"{key}_rss_delta_mb"] = _rss_mb() - rss0
