"""Stage 4 — utility (METRICS U1–U6): TSTR against TRTR — how well models trained on the
synthetic series do on real data, compared with the same models trained on real data.

Two regimes (`config.REGIMES`): R — TRTR, train on the real train split; S — TSTR, train only on
the method's synthetic series. Both are tested on the same real val / OOT rows. R does not depend
on the method: it runs once per (dataset, seed) under the pseudo-method `real`.

Per (dataset, method, seed), for every task × model × regime × test split:

* `metrics.parquet` — point metrics (registry `utility_metrics`), fit seconds, sizes;
* `predictions.parquet` — every test prediction: `pred` for scalar outputs, `pred_vec` (a list per
  row) for multiclass, quantile and multi-step outputs; the labels are in `artifacts/labels/<ds>/
  <task>.parquet`, and `row_scores` joins both into the row-level score (P(y = 1) for binary
  tasks, per-row loss otherwise). Always written: the hypothesis part's row-level tests need them;
* `models.parquet` — weights of every fitted model (`<task>|<model>|<regime>|<param>`).

Custom utility metric:

    from marathonts.bench import registry as R
    @R.utility_metrics.register("my_metric")
    def my_metric(y, pred, ctx):            # ctx: dict(kind, scale, train_share, task)
        if ctx["kind"] != "clf": return {}
        return {"my_metric": ...}
"""
from __future__ import annotations

import time
from pathlib import Path

import numpy as np
import pandas as pd

from . import registry as R
from .config import REGIMES
from .models import model_grid, model_params, prior_correct, supports
from .storage import write_arrays, write_table
from .tasks import LAGS, QUANTILES, make_xy, seasonal_naive_scale, target_params


def _grid_methods(cfg) -> set:
    if cfg.grid_methods == "all":
        return set(cfg.methods)
    return set(cfg.grid_methods) if cfg.grid_methods is not None else {cfg.case_method, cfg.noise_pair[0]}


# ─────────────────────── regimes (U1): TRTR and TSTR ───────────────────────
def build_train(regime: str, Xr, yr, Xs, ys):
    """Training set of a regime and the number of synthetic rows in it: R (TRTR) — real train,
    S (TSTR) — the synthetic series only."""
    if regime == "R":
        return Xr, yr, 0
    if regime == "S":
        return Xs, ys, len(Xs)
    raise ValueError(f"unknown regime {regime!r}: {REGIMES}")


# ─────────────────────── metrics (U4), registered ──────────────────────────
def _ece(y, p, bins=10):
    edges = np.linspace(0, 1, bins + 1)
    idx = np.clip(np.digitize(p, edges) - 1, 0, bins - 1)
    return float(sum(abs(y[idx == b].mean() - p[idx == b].mean()) * (idx == b).mean()
                     for b in range(bins) if (idx == b).any()))


@R.utility_metrics.register("binary")
def binary_metrics(y, p, ctx):
    if ctx["kind"] != "clf":
        return {}
    from sklearn.metrics import average_precision_score, brier_score_loss, f1_score, log_loss, roc_auc_score

    out = {"pos_share": float(y.mean())}
    if len(np.unique(y)) < 2:
        return out
    p = np.clip(p, 1e-6, 1 - 1e-6)
    share = ctx["train_share"]
    thr = np.quantile(p, 1 - share) if 0 < share < 1 else 0.5
    top = p >= np.quantile(p, 0.9)
    out.update(auc=roc_auc_score(y, p), pr_auc=average_precision_score(y, p), brier=brier_score_loss(y, p),
               logloss=log_loss(y, p), ece=_ece(y, p), f1=float(f1_score(y, (p >= thr).astype(int), zero_division=0)),
               lift10=float(y[top].mean() / (y.mean() + 1e-12)))
    return out


@R.utility_metrics.register("multiclass")
def multiclass_metrics(y, P, ctx):
    if ctx["kind"] != "mc":
        return {}
    from sklearn.metrics import f1_score, log_loss, roc_auc_score

    C = ctx["task"].n_classes
    P = np.clip(P, 1e-6, 1)
    P = P / P.sum(1, keepdims=True)
    out = {"logloss": log_loss(y, P, labels=list(range(C))),
           "macro_f1": f1_score(y, P.argmax(1), average="macro", zero_division=0)}
    try:
        out["auc"] = roc_auc_score(y, P, multi_class="ovr", average="macro", labels=list(range(C)))
    except ValueError:
        pass
    return out


@R.utility_metrics.register("regression")
def regression_metrics(y, yhat, ctx):
    if ctx["kind"] not in ("reg", "vol"):
        return {}
    e, scale = yhat - y, ctx["scale"]
    ext = (y <= np.quantile(y, 0.05)) | (y >= np.quantile(y, 0.95))
    return {"mae": float(np.mean(np.abs(e))), "rmse": float(np.sqrt(np.mean(e ** 2))),
            "mase": float(np.mean(np.abs(e)) / scale),
            "smape": float(np.mean(2 * np.abs(e) / (np.abs(y) + np.abs(yhat) + 1e-12))),
            "mae_extreme": float(np.mean(np.abs(e[ext]))) / scale}


@R.utility_metrics.register("quantile")
def quantile_metrics(y, Q, ctx):
    if ctx["kind"] != "qreg":
        return {}
    pl = np.mean([pinball(y, Q[:, i], q) for i, q in enumerate(QUANTILES)], axis=0)
    cov = float(np.mean((y >= Q[:, 0]) & (y <= Q[:, -1])))
    return {"pinball": float(pl.mean() / ctx["scale"]), "coverage80": cov, "coverage80_err": abs(cov - 0.8),
            "crossing_share": float(np.mean(np.any(np.diff(Q, axis=1) < 0, axis=1)))}


@R.utility_metrics.register("multistep")
def multistep_metrics(Y, P, ctx):
    if ctx["kind"] != "ms":
        return {}
    ae = np.abs(P - Y)
    return {"mae": float(ae.mean()), "mase": float(ae.mean() / ctx["scale"]),
            "mase_last": float(ae[:, -1].mean() / ctx["scale"])}


def pinball(y, qhat, q):
    d = y - qhat
    return np.maximum(q * d, (q - 1) * d)


ROW_KINDS = ("clf", "mc", "qreg", "ms", "reg", "vol")


def row_score(kind, y, pred, scale, task=None):
    """Row-level score for paired tests: P(y=1) for clf, per-row loss otherwise; a custom kind uses its
    task's `row_loss`, without one its rows are NaN (with a warning)."""
    if kind not in ROW_KINDS:
        if task is not None and getattr(task, "row_loss", None) is not None:
            return np.asarray(task.row_loss(y, pred, scale), float)
        _warn_once(f"task kind {kind!r}: no row-level loss (Task.row_loss) — its rows are left out of the "
                   "row-level tests")
        return np.full(len(y), np.nan)
    if kind == "clf":
        return pred
    if kind == "mc":
        P = np.clip(pred, 1e-6, 1)
        P = P / P.sum(1, keepdims=True)
        return -np.log(P[np.arange(len(y)), y.astype(int)])
    if kind == "qreg":
        return np.mean([pinball(y, pred[:, i], q) for i, q in enumerate(QUANTILES)], axis=0) / scale
    if kind == "ms":
        return np.abs(pred - y).mean(1) / scale
    return np.abs(pred - y) / scale


def task_labels(p, cfg, task_name: str):
    """Real test labels of one task for every split in `cfg.test_splits` (row = position in the
    split): pyarrow Table split, row, y, y_vec (list, for vector tasks)."""
    import pyarrow as pa

    from .storage import list_array

    task = R.tasks.get(task_name)
    prm = target_params(cfg, p.name, task)
    parts = []
    for s in cfg.test_splits:
        v, h = p.part(s)
        _, yt, rws = make_xy(v, h, task, prm)
        n = len(rws)
        vec = yt.ndim == 2
        parts.append(pa.table({
            "split": pa.array([s] * n, pa.string()), "row": pa.array(rws.astype(np.int32)),
            "y": pa.array((np.full(n, np.nan) if vec else yt).astype(np.float32)),
            "y_vec": list_array(yt) if vec else pa.nulls(n, pa.list_(pa.float32()))}))
    return pa.concat_tables(parts)


def labels_fp(cfg, ds: str | None = None) -> str:
    """Labels depend on the processed data, the test splits and the exogenous thresholds (of `ds`)."""
    return cfg.unit_fingerprint(upstream=(",".join(cfg.test_splits),), files=("targets",), dataset=ds)


def ensure_labels(p, cfg, A) -> None:
    """Write `artifacts/labels/<ds>/<task>.parquet` for every task whose file is missing, unreadable
    or made with other data / test splits / thresholds (fingerprint in the file's metadata)."""
    import pyarrow.parquet as pq

    from .storage import check_done, write_arrow

    R.load_builtins()
    fp = labels_fp(cfg, p.name).encode()
    for tn in cfg.tasks or R.tasks.names():
        f = A.labels(p.name, tn)
        if check_done(f) and (pq.read_schema(f).metadata or {}).get(b"unit_fp") == fp:
            continue
        t = task_labels(p, cfg, tn)
        write_arrow(t.replace_schema_metadata({**(t.schema.metadata or {}), b"unit_fp": fp}), f)


def load_labels(A, ds: str, tasks) -> pd.DataFrame:
    frames = []
    for tn in tasks:
        f = A.labels(ds, tn)
        if f.exists():
            frames.append(pd.read_parquet(f).assign(task=tn))
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


def row_scores(pred_df: pd.DataFrame, labels: pd.DataFrame, scale: float = 1.0) -> pd.DataFrame:
    """Join predictions with labels and add the row-level `score` (P(y=1) for clf, loss otherwise).
    Rows without a label get NaN."""
    pred_df = pred_df.assign(task=pred_df["task"].astype(str), split=pred_df["split"].astype(str))
    labels = labels.assign(task=labels["task"].astype(str), split=labels["split"].astype(str))
    j = pred_df.merge(labels, on=["task", "split", "row"], how="left")
    scores = np.full(len(j), np.nan, np.float32)
    for tn, idx in j.groupby("task").groups.items():
        task = R.tasks.get(tn)
        kind = task.kind
        g = j.loc[idx]
        # vector labels / predictions: the built-in kinds that have them, or, for a custom kind, the data
        yvec = kind == "ms" or (kind not in ROW_KINDS and "y_vec" in g and g["y_vec"].notna().any())
        pvec = kind in ("mc", "qreg", "ms") or (kind not in ROW_KINDS and "pred_vec" in g and g["pred_vec"].notna().any())
        ok = g["y_vec"].notna().to_numpy() if yvec else g["y"].notna().to_numpy()
        if not ok.any():
            continue
        g = g[ok]
        pred = np.stack(g["pred_vec"].to_numpy()) if pvec else g["pred"].to_numpy()
        y = np.stack(g["y_vec"].to_numpy()) if yvec else g["y"].to_numpy()
        scores[j.index.get_indexer(g.index)] = row_score(kind, y, pred, scale, task)
    j["score"] = scores
    return j


# primary metric of each task kind: (key, higher is better) — the hyperparameter search criterion
SELECT_BY = {"clf": ("auc", True), "mc": ("logloss", False), "reg": ("mase", False), "vol": ("mase", False),
             "qreg": ("pinball", False), "ms": ("mase", False)}


def _predict(m, task, X, y_train):
    """Predictions; probabilities of balanced-weight models back on the training class priors."""
    pred = np.asarray(m.predict(X))
    if getattr(m, "balanced", False) and task.kind in ("clf", "mc"):
        pred = prior_correct(pred, task.kind, y_train, getattr(task, "n_classes", 2) or 2)
    return pred


def _fit_model(mn, task, seed, dev, cfg, regime, Xr, yr, Xs, ys, scale, train_share):
    """Fit one model in one regime. With `cfg.hpo` and a grid for the model: every candidate is
    fitted on the regime's own training data without its last `hpo_val_frac` rows and scored on that tail —
    R: the real train tail; S (TSTR): the tail of the synthetic series, so a model trained on synthetic data
    never sees real data before the test (never val / OOT either); the best is refitted on the whole
    training set. Returns (model, params, search log)."""
    import json

    cls = R.models.get(mn)
    grid = model_grid(cfg, mn) if cfg.hpo else []
    params, log = model_params(cfg, mn), []
    Xo, yo = (Xs, ys) if regime == "S" else (Xr, yr)   # the regime's own training rows
    nv = max(10, int(cfg.hpo_val_frac * len(Xo)))
    gap = task.h + max(LAGS)                           # no label or lag of the fit part reaches the tail
    if grid and len(Xo) - nv - gap >= 50:
        Xv, yv = Xo[-nv:], yo[-nv:]
        if regime == "S":
            Xc, yc, _ = build_train(regime, Xr, yr, Xs[:-(nv + gap)], ys[:-(nv + gap)])
        else:
            Xc, yc, _ = build_train(regime, Xr[:-(nv + gap)], yr[:-(nv + gap)], Xs, ys)
        key, higher = getattr(task, "select_by", None) or SELECT_BY.get(task.kind, (None, None))
        if key is None:                                # a custom task kind without a selection metric: no search
            _warn_once(f"task kind {task.kind!r}: no selection metric (SELECT_BY or Task.select_by) — "
                       "hyperparameter search skipped, fixed parameters used")
            grid = []
        best = None
        for cand in grid:
            try:
                m = cls(task, seed, dev, cand, cfg).fit(Xc, yc)
                v = _metrics(task, yv, _predict(m, task, Xv, yc), scale, train_share).get(key, np.nan)
            except Exception:
                v = np.nan
            log.append({"params": json.dumps(cand, sort_keys=True), key: v})
            if np.isfinite(v) and (best is None or (v > best[0] if higher else v < best[0])):
                best = (v, cand)
        if best is not None:
            params = best[1]
    X, y, _ = build_train(regime, Xr, yr, Xs, ys)
    return cls(task, seed, dev, params, cfg).fit(X, y), params, log


_WARNED: set = set()


def _warn_once(msg: str) -> None:
    if msg not in _WARNED:
        _WARNED.add(msg)
        print(f"WARNING: {msg}")


def _metrics(task, y, pred, scale, train_share):
    """Every registered utility metric of one prediction. A key returned by two metric functions keeps the
    first value; a value that is not a number is dropped (the tables hold scalars) — both with a warning."""
    ctx = {"kind": task.kind, "scale": scale, "train_share": train_share, "task": task}
    out = {"n": len(y)}
    for name, fn in R.utility_metrics.items():
        for k, v in fn(y, pred, ctx).items():
            if k in out:
                _warn_once(f"utility metric {k!r} of {name!r} is already set by another metric function: kept the first")
            elif v is None or isinstance(v, (bool, int, float, np.number)):
                out[k] = v
            else:
                _warn_once(f"utility metric {k!r} of {name!r} is not a number ({type(v).__name__}): dropped")
    return out


def _pred_table(tn, mn, regime, split, rows, pred):
    """Predictions of one (task, model, regime, split) as a pyarrow Table (no Python lists)."""
    import pyarrow as pa

    from .storage import list_array

    n = len(rows)
    vec = pred.ndim == 2
    return pa.table({
        "task": pa.array([tn] * n, pa.string()), "model": pa.array([mn] * n, pa.string()),
        "regime": pa.array([regime] * n, pa.string()), "split": pa.array([split] * n, pa.string()),
        "row": pa.array(rows.astype(np.int32)),
        "pred": pa.array((np.full(n, np.nan) if vec else pred).astype(np.float32)),
        "pred_vec": list_array(pred) if vec else pa.nulls(n, pa.list_(pa.float32()))})


# ─────────────────────── per (dataset, method, seed) ───────────────────────
def run_utility(p, synth, method: str, seed: int, cfg, out_dir=None, cells=None, done=None):
    """`synth` is None for the pseudo-method `real` (regime R, TRTR); otherwise the regime is S
    (TSTR). Computes the cells `cells` of the unit (task × model and the decision-transfer grid,
    `cells.utility_cells`; None → every cell) and returns (metrics, predictions). With `out_dir`, the
    computed cells replace their rows in the unit's files, the other rows are kept, and the unit's registry of
    done cells — `done` (`cells.utility_done`) plus the computed ones — is written last; a cell whose fit
    failed is not listed and is retried on the next run (marathonts/bench/cells.py)."""
    from . import cells as CL

    R.load_builtins()
    dev = cfg.device_str()
    want = CL.utility_cells(cfg, method, p.name)
    todo = set(want) if cells is None else set(cells)
    task_names = cfg.tasks or R.tasks.names()
    v_tr, h_tr = p.part("train")
    tests_raw = {s: p.part(s) for s in cfg.test_splits}
    regime = "S" if synth is not None else "R"
    from .progress import bar

    from .models import backend

    # ok: cells done — fitted, or without rows (skipped); here: cells this environment cannot run (a model's
    # kind needing XGBoost, `models.GBDT.all_kinds`) — left as they are for an environment that can
    rows, preds, weights, ok, here = [], [], {}, set(), set()
    for tn in bar(task_names, desc="tasks", leave=False, unit="task"):
        need = {k for k in todo if k != CL.GRID and k.split("|")[0] == tn}
        grid_here = CL.GRID in todo and tn == cfg.model_grid_task
        if not need and not grid_here:
            continue
        task = R.tasks.get(tn)
        prm = target_params(cfg, p.name, task)
        scale = seasonal_naive_scale(v_tr)
        Xr, yr, _ = make_xy(v_tr, h_tr, task, prm)
        Xs = ys = None
        if synth is not None:
            Xs, ys, _ = make_xy(synth.values, synth.how, task, prm)
            if len(Xs) == 0:
                ok |= need | ({CL.GRID} if grid_here else set())
                continue
        tests = {s: make_xy(v, h, task, prm) for s, (v, h) in tests_raw.items()}
        train_share = float(np.mean(yr)) if task.kind == "clf" else None
        X, y, n_syn = build_train(regime, Xr, yr, Xs, ys)
        if task.kind in ("clf", "mc") and len(np.unique(y)) < 2:
            ok |= need                                  # one class: nothing to fit
        else:
            for mn in cfg.models:
                if CL.cell_key(tn, mn) not in need:
                    continue
                if not supports(mn, task.kind):
                    here.add(CL.cell_key(tn, mn))
                    _warn_once(f"model {mn} cannot run task kind {task.kind!r} in this environment "
                               f"({backend(mn) or 'its kinds'}): those cells are left for an environment that can")
                    continue
                try:                                  # one failing fit must not lose the whole unit
                    import json

                    t0 = time.perf_counter()
                    m, used, search = _fit_model(mn, task, seed, dev, cfg, regime, Xr, yr, Xs, ys, scale, train_share)
                    fit_s = time.perf_counter() - t0
                    if cfg.save_model_weights:
                        for k, a in m.state().items():
                            weights[f"{tn}|{mn}|{regime}|{k}"] = a
                    for s, (Xt, yt, rws) in tests.items():
                        t1 = time.perf_counter()
                        pred = _predict(m, task, Xt, y)
                        pred_s = time.perf_counter() - t1
                        met = _metrics(task, yt, pred, scale, train_share)
                        rows.append(dict(dataset=p.name, method=method, seed=seed, task=tn, task_kind=task.kind,
                                         model=mn, regime=regime, split=s, fit_s=fit_s, predict_s=pred_s,
                                         n_train=len(X), n_synth_train=n_syn,
                                         params=json.dumps({**used, **({"_backend": backend(mn)} if backend(mn)
                                                                        not in (None, "xgboost") else {})},
                                                           sort_keys=True),
                                         hpo_candidates=len(search), **met))
                        # always kept: the hypothesis part's row-level tests need them
                        preds.append(_pred_table(tn, mn, regime, s, rws, pred))
                    ok.add(CL.cell_key(tn, mn))
                except Exception as e:
                    rows.append(dict(dataset=p.name, method=method, seed=seed, task=tn, task_kind=task.kind,
                                     model=mn, regime=regime, split="", error=f"{type(e).__name__}: {e}"))
        # U6.1 / U6.4 decision transfer (RQ5 c), optional: the method under test and its same-pool controls
        if grid_here:
            if cfg.decision_transfer and synth is not None and task.kind == "clf" \
                    and len(np.unique(ys)) == 2 and method in _grid_methods(cfg):
                val = tests.get("val") or next(iter(tests.values()))
                try:
                    rows += _decision_transfer(p, method, seed, cfg, task, Xr, yr, Xs, ys, val, dev)
                    ok.add(CL.GRID)
                except Exception as e:
                    rows.append(dict(dataset=p.name, method=method, seed=seed, task=tn, task_kind="grid",
                                     error=f"{type(e).__name__}: {e}"))
            else:
                ok.add(CL.GRID)
    met = pd.DataFrame(rows)
    if len(met):
        met["config_fingerprint"] = cfg.fingerprint()
        met["unit_fp"] = None                        # freshness is per cell (the registry), not per row
    import pyarrow as pa

    pr = pa.concat_tables(preds) if preds else None
    if out_dir is not None:
        redo = todo - here                           # cells this environment cannot run keep their rows
        met, pr = _merge_unit(Path(out_dir), met, pr, weights, redo, cfg)
        CL.write_done(Path(out_dir) / "cells.json",          # last: marks the cells as done
                      {**{k: v for k, v in (done or {}).items() if k not in redo}, **{k: want[k] for k in ok - here}})
    return met, (pr.to_pandas() if pr is not None else pd.DataFrame())


def _merge_unit(out_dir: Path, met: pd.DataFrame, pr, weights: dict, redo: set, cfg):
    """Write the computed cells `redo` into the unit's files: their old rows (metrics, predictions, weights) are
    replaced, the rows of the other cells kept. Returns the merged (metrics, predictions)."""
    import pyarrow as pa
    import pyarrow.parquet as pq

    from . import cells as CL
    from .storage import check_done, read_arrays, read_table, write_arrow

    old = lambda name: out_dir / name if check_done(out_dir / name) else None     # noqa: E731
    if (f := old("metrics.parquet")) is not None:
        prev = read_table(f)
        if len(prev):
            kind = prev["task_kind"] if "task_kind" in prev else pd.Series("", index=prev.index)
            prev = prev[[CL.cell_key(t, m, k) not in redo
                         for t, m, k in zip(prev["task"].astype(str), prev["model"].astype(str), kind)]]
            met = pd.concat([prev, met], ignore_index=True) if len(met) else prev.reset_index(drop=True)
    if (f := old("predictions.parquet")) is not None:
        prev = pq.read_table(f)
        keep = [f"{t}|{m}" not in redo for t, m in zip(prev.column("task").to_pylist(), prev.column("model").to_pylist())]
        prev = prev.filter(pa.array(keep, pa.bool_()))
        pr = pa.concat_tables([prev, pr], promote_options="default") if pr is not None else prev
    if cfg.save_model_weights:
        if (f := old("models.parquet")) is not None:
            weights = {**{k: a for k, a in read_arrays(f).items() if "|".join(k.split("|")[:2]) not in redo}, **weights}
        if weights:
            write_arrays(weights, out_dir / "models.parquet", dtype=cfg.weights_dtype)
    if pr is not None and pr.num_rows:
        write_arrow(pr, out_dir / "predictions.parquet")
    if len(met):
        write_table(met, out_dir / "metrics.parquet")
    return met, pr


def _decision_transfer(p, method, seed, cfg, task, Xr, yr, Xs, ys, val, dev):
    """U6.1: AUC of every grid configuration trained on real (R) and on synthetic (S) data, on val —
    the ranking agreement is tested in RQ5 (c). U6.4: F1 at a threshold chosen on synthetic data versus
    the best threshold on val."""
    from sklearn.metrics import f1_score, roc_auc_score

    Xv, yv, _ = val
    rows, i = [], 0
    clf_models = [mn for mn in cfg.models if mn in R.models and "clf" in getattr(R.models.get(mn), "kinds", ("clf",))]
    for mn in clf_models:                              # every model of the run with a grid (custom ones too)
        for prm in model_grid(cfg, mn):
            for regime, (X, y) in (("R", (Xr, yr)), ("S", (Xs, ys))):
                try:                               # one failing configuration loses only its row
                    m = R.models.get(mn)(task, seed, dev, prm, cfg).fit(X, y)
                    auc = roc_auc_score(yv, m.predict(Xv))
                except Exception:
                    auc = np.nan
                rows.append(dict(dataset=p.name, method=method, seed=seed, task=task.name, task_kind="grid",
                                 model=f"{mn}:{sorted(prm.items())}", regime=regime, split="val", grid_id=i,
                                 auc=auc))
            i += 1
    cut = int(0.8 * len(Xs))
    if ys[cut:].sum() == 0 or ys[:cut].sum() == 0 or yv.sum() == 0:
        return rows                                    # no positives to set a threshold on: no U6.4 row
    tm = "linear" if "linear" in clf_models else (clf_models or [None])[0]     # the threshold model (U6.4)
    if tm is None:
        return rows
    m = R.models.get(tm)(task, seed, dev, model_params(cfg, tm), cfg).fit(Xs[:cut], ys[:cut])
    ps = m.predict(Xs[cut:])
    grid = np.linspace(0.05, 0.95, 91)
    thr_s = grid[np.argmax([f1_score(ys[cut:], ps >= g, zero_division=0) for g in grid])]
    pv = m.predict(Xv)
    thr_v = grid[np.argmax([f1_score(yv, pv >= g, zero_division=0) for g in grid])]
    rows.append(dict(dataset=p.name, method=method, seed=seed, task=task.name, task_kind="threshold",
                     model=tm, regime="S", split="val",
                     f1_transfer=f1_score(yv, pv >= thr_s, zero_division=0),
                     f1_oracle=f1_score(yv, pv >= thr_v, zero_division=0)))
    return rows
