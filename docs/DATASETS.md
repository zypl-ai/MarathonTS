# Datasets for the experiments

Open datasets on which the methods from [BASELINES.md](BASELINES.md) are compared by the
metrics from [METRICS.md](METRICS.md). Licences are listed in [DATASET_LICENSES.md](DATASET_LICENSES.md).

## Principle: the same datasets for all tasks

All utility tasks (U2.1–U2.9) are built from **a single target series** of a dataset, so every
dataset below is used in all 14 tasks (nine task groups U2.1–U2.9) — there is one set of datasets for the whole experiment.
To this end, for all datasets:

- a single target column is chosen (channel 0 of the pipeline);
- the step is brought to one hour (aggregation by mean or sum), the calendar is the hour of week (BENCHMARK.md, Protocol: data);
- the length after aggregation is ≥ 17,000 hours: with a 60 / 20 / 20 split (train / val / OOT, profile
  `max`, the full series) and `T = 168` this gives `K ≥ 60` windows, enough for h = 168 and for events with
  q = 0.99. Profiles `min` and `mid` take the last 10,000 hourly points of every dataset with a 50 / 25 / 25
  split: 9,664 points after the embargoes, train 5,000, val = OOT = 2,332, `K = 30` (`artifacts/run_h200/tables/datasets.parquet`).

## Tasks (from METRICS.md, U2)

| ID | Task | Type |
|---|---|---|
| U2.1 | Upper tail: change over h = 24 above the 0.90 quantile | binary classification |
| U2.2 | The same at horizons h ∈ {1, 6, 168} | binary classification |
| U2.3 | Rare events: q ∈ {0.95, 0.99} | binary classification (strong imbalance) |
| U2.4 | Lower tail: change below the 0.10 quantile | binary classification |
| U2.5 | Down / neutral / up | multiclass classification (3 classes) |
| U2.6 | Value `x[t+h]`, h ∈ {1, 24, 168} | regression |
| U2.7 | Quantiles 0.1 / 0.5 / 0.9 at horizon h = 24 | quantile regression |
| U2.8 | Vector `x[t+1 : t+24]` | multi-step regression |
| U2.9 | std over the next 24 hours | regression (volatility) |

Every dataset below is used in **all** tasks U2.1–U2.9.

## Summary table

`Columns` — in the source file. `Hours` — length of the target series after conversion to an hourly step.
`K` — approximate number of assembled windows with train = 60% and T = 168 (profile `max`; `min` and `mid`: K = 30 for every dataset).

| # | Dataset | File | Columns | Rows in file | Source step | Hours | K | Target column | Tasks |
|---|---|---|---|---|---|---|---|---|---|
| 1 | ETTh1 | `ETTh1.csv` | 8 | 17,420 | 1 h | 17,420 | ≈ 62 | `OT` | U2.1–U2.9 |
| 2 | Electricity Load Diagrams | `LD2011_2014.txt` | 371 | 140,256 | 15 min | 35,065 | ≈ 125 | sum over 370 clients | U2.1–U2.9 |
| 3 | Household Electric Power Consumption | `household_power_consumption.txt` | 9 | 2,075,259 | 1 min | ≈ 34,590 | ≈ 124 | `Global_active_power` | U2.1–U2.9 |
| 4 | PJM Hourly Energy Consumption (PJME) | `PJME_hourly.csv` | 2 | 145,366 | 1 h | 145,392 | ≈ 519 | `PJME_MW` | U2.1–U2.9 |
| 5 | Beijing PM2.5 | `PRSA_data_2010.1.1-2014.12.31.csv` | 13 | 43,824 | 1 h | 43,800 | ≈ 156 | `pm2.5` | U2.1–U2.9 |
| 6 | Jena Climate 2009–2016 | `jena_climate_2009_2016.csv` | 15 | 420,551 | 10 min | ≈ 70,000 | ≈ 250 | `T (degC)` | U2.1–U2.9 |
| 7 | Metro Interstate Traffic Volume | `Metro_Interstate_Traffic_Volume.csv` | 9 | 48,204 | 1 h (with gaps) | ≈ 29,000 (after skipping 2014–2015) | ≈ 103 | `traffic_volume` | U2.1–U2.9 |
| 8 | Bike Sharing (hourly) | `hour.csv` | 17 | 17,379 | 1 h | 17,544 by calendar | ≈ 63 | `cnt` | U2.1–U2.9 |
| 9 | Bitcoin Historical Data | `btcusd_1-min_data.csv` | 6 | 7,767,566 | 1 min | ≈ 85,000 (2017-01 – 2026-10) | ≈ 305 | `Close` (log price) | U2.1–U2.9 |

Columns and rows in the files have been checked against the downloaded data (`data/raw/`, October 2026; Bitcoin
is updated daily, so the number of rows grows). `Hours` runs from the first to the last valid hourly value, gaps included. Values marked ≈ are rounded.

The files are stored in `data/raw/<dataset>/` as Parquet (zstd, lossless: all source columns, float64):
`ett/`, `electricity/`, `household/`, `pjm/` (together with the other PJM regions), `beijing_pm25/`,
`jena/`, `metro/`, `bike/` (together with `day.parquet` and `Readme.txt`), `bitcoin/`. In total ≈ 200 MB
versus 1.3 GB of source CSV. The data are not included in the repository: the stage `python -m marathonts.bench.run raw`
downloads the source files (Kaggle — with `~/.kaggle/kaggle.json`) and converts them to Parquet.
Column names in the table above are the original ones; the number of rows matches the source files.

## Descriptions

### 1. ETTh1 — Electricity Transformer Temperature

Loads and oil temperature of a power transformer in China, July 2016 – June 2018, 1-hour step.
Columns: `date`, six loads (`HUFL`, `HULL`, `MUFL`, `MULL`, `LUFL`, `LULL`) and the oil
temperature `OT`. A standard long-horizon forecasting benchmark (Informer, Autoformer, etc.), with no missing values.
The shortest in the set — the lower bound on length.

- Source: [github.com/zhouhaoyi/ETDataset](https://github.com/zhouhaoyi/ETDataset), file `ETT-small/ETTh1.csv`
- Paper: Zhou H. et al. *Informer: Beyond efficient transformer for long sequence time-series forecasting*. AAAI 2021

### 2. Electricity Load Diagrams 2011–2014

Electricity consumption of 370 clients in Portugal, 2011–2014, kW per 15 minutes. The first column is
the time, the rest are clients; separator `;`, decimal comma. Clients connected later
have zeros at the start. The target series is the total load aggregated to hours: strong daily and
weekly seasonality.

- Source: [UCI #321](https://archive.ics.uci.edu/dataset/321/electricityloaddiagrams20112014)
- Author: Trindade A., 2015

- **Leakage for Chronos:** the Chronos training corpus contains this dataset (Electricity 15 min, hourly
  and weekly, all 370 clients, without only the last 24 points; Ansari et al., *Chronos: Learning the
  Language of Time Series*, TMLR 2024, Table 3). The benchmark's target is the sum of the clients, so
  Chronos has seen the val and OOT periods of this series in aggregated form; its results on
  `electricity` are not out-of-sample.

### 3. Individual Household Electric Power Consumption

Consumption of a single household in France, December 2006 – November 2010, 1-minute step. Columns:
`Date`, `Time`, active and reactive power, voltage, current, three sub-meters. About 1.25% of the rows
are missing (marked `?`). The target series is the hourly mean of `Global_active_power`. A noisy series with
sharp peaks — a test on irregular dynamics.

- Source: [UCI #235](https://archive.ics.uci.edu/dataset/235/individual+household+electric+power+consumption)
- Authors: Hébrail G., Bérard A., 2012
- **Leakage for TimesFM:** the TimesFM 3.0 training data (GiftEvalPretrain) include this dataset as
  `sceaux` (from BuildingsBench): one hourly series, 2007-01-01 – 2010-11-26, equal to the hourly mean of
  `Global_active_power` on every common hour after a 1-hour label shift. TimesFM is left out on
  `household` (`Config.leaked`).

### 4. PJM Hourly Energy Consumption (PJME)

Hourly consumption of the PJM East region (USA), 2002–2018, megawatts. The set also contains ~12 files for
other PJM regions in the same format (`Datetime`, `<REGION>_MW`). The longest series in the set
(largest K). There are isolated duplicates and gaps at the transitions to daylight saving
time.

- Source: [kaggle.com/datasets/robikscube/hourly-energy-consumption](https://www.kaggle.com/datasets/robikscube/hourly-energy-consumption)
- Primary data: PJM Interconnection LLC

### 5. Beijing PM2.5

PM2.5 concentration at the US Embassy in Beijing and airport weather, 2010–2014, 1-hour step. Columns:
`No`, `year`, `month`, `day`, `hour`, `pm2.5`, `DEWP`, `TEMP`, `PRES`, `cbwd`, `Iws`, `Is`, `Ir`.
`pm2.5` has about 2000 missing values. A heavy right tail and smog episodes (tail tasks U2.1–U2.4).

- Source: [UCI #381](https://archive.ics.uci.edu/dataset/381/beijing+pm2+5+data)
- Paper: Liang X. et al. *Assessing Beijing's PM2.5 pollution: severity, weather impact, APEC and winter heating*. Proc. Royal Society A 471, 2015
- **Leakage for TimesFM:** the TimesFM 3.0 training data (GiftEvalPretrain, built on LOTSA) include
  "Beijing Air Quality" (UCI #501: PM2.5 and weather of 12 Beijing stations, March 2013 – February 2017).
  It is another file, but the same city, pollutant and hours as this series over 2013–2014 — the period
  of the `min` window. TimesFM is left out on `beijing_pm25` (`Config.leaked`).
- **Leakage for Chronos:** the Chronos training corpus includes KDD Cup 2018 (air quality of Beijing and
  London stations, January 2017 – March 2018; Benchmark I of Ansari et al., 2024). Same city and
  pollutant, other stations and years: a related pair, so Chronos is left out on `beijing_pm25` too.

### 6. Jena Climate 2009–2016

Weather station of the Max Planck Institute for Biogeochemistry (Jena), 2009–2016, 10-minute step, 14 variables:
pressure, temperature, humidity, wind, etc. The target series is temperature averaged to hours.
Strong daily and yearly seasonality with weak weekly seasonality — a check that the "hour of week" calendar
does not impose spurious structure.

- Source: [Max Planck BGC Jena](https://www.bgc-jena.mpg.de/wetter/); ready-made file —
  [jena_climate_2009_2016.csv.zip](https://storage.googleapis.com/tensorflow/tf-keras-datasets/jena_climate_2009_2016.csv.zip) (Keras / TensorFlow)

### 7. Metro Interstate Traffic Volume

Hourly westbound traffic on I-94 (Minneapolis – St Paul), October 2012 – September
2018, plus weather and holidays. Columns: `holiday`, `temp`, `rain_1h`, `snow_1h`, `clouds_all`,
`weather_main`, `weather_description`, `date_time`, `traffic_volume`. There are duplicate hours (several
weather descriptions) and a large gap in 2014–2015. The duplicate hours are averaged, and the series
starts after the last gap longer than 30 days (June 2015). Very strong weekly structure.

- Source: [UCI #492](https://archive.ics.uci.edu/dataset/492/metro+interstate+traffic+volume)
- Author: Hogue J., 2019

### 8. Bike Sharing (hourly)

Hourly number of Capital Bikeshare bicycle rentals (Washington, D.C.), 2011–2012, with weather and
calendar. Columns of `hour.csv`: `instant`, `dteday`, `season`, `yr`, `mnth`, `hr`, `holiday`,
`weekday`, `workingday`, `weathersit`, `temp`, `atemp`, `hum`, `windspeed`, `casual`,
`registered`, `cnt`. Several hours are missing (zero demand) and are set to 0. Count
data with a trend between years.

- Source: [UCI #275](https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset)
- Paper: Fanaee-T H., Gama J. *Event labeling combining ensemble detectors and background knowledge*. Progress in Artificial Intelligence 2(2–3), 113–127, 2014

### 9. Bitcoin Historical Data

Minute-level OHLCV data for BTC/USD (Bitstamp), from 2012 to the present. Columns: `Timestamp`,
`Open`, `High`, `Low`, `Close`, `Volume`. Before 2017 many minutes have no trades; the series is taken
from `bitcoin_start` = 2017-01-01 to `bitcoin_end` = 2026-10-01 (exclusive). The target series is the log of the hourly close price. A financial series: weak seasonality,
volatility clustering, heavy-tailed increments.

- Source: [kaggle.com/datasets/mczielinski/bitcoin-historical-data](https://www.kaggle.com/datasets/mczielinski/bitcoin-historical-data)
- Author: Mark Zielinski (Kaggle display name "Zielak"; the full name is that of the GitHub account
  [mczielinski](https://github.com/mczielinski/kaggle-bitcoin) linked from the dataset description)
- **Leakage for TimesFM:** GiftEvalPretrain includes the Monash "Bitcoin" set (18 daily series, among
  them the Bitcoin price, 2009 – mid-2021). The same asset at a daily resolution: a related pair, so
  TimesFM is left out on `bitcoin` in every profile — also in `min`, whose window (2025–2026) lies after
  it (`Config.leaked`).

## Leakage into pretrained models

A dataset whose object is in a pretrained model's training data is not out-of-sample for it: the method
is left out on that dataset in every ranking, question and case-study test (`Config.leaked`,
`bench.config.LEAKED`); the other methods keep every dataset. The analysis always applies the list of the
current code (not the copy saved with the tables), so a pair added later takes effect on the next run of
notebook 7 without recomputing anything; `--leaked` replaces it from the command line.

**Rule.** Left out are both
- **exact** pairs: the same data, the same source series, in the training corpus;
- **related** pairs: the same object — the same dataset, the same city and pollutant, the same asset —
  at other stations, years or resolution, whether or not the periods overlap with the benchmark window.

Kept are pairs that share only the phenomenon (bike rentals in another city, gridded weather reanalysis)
and datasets that a model uses only for evaluation.

The audit (October 2026) checked every model × dataset pair against the primary sources: Chronos — the
paper's Appendix B, Table 3 (pretraining = pretraining-only sets + Benchmark I; Benchmark II is
zero-shot evaluation only); TimesFM 3.0 — the model card and the full list of GiftEvalPretrain
sub-datasets (Hugging Face `Salesforce/GiftEvalPretrain`, LOTSA builders of `uni2ts`), with the candidate
sub-datasets downloaded and compared with the benchmark's raw files; Timestral — the model card and
the release note.

| Model | Training data (source) | Left out on |
|---|---|---|
| Chronos T5 (small; base in `max`, same training corpus) | Ansari et al., TMLR 2024, Appendix B, Table 3 | `electricity` (exact), `beijing_pm25` (related: KDD Cup 2018) |
| TimesFM 3.0 | model card: GiftEvalPretrain (without GIFT-Eval test sets and fev-bench overlaps), Wikipedia Pageviews, Google Trends, synthetic | `household` (exact: `sceaux`), `beijing_pm25` (related: Beijing Air Quality), `bitcoin` (related: Monash Bitcoin) |
| Timestral 209M | technical report (Petralia et al., 2026): pretraining on synthetic data only; post-training on a mix of real and synthetic data, the real data not listed | — unknown, cannot be checked (kept) |
| Diffusion-TS, VAE | trained by the benchmark on train only | — |

Every pair of the audit (exact / related / weak / none / unknown):

| Dataset | Chronos T5 | TimesFM 3.0 | Timestral 209M |
|---|---|---|---|
| ETTh1 | none: zero-shot evaluation only (Benchmark II) | none: GIFT-Eval test set, not in GiftEvalPretrain | unknown |
| electricity | **exact**: Electricity 15 min / hourly / weekly in Benchmark I | none: GIFT-Eval test set | unknown |
| household | none (London Smart Meters only: other households) | **exact**: `sceaux` = UCI #235, hourly 2007-01 – 2010-11, equal to the hourly mean of `Global_active_power` on every common hour (after a 1-hour label shift) | unknown |
| pjm | none | none found: no GiftEvalPretrain series equals any of the 11 PJM regions; `pdb` (public Kaggle set of undocumented origin, 2013–2014) correlates with PJME (r = 0.945) — origin unresolved | unknown |
| beijing_pm25 | **related**: KDD Cup 2018 (Beijing and London stations, 2017-01 – 2018-03) | **related**: Beijing Air Quality (UCI #501, 12 stations, 2013-03 – 2017-02; station correlations with our series 0.81–0.96) | unknown |
| jena | weak: WeatherBench gridded reanalysis only | weak: gridded ERA5 / CMIP6 only (jena_weather is a GIFT-Eval test set) | unknown |
| metro | none (traffic sets are PeMS, evaluation only) | none (California and China traffic sets) | unknown |
| bike | weak: Mexico City Bikes (another city) | none | unknown |
| bitcoin | none | **related**: Monash Bitcoin, daily `price`, 2009 – mid-2021 | unknown |

Timestral declares no GIFT-Eval test-data leakage on the GIFT-Eval leaderboard (zero-shot), which weakly
covers ETTh1, electricity and Jena; the other pairs cannot be checked. Earlier TimesFM versions differ
(1.0 / 2.0 also trained on Electricity and the Jena weather data): the benchmark uses 3.0 only.

## How the datasets differ (why there are nine)

| Property | Datasets |
|---|---|
| Strong weekly seasonality | Electricity, PJME, Metro, Bike |
| Strong daily, weak weekly | Jena, ETTh1 |
| Heavy tails, spikes | PM2.5, Household, Bitcoin |
| Volatility clustering, weak seasonality | Bitcoin |
| Trend / level drift | Bike, ETTh1, Bitcoin |
| Gaps and duplicates requiring preprocessing | Household, PM2.5, Metro, Bike, PJME |
| Short (K ≈ 60) | ETTh1, Bike |
| Long (K ≥ 250) | PJME, Jena, Bitcoin |
