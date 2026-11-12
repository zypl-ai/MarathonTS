"""Smoke test on the published results as a clone has them (`artifacts/run_*/tables/` only), for each published
run (`run_h200`, the main run; `run_l4`, the replication run): the tables are real files, the frozen rows pass the
settings check under `min`, and the analysis rebuilds the published rankings, overall leaderboard, questions and
metric values from the tables alone, the methods whose code is not in the repository (zseries, zEDGE and
zEDGE_TS of the main run) included: the analysis needs only their names and roles. A run whose config still
lists a plugin file is skipped. Takes a few minutes per run."""
import json
import subprocess
import sys

import pandas as pd
import pytest

from marathonts.bench import cells as CL
from marathonts.bench.config import Config
from marathonts.bench.run import _check_frozen
from marathonts.bench.storage import is_valid
from conftest import ROOT

RUNS = ("run_h200", "run_l4")
TABLES = ("timing", "fidelity", "utility", "cross_seed")
# outputs that read what is not in the tables (predictions, labels: CS7, CS12, CS13; data/processed: RQ7, CS15)
NEEDS_MORE = ("CS7_rowlevel", "CS12_subgroups", "CS13_rowlevel", "CS15_", "RQ7_")


@pytest.fixture(params=RUNS)
def PUB(request):
    pub = ROOT / "artifacts" / request.param
    if not (pub / "tables").exists():
        pytest.skip(f"no published tables of {request.param}")
    return pub


def _sorted(df):
    """Rows in a fixed order: ties in a ranking may come out in either order."""
    keys = [c for c in df.columns if not pd.api.types.is_float_dtype(df[c])]
    floats = [c for c in df.columns if c not in keys]
    try:
        return df.sort_values(keys + floats, kind="stable").reset_index(drop=True)
    except TypeError:                                  # unorderable values (lists): as written
        return df.reset_index(drop=True)


def test_tables_are_files(PUB):
    for f in sorted((PUB / "tables").glob("*.parquet")):
        assert is_valid(f), f                          # a Git LFS pointer raises with what to do


def test_frozen_rows_match_their_settings(PUB):
    cfg = Config.profile("min")
    if not cfg.frozen_methods:
        pytest.skip("no methods published without code in this version")
    ref = json.loads((PUB / "tables" / CL.FROZEN_REF).read_text())
    now = CL.frozen_reference(cfg)
    for name in TABLES:
        df = pd.read_parquet(PUB / "tables" / f"{name}.parquet")
        assert len(_check_frozen(df, name, cfg, ref, now)) == len(df), name


def test_analysis_reproduces_the_published_results(PUB, tmp_path):
    plugins = json.loads((PUB / "tables" / "config.json").read_text()).get("plugins") or []
    if plugins:
        pytest.skip(f"{PUB.name}: its methods need plugins that are not in the repository ({', '.join(plugins)})")
    art = tmp_path / "min"
    art.mkdir()
    (art / "tables").symlink_to(PUB / "tables")
    (tmp_path / "processed").mkdir()
    subprocess.run([sys.executable, "-m", "marathonts.hypotheses.run", "--artifacts-dir", str(art),
                    "--processed-dir", str(tmp_path / "processed")], cwd=ROOT, check=True)
    missing, differ = [], []
    for sub in ("leaderboard", "overall", "hypotheses", "metric_values"):
        for f in sorted((PUB / sub).glob("*.parquet")):
            g = art / sub / f.name
            if not g.exists():
                if not f.stem.startswith(NEEDS_MORE):
                    missing.append(f"{sub}/{f.name}")
                continue
            try:                                       # float32 in the tables: values agree to ~1e-6
                pd.testing.assert_frame_equal(_sorted(pd.read_parquet(f)), _sorted(pd.read_parquet(g)),
                                              check_dtype=False, rtol=1e-4, atol=1e-5)
            except AssertionError as e:
                differ.append(f"{sub}/{f.name}: {str(e).splitlines()[0]}")
    assert not missing and not differ, (missing, differ)
