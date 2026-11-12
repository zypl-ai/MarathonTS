"""Benchmark of long synthetic time-series generation: pool generators + stitching against
long-series generators, on open datasets. Hardware-agnostic (CUDA when available,
else CPU), all storage Parquet, every component pluggable through `bench.registry`.

Stages (resumable): raw → prepare → pools → generate → fidelity → utility → collect. See BENCHMARK.md
and EXTENDING.md.
"""
from . import registry
from .config import DATASETS, METHODS, METHODS_MIN, Config

__all__ = ["Config", "DATASETS", "METHODS", "METHODS_MIN", "registry"]
