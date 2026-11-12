# Evaluation metrics: fidelity and utility

Metrics for comparing the methods from [BASELINES.md](BASELINES.md). Each method outputs a synthetic series of length `K·T` in the same channels; all metrics below
are computed on it in the same way. Code: `marathonts/bench/fidelity.py` (fidelity), `marathonts/bench/tasks.py`, `marathonts/bench/utility.py`,
`marathonts/bench/models.py` (utility); the column names in the tables are given in the tables below.

## General conditions

- **Real reference samples for fidelity** — three: the primary one is a held-out portion of the series (val; metric
  without a suffix), plus train (`@train`) and OOT (`@oot`). Train shows how well the methods reproduce
  what they were trained on (methods that take reference statistics from the real data take them from train), val shows generalisation, OOT shows generalisation under drift. F10 (distance to train) is computed once, against val.
  The 83 metrics of F1–F12 give 245 columns per series (83 against val, 81 each against train and OOT).
- **Equal length** of the synthetic series `K·T` for all methods (group B tops up windows).
- **Reference rows.** The pseudo-method `real` is the OOT part (shorter than `K·T`; it is not scored against OOT). For the
  first seed every method is also scored on its first len(OOT) points (`<method>@len`), for the comparison with `real`
  at equal length (RQ0).
- **Seeds:** 10; a seed determines the pool sampling, the assembly, the sampling of the long-series generators and the
  downstream models; which generators are retrained per seed depends on the profile (HYPOTHESES.md, §2).
- **Noise margin:** the difference between two random paths of the same pool (`vae_rand` against `vae_rand_b`; in `min`,
  without `vae_rand_b`, the between-seed spread of `vae_rand`). Effects are expressed in units of this margin
  (HYPOTHESES.md, §2).
- **Units.** Fidelity metrics are computed in real units; where a metric compares windows, levels or durations, both
  series are first z-scored with the mean and std of the reference (`z` below). Errors of a scale (std, rates, durations)
  are given as \|log(synth / real)\|; 0 means equal.
- **Windows** (F6, F9, F10): windows of length T (and 2T) with step T/4 cut from the z-scored series, at most 3000
  per series (a random subset kept in time order). **Window features** (F6.2, F6.6, F9): 16 statistics of a window —
  mean, std, skewness, kurtosis, min, max, 10th and 90th percentiles, mean \|Δ\|, std of Δ, lag-1 and lag-24
  autocorrelation, rate of sign changes of the standardised window, relative positions of the maximum and the minimum,
  last − first value.

---

# Fidelity

The orientation of every metric (lower or higher is better) is stored in `bench.fidelity.ORIENT`; for metrics given as
a deviation (`*_err`, `*_dev`, `*_logratio`) 0 means equal to the reference.

## F1. Marginal distribution of values

| ID | Column(s) | How it is computed | Implementation |
|---|---|---|---|
| F1.1 | `F1.1_ks` | KS statistic `ks_2samp(synth, real)` | `scipy.stats` |
| F1.2 | `F1.2_w1` | Wasserstein-1 distance divided by std(real) | `scipy.stats` |
| F1.3 | `F1.3_ad` | Anderson–Darling k-sample statistic | `scipy.stats.anderson_ksamp` |
| F1.4 | `F1.4_qq_corr` | Pearson correlation of the quantiles 0.01…0.99 (99 levels) of synth and real | `numpy` |
| F1.5 | `F1.5_quantile_err`, `F1.5_q01_err`, `F1.5_q99_err` | \|q_p(synth) − q_p(real)\| / std(real): mean over p ∈ {0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99}, and p = 0.01, p = 0.99 | `numpy.quantile` |
| F1.6 | `F1.6_mean_err`, `F1.6_std_err`, `F1.6_skew_err`, `F1.6_kurt_err` | \|Δ mean\| / std(real); \|log(std ratio)\|; \|Δ skewness\|; \|Δ excess kurtosis\| | `scipy.stats` |
| F1.7 | `F1.7_out_of_range` | share of points outside [min, max] of real | in-house |
| F1.8 | `F1.8_coverage` | share of the non-empty bins of the real histogram (50 quantile bins of real) hit by the synthetic series | in-house |
| F1.9 | `F1.9_js` | Jensen–Shannon distance of the histograms on the same bins | `scipy.spatial.distance.jensenshannon` |
| F1.10 | `F1.10_hill_err` | \|Δ Hill estimate\| on the upper 5% (each series shifted by its minimum) | in-house |

## F2. Increments

Δ_k = x[t+k] − x[t].

| ID | Column(s) | How it is computed | Implementation |
|---|---|---|---|
| F2.1 | `F2.1_ks_d1`, `F2.1_ks_d6`, `F2.1_ks_d24`, `F2.1_ks_d168`, `F2.1_w1_d24` | KS of Δ_k for k ∈ {1, 6, 24, 168}; W1 of Δ_24 divided by std(Δ_24 real) | `scipy.stats` |
| F2.2 | `F2.2_vol_ratio_err_d1`, `F2.2_vol_ratio_err_d24` | \|log(std(Δ_k synth) / std(Δ_k real))\|, k ∈ {1, 24} | in-house |
| F2.3 | `F2.3_up_share_err` | \|Δ share of Δ_1 > 0\| | in-house |
| F2.4 | `F2.4_big_jump_share_err` | \|share of \|Δ_1\| above the 99th percentile of real − 0.01\| | in-house |

## F3. Temporal dependence

| ID | Column(s) | How it is computed | Implementation |
|---|---|---|---|
| F3.1 | `F3.1_acf_in_window` | MAE of the ACF, lags 1…T−1 | in-house |
| F3.2 | `F3.2_acf_beyond_window` | MAE of the ACF, lags T…3T (longer than one window) | in-house |
| F3.3 | `F3.3_pacf` | MAE of the PACF, lags 1…48 | `statsmodels.tsa.stattools.pacf` |
| F3.4 | `F3.4_acf_abs_d`, `F3.4_acf_sq_d` | MAE of the ACF (lags 1…48) of \|Δ_1\| and of Δ_1² (volatility clustering) | in-house |
| F3.5 | `F3.5_log_psd` | mean \|log10 PSD(synth) − log10 PSD(real)\| of the normalised Welch spectra (nperseg 512) | `scipy.signal.welch` |
| F3.6 | `F3.6_peak24_err`, `F3.6_peak168_err` | \|Δ share of spectral power\| at the daily (24) and weekly (168) frequency (3 bins around it) | in-house, on top of F3.5 |
| F3.7 | `F3.7_dfa_err` | \|Δ DFA exponent\| (detrended fluctuation analysis, scales 16…256) | in-house |
| F3.8 | `F3.8_calendar_corr_err` | mean \|Δ correlation\| of the value with sin and cos of the hour of week | in-house |

## F4. Seasonality and calendar

| ID | Column(s) | How it is computed | Implementation |
|---|---|---|---|
| F4.1 | `F4.1_how_mean` | MAE between the mean profiles over the 168 hours of the week (z) | `pandas.groupby` |
| F4.2 | `F4.2_how_std` | MAE between the std profiles over the 168 hours (z) | `pandas.groupby` |
| F4.3 | `F4.3_hod_mean` | MAE between the mean profiles over the 24 hours of the day (z) | `pandas.groupby` |
| F4.4 | `F4.4_calendar_continuity` | share of steps where the hour of week of the synthetic series increases by exactly +1 (mod 168) | in-house |
| F4.5 | `F4.5_calendar_seam_breaks` | share of seams at which this step is not +1 | in-house |

## F5. Seams

Defined for series with recorded seams: the assembled series (window boundaries) and the long-series generators that
produce the series in chunks (Diffusion-TS, Chronos: chunk boundaries). For a series without seams the seam metrics
(F4.5, F5.1–F5.4, F5.6, F5.7) are NaN.

| ID | Column(s) | How it is computed | Implementation |
|---|---|---|---|
| F5.1 | `F5.1_ks_seam_vs_real` | KS between Δ_1 at seams and Δ_1 of real | `scipy.stats` |
| F5.2 | `F5.2_ks_seam_vs_inside` | KS between Δ_1 at seams and Δ_1 elsewhere in the synthetic series | `scipy.stats` |
| F5.3 | `F5.3_seam_z_mean`, `F5.3_seam_z_p95` | \|Δ_1 at a seam\| / std(Δ_1 real): mean and 95th percentile | in-house |
| F5.4 | `F5.4_seam_local_acf` | \|Δ\| of the mean lag-1 autocorrelation in a ±24-point window around seams and around random positions | in-house |
| F5.5 | `F5.5_cp_rate_err` | \|Δ number of change points per 1000 points\|, synth against real (PELT, l2 cost, on 2-hour means of the first 40,000 points) | `ruptures` |
| F5.6 | `F5.6_cp_at_seams` | share of the detected change points within ±3 points of a seam | `ruptures` |
| F5.7 | `F5.7_seam_detect_auc_dev` | \|AUC − 0.5\| of a logistic regression (5-fold) telling a ±o snippet (o = max(`edge_overlap`, 6)) around a seam from one at a random position away from seams | `sklearn` |

## F6. Distribution of windows (multivariate fidelity)

| ID | Column(s) | How it is computed | Implementation |
|---|---|---|---|
| F6.1 | `F6.1_disc_score` | \|accuracy − 0.5\| of a post-hoc GRU classifier (hidden size 16, `disc_epochs` epochs) real vs synth on windows of length T; windows overlap, so the split is by time (first 80% of the windows of each class for training, last 20% for testing) | in-house (torch), after [TimeGAN](https://github.com/jsyoon0823/TimeGAN) |
| F6.2 | `F6.2_c2st_auc_dev` | \|AUC − 0.5\| of a HistGradientBoosting classifier on window features; 5 stratified folds without shuffling (consecutive time segments) | `sklearn` |
| F6.3 | `F6.3_pred_score_err` | \|MAE(synth) − MAE(real)\| / std(real) of a one-step ridge forecast on 24 lags, tested on the second half of the reference; MAE(synth): fitted on the synthetic series, MAE(real): fitted on the first half of the reference | `sklearn` |
| F6.4 | `F6.4_mmd`, `F6.4_mmd_2T` | unbiased MMD² (RBF kernel, median-heuristic bandwidth) between windows of length T (every 4th point) and 2T (every 8th point) | in-house (torch) |
| F6.6 | `F6.6_feature_fid` | Fréchet distance between the window features of synth and real | in-house |
| F6.8 | `F6.8_nn_dist_logratio` | \|log\| of the ratio of the median Euclidean nearest-neighbour distance synth → real (first half of the real windows) to the same distance real (second half) → real (first half) | in-house (torch) |

## F7. Long-range structure of the whole series

| ID | Column(s) | How it is computed | Implementation |
|---|---|---|---|
| F7.1 | `F7.1_roll_mean_ks` | KS of the rolling mean (z), mean over the windows 168 and 720 | `pandas.rolling` |
| F7.2 | `F7.2_roll_std_ks` | KS of the rolling std (z), mean over the windows 168 and 720 | `pandas.rolling` |
| F7.3 | `F7.3_crossings_err` | \|log\| of the ratio of the crossing rates of the real 0.1, 0.5 and 0.9 quantiles, mean over the three levels | in-house |
| F7.4 | `F7.4_excursion_ks` | KS of the lengths of runs above the real 0.9 quantile and below the real 0.1 quantile, mean of the two | in-house |
| F7.5 | `F7.5_drawdown_ks` | KS of the drawdown from the rolling weekly (168) maximum (z) | in-house |
| F7.6 | `F7.6_trend_err`, `F7.6_weekly_level_std_err` | \|Δ slope of the linear trend\| per week in units of std(real); \|log\| of the ratio of the std of the weekly means (z) | `numpy.polyfit` |
| F7.7 | `F7.7_regime_dur_err` | \|log\| of the ratio of the mean durations of the high-variance regime of a 2-state Gaussian HMM fitted on Δ_1 of the reference | `hmmlearn` |

## F8. Target

For the case-study task `Config.stitch_task` (default U2.1, `clf_up_h24_q90`), with its exogenous threshold (`target_params`).

| ID | Column(s) | How it is computed | Implementation |
|---|---|---|---|
| F8.1 | `F8.1_class_tvd` | \|Δ share of y = 1\| (TVD of the two-class distribution) | in-house |
| F8.2 | `F8.2_event_dur_ks` | KS of the lengths of runs of y = 1 | in-house |
| F8.3 | `F8.3_interarrival_ks` | KS of the intervals between the starts of runs of y = 1 | in-house |
| F8.4 | `F8.4_event_by_how` | MAE of the profile P(y = 1 \| hour of week) | `pandas.groupby` |
| F8.5 | `F8.5_cond_event_err` | mean \|Δ P(y = 1 \| bin)\| over the quintile bins (real edges) of the past differences d1, d24, d168 | in-house |
| F8.6 | `F8.6_cond_future_ks` | KS of the 24-step change x[t+24] − x[t] conditional on the quintile bin (real edges) of x[t], mean over the 5 bins | in-house |

## F9. Diversity and coverage

| ID | Column(s) | How it is computed | Implementation |
|---|---|---|---|
| F9.1 | `F9.1_precision`, `F9.1_recall` | precision / recall (k = 5 nearest neighbours) on window features standardised by real (Naeem et al., 2020) | in-house (torch), after [prdc](https://github.com/clovaai/generative-evaluation-prdc) |
| F9.2 | `F9.2_density_logdev`, `F9.2_coverage` | \|log density\| (0 at density 1) and coverage, same features | in-house (torch) |
| F9.4 | `F9.4_between_seed_mmd` (table `cross_seed`) | MMD² between the windows of seed k and seed k + 1 of the same method; computed in `collect`, not one of the 83 per-series metrics | in-house |

## F10. Memorisation

Against train, once per series (reference windows: val).

| ID | Column(s) | How it is computed | Implementation |
|---|---|---|---|
| F10.1 | `F10.1_dcr_logratio` | \|log\| of the ratio of the median distance to the nearest train window (DCR): synth → train against val → train | in-house (torch) |
| F10.2 | `F10.2_near_copy_share` | share of synth windows whose DCR is below the 5th percentile of the val → train DCR | in-house |

## F11. Class balance

Over all classification tasks of the run (F8 covers only the case-study task U2.1, `stitch_task`). Task thresholds are exogenous
(`target_params`), as in utility. A rare event is a task with tail probability ≤ 5%
(q ≥ 0.95 or q ≤ 0.05), fixed in advance rather than from the data.

| ID | Column | How it is computed | Implementation |
|---|---|---|---|
| F11.1 | `F11.1_class_share_logratio` | mean over binary tasks of \|log((share_synth + ε) / (share_real + ε))\|, ε = 10⁻⁴ — a relative error, so a rare class weighs as much as a frequent one | in-house |
| F11.2 | `F11.2_rare_share_logratio` | the same over rare tasks only | in-house |
| F11.3 | `F11.3_multiclass_tvd` | TVD of the class distribution, mean over multiclass tasks | in-house |
| F11.4 | `F11.4_minority_lost` | share of binary tasks where the synthetic series has no positive example | in-house |

## F12. Outliers and extremes

| ID | Column | How it is computed | Implementation |
|---|---|---|---|
| F12.1 | `F12.1_exceed_rate_err` | \|log\| of the ratio of the shares of points beyond the real 0.5% and 99.5% quantiles | in-house |
| F12.2 | `F12.2_exceed_magnitude_err` | \|mean exceedance over the threshold, synth − real\| in units of the std of real | in-house |
| F12.3 | `F12.3_spike_rate_err` | \|log\| of the ratio of the shares of points where \|x − rolling median(25)\| exceeds the 99.5% quantile of the same residual of real | in-house |
| F12.4 | `F12.4_block_max_ks` | KS of weekly (168 h) maxima, synth against real | in-house |
| F12.5 | `F12.5_block_min_ks` | KS of weekly minima | in-house |

All F metrics except F10 (and F9.4) are computed against three references: val (no suffix), train (`@train`)
and OOT (`@oot`).

---

# Utility

The base protocol is BENCHMARK.md, Protocol: utility: features and labels are computed on the synthetic series separately, testing is
on real data only. Features (`bench.tasks.features`): the value, the differences at lags 1, 2, 3, 6, 12, 24, 48, 168 and
sin / cos of the hour of week.

## U1. Training regimes

Utility measures the quality of the synthetic data: a model trained only on
synthetic data is compared with a model trained on real data, on the same real
test rows. The benchmark has two regimes (`bench.config.REGIMES`):

| ID | Regime | What is trained on | What it shows |
|---|---|---|---|
| U1.5 | TSTR (S) — train on synthetic, test on real | only the method's synthetic series | how much information useful to a model the synthetic data carry; methods are compared by TSTR (the control `vae_rand` stands for "just other windows of the same pool") |
| U1.6 | TRTR (R) — train on real, test on real | only real train (pseudo-method `real`, once per dataset and seed) | reference for TSTR; transfer ratio = TSTR relative to TRTR (1 means TSTR equals TRTR) |

Regimes that combine real and synthetic data measure the benefit of augmentation rather than the quality of the
synthetic data and are not part of the benchmark.

## U2. Tasks

14 registered tasks (`marathonts/bench/tasks.py`). Thresholds are exogenous quantiles of the real train changes, fixed in
`marathonts/bench/target_params.json` (`target_params_max.json` for `max`).

| ID | Task (name) | Description |
|---|---|---|
| U2.1 | `clf_up_h24_q90` | change over h = 24 above the train 0.90 quantile; task of the case-study cells (`stitch_task`) |
| U2.2 | `clf_up_h1_q90`, `clf_up_h6_q90`, `clf_up_h168_q90` | the same at h ∈ {1, 6, 168} |
| U2.3 | `clf_up_h24_q95`, `clf_up_h24_q99` | rare events: q ∈ {0.95, 0.99} |
| U2.4 | `clf_down_h24_q10` | change over h = 24 below the train 0.10 quantile |
| U2.5 | `mc3_h24` | down / neutral / up: change over 24 h below the 0.10, between, above the 0.90 quantile |
| U2.6 | `reg_h1`, `reg_h24`, `reg_h168` | value `x[t+h]`, h ∈ {1, 24, 168} |
| U2.7 | `qreg_h24` | quantiles 0.1, 0.5, 0.9 of `x[t+24]` |
| U2.8 | `ms_h24` | the whole vector `x[t+1 : t+24]` |
| U2.9 | `vol_h24` | std of the changes over the next 24 hours |

## U3. Models

Description, hyperparameters and libraries: [MODELS.md](MODELS.md). Default models: `linear`, `gbdt`, `mlp`
(`mlp` on U2.1 only in `min` and `mid`, on every task in `max`).

| ID | Model | Implementation |
|---|---|---|
| U3.1 | `linear`: logistic / softmax regression, ridge, linear quantile regression | in-house (`torch`); `sk_linear`: `sklearn` |
| U3.2 | `gbdt`: gradient-boosted trees | `xgboost` (fallback: `sklearn` HistGradientBoosting); `sk_hgb`: `sklearn` |
| U3.4 | `mlp`: fully connected network 64 → 32 on the same features | in-house (`torch`); `sk_mlp`: `sklearn` |

## U4. Quality metrics

Column names of the utility table. Scale-dependent errors are divided by the MASE scale: the MAE of the seasonal
naive forecast (lag 168) on the real train (`bench.tasks.seasonal_naive_scale`).

| ID | Task | Metric (column) |
|---|---|---|
| U4.1 | classification | ROC AUC (`auc`; multiclass: macro one-vs-rest) |
| U4.2 | binary | PR AUC, average precision (`pr_auc`) |
| U4.3 | classification | Brier score (`brier`, binary), log-loss (`logloss`) |
| U4.4 | binary | ECE, 10 equal-width bins (`ece`) |
| U4.5 | classification | F1 at the threshold at which the share of predicted positives equals the positive share of the real train (`f1`); multiclass: macro F1 of the argmax (`macro_f1`) |
| U4.6 | binary | lift in the top decile of the predicted probability (`lift10`) |
| U4.7 | regression, volatility, multi-step | MAE, RMSE (`mae`, `rmse`; multi-step: `mae`) |
| U4.8 | regression, volatility, multi-step | MASE (`mase`; multi-step: over the whole horizon, and `mase_last` at the last step) |
| U4.9 | regression, volatility | sMAPE, mean of 2\|e\| / (\|y\| + \|ŷ\|) (`smape`) |
| U4.10 | quantile regression | pinball loss, mean over the three quantiles, divided by the MASE scale (`pinball`); coverage of the 10–90% interval (`coverage80`) and \|coverage − 0.8\| (`coverage80_err`); share of rows with crossing quantiles (`crossing_share`) |
| U4.12 | regression, volatility | MAE on the test rows whose target is in the lower or upper 5% of the test targets, divided by the MASE scale (`mae_extreme`) |

The primary metric of each task type (hyperparameter search, rankings): AUC (binary), log-loss (multiclass), MASE
(regression, volatility, multi-step), pinball (quantiles).

## U5. Test splits

| ID | Split | What it shows |
|---|---|---|
| U5.1 | val | test on the period after train (after an embargo of 168 rows); primary reference for fidelity |
| U5.2 | OOT | test on the last period, shift over time; split of the confirmatory and case-study pre-specified cells |
| U5.4 | by hour of week | difference on weekdays / weekends (hour of week < 120 / ≥ 120) — exploratory, CS12 |
| U5.5 | by volatility regime | difference in calm / middle / turbulent periods (terciles of the 24-hour rolling mean of \|Δ_1\| of the real series) — exploratory, CS12 |

## U6. Transfer of decisions from synthetic to real

Profile `max` (`Config.decision_transfer`), task `Config.model_grid_task` (U2.1), RQ5 (c).

| ID | Metric | How it is computed |
|---|---|---|
| U6.1 | Agreement of configuration rankings | every configuration of the grids of the classification models of the run (`model_configs.json` → `grids`; 11 for `linear`, `gbdt`, `mlp`) is trained on real train and on the synthetic series and scored by AUC on val; Spearman correlation between the two sets of AUC |
| U6.4 | Threshold transfer | `linear` trained on the first 80% of the synthetic rows; the F1-maximising threshold (grid 0.05…0.95) chosen on the last 20% of the synthetic rows is applied on val; F1 at that threshold divided by F1 at the threshold chosen on val |

## U7. Statistical procedure

Details: [HYPOTHESES.md](HYPOTHESES.md), §2. Implementation: `marathonts/hypotheses/stats.py`, `marathonts/hypotheses/engine.py`.

| ID | Procedure | Implementation |
|---|---|---|
| U7.1 | Paired differences d = orientation · (A − B) on the same seeds (within a dataset) and the same test rows | in-house |
| U7.2 | Moving-block bootstrap of the test rows (block = 168 rows, `Config.boot_block`) for row-level differences of seed-averaged predictions; two-level bootstrap (datasets, then seeds) for intervals across datasets | in-house |
| U7.3 | Wilcoxon signed-rank (one-sided both ways), sign test, one-sample t-test, TOST against the noise margin, Hodges–Lehmann effect | `scipy.stats`, in-house |
| U7.4 | Multiple-comparison correction (Holm, Benjamini–Hochberg) | in-house |
| U7.5 | Ranks of methods across datasets: Friedman test + Nemenyi critical difference; top tier by one-sided Wilcoxon against the first method with Holm | `scipy.stats`, in-house |

## U8. Cost

Recorded per series in the `timing` table (`marathonts/bench/timing.py`) on the hardware of the run; analysed in RQ6.

| ID | Metric | How it is computed |
|---|---|---|
| U8.1 | Time | wall-clock and CPU time of generator training (`fit_*`), sampling (`sample_*`) and assembly (`assemble_*`); `total_wall_s` |
| U8.2 | Memory | peak GPU memory (`*_gpu_peak_mb`, torch; `fit_tf_gpu_peak_mb`, TensorFlow) and resident-memory increase (`*_rss_delta_mb`) |
