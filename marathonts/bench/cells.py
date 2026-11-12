"""Per-cell fingerprints of the utility and fidelity units.

A utility unit (dataset, method, seed) is made of cells — one per task × model (`<task>|<model>`) and the
decision-transfer grid (`grid`) — and a fidelity unit of one cell per metric group. Each cell has its own
fingerprint: what that cell depends on (the series, the labels, that model's configuration; that group's
settings and parameters, the thresholds only for the groups that read them). The cells a unit has done are
listed in a registry next to it (`cells.json` in a utility unit, `seed<k>.cells.json` next to a fidelity
record), written last. An added model, task or metric group therefore computes only its own cells, and a
changed model or group redoes only its own; a cell that failed is not listed and is retried on the next run.
A unit without a registry has no done cells.

The methods published without code (`Config.frozen_methods`) have no series fingerprint here: their cells are
hashed with a stand-in (`frozen_series_fp`) and checked against the reference written with their results
(`frozen_reference`, `tables/frozen.json`).
"""
from __future__ import annotations

import json
from pathlib import Path


from . import registry as R
from .config import Config

FROZEN_REF = "frozen.json"                      # in tables/: the cell fingerprints of the published frozen results
GRID = "grid"                                   # the decision-transfer cell (U6.1 / U6.4, RQ5 c)
# fidelity groups that read the task thresholds of their dataset (F8: the case-study task, F11: every
# classification task of the run) and the list of tasks (F11); the other groups depend on neither
USES_TARGETS = {"F8_target", "F11_class_balance"}
USES_TASKS = {"F11_class_balance"}


def read_done(path: Path) -> dict | None:
    """The registry of done cells {cell: fingerprint}, or None without one (or unreadable)."""
    try:
        return json.loads(Path(path).read_text()) if Path(path).exists() else None
    except ValueError:
        return None


def write_done(path: Path, cells: dict) -> None:
    path = Path(path)
    tmp = path.with_name(f".{path.name}.tmp")
    tmp.write_text(json.dumps(cells, indent=1, sort_keys=True))
    tmp.replace(path)


def cell_key(task: str, model: str, task_kind: str | None = None) -> str:
    return GRID if task_kind in ("grid", "threshold") else f"{task}|{model}"


def _series_fp(cfg: Config, method: str, ds: str) -> str:
    from .methods import series_fp

    return frozen_series_fp(cfg, method, ds) if method in cfg.frozen_methods else series_fp(cfg, method, ds)


# ─────────────────────── utility ───────────────────────────────────────────
def declared(model: str) -> set:
    """Task kinds a model is defined for, whatever this environment can run (`all_kinds`, e.g. gbdt with
    XGBoost): the expected cells do not depend on the environment."""
    cls = R.models.get(model)
    return set(getattr(cls, "all_kinds", None) or cls.kinds)


def utility_cells(cfg: Config, method: str, ds: str) -> dict[str, str]:
    """{cell: fingerprint} of every cell the utility unit of (`ds`, `method`) has under `cfg`."""
    from .models import model_grid, model_params
    from .utility import _grid_methods, labels_fp

    R.load_builtins()
    base = {"series": _series_fp(cfg, method, ds), "labels": labels_fp(cfg, ds), "splits": list(cfg.test_splits),
            "hpo": [cfg.hpo, cfg.hpo_val_frac], "weights": [cfg.save_model_weights, cfg.weights_dtype]}
    out = {}
    for tn in cfg.tasks or R.tasks.names():
        kind = R.tasks.get(tn).kind
        for mn in cfg.models:
            if mn not in R.models or kind not in declared(mn) or (mn in cfg.model_tasks and tn not in cfg.model_tasks[mn]):
                continue
            out[cell_key(tn, mn)] = cfg._hash({**base, "task": tn, "model": mn, "params": model_params(cfg, mn),
                                               "grid": model_grid(cfg, mn) if cfg.hpo else None})
    if cfg.decision_transfer and method != "real" and method in _grid_methods(cfg):
        clf = [mn for mn in cfg.models if mn in R.models and "clf" in R.models.get(mn).kinds]
        out[GRID] = cfg._hash({**base, "grid_task": cfg.model_grid_task,
                               "models": {mn: [model_params(cfg, mn), model_grid(cfg, mn)] for mn in clf}})
    return out


def utility_done(cfg: Config, unit_dir: Path, method: str, ds: str) -> dict:
    """{cell: fingerprint it was made with} of a utility unit: its registry (`cells.json`); {} without one."""
    return read_done(Path(unit_dir) / "cells.json") or {}


# ─────────────────────── fidelity ──────────────────────────────────────────
def _thresholds(cfg: Config, ds: str):
    """The thresholds of `ds` in the thresholds file and the split they were made on."""
    f = Path(cfg.target_params_file)
    t = json.loads(f.read_text()) if f.exists() else {}
    return [t.get(ds), t.get("_split_key", {}).get(ds)]


def fidelity_cells(cfg: Config, m: str, ds: str) -> dict[str, str]:
    """{metric group: fingerprint} of every group the fidelity unit of (`ds`, `m`; `m` may be `<method>@len` or
    `real`) has under `cfg`."""
    R.load_builtins()
    base = {"series": _series_fp(cfg, m.removesuffix("@len"), ds), "unit": m, "data": cfg.data_key(ds),
            "settings": [cfg.fidelity_ref, list(cfg.fidelity_extra_refs), cfg.disc_epochs, cfg.edge_overlap,
                         cfg.stitch_task], "extra": cfg.extra.get("fidelity")}
    targets = _thresholds(cfg, ds)
    tasks = list(cfg.tasks or R.tasks.names())
    return {g: cfg._hash({**base, "group": g, "params": cfg.extra.get(g),
                          "targets": targets if g in USES_TARGETS else None,
                          "tasks": tasks if g in USES_TASKS else None})
            for g in (cfg.fidelity_groups or R.fidelity_metrics.names())}


def fidelity_registry(record: Path) -> Path:
    record = Path(record)
    return record.with_name(record.name.replace(".parquet", ".cells.json"))


def fidelity_done(cfg: Config, record: Path, m: str, ds: str) -> dict:
    """{group: fingerprint it was made with} of a fidelity unit: its registry (`seed<k>.cells.json`); {} without
    one."""
    return read_done(fidelity_registry(record)) or {}


def missing(want: dict, done: dict) -> list[str]:
    """Cells of `want` not done with the same fingerprint."""
    return [k for k, fp in want.items() if done.get(k) != fp]


# ─────────────────────── frozen methods ────────────────────────────────────
def frozen_series_fp(cfg: Config, method: str, ds: str) -> str:
    """Stand-in for the series fingerprint of a frozen method, whose code (and so its own settings) is not here:
    what its series depends on in the open part — the pool it assembles (generator, data, sampling), the settings
    of its assembler and seam processing that are in `Config`, and the thresholds."""
    from .config import suite_entries
    from .methods import pool_fp

    for pre, gen in cfg.pool_suites.items():
        for sfx, a, j, _ in suite_entries(cfg.extra_assemblers, cfg.extra_joiners, "all", None):
            if f"{pre}_{sfx}" == method:
                return cfg.unit_fingerprint(a, *((j,) if j else ()), upstream=(pool_fp(cfg, gen, ds),),
                                            files=("targets",), dataset=ds)
    return cfg.unit_fingerprint(method, files=("targets",), dataset=ds)       # not a suite method: data and thresholds


def frozen_reference(cfg: Config) -> dict:
    """{method: {dataset: {"series": fp, "utility": {cell: fp}, "fidelity": {unit: {group: fp}}}}} of the frozen
    methods under `cfg`. Written next to their published results (`python -m marathonts.bench.run freeze` → `tables/frozen.json`);
    `collect` compares it with the same under its own settings and keeps only the rows that match."""
    return {m: {ds: {"series": frozen_series_fp(cfg, m, ds), "utility": utility_cells(cfg, m, ds),
                     "fidelity": {u: fidelity_cells(cfg, u, ds) for u in (m, f"{m}@len")}}
                for ds in cfg.datasets}
            for m in cfg.frozen_methods}
