"""Generator interfaces.

**PoolGenerator** — learns from train windows and samples windows; a method combines it with an
assembler (stitcher). Windows are `(n, T, F)` float32 in the benchmark channels: channel 0 —
value min-max scaled by train (`ctx.lo / ctx.hi`), channels 1–2 — `(sin + 1) / 2`, `(cos + 1) / 2`
of the hour of week. Train data come in the same form: `ctx.X_core` (training windows),
`ctx.X_hold` (holdout windows for early stopping), `ctx.X_train` (the whole train, (L, F)).

**LongGenerator** — produces the long series itself: `generate(ctx) -> (values, how, seams)`,
values in real units of length `ctx.L`, hour of week per point, seam positions (indices where a
newly generated piece starts; empty if none).

Both may return weights from `state()` — a dict of numpy arrays (use `storage.torch_state`,
`storage.blob` for anything picklable); the benchmark saves them as Parquet. `load_state(arrays,
ctx)` is the inverse: it restores a fitted generator from those arrays without training
(`bench.load.load_generator` reads them from the artifacts). `info` holds training diagnostics
(stored in the run record).

Register:

    from marathonts.bench import registry as R
    from marathonts.bench.generators.base import PoolGenerator

    @R.pool_generators.register("my_gan")
    class MyGAN(PoolGenerator):
        def fit(self, ctx): ...
        def sample(self, n, ctx): return windows      # (n, T, 3) in [0, 1]

Parameters of a custom generator: `Config(extra={"my_gan": {...}})` → `ctx.params`.

Environments: a generator may need its own dependencies (TensorFlow for tsgm, SDV, …). Set
`env = "<name>"` and list them in `envs/<name>.txt`. Pools are cached as artifacts, so the stage
`pools` can run in that environment and the rest of the pipeline in the base one (BENCHMARK.md).
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from ..config import Config
from ..data import Prepared, train_windows


@dataclass
class GenContext:
    p: Prepared
    cfg: Config
    seed: int
    name: str                                    # registry name of the component
    device: str = "cpu"
    _win: tuple | None = field(default=None, repr=False)
    k_override: int | None = None                # an assembler asked for more windows than K (seam processing)

    @property
    def params(self) -> dict:
        return self.cfg.params(self.name)

    def _windows(self):
        if self._win is None:
            self._win = train_windows(self.p, self.cfg)
        return self._win

    @property
    def X_train(self) -> np.ndarray:
        return self._windows()[0]

    @property
    def X_core(self) -> np.ndarray:
        return self._windows()[1]

    @property
    def X_hold(self) -> np.ndarray:
        return self._windows()[2]

    @property
    def T(self) -> int:
        return self.p.meta["T"]

    @property
    def K(self) -> int:
        """Windows the assembler returns: the series' K, or more for a method with seam processing."""
        return self.k_override or self.p.meta["K"]

    @property
    def N(self) -> int:
        from ..data import window_layout

        return window_layout(self.p.meta, self.cfg)["N"]

    @property
    def L(self) -> int:
        return self.p.meta["K"] * self.T

    @property
    def lo(self) -> float:
        return self.p.lo

    @property
    def hi(self) -> float:
        return self.p.hi

    def train_series(self) -> tuple[np.ndarray, np.ndarray]:
        return self.p.part("train")


def missing_requirements(cls) -> list[str]:
    """Modules a generator class needs (`requires`) that are not importable in this environment."""
    import importlib.util

    return [m for m in getattr(cls, "requires", ()) if importlib.util.find_spec(m) is None]


class PoolGenerator:
    info: dict
    env: str = "core"            # environment it needs (envs/<env>.txt); "core" = the main environment
    requires: tuple = ()         # importable modules it needs, checked before fitting

    def __init__(self):
        self.info = {}

    def fit(self, ctx: GenContext) -> None:
        raise NotImplementedError

    def sample(self, n: int, ctx: GenContext) -> np.ndarray:
        raise NotImplementedError

    def state(self) -> dict[str, np.ndarray]:
        return {}

    def load_state(self, arrays: dict[str, np.ndarray], ctx: "GenContext"):
        """Restore a fitted generator from `state()` arrays; returns self."""
        raise NotImplementedError(f"{type(self).__name__} cannot load weights")


class LongGenerator:
    info: dict
    env: str = "core"
    requires: tuple = ()
    uses_windows: bool = False   # trains on ctx.X_core / X_hold: the training-window settings enter its fingerprint

    def __init__(self):
        self.info = {}

    def fit(self, ctx: GenContext) -> None:
        """Optional training step (timed separately as `fit`)."""

    def generate(self, ctx: GenContext) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        raise NotImplementedError

    def state(self) -> dict[str, np.ndarray]:
        return {}

    def load_state(self, arrays: dict[str, np.ndarray], ctx: "GenContext"):
        """Restore a fitted generator from `state()` arrays; returns self."""
        raise NotImplementedError(f"{type(self).__name__} cannot load weights")


def calendar_channels(how: np.ndarray) -> np.ndarray:
    """Hour of week → the two calendar channels in [0, 1]."""
    a = 2 * np.pi * np.asarray(how) / 168
    return np.column_stack([(np.sin(a) + 1) / 2, (np.cos(a) + 1) / 2]).astype(np.float32)
