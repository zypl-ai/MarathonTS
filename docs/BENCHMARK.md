# Benchmark: pipeline

The benchmark (`marathonts/bench/`) generates long synthetic series with every method on every dataset and
measures their fidelity, utility and cost. Statistics and conclusions are separate, in the hypothesis
testing ([HYPOTHESES.md](HYPOTHESES.md), section 7), which reads the benchmark tables. Everything is stored in
Parquet; each part (dataset, generator, assembler, model, metric, target) is plugged in through a
registry —
[EXTENDING.md](EXTENDING.md).

## Profiles: `min`, `mid` and `max`

Everything that speeds up a run is switched on and off in the config (`marathonts/bench/config.py`); three ready-made
sets — `--profile min` (default, run in Colab), `--profile mid` (min + the VAE
retrained on every seed and the noise twin `vae_rand_b`) and `--profile max` (everything on).

| Setting | `min` | `mid` | `max` |
|---|---|---|---|
| methods (`methods`), baselines (`baselines`) | 16 in the tables: run by the pipeline — 12: the random path `vae_rand`, 7 other assemblers on the same pool, Diffusion-TS, Chronos, TimesFM, Timestral; published results (`frozen_methods`) — 4: `vae_zseries` (zseries, the proprietary assembler of zypl.ai (under development)) and its 3 seam-processing variants (`smooth_paths=["zseries"]`); without the noise twin `vae_rand_b` (`noise_twin=False`) | 17: as `min` + `vae_rand_b` (13 run, 4 published) | 35: the 17 + every seam processing over the 6 other assemblers except the random path and `vae_quilting` (`smooth_paths="all"`; 31 run, 4 published) |
| pool size (`pool_size`, `pool_mult`) | N = max(300, 2K) = 300 windows | as `min` | N = max(300, 2K) |
| Diffusion-TS training (`dts_train_per_seed`, `diffusion_train_replicas`) | once per dataset: 9 trainings, seeds change only generation | as `min` (k models per dataset with `diffusion_train_replicas=k`: seed s → model s mod k) | on every seed: 90 trainings |
| VAE training (`pool_train_replicas`) | 1 model per dataset: 9 trainings | on every seed: 90 trainings (independent seeds) | on every seed: 90 trainings |
| Chronos (`chronos_model`) | `chronos-t5-small` | as `min` | `chronos-t5-base` (≈200M, the size of TimesFM 3.0 and Timestral-209M) |
| series length (`max_points`), train / val / OOT shares (`split`) | last 10,000 points, 50 / 25 / 25 | as `min` | whole series, 60 / 20 / 20 |
| hyperparameter tuning (`hpo`) | no: fixed configurations | no | yes: grid on the tail of the regime's own training data (TRTR: real train; TSTR: the synthetic series — no real data before the test) |
| MLP (`model_tasks`) | one task only (`clf_up_h24_q90`) | as `min` | on all tasks |
| MLP epochs (`early_stopping_patience`) | 30, no early stopping | as `min` | up to 200, with early stopping |
| boosting (`model_configs.json` → `gbdt`) | light: 100 trees, depth 4, 64 bins, CPU, vector leaves in multi-step | as `min` | full: 200 trees, depth 6, 256 bins, separate ensemble per step |
| model grid for RQ5 (c) (`decision_transfer`, `grid_methods`) | no (RQ5 (c) is not tested) | no | yes, for all methods |

Profiles write to their own folders — `data/processed/<profile>/` and `artifacts/<profile>/` — so
results do not mix; `mid` uses the prepared data of `min` (they are identical). Below, `artifacts/…` is
short for `artifacts/<profile>/…`.

When a generator model is shared by several seeds, the seed still changes pool sampling and
random paths, and the training time of the shared model is recorded for every seed (used in RQ6). The weights
of the shared model are `artifacts/<profile>/generators/<ds>/<generator>/replica<k>.parquet`. Any
setting can be changed on its own (`Config.profile("min", hpo=True)`). Target parameters
(exogenous, see below): `marathonts/bench/target_params.json` for `min` and `mid` (same data) and
`marathonts/bench/target_params_max.json` for `max` — thresholds are computed on the train of their own split, because
the train of profile `min` falls into the val and OOT of profile `max`.

## Environments

Generators with conflicting dependencies run in their own environments. Environments communicate only
through Parquet artifacts: the `pools` stage trains the pool generator in its environment and writes the pool to
`artifacts/pools/`, while `generate` and everything after it run in the main environment and read the pool from there.
TensorFlow is never imported in the main environment.

| Environment | File | What runs | Dependencies |
|---|---|---|---|
| base | `envs/base.txt` | `raw`, `prepare`; basis of the other environments | numpy, scipy, pandas, pyarrow, psutil, tqdm |
| core | `envs/core.txt` | `generate` (assembly), `fidelity`, `utility`, `collect`, hypothesis testing | base + torch, scikit-learn, statsmodels, xgboost, ruptures, hmmlearn, elkai (`vae_atsp`), ortools (`vae_pctsp`) |
| tsgm | `envs/tsgm.txt` | `pools --pool-generators tsgm_vae` | base + tensorflow, keras, tsgm (no torch) |
| diffusion_ts | `envs/diffusion_ts.txt` | `generate --methods diffusion_ts` | core + einops + Diffusion-TS code |
| chronos | `envs/chronos.txt` | `generate --methods chronos` | core + chronos-forecasting |
| timesfm | `envs/timesfm.txt` | `generate --methods timesfm` | core + timesfm 3.0.2 |
| timestral | `envs/timestral.txt` | `generate --methods timestral` | core + timestral (pinned commit) |
| sdv | `envs/sdv.txt` | `pools --pool-generators sdv_par` | base + sdv |

`requirements.txt` — everything in one environment, if there are no conflicts. Each generator declares its
environment (`env`) and required modules (`requires`). If the modules are missing and the pool has not been computed yet, the stage
skips the generator and reports which environment to run it in — this is not an error.

## How to run

Docker, Colab notebooks or local environments, each with a smoke test, the full run and re-running only the
analysis — [GETTING_STARTED.md](GETTING_STARTED.md). Settings and their effect on the stages —
[CONFIGURATION.md](CONFIGURATION.md).

## What is compared

| Method | How the series of length K·T is obtained |
|---|---|
| `vae_zseries` | pool of N VAE windows (`min`: 300) → zseries, the proprietary assembler of zypl.ai (under development); its results are published (`Config.frozen_methods`), its code is not part of the repository (the case-study method) |
| `vae_rand` | the same pool, K random windows in random order |
| `vae_rand_b` | the same with another permutation seed (noise estimate; `mid` and `max` only) |
| `vae_greedy` | the same pool: greedy nearest neighbour by the jump at the seam from a random window |
| `vae_atsp` | asymmetric travelling salesman problem over the whole pool by the jump at the seam (LKH, `elkai`); the cheapest segment of K windows is taken from the tour |
| `vae_pctsp` | prize-collecting TSP (OR-Tools): choice of K windows out of N and their order at once by the jump at the seam, search up to `pctsp_solutions` = 2000 solutions (reproducible), at most `pctsp_time_s` = 60 s per unit |
| `vae_mbb` | matched-block bootstrap (Carlstein et al. 1998): Markov chain over the pool, P(i→j) ∝ exp(−½ (jump_ij / h)²), h = `mbb_bandwidth` (1) × median jump |
| `vae_knn` | k-nearest-neighbour resampling (Lall & Sharma 1996): the next window among the k = √N whose first point is nearest to the last point of the current one, weight ∝ 1/rank |
| `vae_quilting` | image quilting (Efros & Freeman 2001): the next window at random among those whose overlap error (12 points) is within 1.1 × the best, the overlap cut at the minimum-error point |
| `vae_herding` | kernel herding: K windows by MMD to the train windows, random order |
| `vae_zseries_xfade` | (published results, as `vae_zseries_wsola` and `vae_zseries_quilt`) the `vae_zseries` path, windows overlap by `join_overlap` = 12 points and are blended with a Hann window |
| `vae_zseries_wsola` | the same, but the next window is first shifted by up to 12 points towards the best correlation in the overlap (WSOLA) |
| `vae_zseries_quilt` | in the overlap the series switches to the next window at the point of smallest difference (the boundary cut of image quilting in 1D) |
| `diffusion_ts` | Diffusion-TS is trained on the same windows; the first window is generated, each next one is extended by imputation from the tail of the previous one (context T/2); the calendar is given, only the value is generated |
| `chronos` | Chronos samples a trajectory of K·T continuing the last 512 points of train, in chunks of 64 |
| `timesfm` | TimesFM 3.0, zero-shot: the median forecast of the K·T steps after train, the whole train as context (up to 15 360 points) |
| `timestral` | Timestral 209M (Mistral), zero-shot: the median forecast of the K·T steps after train, the whole train as context (up to 32 768 points), block by block |

A method is "pool generator + assembler (+ seam processing)" or a "long-series generator"
(`marathonts/bench/methods.py`). Built-in components: pool generators `tsgm_vae`, `sdv_par` (SDV
PARSynthesizer), `real_windows`; assemblers `random`, `random_b`, `greedy`, `atsp`, `pctsp`, `mbb`, `knn`,
`quilt_sel`, `herding` (`marathonts/bench/assemblers.py`; the zseries assembler is registered by name only, without code); seam processing
`crossfade`, `wsola`, `quilt` (`marathonts/bench/joiners.py`: the overlap shortens the series, so the assembler
returns more than K windows — 33–35 in `min` — and the series is cut to K·T); long-series generators
`diffusion_ts`, `chronos`, `timesfm`, `timestral`. Custom ones go through the registry. The set of assemblers is defined once (`STITCH_SUITE`)
and run on each pool generator from `Config.pool_suites` (default `{"vae": "tsgm_vae"}`;
another generator is one more entry, methods `<prefix>_zseries`, `<prefix>_rand`, …, EXTENDING.md).
Custom assemblers, seam processing and long-series generators are plugged in with a plugin and one line of
config (`plugins`, `extra_assemblers`, `extra_joiners`, `long_methods`, EXTENDING.md) and
automatically join the set on every pool. All assemblers of one set take the same pool, so
`vae_*` differ only in the choice, order and joining of windows. The alternative assemblers use the seam
criteria of their own literature (BASELINES.md); the solvers (greedy, ATSP, PCTSP) get the jump at the
seam — the Euclidean distance between the last point of a window and the first point of the next over every
channel. Seam processing runs over the assemblers of `smooth_paths` (`min`, `mid`: the `vae_zseries` path, published results; any
list can be set, e.g. `["greedy", "atsp"]`); with `smooth_paths="all"` (`max`) every seam processing runs over
every assembler except the random path and `vae_quilting` (it has its own cut) — `vae_greedy_xfade`,
`vae_atsp_quilt`, … The random path has a single variant, `vae_rand`, plus the noise twin `vae_rand_b` in
`mid` and `max`. The rankings leave out the seam-processing variants unless every assembler has them
(`rank_exclude`, HYPOTHESES.md §3, RQ1); `vae_quilting` is one method (choice and cut), not a variant, and is
ranked. Any method or component is switched off by name (`disabled`). Results published without their code
are listed in `frozen_methods` (default: `vae_zseries`, `vae_zseries_xfade`, `vae_zseries_wsola`, `vae_zseries_quilt`):
no stage runs them, `collect` carries their rows into the tables where the run has the settings of their
results (`tables/frozen.json`), and the analysis ranks them
like any other method ([CONFIGURATION.md](CONFIGURATION.md), "Switching methods on and off").

## Protocol

The common ground of every method: the same channels and windows, the same pool generator for the assembly methods, the same utility test. The code lives in `bench/` (`data.py`, `generators/builtin.py`, `tasks.py`, `utility.py`); the snippets below show the logic.

### Data: channels and windows


The generator and the assembler work with windows `(n, T, 3)` in `[0, 1]`:

- channel 0 — series value, min-max on **train**;
- channels 1–2 — calendar: `(sin + 1) / 2`, `(cos + 1) / 2` of the hour of week.

```python
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view

HOURS_PER_WEEK = 168

def to_channels(values, how, lo, hi):
    a = 2 * np.pi * how / HOURS_PER_WEEK
    return np.column_stack([(values - lo) / (hi - lo),
                            (np.sin(a) + 1) / 2, (np.cos(a) + 1) / 2]).astype(np.float32)

def from_channels(X, lo, hi):
    """Back: values and hour of week (the synthetic calendar is the one the generator produced)."""
    values = X[:, 0] * (hi - lo) + lo
    a = np.arctan2(2 * X[:, 1] - 1, 2 * X[:, 2] - 1)
    how = np.mod(np.rint(a / (2 * np.pi) * HOURS_PER_WEEK), HOURS_PER_WEEK).astype(int)
    return values, how

def slide(X, T, s):
    """Windows of length T with stride s; windows with NaN are dropped."""
    W = sliding_window_view(X, (T, X.shape[1]))[::s, 0]
    return np.ascontiguousarray(W[~np.isnan(W).any(axis=(1, 2))], dtype=np.float32)

# train = values[:n_train], how = hour of week of each row
lo, hi = np.nanmin(train), np.nanmax(train)
X_train = to_channels(train, how[:n_train], lo, hi)        # (n_train, 3)
```

Window parameters (computed on train only; `marathonts/bench/data.py`, `window_layout`):

| Parameter | Rule | `min` |
|---|---|---|
| `T` | window length, one week of hours, the same for every dataset (`Config.T`) | 168 |
| `s` | slicing stride: `max(1, (n_train − T) // max_windows)`, `max_windows` = 5000 | 1 |
| `K` | number of windows in the assembly: `round(n_train / T)`, as much synthetic data as train | 30 |
| `N` | pool size: `max(pool_size, pool_mult · K)` = `max(300, 2K)`; the assembler takes windows without replacement, so `N ≥ K` is required | 300 |

The last 10% of train (`holdout_frac`) is cut off as holdout for early stopping of the generators; between it
and the rest of train (core) there is an embargo of `embargo` = 168 rows. Core and holdout windows do not overlap.

```python
X_core = slide(X_train[:core_end], T, s)
X_hold = slide(X_train[hold_start:], T, s)
```

### Pool generator: VAE


Recipe: `tsgm` `vae_conv5` + `BetaVAE`, latent 16, β = 2, Adam 1e-3, batch 64, up to 400 epochs.
Early stopping on holdout loss (`z = z_mean`), patience 50 epochs, the best weights are kept.
The first 150 epochs (`vae_min_epochs`) do not stop and are not considered for the best weights.
Sampling: `z ~ N(0, 1) · 0.5`.
The learning rate (the Adam default) and the batch size follow TSGM and its VAE tutorial. β, the latent size,
the epoch limits and the prior scale were taken from earlier exploratory work of the authors on other data and
were not tuned on this benchmark. The decoder of `vae_conv5` ends with a sigmoid, so its output is already in
(0, 1): `nan_to_num` replaces a NaN by 0.5, and the clipping to `[0, 1]` is only a safeguard.

```python
import os; os.environ.setdefault("KERAS_BACKEND", "tensorflow")
import keras, tensorflow as tf, tsgm

LATENT, BETA, EPOCHS, PATIENCE, MIN_EPOCHS, NOISE = 16, 2.0, 400, 50, 150, 0.5

arch = tsgm.models.zoo["vae_conv5"](seq_len=T, feat_dim=3, latent_dim=LATENT)
vae = tsgm.models.cvae.BetaVAE(arch.encoder, arch.decoder, beta=BETA)
vae.compile(optimizer=keras.optimizers.Adam(1e-3))

def holdout_loss(X):
    zm, zlv, _ = vae.encoder(X, training=False)
    rec = vae.decoder(zm, training=False)
    r = tf.reduce_mean(vae._get_reconstruction_loss(X, rec))
    kl = tf.reduce_mean(tf.reduce_sum(-0.5 * (1 + zlv - zm ** 2 - tf.exp(zlv)), axis=1))
    return float(r + kl)

best, best_ep, best_w = np.inf, -1, None
for ep in range(EPOCHS):
    vae.fit(X_core, epochs=1, batch_size=64, verbose=0)
    hl = holdout_loss(X_hold)
    if ep + 1 < MIN_EPOCHS:
        continue
    if hl < best:
        best, best_ep = hl, ep
        best_w = vae.encoder.get_weights() + vae.decoder.get_weights()
    if ep - best_ep >= PATIENCE:
        break
ne = len(vae.encoder.get_weights())
vae.encoder.set_weights(best_w[:ne]); vae.decoder.set_weights(best_w[ne:])

# pool: N windows (N, T, 3)
rng = np.random.default_rng(seed)
z = (rng.standard_normal((N, LATENT)) * NOISE).astype(np.float32)
pool = np.clip(np.nan_to_num(np.asarray(vae.decoder(z, training=False)), nan=0.5), 0, 1)
```

Any generator of windows of the same shape `(N, T, 3)` in the same channels can replace the VAE (`pool_suites`, EXTENDING.md); every assembly method of a suite takes the same pool.

### Utility: TSTR versus TRTR

The quality of the synthetic data is tested as follows: a model is trained **only on synthetic data** (TSTR — train on
synthetic, test on real) and compared with the same model trained on real train (TRTR —
train on real, test on real). Both are tested on the same real data (val / OOT); synthetic data
never get there. The closer TSTR is to TRTR, the better the synthetic data. Features and labels of the synthetic data are computed
on the synthetic data themselves. Example: the binary "tail" task (change over `h` steps above a train quantile) and
a point forecast.

```python
import pandas as pd

LAGS = (1, 2, 3, 6, 12, 24, 48, 168)
h = 24
d = train[h:] - train[:-h]
thr = np.nanquantile(d, 0.90)                    # the threshold is fixed on train

def tail_up(values):                             # label at t: change over the next h steps above thr
    v = np.asarray(values, float)
    dd = np.full(len(v), np.nan)
    dd[:-h] = v[h:] - v[:-h]
    return np.where(np.isnan(dd), np.nan, (dd > thr).astype(float))

def make_xy(values, how, task):
    """Features — lags and differences of the series, calendar; target — at horizon h."""
    v = pd.Series(values)
    X = pd.DataFrame({"v": v, **{f"d{l}": v - v.shift(l) for l in LAGS},
                      "sin": np.sin(2 * np.pi * how / 168), "cos": np.cos(2 * np.pi * how / 168)})
    y = tail_up(values) if task == "clf" else v.shift(-h).to_numpy()            # class / value forecast
    ok = X.notna().all(axis=1).to_numpy() & ~np.isnan(y)
    return X[ok].to_numpy(), y[ok]

# real part
Xr, yr = make_xy(train, how[:n_train], task)
# synthetic part: a method's series of length K·T in the channels, back to real units
sv, show = from_channels(series, lo, hi)
Xs, ys = make_xy(sv, show, task)

variants = {"TRTR": (Xr, yr),                    # real train
            "TSTR": (Xs, ys)}                    # the method's synthetic data only
```

Model and metric:

```python
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import roc_auc_score, mean_absolute_error

Xte, yte = make_xy(test_values, test_how, task)       # real val / OOT

for name, (X, y) in variants.items():
    if task == "clf":
        m = LogisticRegression(max_iter=2000, class_weight="balanced").fit(X, y)
        print(name, "AUC", roc_auc_score(yte, m.predict_proba(Xte)[:, 1]))
    else:
        m = Ridge().fit(X, y)
        print(name, "MAE", mean_absolute_error(yte, m.predict(Xte)))
```

**How to compare.** The benchmark uses 10 seeds (a seed sets the generator, the
assembly and the model), the differences `TSTR(method) − TRTR` and `TSTR(method) − TSTR(random path)` on
the same test rows, and intervals by a block bootstrap over time (block = one week). The null reference
for an assembly effect is the difference between two independent random assemblies of the same pool
(`vae_rand` versus `vae_rand_b`, `mid` and `max`); in `min`, without the twin, it is the difference of
`vae_rand` between neighbouring seeds (the pool is resampled on every seed, so this reference is wider).

### What must not be broken

- The scaler, the task thresholds, any reference statistics a method takes from the real data, and
  generator training — on train only.
- The generator sees only train core windows; holdout is used only for early stopping.
- Synthetic features are computed on the synthetic series, without lags across the boundary with the real one.
- `N ≥ K`; every method yields a synthetic series of the same length `K·T`.

## Published runs

Two runs of profile `min` are published. They use the same configuration, datasets, task thresholds and
seeds on different hardware and software stacks. They used different commits of the code (the replication run
the frozen commit of 21 October 2026, the main run a commit of 23 October), which differ in names and in the
handling of results published without code; the fingerprints of all 1 440 common generation units match. Eight datasets
are identical; the prepared ETT series differs at the value level. The environment manifests of the main run
(the raw `pip freeze` of both environments, system and driver) are in `artifacts/run_h200/env/`; `envs/lock/`
holds the installable exact versions taken from them.

| | Main run | Replication run |
|---|---|---|
| GPU | 1× NVIDIA H200 (143 GB), computing infrastructure of [darya.ai](https://www.greendarya.ai/) | 1× NVIDIA L4 (24 GB), Google Colab |
| CPU cores | 192 | 12 |
| System | Ubuntu 22.04.5, driver 580.173.02; Python 3.12.13, PyTorch 2.9.1, TensorFlow 2.20.0 (manifests in `artifacts/run_h200/env/`) | Google Colab (Linux 6.6); the pinned requirements of `envs/` (exact versions not recorded) |
| Methods | 34 run, 24 ranked: the `min` suite on the VAE pool and on the zEDGE pool, the four open long-series generators and zEDGE_TS (`zedge_ts_long`, `zedge_ts_ar`) | 18 run, 13 ranked: the `min` suite on the VAE pool and the four open long-series generators |
| Role | every result of the paper, the leaderboard shown everywhere, the cost | reproduction check |
| Folder | `artifacts/run_h200/` (tables and reports; unit files on Hugging Face, `run_h200/`) | `artifacts/run_l4/` (tables and reports; unit files on Hugging Face, `run_l4/`) |

Ranks are computed within one run, and times measured on different hardware are not compared. The main
run contains its own copy of the 13 ranked methods of the replication run; ranked among themselves, they
are compared with the replication run:

- Kendall's τ between the two orders is 0.64; the first method is the same;
- every mean rank of the main run lies inside the 95 % interval of the replication run, and 12 of 13 mean
  ranks of the replication run lie inside the intervals of the main run;
- the top tier is the same except for `vae_greedy`, at its boundary (outside on the L4, p = 0.05 after Holm;
  inside on the H200);
- places 2 to 4 hold the same methods in a different order; the largest shifts are `vae_zseries` (4th → 2nd)
  and `vae_rand` (7th → 12th).

Sources of the differences, from the per-unit tables of the two runs:

1. **Trained generators** — the main source. The VAE (TensorFlow) and Diffusion-TS are retrained on another GPU
   and software stack; early stopping chooses other epochs (VAE: up to 148 epochs apart), so the weights, the
   pools and every method built on them differ (median relative difference of F1.2 between the runs: 9–28 %
   for the methods of the VAE pool, 13 % for Diffusion-TS).
2. **Sampling.** Chronos is not trained, but with the same seeds it samples other trajectories on another GPU
   (median relative difference of F1.2: 48 %).
3. **Downstream models.** On identical series (the real series, TimesFM, Timestral) the utility scores
   coincide in the median; the largest difference is 0.03 in AUC and 0.04 in MASE.
4. **Data.** The prepared ETT series of the main run (content hash `30545d98975f96a4`) differs at the value
   level from that of the replication run (`a84f966b14c63b36`, the published hash in `marathonts/bench/data_hashes.json`),
   with the same length, split and dates. The cause is not established: the series that the source gives today
   (checked on 29 October 2026) is identical to the replication run's, so `prepare` does not warn, and a new run
   reproduces the ETT data of the replication run, not of the main run. The effect on the metrics is small (at
   most 3·10⁻⁴ for the real series); the other eight datasets are identical in both runs.

The deterministic TimesFM and Timestral produce practically the same series on both GPUs (the median difference of
their fidelity values is 0; fewer than 0.3 % of the values differ by more than 1 %, at most 2.7 %),
which confirms the attribution. The agreement of the two runs is a reproducibility check, not a validation that the reported
intervals cover the variability of training, software, hardware and data. The leaderboard is read by tier, not by
place ([HYPOTHESES.md](HYPOTHESES.md), "Uncertainty and tests"): in this check tier membership reproduced up to a
borderline method, the exact place within the tier did not.

## Hardware

The benchmark is not tied to hardware: the torch part (assembly, Diffusion-TS, Chronos, models `linear` and
`mlp`, heavy fidelity metrics) runs on CUDA if available, otherwise on CPU; the `gbdt` model (XGBoost; scikit-learn
HistGradientBoosting on macOS or without xgboost, CPU only) runs on the device set in `marathonts/bench/model_configs.json`
(`"device"`: `"cpu"` in `min` and `mid`, `"auto"` — CUDA if available — in `max`); the VAE (TensorFlow) runs on GPU if
TensorFlow sees it, otherwise on CPU.
TensorFlow is switched to incremental GPU memory growth so that torch in the same process does not
run out of memory. Assembly computes in float64, so Apple MPS is not used. TPU is not
used. The recommended runtime is GPU.

Each timing record stores the hardware (`gpu`, `cpu_count`, `platform`) and library versions.
**To compare time, all methods of one dataset must be run on the same type of hardware.** Hypothesis testing warns if the timing table contains more than one GPU type.

## Stages

Stages are sequential. Each unit of work writes its own files and is skipped if they already
exist **and were made with the same settings**: the record of each unit (pool, trained replica, shared
Diffusion-TS model, series, labels) holds a fingerprint `unit_fp` — a hash of the
data settings (`data_key`, not the contents of the data), the settings of its components, the contents of `target_params*.json` /
`model_configs.json` (where they matter) and the fingerprints of the units it is made from. Change,
for example, `knn_k` (the setting of `vae_knn`), and its series and everything computed from them are redone, while the VAE pools and
the other assemblies are kept. Processed data store a data-settings key (`data_key`: only
split, number of points and `T`): `prepare` redoes them if these settings changed, and the
other stages refuse to read them otherwise. Keys are per dataset: a setting of one dataset only
(`Config.DATASET_KEYS`, the Bitcoin window `bitcoin_start` / `bitcoin_end`) enters that dataset's keys, and
a unit depends on the task thresholds of its own dataset only; the other datasets hash those settings at fixed
values (`PINNED_KEYS`) and the thresholds of the other built-in datasets enter at the values of the frozen
copies `marathonts/bench/target_params*.pinned.json` (never edit them). A changed Bitcoin window or changed thresholds of
one dataset therefore redo that dataset only.

Utility and fidelity units are fingerprinted per cell (`marathonts/bench/cells.py`): a utility unit per task × model and
the decision-transfer grid, a fidelity unit per metric group. Each cell's fingerprint holds only what it
depends on (the series, the labels, that model's configuration; that group's settings, parameters and, for
F8 / F11, the thresholds and tasks), and the cells a unit has done are listed in a registry next to it
(`cells.json`, `seed<k>.cells.json`), written last. An added model, task or metric group computes only its own
cells and adds them to the unit's files; a changed model or group redoes only its own; a failed cell is not
listed and is retried on the next run; a unit without a registry has no done cells. A model's supported task kinds come from the
environment (`gbdt` handles `ms` only with XGBoost installed), so run every stage in the same environment. The contents of the data are checked separately (§1b). Window slicing for generator training
(`max_windows`, `holdout_frac`) and pool size (`pool_size`, `pool_mult`) are not stored in the data —
they are computed from the config (`data.window_layout`) and enter only the fingerprints of what depends
on them. Pool generator training and pool sampling have different fingerprints, and generator weights
are stored with the record: a changed pool size resamples the pools from the already trained models and
redoes the methods on the pools, while VAE and Diffusion-TS training, the pretrained generators (Chronos, TimesFM,
Timestral), labels, TRTR and the fidelity of the real series are reused. Changed window slicings retrain the VAE and
Diffusion-TS, but not the pretrained generators. The thresholds of an added dataset enter only the fingerprints of
its own units: adding a dataset redoes nothing on the others. An error in one unit is written to `artifacts/errors.log` and does not
stop the run; a utility unit in which all trainings failed is retried on the next
run.

```
              0 raw ──────► data/raw/<ds>/*.parquet        (CSV/TXT → Parquet; download if missing)
                 │
              1 prepare ──► data/processed/<profile>/<ds>.parquet, <ds>.meta.parquet
                 │
              2 pools ────► artifacts/pools, generators      (in the generator's environment)
                 │
              3 generate ─► artifacts/series, records, generators (long-series generators)
                 │
              4 fidelity ─► artifacts/fidelity
                 │
              5 utility ──► artifacts/labels, utility (metrics, predictions, model weights)
                 │
              6 collect ──► artifacts/tables
                 │
              7 hypotheses ► artifacts/reports (Markdown), overall, leaderboard, metric_values, hypotheses
```

### 0. raw — `marathonts/bench/datasets.py`

Source CSV / TXT files are converted to Parquet losslessly (float64, all columns); the original is deleted
only after the row counts are checked. If the files are missing, they are downloaded from the links in the dataset registry.

### 1. prepare — `marathonts/bench/data.py`

- A dataset from the registry yields an hourly series ([DATASETS.md](DATASETS.md)): hourly mean
  (Electricity, Household, Jena), log of the last price of the hour (Bitcoin), as is (the rest).
- Gaps of up to 6 hours are interpolated, longer ones stay NaN (windows with NaN are dropped).
  Metro: the continuous part after the 2014–2015 gap is taken. Bike: a missing hour = 0 rentals.
- The last `max_points` points are taken (`min`: 10,000; `max`: the whole series).
- Time-based split (`min`: 50 / 25 / 25, `max`: 60 / 20 / 20), with an embargo of 168 between parts.
- On train: `lo, hi` for min-max, `T = 168`, `K = round(n_train / T)`, `N = max(pool_size, 2K)`
  (`pool_size` = 300), slicing stride
  `s` (`max_windows` = 5000), core / holdout boundary (last 10% of train, embargo 168).

Profile `min`: all datasets have n = 9664, train = 5000, val = OOT = 2332, K = 30, N = 300, s = 1.
Profile `max`:

| Dataset | n | n_train | K | N |
|---|---|---|---|---|
| ett | 17,084 | 10,452 | 62 | 300 |
| electricity | 34,729 | 21,039 | 125 | 300 |
| household | 34,253 | 20,753 | 124 | 300 |
| pjm | 145,056 | 87,235 | 519 | 1038 |
| beijing_pm25 | 43,464 | 26,280 | 156 | 312 |
| jena | 69,793 | 42,077 | 250 | 500 |
| metro | 28,636 | 17,383 | 103 | 300 |
| bike | 17,208 | 10,526 | 63 | 300 |
| bitcoin | 85,104 | 51,264 | 305 | 610 |

### 1a. targets — exogenous target parameters

Task thresholds (for example, "change over 24 h above X") are set in advance for each dataset in
`marathonts/bench/target_params.json` (`max` — `marathonts/bench/target_params_max.json`) and are only read during a run.
Missing values (a new dataset or a new task) are proposed by the task's rule on train when the `prepare`
stage meets them, and written to the file; the `targets` stage does the same on its own. The file is then
reviewed and committed. Without
parameters the stages fail with a hint. The file remembers which split the thresholds were computed on
(`_split_key`): with another split (other `max_points`, `split`, `embargo`) it is not read — otherwise
thresholds could come from the val or OOT of a run.

### 1b. hashes — content of the published data

The sources can change after a run: a Kaggle dataset is re-uploaded daily (Bitcoin) and may revise its
history, a file may be replaced. Fingerprints do not see this (they hash the data settings, not the
data), so `marathonts/bench/data_hashes.json` stores a content hash of each prepared series of the published results,
per data-settings key: time, value, hour of week and split, independent of the Parquet writer.
`prepare` and loading the prepared data compare against it and warn once per dataset if the series
differ — the run goes on, but its results are not comparable with the published ones. Datasets without
a published hash (custom ones, other data settings) are not checked. The `hashes` stage (not part of
`all`) adds the missing hashes for the current settings and never overwrites existing ones; run it once
after `prepare` of a run that will be published and commit the file. The file is not part of any
fingerprint: adding hashes redoes nothing.

### 2. pools — `marathonts/bench/methods.py`, `marathonts/bench/generators/`

For each (dataset, pool generator, seed) — a pool of N windows `(N, T, 3)` and its record (training and
sampling time, diagnostics). **VAE** (Protocol: pool generator, above): `tsgm` `vae_conv5` + BetaVAE,
latent 16, β = 2, early stopping on holdout; trained once per dataset (`min`) or on every seed (`mid`,
`max`), sampled on every seed. The pool is shared by all methods with this generator, so `vae_*` differ only
in the choice, order and joining of windows. The stage runs in the generator's environment (`envs/tsgm.txt`);
`generate` computes a missing pool itself when the generator's modules are importable there.

### 3. generate — `marathonts/bench/methods.py`, `marathonts/bench/generators/`, `marathonts/bench/assemblers.py`

For each (dataset, seed, method) of `methods` (the methods of `frozen_methods` are skipped) — a series of length K·T in real units, hour of week, the index of the pool
window and of the chunk at each point, a seam flag.

- **Assembly**: every assembler takes the shared pool and returns K windows in order (with seam processing —
  more, and the series is cut to K·T). Each alternative assembler uses the seam criterion of its own
  literature (BASELINES.md A); the solvers `vae_greedy`, `vae_atsp`, `vae_pctsp` get the jump at the seam —
  the Euclidean distance between the last point of a window and the first point of the next over every
  channel (`seam_jump`). `vae_zseries` is zseries, the proprietary assembler of zypl.ai (under development): its results are published (`Config.frozen_methods`),
  its code is not part of the repository; `generate` skips it and its seam-processing variants.
- **Diffusion-TS** (profiles `min` and `mid` — once per dataset, weights in `generators/<ds>/diffusion_ts/seedshared.parquet`, training time recorded for every seed — and `max` — on every seed): model from the official repository (`external/Diffusion-TS`), hyperparameters
  `Config/etth.yaml` with window length T; training by the official recipe (`engine/solver.py`): 18 000 steps,
  batch 128 with gradient accumulation 2, Adam from 1e-5 with warm-up to 8e-4 over 500 steps, then
  ReduceLROnPlateau on the training loss, EMA of the weights (0.995 every 10 steps, as `ema-pytorch` 0.2.1).
  Deviations, the same for every generator of the benchmark: early stopping on the holdout windows, as for
  the VAE; imputation — `fast_sample_infill` with 50 DDIM steps (the repository's imputation config uses
  200), for generation time. The calendar channels are known at all window positions (hour of week
  continues from a random start, different for each seed), the model completes only the value.
- **Chronos**: `amazon/chronos-t5-small` (`max`: `chronos-t5-base`), no fine-tuning, the library's default sampling (temperature 1,
  top-k 50, top-p 1), context 512, bfloat16 on GPU (`chronos-forecasting` 2.3.2). The series is one sample
  path grown in chunks of 64 (the model's prediction length), each chunk conditioned on the previous ones —
  the same as the library's `predict(prediction_length=K·T, num_samples=1)`, which feeds the median of
  the samples (here the only sample) back as context. Its training corpus (Ansari et al., 2024,
  Table 3) contains Electricity (UCI, 370 clients, 15 min / hourly / weekly) up to the last 24 points, so
  on `electricity` Chronos has seen the val and OOT periods: its results there are not out-of-sample
  (DATASETS.md). The corpus also holds KDD Cup 2018 (Beijing air quality, 2017–2018), related to
  `beijing_pm25`: Chronos is left out on `electricity` and `beijing_pm25`. ETT is used by Chronos for
  zero-shot evaluation only; the other datasets are not in the corpus. Loaded once per process; the loading
  time is recorded as `fit_wall_s` of each seed.
- **TimesFM** and **Timestral**: pretrained quantile forecasters in their median-output configurations, used
  strictly as documented, zero-shot, package defaults, no sampling. The context is the whole train split (within the model's limit: 15 360
  and 32 768 steps); the series is the median forecast of the K·T steps after it — TimesFM 3.0
  (`google/timesfm-3.0-pytorch`, package `timesfm` 3.0.2) in one non-autoregressive pass, Timestral-209M
  (`mistralai/Timestral-209M`, package `timestral`) block by block (1024 steps), each block's median fed
  back as context (seams at the block boundaries). Model revisions are pinned (`timesfm_revision`,
  `timestral_revision`). A median forecast has no noise and is the same on every seed, so the
  between-seed spread is zero: in RQ2 the margin of their comparisons is the spread of the compared method
  (HYPOTHESES.md §2); they take part in the rankings and every other question. TimesFM 3.0 is trained on GiftEvalPretrain (built on LOTSA without the GIFT-Eval test sets, and without
  the sets overlapping fev-bench), Wikimedia Pageviews (to Nov 2023), Google Trends (to 2022) and
  synthetic data (model card). Electricity, ETT and Jena weather are GIFT-Eval test sets, so not in it;
  but it holds the household dataset itself (`sceaux`, UCI #235, value-identical 2007–2010), Beijing Air
  Quality (UCI #501: PM2.5 of 12 Beijing stations, 2013–2017 — the same city, pollutant and hours as
  `beijing_pm25`) and the Monash Bitcoin set (daily price, to 2021): TimesFM is left out on `household`,
  `beijing_pm25` and `bitcoin` (exact and related pairs, DATASETS.md). Timestral's training data are not
  disclosed (mostly synthetic, real sets unnamed): its leakage cannot be checked. Licences of the
  weights: TimesFM 3.0 — TimesFM Non-Commercial License v1.0; Timestral — Modified MIT.

**Time and memory** (run record, `artifacts/records/…`):

| Field | What it measures |
|---|---|
| `fit_wall_s` | generator training (VAE, Diffusion-TS, SDV) or model loading (Chronos, TimesFM, Timestral) |
| `sample_wall_s` | pool sampling or generation of the whole series |
| `assemble_wall_s` | assembly of the series from the pool: assembly or random path |
| `total_wall_s` | sum of the three |
| `*_cpu_s`, `*_gpu_peak_mb`, `*_rss_delta_mb` | CPU time, torch GPU memory peak per block, process RAM growth per block |
| `fit_tf_gpu_peak_mb` | TensorFlow GPU memory peak during VAE training |
| diagnostics | VAE epochs and best epoch, Diffusion-TS steps, the seam-jump sum of the alternative assemblers, the model and revision of the pretrained generators, etc. |
| `gpu`, `cpu_count`, `platform` | hardware |

### 4. fidelity — `marathonts/bench/fidelity.py`

83 metrics F1–F12 from [METRICS.md](METRICS.md) for each series (245 values: against three references), in 12 registered groups
(custom groups via `register_fidelity_group`). Each metric is computed against three real
references: the primary one is **val** (`Config.fidelity_ref`, no suffix), plus `Config.fidelity_extra_refs`
(default train and OOT, suffixes `@train`, `@oot`). Train shows how well a method
reproduces what it was trained on (methods trained on train, and methods that take reference statistics from train, use
this data during fitting), val shows generalisation, OOT shows generalisation under drift. Group F10 (distance to train)
is computed once. The pseudo-method `real` is a piece of OOT, so it is not evaluated against OOT. Three
references triple the stage time (the F6.1 GRU discriminator is trained per reference);
`fidelity_extra_refs=[]` evaluates against val only. Each metric has an orientation (`ORIENT`). Pairwise distances (MMD, nearest neighbours, precision / recall) and the
GRU discriminator are computed in torch on GPU.

The pseudo-method `real` is the real OOT; the variants `<method>@len` are the method's series cut to the OOT length
(for comparison with the real series at equal length, RQ0).

| Metric | How it is computed (formulas: METRICS.md) |
|---|---|
| F5.7, F6.2 | \|AUC − 0.5\| (`*_auc_dev`): ideal is indistinguishability |
| F6.8, F10.1 | \|log of ratio\| (`*_logratio`): ideal 0 (ratio = 1) |
| F9.2 density | \|log density\| (`F9.2_density_logdev`): ideal 0 (density = 1) |
| F6.2, F6.6, F9 | window features — 16 in-house statistics |
| F6.8, F10 | Euclidean nearest-neighbour distance |
| F6.4 | unbiased MMD² estimate (no diagonals), RBF with median bandwidth |
| F5.5–F5.6 | PELT on 2-hour means of the first 40,000 points |
| F7.5 | KS of drawdown from the rolling weekly maximum |
| F7.6 | weekly trend slope in std of the real series |

### 5. utility — `marathonts/bench/utility.py`, `marathonts/bench/models.py`

Utility assesses the quality of the synthetic data: **TSTR versus TRTR**. For each (dataset, method, seed) ×
14 tasks (U2.1–U2.9) × models × splits (val, OOT) a model is trained only on the method's synthetic data and
compared with the same model trained on real data. Default models are `linear`, `mlp`
(PyTorch) and `gbdt` (XGBoost, with a scikit-learn HistGradientBoosting fallback); description, parameters and libraries are in [MODELS.md](MODELS.md).

| Regime | Training |
|---|---|
| R — TRTR (train on real, test on real) | real train (pseudo-method `real`, once per seed) |
| S — TSTR (train on synthetic, test on real) | the method's synthetic series only |

The closer TSTR is to TRTR, the more information useful to the model the synthetic data contain (transfer ratio in
the ranking and in questions RQ1, RQ4, RQ5).

Features and labels of the synthetic data are computed on the synthetic data themselves, the test only on real data (BENCHMARK.md, Protocol: utility).
Target thresholds come from train. Metrics (registry `utility_metrics`): AUC, PR AUC, Brier, log-loss,
ECE, F1, lift (binary); macro AUC, log-loss, macro F1 (multiclass); MAE, RMSE, MASE, sMAPE,
error on extremes (regression); pinball, coverage, share of quantile crossings (quantiles); MASE
over the whole horizon and the last step (multi-step). Training and prediction time of
each model are recorded. Only with `decision_transfer` (profile `max`) on the case-study task (`stitch_task`): a grid of 11
model configurations (U6.1) and threshold transfer from synthetic to real (U6.4).

### 6. collect — `marathonts/bench/run.py`

Gathers the files into `artifacts/<profile>/tables/` — **the published result of the benchmark**. The rows of the
methods of `frozen_methods` are taken from their unit files, or from the existing tables when there are none,
for the datasets, seeds and settings of their published results only (`tables/frozen.json`, written by
`python -m marathonts.bench.run freeze`; the rest is left out with a warning); `config.json` stores the paths inside the project relative to it:

| Table | Row = |
|---|---|
| `timing.parquet` | (dataset, method, seed): time, memory, diagnostics, hardware |
| `fidelity.parquet` | (dataset, method, seed): all F metrics |
| `utility.parquet` | (dataset, method, seed, task, model, regime, split): U metrics, time |
| `pools.parquet` | (dataset, pool generator, seed): training and sampling time, diagnostics |
| `cross_seed.parquet` | (dataset, method, seed pair): F9.4 — diversity across seeds |
| `datasets.parquet` | dataset: n, K, N, period, gaps |
| `descriptors.parquet` | dataset: descriptors of the train part (autocorrelation, kurtosis, volatility clustering, trend, gaps) for RQ7 and CS15, so that the analysis needs no data |
| `inventory.parquet` | each artifact file: path, kind, size |
| `hardware.parquet`, `config.json` | hardware and library versions of the environment `collect` runs in (the hardware of each run is in `timing.parquet`), run configuration |

Stage 7 (`python -m marathonts.hypotheses.run`, [HYPOTHESES.md](HYPOTHESES.md) §7) reads these tables and writes the
Markdown reports to `artifacts/<profile>/reports/` — `REPORT.md`, `OVERALL.md`, `LEADERBOARD.md`,
`METRIC_VALUES.md` — and their Parquet tables to `hypotheses/`, `overall/`, `leaderboard/` and `metric_values/`.

## Artifacts

Everything is in `artifacts/<profile>/` (path — `Config.artifacts_dir`), Parquet with zstd compression; floats are float32,
except series values (float64).

```
artifacts/<profile>/
├── pools/<ds>/<generator>/seed<k>.parquet           pool of windows (N, T, 3)
│                          seed<k>.record.parquet    training and sampling time, diagnostics
├── generators/<ds>/<generator>/seed<k>.parquet      generator weights (VAE, Diffusion-TS, SDV, custom)
├── series/<ds>/<method>/seed<k>.parquet             series: t, value, how, window, piece, seam
├── records/<ds>/<method>/seed<k>.parquet            run record: time, memory, hardware
├── fidelity/<ds>/<method>/seed<k>.parquet           all F metrics (+ seed<k>.cells.json: done metric groups)
├── labels/<ds>/<task>.parquet                       real test labels: split, row, y
├── utility/<ds>/<method>/seed<k>/
│   ├── cells.json                                   done cells (task × model, grid) with their fingerprints
│   ├── metrics.parquet                              U metrics
│   ├── predictions.parquet                          each prediction: pred or pred_vec (vector)
│   └── models.parquet                               weights of each trained model
├── tables/                                          summary tables (collect)
├── reports/                                         Markdown reports of stage 7:
│   ├── REPORT.md                                    research questions RQ0–RQ9, confirmatory family, case study
│   ├── OVERALL.md                                   overall leaderboard and its robustness checks
│   ├── LEADERBOARD.md                               rankings of every method in every slice
│   └── METRIC_VALUES.md                             values of the core fidelity metrics and the primary utility
│                                                    metrics by reference, dataset, task, model and split
├── overall/                                         overall leaderboard tables: overall.parquet,
│                                                    sensitivity, field, lodo, weights
├── leaderboard/                                     ranking tables: rankings.parquet (the four rankings),
│                                                    rankings_summary.parquet and others
├── metric_values/                                   fidelity.parquet, utility.parquet: median and IQR over
│                                                    seeds of every metric per dataset and method
├── hypotheses/                                      tables of the questions and the case study (RQ*, CS*),
│                                                    confirmatory.parquet
└── errors.log
```

Weights are loaded back into models without training — `marathonts/bench/load.py`:

```python
from marathonts.bench import load
gen = load.load_generator(cfg, "ett", "tsgm_vae", seed=0)
m = load.load_model(cfg, "ett", "vae_zseries", 0, task="clf_up_h24_q90", model="gbdt", regime="S")
series = load.load_series(cfg, "ett", "vae_zseries", 0)
```

Pools are always saved (the separate environments work through them). The rest is controlled by the flags
`Config.save_generator_weights`, `save_model_weights` (utility predictions are always saved — they
are needed by hypothesis testing); `weights_dtype="float16"` halves
the size of weight files (normalisation statistics always stay float32).
In `min` a utility unit holds about 2 MB of predictions and 0.9 MB of model weights (every dataset has
the same length there); in `max` the volume grows with the length of the series and the full boosting
configuration.

## Compute volume

Generation units: 9 datasets × 10 seeds × 12 methods = 1080 series (`mid`: 13 methods, 1170 series; `max`: 31 methods, 2790 series; the 4 published methods are not generated); VAE trainings — 9 (`min`)
or 90 (`mid`, `max`), Diffusion-TS trainings — 9 (`min`, `mid`) or 90 (`max`). The most expensive
parts:

- **Diffusion-TS, generation**: the series is built autoregressively, T/2 new points per step; for PJM —
  about 1000 sequential imputations of 50 DDIM steps per seed.
- **Assemblers on long datasets** (PJM: K = 519, N = 1038): `vae_pctsp` runs up to `pctsp_solutions` solutions (at most `pctsp_time_s`) per unit.
- **Utility**: per unit (TSTR; TRTR — once per dataset and seed), 14 tasks × 2 models (`linear`, `gbdt`)
  plus the MLP on one task (`clf_up_h24_q90`) in `min` and `mid` (29 fits; 14 × 3 = 42 in `max`), each tested on
  2 splits. Models on
  GPU (torch, XGBoost) are the main speed-up; on CPU one ETTh1 unit takes a few minutes. Units
  are independent: they can be distributed across sessions (`--datasets`, `--seeds`).
