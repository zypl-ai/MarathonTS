"""Benchmark runner: sequential, resumable stages; all storage is Parquet.

    python -m marathonts.bench.run raw                # data/raw: original CSV / TXT → Parquet (download if missing)
    python -m marathonts.bench.run prepare            # data/raw → data/processed (last cfg.max_points points)
    python -m marathonts.bench.run targets            # once: propose missing exogenous target parameters (not in `all`)
    python -m marathonts.bench.run hashes             # once: record content hashes of the prepared data (not in `all`)
    python -m marathonts.bench.run pools              # pool generators: fit + sample (can run in their own env)
    python -m marathonts.bench.run generate           # series (pools read from artifacts), long generators
    python -m marathonts.bench.run fidelity           # F-metrics per series
    python -m marathonts.bench.run utility            # U-metrics, predictions, model weights
    python -m marathonts.bench.run collect            # artifacts/<profile>/* → artifacts/<profile>/tables/*.parquet
    python -m marathonts.bench.run freeze             # tables/frozen.json: the settings of the results published without code
    python -m marathonts.bench.run all [--profile min|mid|max] [--quick] [--datasets ett bike] [--methods vae_greedy chronos]
                            [--seeds 0 1] [--models linear gbdt] [--config cfg.json]
                            [--plugins my_plugins.py]     # register custom components first

Every unit of work writes its own files and is skipped when they exist, so a Colab runtime
that disconnects resumes where it stopped. Notebooks call the same functions:
`from marathonts.bench.run import stage_generate; stage_generate(cfg)`.
"""
from __future__ import annotations

import argparse
import dataclasses
import json
import traceback
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

from . import registry as R
from .config import ROOT, Config
from .data import (DATA_HASHES_FILE, check_data_hash, load_prepared, prepare, prepared_exists,
                   record_data_hashes, save_prepared)
from .fidelity import GROUP_OF, fidelity
from .methods import Artifacts, Synth, generate, is_fresh, load_synth, pool_fp, save_synth, series_fp
from .storage import check_done, read_record, read_table, write_record, write_table
from .timing import hardware, timed
from .tasks import target_params
from .utility import run_utility


def _log(*a):
    from .progress import log

    log(" ".join(map(str, a)))


class _Prepared:
    """Prepared datasets loaded once per stage."""

    def __init__(self, cfg):
        self.cfg, self.cache = cfg, {}

    def __getitem__(self, ds):
        if ds not in self.cache:
            self.cache[ds] = load_prepared(ds, self.cfg)
        return self.cache[ds]


def _ready(cfg: Config) -> list[str]:
    """Datasets prepared with the current data settings; the others are reported and skipped."""
    out = []
    for ds in cfg.datasets:
        if prepared_exists(ds, cfg):
            out.append(ds)
        else:
            _log(f"   skip {ds}: not prepared with these data settings — run the `prepare` stage")
    return out


def _err_msg(cfg: Config, where: str, e: Exception):
    """`_err` for an exception that was caught elsewhere (no active traceback)."""
    p = Path(cfg.artifacts_dir) / "errors.log"
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a") as f:
        f.write(f"== {where}\n" + "".join(traceback.format_exception(e)) + "\n")
    _log(f"   FAILED {where}: {type(e).__name__}: {e}")


def _err(cfg: Config, where: str, e: Exception):
    p = Path(cfg.artifacts_dir) / "errors.log"
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a") as f:
        f.write(f"== {where}\n{traceback.format_exc()}\n")
    _log(f"   FAILED {where}: {type(e).__name__}: {e}")


def load_plugins(paths) -> None:
    """Import Python files that register custom components (datasets, generators, models, …) — once
    per process (`config.load_plugins`). Usually not needed: `Config(plugins=[...])` loads them."""
    from .config import load_plugins as _load

    _load(paths)


# ─────────────────────── stages ────────────────────────────────────────────
def check_datasets(cfg: Config) -> None:
    """Every dataset of the run is registered (built-in or from `cfg.plugins`): a misspelt name stops here
    with the list of known ones instead of failing per stage."""
    R.load_builtins()
    unknown = [d for d in cfg.datasets if d not in R.datasets]
    if unknown:
        raise KeyError(f"datasets {unknown} are not registered; known: {', '.join(R.datasets.names())} "
                       "(a custom dataset: register it in a plugin file listed in Config.plugins, EXTENDING.md)")


def stage_raw(cfg: Config):
    from .datasets import convert_raw, download_raw, raw_path

    check_datasets(cfg)
    for ds in cfg.datasets:
        spec = R.datasets.get(ds)
        if not spec.raw_files or all(raw_path(cfg, ds, f).exists() for f in spec.raw_files):
            continue                                      # custom dataset (own storage) or done
        originals = [cfg.raw_dir / ds / orig for orig, _ in spec.raw_files.values()]
        try:
            if any(o.exists() for o in originals):
                _log(f"raw {ds}: converting to Parquet")
                convert_raw(cfg, [ds])
            else:
                _log(f"raw {ds}: downloading")
                download_raw(cfg, [ds])
        except Exception as e:                          # e.g. no Kaggle credentials: the others go on
            _err(cfg, f"raw {ds}", e)


def stage_prepare(cfg: Config):
    """Hourly series, split, scaling of every dataset of the run. A dataset without task thresholds in
    `cfg.target_params_file` (a new one) gets them proposed by the tasks' rules on its train split and
    written to the file — exogenous for every later stage; review and commit the file."""
    from .tasks import freeze_target_params, missing_target_params

    check_datasets(cfg)

    for ds in cfg.datasets:
        if not prepared_exists(ds, cfg):
            _log(f"prepare {ds}")
            try:
                p = prepare(ds, cfg)
                save_prepared(p, cfg)
                if check_data_hash(p, cfg) is False:
                    _log(f"   WARNING: {ds} differs from the published data ({DATA_HASHES_FILE.name})")
            except Exception as e:
                _err(cfg, f"prepare {ds}", e)
                continue
        try:
            miss = missing_target_params(cfg, ds, cfg.tasks)
            if miss:
                freeze_target_params(cfg, [ds], miss)
                _log(f"   {ds}: task thresholds proposed on train for {len(miss)} tasks → "
                     f"{cfg.target_params_file.name} (review and commit)")
        except Exception as e:
            _err(cfg, f"targets {ds}", e)


def _pool_generators(cfg: Config) -> list[str]:
    R.load_builtins()
    if cfg.pool_generators is not None:
        return list(cfg.pool_generators)
    return sorted({R.methods.get(m).pool for m in cfg.methods if R.methods.get(m).pool})


def _pool_done(cfg, A, ds, gen, seed) -> bool:
    return check_done(A.pool(ds, gen, seed)) and is_fresh(A.pool_record(ds, gen, seed), pool_fp(cfg, gen, ds))


def _tf_first_if_needed(cfg: Config, gens) -> None:
    """TF before torch initialises CUDA (cuDNN load order) — only if a tsgm pool will be fitted here."""
    from .methods import Artifacts

    A = Artifacts(cfg)
    from .generators.base import missing_requirements

    if any(getattr(R.pool_generators.get(g), "env", "") == "tsgm" and not missing_requirements(R.pool_generators.get(g))
           and not _pool_done(cfg, A, ds, g, s) for g in gens for ds in cfg.datasets for s in cfg.seeds):
        from .generators.builtin import init_tensorflow

        init_tensorflow()


_ENV_WARNED: set = set()


def _needs_other_env(name, registry) -> bool:
    """True (and one log line) if the component's dependencies are missing in this environment."""
    from .generators.base import missing_requirements

    cls = registry.get(name)
    miss = missing_requirements(cls)
    if miss and name not in _ENV_WARNED:
        _ENV_WARNED.add(name)
        env = getattr(cls, "env", "?")
        _log(f"   skip {name}: needs {', '.join(miss)} — run it in its environment (envs/{env}.txt), e.g. "
             f"`python -m marathonts.bench.run pools --pool-generators {name}` there"
             if registry is R.pool_generators else
             f"   skip {name}: needs {', '.join(miss)} — run `generate --methods …` in envs/{env}.txt")
    return bool(miss)


def stage_pools(cfg: Config):
    """Fit every pool generator and sample its pool (artifacts/pools, generators). Runs in the
    generator's own environment if it has one (e.g. `envs/tsgm.txt`); `generate` then only reads
    the pools and never imports that generator's dependencies."""
    from .methods import get_pool

    from .progress import bar

    gens = _pool_generators(cfg)
    _tf_first_if_needed(cfg, gens)
    A, P = Artifacts(cfg), _Prepared(cfg)
    todo = [(ds, g, seed) for ds in _ready(cfg) for seed in cfg.seeds for g in gens
            if not _pool_done(cfg, A, ds, g, seed) and not _needs_other_env(g, R.pool_generators)]
    with bar(todo, desc="pools", unit="pool") as it:
        for ds, g, seed in it:
            it.set_postfix_str(f"{ds} {g} seed{seed}")
            try:
                get_pool(P[ds], g, seed, cfg)
            except Exception as e:
                _err(cfg, f"pool {ds} {g} seed{seed}", e)


def stage_generate(cfg: Config):
    """Series of every method. Pool-based methods read the cached pools (stage `pools`; computed
    here if missing); long generators run here."""
    from .progress import bar

    _tf_first_if_needed(cfg, _pool_generators(cfg))
    A, P = Artifacts(cfg), _Prepared(cfg)
    todo = []
    for ds in _ready(cfg):
        for seed in cfg.seeds:
            for m in cfg.methods:
                if load_synth(cfg, ds, m, seed) is not None:
                    continue
                spec = R.methods.get(m)
                if spec.long and _needs_other_env(spec.long, R.long_generators):
                    continue
                if spec.pool and not _pool_done(cfg, A, ds, spec.pool, seed) \
                        and _needs_other_env(spec.pool, R.pool_generators):
                    continue
                todo.append((ds, m, seed))
    with bar(todo, desc="generate", unit="series") as it:
        for ds, m, seed in it:
            it.set_postfix_str(f"{ds} {m} seed{seed}")
            try:
                save_synth(cfg, ds, m, seed, generate(m, P[ds], seed, cfg))
            except Exception as e:                      # one failing method must not stop the run
                _err(cfg, f"generate {ds} {m} seed{seed}", e)


def _real_pseudo_synth(p, cfg):
    """The real ceiling: the OOT part (shorter than K·T — see the length-matched variants)."""
    v, h = p.part("oot")
    L = p.meta["K"] * p.meta["T"]
    return Synth(v[:L], h[:L], np.array([], int), {})


def _truncated(s, n):
    return Synth(s.values[:n], s.how[:n], s.seams[s.seams < n], {})


def _group_params(cfg: Config) -> dict:
    """Parameters of the fidelity groups (`extra[<group name>]`), the groups that have any."""
    return {g: dict(cfg.extra[g]) for g in R.fidelity_metrics.names() if cfg.extra.get(g)}


def _class_task_params(cfg: Config, ds: str) -> dict:
    """{classification task of the run: its exogenous parameters} for F11 class balance; a task
    without parameters for this dataset is left out (F11 then covers the others)."""
    out = {}
    for t in cfg.tasks or R.tasks.names():
        if R.tasks.get(t).kind in ("clf", "mc"):
            try:
                out[t] = target_params(cfg, ds, t)
            except KeyError:
                continue
    return out


def stage_fidelity(cfg: Config):
    """F-metrics per series, against the primary reference and `cfg.fidelity_extra_refs`. For the
    first seed every method is also scored on its first len(OOT) points (method `<name>@len`): the
    ceiling check (RQ0 b) compares those with `real`."""
    from .progress import bar, log

    R.load_builtins()
    A, P = Artifacts(cfg), _Prepared(cfg)
    units = [(ds, m, seed) for ds in _ready(cfg) for m, seed in
             [(m, s) for s in cfg.seeds for m in cfg.methods]
             + [("real", cfg.seeds[0])] + [(f"{m}@len", cfg.seeds[0]) for m in cfg.methods]]
    from . import cells as CL

    # per metric group: only the groups not done with these settings (marathonts/bench/cells.py)
    want = {(ds, m): CL.fidelity_cells(cfg, m, ds) for ds, m in {(ds, m) for ds, m, _ in units}}
    # reading every unit record from Drive takes minutes: shown as its own bar
    todo = []
    for ds, m, seed in bar(units, desc="fidelity: checking done groups", unit="unit"):
        done = CL.fidelity_done(cfg, A.fidelity(ds, m, seed), m, ds)
        if miss := CL.missing(want[(ds, m)], done):
            todo.append((ds, m, seed, miss, done))
    log(f"fidelity: {len(units) - len(todo)} of {len(units)} units up to date, {len(todo)} with "
        f"{sum(len(t[3]) for t in todo)} metric groups to compute")
    with bar(todo, desc="fidelity", unit="series") as it:
        for ds, m, seed, miss, done in it:
            p = P[ds]
            if m == "real":
                s = _real_pseudo_synth(p, cfg)
            else:
                s = load_synth(cfg, ds, m.removesuffix("@len"), seed)
                if s is not None and m.endswith("@len"):
                    s = _truncated(s, len(_real_pseudo_synth(p, cfg).values))
            if s is None:
                continue
            it.set_postfix_str(f"{ds} {m} seed{seed}")
            ref, ref_how = p.part(cfg.fidelity_ref)
            tr, tr_how = p.part("train")
            # `real` is a piece of OOT: scoring it against OOT would compare it with itself
            extra = {r: p.part(r) for r in cfg.fidelity_extra_refs
                     if r != cfg.fidelity_ref and not (m == "real" and r == "oot")}
            try:
                rec: dict = {}
                errs: list = []
                with timed(rec, "metric"), warnings.catch_warnings():
                    warnings.simplefilter("ignore")       # per-series library warnings would redraw the bars
                    f = fidelity(s.values, s.how, s.seams, ref, ref_how, tr, tr_how, T=p.meta["T"], seed=seed,
                                 disc_epochs=cfg.disc_epochs, edge_overlap=cfg.edge_overlap,
                                 target_task=cfg.stitch_task, groups=miss, params=cfg.params("fidelity"),
                                 target_params=target_params(cfg, ds, cfg.stitch_task), extra_refs=extra,
                                 class_tasks=_class_task_params(cfg, ds), group_params=_group_params(cfg),
                                 errors=errs)
                failed = set()
                for e in errs:                            # the unit is kept; the failing metrics are NaN
                    _err_msg(cfg, f"fidelity {ds} {m} seed{seed} group {e['group']}{e['ref']}", e["error"])
                    if e["failed"]:
                        failed.add(e["group"])
                path = A.fidelity(ds, m, seed)
                old = read_record(path) if check_done(path) else {}
                # the computed groups replace their metrics in the record, the others are kept
                old = {k: v for k, v in old.items() if GROUP_OF.get(k) not in miss}
                f = {**old, **f, "dataset": ds, "method": m, "seed": seed,
                     "metric_wall_s": float(old.get("metric_wall_s") or 0) + rec["metric_wall_s"],
                     "config_fingerprint": cfg.fingerprint(), "unit_fp": None}
                write_record(f, path)
                CL.write_done(CL.fidelity_registry(path),      # last: marks the groups as done
                              {**{g: v for g, v in done.items() if g not in miss},
                               **{g: want[(ds, m)][g] for g in miss if g not in failed}})
            except Exception as e:
                _err(cfg, f"fidelity {ds} {m} seed{seed}", e)


def check_models(cfg: Config) -> None:
    """Warnings about the models and tasks of the run: a model that declares no task kinds (it inherits all
    six), a task no model of the run can fit, a model running on another implementation here (gbdt without
    XGBoost) — its results are not comparable with runs that had it."""
    from .cells import declared
    from .models import BaseModel, backend

    R.load_builtins()
    for mn in cfg.models:
        cls = R.models.get(mn) if mn in R.models else None
        # a custom model (the built-in ones support every kind they inherit) that inherits BaseModel's kinds
        if cls is not None and cls.__module__ != BaseModel.__module__ and cls.kinds is BaseModel.kinds:
            _log(f"   WARNING: model {mn} declares no task kinds (`kinds`): it is tried on every kind")
        if backend(mn) not in (None, "xgboost"):
            _log(f"   WARNING: model {mn} runs on {backend(mn)} here, not XGBoost (BENCH_GBDT_BACKEND, macOS default): "
                 "its results are not comparable with XGBoost runs, and it has no multi-step task")
    for tn in cfg.tasks or R.tasks.names():
        kind = R.tasks.get(tn).kind
        if not any(mn in R.models and kind in declared(mn) and (mn not in cfg.model_tasks or tn in cfg.model_tasks[mn])
                   for mn in cfg.models):
            _log(f"   WARNING: task {tn} ({kind}): no model of the run fits this kind — it has no utility")


def stage_utility(cfg: Config):
    from .progress import bar
    from .utility import ensure_labels

    from . import cells as CL
    from .progress import log

    check_models(cfg)
    A, P = Artifacts(cfg), _Prepared(cfg)
    ready = _ready(cfg)
    for ds in ready:
        ensure_labels(P[ds], cfg, A)
    # per cell (task × model, the decision-transfer grid): only the cells not done with these settings
    units = [(ds, m, seed) for ds in ready for seed in cfg.seeds for m in ["real"] + list(cfg.methods)]
    want = {(ds, m): CL.utility_cells(cfg, m, ds) for ds, m in {(ds, m) for ds, m, _ in units}}
    todo = []
    for ds, m, seed in bar(units, desc="utility: checking done cells", unit="unit"):
        done = CL.utility_done(cfg, A.utility_dir(ds, m, seed), m, ds)
        if miss := CL.missing(want[(ds, m)], done):
            todo.append((ds, m, seed, miss, done))
    log(f"utility: {len(units) - len(todo)} of {len(units)} units up to date, {len(todo)} with "
        f"{sum(len(t[3]) for t in todo)} cells to compute")
    with bar(todo, desc="utility", unit="unit") as it:
        for ds, m, seed, miss, done in it:
            s = None
            if m != "real":
                s = load_synth(cfg, ds, m, seed)
                if s is None:
                    continue
            it.set_postfix_str(f"{ds} {m} seed{seed}")
            try:
                run_utility(P[ds], s, m, seed, cfg, A.utility_dir(ds, m, seed), cells=miss, done=done)
            except Exception as e:
                _err(cfg, f"utility {ds} {m} seed{seed}", e)


def stage_cross_seed(cfg: Config) -> pd.DataFrame:
    """F9.4: diversity between seeds of one method (MMD of windows of seed k vs seed k+1), for the methods of
    the run and the frozen methods whose series are on disk."""
    from .fidelity import _mmd, _windows, _zscore

    rows = []
    for ds in cfg.datasets:
        if not prepared_exists(ds, cfg):
            continue
        p = load_prepared(ds, cfg)
        ref, _ = p.part(cfg.fidelity_ref)
        T = p.meta["T"]
        frozen = [m for m in cfg.frozen_methods if m not in cfg.methods]
        for m in list(cfg.methods) + frozen:
            chk = m not in frozen
            for a, b in zip(cfg.seeds[:-1], cfg.seeds[1:]):
                sa, sb = load_synth(cfg, ds, m, a, chk), load_synth(cfg, ds, m, b, chk)
                if sa is None or sb is None:
                    continue
                rng = np.random.default_rng(a)
                Wa = _windows(_zscore(sa.values, ref), T, rng=rng)
                Wb = _windows(_zscore(sb.values, ref), T, rng=rng)
                rows.append({"dataset": ds, "method": m, "seed": a, "seed_b": b,
                             "F9.4_between_seed_mmd": _mmd(Wa[:, ::4], Wb[:, ::4], rng)})
    return pd.DataFrame(rows)


def _gather(paths) -> pd.DataFrame:
    frames = [read_table(f) for f in paths]
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


FROZEN = "<frozen>"                                   # fp_of(...) of a frozen method: rows kept as they are


def _carry_frozen(df: pd.DataFrame, old: Path, frozen: set, key: str = "method") -> pd.DataFrame:
    """Rows of the frozen methods (`Config.frozen_methods`) that have no unit files here are taken from the
    table already in `tables/`, so results published without their code are kept by every `collect`."""
    if not frozen or not old.exists():
        return df
    prev = pd.read_parquet(old)
    if key not in prev:
        return df
    base = prev[key].astype(str).str.removesuffix("@len")
    have = set(df[key].astype(str).str.removesuffix("@len")) if len(df) and key in df else set()
    add = prev[base.isin(frozen - have)]
    return pd.concat([df, add], ignore_index=True) if len(add) else df


def _check_frozen(df: pd.DataFrame, what: str, cfg: Config, ref: dict | None, now: dict) -> pd.DataFrame:
    """Rows of the frozen methods only where they match the settings of their published results: dataset and
    seed in this run and the fingerprints this run gives them (`cells.frozen_reference`, `now`) equal to those
    written with the results (`tables/frozen.json`, `ref`) — per cell in utility, per metric group in fidelity
    (the other groups NaN), the series stand-in elsewhere. A run with other data, seeds, tasks, models or
    settings therefore never mixes the published numbers with its own; what is dropped is logged as a warning.
    Without a reference (`ref` None) the rows are kept as they are."""
    from . import cells as CL

    if not len(df) or "method" not in df:
        return df
    base = df["method"].astype(str).str.removesuffix("@len")
    fr = base.isin(cfg.frozen_methods)
    if not fr.any():
        return df
    df = df.copy()
    ok = df["dataset"].astype(str).isin(cfg.datasets)
    for c in ("seed", "seed_b"):                      # seed_b: the second seed of a cross_seed pair
        if c in df:
            ok &= df[c].isin(cfg.seeds)
    keep = ~fr | ok
    cols: dict = {}
    if what == "fidelity":
        for c in df.columns:
            if c in GROUP_OF:
                cols.setdefault(GROUP_OF[c], []).append(c)
    n_stale = 0
    for i in df.index[fr & keep] if ref is not None else []:
        m, ds = str(df.at[i, "method"]), str(df.at[i, "dataset"])
        r, n = ref.get(m.removesuffix("@len"), {}).get(ds), now[m.removesuffix("@len")][ds]
        if r is None:
            keep[i] = False
        elif what == "utility":
            k = CL.cell_key(str(df.at[i, "task"]), str(df.at[i, "model"]), df.at[i, "task_kind"] if "task_kind" in df else None)
            keep[i] = k in n["utility"] and r["utility"].get(k) == n["utility"][k]
        elif what == "fidelity":
            rf, nf = r["fidelity"].get(m, {}), n["fidelity"].get(m, {})
            fresh = {g for g, v in nf.items() if rf.get(g) == v}
            stale = [c for g, cs in cols.items() if g not in fresh for c in cs]
            keep[i] = bool(fresh)
            if fresh and stale:
                df.loc[i, stale] = np.nan
                n_stale += 1
        else:
            keep[i] = r["series"] == n["series"]
    if (~keep).any() or n_stale:
        part = f" (and metric groups of {n_stale} more)" if n_stale else ""
        _log(f"   WARNING: {what}: {int((~keep).sum())} rows of the results published without code "
             f"({', '.join(sorted(set(base[fr & ~keep])))}) left out{part}: their dataset, seed or settings differ "
             f"from those of the results (tables/{CL.FROZEN_REF}); the published tables bring them back")
    return df[keep].reset_index(drop=True)


def _fresh(df: pd.DataFrame, what: str, key: str, fp_of, by_dataset: bool = False) -> pd.DataFrame:
    """Rows made with the current settings: `unit_fp` equals `fp_of(<key value>)` — or, `by_dataset`,
    `fp_of(<key value>, <dataset>)` (None: not in this run). Files made with other settings (a stale unit that
    could not be redone here, a method not in the config) are dropped, with a log line."""
    if not len(df) or "unit_fp" not in df or key not in df:
        return df
    # keys as tuples: pandas drops a "\x00" separator when it adds string columns
    if by_dataset and "dataset" in df:
        k = list(zip(df[key].astype(str), df["dataset"].astype(str)))
    else:
        k = [(u,) for u in df[key].astype(str)]
    want = {u: fp_of(*u) for u in set(k)}
    w = pd.Series([want[u] for u in k], index=df.index, dtype=object)
    keep = (df["unit_fp"].astype(str) == w) | w.eq(FROZEN)
    if (~keep).any():
        _log(f"   {what}: dropped {int((~keep).sum())} stale rows (other settings or methods): "
             f"{df.loc[~keep, key].astype(str).value_counts().head(8).to_dict()}")
    return df[keep].reset_index(drop=True)


def _fresh_utility(df: pd.DataFrame, cfg: Config, A, frozen: set) -> pd.DataFrame:
    """Utility rows of the cells done with the current settings (marathonts/bench/cells.py); rows of the frozen methods
    as they are; units of methods not in the run dropped."""
    from . import cells as CL

    if not len(df):
        return df
    keep = pd.Series(False, index=df.index)
    for (ds, m, seed), g in df.groupby(["dataset", "method", "seed"]):
        if m in frozen:
            keep[g.index] = True
            continue
        if m != "real" and m not in cfg.methods:
            continue
        want = CL.utility_cells(cfg, m, ds)
        done = CL.utility_done(cfg, A.utility_dir(ds, m, seed), m, ds)
        fresh = {k for k, fp in want.items() if done.get(k) == fp}
        kind = g["task_kind"] if "task_kind" in g else pd.Series("", index=g.index)
        keep[g.index] = [CL.cell_key(t, mo, k) in fresh for t, mo, k in zip(g["task"].astype(str), g["model"].astype(str), kind)]
    if (~keep).any():
        _log(f"   utility: dropped {int((~keep).sum())} stale rows (other settings, models, tasks or methods): "
             f"{df.loc[~keep, 'method'].astype(str).value_counts().head(8).to_dict()}")
    return df[keep].reset_index(drop=True)


def _fresh_fidelity(df: pd.DataFrame, cfg: Config, A, frozen: set) -> pd.DataFrame:
    """Fidelity records with the metrics of the groups done with the current settings (the others NaN); a
    record without any such group dropped; the frozen methods as they are (marathonts/bench/cells.py)."""
    from . import cells as CL

    if not len(df):
        return df
    cols = {}
    for c in df.columns:
        if c in GROUP_OF:
            cols.setdefault(GROUP_OF[c], []).append(c)
    df = df.copy()
    keep, n_stale = [], 0
    for i, r in zip(df.index, df[["dataset", "method", "seed"]].itertuples(index=False)):
        ds, m, seed = r
        base = str(m).removesuffix("@len")
        if base in frozen:
            keep.append(True)
            continue
        if base != "real" and base not in cfg.methods:
            keep.append(False)
            continue
        want = CL.fidelity_cells(cfg, m, ds)
        done = CL.fidelity_done(cfg, A.fidelity(ds, m, int(seed)), m, ds)
        fresh = {g for g, v in want.items() if done.get(g) == v}
        keep.append(bool(fresh))
        stale = [c for g, cs in cols.items() if g not in fresh for c in cs]
        if fresh and stale:
            df.loc[i, stale] = np.nan
            n_stale += 1
    keep = pd.Series(keep, index=df.index)
    if (~keep).any() or n_stale:
        _log(f"   fidelity: dropped {int((~keep).sum())} stale records, {n_stale} records with stale metric groups")
    return df[keep].reset_index(drop=True)


def stage_collect(cfg: Config):
    """Merge per-unit files into `artifacts/tables/` (Parquet): timing (run records), fidelity,
    utility, pools, cross_seed, datasets and inventory (every artifact file with its size). Only
    units made with the current settings and methods enter the tables (`unit_fp`; utility and fidelity per
    cell, marathonts/bench/cells.py); the frozen methods (`Config.frozen_methods`) enter as they are — from their unit
    files or, without them, from the table already in `tables/`."""
    from . import cells as CL

    R.load_builtins()
    A = Artifacts(cfg)
    t, root = A.tables, A.root
    methods, frozen = set(cfg.methods), set(cfg.frozen_methods)

    ref = json.loads((t / CL.FROZEN_REF).read_text()) if (t / CL.FROZEN_REF).exists() else None
    now = CL.frozen_reference(cfg) if frozen else {}
    if frozen and ref is None:
        _log(f"   WARNING: no tables/{CL.FROZEN_REF}: the rows of {sorted(frozen)} are taken without a settings check")

    def chk(df, what):
        return _check_frozen(df, what, cfg, ref, now)

    def fp(fn, m, ds, extra=()):
        base = m.removesuffix("@len")
        return FROZEN if base in frozen else fn(cfg, m, ds) if base in methods | set(extra) else None

    timing = _gather(sorted((root / "records").glob("*/*/seed*.parquet")))
    timing = chk(_carry_frozen(_fresh(timing, "timing", "method", lambda m, ds: fp(series_fp, m, ds), True), t / "timing.parquet", frozen), "timing")
    write_table(timing, t / "timing.parquet")
    if "gpu" in timing and timing["gpu"].nunique() > 1:
        _log(f"   WARNING: series made with {timing['gpu'].nunique()} different GPU types: "
             f"{timing['gpu'].value_counts().to_dict()}")
    fid = _gather(sorted((root / "fidelity").glob("*/*/seed*.parquet")))
    fid = _fresh_fidelity(fid, cfg, A, frozen)
    fid = chk(_carry_frozen(fid, t / "fidelity.parquet", frozen), "fidelity")
    write_table(fid, t / "fidelity.parquet")
    ut = _gather(sorted((root / "utility").glob("*/*/seed*/metrics.parquet")))
    ut = chk(_carry_frozen(_fresh_utility(ut, cfg, A, frozen), t / "utility.parquet", frozen), "utility")
    if "params" in ut:
        be = ut["params"].astype(str).str.extract(r'"_backend": "(\w+)"')[0]
        if be.notna().any():
            _log(f"   WARNING: utility rows made with another implementation than XGBoost: "
                 f"{ut.loc[be.notna(), 'model'].value_counts().to_dict()} ({be.dropna().value_counts().to_dict()})")
    write_table(ut, t / "utility.parquet")
    gens = set(_pool_generators(cfg))
    pools = []
    for f in sorted((root / "pools").glob("*/*/seed*.record.parquet")):
        r = read_record(f)
        r.update(dataset=f.parts[-3], pool_generator=f.parts[-2], seed=int(f.name.split(".")[0][4:]))
        pools.append(r)
    pools = _fresh(pd.DataFrame(pools), "pools", "pool_generator", lambda g, ds: pool_fp(cfg, g, ds) if g in gens else None,
                   by_dataset=True)
    write_table(pools, t / "pools.parquet")
    write_table(chk(_carry_frozen(stage_cross_seed(cfg), t / "cross_seed.parquet", frozen), "cross_seed"), t / "cross_seed.parquet")
    from .data import window_layout

    meta = []
    for ds in cfg.datasets:
        if prepared_exists(ds, cfg):
            m = read_record(cfg.processed_dir / f"{ds}.meta.parquet")
            meta.append({**m, **window_layout(m, cfg)})          # N, s, core / holdout bounds of this run
    write_table(pd.DataFrame(meta), t / "datasets.parquet", keep64=["lo", "hi"])
    inv = [{"path": str(f.relative_to(root)), "kind": f.relative_to(root).parts[0], "bytes": f.stat().st_size}
           for f in root.rglob("*.parquet") if "tables" not in f.relative_to(root).parts]
    write_table(pd.DataFrame(inv), t / "inventory.parquet")
    # paths inside the project are saved relative to it: the file names no machine-specific folder
    saved = json.loads(cfg.to_json())
    for k, v in saved.items():
        if k.endswith(("_dir", "_file")) and isinstance(v, str) and Path(v).is_absolute():
            for cand in (Path(v), Path(v).resolve()):          # as given first: a symlinked data folder stays relative
                try:
                    saved[k] = cand.relative_to(ROOT).as_posix()
                    break
                except ValueError:
                    continue
    (t / "config.json").write_text(json.dumps(saved, indent=2))
    write_record(hardware(), t / "hardware.parquet")
    from .data import DESCRIPTOR_TABLE, descriptors

    if all(prepared_exists(ds, cfg) for ds in cfg.datasets):
        write_table(descriptors(cfg), t / DESCRIPTOR_TABLE)
    _log(f"tables → {t}")


def stage_targets(cfg: Config):
    """Propose the exogenous target parameters still missing from `cfg.target_params_file` (the
    task's rule on train) and write them. Not part of `all`: run once, review, commit the file."""
    from .tasks import freeze_target_params

    added = freeze_target_params(cfg, cfg.datasets, cfg.tasks)
    _log(f"target parameters added to {cfg.target_params_file}: "
         f"{sum(len(v) for v in added.values())} (dataset, task) pairs" if added else "nothing to add")


def stage_freeze(cfg: Config):
    """Write `tables/frozen.json`: the fingerprints of the cells of the frozen methods (`Config.frozen_methods`)
    under these settings (`cells.frozen_reference`). Not part of `all`: run once with the settings of their
    published results, commit the file; `collect` then keeps their rows only where a run has the same settings."""
    from .cells import FROZEN_REF, frozen_reference

    f = Artifacts(cfg).tables / FROZEN_REF
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps(frozen_reference(cfg), indent=1, sort_keys=True))
    _log(f"settings of the frozen results ({', '.join(cfg.frozen_methods) or 'none'}) → {f}")


def stage_hashes(cfg: Config):
    """Record the content hashes of the prepared datasets still missing from `marathonts/bench/data_hashes.json`
    for these data settings. Not part of `all`: run once after `prepare` of a run that will be published,
    commit the file; `prepare` and loading then warn if the data differ."""
    added = record_data_hashes(cfg, cfg.datasets)
    _log(f"data hashes added to {DATA_HASHES_FILE}: {', '.join(added)}" if added else "nothing to add")


STAGES = {"raw": stage_raw, "prepare": stage_prepare, "targets": stage_targets, "hashes": stage_hashes, "freeze": stage_freeze,
          "pools": stage_pools,
          "generate": stage_generate,
          "fidelity": stage_fidelity, "utility": stage_utility, "collect": stage_collect}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=list(STAGES) + ["all"])
    ap.add_argument("--profile", choices=["min", "mid", "max"], default="min",
                    help="min: the Colab run (default); mid: min + the VAE per seed and the noise twin; max: everything on (BENCHMARK.md)")
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--datasets", nargs="*")
    ap.add_argument("--methods", nargs="*")
    ap.add_argument("--models", nargs="*")
    ap.add_argument("--pool-generators", nargs="*", help="stage pools: which pool generators (default: from methods)")
    ap.add_argument("--seeds", nargs="*", type=int)
    ap.add_argument("--artifacts-dir")
    ap.add_argument("--device")
    ap.add_argument("--diffusion-ts-dir")
    ap.add_argument("--plugins", nargs="*", help="Python files registering custom components (or Config.plugins)")
    ap.add_argument("--config", help="JSON written by Config.to_json() (e.g. handed over from a notebook)")
    a = ap.parse_args(argv)
    load_plugins(a.plugins)
    if a.config:
        cfg = Config.from_json(Path(a.config).read_text())
    else:
        cfg = Config.quick() if a.quick else Config.profile(a.profile)
    over = {k: v for k, v in dict(datasets=a.datasets, methods=a.methods, models=a.models, seeds=a.seeds,
                                  device=a.device, pool_generators=a.pool_generators).items() if v}
    if a.plugins:                                    # recorded: collect's config.json names them for the hypothesis part
        over["plugins"] = list(dict.fromkeys([*cfg.plugins, *a.plugins]))
    if a.artifacts_dir:
        over["artifacts_dir"] = Path(a.artifacts_dir)
    if a.diffusion_ts_dir:
        over["diffusion_ts_dir"] = Path(a.diffusion_ts_dir)
    cfg = dataclasses.replace(cfg, **over)
    for name in ([s for s in STAGES if s not in ("targets", "hashes", "freeze")] if a.stage == "all" else [a.stage]):
        _log(f"── stage {name}")
        STAGES[name](cfg)


if __name__ == "__main__":
    main()
