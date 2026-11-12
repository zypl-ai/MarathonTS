"""Utility tasks (METRICS U2) and custom targets.

A task turns one real-unit series into labels: `fit(train_values) -> params` (thresholds etc.,
computed on train only) and `labels(values, params) -> y` ((L,) or (L, k); NaN where the future
is unknown). Features and labels are computed on each series separately (BENCHMARK.md, Protocol: utility).

`kind` decides the models' loss and the utility metrics:
clf (binary) | mc (multiclass, labels 0..n_classes−1) | reg | qreg (quantiles) | ms (vector) | vol.

Custom target:

    from marathonts.bench.tasks import Task, register_task
    register_task(Task("spike_h12", "clf", h=12,
                       fit=lambda v: {"thr": np.nanquantile(np.diff(v), 0.95)},
                       labels=lambda v, p: my_labels(v, p["thr"])))
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from pathlib import Path

import numpy as np
import pandas as pd

from . import registry as R

LAGS = (1, 2, 3, 6, 12, 24, 48, 168)
HIST = max(LAGS)
QUANTILES = (0.1, 0.5, 0.9)


@dataclass(frozen=True)
class Task:
    name: str
    kind: str                                       # clf | mc | reg | qreg | ms | vol
    h: int
    fit: Callable[[np.ndarray], dict] = lambda v: {}
    labels: Callable[[np.ndarray, dict], np.ndarray] | None = None
    n_classes: int = 2
    metrics_id: str = ""
    q: float | None = None
    direction: str = ""
    description: str = ""
    # hyperparameter search criterion (metric, higher is better); None → by kind (`utility.SELECT_BY`)
    select_by: tuple[str, bool] | None = None
    # row-level loss for the case study's paired tests, `row_loss(y, pred, scale) -> (n,)`: needed by a kind
    # other than the built-in ones (`utility.row_score`)
    row_loss: Callable | None = None


def register_task(task: Task, overwrite: bool = False) -> Task:
    return R.tasks.register(task.name, task, overwrite=overwrite)


def _diff_ahead(v: np.ndarray, h: int) -> np.ndarray:
    d = np.full(len(v), np.nan)
    d[:-h] = v[h:] - v[:-h]
    return d


# ─────────────────────── builders of the built-in tasks ────────────────────
def tail_task(name, h, q, direction="up", metrics_id=""):
    def fit(v):
        return {"thr": float(np.nanquantile(_diff_ahead(v, h), q))}

    def lab(v, p):
        d = _diff_ahead(np.asarray(v, float), h)
        y = (d > p["thr"]) if direction == "up" else (d < p["thr"])
        return np.where(np.isnan(d), np.nan, y.astype(float))

    return Task(name, "clf", h, fit, lab, 2, metrics_id, q, direction,
                f"change over {h} h {'above' if direction == 'up' else 'below'} the train {q:.2f}-quantile")


def mc3_task(name, h, metrics_id=""):
    def fit(v):
        d = _diff_ahead(v, h)
        return {"lo": float(np.nanquantile(d, 0.10)), "hi": float(np.nanquantile(d, 0.90))}

    def lab(v, p):
        d = _diff_ahead(np.asarray(v, float), h)
        y = np.where(d < p["lo"], 0.0, np.where(d > p["hi"], 2.0, 1.0))
        return np.where(np.isnan(d), np.nan, y)

    return Task(name, "mc", h, fit, lab, 3, metrics_id, description=f"down / flat / up over {h} h")


def level_task(name, h, kind="reg", metrics_id=""):
    def lab(v, p):
        y = np.full(len(v), np.nan)
        y[:-h] = np.asarray(v, float)[h:]
        return y

    return Task(name, kind, h, labels=lab, metrics_id=metrics_id, description=f"value at t+{h}")


def path_task(name, h, metrics_id=""):
    def lab(v, p):
        v = np.asarray(v, float)
        Y = np.full((len(v), h), np.nan)
        for k in range(1, h + 1):
            Y[:-k, k - 1] = v[k:]
        return Y

    return Task(name, "ms", h, labels=lab, metrics_id=metrics_id, description=f"values t+1..t+{h}")


def vol_task(name, h, metrics_id=""):
    def lab(v, p):
        dv = np.diff(np.asarray(v, float), prepend=np.nan)
        return pd.Series(dv).rolling(h).std().shift(-h).to_numpy()

    return Task(name, "vol", h, labels=lab, metrics_id=metrics_id, description=f"std of changes over next {h} h")


for _t in [
    tail_task("clf_up_h24_q90", 24, 0.90, "up", "U2.1"),
    tail_task("clf_up_h1_q90", 1, 0.90, "up", "U2.2"),
    tail_task("clf_up_h6_q90", 6, 0.90, "up", "U2.2"),
    tail_task("clf_up_h168_q90", 168, 0.90, "up", "U2.2"),
    tail_task("clf_up_h24_q95", 24, 0.95, "up", "U2.3"),
    tail_task("clf_up_h24_q99", 24, 0.99, "up", "U2.3"),
    tail_task("clf_down_h24_q10", 24, 0.10, "down", "U2.4"),
    mc3_task("mc3_h24", 24, "U2.5"),
    level_task("reg_h1", 1, "reg", "U2.6"),
    level_task("reg_h24", 24, "reg", "U2.6"),
    level_task("reg_h168", 168, "reg", "U2.6"),
    level_task("qreg_h24", 24, "qreg", "U2.7"),
    path_task("ms_h24", 24, "U2.8"),
    vol_task("vol_h24", 24, "U2.9"),
]:
    register_task(_t)

TASKS = R.tasks                                     # name → Task (registry; custom tasks included)


def get(name: str) -> Task:
    return R.tasks.get(name)


def thresholds(task: Task, train_values: np.ndarray) -> dict:
    """The task's own rule for its parameters (`Task.fit`) — used ONLY by `freeze_target_params`
    to propose values once; the benchmark reads the frozen values (`target_params`)."""
    return task.fit(np.asarray(train_values, float))


# ─────────────────────── exogenous target parameters ───────────────────────
def _load_params(cfg) -> dict:
    import json

    f = cfg.target_params_file
    return json.loads(f.read_text()) if f.exists() else {}


def target_params(cfg, dataset: str, task: Task | str) -> dict:
    """Exogenous parameters of a task on a dataset (thresholds in real units), read from
    `cfg.target_params_file`. They are fixed in advance — never fitted during a run. Tasks
    without parameters (regression, multi-step, volatility) return {}."""
    task = R.tasks.get(task) if isinstance(task, str) else task
    allp = _load_params(cfg)
    made_on = allp.get("_split_key", {}).get(dataset)
    if made_on is not None and made_on != cfg.split_key(dataset):
        raise RuntimeError(f"{cfg.target_params_file}: thresholds of '{dataset}' were set on another split "
                           f"(other max_points / split / embargo) — they could come from this run's val / OOT. "
                           f"Use the file of this profile, or propose new ones with `python -m marathonts.bench.run targets`.")
    params = allp.get(dataset, {}).get(task.name)
    if params is not None:
        return dict(params)
    if task.fit(np.zeros(400)) == {}:                 # parameter-free task
        return {}
    raise KeyError(f"no exogenous parameters for task '{task.name}' on dataset '{dataset}' in "
                   f"{cfg.target_params_file}. Add them there, or propose them once from train with "
                   f"`python -m marathonts.bench.run targets` (then review and commit the file).")


def missing_target_params(cfg, dataset: str, tasks=None) -> list[str]:
    """Tasks of the run that need exogenous parameters and have none for `dataset` in the file."""
    R.load_builtins()
    have = _load_params(cfg).get(dataset, {})
    return [tn for tn in (tasks or R.tasks.names())
            if tn not in have and R.tasks.get(tn).fit(np.zeros(400)) != {}]


def freeze_target_params(cfg, datasets, tasks=None, overwrite: bool = False) -> dict:
    """Propose the parameters of every (dataset, task) still missing from the file with the task's
    rule on the current train split, and write them to the file. Run once, review, commit."""
    import json

    from .data import load_prepared

    R.load_builtins()
    allp = _load_params(cfg)
    added = {}
    for ds in datasets:
        p = load_prepared(ds, cfg)
        v_tr, _ = p.part("train")
        made_on = allp.get("_split_key", {}).get(ds)
        if made_on is not None and made_on != cfg.split_key(ds) and not overwrite:
            raise RuntimeError(f"{cfg.target_params_file}: the thresholds of '{ds}' were set on another split; "
                               f"adding new ones on this split would mix the two (use the file of this profile)")
        allp.setdefault("_split_key", {})[ds] = cfg.split_key(ds)     # which split the thresholds come from
        for tn in tasks or R.tasks.names():
            task = R.tasks.get(tn)
            if not overwrite and tn in allp.get(ds, {}):
                continue
            prm = {k: float(round(v, 10)) for k, v in thresholds(task, v_tr).items()}
            if prm:
                allp.setdefault(ds, {})[tn] = prm
                added.setdefault(ds, {})[tn] = prm
    f = Path(cfg.target_params_file)
    tmp = f.with_name("." + f.name + ".tmp")                       # atomic: every stage reads this file
    tmp.write_text(json.dumps(allp, indent=2, sort_keys=True) + "\n")
    tmp.replace(f)
    return added


def labels(task: Task, v: np.ndarray, params: dict) -> np.ndarray:
    return task.labels(np.asarray(v, float), params)


def features(v: np.ndarray, how: np.ndarray) -> np.ndarray:
    """Lags/differences of the series and calendar (BENCHMARK.md, Protocol: utility)."""
    s = pd.Series(np.asarray(v, float))
    cols = {"v": s}
    for l in LAGS:
        cols[f"d{l}"] = s - s.shift(l)
    a = 2 * np.pi * np.asarray(how) / 168
    cols["sin"], cols["cos"] = np.sin(a), np.cos(a)
    return pd.DataFrame(cols).to_numpy(np.float32)


def make_xy(v, how, task: Task, params: dict):
    """X, y and the row positions (in the input series) that are usable."""
    X = features(v, how)
    y = labels(task, v, params)
    ok = np.isfinite(X).all(axis=1) & (np.isfinite(y).all(axis=1) if y.ndim == 2 else np.isfinite(y))
    rows = np.flatnonzero(ok)
    return X[ok], y[ok], rows


def seasonal_naive_scale(v_train: np.ndarray, h: int = 168) -> float:
    """MASE denominator: MAE of the seasonal (168) naive forecast on train."""
    v = np.asarray(v_train, float)
    e = np.abs(v[168:] - v[:-168])
    return float(np.nanmean(e)) if np.isfinite(e).any() else 1.0
