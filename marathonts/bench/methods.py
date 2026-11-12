"""Stage 2 — methods: every method produces one series of length K·T per (dataset, seed).

A method is either a pool generator + an assembler (+ optionally a joiner that processes the
seams, `bench.joiners`), or a long generator:

    from marathonts.bench.methods import register_method
    register_method("gan_greedy", pool="my_gan", assembler="greedy")
    register_method("gan_greedy_xfade", pool="my_gan", assembler="greedy", joiner="crossfade")
    register_method("my_long", long="my_long_generator")

The whole stitching suite on another pool generator at once — `register_stitch_suite("gan", "my_gan")`
(gan_zseries, gan_rand, …), or in the config: `Config(pool_suites={"vae": "tsgm_vae", "gan": "my_gan"})`.

Built-in methods (the suite on the tsgm VAE pool, prefix "vae")
-----------------------------------------------------------------
vae_zseries       tsgm VAE pool + zseries, the proprietary stitching method of zypl.ai (under development):
                  published results (`Config.frozen_methods`), code not in the repository.
vae_rand          the same pool, random path (BENCHMARK.md, What is compared).
vae_rand_b        the same, another permutation seed — with vae_rand gives the noise floor (mid, max).
Alternatives on the same pool (BASELINES.md A — other choice / order of the windows):
vae_greedy        nearest neighbour by the jump at the seam.
vae_atsp          ATSP tour over the pool (LKH) by the jump at the seam, its cheapest run of K windows.
vae_pctsp         prize-collecting TSP (OR-Tools) by the jump at the seam: choice and order at once.
vae_mbb           matched-block bootstrap (Carlstein et al. 1998).
vae_knn           k-nearest-neighbour resampling (Lall & Sharma 1996).
vae_quilting      image quilting (Efros & Freeman 2001): patch choice + minimum-error boundary cut.
vae_herding       kernel-herding choice (MMD to train), random order.
Seam processing (BASELINES.md B), over the zseries stitcher's path (published results; max: over every stitcher but the
random path and vae_quilting):
vae_zseries_xfade overlap-add with a Hann crossfade.
vae_zseries_wsola WSOLA: shift to the best correlation, then crossfade.
vae_zseries_quilt minimum-error cut inside the overlap.
Long-series baselines:
diffusion_ts      Diffusion-TS, autoregressive infill.
chronos           Chronos sampling.
timesfm           TimesFM 3.0 (Google), zero-shot median forecast of the whole horizon.
timestral         Timestral (Mistral), zero-shot median forecast, block by block.

Artifacts (all Parquet, see `Artifacts`): the pool and the pool generator's weights per
(dataset, generator, seed) — shared by every method on that pool; per (dataset, method, seed)
the series (value, hour of week, pool window, piece, seam flag per point) and the run record
(timings fit / sample / assemble, memory, diagnostics, hardware).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd

from . import registry as R
from .config import Config
from .data import Prepared, from_channels
from .generators.base import GenContext
from .storage import check_done, read_arrays, read_record, read_table, write_arrays, write_record, write_table
from .timing import hardware, timed


# ─────────────────────── artifact paths ────────────────────────────────────
class Artifacts:
    """Layout of `cfg.artifacts_dir`."""

    def __init__(self, cfg: Config):
        self.root = Path(cfg.artifacts_dir)

    def pool(self, ds, gen, seed):
        return self.root / "pools" / ds / gen / f"seed{seed}.parquet"

    def pool_record(self, ds, gen, seed):
        return self.root / "pools" / ds / gen / f"seed{seed}.record.parquet"

    def generator_weights(self, ds, gen, seed):
        return self.root / "generators" / ds / gen / f"seed{seed}.parquet"

    def generator_replica(self, ds, gen, replica):
        """Weights of a pool generator trained once and shared by several seeds."""
        return self.root / "generators" / ds / gen / f"replica{replica}.parquet"

    def series(self, ds, method, seed):
        return self.root / "series" / ds / method / f"seed{seed}.parquet"

    def record(self, ds, method, seed):
        return self.root / "records" / ds / method / f"seed{seed}.parquet"

    def fidelity(self, ds, method, seed):
        return self.root / "fidelity" / ds / method / f"seed{seed}.parquet"

    def labels(self, ds, task):
        return self.root / "labels" / ds / f"{task}.parquet"

    def utility_dir(self, ds, method, seed):
        return self.root / "utility" / ds / method / f"seed{seed}"

    @property
    def tables(self):
        return self.root / "tables"

    @property
    def hypotheses(self):
        return self.root / "hypotheses"


# ─────────────────────── methods ───────────────────────────────────────────
@dataclass(frozen=True)
class MethodSpec:
    name: str
    pool: str | None = None
    assembler: str | None = None
    long: str | None = None
    description: str = ""
    joiner: str | None = None

    def __post_init__(self):
        if (self.long is None) == (self.pool is None or self.assembler is None):
            raise ValueError(f"method {self.name}: give either pool + assembler, or long")
        if self.joiner is not None and self.long is not None:
            raise ValueError(f"method {self.name}: a joiner needs a pool + assembler")


def register_method(name, pool=None, assembler=None, long=None, description="", overwrite=False, joiner=None):
    if name == "real" or "@" in name:
        raise ValueError(f"method name {name!r}: `real` is the real-data pseudo-method (TRTR, the fidelity ceiling) "
                         "and `@` marks length-matched variants (`<method>@len`) — choose another name")
    return R.methods.register(name, MethodSpec(name, pool, assembler, long, description, joiner), overwrite=overwrite)


def register_stitch_suite(prefix: str, pool: str, overwrite: bool = False, extra_assemblers=(),
                          extra_joiners=()) -> list[str]:
    """Register the whole stitching suite (`config.STITCH_SUITE`: the zseries stitcher, the random path, the
    alternative stitchers of BASELINES.md A–B) on one pool generator: <prefix>_zseries, <prefix>_rand, … —
    plus custom assemblers (<prefix>_<name>) and every seam-processing variant of every stitcher
    (<prefix>_<stitcher>_<tag>; which of them run is `Config.smooth_paths` / `joiners`). Every method of the suite shares the pool, so they differ only in the
    choice, order and seams of the windows. Idempotent; a name already registered with another
    pool / assembler raises unless `overwrite`. Returns the method names."""
    from .config import suite_entries

    names = []
    for suffix, asm, joiner, desc in suite_entries(extra_assemblers, extra_joiners, "all"):
        name = f"{prefix}_{suffix}"
        names.append(name)
        if name in R.methods and not overwrite:
            old = R.methods.get(name)
            if (old.pool, old.assembler, old.joiner) != (pool, asm, joiner):
                raise KeyError(f"method {name} is already registered with pool {old.pool}, "
                               f"assembler {old.assembler} (pass overwrite=True or another prefix)")
            continue
        register_method(name, pool=pool, assembler=asm, joiner=joiner, description=desc, overwrite=overwrite)
    return names


def register_long_method(name: str, long: str | None = None) -> str:
    """A long generator as a method (by default under its own name); idempotent."""
    long = long or name
    if name in R.methods:
        if R.methods.get(name).long != long:
            raise KeyError(f"method {name} is already registered and is not the long generator {long}")
        return name
    register_method(name, long=long, description=f"long generator {long}")
    return name


register_stitch_suite("vae", "tsgm_vae")
register_method("diffusion_ts", long="diffusion_ts", description="Diffusion-TS autoregressive infill")
register_method("chronos", long="chronos", description="Chronos sampling")
register_method("timesfm", long="timesfm", description="TimesFM 3.0, median forecast")
register_method("timestral", long="timestral", description="Timestral, median forecast")


@dataclass
class Synth:
    values: np.ndarray
    how: np.ndarray
    seams: np.ndarray
    record: dict = field(default_factory=dict)
    window: np.ndarray | None = None          # pool index per point (−1 for long generators)
    piece: np.ndarray | None = None           # index of the generated piece per point

    def frame(self) -> pd.DataFrame:
        L = len(self.values)
        seam = np.zeros(L, bool)
        sv = np.asarray(self.seams, int)
        seam[sv[(sv > 0) & (sv < L)]] = True
        piece = self.piece if self.piece is not None else np.cumsum(seam)
        window = self.window if self.window is not None else np.full(L, -1)
        return pd.DataFrame({"t": np.arange(L, dtype=np.int32), "value": np.asarray(self.values, np.float64),
                             "how": np.asarray(self.how, np.int16), "window": np.asarray(window, np.int32),
                             "piece": np.asarray(piece, np.int32), "seam": seam})


def save_synth(cfg: Config, ds: str, method: str, seed: int, s: Synth) -> None:
    A = Artifacts(cfg)
    # the record (with unit_fp) last: if a re-run dies in between, the old record marks the new series stale
    write_table(s.frame(), A.series(ds, method, seed), keep64=["value"])
    write_record(s.record, A.record(ds, method, seed))


# ─────────────────────── unit fingerprints (resume) ─────────────────────────
def train_fp(cfg: Config, gen: str, ds: str | None = None) -> str:
    """What a trained pool generator depends on: the data, its training settings and the training
    windows — not the pool size, its sampling settings or how many replicas there are (replica r is
    always trained with seed r)."""
    return cfg.unit_fingerprint(gen, "windows", dataset=ds)


def pool_fp(cfg: Config, gen: str, ds: str | None = None) -> str:
    """What a pool depends on: the trained generator, which model a seed uses, the sampling settings
    and the pool size (a new size resamples the pool from the stored generator, it does not retrain it)."""
    return cfg.unit_fingerprint("pool_size", "pool_train", f"{gen}:sample", upstream=(train_fp(cfg, gen, ds),),
                                dataset=ds)


def series_fp(cfg: Config, method: str, ds: str | None = None) -> str:
    """What a method's series on dataset `ds` depends on; "real" for the real series."""
    R.load_builtins()                         # long generators / assemblers may not be imported yet (collect)
    if method == "real":
        return cfg.unit_fingerprint(dataset=ds)
    spec = R.methods.get(method)
    if spec.long:
        cls = R.long_generators.get(spec.long)
        k = getattr(cfg, "diffusion_train_replicas", 1) or 1   # enters only when > 1 (units of one model stay valid)
        up = (f"dts_replicas={k}",) if spec.long == "diffusion_ts" and not cfg.dts_train_per_seed and k > 1 else ()
        return cfg.unit_fingerprint(spec.long, *(("windows",) if getattr(cls, "uses_windows", False) else ()),
                                    upstream=up, dataset=ds)
    parts = (spec.assembler,) + ((spec.joiner,) if spec.joiner else ())
    targets = ("targets",) if getattr(R.assemblers.get(spec.assembler), "uses_targets", False) else ()
    return cfg.unit_fingerprint(*parts, upstream=(pool_fp(cfg, spec.pool, ds),), files=targets, dataset=ds)


def is_fresh(rec_path, fp: str) -> bool:
    """The unit's record exists, is readable and was made with the same settings (`unit_fp`)."""
    return check_done(rec_path) and read_record(rec_path).get("unit_fp") == fp


def load_synth(cfg: Config, ds: str, method: str, seed: int, check: bool = True) -> Synth | None:
    """The stored series, or None if missing, truncated or (`check`) made with other settings; `check=False`
    reads the series of a frozen method (`Config.frozen_methods`) as it is."""
    A = Artifacts(cfg)
    p, rp = A.series(ds, method, seed), A.record(ds, method, seed)
    if not check_done(p, rp):                 # missing, or truncated by an interruption (→ *.bad)
        return None
    rec = read_record(rp)
    if check and rec.get("unit_fp") != series_fp(cfg, method, ds):
        return None                           # stale: settings changed since — redone by `generate`
    f = read_table(p)
    return Synth(f["value"].to_numpy(float), f["how"].to_numpy(int), np.flatnonzero(f["seam"].to_numpy()),
                 rec, f["window"].to_numpy(), f["piece"].to_numpy())


def _ctx(p, cfg, seed, name):
    return GenContext(p, cfg, seed, name, cfg.device_str())


def dts_replica(cfg: Config, seed: int) -> int | None:
    """Which shared Diffusion-TS model a seed uses: None — its own (`dts_train_per_seed`); otherwise one of
    `cfg.diffusion_train_replicas` models per dataset (seed % k; k = 1 — the one model per dataset)."""
    if cfg.dts_train_per_seed:
        return None
    return int(seed) % max(1, int(getattr(cfg, "diffusion_train_replicas", 1) or 1))


def dts_shared(cfg: Config, ds: str, replica: int):
    """(weights path, training fingerprint) of a shared Diffusion-TS model; replica 0 of one model per dataset is
    the published `seedshared` (fingerprint without the replica fields)."""
    k = max(1, int(getattr(cfg, "diffusion_train_replicas", 1) or 1))
    tag = "shared" if k == 1 else f"shared_r{replica}of{k}"
    up = () if k == 1 else (f"replica={replica}/{k}",)
    return (Artifacts(cfg).generator_weights(ds, "diffusion_ts", tag),
            cfg.unit_fingerprint("diffusion_ts:train", "windows", upstream=up, dataset=ds))


def train_replica(cfg: Config, seed: int) -> int | None:
    """Which trained generator a seed uses: None — its own (trained on this seed); otherwise one of
    `cfg.pool_train_replicas` models per dataset, shared by the seeds with the same `seed % replicas`
    (the seed still drives the sampling of the pool and the random paths)."""
    r = cfg.pool_train_replicas
    return None if r is None else int(seed) % int(r)


_FITTED: dict = {}          # (artifacts root, dataset, generator, replica, fp) → fitted shared generator (this process)


def _fitted_generator(p, gen, seed, cfg, rec):
    """The trained pool generator of a seed: its own (`pool_train_replicas=None`, trained with this
    seed) or the replica it shares (trained with seed = replica index). Exact weights and a record
    with `train_fp` are stored next to it, so a new pool (e.g. another pool size) reuses the trained
    generator instead of retraining it; own per-seed weights are stored only with
    `save_generator_weights`."""
    from .storage import read_arrays as _ra

    A = Artifacts(cfg)
    rep = train_replica(cfg, seed)
    cls = R.pool_generators.get(gen)
    fp = train_fp(cfg, gen, p.name)
    tseed = seed if rep is None else rep
    w = A.generator_weights(p.name, gen, seed) if rep is None else A.generator_replica(p.name, gen, rep)
    wr = w.with_suffix(".record.parquet")
    save = rep is not None or cfg.save_generator_weights
    key = (str(A.root), p.name, gen, rep, fp)
    r0: dict = {}
    if rep is not None and key in _FITTED and is_fresh(wr, fp):
        g, trained = _FITTED[key], False
    elif check_done(w) and is_fresh(wr, fp):
        g, trained = cls(), False
        try:
            g.load_state(_ra(w), _ctx(p, cfg, tseed, gen))
        except NotImplementedError:              # no load_state: train again, same seed
            trained = True
            with timed(r0, "fit"):
                g.fit(_ctx(p, cfg, tseed, gen))
    else:
        g, trained = cls(), True
        with timed(r0, "fit"):
            g.fit(_ctx(p, cfg, tseed, gen))
        if save:
            write_arrays(g.state() or {"_": np.zeros(1)}, w, dtype=None)   # exact weights: reused by new pools
            write_record({**g.info, "train_wall_s": r0["fit_wall_s"], **{f"train_{k}": v for k, v in r0.items()},
                          "unit_fp": fp}, wr)
    if rep is not None:
        _FITTED[key] = g
    if "fit_wall_s" in r0 or not wr.exists():          # trained here (or no record): this run's cost
        rr = {**g.info, "train_wall_s": r0.get("fit_wall_s", 0.0)}
    else:
        rr = read_record(wr)
    # every seed reports the cost of producing its generator (RQ6), as for a shared Diffusion-TS
    rec["fit_wall_s"] = float(rr["train_wall_s"])
    rec.update({k: v for k, v in rr.items() if k not in ("train_wall_s", "unit_fp") and not k.startswith("train_")})
    rec.update(train_replica=rep, generator_trained_here=trained)
    return g, rep


def get_pool(p: Prepared, gen: str, seed: int, cfg: Config) -> tuple[np.ndarray, dict]:
    """The pool of `gen` on (dataset, seed), cached as Parquet. The generator is trained on this seed
    (`pool_train_replicas=None`) or shared with other seeds (one of `pool_train_replicas` models)."""
    A = Artifacts(cfg)
    pp, pr = A.pool(p.name, gen, seed), A.pool_record(p.name, gen, seed)
    fp = pool_fp(cfg, gen, p.name)
    if check_done(pp) and is_fresh(pr, fp):
        return read_arrays(pp)["pool"], read_record(pr)
    ctx = _ctx(p, cfg, seed, gen)
    rec: dict = {}
    g, rep = _fitted_generator(p, gen, seed, cfg, rec)
    with timed(rec, "sample"):
        pool = np.asarray(g.sample(ctx.N, ctx), np.float32)
    F = ctx.X_core.shape[2]
    if pool.shape[1:] != (ctx.T, F) or len(pool) < ctx.K:
        raise ValueError(f"{gen}: sample() must return (n ≥ K, {ctx.T}, {F}), got {pool.shape}")
    rec.update(g.info)
    import sys

    hw = hardware(use_torch="tensorflow" not in sys.modules or "torch" in sys.modules)   # pools may come from another env (RQ6)
    rec.update(pool_gpu=hw.get("gpu"), pool_platform=hw.get("platform"), pool_cpu_count=hw.get("cpu_count"))
    rec["unit_fp"] = fp
    write_arrays({"pool": pool}, pp, dtype=None)
    write_record(rec, pr)                     # last: unit_fp marks the pool as done
    return pool, rec


def generate(method: str, p: Prepared, seed: int, cfg: Config) -> Synth:
    R.load_builtins()
    spec: MethodSpec = R.methods.get(method)
    T, K = p.meta["T"], p.meta["K"]
    if spec.long is None:
        pool, pool_rec = get_pool(p, spec.pool, seed, cfg)
        rec = dict(pool_rec)
        ctx = _ctx(p, cfg, seed, spec.assembler)
        asm = R.assemblers.get(spec.assembler)()
        from .generators.base import missing_requirements

        miss = missing_requirements(asm)
        if miss:
            raise ImportError(f"assembler {spec.assembler} needs {miss} (envs/core.txt)")
        joiner = R.joiners.get(spec.joiner)() if spec.joiner else None
        need = joiner.windows_needed(K, T, cfg) if joiner else K
        if need > len(pool):
            raise ValueError(f"{method}: needs {need} windows, the pool has {len(pool)} — raise pool_size / pool_mult")
        ctx.k_override = need if need != K else None
        with timed(rec, "assemble"):
            path, info = asm.assemble(pool, ctx)
            path = np.asarray(path, int)
            if len(path) != need:
                raise ValueError(f"{spec.assembler}: path of length {len(path)}, expected {need}")
            if joiner:
                X, seams, src, jinfo = joiner.join(pool[path], K * T, cfg)
                info = {**info, **jinfo}
        rec.update(info)
        if joiner:
            v, how = from_channels(X, p.lo, p.hi)
            s = Synth(v, how, seams, rec, window=path[src], piece=src)
        else:
            v, how = from_channels(np.concatenate(pool[path]), p.lo, p.hi)
            s = Synth(v, how, np.arange(1, K) * T, rec, window=np.repeat(path, T),
                      piece=np.repeat(np.arange(K), T))
    else:
        ctx = _ctx(p, cfg, seed, spec.long)
        g = R.long_generators.get(spec.long)()
        rec: dict = {}
        with timed(rec, "fit"):
            g.fit(ctx)
        if hasattr(g, "load_s"):                     # cached pretrained model: report its load time
            rec["fit_wall_s"] = g.load_s
        with timed(rec, "sample"):
            v, how, seams = g.generate(ctx)
        v, how = np.asarray(v, float), np.asarray(how, int)
        if len(v) != ctx.L:
            raise ValueError(f"{spec.long}: generate() returned {len(v)} points, expected K·T={ctx.L}")
        rec["assemble_wall_s"] = 0.0
        rec.update(g.info)
        if cfg.save_generator_weights and not g.info.get("dts_shared"):    # a shared model is saved once
            st = g.state()
            if st:
                write_arrays(st, Artifacts(cfg).generator_weights(p.name, spec.long, seed), dtype=cfg.weights_dtype)
        s = Synth(v, how, np.asarray(seams, int), rec)
    r = s.record
    r["total_wall_s"] = sum(float(r.get(f"{k}_wall_s", 0.0)) for k in ("fit", "sample", "assemble"))
    hw = hardware()
    r.update(method=method, dataset=p.name, seed=seed, K=K, T=T, length=int(len(s.values)),
             config_fingerprint=cfg.fingerprint(), unit_fp=series_fp(cfg, method, p.name),
             pool_generator=spec.pool or "", assembler=spec.assembler or "", joiner=spec.joiner or "",
             long_generator=spec.long or "",
             gpu=hw.get("gpu"), cpu_count=hw.get("cpu_count"), platform=hw.get("platform"))
    return s
