"""Noise-aware ranks of the overall leaderboard (`overall.rank_noise`): the worked example of the paper, order
invariance and the sum of the ranks of a block."""
import numpy as np
import pandas as pd

from marathonts.hypotheses.overall import rank_noise


def _block(scores, names=None):
    names = names or [f"m{i}" for i in range(len(scores))]
    return pd.DataFrame({"dataset": "d", "seed": 0, "leaf": "l", "slice": "s", "method": names, "score": scores})


def _noise(e):
    return pd.Series([e], index=pd.MultiIndex.from_tuples([("d", "l", "s")]))


def test_three_method_example():
    r = rank_noise(_block([1.2, 0.6, 0.0], ["A", "B", "C"]), 3, _noise(1.0)).set_index("method")["rank"]
    assert r.to_dict() == {"A": 1.5, "B": 2.0, "C": 2.5}       # A ~ B, B ~ C, A beats C: no groups are formed


def test_order_invariance_and_rank_sum():
    rng = np.random.default_rng(0)
    for _ in range(50):
        k = int(rng.integers(3, 12))
        s = rng.normal(size=k)
        e = float(rng.uniform(0, 1))
        r = rank_noise(_block(list(s)), k, _noise(e)).set_index("method")["rank"]
        perm = rng.permutation(k)
        names = [f"x{p:02d}" for p in perm]                     # other names: the methods come in another order
        r2 = rank_noise(_block(list(s), names), k, _noise(e)).set_index("method")["rank"]
        back = dict(zip(names, [f"m{i}" for i in range(k)]))
        r2 = r2.rename(index=back)
        assert np.allclose(r.sort_index().to_numpy(), r2.sort_index().to_numpy())
        assert np.isclose(r.sum(), k * (k + 1) / 2)
