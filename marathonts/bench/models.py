"""Downstream ML models (METRICS U3), registered by name.

Interface (`BaseModel`): `fit(X, y)`, `predict(X)`, `state()` (weights as numpy arrays, saved
as Parquet) and `load_state(arrays)` — restores a fitted model from those arrays, so that
`predict` works without refitting (`bench.load.load_model` reads them from the artifacts). Prediction shapes by task kind: clf → P(y = 1) (n,); mc → probabilities (n, C);
reg / vol → (n,); qreg → (n, len(QUANTILES)); ms → (n, h).

Built-ins (torch, on CUDA when available):
  linear   logistic / softmax with balanced class weights and L2 (C), ridge (closed form),
           linear quantile regression (smoothed pinball) — L-BFGS, full batch.
  mlp      2 hidden layers (64, 32), Adam, weight decay `weight_decay`; optional early stopping
           (`early_stopping_patience`, profile max) on 10% of the distinct rows.
  gbdt     XGBoost (`device="cuda"` when available; quantile and multi-output native);
           sklearn HistGradientBoosting if xgboost is missing and by default on macOS (OpenMP
           conflict with torch there; BENCH_GBDT_BACKEND overrides) — no multi-step task then.
scikit-learn implementations of the same families: sk_linear, sk_hgb, sk_mlp.

Custom model:

    from marathonts.bench import registry as R
    from marathonts.bench.models import BaseModel

    @R.models.register("my_model")
    class MyModel(BaseModel):
        kinds = {"clf", "reg"}
        def fit(self, X, y): ...; return self
        def predict(self, X): ...
"""
from __future__ import annotations

import numpy as np

from . import registry as R
from .storage import blob, torch_state
from .tasks import QUANTILES, Task


class BaseModel:
    kinds: set = {"clf", "mc", "reg", "qreg", "ms", "vol"}
    # trained with balanced class weights (clf / mc): predict() then returns probabilities for equal
    # class priors; the utility stage maps them back to the training priors (`prior_correct`)
    balanced: bool = False

    def __init__(self, task: Task, seed: int = 0, device: str = "cpu", params: dict | None = None, cfg=None):
        self.task, self.seed, self.device, self.params, self.cfg = task, seed, device, dict(params or {}), cfg

    def fit(self, X, y):
        raise NotImplementedError

    def predict(self, X):
        raise NotImplementedError

    def state(self) -> dict[str, np.ndarray]:
        return {}

    def load_state(self, arrays: dict[str, np.ndarray]) -> "BaseModel":
        """Inverse of `state()`: the model predicts as when it was saved."""
        raise NotImplementedError(f"{type(self).__name__} cannot load weights")


def model_params(cfg, name: str) -> dict:
    """Exogenous hyperparameters of a model: `cfg.model_configs_file[name]`, then any explicit
    override in `cfg.extra[name]`. Fixed before the run; the optional search (`Config.hpo`) chooses among
    the configurations of `model_grid`."""
    import json

    base = {}
    f = getattr(cfg, "model_configs_file", None)
    if f is not None and f.exists():
        base = json.loads(f.read_text()).get(name, {})
    return {**base, **(cfg.params(name) if cfg is not None else {})}


def model_grid(cfg, name: str) -> list[dict]:
    """Candidate configurations of a model for the hyperparameter search: each grid entry merged
    over the model's fixed configuration (`model_configs_file["grids"][name]`)."""
    import json

    f = getattr(cfg, "model_configs_file", None)
    grids = json.loads(f.read_text()).get("grids", {}) if f is not None and f.exists() else {}
    base = model_params(cfg, name)
    return [{**base, **g} for g in grids.get(name, [])]


def supports(model_name: str, kind: str) -> bool:
    return kind in R.models.get(model_name).kinds


def prior_correct(pred, kind: str, y_train, n_classes: int = 2):
    """Map probabilities of a model trained with balanced class weights back to the class priors of
    its training set: P(c|x) ∝ P_balanced(c|x) · share(c). Rank metrics (AUC, PR AUC, lift, F1 at a
    quantile) do not change; calibration metrics (Brier, log-loss, ECE) become meaningful."""
    y = np.asarray(y_train)
    if kind == "clf":
        pi = float(np.clip(np.mean(y), 1e-6, 1 - 1e-6))
        p = np.clip(np.asarray(pred, float), 1e-9, 1 - 1e-9)
        odds = p / (1 - p) * pi / (1 - pi)
        return odds / (1 + odds)
    if kind == "mc":
        share = np.bincount(y.astype(int), minlength=n_classes) / max(len(y), 1)
        P = np.asarray(pred, float) * share[None, :]
        return P / np.maximum(P.sum(1, keepdims=True), 1e-12)
    return pred


def _balanced(y, n_classes):
    cnt = np.bincount(y.astype(int), minlength=n_classes).astype(float)
    w = len(y) / (n_classes * np.maximum(cnt, 1))
    return w[y.astype(int)]


# ─────────────────────── torch helpers ─────────────────────────────────────
class _TorchBase(BaseModel):
    def _t(self, a, dtype=None):
        import torch

        return torch.as_tensor(np.asarray(a), dtype=dtype or torch.float32, device=self.device)

    def _scale_fit(self, X, y):
        # a feature constant in training gets std 1 (as StandardScaler): dividing by ~0 would blow
        # up any variation at test time
        sd = X.std(0)
        self.mu, self.sd = X.mean(0), np.where(sd < 1e-6, 1.0, sd).astype(np.float32)
        if self.task.kind in ("reg", "vol", "qreg", "ms"):
            ysd = float(np.std(y))
            self.ymu, self.ysd = float(np.mean(y)), (ysd if ysd > 1e-6 else 1.0)
        else:
            self.ymu, self.ysd = 0.0, 1.0

    def _X(self, X):
        return self._t((np.asarray(X, np.float32) - self.mu) / self.sd)

    def _yt(self, y):
        return (np.asarray(y, np.float32) - self.ymu) / self.ysd


def _smooth_pinball(u, q, eps):
    import torch

    return q * u + eps * torch.nn.functional.softplus(-u / eps)        # → max(q·u, (q−1)·u) as eps → 0


# ─────────────────────── linear (torch) ────────────────────────────────────
@R.models.register("linear")
class TorchLinear(_TorchBase):
    balanced = True

    def fit(self, X, y):
        import torch

        torch.manual_seed(self.seed)
        X, y = np.asarray(X, np.float32), np.asarray(y)
        self._scale_fit(X, y)
        Xt = self._X(X)
        n, d = Xt.shape
        k = self.task.kind
        if k in ("reg", "vol", "ms"):                                   # ridge, closed form (alpha = 1)
            Y = self._t(self._yt(y)).reshape(n, -1)
            A = Xt.T @ Xt + float(self.params["ridge_alpha"]) * torch.eye(d, device=self.device)
            self.W = torch.linalg.solve(A, Xt.T @ Y)                       # y centred, X centred → no bias
            self.b = torch.zeros(Y.shape[1], device=self.device)
            return self
        if k == "clf":
            out, C = 1, float(self.params["C"])
            yt = self._t(y)
            w = self._t(_balanced(y, 2))
        elif k == "mc":
            out, C = self.task.n_classes, float(self.params["C"])
            yt = self._t(y, torch.long)
            w = self._t(_balanced(y, out))
        elif k == "qreg":
            out, C = len(QUANTILES), None
            yt = self._t(self._yt(y))
            qs = self._t(np.array(QUANTILES, np.float32))
        else:
            raise ValueError(k)
        W = torch.zeros(d, out, device=self.device, requires_grad=True)
        b = torch.zeros(out, device=self.device, requires_grad=True)
        opt = torch.optim.LBFGS([W, b], lr=1, max_iter=int(self.params["lbfgs_max_iter"]), line_search_fn="strong_wolfe")
        eps = float(self.params["pinball_eps"])

        def closure():
            opt.zero_grad()
            z = Xt @ W + b
            if k == "clf":
                loss = (w * torch.nn.functional.binary_cross_entropy_with_logits(z[:, 0], yt, reduction="none")).sum()
                loss = loss + 0.5 / C * (W ** 2).sum()
            elif k == "mc":
                loss = (w * torch.nn.functional.cross_entropy(z, yt, reduction="none")).sum() + 0.5 / C * (W ** 2).sum()
            else:
                loss = _smooth_pinball(yt[:, None] - z, qs[None, :], eps).mean()
            loss.backward()
            return loss

        opt.step(closure)
        self.W, self.b = W.detach(), b.detach()
        return self

    def predict(self, X):
        import torch

        z = self._X(X) @ self.W + self.b
        k = self.task.kind
        if k == "clf":
            return torch.sigmoid(z[:, 0]).cpu().numpy()
        if k == "mc":
            return torch.softmax(z, 1).cpu().numpy()
        out = (z * self.ysd + self.ymu).cpu().numpy()
        return out[:, 0] if k in ("reg", "vol") else out

    def state(self):
        return {"W": self.W.cpu().numpy(), "b": self.b.cpu().numpy(), "x_mean": self.mu, "x_std": self.sd,
                "y_mean_std": np.array([self.ymu, self.ysd])}

    def load_state(self, a):
        self.W, self.b = self._t(a["W"]), self._t(a["b"])
        self.mu, self.sd = np.asarray(a["x_mean"], np.float32), np.asarray(a["x_std"], np.float32)
        self.ymu, self.ysd = (float(v) for v in a["y_mean_std"])
        return self


# ─────────────────────── MLP (torch) ───────────────────────────────────────
@R.models.register("mlp")
class TorchMLP(_TorchBase):
    balanced = True

    def fit(self, X, y):
        import torch

        torch.manual_seed(self.seed)
        X, y = np.asarray(X, np.float32), np.asarray(y)
        self._scale_fit(X, y)
        k = self.task.kind
        out = {"clf": 1, "mc": self.task.n_classes, "qreg": len(QUANTILES), "ms": y.shape[1] if y.ndim == 2 else 1,
               "reg": 1, "vol": 1}[k]
        prm = self.params
        self.net = self._build(X.shape[1], out, prm["hidden"])
        opt = torch.optim.Adam(self.net.parameters(), lr=float(prm["lr"]), weight_decay=float(prm["weight_decay"]))
        Xt = self._X(X)
        if k == "mc":
            Yt = self._t(y, torch.long)
            cw = self._t(len(y) / (out * np.maximum(np.bincount(y.astype(int), minlength=out), 1)))
            lossf = torch.nn.CrossEntropyLoss(weight=cw)
        elif k == "clf":
            Yt = self._t(y)
            pos = max(float(y.mean()), 1e-6)
            bce = torch.nn.BCEWithLogitsLoss(pos_weight=self._t(np.array((1 - pos) / pos, np.float32)))
            lossf = lambda z, t: bce(z[:, 0], t)
        elif k == "qreg":
            Yt = self._t(self._yt(y))
            qs = self._t(np.array(QUANTILES, np.float32))
            eps = float(prm["pinball_eps"])
            lossf = lambda z, t: _smooth_pinball(t[:, None] - z, qs[None, :], eps).mean()
        else:
            Yt = self._t(self._yt(y)).reshape(len(y), -1)
            lossf = torch.nn.MSELoss()
        bs = int(prm["batch_size"])
        g = torch.Generator(device=self.device).manual_seed(self.seed)
        idx = torch.arange(len(Xt), device=self.device)
        patience = prm.get("early_stopping_patience")
        if patience:                              # optional (profile max): 10% of rows decide the epoch
            # by distinct row: a repeated row (e.g. the same pool window twice) on both sides would hide overfitting
            _, grp = np.unique(X, axis=0, return_inverse=True)
            grp = grp.reshape(-1)
            gperm = np.random.default_rng(self.seed).permutation(grp.max() + 1)
            is_val = np.isin(grp, gperm[:max(1, len(gperm) // 10)])
            iv = idx[torch.as_tensor(is_val, device=self.device)]
            idx = idx[torch.as_tensor(~is_val, device=self.device)]
        best, best_state, bad = np.inf, None, 0
        for _ in range(int(prm["epochs"])):
            self.net.train()
            order = idx[torch.randperm(len(idx), device=self.device, generator=g)]
            for i in range(0, len(order), bs):
                b = order[i:i + bs]
                opt.zero_grad()
                lossf(self.net(Xt[b]), Yt[b]).backward()
                opt.step()
            if patience:
                self.net.eval()
                with torch.no_grad():
                    vl = float(lossf(self.net(Xt[iv]), Yt[iv]))
                if vl < best - 1e-6:
                    best, bad, best_state = vl, 0, {k: v.clone() for k, v in self.net.state_dict().items()}
                else:
                    bad += 1
                    if bad >= int(patience):
                        break
        if best_state is not None:
            self.net.load_state_dict(best_state)
        self.net.eval()
        return self

    def predict(self, X):
        import torch

        self.net.eval()
        with torch.no_grad():
            z = self.net(self._X(X))
        k = self.task.kind
        if k == "clf":
            return torch.sigmoid(z[:, 0]).cpu().numpy()
        if k == "mc":
            return torch.softmax(z, 1).cpu().numpy()
        out = (z * self.ysd + self.ymu).cpu().numpy()
        return out[:, 0] if k in ("reg", "vol") else out

    def _build(self, d, out, hidden):
        import torch

        layers, prev = [], d
        for h in hidden:
            layers += [torch.nn.Linear(prev, int(h)), torch.nn.ReLU()]
            prev = int(h)
        layers.append(torch.nn.Linear(prev, out))
        return torch.nn.Sequential(*layers).to(self.device)

    def state(self):
        s = torch_state(self.net, "net.")
        s.update(x_mean=self.mu, x_std=self.sd, y_mean_std=np.array([self.ymu, self.ysd]))
        return s

    def load_state(self, a):
        import torch

        sd = {k[4:]: torch.as_tensor(v) for k, v in a.items() if k.startswith("net.")}
        lin = sorted({int(k.split(".")[0]) for k in sd if k.endswith(".weight")})   # Linear layers in order
        hidden = [sd[f"{i}.weight"].shape[0] for i in lin[:-1]]
        self.net = self._build(sd[f"{lin[0]}.weight"].shape[1], sd[f"{lin[-1]}.weight"].shape[0], hidden)
        self.net.load_state_dict({k: v.to(torch.float32) for k, v in sd.items()})
        self.net.eval()
        self.mu, self.sd = np.asarray(a["x_mean"], np.float32), np.asarray(a["x_std"], np.float32)
        self.ymu, self.ysd = (float(v) for v in a["y_mean_std"])
        return self


# ─────────────────────── GBDT (XGBoost, sklearn fallback) ──────────────────
# Backend: XGBoost by default. On macOS torch and xgboost load two different OpenMP runtimes and
# xgboost segfaults once torch has started its thread pool, so there the default is sklearn's
# HistGradientBoosting. Override with the environment variable BENCH_GBDT_BACKEND=xgboost|sklearn.
import os as _os
import platform as _platform

_GBDT_BACKEND = _os.environ.get("BENCH_GBDT_BACKEND",
                                "sklearn" if _platform.system() == "Darwin" else "xgboost")
_XGB_JOBS = -1


@R.models.register("gbdt")
class GBDT(BaseModel):
    balanced = True                              # xgboost and the HistGradientBoosting fallback

    def fit(self, X, y):
        try:
            if _GBDT_BACKEND != "xgboost":
                raise ImportError
            import xgboost as xgb
        except ImportError:
            self.fallback = SkHGB(self.task, self.seed, self.device, self.params, self.cfg).fit(X, y)
            return self
        self.fallback = None
        k = self.task.kind
        prm = self.params
        # device: "auto" (CUDA if the benchmark runs on it), "cpu" or "cuda" — on ~10k rows the CPU is
        # usually faster (GPU launch overhead); max_bin: histogram bins (256 default, 64 faster)
        dev = prm.get("device", "auto")
        dev = ("cuda" if self.device.startswith("cuda") else "cpu") if dev == "auto" else dev
        extra = {"max_bin": int(prm["max_bin"])} if prm.get("max_bin") else {}
        common = dict(n_estimators=int(prm["n_estimators"]), max_depth=prm["max_depth"], learning_rate=float(prm["learning_rate"]),
                      tree_method="hist", device=dev, **extra,
                      random_state=self.seed, n_jobs=_XGB_JOBS)
        X = np.asarray(X, np.float32)
        if k == "clf":
            pos = max(float(np.mean(y)), 1e-6)
            self.m = xgb.XGBClassifier(objective="binary:logistic", scale_pos_weight=(1 - pos) / pos, **common)
            self.m.fit(X, y.astype(int))
        elif k == "mc":
            C = self.task.n_classes
            yi, w = y.astype(int), _balanced(y, C)
            missing = sorted(set(range(C)) - set(np.unique(yi)))
            if missing:                      # xgboost needs every class: one negligible-weight row each
                X = np.vstack([X, np.repeat(X.mean(0, keepdims=True), len(missing), 0)])
                yi = np.r_[yi, missing]
                w = np.r_[w, np.full(len(missing), 1e-9)]
            self.m = xgb.XGBClassifier(objective="multi:softprob", num_class=C, **common)
            self.m.fit(X, yi, sample_weight=w)
        elif k == "qreg":
            self.m = xgb.XGBRegressor(objective="reg:quantileerror", quantile_alpha=np.array(QUANTILES), **common)
            self.m.fit(X, y)
        elif k == "ms":
            # one_output_per_tree: a separate ensemble per step (h × the trees); multi_output_tree: one
            # ensemble with vector leaves (~5–10× faster on the 24-step task)
            self.m = xgb.XGBRegressor(objective="reg:squarederror",
                                      multi_strategy=prm.get("multi_strategy_ms", "one_output_per_tree"), **common)
            self.m.fit(X, y)
        else:
            self.m = xgb.XGBRegressor(objective="reg:squarederror", **common)
            self.m.fit(X, y)
        return self

    def predict(self, X):
        if self.fallback is not None:
            return self.fallback.predict(X)
        X = np.asarray(X, np.float32)
        k = self.task.kind
        if k == "clf":
            return self.m.predict_proba(X)[:, 1]
        if k == "mc":
            P = np.zeros((len(X), self.task.n_classes))
            P[:, self.m.classes_.astype(int)] = self.m.predict_proba(X)
            return P
        return self.m.predict(X)

    def state(self):
        if self.fallback is not None:
            return self.fallback.state()
        return {"booster_ubj": np.frombuffer(bytes(self.m.get_booster().save_raw("ubj")), np.uint8)}

    def load_state(self, a):
        if "sklearn_pickle" in a:                    # saved by the sklearn fallback
            self.fallback = SkHGB(self.task, self.seed, self.device, self.params, self.cfg).load_state(a)
            return self
        import xgboost as xgb

        self.fallback = None
        cls = xgb.XGBClassifier if self.task.kind in ("clf", "mc") else xgb.XGBRegressor
        self.m = cls()
        self.m.load_model(bytearray(np.asarray(a["booster_ubj"], np.uint8).tobytes()))
        if self.task.kind in ("clf", "mc") and not hasattr(self.m, "classes_"):
            self.m.classes_ = np.arange(2 if self.task.kind == "clf" else self.task.n_classes)
        return self


# ─────────────────────── scikit-learn implementations ──────────────────────
class _Sk(BaseModel):
    def state(self):
        return {"sklearn_pickle": blob(self.m if getattr(self, "m", None) is not None else self.ms)}

    def load_state(self, a):
        from .storage import unblob

        obj = unblob(a["sklearn_pickle"])
        if isinstance(obj, list) and obj and isinstance(obj[0], BaseModel):
            self.m, self.ms = None, obj
        else:
            self.m = obj
        return self


@R.models.register("sk_linear")
class SkLinear(_Sk):
    balanced = True

    kinds = {"clf", "mc", "reg", "qreg", "ms", "vol"}

    def fit(self, X, y):
        from sklearn.linear_model import LogisticRegression, Ridge
        from sklearn.pipeline import make_pipeline
        from sklearn.preprocessing import StandardScaler

        k = self.task.kind
        if k in ("clf", "mc"):
            self.m = make_pipeline(StandardScaler(), LogisticRegression(max_iter=int(self.params["max_iter"]),
                                                                        class_weight="balanced", C=float(self.params["C"])))
        elif k == "qreg":
            lin = {"C": self.params["C"], "ridge_alpha": self.params["ridge_alpha"], "lbfgs_max_iter": 300, "pinball_eps": 1e-3}
            self.ms = [TorchLinear(self.task, self.seed, "cpu", lin, self.cfg).fit(X, y)]
            self.m = None
            return self
        else:
            self.m = make_pipeline(StandardScaler(), Ridge(alpha=float(self.params["ridge_alpha"])))
        self.m.fit(X, y)
        return self

    def predict(self, X):
        if self.m is None:
            return self.ms[0].predict(X)
        return _sk_predict(self.m, self.task, X)

    def state(self):                         # qreg: arrays of the torch model (it holds unpicklable lambdas)
        if self.m is None:
            return {f"torch_linear.{k}": v for k, v in self.ms[0].state().items()}
        return super().state()

    def load_state(self, a):
        if any(k.startswith("torch_linear.") for k in a):
            self.m = None
            self.ms = [TorchLinear(self.task, self.seed, "cpu", {}, self.cfg)
                       .load_state({k[len("torch_linear."):]: v for k, v in a.items()})]
            return self
        return super().load_state(a)


@R.models.register("sk_hgb")
class SkHGB(_Sk):
    balanced = True

    kinds = {"clf", "mc", "reg", "qreg", "vol"}

    def fit(self, X, y):
        from sklearn.ensemble import HistGradientBoostingClassifier, HistGradientBoostingRegressor

        k, s, prm = self.task.kind, self.seed, self.params
        hp = dict(max_iter=int(prm["n_estimators"]), max_depth=prm["max_depth"], learning_rate=float(prm["learning_rate"]),
                  random_state=s)                       # fixed: early stopping off (exogenous configuration)
        if k in ("clf", "mc"):
            self.m = HistGradientBoostingClassifier(class_weight="balanced", early_stopping=False, **hp).fit(X, y)
        elif k == "qreg":
            self.m = [HistGradientBoostingRegressor(loss="quantile", quantile=q, early_stopping=False, **hp).fit(X, y)
                      for q in QUANTILES]
        else:
            self.m = HistGradientBoostingRegressor(early_stopping=False, **hp).fit(X, y)
        return self

    def predict(self, X):
        if isinstance(self.m, list):
            return np.column_stack([m.predict(X) for m in self.m])
        return _sk_predict(self.m, self.task, X)


@R.models.register("sk_mlp")
class SkMLP(_Sk):
    kinds = {"clf", "mc", "reg", "ms", "vol"}

    def fit(self, X, y):
        from sklearn.neural_network import MLPClassifier, MLPRegressor
        from sklearn.pipeline import make_pipeline
        from sklearn.preprocessing import StandardScaler

        cls = MLPClassifier if self.task.kind in ("clf", "mc") else MLPRegressor
        self.m = make_pipeline(StandardScaler(), cls(hidden_layer_sizes=tuple(self.params["hidden"]), early_stopping=False,
                                                     max_iter=int(self.params["epochs"]), random_state=self.seed,
                                                     alpha=float(self.params["weight_decay"])))
        self.m.fit(X, y)
        return self

    def predict(self, X):
        return _sk_predict(self.m, self.task, X)


def _sk_predict(m, task, X):
    if task.kind == "clf":
        return m.predict_proba(X)[:, 1]
    if task.kind == "mc":
        P = np.zeros((len(X), task.n_classes))
        P[:, m.classes_.astype(int)] = m.predict_proba(X)
        return P
    return m.predict(X)


def _xgb_available():
    try:
        import importlib.util

        return _GBDT_BACKEND == "xgboost" and importlib.util.find_spec("xgboost") is not None
    except Exception:
        return False


# what gbdt is defined for (XGBoost) and what it runs here: without XGBoost (or on macOS by default) the
# sklearn fallback has no multi-step task. The expected cells follow `all_kinds`, so results made with
# XGBoost stay valid where it is missing; such cells are left for an environment that can run them
GBDT.all_kinds = {"clf", "mc", "reg", "qreg", "ms", "vol"}
GBDT.kinds = set(GBDT.all_kinds) if _xgb_available() else SkHGB.kinds


def backend(model_name: str) -> str | None:
    """The implementation a model runs with here, where it can differ between environments (gbdt)."""
    return ("xgboost" if _xgb_available() else "sklearn") if model_name == "gbdt" else None
