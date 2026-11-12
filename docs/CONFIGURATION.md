# Configuration

Every setting of the benchmark is a field of one dataclass, `Config` (`marathonts/bench/config.py`). A run is defined by a
`Config` object: the stages of `python -m marathonts.bench.run`, the notebooks and the analysis all read it. This file
describes how the object is built, the four ways to change it, every field with its default, the exogenous
files, and which stages a change recomputes. How to run the stages is in [GETTING_STARTED.md](GETTING_STARTED.md),
how to add components in [EXTENDING.md](EXTENDING.md).

## How the configuration works

- `Config()` is profile `min`. `Config.profile("min" | "mid" | "max", **fields)` returns a profile with some
  fields changed; `Config.quick(**fields)` returns the smoke-test configuration.
- When the object is created (`__post_init__`), the plugin files of `plugins` are imported, the assembly suite
  is registered on every pool generator of `pool_suites`, the long-series generators of `long_methods` are
  registered as methods, and — if `methods` is `None` — the method list is built from these fields. Methods that
  are switched off (`disabled`), published without code (`frozen_methods`) or the noise twin without
  `noise_twin=True` are removed from `methods` and `baselines`.
- Components are named by their registry names (`marathonts/bench/registry.py`); the parameters of a component go to
  `extra[<component name>]` and reach it as `ctx.params` (generators, assemblers, fidelity groups) or
  `self.params` (models).
- Each profile has its own folders, `data/processed/<profile>/` and `artifacts/<profile>/`, so results of
  different profiles do not mix (`mid` reads the processed data of `min`, which are identical).

### Profiles

The settings that differ between the profiles are compared in [BENCHMARK.md](BENCHMARK.md), "Profiles". The
fields each profile sets:

| Profile | Fields (everything else as in `Config()`) |
|---|---|
| `min` | the defaults of the reference below |
| `mid` | `profile_name="mid"`, `pool_train_replicas=None` (VAE trained on every seed), `noise_twin=True`, `artifacts_dir=artifacts/mid` |
| `max` | `profile_name="max"`, `processed_dir=data/processed/max`, `artifacts_dir=artifacts/max`, `max_points=None`, `split=(0.6, 0.2, 0.2)`, `target_params_file=marathonts/bench/target_params_max.json`, `smooth_paths="all"`, `noise_twin=True`, `pool_train_replicas=None`, `dts_train_per_seed=True`, `chronos_model="amazon/chronos-t5-base"`, `hpo=True`, `decision_transfer=True`, `grid_methods="all"`, `model_tasks={}`, `extra={"mlp": {"epochs": 200, "early_stopping_patience": 10}, "gbdt": {"n_estimators": 200, "max_depth": 6, "learning_rate": 0.1, "max_bin": 256, "device": "auto", "multi_strategy_ms": "one_output_per_tree"}}` |

### `Config.quick()`

The smoke test (`python -m marathonts.bench.run <stage> --quick`): `datasets=["ett", "bike"]`, `seeds=[0, 1]`,
`vae_epochs=5`, `vae_patience=3`, `vae_min_epochs=1`, `dts_steps=60`, `dts_eval_every=30`, `dts_sampling_steps=5`,
`dts_timesteps=50`, `dts_d_model=32`, `dts_enc_layers=1`, `dts_dec_layers=1`,
`chronos_model="amazon/chronos-t5-tiny"`, `timestral_model="mistralai/Timestral-5M"`, `timestral_revision=None`,
`n_boot=200`, `pool_size=80`, `pctsp_time_s=2.0`, `disc_epochs=3`, `max_windows=800`,
`extra={"mlp": {"epochs": 3}, "gbdt": {"n_estimators": 30}, "sk_hgb": {"n_estimators": 30}}`, folders
`data/processed/quick/` and `artifacts/quick/`, `profile_name="quick"`. Every other field is the `min` default.

## Four ways to set it

### (a) Command-line flags

`python -m marathonts.bench.run <stage> [flags]` (`marathonts/bench/run.py`):

| Flag | Meaning |
|---|---|
| `stage` | `raw`, `prepare`, `targets`, `hashes`, `pools`, `generate`, `fidelity`, `utility`, `collect` or `all` (= `raw` … `collect`, without `targets` and `hashes`) |
| `--profile {min,mid,max}` | the profile (default `min`) |
| `--quick` | `Config.quick()` instead of the profile |
| `--config FILE` | a JSON file written by `Config.to_json()`; replaces `--profile` and `--quick` ([d](#d-a-json-file)) |
| `--datasets NAME …` | `Config.datasets` |
| `--methods NAME …` | `Config.methods`: run exactly these methods (minus `disabled` and `frozen_methods`) |
| `--models NAME …` | `Config.models` (utility) |
| `--seeds N …` | `Config.seeds` |
| `--pool-generators NAME …` | stage `pools`: which pool generators to fit (default: those used by `methods`) |
| `--artifacts-dir DIR` | `Config.artifacts_dir` |
| `--device DEV` | `Config.device` for torch: `cpu`, `cuda`, `cuda:1`, … (default: CUDA if available) |
| `--diffusion-ts-dir DIR` | `Config.diffusion_ts_dir`, the clone of the Diffusion-TS repository |
| `--plugins FILE …` | plugin files, imported before the configuration is built and added to `Config.plugins` |

The scope flags are applied on top of the profile, `--quick` or `--config`; a flag given without values is
ignored. Every other field is set by (b), (c) or (d). Examples:

```bash
python -m marathonts.bench.run all --profile mid --datasets ett jena --seeds 0 1 2
python -m marathonts.bench.run generate --methods vae_greedy vae_knn chronos --device cuda:1
python -m marathonts.bench.run utility --models linear gbdt sk_hgb
python -m marathonts.bench.run all --plugins my_plugins.py --config my_cfg.json
```

The flags of the analysis are listed in [Command line of the analysis](#command-line-of-the-analysis).

### (b) The `cfg` cell of the notebooks

The setup cell of every notebook creates `cfg = Config.profile(PROFILE)`; notebooks 01–06 then change it in
their scope cell. The cell as shipped, with the optional lines commented out:

```python
# ── scope of this run: change freely; finished units are skipped on re-run ──
import dataclasses
cfg = dataclasses.replace(
    cfg,
    datasets=list(cfg.datasets),  # the profile's datasets (marathonts/bench/config.py DATASETS); or a list, e.g. ["ett", "my_ds"]
    methods=None,                # None → the suites on every pool + long_methods; or a list to run a subset
    baselines=None,              # None → long_methods (case study: CS9, CS10)
    # custom components (EXTENDING.md): plugin files + one line each, no code changes:
    # plugins=["my_plugins.py"],                          # files registering them (path from the project folder)
    # pool_suites={"vae": "tsgm_vae", "gan": "my_gan"},   # the whole suite on another pool generator → gan_zseries, …
    # extra_assemblers=["my_stitch"],                     # an assembler on every pool → vae_my_stitch, …
    # extra_joiners=["my_smooth"],                        # your own seam processing (run like the built-in ones)
    # smooth_paths=["zseries", "greedy"],                 # assemblers that get seam processing ("all": all but the random path and vae_quilting; min: ["zseries"])
    # joiners=["crossfade", "wsola"],                     # which seam processings (None: all)
    # disabled=["pctsp", "chronos"],                      # switch off methods or components by name
    # noise_twin=True,                                    # + the noise twin vae_rand_b (min: off; mid, max: on)
    # frozen_methods=[],                                  # published results kept as they are, not run (default: vae_zseries and its
    #                                                     #   seam-processing variants, marathonts/bench/config.py FROZEN_METHODS); [] → left out of the tables
    # long_methods=[*cfg.long_methods, "my_long"],          # + a long-series generator (method and baseline)
    seeds=list(range(10)),
)
```

Any other field is added to the same call, e.g. `knn_k=10`, `hpo=True` or
`extra={**cfg.extra, "my_stitch": {"alpha": 0.5}}`. The cell must be the same in every notebook of a run.
Notebook 02 hands the whole `cfg` to its stage subprocess (`run_in_env(..., config=cfg)`). Notebook 07 does not
use the scope cell: the analysis takes the configuration saved with the tables
([Analysis-only settings](#analysis-only-settings)).

### (c) Python

```python
import dataclasses
from marathonts.bench.config import Config
from marathonts.bench.run import STAGES

cfg = Config.profile("min", hpo=True, datasets=["ett", "jena"], seeds=[0, 1, 2])
cfg = dataclasses.replace(cfg, knn_k=10, extra={**cfg.extra, "mlp": {"epochs": 50}})

for stage in ("raw", "prepare", "pools", "generate", "fidelity", "utility", "collect"):
    STAGES[stage](cfg)                      # or: from marathonts.bench.run import stage_generate; stage_generate(cfg)

from marathonts.hypotheses.run import main
main(["--profile", "min", "--artifacts-dir", str(cfg.artifacts_dir)])
```

Two rules apply to the method list:

- `Config.profile(...)` and `Config.quick(...)` rebuild `methods` when a field that defines it (`pool_suites`,
  `extra_assemblers`, `extra_joiners`, `long_methods`, `smooth_paths`, `joiners`, `disabled`, `noise_twin`,
  `frozen_methods`) is passed without `methods`, and rebuild `baselines` when `long_methods` is passed without
  `baselines`.
- `dataclasses.replace(cfg, ...)` keeps the list of `cfg`: pass `methods=None` (and `baselines=None`) with such
  fields, as the notebook cell does. `disabled` and `frozen_methods` are applied in either case.

`extra` replaces the whole dictionary: `extra={**cfg.extra, ...}` keeps the parameters the profile sets (`max`
sets `mlp` and `gbdt`).

### (d) A JSON file

`Config.to_json()` writes every field; `Config.from_json(text)` reads it back. `--config` hands such a file to
`python -m marathonts.bench.run` and `python -m marathonts.hypotheses.run` (the notebooks use it for their stage subprocesses):

```python
from marathonts.bench.config import Config
cfg = Config.profile("min", seeds=[0, 1, 2], knn_k=10, disabled=["pctsp"])
open("my_cfg.json", "w").write(cfg.to_json())
```

```bash
python -m marathonts.bench.run all --config my_cfg.json
python -m marathonts.hypotheses.run --config my_cfg.json
```

The paths in the file (`*_dir`, `*_file`) are absolute paths of the machine that wrote it. For another machine
or a Docker container, write them relative to the project folder; relative paths are resolved against the
working directory, i.e. the project folder (`/app` in the containers):

```python
import json
from pathlib import Path
from marathonts.bench.config import ROOT, Config

d = json.loads(Config.profile("min", seeds=[0, 1, 2]).to_json())
d = {k: (Path(v).relative_to(ROOT).as_posix() if k.endswith(("_dir", "_file")) and v else v) for k, v in d.items()}
Path("artifacts/my_cfg.json").write_text(json.dumps(d, indent=2))
```

`collect` writes the configuration of a run in this form to `artifacts/<profile>/tables/config.json`.

## Reference of the settings

Defaults are those of `Config()` (profile `min`); the profile columns of [BENCHMARK.md](BENCHMARK.md) and the
table above give the other values.

### Paths

| Field | Default | Meaning |
|---|---|---|
| `raw_dir` | `data/raw` | raw data (`raw` stage) |
| `processed_dir` | `data/processed/min` | prepared data of the profile |
| `artifacts_dir` | `artifacts/min` | every artifact, tables and reports of the run |
| `profile_name` | `"min"` | name of the profile (recorded with the tables) |
| `diffusion_ts_dir` | `external/Diffusion-TS` | clone of the Diffusion-TS repository |
| `target_params_file` | `marathonts/bench/target_params.json` | exogenous task thresholds ([Exogenous files](#exogenous-files)) |
| `model_configs_file` | `marathonts/bench/model_configs.json` | hyperparameters of the ML models ([Exogenous files](#exogenous-files)) |

### Scope

| Field | Default | Meaning |
|---|---|---|
| `datasets` | the 9 built-in datasets | `ett`, `electricity`, `household`, `pjm`, `beijing_pm25`, `jena`, `metro`, `bike`, `bitcoin`; any registered dataset |
| `seeds` | `[0, …, 9]` | a seed sets the pool sampling, the random paths, the generators and the models |
| `methods` | `None` | `None` → the assembly suite on every pool of `pool_suites` + `long_methods`; a list runs exactly that list |
| `pool_suites` | `{"vae": "tsgm_vae"}` | prefix → pool generator; each entry registers the suite `<prefix>_rand`, `<prefix>_greedy`, … |
| `pool_generators` | `None` | stage `pools`: which generators to fit; `None` → those used by `methods` |
| `pool_train_replicas` | `1` | trained pool generators per dataset: `1` — one model shared by all seeds; `k` — seed s uses model s mod k; `None` — one per seed (`mid`, `max`) |
| `plugins` | `[]` | plugin files registering custom components, loaded with the configuration ([EXTENDING.md](EXTENDING.md#plugin-files)) |
| `extra_assemblers` | `[]` | custom assemblers, each run on every pool as `<prefix>_<name>` |
| `extra_joiners` | `[]` | custom seam processing, run like the built-in ones |
| `smooth_paths` | `["zseries"]` | assemblers that get seam processing: suite suffixes or assembler names; `"all"` → every assembler except the random path and `vae_quilting` (`max`); `[]` → none |
| `joiners` | `None` | which seam processings run; `None` → `crossfade`, `wsola`, `quilt` and `extra_joiners` |
| `long_methods` | `["diffusion_ts", "chronos", "timesfm", "timestral"]` | long-series generators run as methods under their own names |
| `baselines` | `None` | long-series baselines of the case study (CS9, CS10); `None` → `long_methods` |
| `disabled` | `[]` | switched off by name: methods, suite suffixes or components ([below](#switching-methods-on-and-off)) |
| `noise_twin` | `False` | run the noise twin `<prefix>_rand_b` (`mid`, `max`: `True`) |
| `frozen_methods` | `["vae_zseries", "vae_zseries_xfade", "vae_zseries_wsola", "vae_zseries_quilt"]` | methods whose results are kept as they are and not run ([below](#switching-methods-on-and-off)) |
| `case_method` | `"vae_zseries"` | the method of the case study CS1–CS15 (analysis) |
| `noise_pair` | `("vae_rand", "vae_rand_b")` | two random paths on one pool: the noise reference of the analysis |
| `device` | `None` | torch device; `None` → CUDA if available, else CPU |

### Switching methods on and off

Every method is selected by the configuration; nothing in the code has to change.

- **Off.** `disabled` takes method names (`"vae_pctsp"`), suite suffixes (`"greedy"` — on every pool) or
  component names: an assembler (`"atsp"`), a seam processing (`"wsola"` — all its variants), a pool generator
  (`"tsgm_vae"` — the whole suite on it) or a long-series generator (`"chronos"`). A switched-off method is not
  run and does not enter the baselines; its rows already in the tables are dropped by the next `collect`.
- **On.** Built-in methods are on unless `disabled`. A custom one is switched on by its line: `extra_assemblers`,
  `extra_joiners`, `long_methods`, `pool_suites` ([EXTENDING.md](EXTENDING.md)).
- **Seam processing over any assembler.** `smooth_paths=["greedy", "atsp"]` adds every seam processing of
  `joiners` over these assemblers (`vae_greedy_xfade`, `vae_atsp_wsola`, …); `"all"` — over every assembler except
  the random path and `vae_quilting` (it has its own cut).
- **Only some methods.** `methods=["vae_rand", "vae_greedy", "chronos"]` (or `--methods`) runs exactly this list.
- **Results without code.** `frozen_methods` lists methods that are not run but whose results stay: `generate`,
  `fidelity` and `utility` skip them, `collect` carries their rows into the tables (from their unit files or, if
  there are none, from the tables already in `tables/`), and they take part in the rankings, the questions and
  the case study. Their rows enter only where the run has the settings of the published results: the dataset
  and seed are in the run, and the fingerprints the run gives them — what their series depend on in the open
  part (pool, data, thresholds) and each utility cell and fidelity group — equal those in `tables/frozen.json`
  (`python -m marathonts.bench.run freeze`, written once with the results). A run with other data, seeds, tasks, models or
  settings leaves the rest out with a warning, so its tables never mix the published numbers with its own. The default (`bench.config.FROZEN_METHODS`) is
  `vae_zseries` (zseries, the proprietary assembler of zypl.ai (under development)) and its three seam-processing variants, published as results; their code is
  not part of the repository, so the assembler `zseries` is never run on any pool. `frozen_methods=[]` leaves them
  out of the tables.

### Data and split

These settings define the processed data (`Config.DATA_KEYS`); changing them redoes `prepare` and every unit of
the affected datasets.

| Field | Default | Meaning |
|---|---|---|
| `max_points` | `10_000` | last N hourly points of every dataset; `None` → the whole series (`max`) |
| `split` | `(0.5, 0.25, 0.25)` | train / val / OOT shares (`max`: `(0.6, 0.2, 0.2)`) |
| `embargo` | `168` | rows dropped between the parts |
| `max_gap_interp` | `6` | gaps up to this many hours are interpolated, longer ones stay NaN |
| `bitcoin_start`, `bitcoin_end` | `"2017-01-01"`, `"2026-10-01"` | window of the Bitcoin series (a fixed end: the source file grows daily); enter the keys of `bitcoin` only |
| `T` | `168` | window length (one week of hours), the same for every dataset |

### Windows and pool

| Field | Default | Meaning |
|---|---|---|
| `max_windows` | `5000` | slicing stride s = max(1, (n_train − T) // max_windows) of the training windows |
| `holdout_frac` | `0.10` | last share of train used as holdout for early stopping of the generators |
| `pool_size` | `300` | pool size N = max(`pool_size`, `pool_mult` · K) |
| `pool_mult` | `2` | see `pool_size` |

### Pool generator (VAE, `tsgm_vae`)

| Field | Default | Meaning |
|---|---|---|
| `vae_latent` | `16` | latent dimension |
| `vae_beta` | `2.0` | β of the β-VAE |
| `vae_epochs` | `400` | maximum epochs |
| `vae_patience` | `50` | early-stopping patience on the holdout loss |
| `vae_min_epochs` | `150` | no stopping and no best-weight pick before this epoch |
| `vae_noise` | `0.5` | sampling: z ~ N(0, 1) · `vae_noise` |
| `vae_batch` | `64` | batch size |

### Assemblers (BASELINES.md A)

| Field | Default | Meaning |
|---|---|---|
| `pctsp_solutions` | `2000` | `vae_pctsp`: the OR-Tools search stops after this many solutions |
| `pctsp_time_s` | `60.0` | `vae_pctsp`: … or after this time per unit |
| `mbb_bandwidth` | `1.0` | `vae_mbb`: Gaussian kernel, h = this × median jump |
| `knn_k` | `None` | `vae_knn`: neighbours; `None` → round(√N) |
| `quilt_tol` | `0.1` | `vae_quilting`: candidates within (1 + tol) × the best overlap error |
| `herding_stride` | `4` | `vae_herding`: every k-th point of a window as features |

### Seam processing (BASELINES.md B)

| Field | Default | Meaning |
|---|---|---|
| `join_overlap` | `12` | points two neighbouring windows overlap (`crossfade`, `wsola`, `quilt`, `vae_quilting`) |
| `join_wsola_shift` | `12` | `wsola`: maximum shift of the next window |

### Diffusion-TS

| Field | Default | Meaning |
|---|---|---|
| `dts_d_model`, `dts_enc_layers`, `dts_dec_layers`, `dts_heads`, `dts_timesteps` | `64`, `3`, `2`, `4`, `500` | model (official `Config/etth.yaml`, window length T) |
| `dts_steps`, `dts_batch`, `dts_grad_accum` | `18000`, `128`, `2` | optimiser steps, batch, gradient accumulation |
| `dts_lr`, `dts_warmup_lr`, `dts_warmup` | `1e-5`, `8e-4`, `500` | Adam from `dts_lr`, linear warm-up to `dts_warmup_lr` over `dts_warmup` steps |
| `dts_lr_factor`, `dts_lr_patience`, `dts_min_lr`, `dts_lr_threshold` | `0.5`, `4000`, `1e-5`, `0.1` | ReduceLROnPlateau on the training loss |
| `dts_ema_decay`, `dts_ema_every`, `dts_ema_after` | `0.995`, `10`, `100` | EMA of the weights |
| `dts_eval_every`, `dts_patience_evals` | `500`, `8` | early stopping on the holdout loss of the EMA model |
| `dts_sampling_steps` | `50` | DDIM steps of the infill |
| `dts_context_frac` | `0.5` | share of the window kept as context in each autoregressive step |
| `dts_infill_coef`, `dts_infill_lr` | `1e-2`, `5e-2` | infill guidance |
| `dts_train_per_seed` | `False` | `True` → one training per seed (`max`); `False` → models per dataset (below) |
| `diffusion_train_replicas` | `1` | without `dts_train_per_seed`: k models per dataset, seed s uses model s mod k |

### Chronos, TimesFM, Timestral

| Field | Default | Meaning |
|---|---|---|
| `chronos_model` | `"amazon/chronos-t5-small"` | Hugging Face model id (`max`: `amazon/chronos-t5-base`) |
| `chronos_context` | `512` | context length |
| `chronos_chunk` | `64` | points generated per step |
| `timesfm_model`, `timesfm_revision` | `"google/timesfm-3.0-pytorch"`, pinned commit | TimesFM 3.0 weights |
| `timestral_model`, `timestral_revision` | `"mistralai/Timestral-209M"`, pinned commit | Timestral weights |

### Fidelity

| Field | Default | Meaning |
|---|---|---|
| `fidelity_ref` | `"val"` | primary real reference (metric names without suffix) |
| `fidelity_extra_refs` | `["train", "oot"]` | further references, suffix `@<part>`; `[]` → val only (a third of the stage time) |
| `fidelity_groups` | `None` | metric groups to compute; `None` → every registered group |
| `disc_epochs` | `30` | epochs of the post-hoc GRU discriminator (F6.1) |
| `edge_overlap` | `5` | F5.7: width of the seam detector's window |
| `stitch_task` | `"clf_up_h24_q90"` | task of F8 and of the case-study cells (CS7, CS10, CS12, CS13) |

### Utility

| Field | Default | Meaning |
|---|---|---|
| `tasks` | `None` | utility tasks; `None` → every registered task (14 built-in) |
| `models` | `["linear", "gbdt", "mlp"]` | ML models; also registered: `sk_linear`, `sk_hgb`, `sk_mlp` ([MODELS.md](MODELS.md)) |
| `model_tasks` | `{"mlp": ["clf_up_h24_q90"]}` | models restricted to some tasks; the others run on every task they support (`max`: `{}`) |
| `test_splits` | `["val", "oot"]` | real test parts |
| `hpo` | `False` | hyperparameter search per fit over the grids of `model_configs.json` (`max`: `True`) |
| `hpo_val_frac` | `0.2` | share of the regime's own training data (its tail) used to choose |
| `decision_transfer` | `False` | the decision-transfer grid U6.1 / U6.4 → RQ5 (c) (`max`: `True`) |
| `grid_methods` | `None` | methods of that grid; `None` → `case_method` and `noise_pair[0]`; `"all"` → every method |
| `model_grid_task` | `"clf_up_h24_q90"` | task of that grid |

### Artifacts

| Field | Default | Meaning |
|---|---|---|
| `save_generator_weights` | `True` | write generator weights (pools are always written) |
| `save_model_weights` | `True` | write the weights of every utility model (predictions are always written) |
| `weights_dtype` | `"float32"` | `"float16"` halves the weight files |

### Statistics

| Field | Default | Meaning |
|---|---|---|
| `alpha` | `0.05` | significance level |
| `n_boot` | `2000` | bootstrap resamples |
| `boot_block` | `168` | block length of the test-row bootstrap (one week) |
| `equivalence_margin_q` | `0.5` | SESOI quantile of the single-run noise ([HYPOTHESES.md](HYPOTHESES.md) §2) |

These fields, `case_method`, `noise_pair` and `baselines` enter no unit fingerprint. The analysis takes them
from the configuration saved with the tables (`tables/config.json`); `--config` or the flags of
[the analysis](#command-line-of-the-analysis) change them for one analysis run.

### Analysis-only settings

`Config.ANALYSIS_KEYS`: they are never part of a fingerprint, so changing them re-runs only stage 7. Unlike the
other fields, the analysis does not take them from `tables/config.json` but from the code defaults of the
run's profile, then applies the command-line flags; `python -m marathonts.hypotheses.run --config FILE` uses the values of
the file instead. Notebook 07 passes its `cfg` this way, so analysis settings set in its `cfg` cell
(`dataclasses.replace(cfg, core_metrics=…)`) apply to the analysis.

| Field | Default | Flag | Meaning |
|---|---|---|---|
| `leaked` | `{"chronos": ["electricity", "beijing_pm25"], "timesfm": ["beijing_pm25", "household", "bitcoin"]}` | `--leaked JSON` | method → datasets in its training corpus, left out of the analysis ([DATASETS.md](DATASETS.md#leakage-into-pretrained-models)); `'{}'` → none |
| `rank_exclude` | `None` | `--rank-exclude [METHOD …]` | methods left out of the rankings; `None` → the seam-processing variants unless every assembler has them; `[]` (flag without names) → rank every method |
| `utility_fail_penalty` | `True` | `--no-fail-penalty` | a TSTR cell a method's series could not train enters as a model that learned nothing; `False` → left out |
| `exclude_datasets` | `[]` | `--exclude-datasets DATASET …` | datasets left out of the analysis; their units stay on disk |
| `exclude_metrics` | `[]` | `--exclude-metrics METRIC …` | a fidelity id (`"F6.1_disc_score"` — every reference), one reference (`"F6.1_disc_score@val"`), a group prefix ending in `.` (`"F12."`) or a utility metric (`"ece"`; not a primary one) |
| `core_metrics` | `None` | — | core fidelity metrics per criterion (core rankings, overall leaderboard, `METRIC_VALUES.md`); `None` → `hypotheses.leaderboard.CORE_METRICS` |
| `metric_criteria` | `{}` | — | fidelity group → criterion, merged over `leaderboard.FID_CRITERIA` |
| `task_criteria` | `{}` | — | task type → utility criterion, merged over `leaderboard.UT_CRITERIA` (`classification` / `regression` enter the four rankings) |
| `primary_metrics` | `{}` | — | task type → primary utility metric, merged over `catalog.PRIMARY_METRIC` |
| `metric_orient` | `{}` | — | utility metric → `+1` (higher is better) / `-1`, merged over the built-in metrics; a utility metric without one is not analysed |
| `near_copy_ratio` | `2.0` | — | memorisation flag of the overall leaderboard: near-copy share ≥ this × that of the real OOT piece (reported, not ranked) |

The fields without a flag reach the analysis through a JSON file built from the run's saved configuration
(the paths are set to those of this checkout):

```python
import dataclasses
from pathlib import Path
from marathonts.bench.config import Config

base = Config.profile("min")                                    # the profile of the run
run = Config.from_json(Path("artifacts/run_h200/tables/config.json").read_text())
paths = {f.name: getattr(base, f.name) for f in dataclasses.fields(Config) if f.name.endswith(("_dir", "_file"))}
cfg = dataclasses.replace(run, **paths, metric_orient={"precision_top10": 1}, near_copy_ratio=3.0)
Path("analysis_cfg.json").write_text(cfg.to_json())
```

```bash
python -m marathonts.hypotheses.run --config analysis_cfg.json
```

At start the analysis warns about roles and choices the tables cannot serve: the noise pair or the case-study
method missing, core metrics or a task type's primary metric missing, utility columns without an orientation.

### Parameters of components: `extra`

| Field | Default | Meaning |
|---|---|---|
| `extra` | `{}` | `{<component name>: {parameter: value}}`: parameters of pool and long-series generators, assemblers, joiners (read from `cfg` in `join`), models (over `model_configs.json`) and fidelity groups |

## Exogenous files

Two JSON files hold values that are fixed before a run and only read during it. Their contents enter the
fingerprints of the units that read them, so an edit redoes exactly those units.

**`marathonts/bench/model_configs.json`** (`Config.model_configs_file`) — hyperparameters of every ML model
([MODELS.md](MODELS.md)): one object per model (`linear`, `mlp`, `gbdt`, `sk_linear`, `sk_hgb`, `sk_mlp`) and,
under `"grids"`, the candidate configurations of the search (`hpo=True`), each merged over the model's fixed
values. A model receives `model_configs_file[<model>]` updated by `extra[<model>]`. A custom model gets its own
object (or only `extra`). Editing one model's entry redoes that model's utility cells only.

```json
{
  "gbdt": {"n_estimators": 100, "max_depth": 4, "learning_rate": 0.2, "max_bin": 64, "device": "cpu",
           "multi_strategy_ms": "multi_output_tree"},
  "grids": {"gbdt": [{"max_depth": 2}, {"max_depth": 4}, {"max_depth": 6}, {"max_depth": 8}]}
}
```

**`marathonts/bench/target_params.json`** (`min`, `mid`) and **`marathonts/bench/target_params_max.json`** (`max`)
(`Config.target_params_file`) — task thresholds per dataset in real units, `{dataset: {task: {parameter:
value}}}`, plus `_split_key`: the data settings each dataset's thresholds were computed on. `prepare` (and the
stage `targets`) proposes the missing ones by the task's rule on the train split and writes them; review and
commit the file. With other data settings (`max_points`, `split`, `embargo`) the file is refused for that
dataset, because thresholds of another split could come from this run's val or OOT: point
`target_params_file` to a new file, and `prepare` fills it from the new train split. Editing the thresholds of
one dataset redoes its labels, its utility cells, the fidelity groups F8 and F11 and the assemblers that read
thresholds (`uses_targets`) on that dataset only. The files `marathonts/bench/target_params*.pinned.json` are frozen copies
used for this per-dataset fingerprinting and are never edited.

`marathonts/bench/data_hashes.json` holds content hashes of the published prepared data; it is written by the stage
`hashes` and enters no fingerprint ([BENCHMARK.md](BENCHMARK.md), stage 1b).

## What a change recomputes

Each unit stores a fingerprint of what it depends on (`Config.unit_fingerprint`, `Config.COMPONENT_KEYS`,
`marathonts/bench/cells.py`); a stage redoes the units whose fingerprint changed and skips the others
([BENCHMARK.md](BENCHMARK.md), "Stages"). Downstream units follow: a redone series redoes its fidelity and utility.

| Change | Redone |
|---|---|
| `datasets`, `seeds`, `methods`, `models`, `tasks`, `fidelity_groups` extended | only the added units or cells |
| `max_points`, `split`, `embargo`, `max_gap_interp`, `T` | `prepare` and every unit of every dataset (a new split also needs thresholds, see above) |
| `bitcoin_start`, `bitcoin_end` | the same, for `bitcoin` only |
| `max_windows`, `holdout_frac` | VAE and Diffusion-TS training and everything after them; not the pretrained generators |
| `vae_latent`, `vae_beta`, `vae_epochs`, `vae_patience`, `vae_min_epochs`, `vae_batch` | VAE training, the pools, the pool-based methods |
| `pool_size`, `pool_mult`, `vae_noise`, `pool_train_replicas` | the pools and the pool-based methods; a stored trained VAE is reused where it fits the new setting (`pool_size`, `pool_mult`, `vae_noise` resample from it) |
| `pctsp_*`, `mbb_*`, `knn_*`, `quilt_tol`, `herding_*` | that assembler's series |
| `join_overlap`, `join_wsola_shift` | the seam-processing variants (`join_overlap` also `vae_quilting`) |
| `dts_*`, `diffusion_train_replicas` | Diffusion-TS series; the shared model (`min`, `mid`) is retrained only when a training setting changes (`dts_d_model` … `dts_ema_after`, not `dts_sampling_steps`, `dts_context_frac`, `dts_infill_*`) |
| `chronos_*`, `timesfm_*`, `timestral_*` | that generator's series |
| `extra[<component>]` | the units of that component |
| an entry of `model_configs.json` | that model's utility cells |
| thresholds of a dataset in `target_params*.json` | that dataset's labels, utility cells, F8 / F11 and assemblers with `uses_targets` |
| `test_splits`, `hpo`, `hpo_val_frac`, `save_model_weights`, `weights_dtype` | every utility cell |
| `decision_transfer`, `grid_methods`, `model_grid_task` | the decision-transfer cell |
| `fidelity_ref`, `fidelity_extra_refs`, `disc_epochs`, `edge_overlap`, `stitch_task` | every fidelity group |
| `extra[<fidelity group>]` | that fidelity group |
| `disabled`, `frozen_methods`, `noise_twin`, `smooth_paths`, `joiners`, `pool_suites`, `extra_assemblers`, `extra_joiners`, `long_methods` | the method list: added methods are computed, removed ones are left out of the tables by the next `collect` |
| statistics fields, `case_method`, `noise_pair`, `baselines`, analysis-only settings | stage 7 only |
| `device`, paths, `save_generator_weights` | nothing |

## Command line of the analysis

`python -m marathonts.hypotheses.run` (`marathonts/hypotheses/run.py`) — every report of stage 7:

| Flag | Meaning |
|---|---|
| `--profile {min,mid,max}` | profile (default `min`); the configuration saved with the tables takes precedence |
| `--artifacts-dir DIR` | the run to analyse (default `artifacts/<profile>`) |
| `--processed-dir DIR` | the prepared data (dataset descriptors of RQ7, CS15, CS12 subgroups) |
| `--out-dir DIR` | base folder of the results: `DIR/reports/`, `DIR/hypotheses/`, `DIR/overall/`, `DIR/leaderboard/`, `DIR/metric_values/` (default: the artifacts folder) |
| `--only ID …` | only these questions / hypotheses (`RQ2`, `CS3`, …); no confirmatory family, overall leaderboard, ranking files or metric values |
| `--no-case-study` | only the research questions, the rankings and the metric values |
| `--plugins FILE …` | plugin files: hypotheses, tests, metrics |
| `--config FILE` | a JSON written by `Config.to_json()`, used instead of the saved configuration |
| `--case-method METHOD` | method of the case study (default `Config.case_method`) |
| `--noise-pair A B` | two random paths on the same pool |
| `--baselines METHOD …` | long-series baselines of the case study |
| `--case-task TASK` | task of the case-study cells CS7, CS10, CS12, CS13 (default `Config.stitch_task`) |
| `--rank-exclude [METHOD …]` | methods left out of the rankings; without names — rank every method |
| `--no-fail-penalty` | leave out the TSTR cells a series could not train |
| `--exclude-datasets DATASET …` | datasets left out of the analysis |
| `--exclude-metrics METRIC …` | metrics left out of the analysis |
| `--leaked JSON` | replaces `Config.leaked` (`'{}'` — nothing left out) |

`python -m marathonts.hypotheses.leaderboard` (`LEADERBOARD.md`) and `python -m marathonts.hypotheses.overall` (`OVERALL.md`) build one
report each:

| Flag | Meaning |
|---|---|
| `--profile`, `--artifacts-dir` | as above |
| `--out DIR` | the tables (default `<artifacts>/leaderboard` or `<artifacts>/overall`); the report goes to `DIR/../reports/` |
| `--n-boot N` | bootstrap resamples (default 1000) |
| `--rank-exclude [METHOD …]`, `--exclude-datasets`, `--exclude-metrics`, `--leaked` | as above |

`python -m marathonts.hypotheses.metric_values` (`METRIC_VALUES.md`) takes `--profile`, `--artifacts-dir`, `--out DIR`
(default `<artifacts>/metric_values`), `--exclude-datasets`, `--exclude-metrics` and `--leaked`.

```bash
python -m marathonts.hypotheses.run --profile max
python -m marathonts.hypotheses.run --artifacts-dir artifacts/run_h200 --out-dir /tmp/analysis
python -m marathonts.hypotheses.run --case-method vae_greedy
python -m marathonts.hypotheses.run --exclude-datasets bitcoin --exclude-metrics F12. --leaked '{}'
python -m marathonts.hypotheses.leaderboard --rank-exclude
```
