"""Dataset registry: raw files (Parquet) → one hourly target series.

A dataset is anything registered in `registry.datasets` as a `DatasetSpec`: a `load(cfg)`
returning an **hourly** `pd.Series` (DatetimeIndex, NaN where unknown). Custom datasets:

    from marathonts.bench.datasets import register_parquet_dataset
    register_parquet_dataset("my_sales", "data/raw/my/sales.parquet", time_col="ts", value_col="units",
                             agg="sum")                      # resampled to hours

or any function: `registry.datasets.register("x", DatasetSpec(load=lambda cfg: series))`.

Built-in datasets keep their raw files in `data/raw/<name>/*.parquet` (lossless conversion of
the downloaded CSV / TXT, see `convert_raw` and `download_raw`).
"""
from __future__ import annotations

import io
import os
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

import numpy as np
import pandas as pd

from . import registry as R
from .storage import read_table, write_table


@dataclass
class DatasetSpec:
    load: Callable                                 # cfg -> hourly pd.Series
    description: str = ""
    raw_files: dict = field(default_factory=dict)  # parquet name → (original file, reader)
    source: str = ""


def hourly(s: pd.Series, how: str = "mean") -> pd.Series:
    """Resample to an hourly grid; `how` = mean | sum | last."""
    s = s.sort_index()
    r = s.resample("h")
    out = {"mean": r.mean, "sum": lambda: r.sum(min_count=1), "last": r.last}[how]()
    return out.asfreq("h")


def register_parquet_dataset(name: str, path, time_col: str, value_col: str, agg: str = "mean",
                             transform: Callable | None = None, description: str = "", overwrite=False):
    """A custom dataset from a Parquet (or CSV) file with a time column and a value column."""
    path = Path(path)

    def load(cfg):
        df = pd.read_parquet(path) if path.suffix == ".parquet" else pd.read_csv(path)
        s = pd.Series(pd.to_numeric(df[value_col], errors="coerce").to_numpy(float),
                      index=pd.to_datetime(df[time_col]))
        s = hourly(s, agg)
        return transform(s) if transform else s

    return R.datasets.register(name, DatasetSpec(load, description, source=str(path)), overwrite=overwrite)


def raw_path(cfg, name: str, file: str) -> Path:
    return cfg.raw_dir / name / f"{file}.parquet"


def _raw(cfg, name, file, columns=None) -> pd.DataFrame:
    return pd.read_parquet(raw_path(cfg, name, file), columns=columns)


# ─────────────────────── built-in datasets ─────────────────────────────────
def _ett(cfg):
    df = _raw(cfg, "ett", "ETTh1")
    return hourly(pd.Series(df["OT"].to_numpy(float), index=pd.to_datetime(df["date"])))


def _electricity(cfg):
    df = _raw(cfg, "electricity", "LD2011_2014")
    idx = pd.to_datetime(df.pop("time"))
    return hourly(pd.Series(df.sum(axis=1).to_numpy(float), index=idx))     # total load of 370 clients, kW


def _household(cfg):
    df = _raw(cfg, "household", "household_power_consumption", ["Date", "Time", "Global_active_power"])
    idx = pd.to_datetime(df["Date"] + " " + df["Time"], format="%d/%m/%Y %H:%M:%S")
    return hourly(pd.Series(pd.to_numeric(df["Global_active_power"], errors="coerce").to_numpy(float), index=idx))


def _pjm(cfg):
    df = _raw(cfg, "pjm", "PJME_hourly")
    s = df.groupby(pd.to_datetime(df["Datetime"]))["PJME_MW"].mean()          # DST duplicates
    return hourly(s)


def _pm25(cfg):
    df = _raw(cfg, "beijing_pm25", "PRSA_data_2010.1.1-2014.12.31")
    idx = pd.to_datetime(df[["year", "month", "day", "hour"]])
    return hourly(pd.Series(df["pm2.5"].to_numpy(float), index=idx))


def _jena(cfg):
    df = _raw(cfg, "jena", "jena_climate_2009_2016", ["Date Time", "T (degC)"])
    idx = pd.to_datetime(df["Date Time"], format="%d.%m.%Y %H:%M:%S")
    return hourly(pd.Series(df["T (degC)"].to_numpy(float), index=idx))


def _metro(cfg):
    df = _raw(cfg, "metro", "Metro_Interstate_Traffic_Volume")
    s = hourly(df.groupby(pd.to_datetime(df["date_time"]))["traffic_volume"].mean())
    # a ~10-month hole in 2014–2015: keep the contiguous part after the last gap longer than 30 days
    gap = s.isna().astype(int).groupby(s.notna().cumsum()).sum()
    big = gap[gap > 24 * 30]
    if len(big):
        start = s.index[s.notna().cumsum() == big.index[-1]][0]
        s = s[start:].iloc[1:]
    return s


def _bike(cfg):
    df = _raw(cfg, "bike", "hour")
    idx = pd.to_datetime(df["dteday"]) + pd.to_timedelta(df["hr"], unit="h")
    return hourly(pd.Series(df["cnt"].to_numpy(float), index=idx)).fillna(0.0)   # missing hour = no rentals


def _bitcoin(cfg):
    df = _raw(cfg, "bitcoin", "btcusd_1-min_data", ["Timestamp", "Close"])
    s = pd.Series(df["Close"].to_numpy(float), index=pd.to_datetime(df["Timestamp"], unit="s"))
    s = s[(s.index >= cfg.bitcoin_start) & (s.index < cfg.bitcoin_end)]
    return np.log(hourly(s, "last"))                                            # log price


def _csv(**kw):
    return lambda f: pd.read_csv(f, **kw)


BUILTIN = {
    "ett": (_ett, "ETTh1, oil temperature OT, hourly", {
        "ETTh1": ("ETTh1.csv", _csv())},
        "https://raw.githubusercontent.com/zhouhaoyi/ETDataset/main/ETT-small/ETTh1.csv"),
    "electricity": (_electricity, "UCI electricity, total load of 370 clients, 15 min → hourly", {
        "LD2011_2014": ("LD2011_2014.txt",
                        lambda f: pd.read_csv(f, sep=";", decimal=",", index_col=0)
                        .rename_axis("time").reset_index())},
        "https://archive.ics.uci.edu/static/public/321/electricityloaddiagrams20112014.zip"),
    "household": (_household, "UCI household power, Global_active_power, 1 min → hourly", {
        "household_power_consumption": ("household_power_consumption.txt",
                                        _csv(sep=";", dtype=str, low_memory=False))},
        "https://archive.ics.uci.edu/static/public/235/individual+household+electric+power+consumption.zip"),
    "pjm": (_pjm, "PJM East hourly load (Kaggle robikscube/hourly-energy-consumption)", {
        "PJME_hourly": ("PJME_hourly.csv", _csv())},
        "kaggle:robikscube/hourly-energy-consumption"),
    "beijing_pm25": (_pm25, "UCI Beijing PM2.5, hourly", {
        "PRSA_data_2010.1.1-2014.12.31": ("PRSA_data_2010.1.1-2014.12.31.csv", _csv())},
        "https://archive.ics.uci.edu/static/public/381/beijing+pm2+5+data.zip"),
    "jena": (_jena, "Jena climate, temperature, 10 min → hourly", {
        "jena_climate_2009_2016": ("jena_climate_2009_2016.csv", _csv())},
        "https://storage.googleapis.com/tensorflow/tf-keras-datasets/jena_climate_2009_2016.csv.zip"),
    "metro": (_metro, "UCI Metro Interstate traffic volume, hourly", {
        "Metro_Interstate_Traffic_Volume": ("Metro_Interstate_Traffic_Volume.csv", _csv())},
        "https://archive.ics.uci.edu/static/public/492/metro+interstate+traffic+volume.zip"),
    "bike": (_bike, "UCI Bike Sharing, hourly rentals cnt", {
        "hour": ("hour.csv", _csv()), "day": ("day.csv", _csv())},
        "https://archive.ics.uci.edu/static/public/275/bike+sharing+dataset.zip"),
    "bitcoin": (_bitcoin, "Bitcoin 1-min OHLCV (Kaggle mczielinski), log close → hourly", {
        "btcusd_1-min_data": ("btcusd_1-min_data.csv", _csv())},
        "kaggle:mczielinski/bitcoin-historical-data"),
}

for _name, (_load, _desc, _files, _src) in BUILTIN.items():
    R.datasets.register(_name, DatasetSpec(_load, _desc, _files, _src))


# ─────────────────────── raw: download and convert ─────────────────────────
def convert_raw(cfg, names=None, remove_original: bool = True) -> list[str]:
    """Original CSV / TXT → lossless Parquet next to it (float64 kept, zstd). The original is
    removed only after the row count of the Parquet file is verified."""
    done = []
    for name in names or cfg.datasets:
        spec = R.datasets.get(name)
        for pq_name, (orig, reader) in spec.raw_files.items():
            src, dst = cfg.raw_dir / name / orig, raw_path(cfg, name, pq_name)
            if dst.exists() or not src.exists():
                continue
            df = reader(src)
            df.columns = [str(c) for c in df.columns]
            write_table(df, dst, keep64=df.columns)
            if len(read_table(dst)) != len(df):
                raise RuntimeError(f"row count mismatch after converting {src}")
            if remove_original:
                os.remove(src)
            done.append(str(dst))
    return done


def download_raw(cfg, names=None) -> None:
    """Download the original files of built-in datasets (Kaggle ones need ~/.kaggle/kaggle.json),
    then convert them to Parquet."""
    import json
    import urllib.request

    for name in names or cfg.datasets:
        spec = R.datasets.get(name)
        d = cfg.raw_dir / name
        d.mkdir(parents=True, exist_ok=True)
        if all(raw_path(cfg, name, f).exists() for f in spec.raw_files):
            continue
        url = spec.source
        if url.startswith("kaggle:"):
            cred = json.loads((Path.home() / ".kaggle" / "kaggle.json").read_text())
            req = urllib.request.Request(f"https://www.kaggle.com/api/v1/datasets/download/{url[7:]}")
            import base64

            tok = base64.b64encode(f"{cred['username']}:{cred['key']}".encode()).decode()
            req.add_header("Authorization", f"Basic {tok}")
            data = urllib.request.urlopen(req).read()
        else:
            data = urllib.request.urlopen(url).read()
        wanted = {orig for orig, _ in spec.raw_files.values()}
        if url.endswith(".csv"):
            (d / Path(url).name).write_bytes(data)
        else:
            with zipfile.ZipFile(io.BytesIO(data)) as z:
                for member in z.namelist():
                    base = Path(member).name
                    if base in wanted:
                        (d / base).write_bytes(z.read(member))
                    elif base.endswith(".gz") and base[:-3] in wanted:          # metro ships .csv.gz
                        import gzip

                        (d / base[:-3]).write_bytes(gzip.decompress(z.read(member)))
    convert_raw(cfg, names)
