"""Assemblers (stitchers): pool of windows → path, the indices of K windows in order.

    from marathonts.bench import registry as R
    from marathonts.bench.assemblers import Assembler

    @R.assemblers.register("my_stitch")
    class MyStitch(Assembler):
        def assemble(self, pool, ctx):              # pool (N, T, F) in benchmark channels
            return path, {"diagnostic": 1.0}         # path: K pool indices, any order, no repeats needed

The assembled series is `concatenate(pool[path])`; seams are at multiples of T (a method with a
joiner — `bench.joiners` — processes the seams instead and asks for more windows: `ctx.K` is then
the number it needs). Built-ins:

* `zseries` — the stitcher of `vae_zseries`, the proprietary stitching method of zypl.ai (under development): its
  results are published (`Config.frozen_methods`), its code is not part of the repository; the registered
  entry only names the method;
* `random` / `random_b` — random paths (two seeds: the noise pair; `random_b` in mid and max);
* alternatives on the same pool (BASELINES.md A), each with the seam criterion of its own literature:
  `greedy` — nearest neighbour from a random start, `atsp` — shortest Hamiltonian tour over the whole
  pool by LKH (elkai), its cheapest run of K windows, `pctsp` — prize-collecting TSP (OR-Tools): choice
  of K of N and their order at once — the three solvers on the jump at the seam (`seam_jump`: Euclidean
  distance between the last point of a window and the first point of the next, every channel — the
  frame distance of video textures, Schödl et al. 2000); `mbb` — matched-block bootstrap (Carlstein et
  al. 1998), the next window drawn with a Gaussian kernel of the jump; `knn` — k-nearest-neighbour
  resampling (Lall & Sharma 1996), the next window drawn among the k nearest with weights ∝ 1/rank;
  `quilt_sel` — the patch choice of image quilting (Efros & Freeman 2001): a random window among those
  whose overlap error is within (1 + `quilt_tol`) of the best, run with the `quilt` joiner; `herding` —
  kernel herding (MMD to the train windows) for the choice, random order.
"""
from __future__ import annotations

import numpy as np

from . import registry as R
from .generators.base import GenContext


class Assembler:
    requires: tuple = ()         # importable modules it needs (checked before assembling)
    uses_targets: bool = False   # reads target_params (the exogenous thresholds): they enter its fingerprint

    def assemble(self, pool: np.ndarray, ctx: GenContext) -> tuple[np.ndarray, dict]:
        raise NotImplementedError


def seam_jump(pool) -> np.ndarray:
    """N × N cost of the seam i → j: Euclidean distance between the last point of window i and the first
    point of window j over every channel (value and calendar, all on [0, 1]) — the frame distance of video
    textures (Schödl et al. 2000); the diagonal is +inf."""
    P = np.asarray(pool, np.float64)
    D = np.sqrt(((P[:, -1, None, :] - P[None, :, 0, :]) ** 2).sum(-1))
    np.fill_diagonal(D, np.inf)
    return D


def _scaled_int(M) -> np.ndarray:
    """Integer costs for the solvers (LKH, OR-Tools): median off-diagonal cost = 1000."""
    N = len(M)
    off = M[~np.eye(N, dtype=bool)]
    Mi = np.rint(np.where(np.isfinite(M), M, 0) * (1000.0 / max(float(np.median(off)), 1e-12))).astype(np.int64)
    np.fill_diagonal(Mi, 0)
    return Mi


def _path_edges(M, path) -> float:
    path = np.asarray(path, int)
    return float(M[path[:-1], path[1:]].sum())


@R.assemblers.register("zseries")
class Unpublished(Assembler):
    """The stitcher of `vae_zseries`: published results only (`Config.frozen_methods`)."""

    def assemble(self, pool, ctx):
        raise NotImplementedError("the stitcher of vae_zseries is not part of the repository: its results are "
                                  "published (Config.frozen_methods)")


class Random(Assembler):
    def __init__(self, offset: int):
        self.offset = offset

    def assemble(self, pool, ctx):
        return np.random.default_rng(self.offset + ctx.seed).permutation(len(pool))[:ctx.K], {}


R.assemblers.register("random", lambda: Random(1000))
R.assemblers.register("random_b", lambda: Random(2000))


# ─────────────────────── alternatives on the same pool (BASELINES.md A) ────
@R.assemblers.register("greedy")
class Greedy(Assembler):
    """Nearest neighbour by the jump at the seam (`seam_jump`) from a random start window."""

    def assemble(self, pool, ctx):
        M = seam_jump(pool)
        rng = np.random.default_rng(7000 + ctx.seed)
        used = np.zeros(len(pool), bool)
        path = [int(rng.integers(len(pool)))]
        used[path[0]] = True
        while len(path) < ctx.K:
            row = np.where(used, np.inf, M[path[-1]])
            j = int(np.argmin(row))
            path.append(j)
            used[j] = True
        return np.asarray(path), {"seam_acc": _path_edges(M, path)}


@R.assemblers.register("atsp")
class ATSP(Assembler):
    """Asymmetric TSP over the whole pool by the jump at the seam (`seam_jump`), Lin–Kernighan–Helsgaun
    (elkai; the LKH licence is non-commercial); the path is the cheapest run of K consecutive windows of
    the tour."""
    requires = ("elkai",)

    def assemble(self, pool, ctx):
        import elkai

        M = seam_jump(pool)
        N, K = len(M), ctx.K
        Mi = _scaled_int(M)                          # LKH works on integers
        tour = [int(i) for i in elkai.DistanceMatrix(Mi.tolist()).solve_tsp()]
        if len(tour) > N:                            # closed tour: the start repeated at the end
            tour = tour[:N]
        best, best_c = None, np.inf
        for s in range(N):                           # cyclic runs of K windows
            seg = [tour[(s + i) % N] for i in range(K)]
            c = _path_edges(M, seg)
            if c < best_c:
                best, best_c = seg, c
        return np.asarray(best), {"seam_acc": best_c}


@R.assemblers.register("pctsp")
class PCTSP(Assembler):
    """Prize-collecting TSP (OR-Tools routing): the choice of K of N windows and their order at once,
    minimising the jump at the seams (`seam_jump`) along the path. Every window can be dropped for a penalty larger than any
    path, and the route holds at most K windows — so exactly K are visited. Time-limited guided local
    search (`pctsp_time_s`)."""
    requires = ("ortools",)

    def assemble(self, pool, ctx):
        from ortools.constraint_solver import pywrapcp, routing_enums_pb2

        M = seam_jump(pool)
        N, K = len(M), ctx.K
        C = _scaled_int(M)
        depot = N                                    # a dummy node: free arcs to and from it (open path)
        manager = pywrapcp.RoutingIndexManager(N + 1, 1, depot)
        routing = pywrapcp.RoutingModel(manager)

        def arc(i, j):
            a, b = manager.IndexToNode(i), manager.IndexToNode(j)
            return 0 if a == depot or b == depot else int(C[a, b])

        routing.SetArcCostEvaluatorOfAllVehicles(routing.RegisterTransitCallback(arc))
        count = routing.RegisterUnaryTransitCallback(lambda i: 0 if manager.IndexToNode(i) == depot else 1)
        routing.AddDimension(count, 0, K, True, "count")
        penalty = int(C.max()) * (K + 1) + 1
        for n in range(N):
            routing.AddDisjunction([manager.NodeToIndex(n)], penalty)
        prm = pywrapcp.DefaultRoutingSearchParameters()
        prm.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
        prm.local_search_metaheuristic = routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
        prm.time_limit.FromMilliseconds(int(1000 * ctx.cfg.pctsp_time_s))      # a cap; the solution limit decides
        prm.solution_limit = int(ctx.cfg.pctsp_solutions)                     # reproducible across machines
        sol = routing.SolveWithParameters(prm)
        if sol is None:
            raise RuntimeError("pctsp: OR-Tools found no solution")
        path, idx = [], routing.Start(0)
        while not routing.IsEnd(idx):
            n = manager.IndexToNode(idx)
            if n != depot:
                path.append(n)
            idx = sol.Value(routing.NextVar(idx))
        if len(path) != K:
            raise RuntimeError(f"pctsp: route of {len(path)} windows, expected K={K}")
        return np.asarray(path), {"seam_acc": _path_edges(M, path)}


def _markov_path(M, K, rng, weights) -> list[int]:
    """A path without repeats from a random start: the next window is drawn with `weights(costs)` over the
    unused windows (costs: row of M, +inf for the used ones)."""
    N = len(M)
    used = np.zeros(N, bool)
    path = [int(rng.integers(N))]
    used[path[0]] = True
    while len(path) < K:
        w = weights(np.where(used, np.inf, M[path[-1]]))
        j = int(rng.choice(N, p=w / w.sum()))
        path.append(j)
        used[j] = True
    return path


@R.assemblers.register("mbb")
class MatchedBlock(Assembler):
    """Matched-block bootstrap (Carlstein, Do, Hall, Hesterberg, Künsch 1998): the next block is drawn with
    a kernel of how well its beginning matches the end of the current one — here a Gaussian kernel of the
    jump at the seam (`seam_jump`), h = `mbb_bandwidth` · median jump; without repeats, random start."""

    def assemble(self, pool, ctx):
        M = seam_jump(pool)
        h = ctx.cfg.mbb_bandwidth * float(np.median(M[np.isfinite(M)]))
        def weights(e):                                    # exp(−½ (e / h)²), computed in logs (no underflow)
            lw = -0.5 * (e / max(h, 1e-12)) ** 2
            return np.exp(lw - lw[np.isfinite(lw)].max())

        path = _markov_path(M, ctx.K, np.random.default_rng(8000 + ctx.seed), weights)
        return np.asarray(path), {"seam_acc": _path_edges(M, path), "mbb_bandwidth": h}


@R.assemblers.register("knn")
class KNNResampling(Assembler):
    """k-nearest-neighbour resampling (Lall & Sharma 1996): the k windows whose first point is nearest to the
    last point of the current one (`seam_jump`), one drawn with weight ∝ 1/rank; k = `knn_k`, by default
    round(√N) as the authors recommend; without repeats, random start."""

    def assemble(self, pool, ctx):
        M = seam_jump(pool)
        N = len(M)
        k = int(ctx.cfg.knn_k or max(1, round(np.sqrt(N))))

        def weights(e):
            w = np.zeros(N)
            free = np.flatnonzero(np.isfinite(e))
            near = free[np.argsort(e[free], kind="stable")[:k]]
            w[near] = 1.0 / np.arange(1, len(near) + 1)
            return w

        path = _markov_path(M, ctx.K, np.random.default_rng(10000 + ctx.seed), weights)
        return np.asarray(path), {"seam_acc": _path_edges(M, path), "knn_k": k}


@R.assemblers.register("quilt_sel")
class QuiltSelect(Assembler):
    """The patch choice of image quilting (Efros & Freeman 2001) in 1D: the next window overlaps the current
    one by `join_overlap` points; its overlap error is the sum of squared differences of the value channel
    over the overlap, and the next window is drawn at random among those within (1 + `quilt_tol`) of the
    smallest error; without repeats, random start. Run with the `quilt` joiner (the minimum-error boundary
    cut in the overlap), as in the original."""

    def assemble(self, pool, ctx):
        o = int(ctx.cfg.join_overlap)
        P = np.asarray(pool[:, :, 0], np.float64)
        tail, head = P[:, -o:], P[:, :o]
        M = np.maximum((tail * tail).sum(1)[:, None] + (head * head).sum(1)[None, :] - 2 * tail @ head.T, 0.0)
        np.fill_diagonal(M, np.inf)
        tol = ctx.cfg.quilt_tol

        def weights(e):
            best = e.min()
            return (np.isfinite(e) & (e <= (1 + tol) * best + 1e-12)).astype(float)

        path = _markov_path(M, ctx.K, np.random.default_rng(11000 + ctx.seed), weights)
        return np.asarray(path), {"overlap_err": _path_edges(M, path)}


@R.assemblers.register("herding")
class Herding(Assembler):
    """Kernel herding (MMD to the train windows) chooses K windows, the order is random — separates
    the effect of the choice from the effect of the order. RBF kernel on every
    `herding_stride`-th point of the value channel, median-heuristic bandwidth."""

    def assemble(self, pool, ctx):
        st = ctx.cfg.herding_stride
        P = pool[:, ::st, 0].astype(np.float64)
        Xt = ctx.X_core[:, ::st, 0].astype(np.float64)
        Xt = Xt[~np.isnan(Xt).any(axis=1)]

        def sq(a, b):
            return np.maximum((a * a).sum(1)[:, None] + (b * b).sum(1)[None, :] - 2 * a @ b.T, 0.0)

        d_pt = sq(P, Xt)
        gamma = 1.0 / max(float(np.median(d_pt)), 1e-12)
        mu = np.exp(-gamma * d_pt).mean(1)                    # mean embedding of train at every pool window
        Kpp = np.exp(-gamma * sq(P, P))
        chosen, acc = [], np.zeros(len(P))
        for t in range(ctx.K):
            score = mu - acc / (t + 1)
            score[chosen] = -np.inf
            j = int(np.argmax(score))
            chosen.append(j)
            acc += Kpp[:, j]
        order = np.random.default_rng(9000 + ctx.seed).permutation(chosen)
        return order, {"herding_gamma": gamma}
