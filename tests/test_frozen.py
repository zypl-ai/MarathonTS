"""collect: rows of the methods published without code enter the tables only under the settings of their results."""
import dataclasses

import numpy as np
import pandas as pd

from marathonts.bench import cells as CL
from marathonts.bench.config import Config
from marathonts.bench.fidelity import GROUP_OF
from marathonts.bench.run import _check_frozen

M = "vae_zseries"


def _cfg(**kw):
    return dataclasses.replace(Config.profile("min"), datasets=["ett", "bike"], seeds=[0, 1],
                               frozen_methods=[M, f"{M}_xfade"], **kw)


def _series_rows():
    return pd.DataFrame({"method": [M, M, M, f"{M}_xfade", "vae_rand"],
                         "dataset": ["ett", "bike", "jena", "ett", "jena"], "seed": [0, 1, 0, 5, 0]})


def test_same_settings_keep_the_run_scope():
    cfg = _cfg()
    out = _check_frozen(_series_rows(), "timing", cfg, CL.frozen_reference(cfg), CL.frozen_reference(cfg))
    # another dataset (jena) or seed (5) of a frozen method is left out; an open method is not touched here
    assert sorted(zip(out.method, out.dataset)) == sorted([(M, "ett"), (M, "bike"), ("vae_rand", "jena")])


def test_other_settings_drop_every_frozen_row():
    ref = CL.frozen_reference(_cfg())
    cfg = _cfg(max_points=5000)
    out = _check_frozen(_series_rows(), "timing", cfg, ref, CL.frozen_reference(cfg))
    assert list(out.method) == ["vae_rand"]


def test_without_reference_rows_are_kept():
    cfg = _cfg()
    out = _check_frozen(_series_rows(), "timing", cfg, None, CL.frozen_reference(cfg))
    assert len(out) == 3                                 # only the run scope (dataset, seed) applies


def test_utility_per_cell():
    cfg = _cfg()
    ref, now = CL.frozen_reference(cfg), CL.frozen_reference(cfg)
    a, b = list(now[M]["ett"]["utility"])[:2]
    ref[M]["ett"]["utility"][b] = "changed"
    df = pd.DataFrame([{"method": M, "dataset": "ett", "seed": 0, "task": k.split("|")[0], "model": k.split("|")[1]}
                       for k in (a, b)])
    out = _check_frozen(df, "utility", cfg, ref, now)
    assert [f"{t}|{m}" for t, m in zip(out.task, out.model)] == [a]


def test_fidelity_per_group():
    cfg = _cfg()
    ref, now = CL.frozen_reference(cfg), CL.frozen_reference(cfg)
    cols = {}
    for c, g in GROUP_OF.items():
        cols.setdefault(g, c)
    g1, g2 = list(now[M]["ett"]["fidelity"][M])[:2]
    ref[M]["ett"]["fidelity"][M][g2] = "changed"
    df = pd.DataFrame({"method": [M], "dataset": ["ett"], "seed": [0], cols[g1]: [0.5], cols[g2]: [0.5]})
    out = _check_frozen(df, "fidelity", cfg, ref, now)
    assert out[cols[g1]].iloc[0] == 0.5 and np.isnan(out[cols[g2]].iloc[0])
