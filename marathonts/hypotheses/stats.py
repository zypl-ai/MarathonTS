"""Statistical tests of the hypothesis part.

Conventions: a paired difference `d` is oriented so that **d > 0 means the method under study is better**.
Seeds are the replication unit inside a dataset; datasets are the unit across datasets.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats


# ─────────────────────── multiplicity ──────────────────────────────────────
def holm(p):
    p = np.asarray(p, float)
    out = np.full_like(p, np.nan)
    ok = np.isfinite(p)
    q = p[ok]
    order = np.argsort(q)
    adj = np.maximum.accumulate((len(q) - np.arange(len(q))) * q[order])
    res = np.empty_like(q)
    res[order] = np.minimum(adj, 1)
    out[ok] = res
    return out


def bh(p):
    p = np.asarray(p, float)
    out = np.full_like(p, np.nan)
    ok = np.isfinite(p)
    q = p[ok]
    n = len(q)
    order = np.argsort(q)
    adj = q[order] * n / (np.arange(n) + 1)
    adj = np.minimum.accumulate(adj[::-1])[::-1]
    res = np.empty_like(q)
    res[order] = np.minimum(adj, 1)
    out[ok] = res
    return out


# ─────────────────────── paired location tests ─────────────────────────────
def wilcoxon(d, alternative="two-sided"):
    d = np.asarray(d, float)
    d = d[np.isfinite(d)]
    if len(d) < 3 or np.all(d == 0):          # exact zeros only: tiny-scale metrics keep their test
        return np.nan
    return float(wilcoxon_rows(d[None], alternative)[0])


def _wilcoxon_scipy(D, alternative):
    try:
        return stats.wilcoxon(D, alternative=alternative, zero_method="zsplit", axis=1).pvalue
    except ValueError:                          # one bad row must not void the batch
        if len(D) == 1:
            return np.full(1, np.nan)
        return np.concatenate([_wilcoxon_scipy(r[None], alternative) for r in D])


_PERM_N = 13                                    # scipy: ties or zeros and n ≤ 13 → exact permutation test


def _wilcoxon_perm(D, alternative):
    """scipy's exact sign-flip permutation test of the zsplit statistic (rows with ties or zeros,
    n ≤ 13) — all 2ⁿ flips as one matrix product instead of scipy's ~50 ms per row. The statistic is a
    sum of half-integer ranks, exact in float, so the p-values are scipy's to the bit."""
    n = D.shape[1]
    r = stats.rankdata(np.abs(D), axis=1)
    rp, rm = r * (D > 0), r * (D < 0)
    obs = rp.sum(1) + (r * (D == 0)).sum(1) / 2
    flip = ((np.arange(2 ** n)[:, None] >> np.arange(n)) & 1).astype(float)    # 2ⁿ × n
    gam = np.abs(np.finfo(float).eps * 100 * obs)
    out = np.empty(len(D))
    step = max(1, _CHUNK // 2 ** n)
    for i in range(0, len(D), step):
        s = slice(i, i + step)
        null = (1 - flip) @ rp[s].T + flip @ rm[s].T + (obs[s] - rp[s].sum(1))     # 2ⁿ × rows
        lo, hi = (null <= obs[s] + gam[s]).mean(0), (null >= obs[s] - gam[s]).mean(0)
        out[s] = {"less": lo, "greater": hi}.get(alternative, np.minimum(lo, hi) * 2)
    return np.clip(out, 0, 1)


def wilcoxon_rows(D, alternative="two-sided"):
    """`wilcoxon` of every row of a matrix of finite values. scipy picks the exact, permutation or
    normal method once for the whole batch — exact only when no row has ties or zeros — so rows with
    and without them are sent separately, as one by one; the permutation test is computed here."""
    D = np.asarray(D, float)
    out = np.full(len(D), np.nan)
    if D.ndim != 2 or D.shape[1] < 3 or not len(D):
        return out
    live = ~np.all(D == 0, axis=1)
    rough = (D == 0).any(1) | (np.diff(np.sort(np.abs(D), axis=1), axis=1) == 0).any(1)
    for sel in (live & ~rough, live & rough):
        if sel.any():
            perm = D.shape[1] <= _PERM_N and rough[sel].all()
            out[sel] = _wilcoxon_perm(D[sel], alternative) if perm else _wilcoxon_scipy(D[sel], alternative)
    return out


def tost_rows(D, margin):
    """`tost` of every row of a matrix of finite values, a margin per row."""
    D = np.asarray(D, float)
    mg = np.broadcast_to(np.asarray(margin, float), (len(D),))
    out = np.full(len(D), np.nan)
    ok = np.isfinite(mg) & (mg > 0)
    if D.ndim != 2 or D.shape[1] < 3 or not ok.any():
        return out
    lo = wilcoxon_rows(D[ok] + mg[ok, None], "greater")
    hi = wilcoxon_rows(D[ok] - mg[ok, None], "less")
    out[ok] = np.where(np.isnan(lo) | np.isnan(hi), np.nan, np.maximum(lo, hi))
    return out


def hodges_lehmann_rows(D):
    """`hodges_lehmann` of every row of a matrix of finite values."""
    D = np.asarray(D, float)
    if D.ndim != 2 or not D.shape[1]:
        return np.full(len(D), np.nan)
    i, j = np.triu_indices(D.shape[1])
    return np.median((D[:, i] + D[:, j]) / 2, axis=1)


def by_rows(rows, fn_rows, fn_one, *args):
    """Row-wise statistic over a ragged list of 1-D arrays: arrays of one length with only finite
    values go to `fn_rows` as one matrix, the rest to `fn_one` one by one; `args` — one value per row."""
    out = np.full(len(rows), np.nan)
    args = [np.asarray(a) for a in args]
    buckets: dict = {}
    for i, r in enumerate(rows):
        if len(r) and np.isfinite(r).all():
            buckets.setdefault(len(r), []).append(i)
        else:
            out[i] = fn_one(r, *(a[i] for a in args))
    for ix in buckets.values():
        ix = np.asarray(ix)
        out[ix] = fn_rows(np.stack([rows[i] for i in ix]), *(a[ix] for a in args))
    return out


def sign_test(d):
    d = np.asarray(d, float)
    d = d[np.isfinite(d) & (d != 0)]
    if not len(d):
        return np.nan
    return float(stats.binomtest(int((d > 0).sum()), len(d)).pvalue)


def hodges_lehmann(d):
    d = np.asarray(d, float)
    d = d[np.isfinite(d)]
    if not len(d):
        return np.nan
    w = (d[:, None] + d[None, :]) / 2
    return float(np.median(w[np.triu_indices(len(d))]))


def rank_biserial(d):
    d = np.asarray(d, float)
    d = d[np.isfinite(d) & (d != 0)]
    if not len(d):
        return np.nan
    r = stats.rankdata(np.abs(d))
    return float((r[d > 0].sum() - r[d < 0].sum()) / r.sum())


def tost(d, margin):
    """Equivalence of the paired difference to 0 within ±margin: two one-sided Wilcoxon tests.
    Returns the TOST p-value (max of the two)."""
    d = np.asarray(d, float)
    d = d[np.isfinite(d)]
    if len(d) < 3 or not np.isfinite(margin) or margin <= 0:
        return np.nan
    p_lo = wilcoxon(d + margin, "greater")
    p_hi = wilcoxon(d - margin, "less")
    if np.isnan(p_lo) or np.isnan(p_hi):
        return np.nan
    return float(max(p_lo, p_hi))


def verdict(p_better, p_worse, p_equiv, effect, margin, alpha=0.05):
    """better / worse / same / inconclusive. Superiority needs significance *and* an effect
    above the noise margin; equivalence needs TOST. Both directions can be concluded, so each
    one-sided p is compared with alpha / 2 (a two-sided test at alpha); TOST — with alpha."""
    big = np.isfinite(margin) and margin > 0 and abs(effect) > margin
    if np.isfinite(p_better) and p_better < alpha / 2 and effect > 0 and big:
        return "better"
    if np.isfinite(p_worse) and p_worse < alpha / 2 and effect < 0 and big:
        return "worse"
    if np.isfinite(p_equiv) and p_equiv < alpha:
        return "same"
    return "inconclusive"


# ─────────────────────── bootstrap ─────────────────────────────────────────
_CHUNK = 4_000_000                              # values drawn per bootstrap chunk (bounds memory)


def padded(groups):
    """Ragged 1-D arrays → (matrix padded with NaN, lengths)."""
    sizes = np.array([len(g) for g in groups])
    M = np.full((len(groups), max(1, sizes.max())), np.nan)
    for i, g in enumerate(groups):
        M[i, : len(g)] = g
    return M, sizes


def resample_groups(rng, sizes, n_boot, width=1):
    """Indices of a two-level bootstrap in chunks: (pick (b, G) — groups with replacement,
    idx (b, G, max size) — members of each picked group with replacement, valid where < its size);
    `width` — values per member (bounds the chunk)."""
    G, mx = len(sizes), int(sizes.max())
    step = max(1, _CHUNK // max(1, G * mx * width))
    for b0 in range(0, n_boot, step):
        b = min(step, n_boot - b0)
        pick = rng.integers(0, G, (b, G))
        n = sizes[pick]
        idx = rng.integers(0, n[..., None], (b, G, mx))
        yield pick, idx, np.arange(mx) < n[..., None]


CI_STAT = "mean"                # Config.ci_stat: "mean" (pre-specified) or "median" (supplementary) over datasets


def hier_bootstrap_ci(table, n_boot=2000, alpha=0.05, seed=0, stat=None):
    """Two-level bootstrap of the grand mean of `d`: resample datasets, then seeds within them; with
    `stat="median"` (or `CI_STAT`), of the median over datasets of the dataset means instead.
    `table`: DataFrame with columns dataset, d."""
    stat = stat or CI_STAT
    rng = np.random.default_rng(seed)
    groups = [g["d"].dropna().to_numpy() for _, g in table.groupby("dataset")]
    groups = [g for g in groups if len(g)]
    if not groups:
        return np.nan, np.nan
    M, sizes = padded(groups)
    means = []
    for pick, idx, valid in resample_groups(rng, sizes, n_boot):
        v = np.where(valid, M[pick[..., None], idx], 0.0)
        dm = v.sum(-1) / sizes[pick]
        means.append(np.median(dm, axis=1) if stat == "median" else dm.mean(1))
    return tuple(np.quantile(np.concatenate(means), [alpha / 2, 1 - alpha / 2]))


def block_indices(n, block, rng, size=None):
    """Moving-block resample of n rows; `size` — that many resamples at once, shape (size, n)."""
    nb = int(np.ceil(n / block))
    hi = max(1, n - block + 1)
    if size is None:
        starts = rng.integers(0, hi, nb)
        return np.concatenate([np.arange(s, min(s + block, n)) for s in starts])[:n]
    starts = rng.integers(0, hi, (size, nb))          # start ≤ n − block: every block fits (n < block: one block, cut)
    return (starts[:, :, None] + np.arange(block)).reshape(size, -1)[:, :n]


def auc_rows(y, S):
    """ROC AUC of every row of scores S (b, n) against labels y (b, n) — ties count ½, as in
    sklearn; NaN where a row has one class only."""
    y = np.asarray(y).astype(bool)
    r = stats.rankdata(S, axis=1)
    m = y.sum(1)
    k = y.shape[1] - m
    with np.errstate(invalid="ignore", divide="ignore"):
        auc = ((r * y).sum(1) - m * (m + 1) / 2) / (m * k)
    return np.where((m > 0) & (k > 0), auc, np.nan)


def paired_block_bootstrap(fn, a, b, y, block=168, n_boot=1000, alpha=0.05, seed=0, fn_rows=None):
    """CI of fn(y, a) − fn(y, b) with moving-block resampling of test rows (block = 1 week).
    `fn_rows(Y, A)` — the same metric of every row of (resamples × rows) matrices, NaN where it is
    undefined: all resamples at once instead of a loop over `fn`."""
    rng = np.random.default_rng(seed)
    n = len(y)
    diffs = []
    if fn_rows is not None:
        a, b, y = np.asarray(a), np.asarray(b), np.asarray(y)
        step = max(1, _CHUNK // max(1, n))
        for b0 in range(0, n_boot, step):
            idx = block_indices(n, block, rng, size=min(step, n_boot - b0))
            d = fn_rows(y[idx], a[idx]) - fn_rows(y[idx], b[idx])
            diffs.extend(d[np.isfinite(d)])
    else:
        for _ in range(n_boot):
            idx = block_indices(n, block, rng)
            try:
                diffs.append(fn(y[idx], a[idx]) - fn(y[idx], b[idx]))
            except ValueError:
                continue
    if not diffs:
        return np.nan, np.nan, np.nan
    diffs = np.asarray(diffs)
    p = 2 * min((diffs <= 0).mean(), (diffs >= 0).mean())
    return (*np.quantile(diffs, [alpha / 2, 1 - alpha / 2]), float(min(1.0, p)))


# ─────────────────────── forecast comparison tests ─────────────────────────
def delong(y, pa, pb):
    """DeLong test for two correlated AUCs. Returns (auc_a − auc_b, two-sided p)."""
    y = np.asarray(y).astype(int)
    pos, neg = y == 1, y == 0
    m, n = pos.sum(), neg.sum()
    if m < 2 or n < 2:
        return np.nan, np.nan

    def comps(p):
        X, Y = p[pos], p[neg]
        allr = stats.rankdata(np.r_[X, Y])
        rx, ry = stats.rankdata(X), stats.rankdata(Y)
        auc = (allr[:m].sum() - m * (m + 1) / 2) / (m * n)
        v10 = (allr[:m] - rx) / n
        v01 = 1 - (allr[m:] - ry) / m
        return auc, v10, v01

    a1, v10a, v01a = comps(np.asarray(pa, float))
    a2, v10b, v01b = comps(np.asarray(pb, float))
    s10 = np.cov(np.vstack([v10a, v10b]))
    s01 = np.cov(np.vstack([v01a, v01b]))
    var = (s10[0, 0] + s10[1, 1] - 2 * s10[0, 1]) / m + (s01[0, 0] + s01[1, 1] - 2 * s01[0, 1]) / n
    if var <= 0:
        return float(a1 - a2), np.nan
    z = (a1 - a2) / np.sqrt(var)
    return float(a1 - a2), float(2 * stats.norm.sf(abs(z)))


def diebold_mariano(loss_a, loss_b, h=1):
    """DM test with HAC (Newey–West, lag h−1… at least 1 week for hourly data) and the Harvey
    small-sample correction. d = loss_b − loss_a, so a positive statistic favours `a`."""
    d = np.asarray(loss_b, float) - np.asarray(loss_a, float)
    d = d[np.isfinite(d)]
    n = len(d)
    if n < 30:
        return np.nan, np.nan
    lag = max(h - 1, 168)
    dc = d - d.mean()
    gamma = [np.dot(dc[k:], dc[: n - k]) / n for k in range(min(lag, n - 1) + 1)]
    var = gamma[0] + 2 * sum((1 - k / (lag + 1)) * gamma[k] for k in range(1, len(gamma)))
    if var <= 0:
        return np.nan, np.nan
    stat = d.mean() / np.sqrt(var / n)
    corr = np.sqrt((n + 1 - 2 * h + h * (h - 1) / n) / n)
    stat *= corr
    return float(stat), float(2 * stats.t.sf(abs(stat), n - 1))


def stouffer(pvals_one_sided):
    p = np.asarray(pvals_one_sided, float)
    p = np.clip(p[np.isfinite(p)], 1e-300, 1 - 1e-16)
    if not len(p):
        return np.nan
    return float(stats.norm.sf(stats.norm.isf(p).sum() / np.sqrt(len(p))))


# ─────────────────────── many methods ──────────────────────────────────────
_Q05 = {2: 1.960, 3: 2.343, 4: 2.569, 5: 2.728, 6: 2.850, 7: 2.949, 8: 3.031, 9: 3.102, 10: 3.164}


def complete_blocks(D: pd.DataFrame, min_values: int = 3) -> pd.DataFrame:
    """A complete blocks × methods table for Friedman-type tests: methods with fewer than `min_values` blocks
    are dropped; then either the incomplete methods (e.g. a method left out on a dataset of its training
    data, `Config.leaked`) or the incomplete blocks are dropped — whichever keeps more cells."""
    D = D.dropna(axis=1, thresh=min_values)
    by_col, by_row = D.dropna(axis=1), D.dropna()
    return by_col if by_col.size >= by_row.size and by_col.shape[1] >= 2 else by_row


def friedman_nemenyi(scores):
    """`scores`: DataFrame blocks × methods, higher = better. Friedman p, average ranks
    (1 = best) and the Nemenyi critical difference at α = 0.05, on `complete_blocks`."""
    S = complete_blocks(scores, 1)
    if len(S) < 3 or S.shape[1] < 2:
        return np.nan, None, np.nan
    p = float(stats.friedmanchisquare(*[S[c] for c in S.columns]).pvalue) if S.shape[1] > 2 else np.nan
    ranks = S.rank(axis=1, ascending=False).mean()
    k, n = S.shape[1], len(S)
    q = _Q05.get(k) or float(stats.studentized_range.ppf(0.95, k, np.inf) / np.sqrt(2))   # any number of methods
    cd = q * np.sqrt(k * (k + 1) / (6 * n))
    return p, ranks.sort_values(), float(cd)


def page_trend(matrix):
    """Page's L test for a monotone trend across ordered conditions (columns), rows = blocks."""
    M = np.asarray(matrix, float)
    M = M[np.isfinite(M).all(1)]
    if len(M) < 3:
        return np.nan
    return float(stats.page_trend_test(M).pvalue)


def ttest_1samp(x):
    """Two-sided one-sample t-test of the dataset means against 0 (parametric companion to Wilcoxon)."""
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    if len(x) < 3 or np.allclose(x, x[0]):
        return np.nan
    return float(stats.ttest_1samp(x, 0.0).pvalue)


# ─────────────────────── custom tests ──────────────────────────────────────
DATASET_TESTS: dict = {}     # name → fn(d: per-seed differences, margin) -> dict of columns
GLOBAL_TESTS: dict = {}      # name → fn(z: dataset means in noise units) -> dict of columns


def register_test(name: str, level: str = "global"):
    """Decorator: add a statistical test to every hypothesis table.

        @register_test("bayes_sign", level="global")
        def bayes_sign(z):                       # dataset-level effects in noise units
            return {"p_bayes_better": ...}

    `level="dataset"`: fn(d, margin) on per-seed paired differences of one dataset."""
    def deco(fn):
        (DATASET_TESTS if level == "dataset" else GLOBAL_TESTS)[name] = fn
        return fn

    return deco


def run_tests(registry: dict, *args) -> dict:
    out = {}
    for name, fn in registry.items():
        try:
            out.update(fn(*args))
        except Exception as e:                    # a broken custom test must not stop the analysis
            out[f"{name}_error"] = f"{type(e).__name__}: {e}"
    return out
