# Getting started

This guide installs MarathonTS and runs it in one of three ways: Docker ([Guide A](#guide-a-docker)), Google
Colab notebooks ([Guide B](#guide-b-google-colab)) or local virtual environments
([Guide C](#guide-c-local-environments)). Each guide ends with the same three runs: a smoke test, the full run
of profile `min`, and re-running only the analysis on existing tables. How to change settings is in
[CONFIGURATION.md](CONFIGURATION.md), how to add components in [EXTENDING.md](EXTENDING.md), and the pipeline,
protocol and artifacts in [BENCHMARK.md](BENCHMARK.md).

The pipeline has eight stages; stages 0–6 are `python -m marathonts.bench.run <stage>`, stage 7 is
`python -m marathonts.hypotheses.run`:

| # | Stage | Writes |
|---|---|---|
| 0 | `raw` | `data/raw/<ds>/*.parquet` (download if missing, CSV / TXT → Parquet) |
| 1 | `prepare` | `data/processed/<profile>/` (hourly series, split, scaling) |
| 2 | `pools` | `artifacts/<profile>/pools/`, `generators/` (pool generator, in its own environment) |
| 3 | `generate` | `artifacts/<profile>/series/`, `records/`, `generators/` |
| 4 | `fidelity` | `artifacts/<profile>/fidelity/` |
| 5 | `utility` | `artifacts/<profile>/labels/`, `utility/` |
| 6 | `collect` | `artifacts/<profile>/tables/` |
| 7 | `hypotheses.run` | `artifacts/<profile>/reports/`, `overall/`, `leaderboard/`, `metric_values/`, `hypotheses/` |

`python -m marathonts.bench.run all` runs stages 0–6 in this order. Two further stages, `targets` and `hashes`, are run on
their own and are not part of `all` ([BENCHMARK.md](BENCHMARK.md), stages 1a and 1b).

## Requirements

### Operating system and Python

- Linux or macOS. The run records use the Unix module `resource` (`marathonts/bench/timing.py`); on Windows use Docker or
  WSL.
- Python 3.11 or 3.12 for local environments; the Docker images use Python 3.11 (`tsgm`: `python:3.11-slim`;
  `bench`: `pytorch/pytorch:2.5.1-cuda12.4-cudnn9-runtime`).
- The `tsgm` environment (the VAE pool generator, `tsgm==0.1.0`) installs with pip on Python ≤ 3.12. On
  Python 3.13 the `setup.py` of tsgm 0.1.0 fails while reading its version; `install_tsgm()` in
  `colab/colab_setup.py` installs it with a one-line patch (used by the Colab notebooks). The single environment
  of `requirements.txt` therefore needs Python ≤ 3.12.
- `git` on the path: Diffusion-TS is cloned from GitHub, and `envs/timestral.txt` installs `timestral` from a
  pinned commit of its Git repository.

### GPU

Every stage runs on CPU; a CUDA GPU shortens the stages marked below. The torch part selects CUDA when it is
available (`Config.device = None`; `--device cpu` forces the CPU), TensorFlow uses a GPU when it sees one.
Apple MPS and TPU are not used.

| Stage | Device |
|---|---|
| `raw`, `prepare`, `collect`, `hypotheses.run` | CPU |
| `pools` | the VAE (TensorFlow) on GPU if TensorFlow sees one, else CPU |
| `generate` | assemblers (torch), Diffusion-TS training and sampling, Chronos, TimesFM, Timestral on CUDA if available |
| `fidelity` | distance metrics (MMD, nearest neighbours, precision / recall) and the GRU discriminator (F6.1) on CUDA if available |
| `utility` | `linear` and `mlp` (torch) on CUDA if available; `gbdt` (XGBoost) on the device of `marathonts/bench/model_configs.json` — `"cpu"` in `min` and `mid`, `"auto"` (CUDA if available) in `max` |

Timing results (RQ6) compare wall times, so all methods of a dataset are to be run on the same hardware type;
`collect` warns when the series were made on more than one GPU type. Of the two published runs, the main run
used one NVIDIA H200 and the replication run one NVIDIA L4 ([BENCHMARK.md](BENCHMARK.md#published-runs)).

### Disk space and time

- Raw data: about 200 MB of Parquet in `data/raw/` after conversion (1.3 GB of source files are downloaded and
  deleted after conversion; [DATASETS.md](DATASETS.md)).
- Artifacts of a full `min` run: about 5 GB for the methods of the replication run (`artifacts/run_l4/tables/inventory.parquet` lists every file with its
  size), most of it utility predictions and model weights — about 2 MB of predictions and 0.9 MB of weights per
  utility unit ([BENCHMARK.md](BENCHMARK.md), "Artifacts"). `Config.save_model_weights=False` or
  `weights_dtype="float16"` reduce it.
- Compute: 9 datasets × 10 seeds × 12 methods = 1080 series in `min` ([BENCHMARK.md](BENCHMARK.md),
  "Compute volume"). The longest single step is the Diffusion-TS training: 1.1–1.6 h per dataset on an NVIDIA
  L4 in the replication run of `min` (9 trainings; 90 in `max`). Utility is the stage with the most fits (29 fits
  per unit in `min`, each tested on 2 splits).

### Credentials and network

- **Kaggle** — two datasets are downloaded through the Kaggle API: `pjm` (`robikscube/hourly-energy-consumption`)
  and `bitcoin` (`mczielinski/bitcoin-historical-data`). They need an API token in `~/.kaggle/kaggle.json`
  (Kaggle → Settings → API → Create New Token). The other seven datasets, including the two of the smoke test
  (`ett`, `bike`), are downloaded without credentials. Without the token, `raw` logs the failure of these two
  datasets to `artifacts/<profile>/errors.log` and continues with the others. The original files can also be
  placed by hand in `data/raw/pjm/PJME_hourly.csv` and `data/raw/bitcoin/btcusd_1-min_data.csv`: `raw` then
  converts them instead of downloading.
- **Hugging Face** — the pretrained long-series generators download their weights on first use:
  `amazon/chronos-t5-small` (`max`: `amazon/chronos-t5-base`; smoke test: `amazon/chronos-t5-tiny`),
  `google/timesfm-3.0-pytorch`, `mistralai/Timestral-209M` (smoke test: `mistralai/Timestral-5M`). TimesFM and
  Timestral are pinned to revisions (`Config.timesfm_revision`, `timestral_revision`).
- **GitHub** — Diffusion-TS (`https://github.com/Y-debug-sys/Diffusion-TS`, commit
  `566307e6cf2d8095e58de4c6e3a6ae965b69b5b5`) is cloned into `external/Diffusion-TS` (`Config.diffusion_ts_dir`,
  flag `--diffusion-ts-dir`).

## Guide A. Docker

Two images are built from `Dockerfile` and connected by `docker-compose.yml`:

| Service | Image | Contents | Default command |
|---|---|---|---|
| `tsgm` | `marathonts:tsgm` | Python 3.11, TensorFlow (with CUDA libraries), Keras, tsgm; `marathonts/` | `pools --pool-generators tsgm_vae` |
| `bench` | `marathonts:bench` | PyTorch 2.5.1 with CUDA 12.4, `envs/core.txt`, Diffusion-TS (pinned commit, in the image), Chronos, TimesFM, Timestral, SDV; `bench/`, `hypotheses/` | `all` |
| `hypotheses` | `marathonts:bench` | entry point `python -m marathonts.hypotheses.run` | — |

The entry point of `tsgm` and `bench` is `python -m marathonts.bench.run`: everything after the service name is passed to it
(a stage and flags). All three services mount the same host folders:

| Host | Container | Purpose |
|---|---|---|
| `./data` | `/app/data` | raw and processed data |
| `./artifacts` | `/app/artifacts` | every artifact, the tables and the reports |
| `~/.kaggle` | `/root/.kaggle` (read-only) | Kaggle API token |

### A1. Build

```bash
git clone https://github.com/zypl-ai/MarathonTS.git
cd MarathonTS
docker compose build
```

**GPU or CPU.** The `deploy` blocks of `docker-compose.yml` reserve every NVIDIA GPU of the host; this needs
the NVIDIA Container Toolkit. On a machine without an NVIDIA GPU, delete the `deploy: *gpu` lines of the `tsgm`
and `bench` services: everything then runs on CPU. A CPU-only `tsgm` image without the CUDA libraries of
TensorFlow is built with `docker compose build --build-arg TF_EXTRA="" tsgm`.

**Model weights.** Chronos, TimesFM and Timestral download their weights into the container's Hugging Face
cache, which `--rm` removes with the container. Mounting a host folder keeps them between runs, e.g.
`docker compose run --rm -v "$HOME/.cache/huggingface:/root/.cache/huggingface" bench generate`.

### A2. Smoke test

`--quick` selects `Config.quick()`: datasets `ett` and `bike`, seeds 0 and 1, small models, output in
`artifacts/quick/` and `data/processed/quick/`. The VAE pools are made in the `tsgm` image, so the data are
prepared first:

```bash
docker compose run --rm bench raw --quick
docker compose run --rm bench prepare --quick
docker compose run --rm tsgm pools --pool-generators tsgm_vae --quick
docker compose run --rm bench all --quick                       # stages 0–6; the finished ones are skipped
docker compose run --rm hypotheses --artifacts-dir artifacts/quick
```

The reports are in `artifacts/quick/reports/`. With 2 datasets and 2 seeds the report has no global verdicts
(at least 3 datasets are required) and the case study is skipped (its method has no results in this run);
the test checks that every stage runs.

### A3. Full run of profile `min`

```bash
docker compose run --rm bench raw            # download and convert the data (Kaggle: ~/.kaggle)
docker compose run --rm bench prepare
docker compose run --rm tsgm                 # VAE pools in the TensorFlow + tsgm image
docker compose run --rm bench generate       # the assemblers + the long-series generators; pools are read
docker compose run --rm bench fidelity
docker compose run --rm bench utility
docker compose run --rm bench collect
docker compose run --rm hypotheses           # reports → artifacts/min/reports/
```

After the `tsgm` step, `docker compose run --rm bench all` runs the remaining stages in one call (the finished
ones are skipped). Flags go after the stage:

```bash
docker compose run --rm bench generate --datasets ett --seeds 0 1 2          # a part of the run
docker compose run --rm bench generate --methods vae_greedy chronos          # selected methods
docker compose run --rm bench utility --device cpu                           # torch on CPU
```

**Profiles.** `--profile mid` or `--profile max` is added to every stage, including the `tsgm` and `hypotheses`
services:

```bash
docker compose run --rm tsgm pools --pool-generators tsgm_vae --profile max
docker compose run --rm bench all --profile max
docker compose run --rm hypotheses --profile max
```

**Your own configuration.** A JSON file written by `Config.to_json()` with paths relative to the project folder
([CONFIGURATION.md](CONFIGURATION.md#d-a-json-file)) is read from the mounted `artifacts/` folder,
e.g. `docker compose run --rm bench all --config artifacts/my_cfg.json`.

**Plugins.** The images contain only the package `marathonts/`; a plugin file is mounted into `/app` and named
with `--plugins` ([EXTENDING.md](EXTENDING.md#plugin-files)):

```bash
docker compose run --rm -v "$PWD/my_plugins.py:/app/my_plugins.py" bench all --plugins my_plugins.py
docker compose run --rm -v "$PWD/my_plugins.py:/app/my_plugins.py" hypotheses
```

`collect` records the plugin files in `tables/config.json`, and the analysis loads them from there, so the
`hypotheses` service needs the same mount.

### A4. Re-run only the analysis

```bash
docker compose run --rm hypotheses                                   # profile min, artifacts/min/tables
docker compose run --rm hypotheses --exclude-datasets bitcoin        # an analysis-only choice
docker compose run --rm hypotheses --profile max
```

Stage 7 reads `artifacts/<profile>/tables/`, the utility predictions and labels (case study) and
`data/processed/<profile>/` (dataset descriptors of RQ7 and CS15, CS12 subgroups; without it these parts are
skipped). Its flags are listed in [CONFIGURATION.md](CONFIGURATION.md#command-line-of-the-analysis).

### A5. Outputs

Everything is written to the host folders `./data` and `./artifacts`: `artifacts/<profile>/` holds the
per-unit files, `tables/` (stage 6), `reports/` and the analysis tables (stage 7), and `errors.log`
([BENCHMARK.md](BENCHMARK.md), "Artifacts").

## Guide B. Google Colab

The folder `colab/` holds one notebook per stage. All of them read and write one project folder on Google
Drive, so each notebook runs on its own runtime and a disconnected runtime resumes where it stopped.

### B1. Put the project on Google Drive

The notebooks expect the project at `/content/drive/MyDrive/Colab Notebooks/MarathonTS`. Either clone it there
from a Colab cell:

```python
from google.colab import drive
drive.mount("/content/drive")
!git clone https://github.com/zypl-ai/MarathonTS.git "/content/drive/MyDrive/Colab Notebooks/MarathonTS"
```

or upload the project folder to `My Drive/Colab Notebooks/MarathonTS` with the Drive web interface. Another
location works when `REPO` is changed in the setup cell of every notebook. For the Kaggle datasets (`pjm`,
`bitcoin`), put the API token at `REPO/kaggle.json`: notebook 01 copies it to `~/.kaggle/kaggle.json`.

### B2. The setup and scope cells

The first code cells of every notebook mount Drive and set three variables before running
`colab/colab_setup.py`:

```python
REPO = "/content/drive/MyDrive/Colab Notebooks/MarathonTS"   # project folder on Drive (or a git clone)
PROFILE = "min"            # "min": the Colab run (fast); "mid": min + the VAE per seed; "max": everything on
# results go to {REPO}/artifacts/<PROFILE>; set ARTIFACTS = "..." to change
exec(open(f"{REPO}/colab/colab_setup.py").read())
```

`colab_setup.py` installs the main environment once per runtime (`envs/core.txt`, Chronos, TimesFM, Timestral,
Diffusion-TS with a clone of its code into `REPO/external/`), changes the working directory to `REPO` and creates
`cfg = Config.profile(PROFILE)` with `artifacts_dir` set to `ARTIFACTS` when given. `PROFILE` and `ARTIFACTS`
must be the same in every notebook of a run. Notebook 02 sets `MAIN_ENVS = ["base"]`: its runtime gets
`envs/base.txt` and tsgm on top of Colab's TensorFlow (`install_tsgm()`), without the torch stack.

Notebooks 01–06 then have a scope cell that changes `cfg` with `dataclasses.replace` (datasets, methods, seeds,
plugins and the other fields of [CONFIGURATION.md](CONFIGURATION.md#b-the-cfg-cell-of-the-notebooks)). Use the
same scope cell in every notebook of a run: `collect` (06) keeps only the methods and settings of its own `cfg`.

### B3. Notebooks, order and runtime type

Run the notebooks in the order 01 → 07. Set the runtime type before running (Runtime → Change runtime type):

| Notebook | Runtime | What it does | Writes (under `REPO/`) |
|---|---|---|---|
| `01_data.ipynb` | CPU | raw data → Parquet (download if missing), preparation | `data/raw/`, `data/processed/<profile>/` |
| `02_pools.ipynb` | GPU (T4 or better) | VAE pools: tsgm on top of Colab's TensorFlow, the `pools` stage in a subprocess (`run_in_env(None, "pools", ...)`) | `artifacts/<profile>/pools/`, `generators/` |
| `03_generate.ipynb` | GPU, the same type as in 02 | the assemblers (except `frozen_methods`), Diffusion-TS, Chronos, TimesFM, Timestral; time and weights | `series/`, `records/`, `generators/` |
| `04_fidelity.ipynb` | GPU recommended, CPU works | metrics F1–F12 | `fidelity/` |
| `05_utility.ipynb` | GPU (T4 or better) | TSTR and TRTR: models, utility metrics, predictions, model weights | `labels/`, `utility/` |
| `06_collect.ipynb` | CPU | the tables | `tables/` |
| `07_hypotheses.ipynb` | CPU | overall leaderboard, rankings, metric values, research questions, case study | `reports/`, `overall/`, `leaderboard/`, `metric_values/`, `hypotheses/` |

After notebook 02 has finished, close its runtime (Runtime → Disconnect and delete runtime) before opening 03:
notebook 03 never imports TensorFlow and reads the pools from Drive. Errors of single units go to
`artifacts/<profile>/errors.log` (notebook 03 prints its tail) and do not stop the notebook.

**Long stages across sessions.** Re-running a notebook after a disconnect continues where it stopped
([Resuming and re-running](#resuming-and-re-running)). Stages 03–05 can also be divided between sessions by
`datasets=[...]` or `seeds=[...]` in the scope cell; notebook 06 is then run with the full scope.

**Other environments.** `run_in_env("<env>", "<stage>", ...)` runs a stage in a virtual environment built from
`envs/<env>.txt` (created once per runtime) and passes the whole `cfg` as JSON, e.g.
`run_in_env("sdv", "pools", "--pool-generators", "sdv_par", config=cfg)` in notebook 02.

### B4. Smoke test

In notebooks 01–06 add a cell after the scope cell, and in notebook 07 after the setup cell:

```python
cfg = Config.quick()        # ett and bike, seeds 0 and 1, small models → REPO/artifacts/quick/
```

and run 01 → 07 as above. Notebook 07 analyses `cfg.artifacts_dir`, i.e. `artifacts/quick/`.

### B5. Full run of profile `min`

Keep `PROFILE = "min"` and the scope cell as shipped (every dataset of the profile, `seeds=list(range(10))`),
and run 01 → 07. For `mid` or `max`, set `PROFILE` in every notebook.

### B6. Re-run only the analysis

Run notebook 07 alone: it reads `artifacts/<profile>/tables/`. Analysis-only choices are added to the arguments
of `main` in its second code cell, e.g.

```python
main(["--profile", PROFILE, "--artifacts-dir", str(cfg.artifacts_dir), "--exclude-datasets", "bitcoin"])
```

([CONFIGURATION.md](CONFIGURATION.md#analysis-only-settings)).

### B7. Outputs

`REPO/data/` and `REPO/artifacts/<profile>/` on Drive, as in the table of B3; the reports are in
`REPO/artifacts/<profile>/reports/`.

## Guide C. Local environments

Two setups: separate virtual environments, one per dependency set (the layout of the Docker images and the
Colab runtimes), or one environment for everything.

| Environment | File | What runs in it |
|---|---|---|
| base | `envs/base.txt` | `raw`, `prepare`; the basis of the others |
| core | `envs/core.txt` | `generate` (assembly), `fidelity`, `utility`, `collect`, `hypotheses.run` |
| tsgm | `envs/tsgm.txt` | `pools --pool-generators tsgm_vae` (TensorFlow, no torch) |
| diffusion_ts, chronos, timesfm, timestral | `envs/<name>.txt` | `generate --methods <name>`; each is core + its package |
| sdv | `envs/sdv.txt` | `pools --pool-generators sdv_par` (optional pool generator) |

A stage skips a component whose modules are missing in the current environment and names the environment to
run it in (see [Troubleshooting](#troubleshooting)).

### C0. Install the package from PyPI

The benchmark is also the Python package `marathonts` (the core environment; extras for the generators that
have their own requirements):

```bash
pip install "marathonts[chronos,timesfm,diffusion-ts]"     # Python 3.11 or 3.12
```

The VAE pool generator (TensorFlow, `envs/tsgm.txt`) and Timestral (`envs/timestral.txt`) are installed
separately, and Diffusion-TS needs its official code (C1). The package keeps its own files (task thresholds,
model configurations, data hashes); the working folders `data/`, `artifacts/` and `external/` are created in
the project folder: the current directory, or `MARATHONTS_HOME` if it is set. The commands are the same as from
a clone: `python -m marathonts.bench.run <stage>`, `python -m marathonts.hypotheses.run`. To re-run the
analysis of a published run, download its tables from Hugging Face
([BENCHMARK.md](BENCHMARK.md#published-runs)) into `artifacts/run_h200/tables/` and run
`python -m marathonts.hypotheses.run --artifacts-dir artifacts/run_h200`.

### Versions

`envs/*.txt` give flexible versions — a lower bound (the oldest the published runs used) and an upper bound where
a newer version is known to change the results (pandas 3 changes the prepared data) — so that they install on
top of Colab's and the Docker images' own torch and TensorFlow. Two sets of exact versions are kept as well:

| File | What it fixes | Use |
|---|---|---|
| `envs/lock/main-run-core.txt`, `envs/lock/main-run-tsgm.txt` | the environments of the main run (Linux x86_64, Python 3.12.13, torch 2.9.1 with CUDA 12.8, TensorFlow 2.20.0), from its `pip freeze` | to repeat the benchmark stages as they were run; the tsgm file is installed in two steps (its header) |
| `tests/requirements.txt` | the analysis environment | `hypotheses.run` rebuilds the published rankings, questions and reports from the published tables bit for bit (checked by CI) |

Results depend on versions in a few places: newer scipy changes some p-values of RQ4 with tied values, GPU
generations and library builds change the trained generators (the two published runs differ mainly for this
reason, [BENCHMARK.md](BENCHMARK.md#published-runs)).

### C1. Install: separate environments

```bash
git clone https://github.com/zypl-ai/MarathonTS.git
cd MarathonTS

python3.12 -m venv .venv-core
.venv-core/bin/pip install -r envs/core.txt -r envs/diffusion_ts.txt -r envs/chronos.txt \
    -r envs/timesfm.txt -r envs/timestral.txt
python3.12 -m venv .venv-tsgm                    # Python ≤ 3.12 (tsgm 0.1.0)
.venv-tsgm/bin/pip install -r envs/tsgm.txt

git clone https://github.com/Y-debug-sys/Diffusion-TS.git external/Diffusion-TS
git -C external/Diffusion-TS checkout 566307e6cf2d8095e58de4c6e3a6ae965b69b5b5
```

The four long-series generators share the core environment here; when their dependencies conflict, each one gets
its own environment from its file and runs with `generate --methods <name>` there.

### C2. Install: one environment

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt                  # every envs/*.txt; Python ≤ 3.12
git clone https://github.com/Y-debug-sys/Diffusion-TS.git external/Diffusion-TS
git -C external/Diffusion-TS checkout 566307e6cf2d8095e58de4c6e3a6ae965b69b5b5
```

In one environment `python -m marathonts.bench.run all` runs every stage, the VAE pools included (TensorFlow is imported
before torch initialises CUDA). The CUDA builds of TensorFlow and torch may require different cuDNN versions;
the separate environments of C1 avoid this.

### C3. Smoke test

One environment:

```bash
python -m marathonts.bench.run all --quick
python -m marathonts.hypotheses.run --artifacts-dir artifacts/quick
```

Separate environments:

```bash
.venv-core/bin/python -m marathonts.bench.run raw --quick
.venv-core/bin/python -m marathonts.bench.run prepare --quick
.venv-tsgm/bin/python -m marathonts.bench.run pools --pool-generators tsgm_vae --quick
.venv-core/bin/python -m marathonts.bench.run all --quick          # generate, fidelity, utility, collect
.venv-core/bin/python -m marathonts.hypotheses.run --artifacts-dir artifacts/quick
```

The reports are in `artifacts/quick/reports/` (see the note in [A2](#a2-smoke-test) on what they contain).

### C4. Full run of profile `min`

Separate environments, stage by stage:

```bash
.venv-core/bin/python -m marathonts.bench.run raw
.venv-core/bin/python -m marathonts.bench.run prepare
.venv-tsgm/bin/python -m marathonts.bench.run pools --pool-generators tsgm_vae
.venv-core/bin/python -m marathonts.bench.run generate
.venv-core/bin/python -m marathonts.bench.run fidelity
.venv-core/bin/python -m marathonts.bench.run utility
.venv-core/bin/python -m marathonts.bench.run collect
.venv-core/bin/python -m marathonts.hypotheses.run
```

One environment:

```bash
python -m marathonts.bench.run all
python -m marathonts.hypotheses.run
```

Other profiles: `--profile mid` or `--profile max` on every command, `hypotheses.run` included. Parts of a run:
`--datasets`, `--seeds`, `--methods`, `--models` ([CONFIGURATION.md](CONFIGURATION.md#a-command-line-flags)).

### C5. Re-run only the analysis

On the tables of a published run (`artifacts/run_h200/`, `artifacts/run_l4/`) or on the tables of your own run; only `envs/core.txt` is needed:

```bash
python -m marathonts.hypotheses.run                                    # profile min
python -m marathonts.hypotheses.run --profile max
python -m marathonts.hypotheses.run --exclude-datasets bitcoin --rank-exclude    # analysis-only choices
python -m marathonts.hypotheses.overall                                # one report only: OVERALL.md
```

Without `data/processed/<profile>/` the parts that read it (RQ7, CS15, CS12 subgroups) are skipped with a
message; `python -m marathonts.bench.run raw` and `prepare` recreate it.

### C6. Outputs

`data/` and `artifacts/<profile>/` in the project folder ([BENCHMARK.md](BENCHMARK.md), "Artifacts");
`--artifacts-dir` writes the artifacts elsewhere.

## Resuming and re-running

Every unit of work (a pool, a series, a fidelity record, a utility unit) writes its own files and is skipped
when they exist and were made with the same settings: its record holds a fingerprint of the data settings, the
settings of its components, the exogenous files it reads and the units it is made from. Fidelity and utility
units are fingerprinted per metric group and per task × model, with the done cells listed in `cells.json` /
`seed<k>.cells.json`. An interrupted stage therefore continues where it stopped when it is run again, a changed
setting redoes only the units that depend on it, and an added model, task or metric group computes only its own
cells. Details: [BENCHMARK.md](BENCHMARK.md), "Stages"; which settings redo which stages:
[CONFIGURATION.md](CONFIGURATION.md#what-a-change-recomputes).

## Troubleshooting

| Message or symptom | Cause and action |
|---|---|
| `skip tsgm_vae: needs tensorflow, tsgm — run it in its environment (envs/tsgm.txt), e.g. python -m marathonts.bench.run pools --pool-generators tsgm_vae there` | the component's modules are not installed in this environment; the stage skips it and continues. Run the named command in that environment (Docker: the `tsgm` service; Colab: notebook 02). The same message for a long-series generator names `generate --methods …` |
| `skip <ds>: not prepared with these data settings — run the prepare stage` | `data/processed/<profile>/` has no data for these data settings (`max_points`, `split`, `embargo`, `max_gap_interp`, `T`, the Bitcoin window); run `prepare` with the same profile and settings |
| `datasets [...] are not registered; known: ...` | a misspelt dataset name or a plugin that is not loaded (`--plugins`, `Config.plugins`) |
| `FAILED raw pjm` / `raw bitcoin` in the log | no Kaggle token in `~/.kaggle/kaggle.json`; the other datasets continue. Add the token or place the source file in `data/raw/<ds>/` and run `raw` again |
| `FAILED generate <ds> diffusion_ts seed<k>` | `external/Diffusion-TS` is missing or at another path (`--diffusion-ts-dir`); the traceback is in `errors.log` |
| `FAILED …` lines in general | one unit failed; the traceback is appended to `artifacts/<profile>/errors.log`, the stage continues, and the unit is retried on the next run |
| files `*.bad` next to the artifacts | a file truncated by an interruption is renamed `<name>.bad` and its unit is redone on the next run; the `.bad` files can be deleted |
| `thresholds of '<ds>' were set on another split` | the task thresholds file belongs to other data settings; use the file of the profile (`target_params.json` for `min` / `mid`, `target_params_max.json` for `max`) or point `target_params_file` to a new file ([CONFIGURATION.md](CONFIGURATION.md#exogenous-files)) |
| `WARNING: <ds> differs from the published data (data_hashes.json)` | the downloaded source differs from the one of the published run (e.g. a re-uploaded Kaggle file); the run continues, its results on that dataset are not comparable with the published ones |
| `WARNING: model gbdt runs on sklearn here, not XGBoost` | on macOS `gbdt` defaults to scikit-learn HistGradientBoosting (`BENCH_GBDT_BACKEND=xgboost` selects XGBoost); its results are not comparable with XGBoost runs and it has no multi-step task |
| `WARNING: series made with N different GPU types` (collect) | the timing table mixes hardware; the cost comparisons (RQ6, cost ranking) assume one hardware type per dataset |
| `dropped N stale rows (other settings or methods)` (collect) | units made with other settings or of methods outside `cfg.methods` are left out of the tables; run `collect` with the scope and settings of the run |
| `WARNING: optional package ... failed to install` (Colab) | `elkai`, `ortools`, `ruptures` or `hmmlearn` did not build: `vae_atsp` / `vae_pctsp` fail, F5.5–F5.6 / F7.7 are NaN |
| `needs N windows, the pool has M — raise pool_size / pool_mult` | a method with seam processing requests more windows than the pool holds |
| `chronos` / `timesfm` missing on some datasets in the reports | these pairs are in the models' training corpora and are left out of the analysis by `Config.leaked` ([DATASETS.md](DATASETS.md#leakage-into-pretrained-models)); `--leaked '{}'` keeps them |
| warnings at the start of the analysis (noise pair, case-study method, core metrics, primary metrics) | a role or choice that the tables cannot serve; the affected parts are empty or skipped. With fewer than 3 datasets there are no global tests, with fewer than 5 seeds the per-dataset verdicts are mostly inconclusive |
