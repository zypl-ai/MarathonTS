# Dataset licences

Licences of the datasets from [DATASETS.md](DATASETS.md) and how they apply to the artifacts of the
benchmark (`artifacts/<profile>/`). This file covers data and artifacts only; the code is licensed
separately. It records the licence terms and the decisions of this project; it is not legal advice.

The "Verified" column shows where the licence was checked against the source (October 2026).

| # | Dataset | Licence | Verified | Commercial use | Sharing adapted material | Obligations |
|---|---|---|---|---|---|---|
| 1 | ETTh1 | **CC BY-ND 4.0** | [LICENSE](https://github.com/zhouhaoyi/ETDataset/blob/main/LICENSE) file in the repository | yes | **not permitted** by the licence (see below what this project withholds) | credit the authors (Zhou et al., 2021) |
| 2 | Electricity Load Diagrams 2011–2014 | CC BY 4.0 | [UCI page](https://archive.ics.uci.edu/dataset/321/electricityloaddiagrams20112014) | yes | yes | credit the author and the source, indicate changes |
| 3 | Household Electric Power Consumption | CC BY 4.0 | [UCI page](https://archive.ics.uci.edu/dataset/235/individual+household+electric+power+consumption) (DOI 10.24432/C58K54) | yes | yes | credit the authors and the source, indicate changes |
| 4 | PJM Hourly Energy Consumption | CC0 1.0 (Public Domain) | Kaggle metadata (`robikscube/hourly-energy-consumption`); primary source — see below | yes | yes | none (attribution desirable) |
| 5 | Beijing PM2.5 | CC BY 4.0 | [UCI page](https://archive.ics.uci.edu/dataset/381/beijing+pm2+5+data) | yes | yes | credit the authors (Liang et al., 2015), indicate changes |
| 6 | Jena Climate 2009–2016 | CC BY 4.0 | [MPI-BGC data download page](https://www.bgc-jena.mpg.de/wetter/weather_data.html): "Terms of Use (as per Creative Commons CC-BY-4.0)" | yes | yes | credit the Max Planck Institute for Biogeochemistry, indicate changes |
| 7 | Metro Interstate Traffic Volume | CC BY 4.0 | [UCI page](https://archive.ics.uci.edu/dataset/492/metro+interstate+traffic+volume) | yes | yes | credit the author and the source, indicate changes |
| 8 | Bike Sharing | CC BY 4.0 | [UCI page](https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset) | yes | yes | credit the authors (Fanaee-T, Gama), indicate changes |
| 9 | Bitcoin Historical Data | **CC BY-SA 4.0** | Kaggle API metadata (`mczielinski/bitcoin-historical-data`); primary source — see below | yes | yes, **under CC BY-SA 4.0** | credit the author, indicate changes; adapted material under CC BY-SA 4.0 |

## Licence terms that matter here

- **CC BY-ND 4.0 (ETTh1).** The licence allows sharing the dataset unchanged, and producing adapted
  material, but not sharing adapted material (§2(a)(1)(B), §3(a)(2)). Adapted material is material
  derived from the dataset and modified "in a manner requiring permission under Copyright and Similar
  Rights". Whether numeric measurements, synthetic series sampled from a generator trained on them, or
  the generator weights are adapted material in this sense is not settled. This project takes the
  conservative reading and withholds them (next section).
- **CC BY-SA 4.0 (Bitcoin).** Adapted material may be shared under CC BY-SA 4.0 (or a later version,
  or a licence listed as BY-SA compatible), with attribution and an indication of changes, and
  without additional terms or technical measures that restrict the rights the licence grants.
- **CC BY 4.0.** Adapted material may be shared under any licence, with attribution, a link to the
  licence and an indication of changes.
- **CC0 1.0 (PJM).** No conditions on the Kaggle copy. The primary source (PJM) restricts
  redistribution of its data and of data derived from them (see "Primary sources"); this project
  withholds the artifacts derived from PJM data on the same basis as ETTh1 (next section).

Metrics, tables, rankings and plots computed from a dataset report results about the data and do not
reproduce it; they are published for all nine datasets, with attribution.

## What is published

`<ds>` is a dataset folder. "Derived from data" means the file contains values computed from the
real series or from a model trained on it.

| Artifact | Content | Derived from data | ETTh1, PJM | Bitcoin | Other datasets |
|---|---|---|---|---|---|
| `tables/`, `reports/`, `overall/`, `leaderboard/`, `metric_values/`, `hypotheses/` | metrics, metric values, rankings, tests, reports | results only | published | published | published |
| `fidelity/<ds>/`, `records/<ds>/` | metrics of each series; time, memory, diagnostics | results only | published | published | published |
| `utility/<ds>/…/metrics.parquet` | utility metrics | results only | published | published | published |
| `labels/<ds>/` | real test labels and targets (regression targets are values of the real series) | yes | **withheld** | CC BY-SA 4.0 | dataset licence |
| `series/<ds>/`, `pools/<ds>/` | synthetic series, pools of synthetic windows | yes | **withheld** | CC BY-SA 4.0 | dataset licence |
| `generators/<ds>/` | weights of generators trained on the dataset | yes | **withheld** | CC BY-SA 4.0 | dataset licence |
| `utility/<ds>/…/models.parquet`, `predictions.parquet` | weights of models trained on real or synthetic data; predictions on real test rows | yes | **withheld** | CC BY-SA 4.0 | dataset licence |

"Dataset licence" means: under CC BY 4.0 with the attribution below.
Withheld ETTh1 and PJM artifacts are reproduced locally by running the pipeline ([GETTING_STARTED.md](GETTING_STARTED.md)); everything
that the hypothesis testing reads from them is regenerated by the same stages.

Data files themselves (`data/raw/`, `data/processed/`) are not distributed for any dataset: the
`raw` stage downloads them from the sources.

## Attribution and changes

Synthetic series and other adapted material in `artifacts/` are based on the datasets listed above,
by their respective authors (see the table and [DATASETS.md](DATASETS.md)). Changes made to the
data: one target column was taken, aggregated to an hourly step (mean, or last log price for
Bitcoin), missing Bike hours were set to 0, Metro was taken after its 2014–2015 gap, gaps of up to
6 hours were interpolated, the last points of the series were taken
(`max_points`; Bitcoin between `bitcoin_start` and `bitcoin_end`), the series was split in time and
min-max scaled on train; synthetic series were generated by the methods of the benchmark. The data are
provided as is, without warranties, as stated in the source licences.

## Primary sources

The licence is set by whoever published the dataset; the primary data may have their own terms.
Checked against the sources in October 2026.

- **PJM (#4):** the Kaggle dataset states that the data come from the PJM website. PJM's current
  data service, [Data Miner 2](https://dataminer2.pjm.com/), states that redistribution of information
  or data contained in or derived from Data Miner 2 requires a PJM-issued Redistribution License, and
  its [terms](https://www.pjm.com/-/media/DotCom/etools/edatafeed/data-license-agreement-edata-feed-data-miner-2.pdf)
  limit non-members to internal business use. The Kaggle dataset does not state through which PJM
  service the data were obtained. The benchmark does not distribute the PJM data (`raw` downloads them
  from Kaggle); whether these terms apply to artifacts derived from the Kaggle copy is a legal question
  for the publisher of the artifacts; this project does not distribute artifacts derived from PJM data
  ("What is published").
- **Bitcoin (#9):** the Kaggle dataset acknowledges the Bitstamp API as its source. The
  [Bitstamp API page](https://www.bitstamp.net/api/) states: "Bitstamp allows the incorporation and
  redistribution of our exchange data for commercial purposes. This includes the right to create
  ratios, calculations, new original works, statistics, and similar, based on the exchange data", and
  directs companies using the exchange data for their own commercial purposes to sign a commercial
  Data License Agreement (partners@bitstamp.net).
- **Jena (#6):** the file is taken from the Keras / TensorFlow mirror of the MPI-BGC data; the licence
  (CC BY 4.0) is stated on the MPI-BGC data download page.
- **Household (#3):** CC BY 4.0 is stated on the UCI dataset page.
- **ETTh1 (#1):** permission from the authors to share synthetic series would lift the restriction
  above; it has not been requested.

## Outputs of pretrained models

The series of the long-series generators are outputs of pretrained models whose weights are
downloaded from Hugging Face (not distributed here); their licences set terms on the use of the models
and, for TimesFM, of their outputs. Checked against the licence files in October 2026.

| Model | Licence | Terms on outputs | Other terms |
|---|---|---|---|
| Chronos (`amazon/chronos-t5-small`; `-base` in `max`) | [Apache 2.0](https://huggingface.co/amazon/chronos-t5-small) | none | — |
| TimesFM 3.0 (`google/timesfm-3.0-pytorch`) | [TimesFM Non-Commercial License v1.0](https://huggingface.co/google/timesfm-3.0-pytorch/blob/main/LICENSE) | outputs (predictions and other results) may not be used for commercial or production purposes; outputs are not Derivatives of the model | Non-Commercial Purpose: testing, evaluation or research not tied to commercial gain, including benchmarking on public datasets, provided the results are not used in commercial decision-making, client deliverables or paid products or services |
| Timestral 209M (`mistralai/Timestral-209M`) | [Modified MIT](https://huggingface.co/mistralai/Timestral-209M/blob/main/LICENSE) | none stated | no rights under the licence for a company whose global consolidated monthly revenue exceeds 20 million USD (a commercial licence from Mistral AI otherwise); the attribution notice must accompany copies of the model |

The benchmark runs TimesFM 3.0 for research and evaluation (a Non-Commercial Purpose of its licence).
The outputs are not Derivatives of the model, and the licence does not restrict their distribution
for non-commercial purposes. The series of `timesfm` (`series/<ds>/timesfm/`) are published with the
notice that they are outputs of TimesFM 3.0 and may not be used for commercial or production purposes
(TimesFM Non-Commercial License v1.0); the dataset terms above apply to them as well.
