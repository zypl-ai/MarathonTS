# Utility ML models

Models that are trained either on real data or only on synthetic data
and evaluated on real data (the `utility` stage, section U3 of [METRICS.md](METRICS.md)). Code:
`marathonts/bench/models.py`; models are selected by name: `Config(models=[...])` or `--models`. You can add your own
model through the registry ([EXTENDING.md](EXTENDING.md)).

By default three models are used: `linear`, `gbdt`, `mlp` (`Config.models`). In the `min` and `mid` profiles `mlp`
runs on the task U2.1 (`clf_up_h24_q90`) only (`Config.model_tasks`); in `max` every model runs on every task it supports.

## Configurations: exogenous, tuning optional

All hyperparameters are fixed in advance in `marathonts/bench/model_configs.json` — the code only reads them, nothing is
tuned on the data. The same file holds the grids (`grids`) for two optional features:

- **hyperparameter tuning** (`Config.hpo`, profile `max`): for each training run the model's grid is
  searched; each configuration is trained on the regime's own training data without its last 20% (`hpo_val_frac`;
  R: the real train, S: the synthetic series) and evaluated on that tail by the task's primary metric (AUC, log-loss, MASE, pinball); the best one is
  retrained on all the data. Val and OOT do not take part in the tuning. The selected configuration
  is written to the `params` column of the utility table. Between the training part and the tail there is a gap of
  h + 168 rows, so that the labels and lags of the training part do not reach into the tail;
- **grid for RQ5 (c)** (`Config.decision_transfer`, profile `max`): all configurations of the grids of the
  classification models are trained on real data and on synthetic data for the task `Config.model_grid_task` (U2.1)
  and scored by AUC on val — the check is whether their rankings agree (METRICS.md, U6.1).

In the `min` (the Colab run) and `mid` profiles both are off: each model has a single fixed configuration.
An explicit override for a run: `Config(extra={"<model>": {...}})`.

## Summary

| Name | Family | Library | Tasks | Where it runs |
|---|---|---|---|---|
| `linear` | logistic / softmax regression, ridge, linear quantile regression | PyTorch (in-house implementation) | all | GPU (CUDA), otherwise CPU |
| `mlp` | fully connected network 64 → 32 | PyTorch (in-house implementation) | all (`min`, `mid`: U2.1 only) | GPU (CUDA), otherwise CPU |
| `gbdt` | gradient-boosted trees | XGBoost; fallback — scikit-learn | all (with XGBoost) | XGBoost — GPU or all CPU cores |
| `sk_linear` | same as `linear` | scikit-learn | all (quantiles via `linear`) | CPU |
| `sk_hgb` | HistGradientBoosting | scikit-learn | all except multi-step | CPU |
| `sk_mlp` | MLP 64 → 32 | scikit-learn | all except quantile | CPU |

The `sk_*` models are scikit-learn implementations of the same model families, for running without a GPU; they are
not used by default.

## Tasks and what the model predicts

| Task type (`kind`) | Tasks (METRICS U2) | Model output |
|---|---|---|
| `clf` — binary classification | U2.1–U2.4: upper and lower tails, different horizons and quantiles | P(y = 1), `(n,)` |
| `mc` — multiclass | U2.5: down / neutral / up | class probabilities, `(n, 3)` |
| `reg` — regression | U2.6: value h = 1, 24, 168 hours ahead | `(n,)` |
| `qreg` — quantile regression | U2.7: quantiles 0.1 / 0.5 / 0.9 | `(n, 3)` |
| `ms` — multi-step forecast | U2.8: vector of values 24 hours ahead | `(n, 24)` |
| `vol` — volatility | U2.9: std of changes over the next 24 hours | `(n,)` |

**Class weights and calibration.** Classifiers (all except `sk_mlp`) are trained with balanced
class weights, so their probabilities correspond to equal class shares. In the `utility` stage
the probabilities are mapped back to the class shares of the training sample of their regime (real train for
TRTR, synthetic series for TSTR):
P(c | x) ∝ P_bal(c | x) · share(c) (`bench.models.prior_correct`). AUC, PR AUC, lift and F1 at the
quantile threshold are unaffected by this, whereas Brier, log-loss and ECE then measure calibration rather
than reweighting. The saved predictions are already corrected; a model loaded via
`load.load_model` returns raw probabilities — to obtain the same values, apply `prior_correct`
with the training labels.

**Training regimes.** Each model is trained in two regimes: R — TRTR, on the real train
(pseudo-method `real`), and S — TSTR, only on the method's synthetic series; the test for both is the same
real val / OOT. Early stopping of the MLP (profile `max`) holds out 10% of *distinct* rows of its
training sample.

All models use the same features: the series value, differences at lags 1, 2, 3, 6, 12, 24, 48, 168 and
sin / cos of the hour of week (BENCHMARK.md, Protocol: utility). All models standardise the features on the training sample; for
regression tasks `linear` and `mlp` also standardise the target and return the forecast in the original
units.

## `linear` — linear models in PyTorch

Source: in-house implementation in `marathonts/bench/models.py` on top of **PyTorch** (`torch`, `torch.optim.LBFGS`,
`torch.linalg.solve`). Trained on the whole sample at once (full batch), on the GPU if one is available.

| Task | Model | Loss function and regularisation | Optimisation |
|---|---|---|---|
| `clf` | logistic regression | weighted binary cross-entropy (class weights `balanced`) + L2 `‖W‖² / (2C)`, C = 1 | L-BFGS with strong Wolfe, up to 300 iterations |
| `mc` | softmax regression | weighted cross-entropy (`balanced`) + L2, C = 1 | L-BFGS |
| `reg`, `vol`, `ms` | ridge | MSE + L2, α = 1 | exact solution `(XᵀX + αI) W = XᵀY` |
| `qreg` | linear quantile regression | smoothed pinball loss `q·u + ε·softplus(−u/ε)`, ε = 10⁻³, all three quantiles at once | L-BFGS |

The objective function for `clf` and `mc` coincides with `LogisticRegression(class_weight="balanced", C=1)`
from scikit-learn.

Saved weights: `W`, `b`, the mean and std of the features, the mean and std of the target.

## `mlp` — neural network in PyTorch

Source: in-house implementation in `marathonts/bench/models.py` in **PyTorch** (`torch.nn`, `torch.optim.Adam`).

- Architecture: `Linear(d, 64) → ReLU → Linear(64, 32) → ReLU → Linear(32, k)`; k is the number of outputs
  of the task (1, 3, 24).
- Optimisation: Adam, learning rate 10⁻³, L2 via `weight_decay` = 10⁻⁴, batch 512.
- Number of epochs: fixed, 30 (`epochs`), without early stopping — profile `min`. In profile `max`
  — up to 200 epochs with early stopping (`early_stopping_patience` = 10): 10% of the distinct rows (random, with a
  seed) are used for validation, and the weights of the epoch with the lowest validation loss are returned.
- The architecture (`hidden`) is also set in the configuration: (64, 32) by default.
- Losses: `clf` — binary cross-entropy with `pos_weight = (1 − p) / p` (class balance);
  `mc` — cross-entropy with class weights `balanced`; `reg`, `vol`, `ms` — MSE; `qreg` —
  smoothed pinball loss over the three quantiles.

Saved weights: the network's `state_dict`, the mean and std of the features and of the target.

## `gbdt` — gradient boosting

Source: the **XGBoost** library (`xgboost.XGBClassifier`, `xgboost.XGBRegressor`).

| Parameter | `min`, `mid` (light, `model_configs.json`) | `max` (full) |
|---|---|---|
| trees (`n_estimators`) | 100 | 200 |
| depth (`max_depth`) | 4 | 6 (in the tuning grid: 2, 4, 6, 8) |
| learning rate | 0.2 | 0.1 |
| histogram bins (`max_bin`) | 64 | 256 |
| where it runs (`device`) | CPU: on ~10,000 rows faster than GPU | CUDA if available |
| multi-step task (`multi_strategy_ms`) | `multi_output_tree`: a single ensemble with vector leaves for 24 outputs | `one_output_per_tree`: a separate ensemble for each step |

Timing on data of `min` size (2 CPU threads): binary task 0.08 s versus 0.37 s for the full configuration,
multi-step 0.95 s versus 10.3 s.

| Task | XGBoost objective |
|---|---|
| `clf` | `binary:logistic`, `scale_pos_weight = (1 − p) / p` |
| `mc` | `multi:softprob`, sample weights `balanced` (a class absent from training — a row with weight ~0) |
| `reg`, `vol` | `reg:squarederror` |
| `qreg` | `reg:quantileerror`, `quantile_alpha = [0.1, 0.5, 0.9]` — one model for all three quantiles |
| `ms` | `reg:squarederror`, strategy from `multi_strategy_ms` |

Saved weights: the XGBoost booster in the binary UBJSON format.

**Fallback.** If XGBoost is not installed, or on macOS (there torch and xgboost load two
different OpenMP libraries, and xgboost crashes in the same process as torch), `gbdt` uses
`HistGradientBoosting` from **scikit-learn** (the `sk_hgb` implementation) with the `gbdt` parameters `n_estimators`
(as `max_iter`), `max_depth` and `learning_rate`; the multi-step task is then skipped. The choice is set by the environment variable `BENCH_GBDT_BACKEND=xgboost|sklearn`. In Docker
and in Colab (Linux) XGBoost is used. The two are different models under one name: a run on the fallback
warns at the start of the utility stage, marks its rows (`"_backend": "sklearn"` in `params`) and `collect`
warns when such rows are in the tables. The expected cells of `gbdt` follow XGBoost (`GBDT.all_kinds`), so
results made with XGBoost stay valid in an environment without it and its multi-step cells are left to an
environment that has it — run every stage in one environment.

## scikit-learn models (`sk_*`)

Source: **scikit-learn**.

| Name | sklearn classes | Parameters |
|---|---|---|
| `sk_linear` | `StandardScaler` + `LogisticRegression` (`clf`, `mc`), `Ridge` (`reg`, `vol`, `ms`) | `class_weight="balanced"`, C = 1, `max_iter=2000`; α = 1. Quantiles via `linear` |
| `sk_hgb` | `HistGradientBoostingClassifier` / `HistGradientBoostingRegressor` | `max_iter=200`, unlimited depth, learning rate 0.1, without early stopping, `class_weight="balanced"`; quantiles — three models with `loss="quantile"` |
| `sk_mlp` | `StandardScaler` + `MLPClassifier` / `MLPRegressor` | `hidden_layer_sizes=(64, 32)`, without early stopping, 30 epochs, α = 10⁻⁴ |

Saved weights: the fitted scikit-learn object (pickle, zstd-compressed inside Parquet).

## Grids (hyperparameter tuning and RQ5 (c))

`marathonts/bench/model_configs.json` → `grids`; each grid point is applied on top of the fixed
configuration of the model:

| Model | Grid |
|---|---|
| `linear` | (C, α ridge) = (0.01, 10), (0.1, 3), (1, 1), (10, 0.1) |
| `gbdt` | depth 2, 4, 6, 8 |
| `mlp` | weight decay 10⁻⁴, 10⁻²; hidden layers (128, 64) |
| `sk_hgb` | depth 2, 4, unlimited |

## Saving and loading

The weights of each trained model are written to `artifacts/<profile>/utility/<dataset>/<method>/seed<k>/models.parquet`
under the key `<task>|<model>|<regime>|<parameter>`. A model is loaded back and predicts without
retraining:

```python
from marathonts.bench import load
m = load.load_model(cfg, "ett", "vae_zseries", 0, task="clf_up_h24_q90", model="gbdt", regime="S")
X, y, _ = load.task_xy(cfg, "ett", "clf_up_h24_q90", split="oot")
p = m.predict(X)
```

The weights of the tuning candidates and of the RQ5 (c) grid are not saved: they contribute metrics to the table, and for the final
model the selected configuration (`params`).

## Library versions

| Library | Used for | Installation |
|---|---|---|
| PyTorch | `linear`, `mlp` | `pip install torch` (already present in Colab and in the Docker image) |
| XGBoost | `gbdt` | `pip install xgboost` (version ≥ 2.0: quantiles and multi-output; `envs/core.txt`) |
| scikit-learn | `sk_*`, fallback `gbdt`, quality metrics | `pip install scikit-learn` |

The requirements are in `envs/core.txt`. The installed versions (`bench.timing.library_versions`) are written to
`artifacts/<profile>/tables/hardware.parquet` by `collect`, for the environment in which `collect` runs; the
configuration of the run is in `artifacts/<profile>/tables/config.json`.
