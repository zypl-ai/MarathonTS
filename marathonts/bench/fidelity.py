"""Stage 3 — fidelity metrics (METRICS.md F1–F12) of one synthetic series against real data.

Metrics are organised in registered **groups** (`registry.fidelity_metrics`); each group is a
function `fn(ctx) -> {metric_id: value}` over a shared `FidelityContext` (synthetic and real
series, windows, window features — computed once, lazily). `fidelity(...)` runs every group in
`Config.fidelity_groups` (default: all) and returns one flat dict.

Every metric has an orientation (`ORIENT`: −1 lower is better, +1 higher is better). Custom group:

    from marathonts.bench.fidelity import register_fidelity_group
    @register_fidelity_group("my_group", {"M1_spikiness": -1})
    def my_group(ctx):
        return {"M1_spikiness": abs(spikiness(ctx.x) - spikiness(ctx.ref))}

The primary real reference is the val part (`Config.fidelity_ref`); its metrics carry no suffix.
Every metric is also computed against the other real parts (`Config.fidelity_extra_refs`, default
train and OOT) under the suffix `@<part>` (`F1.1_ks@train`, `F1.1_ks@oot`): train shows how well a
method reproduces what it was fitted on, val — generalisation, OOT — generalisation under drift.
Methods fitted on train use the `@train` data during fitting.
Groups in `PRIMARY_ONLY` (F10: distance to train) are computed once.
Pairwise distances (MMD, nearest neighbours, PRDC) and the GRU discriminator run in torch on
the GPU when available.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from functools import cached_property

import numpy as np
import pandas as pd
from scipy import signal, stats

from . import registry as R
from .tasks import labels

# metric id → orientation (filled by register_fidelity_group)
ORIENT: dict[str, int] = {}
GROUP_OF: dict[str, str] = {}
REFS = ("train", "val", "oot")             # real parts a metric can be referenced to (suffix `@<part>`)
PRIMARY_ONLY: set[str] = set()             # groups computed against the primary reference only


def split_ref(metric: str, primary: str = "val") -> tuple[str, str]:
    """`F1.1_ks@oot` → ("F1.1_ks", "oot"); an unsuffixed id is referenced to the primary part."""
    base, _, ref = metric.partition("@")
    return (base, ref) if ref in REFS else (metric, primary)


def register_fidelity_group(name: str, spec: dict, overwrite: bool = False, primary_only: bool = False):
    """Decorator: register `fn(ctx) -> dict` under `name`; `spec` = {metric: orientation} (+1 / −1; a tuple
    whose first element is the orientation is accepted too).
    Unless `primary_only`, the `@<part>` copies of every metric are registered too."""
    def deco(fn):
        R.fidelity_metrics.register(name, fn, overwrite=overwrite)
        if primary_only:
            PRIMARY_ONLY.add(name)
        for m, o in spec.items():
            o = o[0] if isinstance(o, (tuple, list)) else o
            for k in [m] + ([] if primary_only else [f"{m}@{r}" for r in REFS]):
                ORIENT[k], GROUP_OF[k] = int(o), name
        return fn

    return deco


_SPEC: dict = {}
for _n, _o in [
    # F1 marginal
    ("F1.1_ks", -1), ("F1.2_w1", -1), ("F1.3_ad", -1), ("F1.4_qq_corr", +1),
    ("F1.5_quantile_err", -1), ("F1.5_q01_err", -1), ("F1.5_q99_err", -1),
    ("F1.6_mean_err", -1), ("F1.6_std_err", -1), ("F1.6_skew_err", -1),
    ("F1.6_kurt_err", -1), ("F1.7_out_of_range", -1), ("F1.8_coverage", +1),
    ("F1.9_js", -1), ("F1.10_hill_err", -1),
    # F2 increments
    ("F2.1_ks_d1", -1), ("F2.1_ks_d6", -1), ("F2.1_ks_d24", -1), ("F2.1_ks_d168", -1),
    ("F2.1_w1_d24", -1), ("F2.2_vol_ratio_err_d1", -1), ("F2.2_vol_ratio_err_d24", -1),
    ("F2.3_up_share_err", -1), ("F2.4_big_jump_share_err", -1),
    # F3 dependence
    ("F3.1_acf_in_window", -1), ("F3.2_acf_beyond_window", -1), ("F3.3_pacf", -1),
    ("F3.4_acf_abs_d", -1), ("F3.4_acf_sq_d", -1), ("F3.5_log_psd", -1),
    ("F3.6_peak24_err", -1), ("F3.6_peak168_err", -1), ("F3.7_dfa_err", -1),
    ("F3.8_calendar_corr_err", -1),
    # F4 seasonality
    ("F4.1_how_mean", -1), ("F4.2_how_std", -1), ("F4.3_hod_mean", -1),
    ("F4.4_calendar_continuity", +1), ("F4.5_calendar_seam_breaks", -1),
    # F5 seams
    ("F5.1_ks_seam_vs_real", -1), ("F5.2_ks_seam_vs_inside", -1), ("F5.3_seam_z_mean", -1),
    ("F5.3_seam_z_p95", -1), ("F5.4_seam_local_acf", -1), ("F5.5_cp_rate_err", -1),
    ("F5.6_cp_at_seams", -1), ("F5.7_seam_detect_auc_dev", -1),
    # F6 window distribution
    ("F6.1_disc_score", -1), ("F6.2_c2st_auc_dev", -1), ("F6.3_pred_score_err", -1),
    ("F6.4_mmd", -1), ("F6.4_mmd_2T", -1), ("F6.6_feature_fid", -1),
    ("F6.8_nn_dist_logratio", -1),
    # F7 long structure
    ("F7.1_roll_mean_ks", -1), ("F7.2_roll_std_ks", -1), ("F7.3_crossings_err", -1),
    ("F7.4_excursion_ks", -1), ("F7.5_drawdown_ks", -1), ("F7.6_trend_err", -1),
    ("F7.6_weekly_level_std_err", -1), ("F7.7_regime_dur_err", -1),
    # F8 target
    ("F8.1_class_tvd", -1), ("F8.2_event_dur_ks", -1), ("F8.3_interarrival_ks", -1),
    ("F8.4_event_by_how", -1), ("F8.5_cond_event_err", -1), ("F8.6_cond_future_ks", -1),
    # F9 diversity / coverage
    ("F9.1_precision", +1), ("F9.1_recall", +1), ("F9.2_density_logdev", -1),
    ("F9.2_coverage", +1),
    # F10 memorisation
    ("F10.1_dcr_logratio", -1), ("F10.2_near_copy_share", -1),
    # F11 class balance over every classification task (F8 is the case-study task `stitch_task` only)
    ("F11.1_class_share_logratio", -1), ("F11.2_rare_share_logratio", -1),
    ("F11.3_multiclass_tvd", -1), ("F11.4_minority_lost", -1),
    # F12 extremes and outliers
    ("F12.1_exceed_rate_err", -1), ("F12.2_exceed_magnitude_err", -1),
    ("F12.3_spike_rate_err", -1), ("F12.4_block_max_ks", -1), ("F12.5_block_min_ks", -1),
]:
    _SPEC[_n] = _o
# F9.4 (diversity between seeds) is computed across seeds in the collect stage.


def _spec(prefix):
    return {k: v for k, v in _SPEC.items() if k.startswith(prefix)}


# ─────────────────────── helpers ───────────────────────────────────────────
def _clean(x):
    x = np.asarray(x, float)
    return x[np.isfinite(x)]


def _acf(x, max_lag):
    x = np.asarray(x, float)
    x = x - np.nanmean(x)
    v = np.nanmean(x * x)
    out = np.empty(max_lag + 1)
    for l in range(max_lag + 1):
        a, b = x[: len(x) - l], x[l:]
        m = np.isfinite(a) & np.isfinite(b)
        out[l] = np.mean(a[m] * b[m]) / v if m.sum() > 10 and v > 0 else np.nan
    return out


def _diff(x, k):
    x = np.asarray(x, float)
    return x[k:] - x[:-k]


def _ks(a, b):
    a, b = _clean(a), _clean(b)
    return float(stats.ks_2samp(a, b).statistic) if len(a) > 5 and len(b) > 5 else np.nan


def _windows(x, T, step=None, max_n=3000, rng=None):
    x = np.asarray(x, float)
    step = step or max(1, T // 4)
    idx = np.arange(0, len(x) - T + 1, step)
    W = np.stack([x[i:i + T] for i in idx]) if len(idx) else np.zeros((0, T))
    W = W[np.isfinite(W).all(axis=1)]
    if rng is not None and len(W) > max_n:
        W = W[np.sort(rng.choice(len(W), max_n, replace=False))]    # kept in time order
    return W


def _window_features(W):
    """16 hand-crafted statistics of each window (F6.2, F6.6, F9; METRICS.md, General conditions)."""
    d = np.diff(W, axis=1)
    mu, sd = W.mean(1), W.std(1) + 1e-12
    Z = (W - mu[:, None]) / sd[:, None]
    ac1 = (Z[:, 1:] * Z[:, :-1]).mean(1)
    ac24 = (Z[:, 24:] * Z[:, :-24]).mean(1) if W.shape[1] > 24 else ac1
    F = np.column_stack([
        mu, sd, stats.skew(W, axis=1), stats.kurtosis(W, axis=1), W.min(1), W.max(1),
        np.percentile(W, 10, axis=1), np.percentile(W, 90, axis=1), np.abs(d).mean(1), d.std(1),
        ac1, ac24, (np.diff(np.sign(Z), axis=1) != 0).mean(1), np.argmax(W, 1) / W.shape[1],
        np.argmin(W, 1) / W.shape[1], W[:, -1] - W[:, 0]])
    return np.nan_to_num(F, nan=0.0, posinf=0.0, neginf=0.0)      # constant window: skew / kurtosis NaN


def _torch_dev():
    import torch

    return "cuda" if torch.cuda.is_available() else "cpu"


def _cdist(A, B, dev=None, sq=False):
    """Pairwise distances on the GPU when available (float32)."""
    import torch

    dev = dev or _torch_dev()
    a = torch.as_tensor(np.asarray(A, np.float32), device=dev)
    b = torch.as_tensor(np.asarray(B, np.float32), device=dev)
    d = torch.cdist(a, b)
    return (d * d if sq else d)


def _mmd(X, Y, rng, n=1000):
    """Unbiased MMD² with an RBF kernel (median heuristic); diagonals excluded, so the estimate
    does not depend on the window counts. torch, GPU when available."""
    import torch

    if len(X) < 5 or len(Y) < 5:
        return np.nan
    X = X[rng.choice(len(X), min(n, len(X)), replace=False)]
    Y = Y[rng.choice(len(Y), min(n, len(Y)), replace=False)]
    Z = np.vstack([X, Y])
    d2 = _cdist(Z, Z, sq=True)
    gamma = 1.0 / (torch.median(d2[d2 > 0]) + 1e-12)
    Kz = torch.exp(-gamma * d2)
    nx, ny = len(X), len(Y)
    kxx, kyy, kxy = Kz[:nx, :nx], Kz[nx:, nx:], Kz[:nx, nx:]
    v = (kxx.sum() - kxx.diagonal().sum()) / (nx * (nx - 1)) + (kyy.sum() - kyy.diagonal().sum()) / (ny * (ny - 1)) \
        - 2 * kxy.mean()
    return float(v)


def _knn_radius(A, k):
    """Distance to the k-th nearest neighbour within A (self excluded)."""
    import torch

    d = _cdist(A, A)
    return torch.topk(d, k + 1, dim=1, largest=False).values[:, -1]


def _fid(A, B):
    from scipy.linalg import sqrtm

    if len(A) < 10 or len(B) < 10:
        return np.nan
    m1, m2 = A.mean(0), B.mean(0)
    c1, c2 = np.cov(A, rowvar=False), np.cov(B, rowvar=False)
    cs = sqrtm(c1 @ c2)
    cs = cs.real if np.iscomplexobj(cs) else cs
    return float(((m1 - m2) ** 2).sum() + np.trace(c1 + c2 - 2 * cs))


def _runs(mask):
    """Lengths of runs of True and gaps between run starts."""
    m = np.asarray(mask, bool).astype(int)
    dm = np.diff(np.concatenate([[0], m, [0]]))
    starts, ends = np.flatnonzero(dm == 1), np.flatnonzero(dm == -1)
    return ends - starts, np.diff(starts)


def _dfa_alpha(x, scales=(16, 32, 64, 128, 256)):
    x = _clean(x)
    y = np.cumsum(x - x.mean())
    F = []
    used = []
    for s in scales:
        n = len(y) // s
        if n < 4:
            continue
        segs = y[: n * s].reshape(n, s)
        t = np.arange(s)
        res = []
        for seg in segs:
            c = np.polyfit(t, seg, 1)
            res.append(np.sqrt(np.mean((seg - np.polyval(c, t)) ** 2)))
        F.append(np.mean(res))
        used.append(s)
    if len(F) < 2:
        return np.nan
    return float(np.polyfit(np.log(used), np.log(F), 1)[0])


def _hill(x, frac=0.05):
    x = np.sort(_clean(x))
    x = x - x.min() + 1e-9
    k = max(5, int(frac * len(x)))
    tail = x[-k:]
    return float(np.mean(np.log(tail / tail[0]))) if tail[0] > 0 else np.nan


def _psd(x, nperseg=512):
    x = _clean(x)
    f, P = signal.welch(x - x.mean(), nperseg=min(nperseg, len(x)))
    return f, P / P.sum()


def _peak(f, P, period):
    i = np.argmin(np.abs(f - 1.0 / period))
    return P[max(0, i - 1): i + 2].sum()


def _profile(x, how, by, fn):
    s = pd.Series(np.asarray(x, float)).groupby(np.asarray(how) % by if by == 24 else np.asarray(how))
    return s.agg(fn).reindex(range(by))


def _zscore(x, ref):
    return (np.asarray(x, float) - np.nanmean(ref)) / (np.nanstd(ref) + 1e-12)


def _gru_disc(Wr, Ws, epochs, seed):
    """F6.1 post-hoc discriminator (TimeGAN): |accuracy − 0.5| of a small GRU on held-out windows."""
    import torch

    torch.manual_seed(seed)
    n = min(len(Wr), len(Ws), 2000)
    if n < 20:
        return np.nan
    rng = np.random.default_rng(seed)
    # windows overlap (step T/4): split each class by time — first 80% train, last 20% test — so a
    # test window has no shifted copy in training (except at the one boundary)
    Wr, Ws = Wr[np.sort(rng.choice(len(Wr), n, replace=False))], Ws[np.sort(rng.choice(len(Ws), n, replace=False))]
    c = int(0.8 * n)
    tr = np.vstack([Wr[:c], Ws[:c]])
    te = np.vstack([Wr[c:], Ws[c:]])
    ytr, yte = np.r_[np.ones(c), np.zeros(c)], np.r_[np.ones(n - c), np.zeros(n - c)]
    perm = rng.permutation(len(tr))                       # shuffle only within training
    X = np.vstack([tr[perm], te])[..., None].astype(np.float32)
    y = np.r_[ytr[perm], yte].astype(np.float32)
    mu, sd = X[:len(tr)].mean(), X[:len(tr)].std() + 1e-9
    X = (X - mu) / sd
    cut = len(tr)

    class Net(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.g = torch.nn.GRU(1, 16, batch_first=True)
            self.o = torch.nn.Linear(16, 1)

        def forward(self, x):
            return self.o(self.g(x)[1][-1]).squeeze(-1)

    dev = _torch_dev()
    net = Net().to(dev)
    opt = torch.optim.Adam(net.parameters(), 1e-3)
    Xt, yt = torch.tensor(X[:cut], device=dev), torch.tensor(y[:cut], device=dev)
    for _ in range(epochs):
        for i in range(0, cut, 128):
            loss = torch.nn.functional.binary_cross_entropy_with_logits(net(Xt[i:i + 128]), yt[i:i + 128])
            opt.zero_grad()
            loss.backward()
            opt.step()
    with torch.no_grad():
        p = net(torch.tensor(X[cut:], device=dev)).cpu().numpy() > 0
    return float(abs((p == (y[cut:] > 0.5)).mean() - 0.5))


def _c2st(Fr, Fs, seed):
    from sklearn.ensemble import HistGradientBoostingClassifier
    from sklearn.metrics import roc_auc_score
    from sklearn.model_selection import cross_val_predict

    n = min(len(Fr), len(Fs))
    if n < 20:
        return np.nan
    rng = np.random.default_rng(seed)
    # rows in time order and unshuffled stratified folds: each fold is a contiguous time block of
    # both classes, so overlapping windows rarely sit on both sides of a split
    X = np.vstack([Fr[np.sort(rng.choice(len(Fr), n, replace=False))],
                   Fs[np.sort(rng.choice(len(Fs), n, replace=False))]])
    y = np.r_[np.ones(n), np.zeros(n)]
    from sklearn.model_selection import StratifiedKFold

    p = cross_val_predict(HistGradientBoostingClassifier(max_iter=100, random_state=seed), X, y,
                          cv=StratifiedKFold(5, shuffle=False), method="predict_proba")[:, 1]
    return float(roc_auc_score(y, p))


def _pred_score(train_like, real_test, lags=24):
    """F6.3: MAE of a one-step ridge fitted on `train_like`, evaluated on `real_test`."""
    from sklearn.linear_model import Ridge

    def xy(x):
        x = np.asarray(x, float)
        X = np.column_stack([x[i: len(x) - lags + i] for i in range(lags)])
        y = x[lags:]
        ok = np.isfinite(X).all(1) & np.isfinite(y)
        return X[ok], y[ok]

    Xa, ya = xy(train_like)
    Xb, yb = xy(real_test)
    if len(Xa) < 50 or len(Xb) < 50:
        return np.nan
    return float(np.mean(np.abs(Ridge(1.0).fit(Xa, ya).predict(Xb) - yb)))


def _prdc(real_f, fake_f, k=5):
    """Precision / recall / density / coverage (Naeem et al., 2020) on window features. torch."""
    if len(real_f) <= k or len(fake_f) <= k:
        return dict(precision=np.nan, recall=np.nan, density=np.nan, coverage=np.nan)
    mu, sd = real_f.mean(0), real_f.std(0) + 1e-12
    R, F = (real_f - mu) / sd, (fake_f - mu) / sd
    rr, ff = _knn_radius(R, k), _knn_radius(F, k)
    d_fr = _cdist(F, R)
    return dict(precision=float((d_fr < rr[None, :]).any(1).float().mean()),
                recall=float((d_fr.T < ff[None, :]).any(1).float().mean()),
                density=float((1.0 / k) * (d_fr < rr[None, :]).sum(1).float().mean()),
                coverage=float((d_fr.min(0).values < rr).float().mean()))


def _nn_min(Q, B):
    """Distance from each row of Q to its nearest row of B (chunked)."""
    out = [_cdist(Q[i:i + 2048], B).min(1).values.cpu().numpy() for i in range(0, len(Q), 2048)]
    return np.concatenate(out) if out else np.zeros(0)


def _seam_detect_auc(x, seams, o, seed):
    """F5.7: can a classifier tell a ±o snippet around a seam from one at a random position?"""
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import roc_auc_score
    from sklearn.model_selection import cross_val_predict

    x = np.asarray(x, float)
    seams = np.asarray([s for s in seams if o <= s < len(x) - o])
    if len(seams) < 10:
        return np.nan
    rng = np.random.default_rng(seed)
    seam_set = set()
    for s in seams:
        seam_set.update(range(s - o, s + o + 1))
    cand = np.array([i for i in range(o, len(x) - o) if i not in seam_set])
    neg = rng.choice(cand, min(len(cand), len(seams)), replace=False)

    def snip(i):
        w = x[i - o: i + o]
        return np.r_[np.diff(w), w.std()]

    X = np.vstack([snip(i) for i in np.r_[seams, neg]])
    y = np.r_[np.ones(len(seams)), np.zeros(len(neg))]
    ok = np.isfinite(X).all(1)
    if ok.sum() < 20 or len(np.unique(y[ok])) < 2:
        return np.nan
    p = cross_val_predict(LogisticRegression(max_iter=1000), X[ok], y[ok], cv=5, method="predict_proba")[:, 1]
    return float(roc_auc_score(y[ok], p))


def _cp_rate(x, pen_scale=3.0, max_len=40000):
    """Change points per 1000 points (PELT on 2-hour means of the first `max_len` points)."""
    try:
        import ruptures as rpt
    except Exception:
        return np.nan, np.array([])
    x = _clean(x)[:max_len]
    if len(x) < 200:
        return np.nan, np.array([])
    # downsample for speed: PELT on 2-hour means
    y = x[: len(x) // 2 * 2].reshape(-1, 2).mean(1)
    pen = pen_scale * np.log(len(y)) * np.var(np.diff(y))
    bk = np.asarray(rpt.Pelt(model="l2", min_size=6, jump=3).fit(y).predict(pen=pen)[:-1]) * 2
    return 1000.0 * len(bk) / len(x), bk


def _regime_durations(x, ref, seed):
    try:
        from hmmlearn.hmm import GaussianHMM
    except Exception:
        return None
    r = _clean(np.diff(ref))[:, None]
    m = GaussianHMM(n_components=2, covariance_type="diag", n_iter=50, random_state=seed).fit(r)
    s = m.predict(_clean(np.diff(x))[:, None])
    lens, _ = _runs(s == np.argmax(m.covars_.ravel()))
    return lens



# ─────────────────────── context ───────────────────────────────────────────
@dataclass
class FidelityContext:
    x: np.ndarray                 # synthetic series, real units
    how: np.ndarray
    seams: np.ndarray
    ref: np.ndarray               # real reference (val)
    ref_how: np.ndarray
    train: np.ndarray             # real train
    train_how: np.ndarray
    T: int
    seed: int = 0
    disc_epochs: int = 30
    edge_overlap: int = 5
    target_task: str = "clf_up_h24_q90"
    params: dict = field(default_factory=dict)
    target_params: dict | None = None             # exogenous parameters of target_task (thresholds)
    class_tasks: dict | None = None               # {classification task: its exogenous parameters} for F11

    def __post_init__(self):
        self.x, self.ref, self.train = (np.asarray(a, float) for a in (self.x, self.ref, self.train))
        self.how, self.ref_how = np.asarray(self.how), np.asarray(self.ref_how)
        self.rng = np.random.default_rng(self.seed)

    @cached_property
    def xc(self):
        return _clean(self.x)

    @cached_property
    def rc(self):
        return _clean(self.ref)

    @cached_property
    def sd(self):
        return np.std(self.rc) + 1e-12

    @cached_property
    def sv(self):
        s = np.asarray(self.seams, int)
        return s[(s > 0) & (s < len(self.x))]

    @cached_property
    def zx(self):
        return _zscore(self.x, self.ref)

    @cached_property
    def zr(self):
        return _zscore(self.ref, self.ref)

    @cached_property
    def windows(self):
        rng = np.random.default_rng(self.seed + 1)
        T = self.T
        return (_windows(self.zx, T, rng=rng), _windows(self.zr, T, rng=rng),
                _windows(self.zx, 2 * T, rng=rng), _windows(self.zr, 2 * T, rng=rng))

    @cached_property
    def features(self):
        Wx, Wr = self.windows[:2]
        return _window_features(Wx), _window_features(Wr)


@register_fidelity_group("F1_marginal", _spec("F1."))
def F1_marginal(ctx):
    xc, rc, sd = ctx.xc, ctx.rc, ctx.sd
    out: dict = {}
    out["F1.1_ks"] = _ks(xc, rc)
    out["F1.2_w1"] = float(stats.wasserstein_distance(xc, rc) / (np.std(rc) + 1e-12))
    try:
        out["F1.3_ad"] = float(stats.anderson_ksamp([xc, rc]).statistic)
    except Exception:
        out["F1.3_ad"] = np.nan
    qs = np.linspace(0.01, 0.99, 99)
    qx, qr = np.quantile(xc, qs), np.quantile(rc, qs)
    out["F1.4_qq_corr"] = float(np.corrcoef(qx, qr)[0, 1])
    sd = np.std(rc) + 1e-12
    pq = np.array([0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99])
    qe = np.abs(np.quantile(xc, pq) - np.quantile(rc, pq)) / sd
    out["F1.5_quantile_err"], out["F1.5_q01_err"], out["F1.5_q99_err"] = float(qe.mean()), float(qe[0]), float(qe[-1])
    out["F1.6_mean_err"] = float(abs(xc.mean() - rc.mean()) / sd)
    out["F1.6_std_err"] = float(abs(np.log((xc.std() + 1e-12) / sd)))
    out["F1.6_skew_err"] = float(abs(stats.skew(xc) - stats.skew(rc)))
    out["F1.6_kurt_err"] = float(abs(stats.kurtosis(xc) - stats.kurtosis(rc)))
    out["F1.7_out_of_range"] = float(((xc < rc.min()) | (xc > rc.max())).mean())
    bins = np.quantile(rc, np.linspace(0, 1, 51))
    bins = np.unique(bins)
    hx, _ = np.histogram(xc, bins)
    hr, _ = np.histogram(rc, bins)
    out["F1.8_coverage"] = float((hx[hr > 0] > 0).mean())
    from scipy.spatial.distance import jensenshannon

    out["F1.9_js"] = float(jensenshannon(hx + 1e-9, hr + 1e-9))
    out["F1.10_hill_err"] = float(abs(_hill(xc) - _hill(rc)))

    return out


@register_fidelity_group("F2_increments", _spec("F2."))
def F2_increments(ctx):
    x, ref = ctx.x, ctx.ref
    out: dict = {}
    for k in (1, 6, 24, 168):
        out[f"F2.1_ks_d{k}"] = _ks(_diff(x, k), _diff(ref, k))
    dr24 = _clean(_diff(ref, 24))
    out["F2.1_w1_d24"] = float(stats.wasserstein_distance(_clean(_diff(x, 24)), dr24) / (dr24.std() + 1e-12))
    for k in (1, 24):
        out[f"F2.2_vol_ratio_err_d{k}"] = float(abs(np.log((np.nanstd(_diff(x, k)) + 1e-12) /
                                                         (np.nanstd(_diff(ref, k)) + 1e-12))))
    d1x, d1r = _clean(_diff(x, 1)), _clean(_diff(ref, 1))
    out["F2.3_up_share_err"] = float(abs((d1x > 0).mean() - (d1r > 0).mean()))
    thr99 = np.quantile(np.abs(d1r), 0.99)
    out["F2.4_big_jump_share_err"] = float(abs((np.abs(d1x) > thr99).mean() - 0.01))

    return out


@register_fidelity_group("F3_dependence", _spec("F3."))
def F3_dependence(ctx):
    x, ref, xc, rc, T = ctx.x, ctx.ref, ctx.xc, ctx.rc, ctx.T
    how, ref_how = ctx.how, ctx.ref_how
    out: dict = {}
    acf_x, acf_r = _acf(x, 3 * T), _acf(ref, 3 * T)
    out["F3.1_acf_in_window"] = float(np.nanmean(np.abs(acf_x[1:T] - acf_r[1:T])))
    out["F3.2_acf_beyond_window"] = float(np.nanmean(np.abs(acf_x[T:3 * T + 1] - acf_r[T:3 * T + 1])))
    try:
        from statsmodels.tsa.stattools import pacf

        out["F3.3_pacf"] = float(np.mean(np.abs(pacf(xc, 48)[1:] - pacf(rc, 48)[1:])))
    except Exception:
        out["F3.3_pacf"] = np.nan
    for tag, fx in (("abs", np.abs), ("sq", np.square)):
        a1, a2 = _acf(fx(_diff(x, 1)), 48), _acf(fx(_diff(ref, 1)), 48)
        out[f"F3.4_acf_{tag}_d"] = float(np.nanmean(np.abs(a1[1:] - a2[1:])))
    f1, P1 = _psd(xc)
    f2, P2 = _psd(rc)
    n = min(len(P1), len(P2))
    out["F3.5_log_psd"] = float(np.mean(np.abs(np.log10(P1[1:n] + 1e-12) - np.log10(P2[1:n] + 1e-12))))
    out["F3.6_peak24_err"] = float(abs(_peak(f1, P1, 24) - _peak(f2, P2, 24)))
    out["F3.6_peak168_err"] = float(abs(_peak(f1, P1, 168) - _peak(f2, P2, 168)))
    out["F3.7_dfa_err"] = float(abs(_dfa_alpha(xc) - _dfa_alpha(rc)))
    a = 2 * np.pi * np.asarray(how) / 168
    ar = 2 * np.pi * np.asarray(ref_how) / 168

    def cal_corr(v, ang):
        m = np.isfinite(v)
        return np.array([np.corrcoef(v[m], np.sin(ang[m]))[0, 1], np.corrcoef(v[m], np.cos(ang[m]))[0, 1]])

    out["F3.8_calendar_corr_err"] = float(np.abs(cal_corr(x, a) - cal_corr(ref, ar)).mean())

    return out


@register_fidelity_group("F4_seasonality", _spec("F4."))
def F4_seasonality(ctx):
    x, ref = ctx.x, ctx.ref
    how, ref_how, sv = ctx.how, ctx.ref_how, ctx.sv
    out: dict = {}
    out["F4.1_how_mean"] = float(np.nanmean(np.abs(_profile(_zscore(x, ref), how, 168, "mean") -
                                                   _profile(_zscore(ref, ref), ref_how, 168, "mean"))))
    out["F4.2_how_std"] = float(np.nanmean(np.abs(_profile(_zscore(x, ref), how, 168, "std") -
                                                  _profile(_zscore(ref, ref), ref_how, 168, "std"))))
    out["F4.3_hod_mean"] = float(np.nanmean(np.abs(_profile(_zscore(x, ref), how, 24, "mean") -
                                                   _profile(_zscore(ref, ref), ref_how, 24, "mean"))))
    step_ok = (np.diff(how) % 168) == 1
    out["F4.4_calendar_continuity"] = float(step_ok.mean())
    out["F4.5_calendar_seam_breaks"] = float((~step_ok[sv - 1]).mean()) if len(sv) else np.nan

    return out


@register_fidelity_group("F5_seams", _spec("F5."))
def F5_seams(ctx):
    x, ref, rng = ctx.x, ctx.ref, ctx.rng
    sv, seed, edge_overlap = ctx.sv, ctx.seed, ctx.edge_overlap
    out: dict = {}
    d1 = np.diff(x)
    if len(sv):
        seam_d = d1[sv - 1]
        inside = np.delete(d1, sv - 1)
        out["F5.1_ks_seam_vs_real"] = _ks(seam_d, _diff(ref, 1))
        out["F5.2_ks_seam_vs_inside"] = _ks(seam_d, inside)
        z = np.abs(seam_d) / (np.nanstd(_diff(ref, 1)) + 1e-12)
        out["F5.3_seam_z_mean"], out["F5.3_seam_z_p95"] = float(np.nanmean(z)), float(np.nanpercentile(z, 95))
        w = 24
        loc = [np.corrcoef(x[s - w: s + w - 1], x[s - w + 1: s + w])[0, 1] for s in sv if w <= s < len(x) - w]
        rnd = rng.integers(w, len(x) - w, size=max(50, len(loc)))
        loc_r = [np.corrcoef(x[s - w: s + w - 1], x[s - w + 1: s + w])[0, 1] for s in rnd]
        out["F5.4_seam_local_acf"] = float(abs(np.nanmean(loc) - np.nanmean(loc_r)))
        out["F5.7_seam_detect_auc_dev"] = abs(_seam_detect_auc(x, sv, max(edge_overlap, 6), seed) - 0.5)
    else:
        for k in ("F5.1_ks_seam_vs_real", "F5.2_ks_seam_vs_inside", "F5.3_seam_z_mean", "F5.3_seam_z_p95",
                  "F5.4_seam_local_acf", "F5.7_seam_detect_auc_dev"):
            out[k] = np.nan
    rate_x, bk = _cp_rate(x)
    rate_r, _ = _cp_rate(ref)
    out["F5.5_cp_rate_err"] = float(abs(rate_x - rate_r)) if np.isfinite(rate_x) and np.isfinite(rate_r) else np.nan
    if len(bk) and len(sv):
        out["F5.6_cp_at_seams"] = float(np.mean([np.min(np.abs(sv - b)) <= 3 for b in bk]))
    else:
        out["F5.6_cp_at_seams"] = np.nan

    return out


@register_fidelity_group("F6_windows", _spec("F6."))
def F6_windows(ctx):
    x, ref, rng = ctx.x, ctx.ref, ctx.rng
    seed, disc_epochs = ctx.seed, ctx.disc_epochs
    Wx, Wr, Wx2, Wr2 = ctx.windows
    Fx, Fr = ctx.features
    out: dict = {}
    out["F6.1_disc_score"] = _gru_disc(Wr, Wx, disc_epochs, seed)
    out["F6.2_c2st_auc_dev"] = abs(_c2st(Fr, Fx, seed) - 0.5)         # 0 = indistinguishable
    tr_half = len(ref) // 2
    real_ps = _pred_score(ref[:tr_half], ref[tr_half:])
    out["F6.3_pred_score_err"] = float(abs(_pred_score(x, ref[tr_half:]) - real_ps) / (np.nanstd(ref) + 1e-12))
    out["F6.4_mmd"] = _mmd(Wx[:, ::4], Wr[:, ::4], rng)
    out["F6.4_mmd_2T"] = _mmd(Wx2[:, ::8], Wr2[:, ::8], rng)
    out["F6.6_feature_fid"] = _fid(Fx, Fr)
    if len(Wr) > 10 and len(Wx) > 10:
        half = len(Wr) // 2
        ratio = np.median(_nn_min(Wx, Wr[:half])) / (np.median(_nn_min(Wr[half:], Wr[:half])) + 1e-12)
        out["F6.8_nn_dist_logratio"] = float(abs(np.log(ratio + 1e-12)))   # 0 = as close as real; deviation in either direction counts
    else:
        out["F6.8_nn_dist_logratio"] = np.nan

    return out


@register_fidelity_group("F7_long_structure", _spec("F7."))
def F7_long_structure(ctx):
    x, ref, xc, rc, sd = ctx.x, ctx.ref, ctx.xc, ctx.rc, ctx.sd
    zx, zr, seed = ctx.zx, ctx.zr, ctx.seed
    out: dict = {}
    for w in (168, 720):
        rmx, rmr = pd.Series(zx).rolling(w).mean(), pd.Series(zr).rolling(w).mean()
        rsx, rsr = pd.Series(zx).rolling(w).std(), pd.Series(zr).rolling(w).std()
        out.setdefault("F7.1_roll_mean_ks", 0.0)
        out.setdefault("F7.2_roll_std_ks", 0.0)
        out["F7.1_roll_mean_ks"] += _ks(rmx, rmr) / 2
        out["F7.2_roll_std_ks"] += _ks(rsx, rsr) / 2
    errs = []
    for q in (0.1, 0.5, 0.9):
        lvl = np.quantile(rc, q)
        cx = np.mean(np.diff(np.sign(xc - lvl)) != 0)
        cr = np.mean(np.diff(np.sign(rc - lvl)) != 0)
        errs.append(abs(np.log((cx + 1e-6) / (cr + 1e-6))))
    out["F7.3_crossings_err"] = float(np.mean(errs))
    exc = []
    for q, up in ((0.9, True), (0.1, False)):
        lvl = np.quantile(rc, q)
        lx, _ = _runs(xc > lvl if up else xc < lvl)
        lr, _ = _runs(rc > lvl if up else rc < lvl)
        exc.append(_ks(lx, lr))
    out["F7.4_excursion_ks"] = float(np.nanmean(exc))
    # drawdown from the rolling weekly max: the all-time max of a stationary series is hit early
    ddx = pd.Series(zx).rolling(168).max() - zx
    ddr = pd.Series(zr).rolling(168).max() - zr
    out["F7.5_drawdown_ks"] = _ks(ddx, ddr)
    # slope per week in units of the real std: comparable across series of different length
    tx = np.polyfit(np.arange(len(xc)), xc, 1)[0] * 168 / sd
    tr = np.polyfit(np.arange(len(rc)), rc, 1)[0] * 168 / sd
    out["F7.6_trend_err"] = float(abs(tx - tr))
    wl = lambda v: pd.Series(v).groupby(np.arange(len(v)) // 168).mean().std()
    out["F7.6_weekly_level_std_err"] = float(abs(np.log((wl(zx) + 1e-9) / (wl(zr) + 1e-9))))
    try:
        dx, dr = _regime_durations(x, ref, seed), _regime_durations(ref, ref, seed)
        out["F7.7_regime_dur_err"] = float(abs(np.log((np.mean(dx) + 1e-9) / (np.mean(dr) + 1e-9)))) if dx is not None else np.nan
    except Exception:
        out["F7.7_regime_dur_err"] = np.nan

    return out


@register_fidelity_group("F8_target", _spec("F8."))
def F8_target(ctx):
    x, ref = ctx.x, ctx.ref
    how, ref_how = ctx.how, ctx.ref_how
    out: dict = {}
    task = R.tasks.get(ctx.target_task)
    if ctx.target_params is None:
        raise ValueError("F8 needs the exogenous target parameters (fidelity(..., target_params=...))")
    thr = ctx.target_params
    yx, yr = labels(task, x, thr), labels(task, ref, thr)
    out["F8.1_class_tvd"] = float(abs(np.nanmean(yx) - np.nanmean(yr)))
    ex, gx = _runs(np.nan_to_num(yx) > 0.5)
    er, gr = _runs(np.nan_to_num(yr) > 0.5)
    out["F8.2_event_dur_ks"], out["F8.3_interarrival_ks"] = _ks(ex, er), _ks(gx, gr)
    px = pd.Series(yx).groupby(np.asarray(how)).mean().reindex(range(168))
    pr = pd.Series(yr).groupby(np.asarray(ref_how)).mean().reindex(range(168))
    out["F8.4_event_by_how"] = float(np.nanmean(np.abs(px - pr)))
    errs = []
    for k in (1, 24, 168):
        fx_, fr_ = np.r_[np.full(k, np.nan), _diff(x, k)], np.r_[np.full(k, np.nan), _diff(ref, k)]
        edges = np.nanquantile(fr_, [0.2, 0.4, 0.6, 0.8])
        bx, br = np.digitize(fx_, edges), np.digitize(fr_, edges)
        for b in range(5):
            mx, mr = (bx == b) & np.isfinite(yx) & np.isfinite(fx_), (br == b) & np.isfinite(yr) & np.isfinite(fr_)
            if mx.sum() > 20 and mr.sum() > 20:
                errs.append(abs(yx[mx].mean() - yr[mr].mean()))
    out["F8.5_cond_event_err"] = float(np.mean(errs)) if errs else np.nan
    ks_c = []
    edges = np.nanquantile(ref, [0.2, 0.4, 0.6, 0.8])
    fx_, fr_ = x[24:] - x[:-24], ref[24:] - ref[:-24]
    bx, br = np.digitize(x[:-24], edges), np.digitize(ref[:-24], edges)
    for b in range(5):
        ks_c.append(_ks(fx_[bx == b], fr_[br == b]))
    out["F8.6_cond_future_ks"] = float(np.nanmean(ks_c))

    return out


@register_fidelity_group("F9_coverage", _spec("F9."))
def F9_coverage(ctx):
    Fx, Fr = ctx.features
    out: dict = {}
    pr_ = _prdc(Fr, Fx)
    out["F9.1_precision"], out["F9.1_recall"] = float(pr_["precision"]), float(pr_["recall"])
    out["F9.2_density_logdev"] = float(abs(np.log(pr_["density"] + 1e-6)))   # 0 at density 1 (as dense as real)
    out["F9.2_coverage"] = float(pr_["coverage"])

    return out


@register_fidelity_group("F10_memorisation", _spec("F10."), primary_only=True)
def F10_memorisation(ctx):
    train, ref, T = ctx.train, ctx.ref, ctx.T
    rng = np.random.default_rng(ctx.seed + 2)
    Wx, Wr = ctx.windows[:2]
    out: dict = {}
    zt = _zscore(train, ref)
    Wt = _windows(zt, T, rng=rng)
    if len(Wt) > 10 and len(Wx) > 10 and len(Wr) > 10:
        dcr_x = _nn_min(Wx[:, ::2], Wt[:, ::2])
        dcr_r = _nn_min(Wr[:, ::2], Wt[:, ::2])
        # 0 = synthetic as far from train as unseen real; < 1 copies train, > 1 is off-distribution
        out["F10.1_dcr_logratio"] = float(abs(np.log(np.median(dcr_x) / (np.median(dcr_r) + 1e-12) + 1e-12)))
        out["F10.2_near_copy_share"] = float((dcr_x < np.percentile(dcr_r, 5)).mean())
    else:
        out["F10.1_dcr_logratio"] = out["F10.2_near_copy_share"] = np.nan
    return out


RARE_TAIL = 0.05          # a classification task is a rare event when its tail probability (min(q, 1 − q)) ≤ this


def _is_rare(task) -> bool:
    return task.q is not None and min(task.q, 1 - task.q) <= RARE_TAIL + 1e-9


@register_fidelity_group("F11_class_balance", _spec("F11."))
def F11_class_balance(ctx):
    """Class shares of the synthetic series against the reference for every classification task
    (`class_tasks`): |log(share_synth / share_real)| — relative, so a rare class (1%) counts as much
    as a common one — over all binary tasks and over the rare ones; TVD of the class distribution of
    multiclass tasks; share of binary tasks whose positive class is absent from the synthetic series."""
    out = {k: np.nan for k in _spec("F11.")}
    if not ctx.class_tasks:
        return out
    eps = 1e-4
    lr, rare, tvd, lost = [], [], [], []
    for name, prm in ctx.class_tasks.items():
        task = R.tasks.get(name)
        yx, yr = labels(task, ctx.x, prm), labels(task, ctx.ref, prm)
        yx, yr = yx[np.isfinite(yx)], yr[np.isfinite(yr)]
        if not len(yx) or not len(yr):
            continue
        if task.kind == "clf":
            sx, sr = float(yx.mean()), float(yr.mean())
            if sr <= 0:
                continue
            e = abs(np.log((sx + eps) / (sr + eps)))
            lr.append(e)
            lost.append(float(sx == 0))
            if _is_rare(task):
                rare.append(e)
        elif task.kind == "mc":
            C = task.n_classes
            px = np.bincount(yx.astype(int), minlength=C)[:C] / len(yx)
            pr = np.bincount(yr.astype(int), minlength=C)[:C] / len(yr)
            tvd.append(0.5 * float(np.abs(px - pr).sum()))
    for k, v in (("F11.1_class_share_logratio", lr), ("F11.2_rare_share_logratio", rare),
                 ("F11.3_multiclass_tvd", tvd), ("F11.4_minority_lost", lost)):
        out[k] = float(np.mean(v)) if v else np.nan
    return out


@register_fidelity_group("F12_extremes", _spec("F12."))
def F12_extremes(ctx):
    """Extremes and outliers against the reference: rate of points beyond the real 0.5 / 99.5%
    quantiles (|log ratio|); their mean excess over the threshold (in real std); rate of local spikes
    — |x − rolling median(25)| above the real 99.5% of the same residual (|log ratio|); KS of the
    weekly (168 h) block maxima and minima — the extreme-value view of the tails."""
    xc, rc, sd = ctx.xc, ctx.rc, ctx.sd
    out: dict = {}
    lo, hi = np.quantile(rc, [0.005, 0.995])
    rate = lambda v: ((v < lo) | (v > hi)).mean()
    out["F12.1_exceed_rate_err"] = float(abs(np.log((rate(xc) + 1e-4) / (rate(rc) + 1e-4))))

    def excess(v):
        e = np.r_[v[v > hi] - hi, lo - v[v < lo]]
        return float(e.mean()) / sd if len(e) else 0.0

    out["F12.2_exceed_magnitude_err"] = abs(excess(xc) - excess(rc))
    res = lambda v: np.abs(v - pd.Series(v).rolling(25, center=True, min_periods=5).median().to_numpy())
    rx, rr = _clean(res(ctx.x)), _clean(res(ctx.ref))
    thr = np.quantile(rr, 0.995)
    out["F12.3_spike_rate_err"] = float(abs(np.log(((rx > thr).mean() + 1e-4) / ((rr > thr).mean() + 1e-4))))
    blocks = lambda v, fn: pd.Series(v).groupby(np.arange(len(v)) // 168).agg(fn).dropna().to_numpy()
    out["F12.4_block_max_ks"] = _ks(blocks(ctx.x, "max"), blocks(ctx.ref, "max"))
    out["F12.5_block_min_ks"] = _ks(blocks(ctx.x, "min"), blocks(ctx.ref, "min"))
    return out


# ─────────────────────── main entry ────────────────────────────────────────
def fidelity(x, how, seams, ref, ref_how, train, train_how, *, T: int, seed: int = 0, disc_epochs: int = 30,
             edge_overlap: int = 5, target_task: str = "clf_up_h24_q90", groups=None, params=None,
             target_params: dict | None = None, extra_refs: dict | None = None,
             class_tasks: dict | None = None, group_params: dict | None = None,
             errors: list | None = None) -> dict:
    """All registered fidelity metrics (or the `groups` given) of one series against `ref`, and
    against every `extra_refs` part {name: (values, how)} under the suffix `@<name>`. `group_params`:
    {group: params} on top of `params` (`ctx.params`). With `errors` (a list), a failing group does not stop
    the others: its metrics are NaN and the error is appended, as is a returned metric without an orientation
    (not in the group's spec — the analysis ignores it), as {group, ref, error, failed}; without it, a failing
    group raises."""
    import zlib

    from .progress import bar

    out: dict[str, float] = {}
    names = list(groups or R.fidelity_metrics.names())
    passes = [("", ref, ref_how, names)]
    passes += [(f"@{r}", v, h, [g for g in names if g not in PRIMARY_ONLY]) for r, (v, h) in (extra_refs or {}).items()]
    # one bar per series over every (reference, group), the reference in its label
    with bar(total=sum(len(gs) for *_, gs in passes), desc="metric groups", leave=False, unit="group") as pb:
        for suffix, rv, rh, gs in passes:
            ctx = FidelityContext(x, how, seams, rv, rh, train, train_how, T, seed, disc_epochs, edge_overlap,
                                  target_task, params or {}, target_params, class_tasks)
            pb.set_description(f"metric groups vs {suffix[1:] or 'primary'}")
            for name in gs:
                # own RNG per group: results do not depend on which other groups ran, or in which order
                ctx.rng = np.random.default_rng([seed, zlib.crc32(name.encode())])
                ctx.params = {**(params or {}), **(group_params or {}).get(name, {})}
                if errors is None:
                    res = R.fidelity_metrics.get(name)(ctx)
                else:
                    try:
                        res = R.fidelity_metrics.get(name)(ctx)
                    except Exception as e:      # noqa: BLE001 — one group must not lose the unit
                        errors.append(dict(group=name, ref=suffix, error=e, failed=True))
                        res = {k: np.nan for k, g in GROUP_OF.items() if g == name and "@" not in k}
                    odd = [k for k in res if k not in ORIENT]
                    if odd:
                        errors.append(dict(group=name, ref=suffix, failed=False, error=ValueError(
                            f"metrics without an orientation (not in the group's spec, ignored by the analysis): "
                            f"{', '.join(odd)}")))
                out.update({k + suffix: (float(v) if v is not None else np.nan) for k, v in res.items()})
                pb.update()
    return out
