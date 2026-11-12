# Benchmark report

Datasets: beijing_pm25, bike, bitcoin, electricity, ett, household, jena, metro, pjm. Seeds: 10. α = 0.05. Metrics left out: F5.1_ks_seam_vs_real, F5.2_ks_seam_vs_inside, F5.3_seam_z_mean, F5.3_seam_z_p95, F5.4_seam_local_acf, F5.6_cp_at_seams, F5.7_seam_detect_auc_dev (Config.exclude_metrics). Leakage (Config.leaked): `chronos` on electricity, beijing_pm25; `timesfm` on beijing_pm25, household, bitcoin. Verdict of a comparison "A vs B": better / worse (A better / worse than B) / same (equivalence, TOST) / inconclusive. Effects are in noise units — divided by the smallest effect size of interest (SESOI: the median |vae_rand − vae_rand_b| on one pool — or, where vae_rand_b is not run (min), the between-seed spread of vae_rand — or the method's between-seed spread, see HYPOTHESES.md §2). Utility: TSTR (training on synthetic data only) vs TRTR (training on real data), tested on the real val / OOT; transfer ratio = 1 — synthetic data train the model as well as real data. Overall leaderboard — `OVERALL.md`; ranking of every method in every slice — `LEADERBOARD.md`; values of the metrics by slice — `METRIC_VALUES.md` (this folder). Tables of the tests — `hypotheses/`.

## Overall leaderboard

Fidelity on the core metrics (each criterion against train, val and OOT) and utility (TSTR classification and regression, val and OOT), equal weights; noise-aware ranks; privacy and cost not included. Composition, columns and the robustness checks — `OVERALL.md`.

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon | fidelity_rank | utility_rank | norm_overall | memorisation_flag |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| vae_herding | optimised selection | 5.44 | 4.72 | 6.11 | 0.786 | 1 |  | True | 4.99 | 5.9 | 0.266 | False |
| diffusion_ts | long-series generator | 6.13 | 4.57 | 7.48 | 0.103 | 0.672 | 0.375 | True | 6.54 | 5.71 | 0.161 | False |
| vae_zseries | optimised selection | 6.31 | 5.54 | 7.14 | 0.081 | 0.589 | 0.375 | True | 5.79 | 6.84 | 0.0662 | False |
| vae_quilting | optimised selection | 6.68 | 6.07 | 7.32 | 0.001 | 0.228 | 0.328 | True | 6.85 | 6.5 | 0.103 | False |
| timesfm | long-series generator | 6.72 | 5.29 | 8.27 | 0.027 | 0.384 | 0.375 | True | 7.37 | 6.06 | 0.0118 | False |
| vae_atsp | optimised selection | 7.04 | 6.48 | 7.71 | 0 | 0.017 | 0.141 | True | 6.73 | 7.35 | 0.0214 | False |
| vae_rand | random selection | 7.11 | 6.22 | 7.92 | 0 | 0.071 | 0.137 | True | 6.85 | 7.37 | 0 | False |
| vae_mbb | optimised selection | 7.12 | 6.31 | 7.87 | 0 | 0.028 | 0.0879 | True | 6.92 | 7.32 | 0.0422 | False |
| vae_pctsp | optimised selection | 7.28 | 6.74 | 7.8 | 0 | 0 | 0.0645 | True | 6.96 | 7.6 | -0.0349 | False |
| vae_knn | optimised selection | 7.44 | 6.89 | 8.02 | 0 | 0 | 0.0879 | True | 7.36 | 7.52 | 0.0286 | False |
| vae_greedy | optimised selection | 7.44 | 6.99 | 7.97 | 0 | 0 | 0.0645 | True | 7.32 | 7.56 | 0.00686 | False |
| chronos | long-series generator | 7.84 | 6.41 | 9.08 | 0.002 | 0.011 | 0.141 | True | 8.69 | 6.98 | -0.034 | False |
| timestral | long-series generator | 8.56 | 7.46 | 9.5 | 0 | 0 | 0.0469 | False | 9.14 | 7.98 | -0.857 | False |


Sensitivity variants:

| variant | text | first | tau_vs_main | main_first_place |
|---|---|---|---|---|
| main | the leaderboard: core metrics, fidelity against train + val + OOT, noise-aware ranks | vae_herding | 1 | 1 |
| plain_ranks | ordinary average ranks (no ties within the noise) | vae_herding | 0.974 | 1 |
| fidelity_train | fidelity against train only | vae_herding | 0.923 | 1 |
| fidelity_holdout | fidelity against val + OOT only | vae_herding | 0.974 | 1 |
| no_unchecked | without F5.7 (seams, no anchor) and F6.1 against val (noise) | vae_herding | 0.949 | 1 |
| all_metrics | every fidelity metric instead of the core set | vae_herding | 0.872 | 1 |
| common_datasets | only the datasets where every method is ranked | vae_herding | 0.821 | 1 |


## Confirmatory inference (C1–C4; TSTR, linear model, OOT; one classification and regression task; Holm over the whole family)

| test | cell | comparison | n_datasets | median_z | ci_lo | ci_hi | p_two_sided | p_holm | p_equiv_holm | n_better | n_worse | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C1 methods differ | clf_up_h24_q90\|linear\|oot | Friedman, all methods | 9 |  |  |  | 0.286 | 1 | 1 |  |  | inconclusive |
| C2 long vs assembly | clf_up_h24_q90\|linear\|oot | diffusion_ts vs assembly_median | 9 | 1.23 | 0.544 | 10.2 | 0.129 | 0.773 | 1 | 5 | 2 | inconclusive |
| C2 long vs assembly | clf_up_h24_q90\|linear\|oot | chronos vs assembly_median | 7 | -0.531 | -16.1 | 1.38 | 0.469 | 1 | 1 | 1 | 3 | inconclusive |
| C3 selection | clf_up_h24_q90\|linear\|oot | optimised selection (mean) vs random | 9 | -0.126 | -0.896 | 1.14 | 0.734 | 1 | 0.82 | 2 | 1 | inconclusive |
| C4 seam processing | clf_up_h24_q90\|linear\|oot | any joiner vs none (all paths) | 9 | -0.776 | -2.16 | -0.282 | 0.0547 | 0.383 | 1 | 0 | 4 | inconclusive |
| C1 methods differ | reg_h24\|linear\|oot | Friedman, all methods | 9 |  |  |  | 0.000115 | 0.00115 | 1 |  |  | differ |
| C2 long vs assembly | reg_h24\|linear\|oot | diffusion_ts vs assembly_median | 9 | 5.56 | 2.09 | 9.99 | 0.0391 | 0.312 | 1 | 5 | 0 | inconclusive |
| C2 long vs assembly | reg_h24\|linear\|oot | chronos vs assembly_median | 7 | 0.758 | -0.0604 | 5.69 | 0.219 | 1 | 1 | 2 | 0 | inconclusive |
| C3 selection | reg_h24\|linear\|oot | optimised selection (mean) vs random | 9 | 0.235 | -1.59 | 1.58 | 0.91 | 1 | 1 | 3 | 3 | inconclusive |
| C4 seam processing | reg_h24\|linear\|oot | any joiner vs none (all paths) | 9 | -0.73 | -3.14 | -0.729 | 0.00391 | 0.0352 | 1 | 0 | 4 | inconclusive |


## The four rankings (RQ1)

Composition of each ranking, the meaning of every column and the privacy and cost tables — `LEADERBOARD.md`.

- `holdout_clf` — **Fidelity: val + OOT; utility: classification**. Fidelity domain — the criteria distribution (F1, F2, F12), dependence (F3, F4), windows (F6, F9), long structure (F7), target (F8, F11), seams (F5), each against val and OOT (each criterion is the mean of the two). Utility domain — TSTR classification (binary and multiclass tasks), primary metric of each task type, tested on val and OOT. Rank = mean of the two domains with equal weight. Not included: privacy (F10), time, memory.
- `holdout_reg` — **Fidelity: val + OOT; utility: regression**. Fidelity domain — the criteria distribution (F1, F2, F12), dependence (F3, F4), windows (F6, F9), long structure (F7), target (F8, F11), seams (F5), each against val and OOT (each criterion is the mean of the two). Utility domain — TSTR regression (point, quantile, multi-step and volatility tasks), primary metric of each task type, tested on val and OOT. Rank = mean of the two domains with equal weight. Not included: privacy (F10), time, memory.
- `train_clf` — **Fidelity: train; utility: classification**. Fidelity domain — the criteria distribution (F1, F2, F12), dependence (F3, F4), windows (F6, F9), long structure (F7), target (F8, F11), seams (F5), each against train. Utility domain — TSTR classification (binary and multiclass tasks), primary metric of each task type, tested on val and OOT. Rank = mean of the two domains with equal weight. Not included: privacy (F10), time, memory.
- `train_reg` — **Fidelity: train; utility: regression**. Fidelity domain — the criteria distribution (F1, F2, F12), dependence (F3, F4), windows (F6, F9), long structure (F7), target (F8, F11), seams (F5), each against train. Utility domain — TSTR regression (point, quantile, multi-step and volatility tasks), primary metric of each task type, tested on val and OOT. Rank = mean of the two domains with equal weight. Not included: privacy (F10), time, memory.

| method | family | holdout_clf:rank | holdout_clf:p_first | holdout_clf:tier | holdout_reg:rank | holdout_reg:p_first | holdout_reg:tier | train_clf:rank | train_clf:p_first | train_clf:tier | train_reg:rank | train_reg:p_first | train_reg:tier | first_in |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| chronos | long-series generator | 7.74 | 0.009 | True | 6.74 | 0.008 | True | 8.09 | 0 | True | 7.08 | 0 | True |  |
| diffusion_ts | long-series generator | 6.19 | 0.212 | True | 5.75 | 0.205 | True | 6.04 | 0.128 | True | 5.6 | 0.246 | True |  |
| timesfm | long-series generator | 7.57 | 0.009 | True | 5.32 | 0.696 | True | 7.56 | 0.001 | True | 5.31 | 0.56 | True | holdout_reg, train_reg |
| timestral | long-series generator | 9.45 | 0 | True | 6.9 | 0 | True | 10.1 | 0 | False | 7.52 | 0 | True |  |
| vae_atsp | optimised selection | 6.95 | 0 | True | 7.45 | 0 | True | 6.87 | 0 | False | 7.37 | 0 | True |  |
| vae_greedy | optimised selection | 7.19 | 0 | True | 7.76 | 0 | True | 7.31 | 0 | False | 7.87 | 0 | True |  |
| vae_herding | optimised selection | 5.7 | 0.63 | True | 6.3 | 0.034 | True | 5.13 | 0.858 | True | 5.74 | 0.12 | True | holdout_clf, train_clf |
| vae_knn | optimised selection | 7.14 | 0 | True | 7.71 | 0 | True | 7.29 | 0 | False | 7.86 | 0 | True |  |
| vae_mbb | optimised selection | 6.9 | 0.002 | True | 7.66 | 0 | True | 6.88 | 0 | False | 7.64 | 0 | True |  |
| vae_pctsp | optimised selection | 6.96 | 0 | True | 7.56 | 0 | True | 6.97 | 0 | False | 7.56 | 0 | True |  |
| vae_quilting | optimised selection | 6.22 | 0.12 | True | 6.89 | 0 | True | 6.28 | 0.011 | True | 6.95 | 0 | True |  |
| vae_zseries | optimised selection | 6.54 | 0.017 | True | 6.66 | 0.057 | True | 6.21 | 0.002 | True | 6.34 | 0.074 | True |  |
| vae_rand | random selection | 6.83 | 0.001 | True | 7.72 | 0 | True | 6.8 | 0 | False | 7.69 | 0 | True |  |


### Ranking `holdout_clf`: Fidelity: val + OOT; utility: classification

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| vae_herding | optimised selection | 5.7 | 5.11 | 6.21 | 0.63 | 0.987 |  | True |
| diffusion_ts | long-series generator | 6.19 | 4.69 | 7.54 | 0.212 | 0.61 | 0.656 | True |
| vae_quilting | optimised selection | 6.22 | 5.66 | 6.83 | 0.12 | 0.744 | 0.656 | True |
| vae_zseries | optimised selection | 6.54 | 5.87 | 7.21 | 0.017 | 0.363 | 0.41 | True |
| vae_rand | random selection | 6.83 | 6.04 | 7.61 | 0.001 | 0.105 | 0.26 | True |
| vae_mbb | optimised selection | 6.9 | 6.12 | 7.62 | 0.002 | 0.048 | 0.26 | True |
| vae_atsp | optimised selection | 6.95 | 6.36 | 7.67 | 0 | 0.006 | 0.176 | True |
| vae_pctsp | optimised selection | 6.96 | 6.45 | 7.5 | 0 | 0 | 0.137 | True |
| vae_knn | optimised selection | 7.14 | 6.58 | 7.7 | 0 | 0 | 0.176 | True |
| vae_greedy | optimised selection | 7.19 | 6.73 | 7.73 | 0 | 0 | 0.107 | True |
| timesfm | long-series generator | 7.57 | 5.74 | 9.41 | 0.009 | 0.091 | 0.656 | True |
| chronos | long-series generator | 7.74 | 6.1 | 9.18 | 0.009 | 0.046 | 0.438 | True |
| timestral | long-series generator | 9.45 | 8.19 | 10.6 | 0 | 0 | 0.0703 | True |


### Ranking `holdout_reg`: Fidelity: val + OOT; utility: regression

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| timesfm | long-series generator | 5.32 | 3.83 | 7.08 | 0.696 | 0.931 |  | True |
| diffusion_ts | long-series generator | 5.75 | 4.52 | 6.9 | 0.205 | 0.875 | 0.781 | True |
| vae_herding | optimised selection | 6.3 | 5.33 | 7.24 | 0.034 | 0.543 | 0.781 | True |
| vae_zseries | optimised selection | 6.66 | 5.86 | 7.45 | 0.057 | 0.217 | 0.781 | True |
| chronos | long-series generator | 6.74 | 5.35 | 7.93 | 0.008 | 0.225 | 0.781 | True |
| vae_quilting | optimised selection | 6.89 | 6.39 | 7.47 | 0 | 0.054 | 0.781 | True |
| timestral | long-series generator | 6.9 | 5.74 | 8.01 | 0 | 0.13 | 0.562 | True |
| vae_atsp | optimised selection | 7.45 | 6.87 | 8.13 | 0 | 0.002 | 0.781 | True |
| vae_pctsp | optimised selection | 7.56 | 7.09 | 8.05 | 0 | 0.002 | 0.781 | True |
| vae_mbb | optimised selection | 7.66 | 6.85 | 8.36 | 0 | 0.009 | 0.781 | True |
| vae_knn | optimised selection | 7.71 | 7.08 | 8.3 | 0 | 0 | 0.781 | True |
| vae_rand | random selection | 7.72 | 6.8 | 8.52 | 0 | 0.012 | 0.562 | True |
| vae_greedy | optimised selection | 7.76 | 7.24 | 8.33 | 0 | 0 | 0.781 | True |


### Ranking `train_clf`: Fidelity: train; utility: classification

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| vae_herding | optimised selection | 5.13 | 4.67 | 5.59 | 0.858 | 0.998 |  | True |
| diffusion_ts | long-series generator | 6.04 | 4.48 | 7.43 | 0.128 | 0.623 | 0.219 | True |
| vae_zseries | optimised selection | 6.21 | 5.43 | 7.02 | 0.002 | 0.584 | 0.0977 | True |
| vae_quilting | optimised selection | 6.28 | 5.53 | 7.01 | 0.011 | 0.565 | 0.109 | True |
| vae_rand | random selection | 6.8 | 6.03 | 7.53 | 0 | 0.078 | 0.0352 | False |
| vae_atsp | optimised selection | 6.87 | 6.22 | 7.62 | 0 | 0.022 | 0.0352 | False |
| vae_mbb | optimised selection | 6.88 | 6.09 | 7.58 | 0 | 0.03 | 0.0352 | False |
| vae_pctsp | optimised selection | 6.97 | 6.33 | 7.6 | 0 | 0.002 | 0.0352 | False |
| vae_knn | optimised selection | 7.29 | 6.85 | 7.79 | 0 | 0 | 0.0234 | False |
| vae_greedy | optimised selection | 7.31 | 6.83 | 7.81 | 0 | 0 | 0.0234 | False |
| timesfm | long-series generator | 7.56 | 5.82 | 9.44 | 0.001 | 0.086 | 0.219 | True |
| chronos | long-series generator | 8.09 | 6.48 | 9.5 | 0 | 0.012 | 0.117 | True |
| timestral | long-series generator | 10.1 | 8.72 | 11.2 | 0 | 0 | 0.0234 | False |


### Ranking `train_reg`: Fidelity: train; utility: regression

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| timesfm | long-series generator | 5.31 | 3.89 | 6.85 | 0.56 | 0.898 |  | True |
| diffusion_ts | long-series generator | 5.6 | 4.3 | 6.76 | 0.246 | 0.826 | 0.703 | True |
| vae_herding | optimised selection | 5.74 | 4.99 | 6.51 | 0.12 | 0.903 | 0.703 | True |
| vae_zseries | optimised selection | 6.34 | 5.47 | 7.25 | 0.074 | 0.303 | 0.703 | True |
| vae_quilting | optimised selection | 6.95 | 6.29 | 7.63 | 0 | 0.012 | 0.703 | True |
| chronos | long-series generator | 7.08 | 5.77 | 8.24 | 0 | 0.046 | 0.703 | True |
| vae_atsp | optimised selection | 7.37 | 6.67 | 8.07 | 0 | 0.001 | 0.516 | True |
| timestral | long-series generator | 7.52 | 6.37 | 8.61 | 0 | 0.004 | 0.188 | True |
| vae_pctsp | optimised selection | 7.56 | 6.96 | 8.12 | 0 | 0.001 | 0.703 | True |
| vae_mbb | optimised selection | 7.64 | 6.88 | 8.29 | 0 | 0.002 | 0.703 | True |
| vae_rand | random selection | 7.69 | 6.82 | 8.44 | 0 | 0.004 | 0.516 | True |
| vae_knn | optimised selection | 7.86 | 7.38 | 8.35 | 0 | 0 | 0.703 | True |
| vae_greedy | optimised selection | 7.87 | 7.44 | 8.35 | 0 | 0 | 0.703 | True |



## Core-metric rankings (RQ1)

The four rankings with the fidelity domain restricted to the core metric set, fixed in advance: distribution (F1.2_w1, F2.1_ks_d24); dependence (F3.5_log_psd, F4.1_how_mean); windows (F6.1_disc_score, F6.4_mmd); long structure (F7.1_roll_mean_ks, F7.2_roll_std_ks); target (F11.1_class_share_logratio); seams (F5.7_seam_detect_auc_dev). Utility unchanged. Each core ranking, the normalised scores (random assembly = 0, real data = 1) and the anchor check — `LEADERBOARD.md`.

| method | family | core_holdout_clf:rank | core_holdout_clf:p_first | core_holdout_clf:tier | core_holdout_reg:rank | core_holdout_reg:p_first | core_holdout_reg:tier | core_train_clf:rank | core_train_clf:p_first | core_train_clf:tier | core_train_reg:rank | core_train_reg:p_first | core_train_reg:tier | first_in |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| chronos | long-series generator | 8.12 | 0.002 | True | 7.12 | 0.007 | True | 8.76 | 0 | False | 7.75 | 0 | True |  |
| diffusion_ts | long-series generator | 6.29 | 0.067 | True | 5.85 | 0.183 | True | 6.24 | 0.013 | True | 5.8 | 0.054 | True |  |
| timesfm | long-series generator | 7.76 | 0 | True | 5.51 | 0.567 | True | 7.7 | 0 | True | 5.44 | 0.246 | True | core_holdout_reg |
| timestral | long-series generator | 9.5 | 0 | False | 6.95 | 0 | True | 10.6 | 0 | False | 8.01 | 0 | False |  |
| vae_atsp | optimised selection | 6.93 | 0 | True | 7.42 | 0 | True | 6.66 | 0 | False | 7.15 | 0 | False |  |
| vae_greedy | optimised selection | 7.19 | 0 | True | 7.76 | 0 | True | 7.32 | 0 | False | 7.88 | 0 | False |  |
| vae_herding | optimised selection | 5.35 | 0.815 | True | 5.95 | 0.132 | True | 4.37 | 0.985 | True | 4.98 | 0.631 | True | core_holdout_clf, core_train_clf, core_train_reg |
| vae_knn | optimised selection | 7.18 | 0 | True | 7.75 | 0 | True | 7.41 | 0 | False | 7.97 | 0 | False |  |
| vae_mbb | optimised selection | 6.84 | 0 | True | 7.6 | 0 | True | 6.7 | 0 | False | 7.46 | 0 | False |  |
| vae_pctsp | optimised selection | 7.06 | 0 | True | 7.65 | 0 | True | 6.94 | 0 | False | 7.53 | 0 | False |  |
| vae_quilting | optimised selection | 6.18 | 0.073 | True | 6.85 | 0.001 | True | 6.42 | 0 | True | 7.1 | 0 | False |  |
| vae_zseries | optimised selection | 6.32 | 0.039 | True | 6.45 | 0.108 | True | 5.95 | 0.002 | True | 6.07 | 0.069 | True |  |
| vae_rand | random selection | 6.78 | 0.004 | True | 7.67 | 0.002 | True | 6.6 | 0 | False | 7.49 | 0 | False |  |


### Normalised scores on the core metrics (random assembly = 0, real data = 1)

| method | fidelity | utility | dependence | distribution | long_structure | target | windows | classification | regression |
|---|---|---|---|---|---|---|---|---|---|
| chronos | -0.672 | 0.157 | 0.181 | -0.631 | 0.141 | -0.712 | -0.33 | -0.2 | 0.605 |
| diffusion_ts | 0.55 | 0.305 | 0.0205 | 0.979 | 0.595 | -1.06 | -0.236 | 0.113 | 0.413 |
| timesfm | 0.05 | 0.608 | -0.0522 | 0.351 | 0.25 | -2.96 | -0.521 | 0.393 | 0.827 |
| timestral | -0 | 0.072 | -0.313 | 0.664 | 0.0975 | -8.46 | 0.282 | -1.02 | 0.686 |
| vae_atsp | -0 | 0.0618 | -0.258 | -0.14 | 0.0223 | 0.108 | 0.187 | -0.0202 | 0.138 |
| vae_greedy | 0.0996 | 0.0802 | -0.637 | -0.0325 | 0.326 | 0.116 | -0.0289 | 0.0575 | 0.0723 |
| vae_herding | 0.608 | 0.147 | 0.0381 | 0.632 | 0.433 | 0.349 | 0.355 | 0.129 | 0.213 |
| vae_knn | 0.114 | 0.091 | -0.151 | 0.0248 | 0.13 | -0.0187 | -0.182 | 0.0971 | 0.096 |
| vae_mbb | 0.0832 | -0.00302 | 0.0373 | 0.111 | 0.149 | 0.0157 | 0.166 | -0.0151 | -0.00783 |
| vae_pctsp | 0.0809 | 0.103 | -0.362 | -0.104 | 0.00459 | -0.395 | 0 | 0.128 | 0.0751 |
| vae_quilting | 0.245 | 0.195 | -0.316 | 0.361 | 0.00791 | 0.0964 | 0.158 | 0.0682 | 0.222 |
| vae_zseries | 0.0653 | 0.097 | -0.221 | -0.197 | 0.0112 | 0.526 | 0.102 | 0.0406 | 0.136 |
| vae_rand | 0 | -0 | -0 | 0 | -0 | -0 | -0 | 0 | -0 |



## Summary

| Question | Verdicts by comparison |
|---|---|
| RQ0. Benchmark validity: noise, real-data ceiling, discriminative power and redundancy of the metrics | discriminative metrics: 122 of 276 |
| RQ1. Ranking of every method in every slice | first by ranking: holdout_clf — vae_herding (Friedman p = 0.0226); holdout_reg — timesfm (Friedman p = 0.106); train_clf — vae_herding (Friedman p = 0.00232); train_reg — timesfm (Friedman p = 0.0158) |
| RQ2. Assembly from a window pool vs long-series generators | inconclusive: 1612 |
| RQ3. Within assembly: window selection × seam processing | same: 590, inconclusive: 2238 |
| RQ4. Does fidelity predict utility (which metrics, against which reference) | predictive pairs: 0 of 872 |
| RQ5. Gap to real data (TSTR / TRTR), stability over time and across models | worse than real: 64 |
| RQ6. Speed and cost: training and generation time, memory, Pareto front "quality × time" | fastest: timestral (7 s) |
| RQ7. Moderators: dataset descriptors and the effects of RQ2 / RQ3 (exploratory) | significant after BH: 0 of 128 |
| RQ8. Class balance: do methods preserve class shares (rare events especially) and what does an error cost | inconclusive: 572 |
| RQ9. Outliers and extremes: do methods preserve tails and outliers, and does it matter to the models | inconclusive: 690 |

## Research questions

### RQ0. Benchmark validity: noise, real-data ceiling, discriminative power and redundancy of the metrics

| unit | kind | group | reference | n_datasets | n_methods | p_friedman | spread_over_noise | p_friedman_bh | discriminative |
|---|---|---|---|---|---|---|---|---|---|
| F1.10_hill_err | fidelity | F1_marginal | val | 9 | 14 | 0.959 | 0.61 | 0.984 | False |
| F1.10_hill_err@oot | fidelity | F1_marginal | oot | 9 | 14 | 0.651 | 1.04 | 0.743 | False |
| F1.10_hill_err@train | fidelity | F1_marginal | train | 9 | 14 | 0.0975 | 0.941 | 0.159 | False |
| F1.1_ks | fidelity | F1_marginal | val | 9 | 14 | 0.365 | 2.33 | 0.466 | False |
| F1.1_ks@oot | fidelity | F1_marginal | oot | 9 | 14 | 0.289 | 1.75 | 0.384 | False |
| F1.1_ks@train | fidelity | F1_marginal | train | 9 | 14 | 6.69e-08 | 2.03 | 1.85e-06 | True |
| F1.2_w1 | fidelity | F1_marginal | val | 9 | 14 | 0.133 | 1.91 | 0.204 | False |
| F1.2_w1@oot | fidelity | F1_marginal | oot | 9 | 14 | 0.927 | 2.16 | 0.971 | False |
| F1.2_w1@train | fidelity | F1_marginal | train | 9 | 14 | 1.55e-05 | 2.26 | 0.000125 | True |
| F1.3_ad | fidelity | F1_marginal | val | 9 | 14 | 0.131 | 3.01 | 0.203 | False |
| F1.3_ad@oot | fidelity | F1_marginal | oot | 9 | 14 | 0.684 | 2.21 | 0.768 | False |
| F1.3_ad@train | fidelity | F1_marginal | train | 9 | 14 | 2.6e-06 | 2.65 | 3.33e-05 | True |
| F1.4_qq_corr | fidelity | F1_marginal | val | 9 | 14 | 0.938 | 1.27 | 0.972 | False |
| F1.4_qq_corr@oot | fidelity | F1_marginal | oot | 9 | 14 | 0.238 | 1.24 | 0.324 | False |
| F1.4_qq_corr@train | fidelity | F1_marginal | train | 9 | 14 | 0.101 | 1.26 | 0.162 | False |
| F1.5_q01_err | fidelity | F1_marginal | val | 9 | 14 | 0.053 | 1.56 | 0.0938 | False |
| F1.5_q01_err@oot | fidelity | F1_marginal | oot | 9 | 14 | 0.00105 | 1.56 | 0.00452 | True |
| F1.5_q01_err@train | fidelity | F1_marginal | train | 9 | 14 | 0.00655 | 1.71 | 0.0178 | True |
| F1.5_q99_err | fidelity | F1_marginal | val | 9 | 14 | 0.708 | 2.32 | 0.788 | False |
| F1.5_q99_err@oot | fidelity | F1_marginal | oot | 9 | 14 | 0.00214 | 2.23 | 0.00757 | True |
| F1.5_q99_err@train | fidelity | F1_marginal | train | 9 | 14 | 0.0847 | 2.54 | 0.141 | False |
| F1.5_quantile_err | fidelity | F1_marginal | val | 9 | 14 | 0.249 | 2.54 | 0.336 | False |
| F1.5_quantile_err@oot | fidelity | F1_marginal | oot | 9 | 14 | 0.933 | 1.65 | 0.971 | False |
| F1.5_quantile_err@train | fidelity | F1_marginal | train | 9 | 14 | 2.67e-06 | 2.5 | 3.33e-05 | True |
| F1.6_kurt_err | fidelity | F1_marginal | val | 9 | 14 | 0.66 | 1.09 | 0.75 | False |
| F1.6_kurt_err@oot | fidelity | F1_marginal | oot | 9 | 14 | 0.129 | 1.32 | 0.199 | False |
| F1.6_kurt_err@train | fidelity | F1_marginal | train | 9 | 14 | 0.617 | 1.46 | 0.727 | False |
| F1.6_mean_err | fidelity | F1_marginal | val | 9 | 14 | 0.0836 | 2.1 | 0.14 | False |
| F1.6_mean_err@oot | fidelity | F1_marginal | oot | 9 | 14 | 0.94 | 2.18 | 0.972 | False |
| F1.6_mean_err@train | fidelity | F1_marginal | train | 9 | 14 | 0.00021 | 2.26 | 0.00116 | True |
| F1.6_skew_err | fidelity | F1_marginal | val | 9 | 14 | 0.652 | 1.21 | 0.743 | False |
| F1.6_skew_err@oot | fidelity | F1_marginal | oot | 9 | 14 | 0.0177 | 0.937 | 0.038 | False |
| F1.6_skew_err@train | fidelity | F1_marginal | train | 9 | 14 | 0.0575 | 1.54 | 0.101 | False |
| F1.6_std_err | fidelity | F1_marginal | val | 9 | 14 | 0.97 | 1.46 | 0.984 | False |
| F1.6_std_err@oot | fidelity | F1_marginal | oot | 9 | 14 | 0.143 | 1.9 | 0.216 | False |
| F1.6_std_err@train | fidelity | F1_marginal | train | 9 | 14 | 0.0768 | 1.98 | 0.131 | False |
| F1.7_out_of_range | fidelity | F1_marginal | val | 9 | 14 | 0.232 | 1.38 | 0.318 | False |
| F1.7_out_of_range@oot | fidelity | F1_marginal | oot | 9 | 14 | 0.0517 | 0.73 | 0.0921 | False |
| F1.7_out_of_range@train | fidelity | F1_marginal | train | 9 | 14 | 0.528 |  | 0.63 | False |
| F1.8_coverage | fidelity | F1_marginal | val | 9 | 14 | 0.00171 | 2.63 | 0.00665 | True |

_Showing 40 rows of 276; all of them — `hypotheses/RQ0_global.parquet`._

**ceiling_share_real_better**

| unit | chronos | diffusion_ts | timesfm | timestral | vae_atsp | vae_greedy | vae_herding | vae_knn | vae_mbb | vae_pctsp | vae_quilting | vae_rand |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F1.10_hill_err | 0.714 | 0.556 | 0.5 | 0.889 | 0.667 | 0.444 | 0.556 | 0.444 | 0.333 | 0.667 | 0.444 | 0.444 |
| F1.10_hill_err@train | 0.714 | 0.667 | 0.833 | 0.889 | 0.778 | 0.778 | 0.667 | 0.667 | 0.444 | 0.667 | 0.556 | 0.667 |
| F1.1_ks | 0.571 | 0.556 | 0.333 | 0.556 | 0.889 | 0.778 | 0.778 | 0.667 | 0.778 | 0.778 | 0.667 | 0.778 |
| F1.1_ks@train | 1 | 0.556 | 1 | 1 | 0.778 | 0.778 | 0.556 | 0.778 | 0.667 | 0.667 | 0.667 | 0.667 |
| F1.2_w1 | 0.571 | 0.556 | 0.167 | 0.333 | 0.778 | 0.667 | 0.778 | 0.667 | 0.778 | 0.778 | 0.778 | 0.778 |
| F1.2_w1@train | 1 | 0.667 | 0.833 | 0.889 | 0.667 | 0.667 | 0.333 | 0.778 | 0.556 | 0.667 | 0.667 | 0.556 |
| F1.3_ad | 0.571 | 0.556 | 0.333 | 0.667 | 0.889 | 0.889 | 1 | 0.667 | 0.778 | 0.778 | 0.778 | 0.778 |
| F1.3_ad@train | 1 | 0.667 | 0.833 | 0.889 | 0.778 | 0.778 | 0.667 | 0.778 | 0.778 | 0.667 | 0.667 | 0.778 |
| F1.4_qq_corr | 0.714 | 0.333 | 0.667 | 0.667 | 0.778 | 0.444 | 0.556 | 0.444 | 0.667 | 0.778 | 0.778 | 0.556 |
| F1.4_qq_corr@train | 0.714 | 0.444 | 0.833 | 0.889 | 0.778 | 0.444 | 0.667 | 0.667 | 0.778 | 0.889 | 0.889 | 0.889 |
| F1.5_q01_err | 0.714 | 0.556 | 0.333 | 0.778 | 0.667 | 0.667 | 0.667 | 0.778 | 0.667 | 0.778 | 0.778 | 0.667 |
| F1.5_q01_err@train | 0.857 | 0.556 | 0.5 | 0.778 | 0.667 | 0.556 | 0.444 | 0.556 | 0.444 | 0.778 | 0.444 | 0.444 |
| F1.5_q99_err | 0.429 | 0.667 | 0.5 | 0.667 | 0.778 | 0.667 | 0.889 | 0.778 | 0.778 | 1 | 0.889 | 0.889 |
| F1.5_q99_err@train | 1 | 0.222 | 0.5 | 0.667 | 0.556 | 0.667 | 0.556 | 0.556 | 0.444 | 0.444 | 0.222 | 0.333 |
| F1.5_quantile_err | 0.571 | 0.444 | 0.667 | 0.556 | 0.889 | 0.778 | 0.889 | 0.778 | 0.778 | 0.778 | 0.778 | 0.889 |
| F1.5_quantile_err@train | 1 | 0.444 | 0.833 | 1 | 0.667 | 0.667 | 0.444 | 0.667 | 0.556 | 0.556 | 0.556 | 0.444 |
| F1.6_kurt_err | 0.857 | 0.556 | 0.5 | 0.667 | 0.556 | 0.556 | 0.333 | 0.556 | 0.667 | 0.444 | 0.556 | 0.778 |
| F1.6_kurt_err@train | 0.714 | 0.667 | 0.833 | 0.778 | 0.556 | 0.556 | 0.333 | 0.889 | 0.556 | 0.667 | 0.778 | 0.556 |
| F1.6_mean_err | 0.571 | 0.556 | 0.333 | 0.333 | 0.778 | 0.778 | 0.889 | 0.667 | 0.778 | 0.778 | 0.778 | 0.778 |
| F1.6_mean_err@train | 0.857 | 0.778 | 0.833 | 0.889 | 0.667 | 0.667 | 0.222 | 0.667 | 0.556 | 0.556 | 0.667 | 0.556 |
| F1.6_skew_err | 0.571 | 0.222 | 0.5 | 0.556 | 0.667 | 0.444 | 0.444 | 0.444 | 0.444 | 0.444 | 0.667 | 0.667 |
| F1.6_skew_err@train | 0.714 | 0.333 | 0.667 | 0.778 | 0.667 | 0.333 | 0.667 | 0.778 | 0.778 | 0.667 | 0.778 | 0.556 |
| F1.6_std_err | 0.714 | 0.556 | 0.667 | 0.667 | 0.556 | 0.667 | 0.778 | 0.444 | 0.556 | 0.667 | 0.556 | 0.667 |
| F1.6_std_err@train | 1 | 0.556 | 0.5 | 0.778 | 0.667 | 0.667 | 0.444 | 0.556 | 0.556 | 0.556 | 0.444 | 0.444 |
| F1.7_out_of_range | 0.429 | 0.556 | 0.167 | 0.111 | 0.444 | 0.444 | 0.556 | 0.333 | 0.667 | 0.556 | 0.556 | 0.556 |
| F1.7_out_of_range@train | 0.429 | 0 | 0.167 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| F1.8_coverage | 0.714 | 0.333 | 1 | 1 | 0.667 | 0.778 | 0.667 | 0.556 | 0.444 | 0.778 | 0.667 | 0.667 |
| F1.8_coverage@train | 1 | 0.222 | 0.667 | 1 | 0.556 | 0.778 | 0.444 | 0.778 | 0.444 | 0.667 | 0.444 | 0.333 |
| F1.9_js | 0.714 | 0.444 | 0.667 | 0.778 | 0.889 | 0.778 | 0.667 | 0.667 | 0.667 | 0.889 | 0.778 | 0.667 |
| F1.9_js@train | 0.857 | 0.556 | 1 | 1 | 0.889 | 0.889 | 0.667 | 0.778 | 0.667 | 0.667 | 0.667 | 0.667 |
| F10.1_dcr_logratio | 0.429 | 0.444 | 0.5 | 0.444 | 0.556 | 0.556 | 0.333 | 0.556 | 0.556 | 0.667 | 0.556 | 0.444 |
| F10.2_near_copy_share | 0.286 | 0.333 | 0.333 | 0.333 | 0.111 | 0.222 | 0.222 | 0.333 | 0.333 | 0.333 | 0.333 | 0.333 |
| F11.1_class_share_logratio | 1 | 0.667 | 1 | 1 | 0.778 | 0.778 | 0.889 | 0.889 | 0.889 | 0.889 | 0.889 | 0.889 |
| F11.1_class_share_logratio@train | 1 | 0.889 | 1 | 1 | 0.889 | 1 | 0.889 | 1 | 0.889 | 1 | 0.889 | 0.889 |
| F11.2_rare_share_logratio | 0.857 | 0.667 | 1 | 0.889 | 0.667 | 1 | 0.667 | 0.667 | 0.889 | 0.667 | 0.778 | 0.778 |
| F11.2_rare_share_logratio@train | 1 | 0.889 | 0.833 | 1 | 0.778 | 0.889 | 0.889 | 0.889 | 0.778 | 0.778 | 0.667 | 0.778 |
| F11.3_multiclass_tvd | 0.857 | 0.778 | 1 | 0.889 | 0.778 | 0.778 | 0.778 | 0.889 | 0.889 | 0.778 | 0.889 | 0.778 |
| F11.3_multiclass_tvd@train | 0.714 | 0.667 | 1 | 1 | 0.667 | 0.556 | 0.667 | 0.778 | 0.667 | 0.778 | 0.667 | 0.778 |
| F11.4_minority_lost | 0.286 | 0.111 | 0.833 | 1 | 0 | 0.111 | 0 | 0 | 0 | 0 | 0 | 0 |
| F11.4_minority_lost@train | 0.286 | 0.222 | 0.833 | 1 | 0 | 0.222 | 0 | 0 | 0 | 0.111 | 0 | 0 |


**uninformative_metrics**: F1.6_skew_err, F1.7_out_of_range@train, F10.2_near_copy_share, F11.4_minority_lost, F11.4_minority_lost@train, F12.2_exceed_magnitude_err@train, F12.3_spike_rate_err, F6.1_disc_score, F7.6_trend_err, F7.6_trend_err@train, F7.7_regime_dur_err

**discriminative_share_by_group**

| kind | group | oot | train | val |
|---|---|---|---|---|
| fidelity | F10_memorisation |  |  | 0.5 |
| fidelity | F11_class_balance | 0.25 | 0.75 | 0.75 |
| fidelity | F12_extremes | 0.4 | 0.6 | 0 |
| fidelity | F1_marginal | 0.27 | 0.53 | 0.07 |
| fidelity | F2_increments | 0.56 | 0.56 | 0.56 |
| fidelity | F3_dependence | 0.4 | 0.4 | 0.3 |
| fidelity | F4_seasonality | 0 | 0.67 | 0 |
| fidelity | F5_seams | 0 | 0 | 0 |
| fidelity | F6_windows | 0.29 | 0.57 | 0 |
| fidelity | F7_long_structure | 0.38 | 0.62 | 0 |
| fidelity | F8_target | 0.67 | 0.83 | 0.83 |
| fidelity | F9_coverage | 1 | 1 | 0.5 |
| utility | clf_down_h24_q10 | 0 |  | 0.5 |
| utility | clf_up_h168_q90 | 1 |  | 1 |
| utility | clf_up_h1_q90 | 0 |  | 0 |
| utility | clf_up_h24_q90 | 1 |  | 0.33 |
| utility | clf_up_h24_q95 | 0 |  | 0 |
| utility | clf_up_h24_q99 | 0 |  | 0 |
| utility | clf_up_h6_q90 | 0 |  | 0.5 |
| utility | mc3_h24 | 1 |  | 1 |
| utility | ms_h24 | 1 |  | 1 |
| utility | qreg_h24 | 0.5 |  | 1 |
| utility | reg_h1 | 0.5 |  | 0 |
| utility | reg_h168 | 1 |  | 1 |
| utility | reg_h24 | 1 |  | 1 |
| utility | vol_h24 | 0 |  | 0 |


**redundant_pairs**

| metric_a | metric_b | rho |
|---|---|---|
| F1.2_w1 | F1.6_mean_err | 0.994 |
| F4.1_how_mean | F4.3_hod_mean | 0.976 |
| F8.1_class_tvd | F8.5_cond_event_err | 0.948 |
| F1.2_w1 | F1.5_quantile_err | 0.936 |
| F6.4_mmd | F6.4_mmd_2T | 0.929 |
| F1.5_quantile_err | F1.6_mean_err | 0.924 |
| F9.1_precision | F9.2_density_logdev | 0.905 |
| F11.3_multiclass_tvd | F8.1_class_tvd | 0.903 |


**reference_agreement**

| metric | rho_val_train | rho_val_oot |
|---|---|---|
| F1.10_hill_err | 0.509 | 0.517 |
| F1.1_ks | 0.108 | 0.48 |
| F1.2_w1 | 0.0669 | 0.526 |
| F1.3_ad | 0.0406 | 0.447 |
| F1.4_qq_corr | 0.637 | 0.594 |
| F1.5_q01_err | 0.609 | 0.571 |
| F1.5_q99_err | 0.206 | 0.615 |
| F1.5_quantile_err | 0.0685 | 0.49 |
| F1.6_kurt_err | 0.173 | 0.338 |
| F1.6_mean_err | 0.0724 | 0.564 |
| F1.6_skew_err | 0.682 | 0.636 |
| F1.6_std_err | 0.163 | 0.415 |
| F1.7_out_of_range | 0.131 | 0.416 |
| F1.8_coverage | 0.52 | 0.562 |
| F1.9_js | 0.33 | 0.462 |
| F10.1_dcr_logratio |  |  |
| F10.2_near_copy_share |  |  |
| F11.1_class_share_logratio | 0.681 | 0.608 |
| F11.2_rare_share_logratio | 0.522 | 0.699 |
| F11.3_multiclass_tvd | 0.595 | 0.636 |
| F11.4_minority_lost | 0.775 | 0.775 |
| F12.1_exceed_rate_err | 0.19 | 0.0718 |
| F12.2_exceed_magnitude_err | -0.215 | 0.248 |
| F12.3_spike_rate_err | 0.329 | 0.24 |
| F12.4_block_max_ks | 0.0846 | 0.0511 |
| F12.5_block_min_ks | 0.233 | 0.5 |
| F2.1_ks_d1 | 0.733 | 0.646 |
| F2.1_ks_d168 | 0.858 | 0.725 |
| F2.1_ks_d24 | 0.91 | 0.878 |
| F2.1_ks_d6 | 0.477 | 0.51 |
| F2.1_w1_d24 | 0.864 | 0.81 |
| F2.2_vol_ratio_err_d1 | 0.79 | 0.65 |
| F2.2_vol_ratio_err_d24 | 0.633 | 0.666 |
| F2.3_up_share_err | 0.701 | 0.525 |
| F2.4_big_jump_share_err | 0.686 | 0.683 |
| F3.1_acf_in_window | 0.484 | 0.676 |
| F3.2_acf_beyond_window | 0.387 | 0.661 |
| F3.3_pacf | 0.893 | 0.918 |
| F3.4_acf_abs_d | 0.793 | 0.775 |
| F3.4_acf_sq_d | 0.74 | 0.622 |


### RQ1. Ranking of every method in every slice

| column | p_friedman | nemenyi_cd | n_blocks | n_methods_friedman | best |
|---|---|---|---|---|---|
| ranking:holdout_clf | 0.0226 | 5.03 | 9 | 11 | vae_herding |
| with_cost:holdout_clf | 1.08e-06 | 5.03 | 9 | 11 | vae_rand |
| ranking:holdout_reg | 0.106 | 5.03 | 9 | 11 | timesfm |
| with_cost:holdout_reg | 1.35e-05 | 5.03 | 9 | 11 | timesfm |
| ranking:train_clf | 0.00232 | 5.03 | 9 | 11 | vae_herding |
| with_cost:train_clf | 4.02e-06 | 5.03 | 9 | 11 | vae_herding |
| ranking:train_reg | 0.0158 | 5.03 | 9 | 11 | timesfm |
| with_cost:train_reg | 1.4e-05 | 5.03 | 9 | 11 | timesfm |
| ranking:core_holdout_clf | 0.00379 | 5.03 | 9 | 11 | vae_herding |
| ranking:core_holdout_reg | 0.142 | 5.03 | 9 | 11 | timesfm |
| ranking:core_train_clf | 0.000198 | 5.03 | 9 | 11 | vae_herding |
| ranking:core_train_reg | 0.00149 | 5.03 | 9 | 11 | vae_herding |
| domain:fidelity@train | 0.000198 | 5.03 | 9 | 11 | vae_herding |
| domain:fidelity@val | 0.121 | 5.03 | 9 | 11 | diffusion_ts |
| domain:fidelity@oot | 0.0626 | 5.03 | 9 | 11 | vae_herding |
| domain:fidelity@all | 0.00601 | 5.03 | 9 | 11 | vae_herding |
| domain:utility@val | 0.0907 | 5.03 | 9 | 11 | diffusion_ts |
| domain:utility@oot | 0.207 | 5.03 | 9 | 11 | vae_herding |
| domain:utility@all | 0.154 | 5.03 | 9 | 11 | diffusion_ts |
| cost@generation | 5.36e-15 | 5.03 | 9 | 11 | vae_rand |
| cost@memory | 1.04e-07 | 5.03 | 9 | 11 | chronos |
| cost@total | 5.36e-15 | 5.03 | 9 | 11 | timestral |
| cost@training | 5.36e-15 | 5.03 | 9 | 11 | timestral |
| fidelity:dependence@oot | 0.875 | 5.03 | 9 | 11 | timesfm |
| fidelity:dependence@train | 0.0265 | 5.03 | 9 | 11 | timesfm |
| fidelity:dependence@val | 0.948 | 5.03 | 9 | 11 | timesfm |
| fidelity:distribution@oot | 0.00435 | 5.03 | 9 | 11 | vae_herding |
| fidelity:distribution@train | 3.48e-07 | 5.03 | 9 | 11 | vae_herding |
| fidelity:distribution@val | 0.486 | 5.03 | 9 | 11 | diffusion_ts |
| fidelity:long_structure@oot | 0.00839 | 5.03 | 9 | 11 | vae_herding |
| fidelity:long_structure@train | 5.17e-06 | 5.03 | 9 | 11 | vae_herding |
| fidelity:long_structure@val | 0.205 | 5.03 | 9 | 11 | vae_mbb |
| fidelity:privacy@— | 0.43 | 5.03 | 9 | 11 | vae_knn |
| fidelity:seams@oot | 0.922 | 5.03 | 9 | 11 | chronos |
| fidelity:seams@train | 0.355 | 5.03 | 9 | 11 | chronos |
| fidelity:seams@val | 0.64 | 5.03 | 9 | 11 | diffusion_ts |
| fidelity:target@oot | 0.0105 | 5.03 | 9 | 11 | vae_herding |
| fidelity:target@train | 0.000931 | 5.03 | 9 | 11 | vae_zseries |
| fidelity:target@val | 0.00139 | 5.03 | 9 | 11 | vae_herding |
| fidelity:windows@oot | 0.00893 | 5.03 | 9 | 11 | vae_zseries |

_Showing 40 rows of 56; all of them — `hypotheses/RQ1_global.parquet`._

**ranking_holdout_clf**

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| vae_herding | optimised selection | 5.7 | 5.11 | 6.21 | 0.63 | 0.987 |  | True |
| diffusion_ts | long-series generator | 6.19 | 4.69 | 7.54 | 0.212 | 0.61 | 0.656 | True |
| vae_quilting | optimised selection | 6.22 | 5.66 | 6.83 | 0.12 | 0.744 | 0.656 | True |
| vae_zseries | optimised selection | 6.54 | 5.87 | 7.21 | 0.017 | 0.363 | 0.41 | True |
| vae_rand | random selection | 6.83 | 6.04 | 7.61 | 0.001 | 0.105 | 0.26 | True |
| vae_mbb | optimised selection | 6.9 | 6.12 | 7.62 | 0.002 | 0.048 | 0.26 | True |
| vae_atsp | optimised selection | 6.95 | 6.36 | 7.67 | 0 | 0.006 | 0.176 | True |
| vae_pctsp | optimised selection | 6.96 | 6.45 | 7.5 | 0 | 0 | 0.137 | True |
| vae_knn | optimised selection | 7.14 | 6.58 | 7.7 | 0 | 0 | 0.176 | True |
| vae_greedy | optimised selection | 7.19 | 6.73 | 7.73 | 0 | 0 | 0.107 | True |
| timesfm | long-series generator | 7.57 | 5.74 | 9.41 | 0.009 | 0.091 | 0.656 | True |
| chronos | long-series generator | 7.74 | 6.1 | 9.18 | 0.009 | 0.046 | 0.438 | True |
| timestral | long-series generator | 9.45 | 8.19 | 10.6 | 0 | 0 | 0.0703 | True |


**ranking_holdout_reg**

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| timesfm | long-series generator | 5.32 | 3.83 | 7.08 | 0.696 | 0.931 |  | True |
| diffusion_ts | long-series generator | 5.75 | 4.52 | 6.9 | 0.205 | 0.875 | 0.781 | True |
| vae_herding | optimised selection | 6.3 | 5.33 | 7.24 | 0.034 | 0.543 | 0.781 | True |
| vae_zseries | optimised selection | 6.66 | 5.86 | 7.45 | 0.057 | 0.217 | 0.781 | True |
| chronos | long-series generator | 6.74 | 5.35 | 7.93 | 0.008 | 0.225 | 0.781 | True |
| vae_quilting | optimised selection | 6.89 | 6.39 | 7.47 | 0 | 0.054 | 0.781 | True |
| timestral | long-series generator | 6.9 | 5.74 | 8.01 | 0 | 0.13 | 0.562 | True |
| vae_atsp | optimised selection | 7.45 | 6.87 | 8.13 | 0 | 0.002 | 0.781 | True |
| vae_pctsp | optimised selection | 7.56 | 7.09 | 8.05 | 0 | 0.002 | 0.781 | True |
| vae_mbb | optimised selection | 7.66 | 6.85 | 8.36 | 0 | 0.009 | 0.781 | True |
| vae_knn | optimised selection | 7.71 | 7.08 | 8.3 | 0 | 0 | 0.781 | True |
| vae_rand | random selection | 7.72 | 6.8 | 8.52 | 0 | 0.012 | 0.562 | True |
| vae_greedy | optimised selection | 7.76 | 7.24 | 8.33 | 0 | 0 | 0.781 | True |


**ranking_train_clf**

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| vae_herding | optimised selection | 5.13 | 4.67 | 5.59 | 0.858 | 0.998 |  | True |
| diffusion_ts | long-series generator | 6.04 | 4.48 | 7.43 | 0.128 | 0.623 | 0.219 | True |
| vae_zseries | optimised selection | 6.21 | 5.43 | 7.02 | 0.002 | 0.584 | 0.0977 | True |
| vae_quilting | optimised selection | 6.28 | 5.53 | 7.01 | 0.011 | 0.565 | 0.109 | True |
| vae_rand | random selection | 6.8 | 6.03 | 7.53 | 0 | 0.078 | 0.0352 | False |
| vae_atsp | optimised selection | 6.87 | 6.22 | 7.62 | 0 | 0.022 | 0.0352 | False |
| vae_mbb | optimised selection | 6.88 | 6.09 | 7.58 | 0 | 0.03 | 0.0352 | False |
| vae_pctsp | optimised selection | 6.97 | 6.33 | 7.6 | 0 | 0.002 | 0.0352 | False |
| vae_knn | optimised selection | 7.29 | 6.85 | 7.79 | 0 | 0 | 0.0234 | False |
| vae_greedy | optimised selection | 7.31 | 6.83 | 7.81 | 0 | 0 | 0.0234 | False |
| timesfm | long-series generator | 7.56 | 5.82 | 9.44 | 0.001 | 0.086 | 0.219 | True |
| chronos | long-series generator | 8.09 | 6.48 | 9.5 | 0 | 0.012 | 0.117 | True |
| timestral | long-series generator | 10.1 | 8.72 | 11.2 | 0 | 0 | 0.0234 | False |


**ranking_train_reg**

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| timesfm | long-series generator | 5.31 | 3.89 | 6.85 | 0.56 | 0.898 |  | True |
| diffusion_ts | long-series generator | 5.6 | 4.3 | 6.76 | 0.246 | 0.826 | 0.703 | True |
| vae_herding | optimised selection | 5.74 | 4.99 | 6.51 | 0.12 | 0.903 | 0.703 | True |
| vae_zseries | optimised selection | 6.34 | 5.47 | 7.25 | 0.074 | 0.303 | 0.703 | True |
| vae_quilting | optimised selection | 6.95 | 6.29 | 7.63 | 0 | 0.012 | 0.703 | True |
| chronos | long-series generator | 7.08 | 5.77 | 8.24 | 0 | 0.046 | 0.703 | True |
| vae_atsp | optimised selection | 7.37 | 6.67 | 8.07 | 0 | 0.001 | 0.516 | True |
| timestral | long-series generator | 7.52 | 6.37 | 8.61 | 0 | 0.004 | 0.188 | True |
| vae_pctsp | optimised selection | 7.56 | 6.96 | 8.12 | 0 | 0.001 | 0.703 | True |
| vae_mbb | optimised selection | 7.64 | 6.88 | 8.29 | 0 | 0.002 | 0.703 | True |
| vae_rand | random selection | 7.69 | 6.82 | 8.44 | 0 | 0.004 | 0.516 | True |
| vae_knn | optimised selection | 7.86 | 7.38 | 8.35 | 0 | 0 | 0.703 | True |
| vae_greedy | optimised selection | 7.87 | 7.44 | 8.35 | 0 | 0 | 0.703 | True |


**ranking_core_holdout_clf**

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| vae_herding | optimised selection | 5.35 | 4.6 | 6.04 | 0.815 | 0.993 |  | True |
| vae_quilting | optimised selection | 6.18 | 5.54 | 6.89 | 0.073 | 0.693 | 0.305 | True |
| diffusion_ts | long-series generator | 6.29 | 4.62 | 7.74 | 0.067 | 0.532 | 0.305 | True |
| vae_zseries | optimised selection | 6.32 | 5.54 | 7.15 | 0.039 | 0.521 | 0.305 | True |
| vae_rand | random selection | 6.78 | 5.89 | 7.64 | 0.004 | 0.128 | 0.244 | True |
| vae_mbb | optimised selection | 6.84 | 5.97 | 7.67 | 0 | 0.061 | 0.244 | True |
| vae_atsp | optimised selection | 6.93 | 6.37 | 7.61 | 0 | 0.002 | 0.137 | True |
| vae_pctsp | optimised selection | 7.06 | 6.47 | 7.63 | 0 | 0 | 0.0645 | True |
| vae_knn | optimised selection | 7.18 | 6.57 | 7.81 | 0 | 0 | 0.0977 | True |
| vae_greedy | optimised selection | 7.19 | 6.68 | 7.8 | 0 | 0 | 0.0977 | True |
| timesfm | long-series generator | 7.76 | 6.1 | 9.54 | 0 | 0.052 | 0.125 | True |
| chronos | long-series generator | 8.12 | 6.5 | 9.6 | 0.002 | 0.018 | 0.141 | True |
| timestral | long-series generator | 9.5 | 8.26 | 10.6 | 0 | 0 | 0.0234 | False |


**ranking_core_holdout_reg**

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| timesfm | long-series generator | 5.51 | 4.12 | 7.19 | 0.567 | 0.898 |  | True |
| diffusion_ts | long-series generator | 5.85 | 4.39 | 7.19 | 0.183 | 0.762 | 0.781 | True |
| vae_herding | optimised selection | 5.95 | 4.82 | 7.08 | 0.132 | 0.751 | 0.781 | True |
| vae_zseries | optimised selection | 6.45 | 5.58 | 7.4 | 0.108 | 0.321 | 0.781 | True |
| vae_quilting | optimised selection | 6.85 | 6.26 | 7.53 | 0.001 | 0.068 | 0.781 | True |
| timestral | long-series generator | 6.95 | 5.81 | 8.05 | 0 | 0.092 | 0.562 | True |
| chronos | long-series generator | 7.12 | 5.78 | 8.34 | 0.007 | 0.068 | 0.781 | True |
| vae_atsp | optimised selection | 7.42 | 6.87 | 8.07 | 0 | 0.003 | 0.781 | True |
| vae_mbb | optimised selection | 7.6 | 6.67 | 8.39 | 0 | 0.012 | 0.562 | True |
| vae_pctsp | optimised selection | 7.65 | 7.08 | 8.17 | 0 | 0.001 | 0.781 | True |
| vae_rand | random selection | 7.67 | 6.63 | 8.58 | 0.002 | 0.022 | 0.781 | True |
| vae_knn | optimised selection | 7.75 | 7.08 | 8.37 | 0 | 0.001 | 0.781 | True |
| vae_greedy | optimised selection | 7.76 | 7.15 | 8.39 | 0 | 0.001 | 0.781 | True |


**ranking_core_train_clf**

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| vae_herding | optimised selection | 4.37 | 3.93 | 4.78 | 0.985 | 1 |  | True |
| vae_zseries | optimised selection | 5.95 | 5.05 | 6.89 | 0.002 | 0.755 | 0.0625 | True |
| diffusion_ts | long-series generator | 6.24 | 4.47 | 7.81 | 0.013 | 0.498 | 0.0625 | True |
| vae_quilting | optimised selection | 6.42 | 5.59 | 7.29 | 0 | 0.362 | 0.0625 | True |
| vae_rand | random selection | 6.6 | 5.78 | 7.45 | 0 | 0.165 | 0.0273 | False |
| vae_atsp | optimised selection | 6.66 | 5.92 | 7.44 | 0 | 0.125 | 0.0234 | False |
| vae_mbb | optimised selection | 6.7 | 5.93 | 7.46 | 0 | 0.039 | 0.0273 | False |
| vae_pctsp | optimised selection | 6.94 | 6.25 | 7.61 | 0 | 0.001 | 0.0234 | False |
| vae_greedy | optimised selection | 7.32 | 6.82 | 7.84 | 0 | 0 | 0.0234 | False |
| vae_knn | optimised selection | 7.41 | 6.9 | 7.98 | 0 | 0 | 0.0234 | False |
| timesfm | long-series generator | 7.7 | 6.07 | 9.52 | 0 | 0.054 | 0.0625 | True |
| chronos | long-series generator | 8.76 | 7.17 | 10.2 | 0 | 0.001 | 0.0391 | False |
| timestral | long-series generator | 10.6 | 9.21 | 11.6 | 0 | 0 | 0.0234 | False |


**ranking_core_train_reg**

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| vae_herding | optimised selection | 4.98 | 4.22 | 5.69 | 0.631 | 1 |  | True |
| timesfm | long-series generator | 5.44 | 4.16 | 6.89 | 0.246 | 0.849 | 0.422 | True |
| diffusion_ts | long-series generator | 5.8 | 4.26 | 7.21 | 0.054 | 0.656 | 0.305 | True |
| vae_zseries | optimised selection | 6.07 | 5.08 | 7.16 | 0.069 | 0.452 | 0.305 | True |
| vae_quilting | optimised selection | 7.1 | 6.35 | 7.85 | 0 | 0.013 | 0.0352 | False |
| vae_atsp | optimised selection | 7.15 | 6.34 | 7.9 | 0 | 0.013 | 0.0488 | False |
| vae_mbb | optimised selection | 7.46 | 6.64 | 8.19 | 0 | 0.003 | 0.0352 | False |
| vae_rand | random selection | 7.49 | 6.46 | 8.43 | 0 | 0.01 | 0.0352 | False |
| vae_pctsp | optimised selection | 7.53 | 6.91 | 8.12 | 0 | 0 | 0.0234 | False |
| chronos | long-series generator | 7.75 | 6.54 | 8.93 | 0 | 0.004 | 0.0625 | True |
| vae_greedy | optimised selection | 7.88 | 7.47 | 8.33 | 0 | 0 | 0.0234 | False |
| vae_knn | optimised selection | 7.97 | 7.46 | 8.53 | 0 | 0 | 0.0234 | False |
| timestral | long-series generator | 8.01 | 6.88 | 8.97 | 0 | 0 | 0.0352 | False |


**rankings**

| family | holdout_clf:rank | holdout_clf:p_first | holdout_clf:tier | holdout_reg:rank | holdout_reg:p_first | holdout_reg:tier | train_clf:rank | train_clf:p_first | train_clf:tier | train_reg:rank | train_reg:p_first | train_reg:tier | first_in |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| long-series generator | 7.74 | 0.009 | True | 6.74 | 0.008 | True | 8.09 | 0 | True | 7.08 | 0 | True |  |
| long-series generator | 6.19 | 0.212 | True | 5.75 | 0.205 | True | 6.04 | 0.128 | True | 5.6 | 0.246 | True |  |
| long-series generator | 7.57 | 0.009 | True | 5.32 | 0.696 | True | 7.56 | 0.001 | True | 5.31 | 0.56 | True | holdout_reg, train_reg |
| long-series generator | 9.45 | 0 | True | 6.9 | 0 | True | 10.1 | 0 | False | 7.52 | 0 | True |  |
| optimised selection | 6.95 | 0 | True | 7.45 | 0 | True | 6.87 | 0 | False | 7.37 | 0 | True |  |
| optimised selection | 7.19 | 0 | True | 7.76 | 0 | True | 7.31 | 0 | False | 7.87 | 0 | True |  |
| optimised selection | 5.7 | 0.63 | True | 6.3 | 0.034 | True | 5.13 | 0.858 | True | 5.74 | 0.12 | True | holdout_clf, train_clf |
| optimised selection | 7.14 | 0 | True | 7.71 | 0 | True | 7.29 | 0 | False | 7.86 | 0 | True |  |
| optimised selection | 6.9 | 0.002 | True | 7.66 | 0 | True | 6.88 | 0 | False | 7.64 | 0 | True |  |
| optimised selection | 6.96 | 0 | True | 7.56 | 0 | True | 6.97 | 0 | False | 7.56 | 0 | True |  |
| optimised selection | 6.22 | 0.12 | True | 6.89 | 0 | True | 6.28 | 0.011 | True | 6.95 | 0 | True |  |
| optimised selection | 6.54 | 0.017 | True | 6.66 | 0.057 | True | 6.21 | 0.002 | True | 6.34 | 0.074 | True |  |
| random selection | 6.83 | 0.001 | True | 7.72 | 0 | True | 6.8 | 0 | False | 7.69 | 0 | True |  |


**rankings_core**

| family | core_holdout_clf:rank | core_holdout_clf:p_first | core_holdout_clf:tier | core_holdout_reg:rank | core_holdout_reg:p_first | core_holdout_reg:tier | core_train_clf:rank | core_train_clf:p_first | core_train_clf:tier | core_train_reg:rank | core_train_reg:p_first | core_train_reg:tier | first_in |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| long-series generator | 8.12 | 0.002 | True | 7.12 | 0.007 | True | 8.76 | 0 | False | 7.75 | 0 | True |  |
| long-series generator | 6.29 | 0.067 | True | 5.85 | 0.183 | True | 6.24 | 0.013 | True | 5.8 | 0.054 | True |  |
| long-series generator | 7.76 | 0 | True | 5.51 | 0.567 | True | 7.7 | 0 | True | 5.44 | 0.246 | True | core_holdout_reg |
| long-series generator | 9.5 | 0 | False | 6.95 | 0 | True | 10.6 | 0 | False | 8.01 | 0 | False |  |
| optimised selection | 6.93 | 0 | True | 7.42 | 0 | True | 6.66 | 0 | False | 7.15 | 0 | False |  |
| optimised selection | 7.19 | 0 | True | 7.76 | 0 | True | 7.32 | 0 | False | 7.88 | 0 | False |  |
| optimised selection | 5.35 | 0.815 | True | 5.95 | 0.132 | True | 4.37 | 0.985 | True | 4.98 | 0.631 | True | core_holdout_clf, core_train_clf, core_train_reg |
| optimised selection | 7.18 | 0 | True | 7.75 | 0 | True | 7.41 | 0 | False | 7.97 | 0 | False |  |
| optimised selection | 6.84 | 0 | True | 7.6 | 0 | True | 6.7 | 0 | False | 7.46 | 0 | False |  |
| optimised selection | 7.06 | 0 | True | 7.65 | 0 | True | 6.94 | 0 | False | 7.53 | 0 | False |  |
| optimised selection | 6.18 | 0.073 | True | 6.85 | 0.001 | True | 6.42 | 0 | True | 7.1 | 0 | False |  |
| optimised selection | 6.32 | 0.039 | True | 6.45 | 0.108 | True | 5.95 | 0.002 | True | 6.07 | 0.069 | True |  |
| random selection | 6.78 | 0.004 | True | 7.67 | 0.002 | True | 6.6 | 0 | False | 7.49 | 0 | False |  |


**normalized_scores**

| method | fidelity | utility | dependence | distribution | long_structure | target | windows | classification | regression |
|---|---|---|---|---|---|---|---|---|---|
| chronos | -0.672 | 0.157 | 0.181 | -0.631 | 0.141 | -0.712 | -0.33 | -0.2 | 0.605 |
| diffusion_ts | 0.55 | 0.305 | 0.0205 | 0.979 | 0.595 | -1.06 | -0.236 | 0.113 | 0.413 |
| timesfm | 0.05 | 0.608 | -0.0522 | 0.351 | 0.25 | -2.96 | -0.521 | 0.393 | 0.827 |
| timestral | -0 | 0.072 | -0.313 | 0.664 | 0.0975 | -8.46 | 0.282 | -1.02 | 0.686 |
| vae_atsp | -0 | 0.0618 | -0.258 | -0.14 | 0.0223 | 0.108 | 0.187 | -0.0202 | 0.138 |
| vae_greedy | 0.0996 | 0.0802 | -0.637 | -0.0325 | 0.326 | 0.116 | -0.0289 | 0.0575 | 0.0723 |
| vae_herding | 0.608 | 0.147 | 0.0381 | 0.632 | 0.433 | 0.349 | 0.355 | 0.129 | 0.213 |
| vae_knn | 0.114 | 0.091 | -0.151 | 0.0248 | 0.13 | -0.0187 | -0.182 | 0.0971 | 0.096 |
| vae_mbb | 0.0832 | -0.00302 | 0.0373 | 0.111 | 0.149 | 0.0157 | 0.166 | -0.0151 | -0.00783 |
| vae_pctsp | 0.0809 | 0.103 | -0.362 | -0.104 | 0.00459 | -0.395 | 0 | 0.128 | 0.0751 |
| vae_quilting | 0.245 | 0.195 | -0.316 | 0.361 | 0.00791 | 0.0964 | 0.158 | 0.0682 | 0.222 |
| vae_zseries | 0.0653 | 0.097 | -0.221 | -0.197 | 0.0112 | 0.526 | 0.102 | 0.0406 | 0.136 |
| vae_rand | 0 | -0 | -0 | 0 | -0 | -0 | -0 | 0 | -0 |


**anchor_check**

| leaf | kind | criterion | core | n_datasets | ratio_all | separated_all | ratio_even | ratio_odd | separated_even | separated_odd | flip |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F1.10_hill_err | fidelity | fidelity:distribution | False | 9 | 0.611 | False | 0.855 | 0.8 | False | False | False |
| F1.10_hill_err@train | fidelity | fidelity:distribution | False | 9 | 1.46 | True | 1.09 | 1.6 | True | True | False |
| F1.1_ks | fidelity | fidelity:distribution | False | 9 | 7.52 | True | 8.87 | 4.46 | True | True | False |
| F1.1_ks@train | fidelity | fidelity:distribution | False | 9 | 4.36 | True | 7.17 | 2.92 | True | True | False |
| F1.2_w1 | fidelity | fidelity:distribution | True | 9 | 7.14 | True | 8.31 | 4.8 | True | True | False |
| F1.2_w1@train | fidelity | fidelity:distribution | True | 9 | 5.77 | True | 9.44 | 4.38 | True | True | False |
| F1.3_ad | fidelity | fidelity:distribution | False | 9 | 6.43 | True | 7.08 | 5.91 | True | True | False |
| F1.3_ad@train | fidelity | fidelity:distribution | False | 9 | 4.37 | True | 5.08 | 2.99 | True | True | False |
| F1.4_qq_corr | fidelity | fidelity:distribution | False | 9 | 3.26 | True | 3.64 | 2.4 | True | True | False |
| F1.4_qq_corr@train | fidelity | fidelity:distribution | False | 9 | 2.72 | True | 2.36 | 2 | True | True | False |
| F1.5_q01_err | fidelity | fidelity:distribution | False | 9 | 5.72 | True | 5.36 | 4.9 | True | True | False |
| F1.5_q01_err@train | fidelity | fidelity:distribution | False | 9 | 3.81 | True | 3.28 | 2.79 | True | True | False |
| F1.5_q99_err | fidelity | fidelity:distribution | False | 9 | 4.71 | True | 3.55 | 3.6 | True | True | False |
| F1.5_q99_err@train | fidelity | fidelity:distribution | False | 9 | 3.49 | True | 3.06 | 1.83 | True | True | False |
| F1.5_quantile_err | fidelity | fidelity:distribution | False | 9 | 6.8 | True | 6.17 | 4.1 | True | True | False |
| F1.5_quantile_err@train | fidelity | fidelity:distribution | False | 9 | 4.58 | True | 4.02 | 3.76 | True | True | False |
| F1.6_kurt_err | fidelity | fidelity:distribution | False | 9 | 1.65 | True | 1.35 | 2.12 | True | True | False |
| F1.6_kurt_err@train | fidelity | fidelity:distribution | False | 9 | 1.47 | True | 0.741 | 2.41 | False | True | True |
| F1.6_mean_err | fidelity | fidelity:distribution | False | 9 | 8.07 | True | 7.67 | 6.07 | True | True | False |
| F1.6_mean_err@train | fidelity | fidelity:distribution | False | 9 | 5.17 | True | 8.88 | 5.32 | True | True | False |
| F1.6_skew_err | fidelity | fidelity:distribution | False | 9 | 1.79 | True | 3.14 | 2.23 | True | True | False |
| F1.6_skew_err@train | fidelity | fidelity:distribution | False | 9 | 3.66 | True | 5.42 | 3.31 | True | True | False |
| F1.6_std_err | fidelity | fidelity:distribution | False | 9 | 2.46 | True | 1.85 | 3.15 | True | True | False |
| F1.6_std_err@train | fidelity | fidelity:distribution | False | 9 | 2.46 | True | 1.8 | 2.02 | True | True | False |
| F1.7_out_of_range | fidelity | fidelity:distribution | False | 9 | 4.21 | True | 4.38 | 3.65 | True | True | False |
| F1.7_out_of_range@train | fidelity | fidelity:distribution | False | 9 |  | False |  |  | False | False | False |
| F1.8_coverage | fidelity | fidelity:distribution | False | 9 | 3.95 | True | 2.78 | 4.1 | True | True | False |
| F1.8_coverage@train | fidelity | fidelity:distribution | False | 9 | 5.51 | True | 1.37 | 2.1 | True | True | False |
| F1.9_js | fidelity | fidelity:distribution | False | 9 | 5.81 | True | 7.72 | 4.86 | True | True | False |
| F1.9_js@train | fidelity | fidelity:distribution | False | 9 | 6.28 | True | 5.12 | 4.71 | True | True | False |
| F11.1_class_share_logratio | fidelity | fidelity:target | True | 9 | 5.72 | True | 4.38 | 4.76 | True | True | False |
| F11.1_class_share_logratio@train | fidelity | fidelity:target | True | 9 | 7.61 | True | 7.46 | 6.65 | True | True | False |
| F11.2_rare_share_logratio | fidelity | fidelity:target | False | 9 | 3.93 | True | 4.11 | 3.5 | True | True | False |
| F11.2_rare_share_logratio@train | fidelity | fidelity:target | False | 9 | 6.92 | True | 11.3 | 3.34 | True | True | False |
| F11.3_multiclass_tvd | fidelity | fidelity:target | False | 9 | 3.4 | True | 3.22 | 3.09 | True | True | False |
| F11.3_multiclass_tvd@train | fidelity | fidelity:target | False | 9 | 3.2 | True | 2.65 | 3.76 | True | True | False |
| F11.4_minority_lost | fidelity | fidelity:target | False | 9 |  | False |  |  | False | False | False |
| F11.4_minority_lost@train | fidelity | fidelity:target | False | 9 |  | False |  |  | False | False | False |
| F12.1_exceed_rate_err | fidelity | fidelity:distribution | False | 9 | 6 | True | 6 | 3.17 | True | True | False |
| F12.1_exceed_rate_err@train | fidelity | fidelity:distribution | False | 9 | 3.72 | True | 4.26 | 3.68 | True | True | False |


**note**: full ranking by slice — reports/LEADERBOARD.md

### RQ2. Assembly from a window pool vs long-series generators

| comparison | kind | unit | n_datasets | median_z | mean_z | ci_lo | ci_hi | p_better_adj | p_worse_adj | p_equiv_adj | n_better | n_worse | n_same | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| diffusion_ts vs vae_rand | utility | clf_down_h24_q10\|gbdt\|S\|val\|auc | 9 | 0.865 | 1.83 | 0.593 | 3.44 | 0.175 | 1 | 1 | 3 | 0 | 0 | inconclusive |
| diffusion_ts vs vae_rand | utility | reg_h168\|linear\|S\|val\|mase | 9 | 3.9 | 3.65 | 2.56 | 4.73 | 0.175 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| timestral vs vae_rand | utility | ms_h24\|linear\|S\|val\|mase | 9 | 3.07 | 3.61 | 1.9 | 5.7 | 0.175 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| timestral vs vae_rand | utility | reg_h168\|gbdt\|S\|val\|mase | 9 | 2.89 | 3.43 | 2.47 | 4.53 | 0.175 | 1 | 1 | 8 | 0 | 0 | inconclusive |
| timestral vs vae_rand | utility | reg_h168\|linear\|S\|val\|mase | 9 | 4.06 | 4.16 | 2.99 | 5.22 | 0.175 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| timestral vs vae_rand | utility | reg_h24\|gbdt\|S\|val\|mase | 9 | 5.32 | 6.22 | 3.47 | 9.17 | 0.175 | 1 | 1 | 8 | 0 | 0 | inconclusive |
| timestral vs vae_rand | utility | reg_h24\|linear\|S\|val\|mase | 9 | 4.24 | 4.9 | 3.55 | 6.33 | 0.175 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| timestral vs assembly_median | utility | reg_h168\|gbdt\|S\|oot\|mase | 9 | 6.42 | 5.84 | 3.29 | 8.63 | 0.175 | 1 | 1 | 8 | 0 | 0 | inconclusive |
| timestral vs assembly_median | utility | reg_h168\|gbdt\|S\|val\|mase | 9 | 6 | 7.29 | 3.67 | 12 | 0.175 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| timestral vs assembly_median | utility | reg_h168\|linear\|S\|val\|mase | 9 | 6.06 | 6.04 | 3.57 | 8.79 | 0.175 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| timestral vs assembly_median | utility | reg_h24\|linear\|S\|oot\|mase | 9 | 5.68 | 6.7 | 4.18 | 9.91 | 0.175 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| timestral vs assembly_median | utility | reg_h24\|linear\|S\|val\|mase | 9 | 6.7 | 10 | 5.97 | 15.7 | 0.175 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| timestral vs vae_rand | fidelity | F3.8_calendar_corr_err@oot | 9 | 3.09 | 6.05 | 2.3 | 11.4 | 0.175 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| timestral vs vae_rand | fidelity | F6.1_disc_score | 9 | 0.6 | 1.13 | 0.493 | 1.88 | 0.175 | 1 | 1 | 2 | 0 | 0 | inconclusive |
| timestral vs vae_rand | fidelity | F8.4_event_by_how | 9 | 7.79 | 7.27 | 4.19 | 10.7 | 0.175 | 1 | 1 | 8 | 0 | 0 | inconclusive |
| timestral vs assembly_median | fidelity | F3.8_calendar_corr_err | 9 | 4.76 | 6.74 | 2.97 | 11.2 | 0.175 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| timestral vs assembly_median | fidelity | F3.8_calendar_corr_err@oot | 9 | 7.75 | 7.9 | 4.65 | 11.7 | 0.175 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| timestral vs assembly_median | fidelity | F8.4_event_by_how | 9 | 9.63 | 11.4 | 5.8 | 18.4 | 0.175 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| chronos vs vae_rand | utility | clf_up_h1_q90\|linear\|S\|oot\|auc | 7 | -1.06 | -1.79 | -3.4 | -0.554 | 1 | 0.199 | 1 | 0 | 3 | 0 | inconclusive |
| chronos vs assembly_median | utility | clf_up_h1_q90\|linear\|S\|oot\|auc | 7 | -0.892 | -1.71 | -3.23 | -0.581 | 1 | 0.199 | 1 | 0 | 3 | 0 | inconclusive |
| timestral vs vae_rand | utility | clf_up_h168_q90\|gbdt\|S\|val\|auc | 9 | -1.59 | -1.62 | -2.56 | -0.838 | 1 | 0.199 | 1 | 0 | 7 | 0 | inconclusive |
| timestral vs vae_rand | utility | mc3_h24\|gbdt\|S\|oot\|logloss | 9 | -4.14 | -6.94 | -12.1 | -2.5 | 1 | 0.199 | 1 | 1 | 7 | 0 | inconclusive |
| timestral vs vae_rand | utility | mc3_h24\|gbdt\|S\|val\|logloss | 9 | -4.33 | -8.79 | -15.3 | -3.57 | 1 | 0.199 | 1 | 0 | 8 | 0 | inconclusive |
| timestral vs vae_rand | utility | reg_h1\|linear\|S\|oot\|mase | 9 | -8.62 | -21.2 | -39.8 | -6.17 | 1 | 0.199 | 1 | 1 | 7 | 0 | inconclusive |
| timestral vs assembly_median | utility | clf_down_h24_q10\|linear\|S\|val\|auc | 9 | -6.59 | -33.3 | -85.5 | -3.53 | 1 | 0.199 | 1 | 1 | 7 | 0 | inconclusive |
| timestral vs assembly_median | utility | clf_up_h168_q90\|gbdt\|S\|val\|auc | 9 | -2.83 | -4.8 | -9.56 | -2.04 | 1 | 0.199 | 1 | 0 | 8 | 0 | inconclusive |
| timestral vs assembly_median | utility | clf_up_h24_q99\|gbdt\|S\|oot\|auc | 9 | -3.27 | -3.02 | -4.83 | -1.24 | 1 | 0.199 | 1 | 1 | 7 | 0 | inconclusive |
| timestral vs assembly_median | utility | clf_up_h24_q99\|linear\|S\|oot\|auc | 9 | -2.95 | -18.3 | -43.5 | -1.28 | 1 | 0.199 | 1 | 2 | 7 | 0 | inconclusive |
| timestral vs assembly_median | utility | mc3_h24\|gbdt\|S\|val\|logloss | 9 | -6.12 | -18.8 | -34.9 | -6.99 | 1 | 0.199 | 1 | 0 | 8 | 0 | inconclusive |
| timestral vs assembly_median | utility | mc3_h24\|linear\|S\|val\|logloss | 9 | -9.32 | -9.04 | -14.5 | -3.87 | 1 | 0.199 | 1 | 1 | 7 | 0 | inconclusive |
| chronos vs vae_rand | fidelity | F1.2_w1@oot | 7 | -1.37 | -4.56 | -14.3 | -0.79 | 1 | 0.199 | 1 | 0 | 3 | 0 | inconclusive |
| chronos vs vae_rand | fidelity | F1.5_quantile_err@oot | 7 | -2.02 | -9.32 | -32.8 | -0.885 | 1 | 0.199 | 1 | 0 | 4 | 0 | inconclusive |
| chronos vs vae_rand | fidelity | F1.6_kurt_err@oot | 7 | -0.942 | -1.59 | -3.64 | -0.344 | 1 | 0.199 | 1 | 0 | 2 | 0 | inconclusive |
| chronos vs vae_rand | fidelity | F1.6_mean_err@oot | 7 | -1.37 | -4.14 | -12.8 | -0.752 | 1 | 0.199 | 1 | 0 | 2 | 0 | inconclusive |
| chronos vs vae_rand | fidelity | F1.6_skew_err@oot | 7 | -0.588 | -0.53 | -0.963 | -0.125 | 1 | 0.199 | 1 | 0 | 1 | 0 | inconclusive |
| chronos vs vae_rand | fidelity | F1.6_std_err@oot | 7 | -1.21 | -0.984 | -1.61 | -0.377 | 1 | 0.199 | 1 | 0 | 4 | 0 | inconclusive |
| chronos vs vae_rand | fidelity | F1.7_out_of_range@oot | 7 | -1.71 | -10.7 | -31 | -1.14 | 1 | 0.199 | 1 | 0 | 4 | 0 | inconclusive |
| chronos vs vae_rand | fidelity | F2.4_big_jump_share_err | 7 | -4.58 | -7 | -18.8 | -1.97 | 1 | 0.199 | 1 | 0 | 6 | 0 | inconclusive |
| chronos vs vae_rand | fidelity | F2.4_big_jump_share_err@oot | 7 | -1.56 | -6.8 | -21.7 | -1.09 | 1 | 0.199 | 1 | 0 | 4 | 0 | inconclusive |
| chronos vs vae_rand | fidelity | F6.1_disc_score@oot | 7 | -1.26 | -1.66 | -2.81 | -0.758 | 1 | 0.199 | 1 | 0 | 2 | 0 | inconclusive |

_Showing 40 rows of 1612 (rows with a better / worse / same verdict first); all of them — `hypotheses/RQ2_global.parquet`._

### RQ3. Within assembly: window selection × seam processing

| comparison | kind | unit | n_datasets | median_z | mean_z | ci_lo | ci_hi | p_better_adj | p_worse_adj | p_equiv_adj | n_better | n_worse | n_same | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| seams: vae_zseries_quilt vs vae_zseries | fidelity | F4.1_how_mean@oot | 9 | -0.261 | -0.312 | -0.608 | -0.107 | 1 | 0.0588 | 0.0226 | 0 | 0 | 6 | same |
| seams: vae_zseries_xfade vs vae_zseries | fidelity | F1.6_std_err@oot | 9 | -0.241 | -0.321 | -0.542 | -0.105 | 1 | 0.0588 | 0.0226 | 0 | 0 | 6 | same |
| seams: vae_zseries_xfade vs vae_zseries | fidelity | F4.1_how_mean@oot | 9 | -0.34 | -0.442 | -0.737 | -0.198 | 1 | 0.0588 | 0.0262 | 0 | 0 | 6 | same |
| main effect: seams crossfade vs none | fidelity | F1.6_std_err@oot | 9 | -0.241 | -0.321 | -0.542 | -0.105 | 1 | 0.0588 | 0.0226 | 0 | 0 | 6 | same |
| main effect: seams crossfade vs none | fidelity | F4.1_how_mean@oot | 9 | -0.34 | -0.442 | -0.737 | -0.198 | 1 | 0.0588 | 0.0262 | 0 | 0 | 6 | same |
| main effect: seams quilt vs none | fidelity | F4.1_how_mean@oot | 9 | -0.261 | -0.312 | -0.608 | -0.107 | 1 | 0.0588 | 0.0226 | 0 | 0 | 6 | same |
| selection: vae_mbb vs vae_rand | fidelity | F2.4_big_jump_share_err | 9 | -0.45 | -0.482 | -0.779 | -0.167 | 1 | 0.08 | 0.0226 | 0 | 0 | 0 | same |
| seams: vae_zseries_xfade vs vae_zseries | fidelity | F4.3_hod_mean@oot | 9 | -0.347 | -0.343 | -0.58 | -0.148 | 1 | 0.08 | 0.0226 | 0 | 0 | 6 | same |
| main effect: seams crossfade vs none | fidelity | F4.3_hod_mean@oot | 9 | -0.347 | -0.343 | -0.58 | -0.148 | 1 | 0.08 | 0.0226 | 0 | 0 | 6 | same |
| seams: vae_zseries_wsola vs vae_zseries | fidelity | F11.3_multiclass_tvd | 9 | -0.262 | -0.293 | -0.607 | -0.0249 | 1 | 0.0936 | 0.0226 | 0 | 0 | 4 | same |
| main effect: seams wsola vs none | fidelity | F11.3_multiclass_tvd | 9 | -0.262 | -0.293 | -0.607 | -0.0249 | 1 | 0.0936 | 0.0226 | 0 | 0 | 4 | same |
| selection: vae_mbb vs vae_rand | fidelity | F2.4_big_jump_share_err@oot | 9 | -0.357 | -0.342 | -0.867 | 0.231 | 1 | 0.11 | 0.0262 | 0 | 0 | 1 | same |
| selection: vae_mbb vs vae_rand | fidelity | F3.3_pacf | 9 | -0.394 | -0.404 | -1.03 | 0.0795 | 1 | 0.11 | 0.0262 | 0 | 0 | 1 | same |
| selection: vae_mbb vs vae_rand | fidelity | F8.4_event_by_how@oot | 9 | -0.208 | -0.323 | -0.672 | 0.011 | 1 | 0.11 | 0.0262 | 0 | 0 | 0 | same |
| seams: vae_zseries_quilt vs vae_zseries | fidelity | F1.9_js@oot | 9 | -0.474 | -0.428 | -0.772 | -0.154 | 1 | 0.11 | 0.0262 | 0 | 0 | 3 | same |
| seams: vae_zseries_quilt vs vae_zseries | fidelity | F2.4_big_jump_share_err@oot | 9 | -0.233 | -0.35 | -0.712 | 0.0139 | 1 | 0.11 | 0.0468 | 0 | 1 | 3 | same |
| seams: vae_zseries_wsola vs vae_zseries | fidelity | F12.3_spike_rate_err | 8 | -0.346 | -0.424 | -0.907 | -0.041 | 1 | 0.11 | 0.0425 | 0 | 0 | 1 | same |
| main effect: seams quilt vs none | fidelity | F1.9_js@oot | 9 | -0.474 | -0.428 | -0.772 | -0.154 | 1 | 0.11 | 0.0262 | 0 | 0 | 3 | same |
| main effect: seams quilt vs none | fidelity | F2.4_big_jump_share_err@oot | 9 | -0.233 | -0.35 | -0.712 | 0.0139 | 1 | 0.11 | 0.0468 | 0 | 1 | 3 | same |
| main effect: seams wsola vs none | fidelity | F12.3_spike_rate_err | 8 | -0.346 | -0.424 | -0.907 | -0.041 | 1 | 0.11 | 0.0425 | 0 | 0 | 1 | same |
| seams: vae_zseries_wsola vs vae_zseries | fidelity | F8.1_class_tvd | 9 | -0.415 | -0.287 | -0.561 | 0.00605 | 1 | 0.132 | 0.0226 | 0 | 0 | 3 | same |
| main effect: seams wsola vs none | fidelity | F8.1_class_tvd | 9 | -0.415 | -0.287 | -0.561 | 0.00605 | 1 | 0.132 | 0.0226 | 0 | 0 | 3 | same |
| seams: vae_zseries_xfade vs vae_zseries | fidelity | F1.10_hill_err | 9 | -0.179 | -0.281 | -0.585 | -0.0372 | 1 | 0.156 | 0.0262 | 0 | 0 | 6 | same |
| seams: vae_zseries_xfade vs vae_zseries | fidelity | F1.1_ks | 9 | -0.22 | -0.234 | -0.483 | 0.00211 | 1 | 0.156 | 0.0226 | 0 | 0 | 5 | same |
| main effect: seams crossfade vs none | fidelity | F1.10_hill_err | 9 | -0.179 | -0.281 | -0.585 | -0.0372 | 1 | 0.156 | 0.0262 | 0 | 0 | 6 | same |
| main effect: seams crossfade vs none | fidelity | F1.1_ks | 9 | -0.22 | -0.234 | -0.483 | 0.00211 | 1 | 0.156 | 0.0226 | 0 | 0 | 5 | same |
| seams: vae_zseries_quilt vs vae_zseries | fidelity | F1.10_hill_err | 9 | -0.249 | -0.24 | -0.465 | -0.0383 | 1 | 0.19 | 0.0226 | 0 | 0 | 6 | same |
| seams: vae_zseries_quilt vs vae_zseries | fidelity | F1.10_hill_err@oot | 9 | -0.462 | -0.308 | -0.577 | -0.0457 | 1 | 0.19 | 0.0226 | 0 | 0 | 2 | same |
| seams: vae_zseries_wsola vs vae_zseries | fidelity | F1.10_hill_err | 9 | -0.216 | -0.257 | -0.536 | -0.0198 | 1 | 0.19 | 0.0226 | 0 | 0 | 5 | same |
| main effect: seams quilt vs none | fidelity | F1.10_hill_err | 9 | -0.249 | -0.24 | -0.465 | -0.0383 | 1 | 0.19 | 0.0226 | 0 | 0 | 6 | same |
| main effect: seams quilt vs none | fidelity | F1.10_hill_err@oot | 9 | -0.462 | -0.308 | -0.577 | -0.0457 | 1 | 0.19 | 0.0226 | 0 | 0 | 2 | same |
| main effect: seams wsola vs none | fidelity | F1.10_hill_err | 9 | -0.216 | -0.257 | -0.536 | -0.0198 | 1 | 0.19 | 0.0226 | 0 | 0 | 5 | same |
| seams: vae_zseries_quilt vs vae_zseries | fidelity | F4.3_hod_mean@oot | 9 | -0.228 | -0.209 | -0.457 | 0.0044 | 1 | 0.227 | 0.0226 | 0 | 0 | 6 | same |
| seams: vae_zseries_xfade vs vae_zseries | fidelity | F1.5_q99_err | 9 | -0.121 | -0.166 | -0.424 | 0.0561 | 1 | 0.227 | 0.0226 | 0 | 0 | 6 | same |
| seams: vae_zseries_xfade vs vae_zseries | fidelity | F4.1_how_mean | 9 | -0.288 | -0.287 | -0.576 | -0.017 | 1 | 0.227 | 0.0226 | 0 | 0 | 6 | same |
| main effect: seams crossfade vs none | fidelity | F1.5_q99_err | 9 | -0.121 | -0.166 | -0.424 | 0.0561 | 1 | 0.227 | 0.0226 | 0 | 0 | 6 | same |
| main effect: seams crossfade vs none | fidelity | F4.1_how_mean | 9 | -0.288 | -0.287 | -0.576 | -0.017 | 1 | 0.227 | 0.0226 | 0 | 0 | 6 | same |
| main effect: seams quilt vs none | fidelity | F4.3_hod_mean@oot | 9 | -0.228 | -0.209 | -0.457 | 0.0044 | 1 | 0.227 | 0.0226 | 0 | 0 | 6 | same |
| seams: vae_zseries_xfade vs vae_zseries | fidelity | F7.4_excursion_ks@oot | 8 | -0.368 | -0.4 | -0.771 | -0.0247 | 1 | 0.233 | 0.0262 | 0 | 0 | 2 | same |
| main effect: seams crossfade vs none | fidelity | F7.4_excursion_ks@oot | 8 | -0.368 | -0.4 | -0.771 | -0.0247 | 1 | 0.233 | 0.0262 | 0 | 0 | 2 | same |

_Showing 40 rows of 2828 (rows with a better / worse / same verdict first); all of them — `hypotheses/RQ3_global.parquet`._

**grid**

| assembler | joiner | method |
|---|---|---|
| atsp | none | vae_atsp |
| greedy | none | vae_greedy |
| herding | none | vae_herding |
| knn | none | vae_knn |
| mbb | none | vae_mbb |
| pctsp | none | vae_pctsp |
| quilt_sel | quilt | vae_quilting |
| random | none | vae_rand |
| zseries | crossfade | vae_zseries_xfade |
| zseries | quilt | vae_zseries_quilt |
| zseries | wsola | vae_zseries_wsola |
| zseries | none | vae_zseries |


### RQ4. Does fidelity predict utility (which metrics, against which reference)

| unit | metric | reference | group | criterion | n_datasets | median_rho | share_positive | p_two_sided | p_bh | predictive |
|---|---|---|---|---|---|---|---|---|---|---|
| F3.1_acf_in_window@train | F3.1_acf_in_window | train | F3_dependence | regression@val | 9 | 0.809 | 0.667 | 0.0547 | 0.167 | False |
| F3.2_acf_beyond_window@train | F3.2_acf_beyond_window | train | F3_dependence | regression@val | 9 | 0.779 | 0.667 | 0.0977 | 0.231 | False |
| F3.1_acf_in_window@oot | F3.1_acf_in_window | oot | F3_dependence | regression@oot | 9 | 0.732 | 1 | 0.00391 | 0.0501 | False |
| F3.1_acf_in_window | F3.1_acf_in_window | val | F3_dependence | regression@oot | 9 | 0.712 | 0.778 | 0.0391 | 0.135 | False |
| F6.6_feature_fid@oot | F6.6_feature_fid | oot | F6_windows | regression@oot | 9 | 0.697 | 0.889 | 0.0195 | 0.0892 | False |
| F3.2_acf_beyond_window@oot | F3.2_acf_beyond_window | oot | F3_dependence | classification@oot | 9 | 0.684 | 0.889 | 0.0273 | 0.108 | False |
| F8.4_event_by_how | F8.4_event_by_how | val | F8_target | regression@val | 9 | 0.668 | 0.889 | 0.0117 | 0.0695 | False |
| F3.2_acf_beyond_window@oot | F3.2_acf_beyond_window | oot | F3_dependence | regression@oot | 9 | 0.665 | 0.889 | 0.0273 | 0.108 | False |
| F2.1_ks_d168@oot | F2.1_ks_d168 | oot | F2_increments | classification@oot | 9 | 0.64 | 0.778 | 0.0195 | 0.0892 | False |
| F8.6_cond_future_ks@oot | F8.6_cond_future_ks | oot | F8_target | classification@val | 9 | 0.638 | 1 | 0.00391 | 0.0501 | False |
| F6.6_feature_fid@train | F6.6_feature_fid | train | F6_windows | regression@oot | 9 | 0.626 | 0.667 | 0.0977 | 0.231 | False |
| F8.6_cond_future_ks@oot | F8.6_cond_future_ks | oot | F8_target | regression@oot | 9 | 0.626 | 0.889 | 0.00781 | 0.0587 | False |
| F6.6_feature_fid | F6.6_feature_fid | val | F6_windows | regression@oot | 9 | 0.626 | 0.778 | 0.0508 | 0.167 | False |
| F8.4_event_by_how@train | F8.4_event_by_how | train | F8_target | regression@oot | 9 | 0.623 | 0.889 | 0.00781 | 0.0587 | False |
| F8.4_event_by_how@oot | F8.4_event_by_how | oot | F8_target | regression@oot | 9 | 0.623 | 0.778 | 0.0273 | 0.108 | False |
| F3.1_acf_in_window | F3.1_acf_in_window | val | F3_dependence | classification@val | 9 | 0.62 | 0.778 | 0.0742 | 0.2 | False |
| F1.9_js | F1.9_js | val | F1_marginal | classification@val | 9 | 0.618 | 0.667 | 0.0977 | 0.231 | False |
| F3.4_acf_sq_d | F3.4_acf_sq_d | val | F3_dependence | classification@val | 9 | 0.609 | 0.778 | 0.0977 | 0.231 | False |
| F3.2_acf_beyond_window@oot | F3.2_acf_beyond_window | oot | F3_dependence | classification@val | 9 | 0.604 | 0.778 | 0.0547 | 0.167 | False |
| F3.2_acf_beyond_window | F3.2_acf_beyond_window | val | F3_dependence | classification@val | 9 | 0.604 | 1 | 0.00391 | 0.0501 | False |
| F2.2_vol_ratio_err_d24@oot | F2.2_vol_ratio_err_d24 | oot | F2_increments | classification@oot | 9 | 0.586 | 0.889 | 0.00781 | 0.0587 | False |
| F8.5_cond_event_err | F8.5_cond_event_err | val | F8_target | regression@val | 9 | 0.585 | 0.778 | 0.0742 | 0.2 | False |
| F8.6_cond_future_ks@oot | F8.6_cond_future_ks | oot | F8_target | classification@oot | 9 | 0.582 | 0.889 | 0.00781 | 0.0587 | False |
| F3.8_calendar_corr_err@oot | F3.8_calendar_corr_err | oot | F3_dependence | regression@val | 9 | 0.582 | 0.778 | 0.0195 | 0.0892 | False |
| F1.9_js@oot | F1.9_js | oot | F1_marginal | classification@val | 9 | 0.582 | 0.889 | 0.0273 | 0.108 | False |
| F3.1_acf_in_window@oot | F3.1_acf_in_window | oot | F3_dependence | regression@val | 9 | 0.579 | 0.667 | 0.203 | 0.377 | False |
| F2.1_ks_d168@train | F2.1_ks_d168 | train | F2_increments | classification@oot | 9 | 0.578 | 0.778 | 0.0391 | 0.135 | False |
| F3.1_acf_in_window@train | F3.1_acf_in_window | train | F3_dependence | regression@oot | 9 | 0.576 | 0.778 | 0.0391 | 0.135 | False |
| F3.1_acf_in_window | F3.1_acf_in_window | val | F3_dependence | classification@oot | 9 | 0.572 | 0.889 | 0.0156 | 0.0892 | False |
| F3.4_acf_sq_d@oot | F3.4_acf_sq_d | oot | F3_dependence | classification@val | 9 | 0.562 | 1 | 0.00391 | 0.0501 | False |
| F3.8_calendar_corr_err@train | F3.8_calendar_corr_err | train | F3_dependence | regression@val | 9 | 0.561 | 0.778 | 0.0195 | 0.0892 | False |
| F11.2_rare_share_logratio@train | F11.2_rare_share_logratio | train | F11_class_balance | classification@val | 9 | 0.559 | 1 | 0.00391 | 0.0501 | False |
| F8.6_cond_future_ks | F8.6_cond_future_ks | val | F8_target | classification@oot | 9 | 0.553 | 0.889 | 0.0117 | 0.0695 | False |
| F8.6_cond_future_ks | F8.6_cond_future_ks | val | F8_target | classification@val | 9 | 0.552 | 0.667 | 0.0547 | 0.167 | False |
| F2.1_w1_d24@train | F2.1_w1_d24 | train | F2_increments | regression@oot | 9 | 0.55 | 0.889 | 0.00781 | 0.0587 | False |
| F2.1_w1_d24 | F2.1_w1_d24 | val | F2_increments | regression@oot | 9 | 0.547 | 0.889 | 0.00781 | 0.0587 | False |
| F8.6_cond_future_ks@train | F8.6_cond_future_ks | train | F8_target | regression@oot | 9 | 0.544 | 0.889 | 0.0117 | 0.0695 | False |
| F8.6_cond_future_ks@train | F8.6_cond_future_ks | train | F8_target | classification@val | 9 | 0.544 | 1 | 0.00391 | 0.0501 | False |
| F2.1_w1_d24@oot | F2.1_w1_d24 | oot | F2_increments | regression@oot | 9 | 0.544 | 0.889 | 0.0117 | 0.0695 | False |
| F3.4_acf_sq_d | F3.4_acf_sq_d | val | F3_dependence | classification@oot | 9 | 0.539 | 0.889 | 0.00781 | 0.0587 | False |

_Showing 40 rows of 872; all of them — `hypotheses/RQ4_global.parquet`._

**by_reference**

| criterion | reference | median_rho | share_predictive |
|---|---|---|---|
| classification@oot | oot | 0.321 | 0 |
| classification@oot | train | 0.285 | 0 |
| classification@oot | val | 0.195 | 0 |
| classification@val | oot | 0.321 | 0 |
| classification@val | train | 0.287 | 0 |
| classification@val | val | 0.277 | 0 |
| regression@oot | oot | 0.254 | 0 |
| regression@oot | train | 0.187 | 0 |
| regression@oot | val | 0.239 | 0 |
| regression@val | oot | -0.022 | 0 |
| regression@val | train | -0.024 | 0 |
| regression@val | val | 0.125 | 0 |


**by_group**

| group | reference | classification@oot | classification@val | regression@oot | regression@val |
|---|---|---|---|---|---|
| F10_memorisation | val | -0.068 | 0.038 | -0.125 | -0.313 |
| F11_class_balance | oot | 0.5 | 0.421 | 0.16 | -0.094 |
| F11_class_balance | train | 0.451 | 0.437 | 0.081 | -0.205 |
| F11_class_balance | val | 0.307 | 0.317 | 0.271 | -0.033 |
| F12_extremes | oot | 0.2 | 0.074 | -0.069 | -0.17 |
| F12_extremes | train | 0.124 | 0.168 | -0.035 | -0.132 |
| F12_extremes | val | 0.007 | 0.077 | 0.179 | 0.1 |
| F1_marginal | oot | 0.196 | 0.226 | 0.253 | 0.021 |
| F1_marginal | train | 0.186 | 0.121 | 0.065 | -0.071 |
| F1_marginal | val | 0.13 | 0.248 | 0.207 | 0.254 |
| F2_increments | oot | 0.472 | 0.276 | 0.347 | -0.035 |
| F2_increments | train | 0.385 | 0.316 | 0.171 | -0.006 |
| F2_increments | val | 0.274 | 0.311 | 0.186 | 0.065 |
| F3_dependence | oot | 0.438 | 0.364 | 0.266 | -0.11 |
| F3_dependence | train | 0.401 | 0.368 | 0.253 | -0.024 |
| F3_dependence | val | 0.448 | 0.472 | 0.191 | -0.049 |
| F4_seasonality | oot | 0.271 | 0.276 | 0.371 | 0.261 |
| F4_seasonality | train | 0.256 | 0.255 | 0.256 | 0.185 |
| F4_seasonality | val | 0.256 | 0.361 | 0.385 | 0.412 |
| F5_seams | oot | 0.159 | 0.075 | 0.161 | 0.018 |
| F5_seams | train | 0.225 | 0.002 | 0.089 | -0.074 |
| F5_seams | val | 0.225 | 0.135 | 0.339 | 0.236 |
| F6_windows | oot | 0.406 | 0.407 | 0.374 | -0.014 |
| F6_windows | train | 0.275 | 0.261 | 0.368 | -0.002 |
| F6_windows | val | 0.311 | 0.296 | 0.376 | 0.338 |
| F7_long_structure | oot | 0.199 | 0.197 | 0.005 | -0.25 |
| F7_long_structure | train | 0.211 | 0.13 | 0.089 | -0.043 |
| F7_long_structure | val | 0.074 | 0.183 | 0.096 | 0.001 |
| F8_target | oot | 0.377 | 0.395 | 0.476 | 0.246 |
| F8_target | train | 0.291 | 0.305 | 0.432 | 0.247 |
| F8_target | val | 0.369 | 0.379 | 0.379 | 0.326 |
| F9_coverage | oot | 0.381 | 0.357 | 0.172 | -0.052 |
| F9_coverage | train | 0.442 | 0.443 | 0.408 | 0.256 |
| F9_coverage | val | 0.129 | 0.338 | 0.431 | 0.354 |


**top_predictors**

| unit | metric | reference | group | criterion | n_datasets | median_rho | share_positive | p_two_sided | p_bh | predictive |
|---|---|---|---|---|---|---|---|---|---|---|
| F3.1_acf_in_window@train | F3.1_acf_in_window | train | F3_dependence | regression@val | 9 | 0.809 | 0.667 | 0.0547 | 0.167 | False |
| F3.2_acf_beyond_window@train | F3.2_acf_beyond_window | train | F3_dependence | regression@val | 9 | 0.779 | 0.667 | 0.0977 | 0.231 | False |
| F3.1_acf_in_window@oot | F3.1_acf_in_window | oot | F3_dependence | regression@oot | 9 | 0.732 | 1 | 0.00391 | 0.0501 | False |
| F3.1_acf_in_window | F3.1_acf_in_window | val | F3_dependence | regression@oot | 9 | 0.712 | 0.778 | 0.0391 | 0.135 | False |
| F6.6_feature_fid@oot | F6.6_feature_fid | oot | F6_windows | regression@oot | 9 | 0.697 | 0.889 | 0.0195 | 0.0892 | False |
| F3.2_acf_beyond_window@oot | F3.2_acf_beyond_window | oot | F3_dependence | classification@oot | 9 | 0.684 | 0.889 | 0.0273 | 0.108 | False |
| F8.4_event_by_how | F8.4_event_by_how | val | F8_target | regression@val | 9 | 0.668 | 0.889 | 0.0117 | 0.0695 | False |
| F3.2_acf_beyond_window@oot | F3.2_acf_beyond_window | oot | F3_dependence | regression@oot | 9 | 0.665 | 0.889 | 0.0273 | 0.108 | False |
| F2.1_ks_d168@oot | F2.1_ks_d168 | oot | F2_increments | classification@oot | 9 | 0.64 | 0.778 | 0.0195 | 0.0892 | False |
| F8.6_cond_future_ks@oot | F8.6_cond_future_ks | oot | F8_target | classification@val | 9 | 0.638 | 1 | 0.00391 | 0.0501 | False |
| F6.6_feature_fid | F6.6_feature_fid | val | F6_windows | regression@oot | 9 | 0.626 | 0.778 | 0.0508 | 0.167 | False |
| F3.1_acf_in_window | F3.1_acf_in_window | val | F3_dependence | classification@val | 9 | 0.62 | 0.778 | 0.0742 | 0.2 | False |
| F1.9_js | F1.9_js | val | F1_marginal | classification@val | 9 | 0.618 | 0.667 | 0.0977 | 0.231 | False |
| F3.4_acf_sq_d | F3.4_acf_sq_d | val | F3_dependence | classification@val | 9 | 0.609 | 0.778 | 0.0977 | 0.231 | False |
| F3.2_acf_beyond_window | F3.2_acf_beyond_window | val | F3_dependence | classification@val | 9 | 0.604 | 1 | 0.00391 | 0.0501 | False |
| F2.2_vol_ratio_err_d24@oot | F2.2_vol_ratio_err_d24 | oot | F2_increments | classification@oot | 9 | 0.586 | 0.889 | 0.00781 | 0.0587 | False |
| F8.5_cond_event_err | F8.5_cond_event_err | val | F8_target | regression@val | 9 | 0.585 | 0.778 | 0.0742 | 0.2 | False |
| F8.6_cond_future_ks@oot | F8.6_cond_future_ks | oot | F8_target | classification@oot | 9 | 0.582 | 0.889 | 0.00781 | 0.0587 | False |
| F3.8_calendar_corr_err@oot | F3.8_calendar_corr_err | oot | F3_dependence | regression@val | 9 | 0.582 | 0.778 | 0.0195 | 0.0892 | False |
| F2.1_ks_d168@train | F2.1_ks_d168 | train | F2_increments | classification@oot | 9 | 0.578 | 0.778 | 0.0391 | 0.135 | False |


### RQ5. Gap to real data (TSTR / TRTR), stability over time and across models

| method | unit | n_datasets | median_ratio | ci_lo | ci_hi | p_below_real | p_below_real_bh | verdict |
|---|---|---|---|---|---|---|---|---|
| chronos | classification@oot | 7 | 0.49 | 0 | 0.858 | 0.00781 | 0.00847 | worse than real |
| chronos | classification@val | 7 | 0.52 | 0.0783 | 0.895 | 0.00781 | 0.00847 | worse than real |
| chronos | regression@oot | 7 | 0.684 | 0.655 | 0.814 | 0.00781 | 0.00847 | worse than real |
| chronos | regression@val | 7 | 0.818 | 0.575 | 0.961 | 0.0156 | 0.0159 | worse than real |
| diffusion_ts | classification@oot | 9 | 0.647 | 0.487 | 0.901 | 0.00195 | 0.0025 | worse than real |
| diffusion_ts | classification@val | 9 | 0.719 | 0.369 | 0.981 | 0.00195 | 0.0025 | worse than real |
| diffusion_ts | regression@oot | 9 | 0.795 | 0.571 | 0.903 | 0.00195 | 0.0025 | worse than real |
| diffusion_ts | regression@val | 9 | 0.724 | 0.582 | 0.946 | 0.00195 | 0.0025 | worse than real |
| timesfm | classification@oot | 6 | 0.686 | 0 | 0.964 | 0.0156 | 0.0159 | worse than real |
| timesfm | classification@val | 6 | 0.754 | 0 | 0.919 | 0.0156 | 0.0159 | worse than real |
| timesfm | regression@oot | 6 | 0.871 | 0.839 | 0.937 | 0.0156 | 0.0159 | worse than real |
| timesfm | regression@val | 6 | 0.89 | 0.782 | 0.991 | 0.0312 | 0.0312 | worse than real |
| timestral | classification@oot | 9 | 0 | -0.0351 | 0.832 | 0.00195 | 0.0025 | worse than real |
| timestral | classification@val | 9 | 0 | 0 | 0.277 | 0.00195 | 0.0025 | worse than real |
| timestral | regression@oot | 9 | 0.782 | 0.669 | 0.864 | 0.00195 | 0.0025 | worse than real |
| timestral | regression@val | 9 | 0.835 | 0.722 | 0.966 | 0.00195 | 0.0025 | worse than real |
| vae_atsp | classification@oot | 9 | 0.611 | 0.571 | 0.905 | 0.00391 | 0.00446 | worse than real |
| vae_atsp | classification@val | 9 | 0.596 | 0.443 | 0.907 | 0.00195 | 0.0025 | worse than real |
| vae_atsp | regression@oot | 9 | 0.617 | 0.443 | 0.776 | 0.00195 | 0.0025 | worse than real |
| vae_atsp | regression@val | 9 | 0.507 | 0.461 | 0.689 | 0.00195 | 0.0025 | worse than real |
| vae_greedy | classification@oot | 9 | 0.644 | 0.562 | 0.819 | 0.00195 | 0.0025 | worse than real |
| vae_greedy | classification@val | 9 | 0.621 | 0.45 | 0.876 | 0.00195 | 0.0025 | worse than real |
| vae_greedy | regression@oot | 9 | 0.593 | 0.485 | 0.791 | 0.00195 | 0.0025 | worse than real |
| vae_greedy | regression@val | 9 | 0.514 | 0.465 | 0.72 | 0.00195 | 0.0025 | worse than real |
| vae_herding | classification@oot | 9 | 0.654 | 0.561 | 0.908 | 0.00391 | 0.00446 | worse than real |
| vae_herding | classification@val | 9 | 0.745 | 0.501 | 0.814 | 0.00195 | 0.0025 | worse than real |
| vae_herding | regression@oot | 9 | 0.698 | 0.468 | 0.823 | 0.00195 | 0.0025 | worse than real |
| vae_herding | regression@val | 9 | 0.508 | 0.426 | 0.572 | 0.00195 | 0.0025 | worse than real |
| vae_knn | classification@oot | 9 | 0.657 | 0.519 | 0.875 | 0.00391 | 0.00446 | worse than real |
| vae_knn | classification@val | 9 | 0.609 | 0.565 | 0.865 | 0.00195 | 0.0025 | worse than real |
| vae_knn | regression@oot | 9 | 0.572 | 0.395 | 0.814 | 0.00195 | 0.0025 | worse than real |
| vae_knn | regression@val | 9 | 0.507 | 0.447 | 0.707 | 0.00195 | 0.0025 | worse than real |
| vae_mbb | classification@oot | 9 | 0.712 | 0.437 | 0.802 | 0.00391 | 0.00446 | worse than real |
| vae_mbb | classification@val | 9 | 0.654 | 0.464 | 0.829 | 0.00195 | 0.0025 | worse than real |
| vae_mbb | regression@oot | 9 | 0.511 | 0.378 | 0.785 | 0.00195 | 0.0025 | worse than real |
| vae_mbb | regression@val | 9 | 0.471 | 0.453 | 0.666 | 0.00195 | 0.0025 | worse than real |
| vae_pctsp | classification@oot | 9 | 0.648 | 0.536 | 0.841 | 0.00195 | 0.0025 | worse than real |
| vae_pctsp | classification@val | 9 | 0.61 | 0.598 | 0.835 | 0.00195 | 0.0025 | worse than real |
| vae_pctsp | regression@oot | 9 | 0.634 | 0.43 | 0.796 | 0.00195 | 0.0025 | worse than real |
| vae_pctsp | regression@val | 9 | 0.537 | 0.408 | 0.71 | 0.00195 | 0.0025 | worse than real |

_Showing 40 rows of 64 (rows with a better / worse / same verdict first); all of them — `hypotheses/RQ5_global.parquet`._

**rank_stability**

| comparison | criterion | tau |
|---|---|---|
| val ↔ oot | fidelity:dependence | 0.282 |
| val ↔ oot | fidelity:distribution | 0.41 |
| val ↔ oot | fidelity:long_structure | 0.333 |
| val ↔ oot | fidelity:seams | 0.231 |
| val ↔ oot | fidelity:target | 0.744 |
| val ↔ oot | fidelity:windows | -0.103 |
| val ↔ oot | theme:class_balance:fidelity | 0.667 |
| val ↔ oot | theme:class_balance:utility | 0.744 |
| val ↔ oot | theme:extremes:fidelity | 0.641 |
| val ↔ oot | theme:extremes:utility | 0.641 |
| val ↔ oot | utility:classification | 0.821 |
| val ↔ oot | utility:regression | 0.59 |
| linear ↔ gbdt | utility:classification@oot | 0.744 |
| linear ↔ gbdt | utility:classification@val | 0.513 |
| linear ↔ gbdt | utility:regression@oot | 0.462 |
| linear ↔ gbdt | utility:regression@val | 0.718 |


**rank_shift_oot_minus_val**

| method | utility:classification | utility:regression |
|---|---|---|
| chronos | 0.42 | 2.39 |
| diffusion_ts | 0.62 | -0.1 |
| timesfm | 0.31 | -0.13 |
| timestral | -0.38 | 1.59 |
| vae_atsp | 0 | -0.49 |
| vae_greedy | 0.06 | 0.15 |
| vae_herding | -0.62 | -1.5 |
| vae_knn | 0.2 | 0.31 |
| vae_mbb | 0 | -0.41 |
| vae_pctsp | -0.13 | -0.31 |
| vae_quilting | -0.32 | -0.3 |
| vae_rand | -0.18 | -0.43 |
| vae_zseries | 0.22 | -0.29 |


**decision_transfer**: no model grid: profile max (decision_transfer=True)

### RQ6. Speed and cost: training and generation time, memory, Pareto front "quality × time"

| method | median_time_s | ci_lo | ci_hi | n_datasets | x_fastest |
|---|---|---|---|---|---|
| timestral | 6.84 | 6.83 | 6.84 | 9 | 1 |
| timesfm | 21.8 | 21.8 | 21.8 | 6 | 3.19 |
| chronos | 79.2 | 78.8 | 80.8 | 7 | 11.6 |
| vae_rand | 127 | 111 | 132 | 9 | 18.6 |
| vae_quilting | 127 | 111 | 132 | 9 | 18.6 |
| vae_greedy | 127 | 112 | 132 | 9 | 18.6 |
| vae_knn | 127 | 111 | 132 | 9 | 18.6 |
| vae_mbb | 127 | 111 | 132 | 9 | 18.6 |
| vae_herding | 127 | 111 | 132 | 9 | 18.6 |
| vae_zseries | 131 | 115 | 136 | 9 | 19.2 |
| vae_zseries_xfade | 132 | 116 | 137 | 9 | 19.3 |
| vae_zseries_quilt | 132 | 116 | 137 | 9 | 19.3 |
| vae_zseries_wsola | 132 | 117 | 137 | 9 | 19.3 |
| vae_atsp | 149 | 137 | 153 | 9 | 21.8 |
| vae_pctsp | 187 | 171 | 192 | 9 | 27.3 |
| diffusion_ts | 5.83e+03 | 4.26e+03 | 5.85e+03 | 9 | 853 |

**cost_parts**

| method | total:wall_time | training:wall_time | generation:wall_time | memory:gpu_peak_mb | memory:rss_delta_mb |
|---|---|---|---|---|---|
| timestral | 6.8 | 6.4 | 0.5 | 2.1e+03 | 0 |
| timesfm | 21.8 | 21.1 | 0.7 | 2.11e+03 | 0 |
| chronos | 79.2 | 13.7 | 65.2 | 137 | 0 |
| vae_rand | 127 | 127 | 0 | 778 | 0 |
| vae_quilting | 127 | 127 | 0 | 2.08e+03 | 0 |
| vae_greedy | 127 | 127 | 0 | 2.08e+03 | 0 |
| vae_knn | 127 | 127 | 0 | 2.08e+03 | 0 |
| vae_mbb | 127 | 127 | 0 | 2.08e+03 | 0 |
| vae_herding | 127 | 127 | 0.1 | 778 | 0 |
| vae_zseries | 132 | 127 | 4.6 | 778 | 0 |
| vae_zseries_xfade | 132 | 127 | 5 | 778 | 0 |
| vae_zseries_quilt | 132 | 127 | 5 | 778 | 0 |
| vae_zseries_wsola | 132 | 127 | 5.4 | 778 | 0 |
| vae_atsp | 149 | 127 | 20.1 | 2.08e+03 | 0.4 |
| vae_pctsp | 187 | 127 | 60 | 2.08e+03 | 0 |
| diffusion_ts | 5.83e+03 | 5.71e+03 | 126 | 2.09e+03 | 5.5 |


**cost_ranks**

| method | cost@generation | cost@memory | cost@total | cost@training |
|---|---|---|---|---|
| timestral | 7.32 | 7.22 | 1 | 1 |
| timesfm | 8.11 | 8.44 | 2.02 | 2.85 |
| chronos | 12 | 3.37 | 2.74 | 2.03 |
| vae_rand | 1 | 5.42 | 3.53 | 7.74 |
| vae_quilting | 2.06 | 6.96 | 4.59 | 7.74 |
| vae_greedy | 3.12 | 6.98 | 5.64 | 7.74 |
| vae_knn | 4.14 | 6.96 | 6.66 | 7.74 |
| vae_mbb | 5.21 | 6.98 | 7.74 | 7.74 |
| vae_herding | 6.26 | 5.67 | 8.79 | 7.74 |
| vae_zseries | 9.04 | 6.05 | 9.84 | 7.74 |
| vae_zseries_xfade |  |  |  |  |
| vae_zseries_quilt |  |  |  |  |
| vae_zseries_wsola |  |  |  |  |
| vae_atsp | 10.1 | 9 | 10.9 | 7.74 |
| vae_pctsp | 11.1 | 7 | 11.9 | 7.74 |
| diffusion_ts | 13 | 10.6 | 13 | 13 |


**pareto**

| ranking | method | family | avg_rank | rank_with_cost | median_time_s | pareto |
|---|---|---|---|---|---|---|
| holdout_clf | timestral | long-series generator | 9.45 | 7.67 | 6.84 | True |
| holdout_clf | timesfm | long-series generator | 7.57 | 6.79 | 21.8 | True |
| holdout_clf | chronos | long-series generator | 7.74 | 6.18 | 79.9 | False |
| holdout_clf | vae_rand | random selection | 6.83 | 6.05 | 127 | True |
| holdout_clf | vae_quilting | optimised selection | 6.22 | 6.07 | 127 | True |
| holdout_clf | vae_greedy | optimised selection | 7.19 | 6.9 | 127 | False |
| holdout_clf | vae_knn | optimised selection | 7.14 | 7.03 | 127 | False |
| holdout_clf | vae_mbb | optimised selection | 6.9 | 7.05 | 127 | False |
| holdout_clf | vae_herding | optimised selection | 5.7 | 6.21 | 127 | True |
| holdout_clf | vae_zseries | optimised selection | 6.54 | 7.01 | 131 | False |
| holdout_clf | vae_atsp | optimised selection | 6.95 | 7.95 | 148 | False |
| holdout_clf | vae_pctsp | optimised selection | 6.96 | 7.8 | 184 | False |
| holdout_clf | diffusion_ts | long-series generator | 6.19 | 8.06 | 5.83e+03 | False |
| holdout_reg | timestral | long-series generator | 6.9 | 5.97 | 6.84 | True |
| holdout_reg | timesfm | long-series generator | 5.32 | 5.29 | 21.8 | True |
| holdout_reg | chronos | long-series generator | 6.74 | 5.51 | 79.9 | False |
| holdout_reg | vae_rand | random selection | 7.72 | 6.64 | 127 | False |
| holdout_reg | vae_quilting | optimised selection | 6.89 | 6.52 | 127 | False |
| holdout_reg | vae_greedy | optimised selection | 7.76 | 7.28 | 127 | False |
| holdout_reg | vae_knn | optimised selection | 7.71 | 7.41 | 127 | False |
| holdout_reg | vae_mbb | optimised selection | 7.66 | 7.56 | 127 | False |
| holdout_reg | vae_herding | optimised selection | 6.3 | 6.61 | 127 | False |
| holdout_reg | vae_zseries | optimised selection | 6.66 | 7.09 | 131 | False |
| holdout_reg | vae_atsp | optimised selection | 7.45 | 8.28 | 148 | False |
| holdout_reg | vae_pctsp | optimised selection | 7.56 | 8.19 | 184 | False |
| holdout_reg | diffusion_ts | long-series generator | 5.75 | 7.77 | 5.83e+03 | False |
| train_clf | timestral | long-series generator | 10.1 | 8.08 | 6.84 | True |
| train_clf | timesfm | long-series generator | 7.56 | 6.79 | 21.8 | True |
| train_clf | chronos | long-series generator | 8.09 | 6.41 | 79.9 | False |
| train_clf | vae_rand | random selection | 6.8 | 6.02 | 127 | True |
| train_clf | vae_quilting | optimised selection | 6.28 | 6.11 | 127 | True |
| train_clf | vae_greedy | optimised selection | 7.31 | 6.98 | 127 | False |
| train_clf | vae_knn | optimised selection | 7.29 | 7.13 | 127 | False |
| train_clf | vae_mbb | optimised selection | 6.88 | 7.04 | 127 | False |
| train_clf | vae_herding | optimised selection | 5.13 | 5.83 | 127 | True |
| train_clf | vae_zseries | optimised selection | 6.21 | 6.79 | 131 | False |
| train_clf | vae_atsp | optimised selection | 6.87 | 7.9 | 148 | False |
| train_clf | vae_pctsp | optimised selection | 6.97 | 7.8 | 184 | False |
| train_clf | diffusion_ts | long-series generator | 6.04 | 7.96 | 5.83e+03 | False |
| train_reg | timestral | long-series generator | 7.52 | 6.38 | 6.84 | True |


**hardware**: ['NVIDIA L4']

### RQ7. Moderators: dataset descriptors and the effects of RQ2 / RQ3 (exploratory)

| effect | descriptor | spearman | p | n | p_bh |
|---|---|---|---|---|---|
| RQ2:fidelity:chronos vs assembly_median | acf24 | 0 | 1 | 7 | 1 |
| RQ2:fidelity:chronos vs assembly_median | acf168 | 0.393 | 0.383 | 7 | 0.663 |
| RQ2:fidelity:chronos vs assembly_median | kurt_d24 | 0.5 | 0.253 | 7 | 0.569 |
| RQ2:fidelity:chronos vs assembly_median | volclust | 0.536 | 0.215 | 7 | 0.52 |
| RQ2:fidelity:chronos vs assembly_median | trend | -0.107 | 0.819 | 7 | 0.902 |
| RQ2:fidelity:chronos vs assembly_median | nan_share | -0.612 | 0.144 | 7 | 0.454 |
| RQ2:utility:chronos vs assembly_median | acf24 | 0.179 | 0.702 | 7 | 0.892 |
| RQ2:utility:chronos vs assembly_median | acf168 | 0.75 | 0.0522 | 7 | 0.352 |
| RQ2:utility:chronos vs assembly_median | kurt_d24 | 0.679 | 0.0938 | 7 | 0.429 |
| RQ2:utility:chronos vs assembly_median | volclust | 0.464 | 0.294 | 7 | 0.607 |
| RQ2:utility:chronos vs assembly_median | trend | 0.107 | 0.819 | 7 | 0.902 |
| RQ2:utility:chronos vs assembly_median | nan_share | -0.612 | 0.144 | 7 | 0.454 |
| RQ2:fidelity:chronos vs vae_rand | acf24 | 0 | 1 | 7 | 1 |
| RQ2:fidelity:chronos vs vae_rand | acf168 | 0.429 | 0.337 | 7 | 0.626 |
| RQ2:fidelity:chronos vs vae_rand | kurt_d24 | 0.429 | 0.337 | 7 | 0.626 |
| RQ2:fidelity:chronos vs vae_rand | volclust | 0.714 | 0.0713 | 7 | 0.41 |
| RQ2:fidelity:chronos vs vae_rand | trend | -0.107 | 0.819 | 7 | 0.902 |
| RQ2:fidelity:chronos vs vae_rand | nan_share | -0.612 | 0.144 | 7 | 0.454 |
| RQ2:utility:chronos vs vae_rand | acf24 | 0.179 | 0.702 | 7 | 0.892 |
| RQ2:utility:chronos vs vae_rand | acf168 | 0.75 | 0.0522 | 7 | 0.352 |
| RQ2:utility:chronos vs vae_rand | kurt_d24 | 0.679 | 0.0938 | 7 | 0.429 |
| RQ2:utility:chronos vs vae_rand | volclust | 0.464 | 0.294 | 7 | 0.607 |
| RQ2:utility:chronos vs vae_rand | trend | 0.107 | 0.819 | 7 | 0.902 |
| RQ2:utility:chronos vs vae_rand | nan_share | -0.612 | 0.144 | 7 | 0.454 |
| RQ2:fidelity:diffusion_ts vs assembly_median | acf24 | -0.583 | 0.0992 | 9 | 0.438 |
| RQ2:fidelity:diffusion_ts vs assembly_median | acf168 | -0.35 | 0.356 | 9 | 0.633 |
| RQ2:fidelity:diffusion_ts vs assembly_median | kurt_d24 | 0.133 | 0.732 | 9 | 0.901 |
| RQ2:fidelity:diffusion_ts vs assembly_median | volclust | -0.383 | 0.308 | 9 | 0.607 |
| RQ2:fidelity:diffusion_ts vs assembly_median | trend | -0.6 | 0.0876 | 9 | 0.429 |
| RQ2:fidelity:diffusion_ts vs assembly_median | nan_share | 0.525 | 0.147 | 9 | 0.454 |
| RQ2:utility:diffusion_ts vs assembly_median | acf24 | -0.517 | 0.154 | 9 | 0.454 |
| RQ2:utility:diffusion_ts vs assembly_median | acf168 | -0.05 | 0.898 | 9 | 0.935 |
| RQ2:utility:diffusion_ts vs assembly_median | kurt_d24 | 0.533 | 0.139 | 9 | 0.454 |
| RQ2:utility:diffusion_ts vs assembly_median | volclust | -0.183 | 0.637 | 9 | 0.849 |
| RQ2:utility:diffusion_ts vs assembly_median | trend | -0.75 | 0.0199 | 9 | 0.284 |
| RQ2:utility:diffusion_ts vs assembly_median | nan_share | 0.434 | 0.244 | 9 | 0.558 |
| RQ2:fidelity:diffusion_ts vs vae_rand | acf24 | -0.517 | 0.154 | 9 | 0.454 |
| RQ2:fidelity:diffusion_ts vs vae_rand | acf168 | -0.217 | 0.576 | 9 | 0.819 |
| RQ2:fidelity:diffusion_ts vs vae_rand | kurt_d24 | 0.267 | 0.488 | 9 | 0.752 |
| RQ2:fidelity:diffusion_ts vs vae_rand | volclust | -0.217 | 0.576 | 9 | 0.819 |

_Showing 40 rows of 128; all of them — `hypotheses/RQ7_global.parquet`._

### RQ8. Class balance: do methods preserve class shares (rare events especially) and what does an error cost

| comparison | kind | unit | n_datasets | median_z | mean_z | ci_lo | ci_hi | p_better_adj | p_worse_adj | p_equiv_adj | n_better | n_worse | n_same | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| vae_atsp vs vae_rand | fidelity | F11.1_class_share_logratio | 9 | 2.35 | 2.56 | 0.74 | 4.51 | 0.434 | 1 | 0.96 | 4 | 0 | 0 | inconclusive |
| vae_herding vs vae_rand | fidelity | F11.1_class_share_logratio | 9 | 2.89 | 2.77 | 1.09 | 4.38 | 0.434 | 1 | 0.98 | 7 | 1 | 0 | inconclusive |
| vae_herding vs vae_rand | fidelity | F11.3_multiclass_tvd | 9 | 2.26 | 2.18 | 0.928 | 3.55 | 0.434 | 1 | 0.96 | 5 | 0 | 0 | inconclusive |
| vae_herding vs vae_rand | fidelity | F8.1_class_tvd | 9 | 1.68 | 1.73 | 0.495 | 2.8 | 0.434 | 1 | 0.936 | 4 | 0 | 0 | inconclusive |
| vae_zseries vs vae_rand | fidelity | F11.1_class_share_logratio | 9 | 3.36 | 4.9 | 2.47 | 7.58 | 0.434 | 1 | 0.998 | 7 | 0 | 0 | inconclusive |
| vae_atsp vs vae_rand | utility | clf_up_h168_q90\|gbdt\|S\|val\|ece | 9 | 1.67 | 1.95 | 0.608 | 3.6 | 0.434 | 1 | 0.96 | 4 | 1 | 0 | inconclusive |
| vae_atsp vs vae_rand | utility | clf_up_h168_q90\|linear\|S\|oot\|ece | 9 | 1.86 | 2.99 | 1.36 | 4.88 | 0.434 | 1 | 0.98 | 4 | 0 | 0 | inconclusive |
| vae_atsp vs vae_rand | utility | clf_up_h168_q90\|linear\|S\|val\|ece | 9 | 1.67 | 2.7 | 0.93 | 4.9 | 0.434 | 1 | 0.968 | 4 | 0 | 0 | inconclusive |
| vae_greedy vs vae_rand | utility | clf_up_h168_q90\|gbdt\|S\|val\|ece | 9 | 1.87 | 1.54 | 0.653 | 2.32 | 0.434 | 1 | 0.96 | 5 | 0 | 0 | inconclusive |
| vae_greedy vs vae_rand | utility | clf_up_h168_q90\|linear\|S\|oot\|ece | 9 | 2.88 | 2.64 | 1.33 | 3.94 | 0.434 | 1 | 0.986 | 5 | 0 | 0 | inconclusive |
| vae_greedy vs vae_rand | utility | clf_up_h168_q90\|linear\|S\|val\|ece | 9 | 2.55 | 2.55 | 1.35 | 3.69 | 0.434 | 1 | 0.993 | 6 | 0 | 0 | inconclusive |
| vae_herding vs vae_rand | utility | clf_down_h24_q10\|gbdt\|S\|oot\|ece | 9 | 0.62 | 0.994 | 0.298 | 1.95 | 0.434 | 1 | 0.639 | 3 | 0 | 0 | inconclusive |
| vae_herding vs vae_rand | utility | clf_up_h6_q90\|gbdt\|S\|oot\|ece | 9 | 1.38 | 1.46 | 0.349 | 2.78 | 0.434 | 1 | 0.906 | 2 | 1 | 0 | inconclusive |
| vae_knn vs vae_rand | utility | clf_up_h168_q90\|linear\|S\|val\|ece | 9 | 1.54 | 1.78 | 0.62 | 2.88 | 0.434 | 1 | 0.968 | 4 | 0 | 0 | inconclusive |
| vae_pctsp vs vae_rand | utility | clf_up_h168_q90\|gbdt\|S\|val\|ece | 9 | 2.02 | 1.77 | 0.726 | 2.79 | 0.434 | 1 | 0.96 | 6 | 0 | 0 | inconclusive |
| vae_quilting vs vae_rand | utility | clf_up_h168_q90\|linear\|S\|val\|ece | 9 | 1.82 | 3.12 | 0.551 | 6.32 | 0.434 | 1 | 0.92 | 3 | 1 | 0 | inconclusive |
| vae_zseries vs vae_rand | utility | clf_up_h168_q90\|gbdt\|S\|val\|ece | 9 | 1.53 | 1.44 | 0.358 | 2.64 | 0.434 | 1 | 0.906 | 4 | 1 | 0 | inconclusive |
| vae_zseries vs vae_rand | utility | clf_up_h168_q90\|linear\|S\|val\|ece | 9 | 2 | 2.06 | 0.556 | 3.87 | 0.434 | 1 | 0.906 | 3 | 0 | 0 | inconclusive |
| vae_herding vs vae_rand | fidelity | F11.2_rare_share_logratio | 9 | 1.26 | 1.72 | 0.384 | 3.18 | 0.46 | 1 | 0.881 | 5 | 1 | 0 | inconclusive |
| vae_zseries vs vae_rand | fidelity | F11.2_rare_share_logratio | 9 | 2.56 | 3.1 | 0.94 | 5.79 | 0.46 | 1 | 0.968 | 5 | 0 | 0 | inconclusive |
| vae_zseries_wsola vs vae_rand | fidelity | F11.1_class_share_logratio | 9 | 2.79 | 3.16 | 0.67 | 5.63 | 0.46 | 1 | 0.968 | 6 | 1 | 0 | inconclusive |
| vae_zseries_wsola vs vae_rand | fidelity | F11.2_rare_share_logratio | 9 | 1.48 | 2.59 | 0.324 | 5.29 | 0.46 | 1 | 0.906 | 3 | 1 | 0 | inconclusive |
| vae_herding vs vae_rand | utility | clf_down_h24_q10\|gbdt\|S\|val\|ece | 9 | 2.06 | 1.67 | 0.298 | 3.02 | 0.46 | 1 | 0.92 | 1 | 0 | 0 | inconclusive |
| vae_knn vs vae_rand | utility | clf_up_h168_q90\|gbdt\|S\|val\|ece | 9 | 1.36 | 1.07 | 0.219 | 1.87 | 0.46 | 1 | 0.783 | 4 | 0 | 0 | inconclusive |
| vae_knn vs vae_rand | utility | clf_up_h168_q90\|linear\|S\|oot\|ece | 9 | 1.26 | 1.72 | 0.462 | 2.98 | 0.46 | 1 | 0.92 | 5 | 0 | 0 | inconclusive |
| vae_pctsp vs vae_rand | utility | clf_up_h168_q90\|linear\|S\|oot\|ece | 9 | 1.53 | 2.17 | 0.475 | 3.9 | 0.46 | 1 | 0.952 | 5 | 0 | 0 | inconclusive |
| vae_pctsp vs vae_rand | utility | clf_up_h168_q90\|linear\|S\|val\|ece | 9 | 2.18 | 2.37 | 0.644 | 4.23 | 0.46 | 1 | 0.92 | 5 | 0 | 0 | inconclusive |
| vae_quilting vs vae_rand | utility | clf_up_h168_q90\|gbdt\|S\|val\|ece | 9 | 1.64 | 2.03 | 0.471 | 4.03 | 0.46 | 1 | 0.859 | 4 | 0 | 0 | inconclusive |
| vae_quilting vs vae_rand | utility | clf_up_h168_q90\|linear\|S\|oot\|ece | 9 | 0.805 | 2.61 | 0.0729 | 5.55 | 0.46 | 1 | 0.796 | 3 | 1 | 0 | inconclusive |
| vae_quilting vs vae_rand | utility | clf_up_h24_q90\|gbdt\|S\|oot\|ece | 9 | 0.825 | 0.95 | 0.187 | 1.69 | 0.46 | 1 | 0.713 | 3 | 0 | 0 | inconclusive |
| vae_zseries vs vae_rand | utility | clf_up_h168_q90\|linear\|S\|oot\|ece | 9 | 2.15 | 2.1 | 0.715 | 3.66 | 0.46 | 1 | 0.96 | 4 | 0 | 0 | inconclusive |
| vae_zseries_wsola vs vae_rand | utility | clf_up_h168_q90\|gbdt\|S\|val\|ece | 9 | 0.991 | 0.923 | 0.0939 | 1.69 | 0.46 | 1 | 0.72 | 4 | 0 | 0 | inconclusive |
| diffusion_ts vs assembly_median | utility | clf_up_h24_q90\|mlp\|S\|val\|ece | 9 | 2.09 | 2.08 | 0.364 | 3.79 | 0.46 | 1 | 0.92 | 6 | 0 | 0 | inconclusive |
| timesfm vs assembly_median | utility | clf_up_h6_q90\|gbdt\|S\|val\|ece | 6 | 4.46 | 9.33 | 2.79 | 16.9 | 0.46 | 1 | 0.993 | 5 | 0 | 0 | inconclusive |
| timestral vs assembly_median | fidelity | F11.1_class_share_logratio | 9 | -84.5 | -77 | -103 | -50.7 | 1 | 0.559 | 1 | 0 | 9 | 0 | inconclusive |
| timestral vs assembly_median | fidelity | F11.1_class_share_logratio@oot | 9 | -91 | -90.3 | -127 | -53.7 | 1 | 0.559 | 0.998 | 1 | 8 | 0 | inconclusive |
| vae_mbb vs vae_rand | utility | clf_down_h24_q10\|gbdt\|S\|oot\|ece | 9 | -0.136 | -0.351 | -0.76 | -0.0183 | 1 | 0.559 | 0.0931 | 0 | 0 | 0 | inconclusive |
| vae_zseries_quilt vs vae_rand | utility | clf_down_h24_q10\|gbdt\|S\|oot\|ece | 9 | -0.328 | -0.816 | -1.52 | -0.123 | 1 | 0.559 | 0.639 | 0 | 3 | 0 | inconclusive |
| vae_atsp vs vae_rand | fidelity | F11.2_rare_share_logratio | 9 | 1.27 | 1.98 | 0.205 | 3.72 | 0.576 | 1 | 0.906 | 3 | 1 | 0 | inconclusive |
| vae_atsp vs vae_rand | fidelity | F11.3_multiclass_tvd | 9 | 1.24 | 1.13 | -0.582 | 2.53 | 0.576 | 1 | 0.796 | 4 | 1 | 0 | inconclusive |

_Showing 40 rows of 572 (rows with a better / worse / same verdict first); all of them — `hypotheses/RQ8_global.parquet`._

**ranking**

| theme:class_balance:fidelity@oot | theme:class_balance:fidelity@train | theme:class_balance:fidelity@val | theme:class_balance:utility@oot | theme:class_balance:utility@val |
|---|---|---|---|---|
| 8.02 | 8.16 | 7.54 | 7.27 | 6.59 |
| 6.97 | 6.63 | 6.05 | 5.99 | 5.7 |
| 8.65 | 8.27 | 9.15 | 7.13 | 7.02 |
| 10.4 | 10.6 | 10 | 9.4 | 9.23 |
| 6.18 | 5.93 | 6.06 | 6.83 | 6.97 |
| 7.24 | 7.41 | 7.35 | 7.38 | 7.07 |
| 5.38 | 5.17 | 5.22 | 5.67 | 6.41 |
| 7.48 | 7.65 | 7.68 | 7.37 | 7.07 |
| 7.07 | 7.23 | 7.84 | 7.28 | 7.24 |
| 6.5 | 6.83 | 6.11 | 7 | 6.93 |
| 5.94 | 6.26 | 6.44 | 6.43 | 6.92 |
| 5.01 | 4.41 | 4.59 | 6.03 | 6.42 |
| 6.9 | 7.13 | 7.77 | 7.31 | 7.35 |


**ranking_tests**

| column | p_friedman | nemenyi_cd | n_blocks | n_methods_friedman | best |
|---|---|---|---|---|---|
| theme:class_balance:fidelity@oot | 0.0195 | 5.03 | 9 | 11 | vae_zseries |
| theme:class_balance:fidelity@train | 0.000406 | 5.03 | 9 | 11 | vae_zseries |
| theme:class_balance:fidelity@val | 0.000311 | 5.03 | 9 | 11 | vae_zseries |
| theme:class_balance:utility@oot | 0.0787 | 5.03 | 9 | 11 | vae_herding |
| theme:class_balance:utility@val | 0.272 | 5.03 | 9 | 11 | diffusion_ts |


**verdicts_by_comparison**

| kind | comparison | inconclusive |
|---|---|---|
| fidelity | chronos vs assembly_median | 10 |
| fidelity | diffusion_ts vs assembly_median | 8 |
| fidelity | timesfm vs assembly_median | 8 |
| fidelity | timestral vs assembly_median | 8 |
| fidelity | vae_atsp vs vae_rand | 8 |
| fidelity | vae_greedy vs vae_rand | 8 |
| fidelity | vae_herding vs vae_rand | 8 |
| fidelity | vae_knn vs vae_rand | 8 |
| fidelity | vae_mbb vs vae_rand | 8 |
| fidelity | vae_pctsp vs vae_rand | 8 |
| fidelity | vae_quilting vs vae_rand | 8 |
| fidelity | vae_zseries vs vae_rand | 8 |
| fidelity | vae_zseries_quilt vs vae_rand | 8 |
| fidelity | vae_zseries_wsola vs vae_rand | 8 |
| fidelity | vae_zseries_xfade vs vae_rand | 8 |
| utility | chronos vs assembly_median | 30 |
| utility | diffusion_ts vs assembly_median | 30 |
| utility | timesfm vs assembly_median | 30 |
| utility | timestral vs assembly_median | 30 |
| utility | vae_atsp vs vae_rand | 30 |
| utility | vae_greedy vs vae_rand | 30 |
| utility | vae_herding vs vae_rand | 30 |
| utility | vae_knn vs vae_rand | 30 |
| utility | vae_mbb vs vae_rand | 30 |
| utility | vae_pctsp vs vae_rand | 30 |
| utility | vae_quilting vs vae_rand | 30 |
| utility | vae_zseries vs vae_rand | 30 |
| utility | vae_zseries_quilt vs vae_rand | 30 |
| utility | vae_zseries_wsola vs vae_rand | 30 |
| utility | vae_zseries_xfade vs vae_rand | 30 |


**fidelity_predicts_utility**

| unit | reference | n_datasets | median_rho | share_positive | p_two_sided | p_bh |
|---|---|---|---|---|---|---|
| F11.1_class_share_logratio@oot | oot | 9 | 0.682 | 0.889 | 0.0117 | 0.0167 |
| F11.2_rare_share_logratio@oot | oot | 9 | 0.632 | 0.889 | 0.00781 | 0.0156 |
| F11.3_multiclass_tvd | val | 9 | 0.623 | 1 | 0.00391 | 0.00977 |
| F8.1_class_tvd | val | 9 | 0.555 | 1 | 0.00391 | 0.00977 |
| F11.3_multiclass_tvd@oot | oot | 9 | 0.545 | 0.889 | 0.0117 | 0.0167 |
| F11.1_class_share_logratio | val | 9 | 0.477 | 1 | 0.00391 | 0.00977 |
| F8.1_class_tvd@oot | oot | 9 | 0.471 | 0.889 | 0.0195 | 0.0244 |
| F11.2_rare_share_logratio | val | 9 | 0.455 | 1 | 0.00391 | 0.00977 |
| F11.4_minority_lost | val | 9 | 0.235 | 0.778 | 0.0742 | 0.0825 |
| F11.4_minority_lost@oot | oot | 9 | 0.134 | 0.778 | 0.164 | 0.164 |


### RQ9. Outliers and extremes: do methods preserve tails and outliers, and does it matter to the models

| comparison | kind | unit | n_datasets | median_z | mean_z | ci_lo | ci_hi | p_better_adj | p_worse_adj | p_equiv_adj | n_better | n_worse | n_same | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| vae_herding vs vae_rand | fidelity | F1.5_q01_err@oot | 9 | 1.73 | 1.91 | 1.14 | 2.71 | 0.0842 | 1 | 1 | 4 | 0 | 0 | inconclusive |
| vae_atsp vs vae_rand | utility | reg_h168\|linear\|S\|oot\|mae_extreme | 9 | 3.42 | 3.74 | 2.1 | 5.89 | 0.0842 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| vae_greedy vs vae_rand | utility | reg_h168\|gbdt\|S\|oot\|mae_extreme | 9 | 2.2 | 2.37 | 1.34 | 3.66 | 0.0842 | 1 | 1 | 5 | 0 | 0 | inconclusive |
| vae_herding vs vae_rand | utility | reg_h24\|linear\|S\|oot\|mae_extreme | 9 | 1.63 | 1.45 | 0.866 | 2.13 | 0.0842 | 1 | 1 | 5 | 0 | 0 | inconclusive |
| vae_quilting vs vae_rand | utility | reg_h24\|gbdt\|S\|oot\|mae_extreme | 9 | 1.02 | 2.07 | 0.611 | 4.18 | 0.0842 | 1 | 0.95 | 4 | 0 | 0 | inconclusive |
| vae_zseries vs vae_rand | utility | reg_h168\|linear\|S\|oot\|mae_extreme | 9 | 3.15 | 3.42 | 1.84 | 5.6 | 0.0842 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| vae_zseries vs vae_rand | utility | reg_h24\|gbdt\|S\|oot\|mae_extreme | 9 | 1.22 | 1.12 | 0.577 | 1.77 | 0.0842 | 1 | 0.915 | 2 | 0 | 0 | inconclusive |
| vae_zseries vs vae_rand | utility | reg_h24\|gbdt\|S\|val\|mae_extreme | 9 | 1.79 | 1.4 | 0.803 | 2.05 | 0.0842 | 1 | 1 | 2 | 0 | 0 | inconclusive |
| vae_zseries_wsola vs vae_rand | utility | reg_h24\|gbdt\|S\|val\|mae_extreme | 9 | 1.58 | 1.28 | 0.65 | 1.98 | 0.0842 | 1 | 0.989 | 1 | 0 | 0 | inconclusive |
| diffusion_ts vs assembly_median | utility | clf_up_h24_q95\|linear\|S\|val\|pr_auc | 9 | 1.3 | 1.55 | 0.793 | 2.42 | 0.0842 | 1 | 0.989 | 4 | 0 | 0 | inconclusive |
| diffusion_ts vs assembly_median | utility | reg_h168\|linear\|S\|oot\|mae_extreme | 9 | 5.53 | 6.85 | 4 | 10.5 | 0.0842 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| diffusion_ts vs assembly_median | utility | vol_h24\|gbdt\|S\|val\|mae_extreme | 9 | 1.34 | 2 | 0.879 | 3.44 | 0.0842 | 1 | 0.989 | 5 | 0 | 0 | inconclusive |
| timestral vs assembly_median | utility | reg_h168\|gbdt\|S\|oot\|mae_extreme | 9 | 4.88 | 7.34 | 3.54 | 11.9 | 0.0842 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| timestral vs assembly_median | utility | reg_h168\|gbdt\|S\|val\|mae_extreme | 9 | 4.51 | 4.66 | 2.88 | 6.83 | 0.0842 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| timestral vs assembly_median | utility | reg_h24\|linear\|S\|oot\|mae_extreme | 9 | 9.98 | 12 | 8.51 | 15.6 | 0.0842 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| timestral vs assembly_median | utility | reg_h24\|linear\|S\|val\|mae_extreme | 9 | 8.99 | 17.3 | 7.7 | 32.5 | 0.0842 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| vae_atsp vs vae_rand | utility | reg_h168\|linear\|S\|val\|mae_extreme | 9 | 3.1 | 2.91 | 1.41 | 4.53 | 0.0963 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| vae_greedy vs vae_rand | utility | reg_h168\|gbdt\|S\|val\|mae_extreme | 9 | 1.56 | 1.79 | 0.97 | 2.58 | 0.0963 | 1 | 1 | 5 | 0 | 0 | inconclusive |
| vae_greedy vs vae_rand | utility | reg_h168\|linear\|S\|oot\|mae_extreme | 9 | 3.24 | 3.96 | 2.05 | 6.54 | 0.0963 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| vae_greedy vs vae_rand | utility | reg_h168\|linear\|S\|val\|mae_extreme | 9 | 2.94 | 3.07 | 1.6 | 4.78 | 0.0963 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| vae_knn vs vae_rand | utility | reg_h168\|gbdt\|S\|oot\|mae_extreme | 9 | 1.4 | 1.52 | 0.502 | 2.82 | 0.0963 | 1 | 0.872 | 4 | 0 | 0 | inconclusive |
| vae_knn vs vae_rand | utility | reg_h168\|linear\|S\|oot\|mae_extreme | 9 | 2.35 | 2.77 | 1.32 | 4.72 | 0.0963 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| vae_knn vs vae_rand | utility | reg_h24\|gbdt\|S\|oot\|mae_extreme | 9 | 0.873 | 1.19 | 0.498 | 2.16 | 0.0963 | 1 | 0.713 | 1 | 0 | 0 | inconclusive |
| vae_pctsp vs vae_rand | utility | reg_h168\|linear\|S\|oot\|mae_extreme | 9 | 3.16 | 3.77 | 1.57 | 6.93 | 0.0963 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| vae_quilting vs vae_rand | utility | reg_h168\|linear\|S\|oot\|mae_extreme | 9 | 1.9 | 2.69 | 1.39 | 4.11 | 0.0963 | 1 | 1 | 5 | 0 | 0 | inconclusive |
| diffusion_ts vs assembly_median | utility | clf_up_h24_q95\|gbdt\|S\|val\|pr_auc | 9 | 0.69 | 0.768 | 0.333 | 1.21 | 0.0963 | 1 | 0.54 | 2 | 0 | 0 | inconclusive |
| diffusion_ts vs assembly_median | utility | reg_h168\|gbdt\|S\|val\|mae_extreme | 9 | 3.37 | 3.42 | 2.01 | 4.71 | 0.0963 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| diffusion_ts vs assembly_median | utility | reg_h168\|linear\|S\|val\|mae_extreme | 9 | 6.74 | 5.86 | 3.05 | 8.89 | 0.0963 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| vae_atsp vs vae_rand | utility | reg_h24\|gbdt\|S\|oot\|mae_extreme | 9 | 0.75 | 0.947 | 0.259 | 1.95 | 0.116 | 1 | 0.54 | 2 | 0 | 0 | inconclusive |
| vae_knn vs vae_rand | utility | reg_h168\|linear\|S\|val\|mae_extreme | 9 | 2.05 | 2.24 | 1.02 | 3.57 | 0.116 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| vae_quilting vs vae_rand | utility | reg_h168\|gbdt\|S\|val\|mae_extreme | 9 | 1.03 | 1.57 | 0.593 | 2.74 | 0.116 | 1 | 0.956 | 3 | 0 | 0 | inconclusive |
| vae_quilting vs vae_rand | utility | reg_h168\|linear\|S\|val\|mae_extreme | 9 | 1.96 | 1.98 | 0.933 | 3.02 | 0.116 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| vae_quilting vs vae_rand | utility | reg_h24\|gbdt\|S\|val\|mae_extreme | 9 | 1.4 | 1.67 | 0.679 | 2.67 | 0.116 | 1 | 1 | 5 | 0 | 0 | inconclusive |
| vae_zseries vs vae_rand | utility | reg_h168\|linear\|S\|val\|mae_extreme | 9 | 2.83 | 2.52 | 1.08 | 4.04 | 0.116 | 1 | 1 | 7 | 1 | 0 | inconclusive |
| diffusion_ts vs assembly_median | utility | reg_h168\|gbdt\|S\|oot\|mae_extreme | 9 | 2.87 | 3.55 | 1.6 | 5.67 | 0.116 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| vae_atsp vs vae_rand | utility | reg_h24\|gbdt\|S\|val\|mae_extreme | 9 | 0.791 | 0.864 | 0.23 | 1.5 | 0.15 | 1 | 0.677 | 2 | 0 | 0 | inconclusive |
| vae_greedy vs vae_rand | utility | reg_h24\|gbdt\|S\|oot\|mae_extreme | 9 | 0.799 | 1.08 | 0.255 | 2.21 | 0.15 | 1 | 0.611 | 1 | 0 | 0 | inconclusive |
| vae_herding vs vae_rand | utility | reg_h24\|gbdt\|S\|oot\|mae_extreme | 9 | 0.831 | 0.956 | 0.248 | 1.96 | 0.15 | 1 | 0.377 | 0 | 0 | 0 | inconclusive |
| vae_herding vs vae_rand | utility | vol_h24\|linear\|S\|val\|mae_extreme | 9 | 1.58 | 1.42 | 0.537 | 2.34 | 0.15 | 1 | 0.956 | 3 | 0 | 0 | inconclusive |
| vae_knn vs vae_rand | utility | reg_h24\|gbdt\|S\|val\|mae_extreme | 9 | 1.71 | 1.27 | 0.492 | 1.99 | 0.15 | 1 | 0.989 | 4 | 0 | 0 | inconclusive |

_Showing 40 rows of 690 (rows with a better / worse / same verdict first); all of them — `hypotheses/RQ9_global.parquet`._

**ranking**

| theme:extremes:fidelity@oot | theme:extremes:fidelity@train | theme:extremes:fidelity@val | theme:extremes:utility@oot | theme:extremes:utility@val |
|---|---|---|---|---|
| 9.13 | 9.12 | 7.61 | 7.24 | 6.53 |
| 7.55 | 6.27 | 6.6 | 5.85 | 5.07 |
| 7.96 | 6.67 | 7.28 | 4.77 | 4.96 |
| 9.22 | 9.72 | 7.88 | 7.42 | 6.94 |
| 6.62 | 7.22 | 7.28 | 7.03 | 7.26 |
| 6.77 | 7.41 | 7.03 | 7.25 | 7.45 |
| 5.79 | 4.68 | 6.63 | 6.86 | 7.31 |
| 6.63 | 7.16 | 6.83 | 7.62 | 7.62 |
| 6 | 6.1 | 6.39 | 8.13 | 8.09 |
| 6.98 | 7.45 | 7.45 | 6.85 | 7.12 |
| 6.86 | 7.47 | 7.43 | 6.46 | 6.88 |
| 6.68 | 6.12 | 6.58 | 6.88 | 6.87 |
| 5.75 | 6.06 | 6.37 | 7.96 | 8.12 |


**ranking_tests**

| column | p_friedman | nemenyi_cd | n_blocks | n_methods_friedman | best |
|---|---|---|---|---|---|
| theme:extremes:fidelity@oot | 0.0275 | 5.03 | 9 | 11 | vae_rand |
| theme:extremes:fidelity@train | 4.38e-06 | 5.03 | 9 | 11 | vae_herding |
| theme:extremes:fidelity@val | 0.645 | 5.03 | 9 | 11 | vae_rand |
| theme:extremes:utility@oot | 0.297 | 5.03 | 9 | 11 | timesfm |
| theme:extremes:utility@val | 0.0629 | 5.03 | 9 | 11 | timesfm |


**verdicts_by_comparison**

| kind | comparison | inconclusive |
|---|---|---|
| fidelity | chronos vs assembly_median | 22 |
| fidelity | diffusion_ts vs assembly_median | 22 |
| fidelity | timesfm vs assembly_median | 22 |
| fidelity | timestral vs assembly_median | 22 |
| fidelity | vae_atsp vs vae_rand | 22 |
| fidelity | vae_greedy vs vae_rand | 22 |
| fidelity | vae_herding vs vae_rand | 22 |
| fidelity | vae_knn vs vae_rand | 22 |
| fidelity | vae_mbb vs vae_rand | 22 |
| fidelity | vae_pctsp vs vae_rand | 22 |
| fidelity | vae_quilting vs vae_rand | 22 |
| fidelity | vae_zseries vs vae_rand | 22 |
| fidelity | vae_zseries_quilt vs vae_rand | 22 |
| fidelity | vae_zseries_wsola vs vae_rand | 22 |
| fidelity | vae_zseries_xfade vs vae_rand | 22 |
| utility | chronos vs assembly_median | 24 |
| utility | diffusion_ts vs assembly_median | 24 |
| utility | timesfm vs assembly_median | 24 |
| utility | timestral vs assembly_median | 24 |
| utility | vae_atsp vs vae_rand | 24 |
| utility | vae_greedy vs vae_rand | 24 |
| utility | vae_herding vs vae_rand | 24 |
| utility | vae_knn vs vae_rand | 24 |
| utility | vae_mbb vs vae_rand | 24 |
| utility | vae_pctsp vs vae_rand | 24 |
| utility | vae_quilting vs vae_rand | 24 |
| utility | vae_zseries vs vae_rand | 24 |
| utility | vae_zseries_quilt vs vae_rand | 24 |
| utility | vae_zseries_wsola vs vae_rand | 24 |
| utility | vae_zseries_xfade vs vae_rand | 24 |


**fidelity_predicts_utility**

| unit | reference | n_datasets | median_rho | share_positive | p_two_sided | p_bh |
|---|---|---|---|---|---|---|
| F2.4_big_jump_share_err@oot | oot | 9 | 0.287 | 0.556 | 0.164 | 0.722 |
| F1.5_q01_err@oot | oot | 9 | 0.244 | 0.778 | 0.082 | 0.722 |
| F1.6_kurt_err | val | 9 | 0.221 | 0.556 | 0.734 | 0.977 |
| F1.10_hill_err | val | 9 | 0.2 | 0.667 | 0.164 | 0.722 |
| F12.5_block_min_ks@oot | oot | 9 | 0.191 | 0.889 | 0.0742 | 0.722 |
| F1.5_q99_err@oot | oot | 9 | 0.186 | 0.667 | 0.496 | 0.977 |
| F12.4_block_max_ks | val | 8 | 0.171 | 0.625 | 0.25 | 0.917 |
| F12.3_spike_rate_err | val | 8 | 0.15 | 0.625 | 0.547 | 0.977 |
| F1.10_hill_err@oot | oot | 9 | 0.141 | 0.556 | 0.496 | 0.977 |
| F2.4_big_jump_share_err | val | 9 | 0.136 | 0.556 | 0.652 | 0.977 |
| F1.5_q01_err | val | 9 | 0.1 | 0.556 | 0.734 | 0.977 |
| F12.2_exceed_magnitude_err | val | 9 | 0.0643 | 0.556 | 0.652 | 0.977 |
| F12.1_exceed_rate_err@oot | oot | 9 | 0.0618 | 0.556 | 0.91 | 0.982 |
| F7.4_excursion_ks@oot | oot | 6 | 0.025 | 0.5 | 0.938 | 0.982 |
| F12.3_spike_rate_err@oot | oot | 8 | -0.0108 | 0.5 | 0.844 | 0.977 |
| F12.5_block_min_ks | val | 9 | -0.0132 | 0.444 | 1 | 1 |
| F1.5_q99_err | val | 9 | -0.0176 | 0.444 | 0.57 | 0.977 |
| F12.1_exceed_rate_err | val | 9 | -0.0235 | 0.444 | 0.426 | 0.977 |
| F7.4_excursion_ks | val | 6 | -0.0728 | 0.333 | 0.844 | 0.977 |
| F12.4_block_max_ks@oot | oot | 9 | -0.141 | 0.444 | 0.734 | 0.977 |
| F1.6_kurt_err@oot | oot | 9 | -0.143 | 0.444 | 0.82 | 0.977 |
| F12.2_exceed_magnitude_err@oot | oot | 9 | -0.182 | 0.111 | 0.129 | 0.722 |

