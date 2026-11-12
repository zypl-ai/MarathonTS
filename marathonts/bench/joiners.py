"""Seam processing (BASELINES.md B): the windows of a path → one series with processed seams.

A joiner gets the windows of a path in order, `(n, T, F)` in the benchmark channels, and returns
the first `L = K·T` points of the joined series. Overlapping windows shorten the series, so it may
need more than K windows: `windows_needed(K, T, cfg)` is what the method's assembler is asked for
(`ctx.K`). A method is then pool + assembler + joiner:

    from marathonts.bench.methods import register_method
    register_method("vae_greedy_xfade", pool="tsgm_vae", assembler="greedy", joiner="crossfade")

Custom joiner:

    from marathonts.bench import registry as R
    from marathonts.bench.joiners import Joiner

    @R.joiners.register("my_join")
    class MyJoin(Joiner):
        def windows_needed(self, K, T, cfg): return K + 5
        def join(self, W, L, cfg):
            return X, seams, src, info     # X (L, F); seams: indices; src: index into W per point

Only the value channel is processed: `crossfade` and `wsola` keep the calendar channels of the
earlier window over the overlap, `quilt` takes all channels of the next window from the cut on. Built-ins: `crossfade` — the windows overlap by `join_overlap` points mixed with a
Hann ramp (overlap-add, Allen & Rabiner 1977); `wsola` — before mixing, the next window is shifted
by up to `join_wsola_shift` points to the best correlation over the overlap (Verhelst & Roelands
1993); `quilt` — in the overlap the series switches to the next window at the point of the smallest
|difference| (image quilting's minimum-error boundary cut in 1D, Efros & Freeman 2001).
"""
from __future__ import annotations

import numpy as np

from . import registry as R


class Joiner:
    def windows_needed(self, K: int, T: int, cfg) -> int:
        raise NotImplementedError

    def join(self, W: np.ndarray, L: int, cfg):
        raise NotImplementedError


def _ramp(o: int) -> np.ndarray:
    """Hann ramp 0 → 1 over `o` points (weight of the next window)."""
    return 0.5 * (1 - np.cos(np.pi * (np.arange(o) + 0.5) / o))


class _Overlap(Joiner):
    """Common loop: each next window overlaps the series tail by `join_overlap` points."""

    def _shift_max(self, cfg) -> int:
        return 0

    def windows_needed(self, K, T, cfg):
        step = T - cfg.join_overlap - self._shift_max(cfg)     # fewest new points one window adds
        if cfg.join_overlap < 1 or step < 1:
            raise ValueError(f"join_overlap={cfg.join_overlap} (+ shift) leaves no new points of a window of {T}")
        return 1 + int(np.ceil((K * T - T) / step))

    def _shift(self, tail, w, o, cfg) -> int:
        return 0

    def _merge(self, X, n, w, o):
        """Write window `w` (its overlap at X[n−o:n]) and return (new length, seam position)."""
        raise NotImplementedError

    def join(self, W, L, cfg):
        n_w, T, F = W.shape
        o = cfg.join_overlap
        X = np.zeros((n_w * T, F), np.float32)
        src = np.zeros(n_w * T, np.int64)
        X[:T], n, seams, shifts = W[0], T, [], []
        for k in range(1, n_w):
            if n >= L:
                break
            s = self._shift(X[n - o:n, 0], W[k, :, 0], o, cfg)
            shifts.append(s)
            w = W[k, s:]
            n_new, seam = self._merge(X, n, w, o)
            src[seam:n_new] = k
            seams.append(seam)
            n = n_new
        if n < L:
            raise ValueError(f"{type(self).__name__}: {n_w} windows give {n} points, need {L}")
        seams = np.asarray([s for s in seams if 0 < s < L], int)
        return X[:L], seams, src[:L], {"join_overlap": o, "join_windows": int(src[:L].max()) + 1,
                                       "join_mean_shift": float(np.mean(shifts)) if shifts else 0.0}


@R.joiners.register("crossfade")
class Crossfade(_Overlap):
    def _merge(self, X, n, w, o):
        r = _ramp(o)
        X[n - o:n, 0] = (1 - r) * X[n - o:n, 0] + r * w[:o, 0]
        m = len(w) - o
        X[n:n + m] = w[o:]
        return n + m, n - o // 2                     # seam: the middle of the blend


@R.joiners.register("wsola")
class WSOLA(Crossfade):
    def _shift_max(self, cfg):
        return cfg.join_wsola_shift

    def _shift(self, tail, w, o, cfg):
        best, best_s = -np.inf, 0
        for s in range(0, min(cfg.join_wsola_shift, len(w) - o - 1) + 1):
            head = w[s:s + o]
            if np.std(tail) > 0 and np.std(head) > 0:
                score = float(np.corrcoef(tail, head)[0, 1])
            else:
                score = -float(np.mean(np.abs(tail - head)))
            if score > best:
                best, best_s = score, s
        return best_s


@R.joiners.register("quilt")
class Quilt(_Overlap):
    def _merge(self, X, n, w, o):
        c = int(np.argmin(np.abs(X[n - o:n, 0] - w[:o, 0])))   # minimum-error cut inside the overlap
        start = n - o + c
        X[start:start + len(w) - c] = w[c:]
        return start + len(w) - c, start
