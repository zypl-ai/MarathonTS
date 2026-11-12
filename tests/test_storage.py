"""marathonts/bench/storage.py: a unit is done only if its file reads back; a Git LFS pointer stops the run untouched."""
import pandas as pd
import pytest

from marathonts.bench.storage import LfsPointerError, check_done, is_valid, read_table, write_table

POINTER = ("version https://git-lfs.github.com/spec/v1\n"
           "oid sha256:4d7a214614ab2935c943f9e0ff69d22eadbb8f32b1258daaa5e2ca24d17e2393\nsize 12345\n")


def test_valid_file(tmp_path):
    p = write_table(pd.DataFrame({"a": [1.0, 2.0]}), tmp_path / "t.parquet")
    assert is_valid(p) and check_done(p)


def test_truncated_file_is_set_aside(tmp_path):
    p = write_table(pd.DataFrame({"a": range(100)}), tmp_path / "t.parquet")
    p.write_bytes(p.read_bytes()[:20])
    assert not check_done(p)
    assert not p.exists() and (tmp_path / "t.parquet.bad").exists()


def test_lfs_pointer_stops_the_run_and_is_kept(tmp_path):
    p = tmp_path / "t.parquet"
    p.write_text(POINTER)
    for fn in (is_valid, check_done, read_table):
        with pytest.raises(LfsPointerError, match="git lfs"):
            fn(p)
    assert p.read_text() == POINTER and not (tmp_path / "t.parquet.bad").exists()
