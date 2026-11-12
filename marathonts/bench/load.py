"""Load anything back from the artifacts: generators and downstream models with their weights
(ready to `sample` / `generate` / `predict`), pools, series, predictions, metrics.

    from marathonts.bench.config import Config
    from marathonts.bench import load
    cfg = Config()
    gen = load.load_generator(cfg, "ett", "tsgm_vae", seed=0)          # fitted VAE, no training
    windows = gen.sample(100, load.gen_context(cfg, "ett", "tsgm_vae", 0))
    m = load.load_model(cfg, "ett", "vae_zseries", 0, task="clf_up_h24_q90", model="linear", regime="S")
    X, y, _ = load.task_xy(cfg, "ett", "clf_up_h24_q90", split="oot")
    p = m.predict(X)
"""
from __future__ import annotations

import json

import numpy as np
import pandas as pd

from . import registry as R
from .config import Config
from .data import load_prepared
from .generators.base import GenContext
from .methods import Artifacts, load_synth
from .storage import read_arrays, read_record, read_table
from .tasks import make_xy, target_params


def gen_context(cfg: Config, ds: str, name: str, seed: int) -> GenContext:
    return GenContext(load_prepared(ds, cfg), cfg, seed, name, cfg.device_str())


def load_generator(cfg: Config, ds: str, gen: str, seed: int):
    """A fitted pool or long generator restored from the artifacts — the weights this config uses
    for the seed: a pool generator's own (`seed<k>`) or shared replica (`replica<r>`), Diffusion-TS
    per seed or the one model per dataset (`seedshared`). Weights made with other training settings
    (record `unit_fp`) are refused."""
    R.load_builtins()
    from .methods import dts_replica, dts_shared, is_fresh, train_fp, train_replica

    ctx = gen_context(cfg, ds, gen, seed)
    A = Artifacts(cfg)
    if gen in R.pool_generators:
        cls = R.pool_generators.get(gen)
        rep = train_replica(cfg, seed)
        path = A.generator_weights(ds, gen, seed) if rep is None else A.generator_replica(ds, gen, rep)
        fp = train_fp(cfg, gen, ds)
    else:
        cls = R.long_generators.get(gen)
        shared = gen == "diffusion_ts" and not cfg.dts_train_per_seed
        path, fp = dts_shared(cfg, ds, dts_replica(cfg, seed)) if shared else (A.generator_weights(ds, gen, seed), None)
    rec = path.with_name(path.name.replace(".parquet", ".record.parquet"))
    if fp is not None and rec.exists() and not is_fresh(rec, fp):
        raise RuntimeError(f"{path}: trained with other settings than this config — run the pipeline first")
    if not path.exists() and gen in R.pool_generators:
        raise FileNotFoundError(f"{path}: no weights (not trained yet, or save_generator_weights=False)")
    arrays = read_arrays(path) if path.exists() else {}
    return cls().load_state(arrays, ctx)


def model_keys(cfg: Config, ds: str, method: str, seed: int) -> pd.DataFrame:
    """Which fitted models are stored for a unit: task, model, regime."""
    path = Artifacts(cfg).utility_dir(ds, method, seed) / "models.parquet"
    names = pd.read_parquet(path, columns=["name"])["name"]
    parts = names.str.split("|", n=3, expand=True)
    return parts.iloc[:, :3].drop_duplicates().set_axis(["task", "model", "regime"], axis=1).reset_index(drop=True)


def load_model(cfg: Config, ds: str, method: str, seed: int, task: str, model: str, regime: str):
    """A fitted downstream model restored from `artifacts/utility/.../models.parquet`."""
    R.load_builtins()
    path = Artifacts(cfg).utility_dir(ds, method, seed) / "models.parquet"
    prefix = f"{task}|{model}|{regime}|"
    df = pd.read_parquet(path, filters=[("name", ">=", prefix), ("name", "<", prefix + "￿")])
    arrays = {r.name[len(prefix):]: np.frombuffer(r.data, dtype=np.dtype(r.dtype)).reshape(json.loads(r.shape)).copy()
              for r in df.itertuples()}
    if not arrays:
        raise KeyError(f"no weights for {prefix} in {path}")
    from .models import model_params

    m = R.models.get(model)(R.tasks.get(task), seed, cfg.device_str(), model_params(cfg, model), cfg)
    return m.load_state(arrays)


def task_xy(cfg: Config, ds: str, task: str, split: str = "oot"):
    """Real features / labels of a split for a task (thresholds from train) — to feed loaded models."""
    R.load_builtins()
    p = load_prepared(ds, cfg)
    t = R.tasks.get(task)
    prm = target_params(cfg, ds, t)
    v, h = p.part(split)
    return make_xy(v, h, t, prm)


def load_pool(cfg: Config, ds: str, gen: str, seed: int) -> np.ndarray:
    return read_arrays(Artifacts(cfg).pool(ds, gen, seed))["pool"]


def load_series(cfg: Config, ds: str, method: str, seed: int) -> pd.DataFrame:
    return read_table(Artifacts(cfg).series(ds, method, seed))


def load_record(cfg: Config, ds: str, method: str, seed: int) -> dict:
    return read_record(Artifacts(cfg).record(ds, method, seed))


def load_predictions(cfg: Config, ds: str, method: str, seed: int, with_scores: bool = False) -> pd.DataFrame:
    """Every test prediction of a unit; `with_scores=True` joins the labels and the row-level score
    (losses divided by the seasonal-naive MAE of train, as in metrics.parquet — comparable across
    datasets)."""
    pr = read_table(Artifacts(cfg).utility_dir(ds, method, seed) / "predictions.parquet")
    if not with_scores:
        return pr
    from .tasks import seasonal_naive_scale
    from .utility import load_labels, row_scores

    scale = seasonal_naive_scale(load_prepared(ds, cfg).part("train")[0])
    return row_scores(pr, load_labels(Artifacts(cfg), ds, sorted(pr["task"].astype(str).unique())), scale)


def load_labels(cfg: Config, ds: str, tasks=None) -> pd.DataFrame:
    from .utility import load_labels as _ll

    R.load_builtins()
    return _ll(Artifacts(cfg), ds, tasks or R.tasks.names())


__all__ = ["gen_context", "load_generator", "model_keys", "load_model", "task_xy", "load_pool", "load_series",
           "load_record", "load_predictions", "load_labels", "load_synth"]
