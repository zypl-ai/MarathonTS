# Benchmark report

Datasets: beijing_pm25, bike, bitcoin, electricity, ett, household, jena, metro, pjm. Seeds: 10. α = 0.05. Leakage (Config.leaked): `chronos` on electricity, beijing_pm25; `timesfm` on beijing_pm25, household, bitcoin. Verdict of a comparison "A vs B": better / worse (A better / worse than B) / same (equivalence, TOST) / inconclusive. Effects are in noise units — divided by the smallest effect size of interest (SESOI: the median |vae_rand − vae_rand_b| on one pool — or, where vae_rand_b is not run (min), the between-seed spread of vae_rand — or the method's between-seed spread, see HYPOTHESES.md §2). Utility: TSTR (training on synthetic data only) vs TRTR (training on real data), tested on the real val / OOT; transfer ratio = 1 — synthetic data train the model as well as real data. Overall leaderboard — `OVERALL.md`; ranking of every method in every slice — `LEADERBOARD.md`; values of the metrics by slice — `METRIC_VALUES.md` (this folder). Tables of the tests — `hypotheses/`.

## Overall leaderboard

Fidelity on the core metrics (each criterion against train, val and OOT) and utility (TSTR classification and regression, val and OOT), equal weights; noise-aware ranks; privacy and cost not included. Composition, columns and the robustness checks — `OVERALL.md`.

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon | fidelity_rank | utility_rank | norm_overall | memorisation_flag |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| vae_herding | optimised selection | 5.54 | 4.86 | 6.18 | 0.783 | 0.999 |  | True | 5.19 | 5.9 | 0.266 | False |
| diffusion_ts | long-series generator | 6.27 | 4.76 | 7.59 | 0.08 | 0.565 | 0.5 | True | 6.83 | 5.71 | 0.161 | False |
| vae_quilting | optimised selection | 6.36 | 5.82 | 6.92 | 0.028 | 0.531 | 0.5 | True | 6.22 | 6.5 | 0.103 | False |
| vae_zseries | optimised selection | 6.41 | 5.67 | 7.2 | 0.068 | 0.473 | 0.5 | True | 5.97 | 6.84 | 0.0662 | False |
| timesfm | long-series generator | 6.72 | 5.29 | 8.27 | 0.035 | 0.358 | 0.5 | True | 7.37 | 6.06 | 0.0118 | False |
| vae_atsp | optimised selection | 7.11 | 6.55 | 7.74 | 0 | 0.004 | 0.0879 | True | 6.86 | 7.35 | 0.0214 | False |
| vae_rand | random selection | 7.2 | 6.45 | 7.86 | 0 | 0.028 | 0.0879 | True | 7.03 | 7.37 | 0 | False |
| vae_mbb | optimised selection | 7.22 | 6.57 | 7.83 | 0 | 0.008 | 0.0879 | True | 7.12 | 7.32 | 0.0422 | False |
| vae_pctsp | optimised selection | 7.23 | 6.79 | 7.7 | 0 | 0 | 0.0879 | True | 6.87 | 7.6 | -0.0349 | False |
| chronos | long-series generator | 7.43 | 6.11 | 8.59 | 0.006 | 0.034 | 0.391 | True | 7.87 | 6.98 | -0.034 | False |
| vae_knn | optimised selection | 7.56 | 7.1 | 8.08 | 0 | 0 | 0.0586 | True | 7.61 | 7.52 | 0.0286 | False |
| vae_greedy | optimised selection | 7.6 | 7.16 | 8.08 | 0 | 0 | 0.0469 | False | 7.64 | 7.56 | 0.00686 | False |
| timestral | long-series generator | 8.56 | 7.46 | 9.5 | 0 | 0 | 0.0469 | False | 9.14 | 7.98 | -0.857 | False |


Sensitivity variants:

| variant | text | first | tau_vs_main | main_first_place |
|---|---|---|---|---|
| main | the leaderboard: core metrics, fidelity against train + val + OOT, noise-aware ranks | vae_herding | 1 | 1 |
| plain_ranks | ordinary average ranks (no ties within the noise) | vae_herding | 0.949 | 1 |
| fidelity_train | fidelity against train only | vae_herding | 0.872 | 1 |
| fidelity_holdout | fidelity against val + OOT only | vae_herding | 0.897 | 1 |
| no_unchecked | without F5.7 (seams, no anchor) and F6.1 against val (noise) | vae_herding | 0.872 | 1 |
| all_metrics | every fidelity metric instead of the core set | diffusion_ts | 0.718 | 2 |
| common_datasets | only the datasets where every method is ranked | vae_herding | 0.744 | 1 |


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
| chronos | long-series generator | 7.65 | 0.01 | True | 6.65 | 0.012 | True | 8.06 | 0 | True | 7.05 | 0 | True |  |
| diffusion_ts | long-series generator | 6.23 | 0.264 | True | 5.79 | 0.211 | True | 6.13 | 0.181 | True | 5.69 | 0.244 | True |  |
| timesfm | long-series generator | 7.57 | 0.012 | True | 5.32 | 0.716 | True | 7.56 | 0.002 | True | 5.31 | 0.642 | True | holdout_reg, train_reg |
| timestral | long-series generator | 9.12 | 0 | True | 6.57 | 0.001 | True | 9.68 | 0 | False | 7.13 | 0 | True |  |
| vae_atsp | optimised selection | 6.89 | 0 | True | 7.39 | 0 | True | 6.8 | 0 | False | 7.29 | 0 | True |  |
| vae_greedy | optimised selection | 7.14 | 0 | True | 7.71 | 0 | True | 7.25 | 0 | False | 7.81 | 0 | True |  |
| vae_herding | optimised selection | 5.95 | 0.319 | True | 6.55 | 0.004 | True | 5.47 | 0.701 | True | 6.07 | 0.015 | True | holdout_clf, train_clf |
| vae_knn | optimised selection | 7.19 | 0 | True | 7.76 | 0 | True | 7.3 | 0 | False | 7.87 | 0 | True |  |
| vae_mbb | optimised selection | 7.12 | 0 | True | 7.87 | 0 | True | 7.07 | 0 | False | 7.83 | 0 | True |  |
| vae_pctsp | optimised selection | 6.86 | 0 | True | 7.45 | 0 | True | 6.84 | 0 | False | 7.43 | 0 | True |  |
| vae_quilting | optimised selection | 5.98 | 0.387 | True | 6.65 | 0.002 | True | 6.05 | 0.105 | True | 6.73 | 0.001 | True |  |
| vae_zseries | optimised selection | 6.52 | 0.007 | True | 6.65 | 0.054 | True | 6.21 | 0.011 | True | 6.34 | 0.098 | True |  |
| vae_rand | random selection | 7.09 | 0.001 | True | 7.98 | 0 | True | 7.04 | 0 | False | 7.93 | 0 | True |  |


### Ranking `holdout_clf`: Fidelity: val + OOT; utility: classification

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| vae_herding | optimised selection | 5.95 | 5.43 | 6.42 | 0.319 | 0.971 |  | True |
| vae_quilting | optimised selection | 5.98 | 5.44 | 6.58 | 0.387 | 0.904 | 0.734 | True |
| diffusion_ts | long-series generator | 6.23 | 4.82 | 7.49 | 0.264 | 0.603 | 0.734 | True |
| vae_zseries | optimised selection | 6.52 | 5.89 | 7.16 | 0.007 | 0.35 | 0.602 | True |
| vae_pctsp | optimised selection | 6.86 | 6.42 | 7.34 | 0 | 0.005 | 0.176 | True |
| vae_atsp | optimised selection | 6.89 | 6.35 | 7.56 | 0 | 0.013 | 0.219 | True |
| vae_rand | random selection | 7.09 | 6.33 | 7.83 | 0.001 | 0.026 | 0.219 | True |
| vae_mbb | optimised selection | 7.12 | 6.39 | 7.81 | 0 | 0.007 | 0.223 | True |
| vae_greedy | optimised selection | 7.14 | 6.69 | 7.62 | 0 | 0 | 0.117 | True |
| vae_knn | optimised selection | 7.19 | 6.73 | 7.69 | 0 | 0 | 0.137 | True |
| timesfm | long-series generator | 7.57 | 5.74 | 9.41 | 0.012 | 0.077 | 0.656 | True |
| chronos | long-series generator | 7.65 | 6.04 | 9.11 | 0.01 | 0.044 | 0.391 | True |
| timestral | long-series generator | 9.12 | 8.02 | 10.1 | 0 | 0 | 0.117 | True |


### Ranking `holdout_reg`: Fidelity: val + OOT; utility: regression

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| timesfm | long-series generator | 5.32 | 3.83 | 7.08 | 0.716 | 0.933 |  | True |
| diffusion_ts | long-series generator | 5.79 | 4.6 | 6.88 | 0.211 | 0.852 | 0.781 | True |
| vae_herding | optimised selection | 6.55 | 5.64 | 7.4 | 0.004 | 0.346 | 0.781 | True |
| timestral | long-series generator | 6.57 | 5.56 | 7.54 | 0.001 | 0.266 | 0.781 | True |
| chronos | long-series generator | 6.65 | 5.29 | 7.83 | 0.012 | 0.257 | 0.781 | True |
| vae_zseries | optimised selection | 6.65 | 5.9 | 7.41 | 0.054 | 0.217 | 0.781 | True |
| vae_quilting | optimised selection | 6.65 | 6.17 | 7.18 | 0.002 | 0.12 | 0.781 | True |
| vae_atsp | optimised selection | 7.39 | 6.85 | 8.03 | 0 | 0.003 | 0.781 | True |
| vae_pctsp | optimised selection | 7.45 | 7.04 | 7.89 | 0 | 0.002 | 0.781 | True |
| vae_greedy | optimised selection | 7.71 | 7.25 | 8.19 | 0 | 0 | 0.781 | True |
| vae_knn | optimised selection | 7.76 | 7.23 | 8.26 | 0 | 0 | 0.781 | True |
| vae_mbb | optimised selection | 7.87 | 7.11 | 8.52 | 0 | 0 | 0.562 | True |
| vae_rand | random selection | 7.98 | 7.1 | 8.72 | 0 | 0.004 | 0.562 | True |


### Ranking `train_clf`: Fidelity: train; utility: classification

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| vae_herding | optimised selection | 5.47 | 5.09 | 5.86 | 0.701 | 0.997 |  | True |
| vae_quilting | optimised selection | 6.05 | 5.34 | 6.76 | 0.105 | 0.761 | 0.539 | True |
| diffusion_ts | long-series generator | 6.13 | 4.63 | 7.48 | 0.181 | 0.573 | 0.539 | True |
| vae_zseries | optimised selection | 6.21 | 5.49 | 6.97 | 0.011 | 0.535 | 0.406 | True |
| vae_atsp | optimised selection | 6.8 | 6.19 | 7.5 | 0 | 0.029 | 0.0352 | False |
| vae_pctsp | optimised selection | 6.84 | 6.32 | 7.37 | 0 | 0 | 0.0352 | False |
| vae_rand | random selection | 7.04 | 6.32 | 7.75 | 0 | 0.017 | 0.0352 | False |
| vae_mbb | optimised selection | 7.07 | 6.37 | 7.75 | 0 | 0.005 | 0.0352 | False |
| vae_greedy | optimised selection | 7.25 | 6.81 | 7.73 | 0 | 0 | 0.0234 | False |
| vae_knn | optimised selection | 7.3 | 6.91 | 7.74 | 0 | 0 | 0.0234 | False |
| timesfm | long-series generator | 7.56 | 5.82 | 9.44 | 0.002 | 0.073 | 0.539 | True |
| chronos | long-series generator | 8.06 | 6.48 | 9.49 | 0 | 0.01 | 0.195 | True |
| timestral | long-series generator | 9.68 | 8.51 | 10.7 | 0 | 0 | 0.0234 | False |


### Ranking `train_reg`: Fidelity: train; utility: regression

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| timesfm | long-series generator | 5.31 | 3.89 | 6.85 | 0.642 | 0.906 |  | True |
| diffusion_ts | long-series generator | 5.69 | 4.47 | 6.79 | 0.244 | 0.835 | 0.781 | True |
| vae_herding | optimised selection | 6.07 | 5.44 | 6.68 | 0.015 | 0.732 | 0.781 | True |
| vae_zseries | optimised selection | 6.34 | 5.51 | 7.21 | 0.098 | 0.358 | 0.781 | True |
| vae_quilting | optimised selection | 6.73 | 6.11 | 7.32 | 0.001 | 0.053 | 0.781 | True |
| chronos | long-series generator | 7.05 | 5.79 | 8.19 | 0 | 0.066 | 0.781 | True |
| timestral | long-series generator | 7.13 | 6.08 | 8.1 | 0 | 0.046 | 0.188 | True |
| vae_atsp | optimised selection | 7.29 | 6.62 | 7.98 | 0 | 0.003 | 0.547 | True |
| vae_pctsp | optimised selection | 7.43 | 6.94 | 7.91 | 0 | 0 | 0.547 | True |
| vae_greedy | optimised selection | 7.81 | 7.42 | 8.22 | 0 | 0 | 0.516 | True |
| vae_mbb | optimised selection | 7.83 | 7.13 | 8.46 | 0 | 0 | 0.516 | True |
| vae_knn | optimised selection | 7.87 | 7.44 | 8.3 | 0 | 0 | 0.516 | True |
| vae_rand | random selection | 7.93 | 7.1 | 8.64 | 0 | 0.001 | 0.516 | True |



## Core-metric rankings (RQ1)

The four rankings with the fidelity domain restricted to the core metric set, fixed in advance: distribution (F1.2_w1, F2.1_ks_d24); dependence (F3.5_log_psd, F4.1_how_mean); windows (F6.1_disc_score, F6.4_mmd); long structure (F7.1_roll_mean_ks, F7.2_roll_std_ks); target (F11.1_class_share_logratio); seams (F5.7_seam_detect_auc_dev). Utility unchanged. Each core ranking, the normalised scores (random assembly = 0, real data = 1) and the anchor check — `LEADERBOARD.md`.

| method | family | core_holdout_clf:rank | core_holdout_clf:p_first | core_holdout_clf:tier | core_holdout_reg:rank | core_holdout_reg:p_first | core_holdout_reg:tier | core_train_clf:rank | core_train_clf:p_first | core_train_clf:tier | core_train_reg:rank | core_train_reg:p_first | core_train_reg:tier | first_in |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| chronos | long-series generator | 7.75 | 0.004 | True | 6.74 | 0.026 | True | 8.28 | 0 | True | 7.27 | 0 | True |  |
| diffusion_ts | long-series generator | 6.43 | 0.055 | True | 5.99 | 0.156 | True | 6.39 | 0.013 | True | 5.95 | 0.054 | True |  |
| timesfm | long-series generator | 7.76 | 0 | True | 5.51 | 0.604 | True | 7.7 | 0 | True | 5.44 | 0.348 | True | core_holdout_reg |
| timestral | long-series generator | 9.5 | 0 | False | 6.95 | 0 | True | 10.6 | 0 | False | 8.01 | 0 | False |  |
| vae_atsp | optimised selection | 7 | 0 | True | 7.49 | 0 | True | 6.77 | 0 | False | 7.27 | 0 | True |  |
| vae_greedy | optimised selection | 7.35 | 0 | True | 7.91 | 0 | True | 7.45 | 0 | False | 8.02 | 0 | False |  |
| vae_herding | optimised selection | 5.39 | 0.749 | True | 6 | 0.112 | True | 4.58 | 0.985 | True | 5.18 | 0.529 | True | core_holdout_clf, core_train_clf, core_train_reg |
| vae_knn | optimised selection | 7.32 | 0 | True | 7.89 | 0 | True | 7.51 | 0 | False | 8.08 | 0 | False |  |
| vae_mbb | optimised selection | 6.94 | 0 | True | 7.69 | 0 | True | 6.82 | 0 | False | 7.58 | 0 | False |  |
| vae_pctsp | optimised selection | 7 | 0 | True | 7.59 | 0 | True | 6.9 | 0 | False | 7.49 | 0 | False |  |
| vae_quilting | optimised selection | 5.86 | 0.183 | True | 6.53 | 0.011 | True | 6.06 | 0 | True | 6.74 | 0 | True |  |
| vae_zseries | optimised selection | 6.41 | 0.009 | True | 6.53 | 0.091 | True | 6.09 | 0.002 | True | 6.22 | 0.069 | True |  |
| vae_rand | random selection | 6.86 | 0 | True | 7.75 | 0 | True | 6.72 | 0 | False | 7.6 | 0 | False |  |


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
| RQ0. Benchmark validity: noise, real-data ceiling, discriminative power and redundancy of the metrics | discriminative metrics: 143 of 297 |
| RQ1. Ranking of every method in every slice | first by ranking: holdout_clf — vae_herding (Friedman p = 0.0177); holdout_reg — timesfm (Friedman p = 0.0329); train_clf — vae_herding (Friedman p = 0.00104); train_reg — timesfm (Friedman p = 0.00177) |
| RQ2. Assembly from a window pool vs long-series generators | inconclusive: 1684 |
| RQ3. Within assembly: window selection × seam processing | same: 599, inconclusive: 2425 |
| RQ4. Does fidelity predict utility (which metrics, against which reference) | predictive pairs: 0 of 956 |
| RQ5. Gap to real data (TSTR / TRTR), stability over time and across models | worse than real: 64 |
| RQ6. Speed and cost: training and generation time, memory, Pareto front "quality × time" | fastest: timestral (7 s) |
| RQ7. Moderators: dataset descriptors and the effects of RQ2 / RQ3 (exploratory) | significant after BH: 0 of 128 |
| RQ8. Class balance: do methods preserve class shares (rare events especially) and what does an error cost | inconclusive: 572 |
| RQ9. Outliers and extremes: do methods preserve tails and outliers, and does it matter to the models | inconclusive: 690 |

## Research questions

### RQ0. Benchmark validity: noise, real-data ceiling, discriminative power and redundancy of the metrics

| unit | kind | group | reference | n_datasets | n_methods | p_friedman | spread_over_noise | p_friedman_bh | discriminative |
|---|---|---|---|---|---|---|---|---|---|
| F1.10_hill_err | fidelity | F1_marginal | val | 9 | 14 | 0.959 | 0.61 | 0.982 | False |
| F1.10_hill_err@oot | fidelity | F1_marginal | oot | 9 | 14 | 0.651 | 1.04 | 0.736 | False |
| F1.10_hill_err@train | fidelity | F1_marginal | train | 9 | 14 | 0.0975 | 0.941 | 0.152 | False |
| F1.1_ks | fidelity | F1_marginal | val | 9 | 14 | 0.365 | 2.33 | 0.457 | False |
| F1.1_ks@oot | fidelity | F1_marginal | oot | 9 | 14 | 0.289 | 1.75 | 0.375 | False |
| F1.1_ks@train | fidelity | F1_marginal | train | 9 | 14 | 6.69e-08 | 2.03 | 9.03e-07 | True |
| F1.2_w1 | fidelity | F1_marginal | val | 9 | 14 | 0.133 | 1.91 | 0.197 | False |
| F1.2_w1@oot | fidelity | F1_marginal | oot | 9 | 14 | 0.927 | 2.16 | 0.969 | False |
| F1.2_w1@train | fidelity | F1_marginal | train | 9 | 14 | 1.55e-05 | 2.26 | 8.83e-05 | True |
| F1.3_ad | fidelity | F1_marginal | val | 9 | 14 | 0.131 | 3.01 | 0.195 | False |
| F1.3_ad@oot | fidelity | F1_marginal | oot | 9 | 14 | 0.684 | 2.21 | 0.761 | False |
| F1.3_ad@train | fidelity | F1_marginal | train | 9 | 14 | 2.6e-06 | 2.65 | 1.98e-05 | True |
| F1.4_qq_corr | fidelity | F1_marginal | val | 9 | 14 | 0.938 | 1.27 | 0.97 | False |
| F1.4_qq_corr@oot | fidelity | F1_marginal | oot | 9 | 14 | 0.238 | 1.24 | 0.316 | False |
| F1.4_qq_corr@train | fidelity | F1_marginal | train | 9 | 14 | 0.101 | 1.26 | 0.155 | False |
| F1.5_q01_err | fidelity | F1_marginal | val | 9 | 14 | 0.053 | 1.56 | 0.0889 | False |
| F1.5_q01_err@oot | fidelity | F1_marginal | oot | 9 | 14 | 0.00105 | 1.56 | 0.00366 | True |
| F1.5_q01_err@train | fidelity | F1_marginal | train | 9 | 14 | 0.00655 | 1.71 | 0.0159 | True |
| F1.5_q99_err | fidelity | F1_marginal | val | 9 | 14 | 0.708 | 2.32 | 0.782 | False |
| F1.5_q99_err@oot | fidelity | F1_marginal | oot | 9 | 14 | 0.00214 | 2.23 | 0.00642 | True |
| F1.5_q99_err@train | fidelity | F1_marginal | train | 9 | 14 | 0.0847 | 2.54 | 0.135 | False |
| F1.5_quantile_err | fidelity | F1_marginal | val | 9 | 14 | 0.249 | 2.54 | 0.328 | False |
| F1.5_quantile_err@oot | fidelity | F1_marginal | oot | 9 | 14 | 0.933 | 1.65 | 0.969 | False |
| F1.5_quantile_err@train | fidelity | F1_marginal | train | 9 | 14 | 2.67e-06 | 2.5 | 1.98e-05 | True |
| F1.6_kurt_err | fidelity | F1_marginal | val | 9 | 14 | 0.66 | 1.09 | 0.743 | False |
| F1.6_kurt_err@oot | fidelity | F1_marginal | oot | 9 | 14 | 0.129 | 1.32 | 0.192 | False |
| F1.6_kurt_err@train | fidelity | F1_marginal | train | 9 | 14 | 0.617 | 1.46 | 0.718 | False |
| F1.6_mean_err | fidelity | F1_marginal | val | 9 | 14 | 0.0836 | 2.1 | 0.133 | False |
| F1.6_mean_err@oot | fidelity | F1_marginal | oot | 9 | 14 | 0.94 | 2.18 | 0.97 | False |
| F1.6_mean_err@train | fidelity | F1_marginal | train | 9 | 14 | 0.00021 | 2.26 | 0.000879 | True |
| F1.6_skew_err | fidelity | F1_marginal | val | 9 | 14 | 0.652 | 1.21 | 0.736 | False |
| F1.6_skew_err@oot | fidelity | F1_marginal | oot | 9 | 14 | 0.0177 | 0.937 | 0.0351 | False |
| F1.6_skew_err@train | fidelity | F1_marginal | train | 9 | 14 | 0.0575 | 1.54 | 0.096 | False |
| F1.6_std_err | fidelity | F1_marginal | val | 9 | 14 | 0.97 | 1.46 | 0.983 | False |
| F1.6_std_err@oot | fidelity | F1_marginal | oot | 9 | 14 | 0.143 | 1.9 | 0.209 | False |
| F1.6_std_err@train | fidelity | F1_marginal | train | 9 | 14 | 0.0768 | 1.98 | 0.125 | False |
| F1.7_out_of_range | fidelity | F1_marginal | val | 9 | 14 | 0.232 | 1.38 | 0.31 | False |
| F1.7_out_of_range@oot | fidelity | F1_marginal | oot | 9 | 14 | 0.0517 | 0.73 | 0.0873 | False |
| F1.7_out_of_range@train | fidelity | F1_marginal | train | 9 | 14 | 0.528 |  | 0.622 | False |
| F1.8_coverage | fidelity | F1_marginal | val | 9 | 14 | 0.00171 | 2.63 | 0.00552 | True |

_Showing 40 rows of 297; all of them — `hypotheses/RQ0_global.parquet`._

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
| fidelity | F5_seams | 0.88 | 0.88 | 0.88 |
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
| F5.3_seam_z_mean | F5.3_seam_z_p95 | 0.938 |
| F1.2_w1 | F1.5_quantile_err | 0.936 |
| F6.4_mmd | F6.4_mmd_2T | 0.929 |
| F1.5_quantile_err | F1.6_mean_err | 0.924 |
| F5.1_ks_seam_vs_real | F5.2_ks_seam_vs_inside | 0.922 |
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
| ranking:holdout_clf | 0.0177 | 5.03 | 9 | 11 | vae_herding |
| with_cost:holdout_clf | 1.7e-06 | 5.03 | 9 | 11 | vae_quilting |
| ranking:holdout_reg | 0.0329 | 5.03 | 9 | 11 | timesfm |
| with_cost:holdout_reg | 1.48e-06 | 5.03 | 9 | 11 | timesfm |
| ranking:train_clf | 0.00104 | 5.03 | 9 | 11 | vae_herding |
| with_cost:train_clf | 8.49e-07 | 5.03 | 9 | 11 | vae_quilting |
| ranking:train_reg | 0.00177 | 5.03 | 9 | 11 | timesfm |
| with_cost:train_reg | 2.83e-06 | 5.03 | 9 | 11 | timesfm |
| ranking:core_holdout_clf | 0.00111 | 5.03 | 9 | 11 | vae_herding |
| ranking:core_holdout_reg | 0.0291 | 5.03 | 9 | 11 | timesfm |
| ranking:core_train_clf | 1.54e-05 | 5.03 | 9 | 11 | vae_herding |
| ranking:core_train_reg | 0.000676 | 5.03 | 9 | 11 | vae_herding |
| domain:fidelity@train | 3.32e-06 | 5.03 | 9 | 11 | vae_zseries |
| domain:fidelity@val | 0.0406 | 5.03 | 9 | 11 | diffusion_ts |
| domain:fidelity@oot | 0.00114 | 5.03 | 9 | 11 | vae_quilting |
| domain:fidelity@all | 0.000671 | 5.03 | 9 | 11 | vae_zseries |
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
| fidelity:seams@oot | 4.47e-11 | 5.03 | 9 | 11 | vae_quilting |
| fidelity:seams@train | 3.84e-11 | 5.03 | 9 | 11 | vae_quilting |
| fidelity:seams@val | 1.58e-11 | 5.03 | 9 | 11 | vae_quilting |
| fidelity:target@oot | 0.0105 | 5.03 | 9 | 11 | vae_herding |
| fidelity:target@train | 0.000931 | 5.03 | 9 | 11 | vae_zseries |
| fidelity:target@val | 0.00139 | 5.03 | 9 | 11 | vae_herding |
| fidelity:windows@oot | 0.00893 | 5.03 | 9 | 11 | vae_zseries |

_Showing 40 rows of 56; all of them — `hypotheses/RQ1_global.parquet`._

**ranking_holdout_clf**

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| vae_herding | optimised selection | 5.95 | 5.43 | 6.42 | 0.319 | 0.971 |  | True |
| vae_quilting | optimised selection | 5.98 | 5.44 | 6.58 | 0.387 | 0.904 | 0.734 | True |
| diffusion_ts | long-series generator | 6.23 | 4.82 | 7.49 | 0.264 | 0.603 | 0.734 | True |
| vae_zseries | optimised selection | 6.52 | 5.89 | 7.16 | 0.007 | 0.35 | 0.602 | True |
| vae_pctsp | optimised selection | 6.86 | 6.42 | 7.34 | 0 | 0.005 | 0.176 | True |
| vae_atsp | optimised selection | 6.89 | 6.35 | 7.56 | 0 | 0.013 | 0.219 | True |
| vae_rand | random selection | 7.09 | 6.33 | 7.83 | 0.001 | 0.026 | 0.219 | True |
| vae_mbb | optimised selection | 7.12 | 6.39 | 7.81 | 0 | 0.007 | 0.223 | True |
| vae_greedy | optimised selection | 7.14 | 6.69 | 7.62 | 0 | 0 | 0.117 | True |
| vae_knn | optimised selection | 7.19 | 6.73 | 7.69 | 0 | 0 | 0.137 | True |
| timesfm | long-series generator | 7.57 | 5.74 | 9.41 | 0.012 | 0.077 | 0.656 | True |
| chronos | long-series generator | 7.65 | 6.04 | 9.11 | 0.01 | 0.044 | 0.391 | True |
| timestral | long-series generator | 9.12 | 8.02 | 10.1 | 0 | 0 | 0.117 | True |


**ranking_holdout_reg**

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| timesfm | long-series generator | 5.32 | 3.83 | 7.08 | 0.716 | 0.933 |  | True |
| diffusion_ts | long-series generator | 5.79 | 4.6 | 6.88 | 0.211 | 0.852 | 0.781 | True |
| vae_herding | optimised selection | 6.55 | 5.64 | 7.4 | 0.004 | 0.346 | 0.781 | True |
| timestral | long-series generator | 6.57 | 5.56 | 7.54 | 0.001 | 0.266 | 0.781 | True |
| chronos | long-series generator | 6.65 | 5.29 | 7.83 | 0.012 | 0.257 | 0.781 | True |
| vae_zseries | optimised selection | 6.65 | 5.9 | 7.41 | 0.054 | 0.217 | 0.781 | True |
| vae_quilting | optimised selection | 6.65 | 6.17 | 7.18 | 0.002 | 0.12 | 0.781 | True |
| vae_atsp | optimised selection | 7.39 | 6.85 | 8.03 | 0 | 0.003 | 0.781 | True |
| vae_pctsp | optimised selection | 7.45 | 7.04 | 7.89 | 0 | 0.002 | 0.781 | True |
| vae_greedy | optimised selection | 7.71 | 7.25 | 8.19 | 0 | 0 | 0.781 | True |
| vae_knn | optimised selection | 7.76 | 7.23 | 8.26 | 0 | 0 | 0.781 | True |
| vae_mbb | optimised selection | 7.87 | 7.11 | 8.52 | 0 | 0 | 0.562 | True |
| vae_rand | random selection | 7.98 | 7.1 | 8.72 | 0 | 0.004 | 0.562 | True |


**ranking_train_clf**

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| vae_herding | optimised selection | 5.47 | 5.09 | 5.86 | 0.701 | 0.997 |  | True |
| vae_quilting | optimised selection | 6.05 | 5.34 | 6.76 | 0.105 | 0.761 | 0.539 | True |
| diffusion_ts | long-series generator | 6.13 | 4.63 | 7.48 | 0.181 | 0.573 | 0.539 | True |
| vae_zseries | optimised selection | 6.21 | 5.49 | 6.97 | 0.011 | 0.535 | 0.406 | True |
| vae_atsp | optimised selection | 6.8 | 6.19 | 7.5 | 0 | 0.029 | 0.0352 | False |
| vae_pctsp | optimised selection | 6.84 | 6.32 | 7.37 | 0 | 0 | 0.0352 | False |
| vae_rand | random selection | 7.04 | 6.32 | 7.75 | 0 | 0.017 | 0.0352 | False |
| vae_mbb | optimised selection | 7.07 | 6.37 | 7.75 | 0 | 0.005 | 0.0352 | False |
| vae_greedy | optimised selection | 7.25 | 6.81 | 7.73 | 0 | 0 | 0.0234 | False |
| vae_knn | optimised selection | 7.3 | 6.91 | 7.74 | 0 | 0 | 0.0234 | False |
| timesfm | long-series generator | 7.56 | 5.82 | 9.44 | 0.002 | 0.073 | 0.539 | True |
| chronos | long-series generator | 8.06 | 6.48 | 9.49 | 0 | 0.01 | 0.195 | True |
| timestral | long-series generator | 9.68 | 8.51 | 10.7 | 0 | 0 | 0.0234 | False |


**ranking_train_reg**

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| timesfm | long-series generator | 5.31 | 3.89 | 6.85 | 0.642 | 0.906 |  | True |
| diffusion_ts | long-series generator | 5.69 | 4.47 | 6.79 | 0.244 | 0.835 | 0.781 | True |
| vae_herding | optimised selection | 6.07 | 5.44 | 6.68 | 0.015 | 0.732 | 0.781 | True |
| vae_zseries | optimised selection | 6.34 | 5.51 | 7.21 | 0.098 | 0.358 | 0.781 | True |
| vae_quilting | optimised selection | 6.73 | 6.11 | 7.32 | 0.001 | 0.053 | 0.781 | True |
| chronos | long-series generator | 7.05 | 5.79 | 8.19 | 0 | 0.066 | 0.781 | True |
| timestral | long-series generator | 7.13 | 6.08 | 8.1 | 0 | 0.046 | 0.188 | True |
| vae_atsp | optimised selection | 7.29 | 6.62 | 7.98 | 0 | 0.003 | 0.547 | True |
| vae_pctsp | optimised selection | 7.43 | 6.94 | 7.91 | 0 | 0 | 0.547 | True |
| vae_greedy | optimised selection | 7.81 | 7.42 | 8.22 | 0 | 0 | 0.516 | True |
| vae_mbb | optimised selection | 7.83 | 7.13 | 8.46 | 0 | 0 | 0.516 | True |
| vae_knn | optimised selection | 7.87 | 7.44 | 8.3 | 0 | 0 | 0.516 | True |
| vae_rand | random selection | 7.93 | 7.1 | 8.64 | 0 | 0.001 | 0.516 | True |


**ranking_core_holdout_clf**

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| vae_herding | optimised selection | 5.39 | 4.73 | 6.03 | 0.749 | 0.997 |  | True |
| vae_quilting | optimised selection | 5.86 | 5.28 | 6.49 | 0.183 | 0.92 | 0.326 | True |
| vae_zseries | optimised selection | 6.41 | 5.66 | 7.2 | 0.009 | 0.46 | 0.246 | True |
| diffusion_ts | long-series generator | 6.43 | 4.74 | 7.87 | 0.055 | 0.484 | 0.246 | True |
| vae_rand | random selection | 6.86 | 6.11 | 7.59 | 0 | 0.052 | 0.137 | True |
| vae_mbb | optimised selection | 6.94 | 6.21 | 7.64 | 0 | 0.019 | 0.109 | True |
| vae_atsp | optimised selection | 7 | 6.46 | 7.65 | 0 | 0.001 | 0.137 | True |
| vae_pctsp | optimised selection | 7 | 6.5 | 7.53 | 0 | 0 | 0.0879 | True |
| vae_knn | optimised selection | 7.32 | 6.79 | 7.9 | 0 | 0 | 0.0645 | True |
| vae_greedy | optimised selection | 7.35 | 6.84 | 7.88 | 0 | 0 | 0.0645 | True |
| chronos | long-series generator | 7.75 | 6.22 | 9.14 | 0.004 | 0.031 | 0.219 | True |
| timesfm | long-series generator | 7.76 | 6.1 | 9.54 | 0 | 0.036 | 0.156 | True |
| timestral | long-series generator | 9.5 | 8.26 | 10.6 | 0 | 0 | 0.0234 | False |


**ranking_core_holdout_reg**

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| timesfm | long-series generator | 5.51 | 4.12 | 7.19 | 0.604 | 0.895 |  | True |
| diffusion_ts | long-series generator | 5.99 | 4.54 | 7.3 | 0.156 | 0.68 | 0.562 | True |
| vae_herding | optimised selection | 6 | 4.94 | 7.05 | 0.112 | 0.697 | 0.625 | True |
| vae_zseries | optimised selection | 6.53 | 5.68 | 7.42 | 0.091 | 0.273 | 0.938 | True |
| vae_quilting | optimised selection | 6.53 | 6 | 7.13 | 0.011 | 0.204 | 0.938 | True |
| chronos | long-series generator | 6.74 | 5.52 | 7.87 | 0.026 | 0.156 | 0.938 | True |
| timestral | long-series generator | 6.95 | 5.81 | 8.05 | 0 | 0.084 | 0.562 | True |
| vae_atsp | optimised selection | 7.49 | 6.92 | 8.11 | 0 | 0 | 0.562 | True |
| vae_pctsp | optimised selection | 7.59 | 7.11 | 8.07 | 0 | 0.002 | 0.562 | True |
| vae_mbb | optimised selection | 7.69 | 6.96 | 8.36 | 0 | 0.003 | 0.562 | True |
| vae_rand | random selection | 7.75 | 6.88 | 8.54 | 0 | 0.006 | 0.562 | True |
| vae_knn | optimised selection | 7.89 | 7.31 | 8.43 | 0 | 0 | 0.562 | True |
| vae_greedy | optimised selection | 7.91 | 7.37 | 8.47 | 0 | 0 | 0.562 | True |


**ranking_core_train_clf**

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| vae_herding | optimised selection | 4.58 | 4.15 | 4.95 | 0.985 | 1 |  | True |
| vae_quilting | optimised selection | 6.06 | 5.3 | 6.83 | 0 | 0.711 | 0.0781 | True |
| vae_zseries | optimised selection | 6.09 | 5.26 | 6.96 | 0.002 | 0.66 | 0.0781 | True |
| diffusion_ts | long-series generator | 6.39 | 4.58 | 7.94 | 0.013 | 0.435 | 0.0781 | True |
| vae_rand | random selection | 6.72 | 6.02 | 7.41 | 0 | 0.058 | 0.0234 | False |
| vae_atsp | optimised selection | 6.77 | 6.05 | 7.51 | 0 | 0.064 | 0.0234 | False |
| vae_mbb | optimised selection | 6.82 | 6.18 | 7.45 | 0 | 0.015 | 0.0234 | False |
| vae_pctsp | optimised selection | 6.9 | 6.28 | 7.52 | 0 | 0 | 0.0234 | False |
| vae_greedy | optimised selection | 7.45 | 6.97 | 7.96 | 0 | 0 | 0.0234 | False |
| vae_knn | optimised selection | 7.51 | 7.03 | 8.06 | 0 | 0 | 0.0234 | False |
| timesfm | long-series generator | 7.7 | 6.07 | 9.52 | 0 | 0.053 | 0.0781 | True |
| chronos | long-series generator | 8.28 | 6.81 | 9.66 | 0 | 0.004 | 0.0781 | True |
| timestral | long-series generator | 10.6 | 9.21 | 11.6 | 0 | 0 | 0.0234 | False |


**ranking_core_train_reg**

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| vae_herding | optimised selection | 5.18 | 4.42 | 5.89 | 0.529 | 1 |  | True |
| timesfm | long-series generator | 5.44 | 4.16 | 6.89 | 0.348 | 0.866 | 0.422 | True |
| diffusion_ts | long-series generator | 5.95 | 4.42 | 7.29 | 0.054 | 0.648 | 0.305 | True |
| vae_zseries | optimised selection | 6.22 | 5.27 | 7.22 | 0.069 | 0.411 | 0.305 | True |
| vae_quilting | optimised selection | 6.74 | 6.07 | 7.39 | 0 | 0.05 | 0.0977 | True |
| vae_atsp | optimised selection | 7.27 | 6.46 | 7.99 | 0 | 0.008 | 0.0586 | True |
| chronos | long-series generator | 7.27 | 6.16 | 8.3 | 0 | 0.013 | 0.156 | True |
| vae_pctsp | optimised selection | 7.49 | 6.95 | 8.04 | 0 | 0 | 0.0234 | False |
| vae_mbb | optimised selection | 7.58 | 6.92 | 8.15 | 0 | 0 | 0.0352 | False |
| vae_rand | random selection | 7.6 | 6.7 | 8.43 | 0 | 0.004 | 0.0352 | False |
| timestral | long-series generator | 8.01 | 6.88 | 8.97 | 0 | 0 | 0.0352 | False |
| vae_greedy | optimised selection | 8.02 | 7.62 | 8.44 | 0 | 0 | 0.0234 | False |
| vae_knn | optimised selection | 8.08 | 7.61 | 8.57 | 0 | 0 | 0.0234 | False |


**rankings**

| family | holdout_clf:rank | holdout_clf:p_first | holdout_clf:tier | holdout_reg:rank | holdout_reg:p_first | holdout_reg:tier | train_clf:rank | train_clf:p_first | train_clf:tier | train_reg:rank | train_reg:p_first | train_reg:tier | first_in |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| long-series generator | 7.65 | 0.01 | True | 6.65 | 0.012 | True | 8.06 | 0 | True | 7.05 | 0 | True |  |
| long-series generator | 6.23 | 0.264 | True | 5.79 | 0.211 | True | 6.13 | 0.181 | True | 5.69 | 0.244 | True |  |
| long-series generator | 7.57 | 0.012 | True | 5.32 | 0.716 | True | 7.56 | 0.002 | True | 5.31 | 0.642 | True | holdout_reg, train_reg |
| long-series generator | 9.12 | 0 | True | 6.57 | 0.001 | True | 9.68 | 0 | False | 7.13 | 0 | True |  |
| optimised selection | 6.89 | 0 | True | 7.39 | 0 | True | 6.8 | 0 | False | 7.29 | 0 | True |  |
| optimised selection | 7.14 | 0 | True | 7.71 | 0 | True | 7.25 | 0 | False | 7.81 | 0 | True |  |
| optimised selection | 5.95 | 0.319 | True | 6.55 | 0.004 | True | 5.47 | 0.701 | True | 6.07 | 0.015 | True | holdout_clf, train_clf |
| optimised selection | 7.19 | 0 | True | 7.76 | 0 | True | 7.3 | 0 | False | 7.87 | 0 | True |  |
| optimised selection | 7.12 | 0 | True | 7.87 | 0 | True | 7.07 | 0 | False | 7.83 | 0 | True |  |
| optimised selection | 6.86 | 0 | True | 7.45 | 0 | True | 6.84 | 0 | False | 7.43 | 0 | True |  |
| optimised selection | 5.98 | 0.387 | True | 6.65 | 0.002 | True | 6.05 | 0.105 | True | 6.73 | 0.001 | True |  |
| optimised selection | 6.52 | 0.007 | True | 6.65 | 0.054 | True | 6.21 | 0.011 | True | 6.34 | 0.098 | True |  |
| random selection | 7.09 | 0.001 | True | 7.98 | 0 | True | 7.04 | 0 | False | 7.93 | 0 | True |  |


**rankings_core**

| family | core_holdout_clf:rank | core_holdout_clf:p_first | core_holdout_clf:tier | core_holdout_reg:rank | core_holdout_reg:p_first | core_holdout_reg:tier | core_train_clf:rank | core_train_clf:p_first | core_train_clf:tier | core_train_reg:rank | core_train_reg:p_first | core_train_reg:tier | first_in |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| long-series generator | 7.75 | 0.004 | True | 6.74 | 0.026 | True | 8.28 | 0 | True | 7.27 | 0 | True |  |
| long-series generator | 6.43 | 0.055 | True | 5.99 | 0.156 | True | 6.39 | 0.013 | True | 5.95 | 0.054 | True |  |
| long-series generator | 7.76 | 0 | True | 5.51 | 0.604 | True | 7.7 | 0 | True | 5.44 | 0.348 | True | core_holdout_reg |
| long-series generator | 9.5 | 0 | False | 6.95 | 0 | True | 10.6 | 0 | False | 8.01 | 0 | False |  |
| optimised selection | 7 | 0 | True | 7.49 | 0 | True | 6.77 | 0 | False | 7.27 | 0 | True |  |
| optimised selection | 7.35 | 0 | True | 7.91 | 0 | True | 7.45 | 0 | False | 8.02 | 0 | False |  |
| optimised selection | 5.39 | 0.749 | True | 6 | 0.112 | True | 4.58 | 0.985 | True | 5.18 | 0.529 | True | core_holdout_clf, core_train_clf, core_train_reg |
| optimised selection | 7.32 | 0 | True | 7.89 | 0 | True | 7.51 | 0 | False | 8.08 | 0 | False |  |
| optimised selection | 6.94 | 0 | True | 7.69 | 0 | True | 6.82 | 0 | False | 7.58 | 0 | False |  |
| optimised selection | 7 | 0 | True | 7.59 | 0 | True | 6.9 | 0 | False | 7.49 | 0 | False |  |
| optimised selection | 5.86 | 0.183 | True | 6.53 | 0.011 | True | 6.06 | 0 | True | 6.74 | 0 | True |  |
| optimised selection | 6.41 | 0.009 | True | 6.53 | 0.091 | True | 6.09 | 0.002 | True | 6.22 | 0.069 | True |  |
| random selection | 6.86 | 0 | True | 7.75 | 0 | True | 6.72 | 0 | False | 7.6 | 0 | False |  |


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
| diffusion_ts vs vae_rand | utility | clf_down_h24_q10\|gbdt\|S\|val\|auc | 9 | 0.865 | 1.83 | 0.593 | 3.44 | 0.117 | 1 | 1 | 4 | 0 | 0 | inconclusive |
| diffusion_ts vs vae_rand | utility | reg_h168\|linear\|S\|val\|mase | 9 | 3.9 | 3.65 | 2.56 | 4.73 | 0.117 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| timestral vs vae_rand | utility | ms_h24\|linear\|S\|val\|mase | 9 | 3.07 | 3.61 | 1.9 | 5.7 | 0.117 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| timestral vs vae_rand | utility | reg_h168\|gbdt\|S\|val\|mase | 9 | 2.89 | 3.43 | 2.47 | 4.53 | 0.117 | 1 | 1 | 8 | 0 | 0 | inconclusive |
| timestral vs vae_rand | utility | reg_h168\|linear\|S\|val\|mase | 9 | 4.06 | 4.16 | 2.99 | 5.22 | 0.117 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| timestral vs vae_rand | utility | reg_h24\|gbdt\|S\|val\|mase | 9 | 5.32 | 6.22 | 3.47 | 9.17 | 0.117 | 1 | 1 | 8 | 0 | 0 | inconclusive |
| timestral vs vae_rand | utility | reg_h24\|linear\|S\|val\|mase | 9 | 4.24 | 4.9 | 3.55 | 6.33 | 0.117 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| timestral vs assembly_median | utility | reg_h168\|gbdt\|S\|oot\|mase | 9 | 6.42 | 5.84 | 3.29 | 8.63 | 0.117 | 1 | 1 | 8 | 0 | 0 | inconclusive |
| timestral vs assembly_median | utility | reg_h168\|gbdt\|S\|val\|mase | 9 | 6 | 7.29 | 3.67 | 12 | 0.117 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| timestral vs assembly_median | utility | reg_h168\|linear\|S\|val\|mase | 9 | 6.06 | 6.04 | 3.57 | 8.79 | 0.117 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| timestral vs assembly_median | utility | reg_h24\|linear\|S\|oot\|mase | 9 | 5.68 | 6.7 | 4.18 | 9.91 | 0.117 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| timestral vs assembly_median | utility | reg_h24\|linear\|S\|val\|mase | 9 | 6.7 | 10 | 5.97 | 15.7 | 0.117 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| diffusion_ts vs vae_rand | fidelity | F5.3_seam_z_mean | 9 | 4.1 | 4.69 | 3.64 | 6.16 | 0.117 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| diffusion_ts vs vae_rand | fidelity | F5.3_seam_z_mean@oot | 9 | 4.1 | 4.69 | 3.64 | 6.16 | 0.117 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| diffusion_ts vs vae_rand | fidelity | F5.3_seam_z_p95 | 9 | 5.03 | 5.95 | 4.08 | 7.96 | 0.117 | 1 | 1 | 8 | 0 | 0 | inconclusive |
| diffusion_ts vs vae_rand | fidelity | F5.3_seam_z_p95@oot | 9 | 5.03 | 5.95 | 4.08 | 7.96 | 0.117 | 1 | 1 | 8 | 0 | 0 | inconclusive |
| diffusion_ts vs vae_rand | fidelity | F5.4_seam_local_acf | 9 | 1.07 | 1.47 | 0.759 | 2.3 | 0.117 | 1 | 1 | 5 | 0 | 0 | inconclusive |
| diffusion_ts vs vae_rand | fidelity | F5.4_seam_local_acf@oot | 9 | 1.07 | 1.47 | 0.759 | 2.3 | 0.117 | 1 | 1 | 5 | 0 | 0 | inconclusive |
| timestral vs vae_rand | fidelity | F3.8_calendar_corr_err@oot | 9 | 3.09 | 6.05 | 2.3 | 11.4 | 0.117 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| timestral vs vae_rand | fidelity | F5.3_seam_z_mean | 9 | 5.97 | 7.04 | 5.31 | 8.84 | 0.117 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| timestral vs vae_rand | fidelity | F5.3_seam_z_mean@oot | 9 | 5.97 | 7.04 | 5.31 | 8.84 | 0.117 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| timestral vs vae_rand | fidelity | F5.3_seam_z_p95 | 9 | 7.52 | 9.98 | 6.77 | 14 | 0.117 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| timestral vs vae_rand | fidelity | F5.3_seam_z_p95@oot | 9 | 7.52 | 9.98 | 6.77 | 14 | 0.117 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| timestral vs vae_rand | fidelity | F6.1_disc_score | 9 | 0.6 | 1.13 | 0.493 | 1.88 | 0.117 | 1 | 1 | 2 | 0 | 0 | inconclusive |
| timestral vs vae_rand | fidelity | F8.4_event_by_how | 9 | 7.79 | 7.27 | 4.19 | 10.7 | 0.117 | 1 | 1 | 8 | 0 | 0 | inconclusive |
| timestral vs assembly_median | fidelity | F3.8_calendar_corr_err | 9 | 4.76 | 6.74 | 2.97 | 11.2 | 0.117 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| timestral vs assembly_median | fidelity | F3.8_calendar_corr_err@oot | 9 | 7.75 | 7.9 | 4.65 | 11.7 | 0.117 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| timestral vs assembly_median | fidelity | F8.4_event_by_how | 9 | 9.63 | 11.4 | 5.8 | 18.4 | 0.117 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| diffusion_ts vs vae_rand | utility | reg_h168\|gbdt\|S\|oot\|mase | 9 | 3.14 | 3.85 | 2.1 | 5.92 | 0.157 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| diffusion_ts vs vae_rand | utility | reg_h168\|gbdt\|S\|val\|mase | 9 | 2.95 | 2.62 | 1.41 | 3.91 | 0.157 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| diffusion_ts vs vae_rand | utility | reg_h168\|linear\|S\|oot\|mase | 9 | 4.11 | 4.4 | 2.83 | 5.92 | 0.157 | 1 | 1 | 8 | 0 | 0 | inconclusive |
| diffusion_ts vs vae_rand | utility | reg_h24\|gbdt\|S\|oot\|mase | 9 | 2.48 | 2.45 | 1.44 | 3.48 | 0.157 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| diffusion_ts vs assembly_median | utility | reg_h168\|gbdt\|S\|oot\|mase | 9 | 4.03 | 4.37 | 2.78 | 5.84 | 0.157 | 1 | 1 | 8 | 0 | 0 | inconclusive |
| diffusion_ts vs assembly_median | utility | reg_h168\|gbdt\|S\|val\|mase | 9 | 2.91 | 3.45 | 1.79 | 5.17 | 0.157 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| diffusion_ts vs assembly_median | utility | reg_h168\|linear\|S\|oot\|mase | 9 | 5.04 | 5.01 | 2.98 | 7.05 | 0.157 | 1 | 1 | 8 | 0 | 0 | inconclusive |
| diffusion_ts vs assembly_median | utility | reg_h168\|linear\|S\|val\|mase | 9 | 4.63 | 5.2 | 2.56 | 8.19 | 0.157 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| timestral vs vae_rand | utility | reg_h168\|gbdt\|S\|oot\|mase | 9 | 3.48 | 4.06 | 2.14 | 6.29 | 0.157 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| timestral vs vae_rand | utility | reg_h24\|gbdt\|S\|oot\|mase | 9 | 5.38 | 4.76 | 2.92 | 6.53 | 0.157 | 1 | 1 | 8 | 0 | 0 | inconclusive |
| timestral vs assembly_median | utility | ms_h24\|linear\|S\|val\|mase | 9 | 6.08 | 6.96 | 3.52 | 10.5 | 0.157 | 1 | 1 | 8 | 1 | 0 | inconclusive |
| diffusion_ts vs vae_rand | fidelity | F5.1_ks_seam_vs_real@oot | 9 | 1.07 | 1.41 | 0.588 | 2.33 | 0.157 | 1 | 1 | 4 | 0 | 0 | inconclusive |

_Showing 40 rows of 1684 (rows with a better / worse / same verdict first); all of them — `hypotheses/RQ2_global.parquet`._

### RQ3. Within assembly: window selection × seam processing

| comparison | kind | unit | n_datasets | median_z | mean_z | ci_lo | ci_hi | p_better_adj | p_worse_adj | p_equiv_adj | n_better | n_worse | n_same | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| seams: vae_zseries_quilt vs vae_zseries | fidelity | F4.1_how_mean@oot | 9 | -0.261 | -0.312 | -0.608 | -0.107 | 1 | 0.0628 | 0.024 | 0 | 0 | 6 | same |
| seams: vae_zseries_xfade vs vae_zseries | fidelity | F1.6_std_err@oot | 9 | -0.241 | -0.321 | -0.542 | -0.105 | 1 | 0.0628 | 0.024 | 0 | 0 | 6 | same |
| seams: vae_zseries_xfade vs vae_zseries | fidelity | F4.1_how_mean@oot | 9 | -0.34 | -0.442 | -0.737 | -0.198 | 1 | 0.0628 | 0.0275 | 0 | 0 | 6 | same |
| main effect: seams crossfade vs none | fidelity | F1.6_std_err@oot | 9 | -0.241 | -0.321 | -0.542 | -0.105 | 1 | 0.0628 | 0.024 | 0 | 0 | 6 | same |
| main effect: seams crossfade vs none | fidelity | F4.1_how_mean@oot | 9 | -0.34 | -0.442 | -0.737 | -0.198 | 1 | 0.0628 | 0.0275 | 0 | 0 | 6 | same |
| main effect: seams quilt vs none | fidelity | F4.1_how_mean@oot | 9 | -0.261 | -0.312 | -0.608 | -0.107 | 1 | 0.0628 | 0.024 | 0 | 0 | 6 | same |
| selection: vae_mbb vs vae_rand | fidelity | F2.4_big_jump_share_err | 9 | -0.45 | -0.482 | -0.779 | -0.167 | 1 | 0.0856 | 0.024 | 0 | 0 | 0 | same |
| seams: vae_zseries_xfade vs vae_zseries | fidelity | F4.3_hod_mean@oot | 9 | -0.347 | -0.343 | -0.58 | -0.148 | 1 | 0.0856 | 0.024 | 0 | 0 | 6 | same |
| main effect: seams crossfade vs none | fidelity | F4.3_hod_mean@oot | 9 | -0.347 | -0.343 | -0.58 | -0.148 | 1 | 0.0856 | 0.024 | 0 | 0 | 6 | same |
| seams: vae_zseries_wsola vs vae_zseries | fidelity | F11.3_multiclass_tvd | 9 | -0.262 | -0.293 | -0.607 | -0.0249 | 1 | 0.1 | 0.024 | 0 | 0 | 4 | same |
| main effect: seams wsola vs none | fidelity | F11.3_multiclass_tvd | 9 | -0.262 | -0.293 | -0.607 | -0.0249 | 1 | 0.1 | 0.024 | 0 | 0 | 4 | same |
| selection: vae_mbb vs vae_rand | fidelity | F2.4_big_jump_share_err@oot | 9 | -0.357 | -0.342 | -0.867 | 0.231 | 1 | 0.118 | 0.0275 | 0 | 0 | 1 | same |
| selection: vae_mbb vs vae_rand | fidelity | F3.3_pacf | 9 | -0.394 | -0.404 | -1.03 | 0.0795 | 1 | 0.118 | 0.0275 | 0 | 0 | 1 | same |
| selection: vae_mbb vs vae_rand | fidelity | F8.4_event_by_how@oot | 9 | -0.208 | -0.323 | -0.672 | 0.011 | 1 | 0.118 | 0.0275 | 0 | 0 | 0 | same |
| seams: vae_zseries_quilt vs vae_zseries | fidelity | F1.9_js@oot | 9 | -0.474 | -0.428 | -0.772 | -0.154 | 1 | 0.118 | 0.0275 | 0 | 0 | 3 | same |
| seams: vae_zseries_quilt vs vae_zseries | fidelity | F2.4_big_jump_share_err@oot | 9 | -0.233 | -0.35 | -0.712 | 0.0139 | 1 | 0.118 | 0.0493 | 0 | 1 | 3 | same |
| seams: vae_zseries_wsola vs vae_zseries | fidelity | F12.3_spike_rate_err | 8 | -0.346 | -0.424 | -0.907 | -0.041 | 1 | 0.118 | 0.0448 | 0 | 0 | 1 | same |
| main effect: seams quilt vs none | fidelity | F1.9_js@oot | 9 | -0.474 | -0.428 | -0.772 | -0.154 | 1 | 0.118 | 0.0275 | 0 | 0 | 3 | same |
| main effect: seams quilt vs none | fidelity | F2.4_big_jump_share_err@oot | 9 | -0.233 | -0.35 | -0.712 | 0.0139 | 1 | 0.118 | 0.0493 | 0 | 1 | 3 | same |
| main effect: seams wsola vs none | fidelity | F12.3_spike_rate_err | 8 | -0.346 | -0.424 | -0.907 | -0.041 | 1 | 0.118 | 0.0448 | 0 | 0 | 1 | same |
| seams: vae_zseries_wsola vs vae_zseries | fidelity | F8.1_class_tvd | 9 | -0.415 | -0.287 | -0.561 | 0.00605 | 1 | 0.141 | 0.024 | 0 | 0 | 3 | same |
| main effect: seams wsola vs none | fidelity | F8.1_class_tvd | 9 | -0.415 | -0.287 | -0.561 | 0.00605 | 1 | 0.141 | 0.024 | 0 | 0 | 3 | same |
| seams: vae_zseries_xfade vs vae_zseries | fidelity | F1.10_hill_err | 9 | -0.179 | -0.281 | -0.585 | -0.0372 | 1 | 0.167 | 0.0275 | 0 | 0 | 6 | same |
| seams: vae_zseries_xfade vs vae_zseries | fidelity | F1.1_ks | 9 | -0.22 | -0.234 | -0.483 | 0.00211 | 1 | 0.167 | 0.024 | 0 | 0 | 5 | same |
| main effect: seams crossfade vs none | fidelity | F1.10_hill_err | 9 | -0.179 | -0.281 | -0.585 | -0.0372 | 1 | 0.167 | 0.0275 | 0 | 0 | 6 | same |
| main effect: seams crossfade vs none | fidelity | F1.1_ks | 9 | -0.22 | -0.234 | -0.483 | 0.00211 | 1 | 0.167 | 0.024 | 0 | 0 | 5 | same |
| selection: vae_mbb vs vae_rand | fidelity | F10.1_dcr_logratio | 9 | 0.535 | 0.495 | -0.0158 | 0.98 | 0.2 | 1 | 0.0493 | 0 | 0 | 0 | same |
| seams: vae_zseries_quilt vs vae_zseries | fidelity | F1.10_hill_err | 9 | -0.249 | -0.24 | -0.465 | -0.0383 | 1 | 0.204 | 0.024 | 0 | 0 | 6 | same |
| seams: vae_zseries_quilt vs vae_zseries | fidelity | F1.10_hill_err@oot | 9 | -0.462 | -0.308 | -0.577 | -0.0457 | 1 | 0.204 | 0.024 | 0 | 0 | 2 | same |
| seams: vae_zseries_wsola vs vae_zseries | fidelity | F1.10_hill_err | 9 | -0.216 | -0.257 | -0.536 | -0.0198 | 1 | 0.204 | 0.024 | 0 | 0 | 5 | same |
| main effect: seams quilt vs none | fidelity | F1.10_hill_err | 9 | -0.249 | -0.24 | -0.465 | -0.0383 | 1 | 0.204 | 0.024 | 0 | 0 | 6 | same |
| main effect: seams quilt vs none | fidelity | F1.10_hill_err@oot | 9 | -0.462 | -0.308 | -0.577 | -0.0457 | 1 | 0.204 | 0.024 | 0 | 0 | 2 | same |
| main effect: seams wsola vs none | fidelity | F1.10_hill_err | 9 | -0.216 | -0.257 | -0.536 | -0.0198 | 1 | 0.204 | 0.024 | 0 | 0 | 5 | same |
| seams: vae_zseries_quilt vs vae_zseries | fidelity | F4.3_hod_mean@oot | 9 | -0.228 | -0.209 | -0.457 | 0.0044 | 1 | 0.242 | 0.024 | 0 | 0 | 6 | same |
| seams: vae_zseries_xfade vs vae_zseries | fidelity | F1.5_q99_err | 9 | -0.121 | -0.166 | -0.424 | 0.0561 | 1 | 0.242 | 0.024 | 0 | 0 | 6 | same |
| seams: vae_zseries_xfade vs vae_zseries | fidelity | F4.1_how_mean | 9 | -0.288 | -0.287 | -0.576 | -0.017 | 1 | 0.242 | 0.024 | 0 | 0 | 6 | same |
| main effect: seams crossfade vs none | fidelity | F1.5_q99_err | 9 | -0.121 | -0.166 | -0.424 | 0.0561 | 1 | 0.242 | 0.024 | 0 | 0 | 6 | same |
| main effect: seams crossfade vs none | fidelity | F4.1_how_mean | 9 | -0.288 | -0.287 | -0.576 | -0.017 | 1 | 0.242 | 0.024 | 0 | 0 | 6 | same |
| main effect: seams quilt vs none | fidelity | F4.3_hod_mean@oot | 9 | -0.228 | -0.209 | -0.457 | 0.0044 | 1 | 0.242 | 0.024 | 0 | 0 | 6 | same |
| seams: vae_zseries_xfade vs vae_zseries | fidelity | F7.4_excursion_ks@oot | 8 | -0.368 | -0.4 | -0.771 | -0.0247 | 1 | 0.247 | 0.0275 | 0 | 0 | 2 | same |

_Showing 40 rows of 3024 (rows with a better / worse / same verdict first); all of them — `hypotheses/RQ3_global.parquet`._

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
| F3.1_acf_in_window@train | F3.1_acf_in_window | train | F3_dependence | regression@val | 9 | 0.809 | 0.667 | 0.0547 | 0.177 | False |
| F3.2_acf_beyond_window@train | F3.2_acf_beyond_window | train | F3_dependence | regression@val | 9 | 0.779 | 0.667 | 0.0977 | 0.243 | False |
| F3.1_acf_in_window@oot | F3.1_acf_in_window | oot | F3_dependence | regression@oot | 9 | 0.732 | 1 | 0.00391 | 0.0549 | False |
| F3.1_acf_in_window | F3.1_acf_in_window | val | F3_dependence | regression@oot | 9 | 0.712 | 0.778 | 0.0391 | 0.145 | False |
| F6.6_feature_fid@oot | F6.6_feature_fid | oot | F6_windows | regression@oot | 9 | 0.697 | 0.889 | 0.0195 | 0.0962 | False |
| F3.2_acf_beyond_window@oot | F3.2_acf_beyond_window | oot | F3_dependence | classification@oot | 9 | 0.684 | 0.889 | 0.0273 | 0.115 | False |
| F8.4_event_by_how | F8.4_event_by_how | val | F8_target | regression@val | 9 | 0.668 | 0.889 | 0.0117 | 0.0762 | False |
| F3.2_acf_beyond_window@oot | F3.2_acf_beyond_window | oot | F3_dependence | regression@oot | 9 | 0.665 | 0.889 | 0.0273 | 0.115 | False |
| F2.1_ks_d168@oot | F2.1_ks_d168 | oot | F2_increments | classification@oot | 9 | 0.64 | 0.778 | 0.0195 | 0.0962 | False |
| F8.6_cond_future_ks@oot | F8.6_cond_future_ks | oot | F8_target | classification@val | 9 | 0.638 | 1 | 0.00391 | 0.0549 | False |
| F6.6_feature_fid | F6.6_feature_fid | val | F6_windows | regression@oot | 9 | 0.626 | 0.778 | 0.0508 | 0.177 | False |
| F6.6_feature_fid@train | F6.6_feature_fid | train | F6_windows | regression@oot | 9 | 0.626 | 0.667 | 0.0977 | 0.243 | False |
| F8.6_cond_future_ks@oot | F8.6_cond_future_ks | oot | F8_target | regression@oot | 9 | 0.626 | 0.889 | 0.00781 | 0.0644 | False |
| F8.4_event_by_how@oot | F8.4_event_by_how | oot | F8_target | regression@oot | 9 | 0.623 | 0.778 | 0.0273 | 0.115 | False |
| F8.4_event_by_how@train | F8.4_event_by_how | train | F8_target | regression@oot | 9 | 0.623 | 0.889 | 0.00781 | 0.0644 | False |
| F3.1_acf_in_window | F3.1_acf_in_window | val | F3_dependence | classification@val | 9 | 0.62 | 0.778 | 0.0742 | 0.213 | False |
| F1.9_js | F1.9_js | val | F1_marginal | classification@val | 9 | 0.618 | 0.667 | 0.0977 | 0.243 | False |
| F3.4_acf_sq_d | F3.4_acf_sq_d | val | F3_dependence | classification@val | 9 | 0.609 | 0.778 | 0.0977 | 0.243 | False |
| F3.2_acf_beyond_window | F3.2_acf_beyond_window | val | F3_dependence | classification@val | 9 | 0.604 | 1 | 0.00391 | 0.0549 | False |
| F3.2_acf_beyond_window@oot | F3.2_acf_beyond_window | oot | F3_dependence | classification@val | 9 | 0.604 | 0.778 | 0.0547 | 0.177 | False |
| F2.2_vol_ratio_err_d24@oot | F2.2_vol_ratio_err_d24 | oot | F2_increments | classification@oot | 9 | 0.586 | 0.889 | 0.00781 | 0.0644 | False |
| F8.5_cond_event_err | F8.5_cond_event_err | val | F8_target | regression@val | 9 | 0.585 | 0.778 | 0.0742 | 0.213 | False |
| F8.6_cond_future_ks@oot | F8.6_cond_future_ks | oot | F8_target | classification@oot | 9 | 0.582 | 0.889 | 0.00781 | 0.0644 | False |
| F1.9_js@oot | F1.9_js | oot | F1_marginal | classification@val | 9 | 0.582 | 0.889 | 0.0273 | 0.115 | False |
| F3.8_calendar_corr_err@oot | F3.8_calendar_corr_err | oot | F3_dependence | regression@val | 9 | 0.582 | 0.778 | 0.0195 | 0.0962 | False |
| F3.1_acf_in_window@oot | F3.1_acf_in_window | oot | F3_dependence | regression@val | 9 | 0.579 | 0.667 | 0.203 | 0.391 | False |
| F2.1_ks_d168@train | F2.1_ks_d168 | train | F2_increments | classification@oot | 9 | 0.578 | 0.778 | 0.0391 | 0.145 | False |
| F3.1_acf_in_window@train | F3.1_acf_in_window | train | F3_dependence | regression@oot | 9 | 0.576 | 0.778 | 0.0391 | 0.145 | False |
| F3.1_acf_in_window | F3.1_acf_in_window | val | F3_dependence | classification@oot | 9 | 0.572 | 0.889 | 0.0156 | 0.0962 | False |
| F3.4_acf_sq_d@oot | F3.4_acf_sq_d | oot | F3_dependence | classification@val | 9 | 0.562 | 1 | 0.00391 | 0.0549 | False |
| F3.8_calendar_corr_err@train | F3.8_calendar_corr_err | train | F3_dependence | regression@val | 9 | 0.561 | 0.778 | 0.0195 | 0.0962 | False |
| F11.2_rare_share_logratio@train | F11.2_rare_share_logratio | train | F11_class_balance | classification@val | 9 | 0.559 | 1 | 0.00391 | 0.0549 | False |
| F8.6_cond_future_ks | F8.6_cond_future_ks | val | F8_target | classification@oot | 9 | 0.553 | 0.889 | 0.0117 | 0.0762 | False |
| F8.6_cond_future_ks | F8.6_cond_future_ks | val | F8_target | classification@val | 9 | 0.552 | 0.667 | 0.0547 | 0.177 | False |
| F2.1_w1_d24@train | F2.1_w1_d24 | train | F2_increments | regression@oot | 9 | 0.55 | 0.889 | 0.00781 | 0.0644 | False |
| F2.1_w1_d24 | F2.1_w1_d24 | val | F2_increments | regression@oot | 9 | 0.547 | 0.889 | 0.00781 | 0.0644 | False |
| F8.6_cond_future_ks@train | F8.6_cond_future_ks | train | F8_target | regression@oot | 9 | 0.544 | 0.889 | 0.0117 | 0.0762 | False |
| F8.6_cond_future_ks@train | F8.6_cond_future_ks | train | F8_target | classification@val | 9 | 0.544 | 1 | 0.00391 | 0.0549 | False |
| F2.1_w1_d24@oot | F2.1_w1_d24 | oot | F2_increments | regression@oot | 9 | 0.544 | 0.889 | 0.0117 | 0.0762 | False |
| F3.4_acf_sq_d | F3.4_acf_sq_d | val | F3_dependence | classification@oot | 9 | 0.539 | 0.889 | 0.00781 | 0.0644 | False |

_Showing 40 rows of 956; all of them — `hypotheses/RQ4_global.parquet`._

**by_reference**

| criterion | reference | median_rho | share_predictive |
|---|---|---|---|
| classification@oot | oot | 0.288 | 0 |
| classification@oot | train | 0.266 | 0 |
| classification@oot | val | 0.179 | 0 |
| classification@val | oot | 0.276 | 0 |
| classification@val | train | 0.265 | 0 |
| classification@val | val | 0.268 | 0 |
| regression@oot | oot | 0.235 | 0 |
| regression@oot | train | 0.171 | 0 |
| regression@oot | val | 0.224 | 0 |
| regression@val | oot | 0.021 | 0 |
| regression@val | train | -0.011 | 0 |
| regression@val | val | 0.143 | 0 |


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
| F5_seams | oot | -0.091 | -0.231 | -0.022 | 0.152 |
| F5_seams | train | -0.091 | -0.231 | -0.022 | 0.163 |
| F5_seams | val | -0.091 | -0.251 | -0.022 | 0.185 |
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
| F3.1_acf_in_window@train | F3.1_acf_in_window | train | F3_dependence | regression@val | 9 | 0.809 | 0.667 | 0.0547 | 0.177 | False |
| F3.2_acf_beyond_window@train | F3.2_acf_beyond_window | train | F3_dependence | regression@val | 9 | 0.779 | 0.667 | 0.0977 | 0.243 | False |
| F3.1_acf_in_window@oot | F3.1_acf_in_window | oot | F3_dependence | regression@oot | 9 | 0.732 | 1 | 0.00391 | 0.0549 | False |
| F3.1_acf_in_window | F3.1_acf_in_window | val | F3_dependence | regression@oot | 9 | 0.712 | 0.778 | 0.0391 | 0.145 | False |
| F6.6_feature_fid@oot | F6.6_feature_fid | oot | F6_windows | regression@oot | 9 | 0.697 | 0.889 | 0.0195 | 0.0962 | False |
| F3.2_acf_beyond_window@oot | F3.2_acf_beyond_window | oot | F3_dependence | classification@oot | 9 | 0.684 | 0.889 | 0.0273 | 0.115 | False |
| F8.4_event_by_how | F8.4_event_by_how | val | F8_target | regression@val | 9 | 0.668 | 0.889 | 0.0117 | 0.0762 | False |
| F3.2_acf_beyond_window@oot | F3.2_acf_beyond_window | oot | F3_dependence | regression@oot | 9 | 0.665 | 0.889 | 0.0273 | 0.115 | False |
| F2.1_ks_d168@oot | F2.1_ks_d168 | oot | F2_increments | classification@oot | 9 | 0.64 | 0.778 | 0.0195 | 0.0962 | False |
| F8.6_cond_future_ks@oot | F8.6_cond_future_ks | oot | F8_target | classification@val | 9 | 0.638 | 1 | 0.00391 | 0.0549 | False |
| F6.6_feature_fid | F6.6_feature_fid | val | F6_windows | regression@oot | 9 | 0.626 | 0.778 | 0.0508 | 0.177 | False |
| F3.1_acf_in_window | F3.1_acf_in_window | val | F3_dependence | classification@val | 9 | 0.62 | 0.778 | 0.0742 | 0.213 | False |
| F1.9_js | F1.9_js | val | F1_marginal | classification@val | 9 | 0.618 | 0.667 | 0.0977 | 0.243 | False |
| F3.4_acf_sq_d | F3.4_acf_sq_d | val | F3_dependence | classification@val | 9 | 0.609 | 0.778 | 0.0977 | 0.243 | False |
| F3.2_acf_beyond_window | F3.2_acf_beyond_window | val | F3_dependence | classification@val | 9 | 0.604 | 1 | 0.00391 | 0.0549 | False |
| F2.2_vol_ratio_err_d24@oot | F2.2_vol_ratio_err_d24 | oot | F2_increments | classification@oot | 9 | 0.586 | 0.889 | 0.00781 | 0.0644 | False |
| F8.5_cond_event_err | F8.5_cond_event_err | val | F8_target | regression@val | 9 | 0.585 | 0.778 | 0.0742 | 0.213 | False |
| F8.6_cond_future_ks@oot | F8.6_cond_future_ks | oot | F8_target | classification@oot | 9 | 0.582 | 0.889 | 0.00781 | 0.0644 | False |
| F3.8_calendar_corr_err@oot | F3.8_calendar_corr_err | oot | F3_dependence | regression@val | 9 | 0.582 | 0.778 | 0.0195 | 0.0962 | False |
| F2.1_ks_d168@train | F2.1_ks_d168 | train | F2_increments | classification@oot | 9 | 0.578 | 0.778 | 0.0391 | 0.145 | False |


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
| val ↔ oot | fidelity:seams | 0.974 |
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
| holdout_clf | timestral | long-series generator | 9.12 | 7.45 | 6.84 | True |
| holdout_clf | timesfm | long-series generator | 7.57 | 6.79 | 21.8 | True |
| holdout_clf | chronos | long-series generator | 7.65 | 6.12 | 79.9 | False |
| holdout_clf | vae_rand | random selection | 7.09 | 6.21 | 127 | True |
| holdout_clf | vae_quilting | optimised selection | 5.98 | 5.91 | 127 | True |
| holdout_clf | vae_greedy | optimised selection | 7.14 | 6.87 | 127 | False |
| holdout_clf | vae_knn | optimised selection | 7.19 | 7.06 | 127 | False |
| holdout_clf | vae_mbb | optimised selection | 7.12 | 7.2 | 127 | False |
| holdout_clf | vae_herding | optimised selection | 5.95 | 6.38 | 127 | True |
| holdout_clf | vae_zseries | optimised selection | 6.52 | 7 | 131 | False |
| holdout_clf | vae_atsp | optimised selection | 6.89 | 7.91 | 148 | False |
| holdout_clf | vae_pctsp | optimised selection | 6.86 | 7.73 | 184 | False |
| holdout_clf | diffusion_ts | long-series generator | 6.23 | 8.09 | 5.83e+03 | False |
| holdout_reg | timestral | long-series generator | 6.57 | 5.75 | 6.84 | True |
| holdout_reg | timesfm | long-series generator | 5.32 | 5.29 | 21.8 | True |
| holdout_reg | chronos | long-series generator | 6.65 | 5.45 | 79.9 | False |
| holdout_reg | vae_rand | random selection | 7.98 | 6.81 | 127 | False |
| holdout_reg | vae_quilting | optimised selection | 6.65 | 6.36 | 127 | False |
| holdout_reg | vae_greedy | optimised selection | 7.71 | 7.24 | 127 | False |
| holdout_reg | vae_knn | optimised selection | 7.76 | 7.44 | 127 | False |
| holdout_reg | vae_mbb | optimised selection | 7.87 | 7.7 | 127 | False |
| holdout_reg | vae_herding | optimised selection | 6.55 | 6.78 | 127 | False |
| holdout_reg | vae_zseries | optimised selection | 6.65 | 7.08 | 131 | False |
| holdout_reg | vae_atsp | optimised selection | 7.39 | 8.24 | 148 | False |
| holdout_reg | vae_pctsp | optimised selection | 7.45 | 8.12 | 184 | False |
| holdout_reg | diffusion_ts | long-series generator | 5.79 | 7.8 | 5.83e+03 | False |
| train_clf | timestral | long-series generator | 9.68 | 7.83 | 6.84 | True |
| train_clf | timesfm | long-series generator | 7.56 | 6.79 | 21.8 | True |
| train_clf | chronos | long-series generator | 8.06 | 6.39 | 79.9 | False |
| train_clf | vae_rand | random selection | 7.04 | 6.18 | 127 | True |
| train_clf | vae_quilting | optimised selection | 6.05 | 5.96 | 127 | True |
| train_clf | vae_greedy | optimised selection | 7.25 | 6.94 | 127 | False |
| train_clf | vae_knn | optimised selection | 7.3 | 7.14 | 127 | False |
| train_clf | vae_mbb | optimised selection | 7.07 | 7.17 | 127 | False |
| train_clf | vae_herding | optimised selection | 5.47 | 6.06 | 127 | True |
| train_clf | vae_zseries | optimised selection | 6.21 | 6.79 | 131 | False |
| train_clf | vae_atsp | optimised selection | 6.8 | 7.85 | 148 | False |
| train_clf | vae_pctsp | optimised selection | 6.84 | 7.72 | 184 | False |
| train_clf | diffusion_ts | long-series generator | 6.13 | 8.02 | 5.83e+03 | False |
| train_reg | timestral | long-series generator | 7.13 | 6.13 | 6.84 | True |


**hardware**: ['NVIDIA L4']

### RQ7. Moderators: dataset descriptors and the effects of RQ2 / RQ3 (exploratory)

| effect | descriptor | spearman | p | n | p_bh |
|---|---|---|---|---|---|
| RQ2:fidelity:chronos vs assembly_median | acf24 | 0 | 1 | 7 | 1 |
| RQ2:fidelity:chronos vs assembly_median | acf168 | 0.393 | 0.383 | 7 | 0.681 |
| RQ2:fidelity:chronos vs assembly_median | kurt_d24 | 0.5 | 0.253 | 7 | 0.569 |
| RQ2:fidelity:chronos vs assembly_median | volclust | 0.536 | 0.215 | 7 | 0.524 |
| RQ2:fidelity:chronos vs assembly_median | trend | -0.107 | 0.819 | 7 | 0.917 |
| RQ2:fidelity:chronos vs assembly_median | nan_share | -0.612 | 0.144 | 7 | 0.454 |
| RQ2:utility:chronos vs assembly_median | acf24 | 0.179 | 0.702 | 7 | 0.892 |
| RQ2:utility:chronos vs assembly_median | acf168 | 0.75 | 0.0522 | 7 | 0.334 |
| RQ2:utility:chronos vs assembly_median | kurt_d24 | 0.679 | 0.0938 | 7 | 0.438 |
| RQ2:utility:chronos vs assembly_median | volclust | 0.464 | 0.294 | 7 | 0.598 |
| RQ2:utility:chronos vs assembly_median | trend | 0.107 | 0.819 | 7 | 0.917 |
| RQ2:utility:chronos vs assembly_median | nan_share | -0.612 | 0.144 | 7 | 0.454 |
| RQ2:fidelity:chronos vs vae_rand | acf24 | -0.0714 | 0.879 | 7 | 0.938 |
| RQ2:fidelity:chronos vs vae_rand | acf168 | 0.321 | 0.482 | 7 | 0.753 |
| RQ2:fidelity:chronos vs vae_rand | kurt_d24 | 0.393 | 0.383 | 7 | 0.681 |
| RQ2:fidelity:chronos vs vae_rand | volclust | 0.679 | 0.0938 | 7 | 0.438 |
| RQ2:fidelity:chronos vs vae_rand | trend | -0.143 | 0.76 | 7 | 0.915 |
| RQ2:fidelity:chronos vs vae_rand | nan_share | -0.612 | 0.144 | 7 | 0.454 |
| RQ2:utility:chronos vs vae_rand | acf24 | 0.179 | 0.702 | 7 | 0.892 |
| RQ2:utility:chronos vs vae_rand | acf168 | 0.75 | 0.0522 | 7 | 0.334 |
| RQ2:utility:chronos vs vae_rand | kurt_d24 | 0.679 | 0.0938 | 7 | 0.438 |
| RQ2:utility:chronos vs vae_rand | volclust | 0.464 | 0.294 | 7 | 0.598 |
| RQ2:utility:chronos vs vae_rand | trend | 0.107 | 0.819 | 7 | 0.917 |
| RQ2:utility:chronos vs vae_rand | nan_share | -0.612 | 0.144 | 7 | 0.454 |
| RQ2:fidelity:diffusion_ts vs assembly_median | acf24 | -0.583 | 0.0992 | 9 | 0.438 |
| RQ2:fidelity:diffusion_ts vs assembly_median | acf168 | -0.317 | 0.406 | 9 | 0.694 |
| RQ2:fidelity:diffusion_ts vs assembly_median | kurt_d24 | 0.133 | 0.732 | 9 | 0.901 |
| RQ2:fidelity:diffusion_ts vs assembly_median | volclust | -0.4 | 0.286 | 9 | 0.598 |
| RQ2:fidelity:diffusion_ts vs assembly_median | trend | -0.55 | 0.125 | 9 | 0.454 |
| RQ2:fidelity:diffusion_ts vs assembly_median | nan_share | 0.525 | 0.147 | 9 | 0.454 |
| RQ2:utility:diffusion_ts vs assembly_median | acf24 | -0.517 | 0.154 | 9 | 0.454 |
| RQ2:utility:diffusion_ts vs assembly_median | acf168 | -0.05 | 0.898 | 9 | 0.95 |
| RQ2:utility:diffusion_ts vs assembly_median | kurt_d24 | 0.533 | 0.139 | 9 | 0.454 |
| RQ2:utility:diffusion_ts vs assembly_median | volclust | -0.183 | 0.637 | 9 | 0.867 |
| RQ2:utility:diffusion_ts vs assembly_median | trend | -0.75 | 0.0199 | 9 | 0.284 |
| RQ2:utility:diffusion_ts vs assembly_median | nan_share | 0.434 | 0.244 | 9 | 0.558 |
| RQ2:fidelity:diffusion_ts vs vae_rand | acf24 | -0.55 | 0.125 | 9 | 0.454 |
| RQ2:fidelity:diffusion_ts vs vae_rand | acf168 | -0.25 | 0.516 | 9 | 0.787 |
| RQ2:fidelity:diffusion_ts vs vae_rand | kurt_d24 | 0.217 | 0.576 | 9 | 0.837 |
| RQ2:fidelity:diffusion_ts vs vae_rand | volclust | -0.133 | 0.732 | 9 | 0.901 |

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


## Case study: method `vae_zseries` (secondary, BH within a hypothesis)

Method `vae_zseries` vs the controls on its own pool, alternative stitchers and long-series generators. Sign of the effect: > 0 — the method is better than the comparator. Pre-specified cell (TSTR, task clf_up_h24_q90, linear model, OOT; Holm over CS7 and CS10):

| hypothesis | comparator | n_datasets | median_z | ci_lo | ci_hi | p_better_holm | p_worse_holm | p_equiv_holm | n_better | n_worse | n_same | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CS7 | vae_rand | 9 | -0.906 | -1.98 | 1.66 | 1 | 0.57 | 1 | 2 | 3 | 0 | inconclusive |
| CS10 | diffusion_ts | 9 | -2.4 | -7.62 | -0.996 | 1 | 0.0586 | 1 | 1 | 4 | 0 | inconclusive |
| CS10 | chronos | 7 | 1.38 | -1.95 | 3.62 | 0.867 | 0.766 | 1 | 2 | 1 | 0 | inconclusive |


| Hypothesis | Verdicts |
|---|---|
| CS1. Distribution and dependence against train | inconclusive: 31 |
| CS2. Distribution and dependence against val | inconclusive: 33 |
| CS3. Seam artefacts | better: 5, inconclusive: 3 |
| CS4. Structure longer than a window | inconclusive: 10 |
| CS5. Target structure | inconclusive: 6 |
| CS6. Realism of single windows and memorisation | inconclusive: 11 |
| CS7. TSTR of the method vs the random path (case-study task) | inconclusive: 6 |
| CS8. The same on the other tasks | inconclusive: 52 |
| CS9. Fidelity vs other stitchers of the same pool and the long-series generators | inconclusive: 870 |
| CS10. TSTR vs other stitchers of the same pool and the long-series generators | inconclusive: 638 |
| CS11. The method's effect on TSTR across model classes |  |
| CS12. The method's effect on TSTR over time (val vs OOT) and across subgroups |  |
| CS13. TSTR of the method vs TRTR | worse: 52, inconclusive: 6 |
| CS14. Computational cost of the method vs the others |  |
| CS15. Moderators of the method's effect (exploratory) | significant after BH: 1 of 83 |

### CS1. Distribution and dependence against train

| unit | comparator | n_datasets | median_z | mean_z | ci_lo | ci_hi | p_better_adj | p_worse_adj | p_equiv_adj | n_better | n_worse | n_same | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F3.6_peak24_err@train | vae_rand | 9 | 3.18 | 3.12 | 2.02 | 4.3 | 0.0605 | 1 | 0.998 | 6 | 0 | 0 | inconclusive |
| F3.1_acf_in_window@train | vae_rand | 9 | 2.87 | 5.88 | 1.44 | 13 | 0.0908 | 1 | 0.998 | 6 | 0 | 0 | inconclusive |
| F1.1_ks@train | vae_rand | 9 | 1.89 | 1.91 | 0.713 | 3.07 | 0.121 | 1 | 0.998 | 7 | 1 | 0 | inconclusive |
| F1.5_q99_err@train | vae_rand | 9 | 1.12 | 1.54 | 0.103 | 2.95 | 0.121 | 1 | 0.998 | 4 | 0 | 0 | inconclusive |
| F1.9_js@train | vae_rand | 9 | 1.77 | 1.99 | 0.755 | 3.15 | 0.121 | 1 | 0.998 | 5 | 1 | 0 | inconclusive |
| F2.4_big_jump_share_err@train | vae_rand | 9 | -2.34 | -2.76 | -4.47 | -1.24 | 0.998 | 0.121 | 0.998 | 0 | 5 | 0 | inconclusive |
| F2.1_ks_d168@train | vae_rand | 9 | 3.01 | 5.53 | 1.48 | 9.6 | 0.141 | 1 | 0.998 | 5 | 1 | 0 | inconclusive |
| F2.1_w1_d24@train | vae_rand | 9 | 2.5 | 2.34 | 0.168 | 4.39 | 0.164 | 1 | 0.998 | 6 | 1 | 0 | inconclusive |
| F1.3_ad@train | vae_rand | 9 | 1.32 | 1.38 | -0.138 | 2.71 | 0.168 | 1 | 0.998 | 5 | 1 | 0 | inconclusive |
| F2.1_ks_d6@train | vae_rand | 9 | 2.58 | 1.87 | 0.0901 | 3.46 | 0.168 | 1 | 0.998 | 5 | 1 | 0 | inconclusive |
| F2.2_vol_ratio_err_d24@train | vae_rand | 9 | 2.59 | 2.55 | -0.201 | 5.26 | 0.2 | 1 | 0.998 | 5 | 1 | 1 | inconclusive |
| F1.6_std_err@train | vae_rand | 9 | 0.695 | 0.804 | -0.246 | 1.74 | 0.231 | 1 | 0.998 | 4 | 1 | 0 | inconclusive |
| F3.4_acf_abs_d@train | vae_rand | 9 | 1.77 | 1.36 | -1.83 | 4.14 | 0.262 | 1 | 0.998 | 5 | 1 | 0 | inconclusive |
| F3.7_dfa_err@train | vae_rand | 9 | 1.21 | 1.18 | -0.0679 | 2.5 | 0.298 | 1 | 0.998 | 4 | 1 | 0 | inconclusive |
| F3.4_acf_sq_d@train | vae_rand | 9 | 6.98 | 2.22 | -9.69 | 10.8 | 0.333 | 1 | 0.998 | 7 | 2 | 0 | inconclusive |
| F2.1_ks_d1@train | vae_rand | 9 | 2.19 | 0.0901 | -4.56 | 3.58 | 0.371 | 1 | 0.998 | 5 | 1 | 0 | inconclusive |
| F3.3_pacf@train | vae_rand | 9 | -2.96 | -8.78 | -20.3 | -1.28 | 0.998 | 0.424 | 0.998 | 1 | 6 | 0 | inconclusive |
| F1.5_quantile_err@train | vae_rand | 9 | 0.908 | 0.6 | -1.45 | 2.52 | 0.427 | 1 | 0.982 | 4 | 3 | 0 | inconclusive |
| F1.6_mean_err@train | vae_rand | 9 | 1.3 | 0.692 | -1.06 | 2.25 | 0.427 | 1 | 0.998 | 3 | 2 | 0 | inconclusive |
| F2.1_ks_d24@train | vae_rand | 9 | 2.24 | 0.831 | -1 | 2.4 | 0.427 | 1 | 0.998 | 5 | 2 | 0 | inconclusive |
| F1.2_w1@train | vae_rand | 9 | 1.21 | 0.463 | -1.81 | 2.36 | 0.465 | 1 | 0.998 | 3 | 2 | 0 | inconclusive |
| F3.8_calendar_corr_err@train | vae_rand | 9 | -0.759 | 0.27 | -1.31 | 1.95 | 0.506 | 1 | 0.943 | 3 | 1 | 0 | inconclusive |
| F1.10_hill_err@train | vae_rand | 9 | 0.343 | -0.0513 | -1.26 | 0.921 | 0.542 | 1 | 0.943 | 2 | 2 | 0 | inconclusive |
| F1.6_skew_err@train | vae_rand | 9 | 0.268 | 0.089 | -1.23 | 1.37 | 0.674 | 1 | 0.943 | 2 | 0 | 0 | inconclusive |
| F2.3_up_share_err@train | vae_rand | 9 | 0.0728 | -0.633 | -2.97 | 1.09 | 0.674 | 1 | 0.943 | 1 | 1 | 0 | inconclusive |
| F2.2_vol_ratio_err_d1@train | vae_rand | 9 | 0.566 | -0.203 | -2.46 | 1.77 | 0.704 | 1 | 0.982 | 3 | 2 | 0 | inconclusive |
| F3.6_peak168_err@train | vae_rand | 9 | 0.637 | -0.395 | -1.71 | 0.739 | 0.785 | 1 | 0.943 | 1 | 1 | 0 | inconclusive |
| F1.5_q01_err@train | vae_rand | 9 | -0.649 | -0.365 | -2.03 | 1.11 | 0.897 | 1 | 0.943 | 2 | 2 | 0 | inconclusive |
| F1.4_qq_corr@train | vae_rand | 9 | -0.102 | -0.429 | -1.67 | 0.784 | 0.904 | 1 | 0.943 | 2 | 2 | 0 | inconclusive |
| F1.6_kurt_err@train | vae_rand | 9 | -0.17 | -0.857 | -2.17 | 0.266 | 0.96 | 1 | 0.998 | 1 | 2 | 0 | inconclusive |
| F3.5_log_psd@train | vae_rand | 9 | -3.73 | -2.26 | -5.27 | 1.16 | 0.96 | 1 | 0.998 | 1 | 4 | 0 | inconclusive |

### CS2. Distribution and dependence against val

| unit | comparator | n_datasets | median_z | mean_z | ci_lo | ci_hi | p_better_adj | p_worse_adj | p_equiv_adj | n_better | n_worse | n_same | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F2.1_ks_d168 | vae_rand | 9 | 5.23 | 6.33 | 3.26 | 9.75 | 0.129 | 0.998 | 0.998 | 8 | 0 | 0 | inconclusive |
| F2.2_vol_ratio_err_d24 | vae_rand | 9 | 2.59 | 3.15 | 0.989 | 5.46 | 0.226 | 0.998 | 0.998 | 5 | 0 | 0 | inconclusive |
| F2.4_big_jump_share_err | vae_rand | 9 | -2.58 | -2.03 | -2.99 | -0.994 | 1 | 0.322 | 0.998 | 0 | 6 | 0 | inconclusive |
| F3.3_pacf | vae_rand | 9 | -3.05 | -4.58 | -8.66 | -1.24 | 1 | 0.322 | 0.998 | 1 | 6 | 0 | inconclusive |
| F2.1_w1_d24 | vae_rand | 9 | 2.63 | 3.02 | 0.512 | 5.73 | 0.408 | 0.998 | 0.998 | 6 | 2 | 0 | inconclusive |
| F1.8_coverage | vae_rand | 4 | -2.1 | -2.15 | -4.1 | -0.437 | 1 | 0.688 | 0.998 | 0 | 1 | 0 | inconclusive |
| F1.10_hill_err | vae_rand | 9 | 0.333 | 0.312 | -0.281 | 0.893 | 0.72 | 0.963 | 0.588 | 1 | 1 | 0 | inconclusive |
| F1.1_ks | vae_rand | 9 | -0.728 | 0.755 | -1.18 | 2.89 | 0.72 | 0.928 | 0.588 | 3 | 1 | 0 | inconclusive |
| F1.2_w1 | vae_rand | 9 | -1.3 | 0.0552 | -2.03 | 2.48 | 0.72 | 0.928 | 0.588 | 3 | 3 | 0 | inconclusive |
| F1.3_ad | vae_rand | 9 | -1.11 | 0.359 | -1.73 | 2.6 | 0.72 | 0.928 | 0.588 | 4 | 2 | 0 | inconclusive |
| F1.4_qq_corr | vae_rand | 9 | 0.782 | 0.239 | -1.06 | 1.55 | 0.72 | 0.928 | 0.588 | 4 | 1 | 0 | inconclusive |
| F1.5_q01_err | vae_rand | 9 | 0.0731 | -0.102 | -1.62 | 1.26 | 0.72 | 0.928 | 0.588 | 2 | 1 | 0 | inconclusive |
| F1.5_q99_err | vae_rand | 9 | -0.352 | -0.119 | -1.76 | 1.72 | 0.72 | 0.928 | 0.588 | 2 | 2 | 0 | inconclusive |
| F1.5_quantile_err | vae_rand | 9 | -0.662 | -0.0851 | -2.2 | 2.31 | 0.72 | 0.928 | 0.588 | 3 | 4 | 0 | inconclusive |
| F1.6_kurt_err | vae_rand | 9 | 0.143 | 0.686 | -0.401 | 1.95 | 0.72 | 0.963 | 0.588 | 3 | 0 | 0 | inconclusive |
| F1.6_mean_err | vae_rand | 9 | -1.3 | 0.0457 | -2.07 | 2.54 | 0.72 | 0.928 | 0.588 | 3 | 3 | 0 | inconclusive |
| F1.6_skew_err | vae_rand | 9 | 0.268 | 0.791 | -0.64 | 2.38 | 0.72 | 0.928 | 0.588 | 3 | 0 | 0 | inconclusive |
| F1.6_std_err | vae_rand | 9 | 0.567 | 0.26 | -0.856 | 1.33 | 0.72 | 0.928 | 0.588 | 4 | 1 | 0 | inconclusive |
| F1.7_out_of_range | vae_rand | 8 | -0.904 | -0.165 | -1.72 | 1.4 | 0.72 | 0.928 | 0.588 | 3 | 2 | 0 | inconclusive |
| F1.9_js | vae_rand | 9 | -0.485 | 0.639 | -0.94 | 2.39 | 0.72 | 0.928 | 0.588 | 4 | 1 | 0 | inconclusive |
| F2.1_ks_d1 | vae_rand | 9 | 1.16 | -1.23 | -6.59 | 2.39 | 0.72 | 0.928 | 0.692 | 2 | 2 | 0 | inconclusive |
| F2.1_ks_d24 | vae_rand | 9 | 1.06 | 0.564 | -1.43 | 2.41 | 0.72 | 0.928 | 0.588 | 3 | 2 | 0 | inconclusive |
| F2.1_ks_d6 | vae_rand | 9 | 0.192 | 0.285 | -2.15 | 2.93 | 0.72 | 0.928 | 0.588 | 3 | 3 | 0 | inconclusive |
| F2.2_vol_ratio_err_d1 | vae_rand | 9 | -0.425 | -0.28 | -1.9 | 1.35 | 0.72 | 0.928 | 0.588 | 2 | 2 | 0 | inconclusive |
| F2.3_up_share_err | vae_rand | 9 | -0.105 | -0.476 | -2.06 | 0.961 | 0.72 | 0.928 | 0.588 | 2 | 3 | 0 | inconclusive |
| F3.1_acf_in_window | vae_rand | 9 | -0.0918 | 0.234 | -2.61 | 2.98 | 0.72 | 0.928 | 0.588 | 4 | 3 | 0 | inconclusive |
| F3.4_acf_abs_d | vae_rand | 9 | 0.859 | -0.346 | -4.36 | 3.33 | 0.72 | 0.928 | 0.588 | 2 | 3 | 0 | inconclusive |
| F3.4_acf_sq_d | vae_rand | 9 | 2.3 | -8.86 | -25.8 | 4.75 | 0.72 | 0.928 | 0.692 | 4 | 2 | 0 | inconclusive |
| F3.6_peak168_err | vae_rand | 9 | 1.02 | 0.5 | -0.618 | 1.57 | 0.72 | 0.928 | 0.588 | 3 | 1 | 0 | inconclusive |
| F3.6_peak24_err | vae_rand | 9 | 1.19 | -0.0282 | -3.29 | 2.95 | 0.72 | 0.928 | 0.588 | 4 | 3 | 0 | inconclusive |
| F3.7_dfa_err | vae_rand | 9 | 0.232 | 0.587 | -1.68 | 2.38 | 0.72 | 0.928 | 0.692 | 4 | 1 | 0 | inconclusive |
| F3.8_calendar_corr_err | vae_rand | 9 | -1.19 | -0.191 | -1.66 | 1.53 | 0.72 | 0.928 | 0.588 | 2 | 3 | 0 | inconclusive |
| F3.5_log_psd | vae_rand | 9 | -4.33 | -1.69 | -6.06 | 3.43 | 0.902 | 0.928 | 0.874 | 2 | 5 | 0 | inconclusive |

### CS3. Seam artefacts

| unit | comparator | n_datasets | median_z | mean_z | ci_lo | ci_hi | p_better_adj | p_worse_adj | p_equiv_adj | n_better | n_worse | n_same | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F5.3_seam_z_mean | vae_rand | 9 | 4.92 | 5.36 | 3.81 | 7.19 | 0.00781 | 1 | 1 | 9 | 0 | 0 | better |
| F5.3_seam_z_p95 | vae_rand | 9 | 6.18 | 6.8 | 4.36 | 9.85 | 0.00781 | 1 | 1 | 9 | 0 | 0 | better |
| F5.6_cp_at_seams | vae_rand | 8 | 2.02 | 2.1 | 1.64 | 2.63 | 0.0104 | 1 | 1 | 7 | 0 | 0 | better |
| F5.1_ks_seam_vs_real | vae_rand | 9 | 1.62 | 2.01 | 0.705 | 3.78 | 0.0117 | 1 | 1 | 5 | 0 | 0 | better |
| F5.2_ks_seam_vs_inside | vae_rand | 9 | 2.66 | 2.78 | 1.12 | 4.77 | 0.0156 | 1 | 1 | 6 | 0 | 0 | better |
| F5.4_seam_local_acf | vae_rand | 9 | 0.748 | 0.852 | 0.211 | 1.54 | 0.026 | 1 | 0.979 | 4 | 0 | 0 | inconclusive |
| F5.7_seam_detect_auc_dev | vae_rand | 9 | 0.662 | 0.628 | -0.215 | 1.65 | 0.116 | 1 | 0.602 | 2 | 0 | 0 | inconclusive |
| F5.5_cp_rate_err | vae_rand | 9 | 0.243 | -0.31 | -1.43 | 0.678 | 0.545 | 1 | 0.602 | 1 | 1 | 0 | inconclusive |

### CS4. Structure longer than a window

| unit | comparator | n_datasets | median_z | mean_z | ci_lo | ci_hi | p_better_adj | p_worse_adj | p_equiv_adj | n_better | n_worse | n_same | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F6.4_mmd_2T | vae_rand | 9 | 1.91 | 1.44 | -0.251 | 3.16 | 0.488 | 0.963 | 0.787 | 4 | 1 | 0 | inconclusive |
| F7.7_regime_dur_err | vae_rand | 9 | 0.425 | 0.52 | -0.308 | 1.28 | 0.625 | 0.963 | 0.576 | 3 | 1 | 0 | inconclusive |
| F7.6_trend_err | vae_rand | 9 | -0.334 | -0.442 | -1.02 | 0.0983 | 0.951 | 0.645 | 0.186 | 0 | 1 | 1 | inconclusive |
| F3.2_acf_beyond_window | vae_rand | 9 | 0.625 | 0.719 | -2.19 | 3.38 | 0.652 | 0.962 | 0.605 | 3 | 3 | 0 | inconclusive |
| F7.1_roll_mean_ks | vae_rand | 8 | 0.0356 | 1.1 | -0.787 | 3.37 | 0.652 | 0.962 | 0.605 | 3 | 2 | 0 | inconclusive |
| F7.4_excursion_ks | vae_rand | 9 | 0.17 | 0.00584 | -0.677 | 0.661 | 0.652 | 0.962 | 0.137 | 0 | 1 | 0 | inconclusive |
| F7.2_roll_std_ks | vae_rand | 8 | -0.749 | 0.247 | -1.31 | 2.42 | 0.836 | 0.82 | 0.576 | 1 | 3 | 0 | inconclusive |
| F7.3_crossings_err | vae_rand | 9 | -1.08 | -0.698 | -3.19 | 1.85 | 0.836 | 0.82 | 0.605 | 3 | 2 | 0 | inconclusive |
| F7.5_drawdown_ks | vae_rand | 9 | 0.372 | -0.567 | -2.18 | 0.745 | 0.836 | 0.82 | 0.605 | 2 | 3 | 0 | inconclusive |
| F7.6_weekly_level_std_err | vae_rand | 9 | -1.36 | 0.111 | -2.06 | 3.15 | 0.836 | 0.82 | 0.605 | 3 | 4 | 0 | inconclusive |

### CS5. Target structure

| unit | comparator | n_datasets | median_z | mean_z | ci_lo | ci_hi | p_better_adj | p_worse_adj | p_equiv_adj | n_better | n_worse | n_same | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F8.1_class_tvd | vae_rand | 9 | 2.47 | 1.86 | 0.0373 | 3.24 | 0.0984 | 0.98 | 0.875 | 6 | 1 | 0 | inconclusive |
| F8.2_event_dur_ks | vae_rand | 9 | 0.606 | 0.633 | -0.229 | 1.53 | 0.0984 | 0.98 | 0.744 | 1 | 0 | 0 | inconclusive |
| F8.4_event_by_how | vae_rand | 9 | 1.61 | 1.07 | -0.147 | 2.34 | 0.0984 | 0.98 | 0.875 | 5 | 2 | 0 | inconclusive |
| F8.5_cond_event_err | vae_rand | 9 | 1.81 | 1.09 | -0.391 | 2.16 | 0.0984 | 0.98 | 0.875 | 6 | 1 | 0 | inconclusive |
| F8.6_cond_future_ks | vae_rand | 9 | 1.35 | 1.78 | 0.339 | 3.19 | 0.0984 | 0.98 | 0.875 | 4 | 1 | 0 | inconclusive |
| F8.3_interarrival_ks | vae_rand | 9 | 0.29 | 0.171 | -0.677 | 1.04 | 0.326 | 0.98 | 0.223 | 1 | 1 | 0 | inconclusive |

### CS6. Realism of single windows and memorisation

| unit | comparator | n_datasets | median_z | mean_z | ci_lo | ci_hi | p_better_adj | p_worse_adj | p_equiv_adj | n_better | n_worse | n_same | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F10.2_near_copy_share | vae_rand | 8 | -2.42 | -2.34 | -3.99 | -0.658 | 0.988 | 0.215 | 0.902 | 0 | 3 | 0 | inconclusive |
| F9.1_recall | vae_rand | 6 | -0.614 | -0.625 | -1.34 | 0.275 | 0.988 | 0.258 | 0.516 | 0 | 1 | 0 | inconclusive |
| F6.4_mmd | vae_rand | 9 | 1.82 | 1.56 | -0.322 | 3.66 | 0.344 | 0.938 | 0.874 | 5 | 1 | 0 | inconclusive |
| F6.6_feature_fid | vae_rand | 9 | 1.58 | 1.06 | -0.664 | 2.7 | 0.344 | 0.938 | 0.874 | 5 | 0 | 0 | inconclusive |
| F6.8_nn_dist_logratio | vae_rand | 9 | 1.67 | 1.34 | -0.198 | 2.95 | 0.344 | 0.938 | 0.874 | 5 | 1 | 0 | inconclusive |
| F9.1_precision | vae_rand | 4 | 2.47 | 6.12 | 0.00833 | 15.2 | 0.344 | 0.938 | 0.894 | 2 | 0 | 0 | inconclusive |
| F9.2_density_logdev | vae_rand | 4 | 1.05 | 1.16 | -1.65 | 3.5 | 0.412 | 0.938 | 0.874 | 2 | 0 | 0 | inconclusive |
| F6.1_disc_score | vae_rand | 9 | 0.1 | 0.0815 | -0.446 | 0.683 | 0.811 | 0.938 | 0.107 | 1 | 0 | 0 | inconclusive |
| F6.2_c2st_auc_dev | vae_rand | 8 | -0.0823 | 0.101 | -0.684 | 1.03 | 0.811 | 0.938 | 0.301 | 0 | 0 | 0 | inconclusive |
| F9.2_coverage | vae_rand | 4 | -0.217 | 0.167 | -0.908 | 1.38 | 0.811 | 0.938 | 0.516 | 1 | 0 | 0 | inconclusive |
| F10.1_dcr_logratio | vae_rand | 9 | -1.76 | -0.468 | -3.2 | 2.4 | 0.874 | 0.938 | 0.874 | 2 | 3 | 0 | inconclusive |

### CS7. TSTR of the method vs the random path (case-study task)

| unit | comparator | n_datasets | median_z | mean_z | ci_lo | ci_hi | p_better_adj | p_worse_adj | p_equiv_adj | n_better | n_worse | n_same | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| clf_up_h24_q90\|gbdt\|S\|oot\|auc | vae_rand | 9 | -0.213 | 0.166 | -0.942 | 1.45 | 1 | 1 | 0.508 | 1 | 1 | 0 | inconclusive |
| clf_up_h24_q90\|gbdt\|S\|val\|auc | vae_rand | 9 | -0.0743 | -0.111 | -1.32 | 1.05 | 1 | 1 | 0.293 | 1 | 1 | 1 | inconclusive |
| clf_up_h24_q90\|linear\|S\|oot\|auc | vae_rand | 9 | -0.906 | -0.278 | -1.98 | 1.66 | 1 | 1 | 0.82 | 2 | 3 | 0 | inconclusive |
| clf_up_h24_q90\|linear\|S\|val\|auc | vae_rand | 9 | -0.326 | -1.7 | -5.03 | 1.34 | 1 | 1 | 0.82 | 1 | 1 | 1 | inconclusive |
| clf_up_h24_q90\|mlp\|S\|oot\|auc | vae_rand | 9 | -0.0695 | -1.59 | -5.44 | 1.11 | 1 | 1 | 0.744 | 1 | 2 | 0 | inconclusive |
| clf_up_h24_q90\|mlp\|S\|val\|auc | vae_rand | 9 | -0.293 | -0.0201 | -1.4 | 1.68 | 1 | 1 | 0.602 | 1 | 2 | 0 | inconclusive |

**rowlevel**

| dataset | model | split | comparator | n_seeds | n_rows | diff | boot_ci_lo | boot_ci_hi | p_boot | p_boot_bh |
|---|---|---|---|---|---|---|---|---|---|---|
| beijing_pm25 | gbdt | oot | vae_rand | 10 | 1944 | -0.0428 | -0.0955 | 0.0324 | 0.304 | 0.469 |
| beijing_pm25 | gbdt | val | vae_rand | 10 | 2083 | -0.0645 | -0.11 | 0.0183 | 0.14 | 0.261 |
| beijing_pm25 | linear | oot | vae_rand | 10 | 1944 | -0.042 | -0.119 | 0.0559 | 0.436 | 0.589 |
| beijing_pm25 | linear | val | vae_rand | 10 | 2083 | -0.0695 | -0.167 | 0.0563 | 0.216 | 0.36 |
| beijing_pm25 | mlp | oot | vae_rand | 10 | 1944 | 0.015 | -0.0332 | 0.0675 | 0.392 | 0.543 |
| beijing_pm25 | mlp | val | vae_rand | 10 | 2083 | -0.0377 | -0.12 | 0.0789 | 0.56 | 0.703 |
| bike | gbdt | oot | vae_rand | 10 | 2140 | 0.0626 | 0.0361 | 0.0932 | 0 | 0 |
| bike | gbdt | val | vae_rand | 10 | 2140 | 0.0783 | 0.0447 | 0.109 | 0 | 0 |
| bike | linear | oot | vae_rand | 10 | 2140 | -0.00595 | -0.0264 | 0.0216 | 0.776 | 0.855 |
| bike | linear | val | vae_rand | 10 | 2140 | 0.00439 | -0.0236 | 0.0252 | 0.952 | 0.976 |
| bike | mlp | oot | vae_rand | 10 | 2140 | 0.0584 | 0.0349 | 0.0853 | 0 | 0 |
| bike | mlp | val | vae_rand | 10 | 2140 | 0.0543 | 0.0301 | 0.0752 | 0 | 0 |
| bitcoin | gbdt | oot | vae_rand | 10 | 2140 | -0.101 | -0.197 | 0.0051 | 0.064 | 0.138 |
| bitcoin | gbdt | val | vae_rand | 10 | 2140 | -0.0631 | -0.158 | 0.0325 | 0.12 | 0.231 |
| bitcoin | linear | oot | vae_rand | 10 | 2140 | -0.0547 | -0.127 | 0.00116 | 0.06 | 0.135 |
| bitcoin | linear | val | vae_rand | 10 | 2140 | 0.0204 | -0.0643 | 0.0536 | 0.964 | 0.976 |
| bitcoin | mlp | oot | vae_rand | 10 | 2140 | -0.0721 | -0.131 | -0.00299 | 0.028 | 0.0687 |
| bitcoin | mlp | val | vae_rand | 10 | 2140 | -0.0771 | -0.192 | -0.0259 | 0.004 | 0.012 |
| electricity | gbdt | oot | vae_rand | 10 | 2140 | 0.0584 | 0.0234 | 0.0861 | 0 | 0 |
| electricity | gbdt | val | vae_rand | 10 | 2140 | 0.0967 | 0.0758 | 0.124 | 0 | 0 |
| electricity | linear | oot | vae_rand | 10 | 2140 | 0.0612 | 0.0311 | 0.0889 | 0 | 0 |
| electricity | linear | val | vae_rand | 10 | 2140 | 0.0984 | 0.0807 | 0.123 | 0 | 0 |
| electricity | mlp | oot | vae_rand | 10 | 2140 | 0.0762 | 0.0391 | 0.104 | 0 | 0 |
| electricity | mlp | val | vae_rand | 10 | 2140 | 0.0824 | 0.0583 | 0.11 | 0 | 0 |
| ett | gbdt | oot | vae_rand | 10 | 2140 | 0.0338 | -0.0822 | 0.0858 | 0.952 | 0.976 |
| ett | gbdt | val | vae_rand | 10 | 2140 | -0.0292 | -0.109 | 0.0598 | 0.656 | 0.77 |
| ett | linear | oot | vae_rand | 10 | 2140 | -0.0695 | -0.123 | -0.0141 | 0.012 | 0.0341 |
| ett | linear | val | vae_rand | 10 | 2140 | -0.0667 | -0.109 | -0.0232 | 0 | 0 |
| ett | mlp | oot | vae_rand | 10 | 2140 | -0.0162 | -0.0795 | 0.0206 | 0.216 | 0.36 |
| ett | mlp | val | vae_rand | 10 | 2140 | -0.0486 | -0.131 | 0.0538 | 0.368 | 0.523 |
| household | gbdt | oot | vae_rand | 10 | 1867 | -0.0442 | -0.0848 | 0.00229 | 0.076 | 0.158 |
| household | gbdt | val | vae_rand | 10 | 2140 | -0.00349 | -0.0757 | 0.0596 | 0.976 | 0.976 |
| household | linear | oot | vae_rand | 10 | 1867 | -0.0703 | -0.1 | -0.0287 | 0 | 0 |
| household | linear | val | vae_rand | 10 | 2140 | -0.0811 | -0.12 | -0.0262 | 0 | 0 |
| household | mlp | oot | vae_rand | 10 | 1867 | -0.0357 | -0.0767 | 0.0155 | 0.22 | 0.36 |
| household | mlp | val | vae_rand | 10 | 2140 | -0.0373 | -0.0935 | 0.0343 | 0.368 | 0.523 |
| jena | gbdt | oot | vae_rand | 10 | 1922 | -0.116 | -0.177 | -0.0211 | 0.02 | 0.054 |
| jena | gbdt | val | vae_rand | 10 | 2140 | -0.0057 | -0.0626 | 0.0382 | 0.692 | 0.778 |
| jena | linear | oot | vae_rand | 10 | 1922 | -0.0327 | -0.0982 | 0.0536 | 0.548 | 0.703 |
| jena | linear | val | vae_rand | 10 | 2140 | -0.0197 | -0.0739 | 0.0578 | 0.648 | 0.77 |


### CS8. The same on the other tasks

| unit | comparator | n_datasets | median_z | mean_z | ci_lo | ci_hi | p_better_adj | p_worse_adj | p_equiv_adj | n_better | n_worse | n_same | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| clf_up_h168_q90\|linear\|S\|oot\|auc | vae_rand | 9 | -1.63 | -2.29 | -3.47 | -1.15 | 1 | 0.102 | 0.982 | 0 | 4 | 0 | inconclusive |
| clf_up_h168_q90\|linear\|S\|val\|auc | vae_rand | 9 | -1.44 | -1.75 | -2.92 | -0.786 | 1 | 0.102 | 0.955 | 0 | 3 | 0 | inconclusive |
| reg_h168\|linear\|S\|val\|mase | vae_rand | 9 | 2.84 | 2.38 | 1.65 | 3.11 | 0.102 | 1 | 0.996 | 5 | 0 | 0 | inconclusive |
| reg_h168\|gbdt\|S\|val\|mase | vae_rand | 9 | 0.979 | 1.25 | 0.415 | 2.16 | 0.254 | 1 | 0.762 | 3 | 0 | 0 | inconclusive |
| clf_up_h1_q90\|gbdt\|S\|val\|auc | vae_rand | 9 | 0.134 | 0.0153 | -0.72 | 0.591 | 0.388 | 1 | 0.284 | 0 | 1 | 0 | inconclusive |
| clf_up_h24_q99\|gbdt\|S\|val\|auc | vae_rand | 6 | 0.577 | 0.519 | -0.111 | 1.11 | 0.388 | 1 | 0.388 | 0 | 0 | 0 | inconclusive |
| mc3_h24\|linear\|S\|val\|logloss | vae_rand | 9 | 1.17 | 1.81 | -0.566 | 5.26 | 0.388 | 1 | 0.746 | 2 | 1 | 0 | inconclusive |
| ms_h24\|gbdt\|S\|oot\|mase | vae_rand | 9 | 0.956 | 0.787 | -0.385 | 1.82 | 0.388 | 1 | 0.667 | 3 | 1 | 0 | inconclusive |
| ms_h24\|gbdt\|S\|val\|mase | vae_rand | 9 | 0.798 | 1.56 | -0.417 | 4.05 | 0.388 | 1 | 0.696 | 2 | 1 | 0 | inconclusive |
| reg_h168\|gbdt\|S\|oot\|mase | vae_rand | 9 | 1.91 | 1.32 | 0.244 | 2.43 | 0.388 | 1 | 0.832 | 4 | 1 | 0 | inconclusive |
| reg_h168\|linear\|S\|oot\|mase | vae_rand | 9 | 2.33 | 1.25 | -1.52 | 3.12 | 0.388 | 1 | 0.955 | 6 | 1 | 0 | inconclusive |
| reg_h24\|gbdt\|S\|oot\|mase | vae_rand | 9 | 1.15 | 0.878 | -0.483 | 1.94 | 0.388 | 1 | 0.762 | 3 | 1 | 0 | inconclusive |
| reg_h24\|gbdt\|S\|val\|mase | vae_rand | 9 | 1.42 | 1.33 | 0.252 | 2.41 | 0.388 | 1 | 0.92 | 3 | 1 | 0 | inconclusive |
| qreg_h24\|linear\|S\|val\|pinball | vae_rand | 9 | 1.5 | 0.961 | -0.602 | 2.39 | 0.406 | 1 | 0.762 | 5 | 1 | 0 | inconclusive |
| vol_h24\|gbdt\|S\|val\|mase | vae_rand | 9 | 0.684 | 0.787 | -0.245 | 1.93 | 0.406 | 1 | 0.606 | 2 | 1 | 0 | inconclusive |
| reg_h1\|gbdt\|S\|oot\|mase | vae_rand | 9 | 1.43 | 0.818 | -0.462 | 1.88 | 0.433 | 1 | 0.746 | 5 | 0 | 0 | inconclusive |
| reg_h24\|linear\|S\|val\|mase | vae_rand | 9 | 0.713 | 1.05 | -0.372 | 2.4 | 0.433 | 1 | 0.762 | 4 | 1 | 0 | inconclusive |
| vol_h24\|gbdt\|S\|oot\|mase | vae_rand | 9 | 0.506 | 0.933 | -0.33 | 2.35 | 0.46 | 1 | 0.696 | 3 | 1 | 0 | inconclusive |
| vol_h24\|linear\|S\|oot\|mase | vae_rand | 9 | 1.64 | 1.73 | -0.403 | 4.17 | 0.46 | 1 | 0.762 | 4 | 2 | 0 | inconclusive |
| clf_up_h24_q99\|gbdt\|S\|oot\|auc | vae_rand | 9 | 0.291 | 0.559 | -0.209 | 1.6 | 0.583 | 1 | 0.388 | 1 | 0 | 0 | inconclusive |
| clf_up_h6_q90\|gbdt\|S\|oot\|auc | vae_rand | 9 | 0.209 | 0.21 | -0.398 | 0.805 | 0.583 | 1 | 0.237 | 1 | 0 | 0 | inconclusive |
| clf_down_h24_q10\|linear\|S\|val\|auc | vae_rand | 9 | -1.47 | -2.09 | -4.84 | -0.175 | 1 | 0.635 | 0.762 | 1 | 2 | 0 | inconclusive |
| mc3_h24\|gbdt\|S\|oot\|logloss | vae_rand | 9 | -1.06 | -0.951 | -1.95 | 0.0419 | 1 | 0.635 | 0.743 | 0 | 2 | 0 | inconclusive |
| clf_up_h24_q95\|gbdt\|S\|oot\|auc | vae_rand | 9 | 0.392 | 0.554 | -0.455 | 1.87 | 0.645 | 1 | 0.412 | 1 | 0 | 0 | inconclusive |
| clf_down_h24_q10\|linear\|S\|oot\|auc | vae_rand | 9 | -1.01 | -1.93 | -4.34 | 0.00872 | 1 | 0.711 | 0.762 | 0 | 1 | 0 | inconclusive |
| clf_up_h168_q90\|gbdt\|S\|val\|auc | vae_rand | 9 | -0.591 | -0.478 | -1.04 | 0.121 | 1 | 0.711 | 0.388 | 0 | 1 | 0 | inconclusive |
| clf_up_h1_q90\|gbdt\|S\|oot\|auc | vae_rand | 9 | 0.129 | 0.112 | -0.653 | 0.806 | 0.737 | 1 | 0.237 | 2 | 0 | 0 | inconclusive |
| reg_h24\|linear\|S\|oot\|mase | vae_rand | 9 | 0.218 | 0.701 | -1.75 | 3.21 | 0.737 | 1 | 0.616 | 3 | 3 | 0 | inconclusive |
| vol_h24\|linear\|S\|val\|mase | vae_rand | 9 | 0.00446 | 0.635 | -0.987 | 2.34 | 0.737 | 1 | 0.606 | 3 | 1 | 0 | inconclusive |
| clf_up_h168_q90\|gbdt\|S\|oot\|auc | vae_rand | 9 | -0.888 | -0.599 | -1.51 | 0.302 | 1 | 0.754 | 0.481 | 1 | 2 | 0 | inconclusive |
| clf_up_h24_q95\|gbdt\|S\|val\|auc | vae_rand | 9 | 0.287 | 0.259 | -0.621 | 1.27 | 0.764 | 1 | 0.388 | 1 | 0 | 0 | inconclusive |
| mc3_h24\|linear\|S\|oot\|logloss | vae_rand | 9 | 0.705 | -0.308 | -2.47 | 1.39 | 0.764 | 1 | 0.481 | 2 | 2 | 0 | inconclusive |
| clf_up_h6_q90\|linear\|S\|oot\|auc | vae_rand | 9 | -0.018 | -0.0372 | -1.9 | 1.55 | 0.845 | 1 | 0.412 | 1 | 1 | 0 | inconclusive |
| qreg_h24\|gbdt\|S\|oot\|pinball | vae_rand | 9 | 0.354 | -0.035 | -1.66 | 1.43 | 0.845 | 1 | 0.412 | 2 | 3 | 0 | inconclusive |
| reg_h1\|gbdt\|S\|val\|mase | vae_rand | 9 | 0.429 | 0.134 | -1.15 | 1.3 | 0.845 | 1 | 0.481 | 3 | 1 | 0 | inconclusive |
| qreg_h24\|gbdt\|S\|val\|pinball | vae_rand | 9 | 0.669 | 0.0173 | -1.38 | 1.28 | 0.897 | 1 | 0.412 | 2 | 2 | 0 | inconclusive |
| ms_h24\|linear\|S\|val\|mase | vae_rand | 9 | 0.261 | -0.0681 | -1.6 | 1.42 | 0.914 | 1 | 0.412 | 4 | 3 | 0 | inconclusive |
| qreg_h24\|linear\|S\|oot\|pinball | vae_rand | 9 | 0.813 | -0.191 | -2.06 | 1.36 | 0.914 | 1 | 0.537 | 4 | 2 | 0 | inconclusive |
| clf_up_h24_q95\|linear\|S\|val\|auc | vae_rand | 9 | -0.247 | -0.448 | -4.49 | 3.19 | 0.929 | 1 | 0.481 | 2 | 1 | 0 | inconclusive |
| clf_up_h24_q99\|linear\|S\|oot\|auc | vae_rand | 9 | -0.692 | -1.55 | -6.81 | 1.83 | 0.929 | 1 | 0.606 | 3 | 0 | 0 | inconclusive |

_Showing 40 rows of 52 (rows with a better / worse / same verdict first); all of them — `hypotheses/CS8_global.parquet`._

### CS9. Fidelity vs other stitchers of the same pool and the long-series generators

| unit | comparator | n_datasets | median_z | mean_z | ci_lo | ci_hi | p_better_adj | p_worse_adj | p_equiv_adj | n_better | n_worse | n_same | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F11.1_class_share_logratio | vae_greedy | 9 | 3.74 | 4.6 | 2.06 | 7.57 | 0.106 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| F11.3_multiclass_tvd | vae_greedy | 9 | 1.65 | 2.23 | 1.13 | 3.4 | 0.106 | 1 | 1 | 5 | 0 | 0 | inconclusive |
| F5.3_seam_z_mean | vae_herding | 9 | 4.3 | 5.14 | 3.39 | 7.06 | 0.106 | 1 | 1 | 8 | 0 | 0 | inconclusive |
| F5.3_seam_z_p95 | vae_herding | 9 | 4.71 | 5.83 | 4.01 | 7.83 | 0.106 | 1 | 1 | 8 | 0 | 0 | inconclusive |
| F11.1_class_share_logratio | vae_knn | 9 | 4.29 | 4.77 | 2.18 | 7.65 | 0.106 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| F11.3_multiclass_tvd | vae_knn | 9 | 2.47 | 2.37 | 1.2 | 3.58 | 0.106 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| F11.1_class_share_logratio | vae_mbb | 9 | 4.89 | 5.02 | 2.67 | 7.53 | 0.106 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| F5.3_seam_z_mean | vae_mbb | 9 | 4.3 | 4.8 | 3.55 | 6.24 | 0.106 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| F5.3_seam_z_p95 | vae_mbb | 9 | 5.24 | 6.15 | 4.02 | 8.6 | 0.106 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| F1.5_q01_err | vae_pctsp | 9 | 0.772 | 2.98 | 0.637 | 6.35 | 0.106 | 1 | 1 | 2 | 0 | 0 | inconclusive |
| F3.3_pacf | vae_pctsp | 9 | 2.73 | 3.39 | 1.73 | 5.76 | 0.106 | 1 | 1 | 2 | 0 | 0 | inconclusive |
| F6.3_pred_score_err | vae_pctsp | 9 | 2.86 | 4.01 | 1.61 | 7.46 | 0.106 | 1 | 1 | 3 | 0 | 0 | inconclusive |
| F11.1_class_share_logratio | vae_quilting | 9 | 1.94 | 3.35 | 1.57 | 5.81 | 0.106 | 1 | 1 | 5 | 0 | 0 | inconclusive |
| F3.3_pacf | vae_quilting | 9 | 4.77 | 5.71 | 2.86 | 8.92 | 0.106 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| F11.1_class_share_logratio | timestral | 9 | 50.7 | 75.7 | 29.2 | 140 | 0.106 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| F2.1_ks_d168 | timestral | 9 | 18.8 | 16.3 | 9.18 | 23.6 | 0.106 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| F1.5_q01_err | vae_atsp | 9 | 0.709 | 1.74 | 0.336 | 3.28 | 0.126 | 1 | 1 | 1 | 0 | 1 | inconclusive |
| F3.3_pacf | vae_atsp | 9 | 1.32 | 2.46 | 0.773 | 4.86 | 0.126 | 1 | 1 | 1 | 0 | 0 | inconclusive |
| F3.3_pacf | vae_greedy | 9 | 2.05 | 2.51 | 1.09 | 4.47 | 0.126 | 1 | 1 | 2 | 0 | 0 | inconclusive |
| F2.1_ks_d168 | vae_herding | 9 | 5.83 | 6.58 | 3.62 | 9.97 | 0.126 | 1 | 1 | 8 | 0 | 0 | inconclusive |
| F5.6_cp_at_seams | vae_herding | 8 | 2.53 | 2.53 | 1.95 | 3.09 | 0.126 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| F2.2_vol_ratio_err_d24 | vae_knn | 9 | 1.18 | 2.18 | 0.712 | 3.92 | 0.126 | 1 | 1 | 4 | 0 | 0 | inconclusive |
| F2.1_ks_d168 | vae_mbb | 9 | 5.18 | 6.33 | 3.39 | 9.59 | 0.126 | 1 | 1 | 8 | 1 | 0 | inconclusive |
| F5.6_cp_at_seams | vae_mbb | 8 | 1.84 | 1.98 | 1.58 | 2.45 | 0.126 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| F11.2_rare_share_logratio | timestral | 9 | 11.7 | 18.7 | 6.67 | 35.1 | 0.126 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| F2.2_vol_ratio_err_d24 | timestral | 9 | 6.15 | 29.6 | 10 | 52.7 | 0.126 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| F3.5_log_psd | timestral | 9 | 8.24 | 15.5 | 5.23 | 31.1 | 0.126 | 1 | 1 | 8 | 0 | 0 | inconclusive |
| F8.4_event_by_how | vae_atsp | 9 | 1.02 | 1.1 | 0.412 | 1.85 | 0.138 | 1 | 1 | 2 | 0 | 0 | inconclusive |
| F2.1_w1_d24 | vae_greedy | 9 | 2.08 | 2.15 | 0.789 | 3.9 | 0.138 | 1 | 1 | 5 | 0 | 0 | inconclusive |
| F2.2_vol_ratio_err_d24 | vae_greedy | 9 | 0.885 | 1.57 | 0.49 | 2.8 | 0.138 | 1 | 1 | 4 | 0 | 0 | inconclusive |
| F8.5_cond_event_err | vae_greedy | 9 | 1.43 | 1.63 | 0.671 | 2.76 | 0.138 | 1 | 1 | 5 | 0 | 0 | inconclusive |
| F8.6_cond_future_ks | vae_greedy | 9 | 1.76 | 1.68 | 0.604 | 2.73 | 0.138 | 1 | 1 | 2 | 0 | 0 | inconclusive |
| F2.1_w1_d24 | vae_knn | 9 | 2.1 | 2.8 | 1.09 | 4.91 | 0.138 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| F5.1_ks_seam_vs_real | vae_mbb | 9 | 1.39 | 2.14 | 0.759 | 3.96 | 0.138 | 1 | 1 | 5 | 0 | 0 | inconclusive |
| F5.2_ks_seam_vs_inside | vae_mbb | 9 | 2.54 | 3.21 | 1.12 | 5.85 | 0.138 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| F6.4_mmd_2T | vae_pctsp | 9 | 1.5 | 1.51 | 0.566 | 2.39 | 0.138 | 1 | 1 | 3 | 0 | 1 | inconclusive |
| F3.5_log_psd | vae_quilting | 9 | 3.38 | 3.99 | 1.77 | 6.46 | 0.138 | 1 | 1 | 6 | 1 | 0 | inconclusive |
| F8.1_class_tvd | vae_atsp | 9 | 1.89 | 1.47 | 0.658 | 2.31 | 0.163 | 1 | 1 | 4 | 0 | 1 | inconclusive |
| F11.2_rare_share_logratio | vae_greedy | 9 | 2.18 | 2.23 | 0.799 | 3.79 | 0.163 | 1 | 1 | 4 | 0 | 0 | inconclusive |
| F2.1_ks_d168 | vae_greedy | 9 | 2.1 | 1.91 | 0.74 | 3.16 | 0.163 | 1 | 1 | 3 | 0 | 0 | inconclusive |

_Showing 40 rows of 870 (rows with a better / worse / same verdict first); all of them — `hypotheses/CS9_global.parquet`._

### CS10. TSTR vs other stitchers of the same pool and the long-series generators

| unit | comparator | n_datasets | median_z | mean_z | ci_lo | ci_hi | p_better_adj | p_worse_adj | p_equiv_adj | n_better | n_worse | n_same | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| clf_up_h168_q90\|gbdt\|S\|val\|auc | vae_atsp | 9 | -0.605 | -0.996 | -1.67 | -0.358 | 1 | 0.0959 | 0.851 | 0 | 4 | 0 | inconclusive |
| clf_up_h168_q90\|linear\|S\|val\|auc | vae_atsp | 9 | -2.77 | -2.57 | -3.56 | -1.54 | 1 | 0.0959 | 1 | 0 | 4 | 0 | inconclusive |
| clf_up_h168_q90\|linear\|S\|oot\|auc | vae_herding | 9 | -1.48 | -2.24 | -3.54 | -1 | 1 | 0.0959 | 1 | 0 | 4 | 0 | inconclusive |
| clf_up_h168_q90\|linear\|S\|val\|auc | vae_herding | 9 | -1.29 | -1.9 | -3.21 | -0.836 | 1 | 0.0959 | 1 | 0 | 3 | 0 | inconclusive |
| clf_up_h168_q90\|linear\|S\|oot\|auc | vae_mbb | 9 | -1.88 | -2.13 | -3.26 | -1.01 | 1 | 0.0959 | 1 | 0 | 4 | 0 | inconclusive |
| clf_up_h168_q90\|gbdt\|S\|oot\|auc | vae_quilting | 9 | -1.05 | -2 | -3.6 | -0.918 | 1 | 0.0959 | 1 | 0 | 3 | 0 | inconclusive |
| clf_up_h168_q90\|gbdt\|S\|val\|auc | vae_quilting | 9 | -1.24 | -1.23 | -1.74 | -0.714 | 1 | 0.0959 | 0.986 | 0 | 4 | 0 | inconclusive |
| clf_up_h168_q90\|linear\|S\|oot\|auc | vae_quilting | 9 | -4.53 | -4.88 | -7.58 | -2.59 | 1 | 0.0959 | 1 | 0 | 6 | 0 | inconclusive |
| clf_up_h168_q90\|linear\|S\|val\|auc | vae_quilting | 9 | -2.71 | -3.85 | -6.33 | -1.89 | 1 | 0.0959 | 1 | 0 | 5 | 0 | inconclusive |
| reg_h168\|gbdt\|S\|oot\|mase | timestral | 9 | -3 | -3.38 | -5.4 | -1.64 | 1 | 0.0959 | 1 | 0 | 6 | 0 | inconclusive |
| reg_h168\|linear\|S\|val\|mase | timestral | 9 | -3.16 | -2.91 | -4.35 | -1.67 | 1 | 0.0959 | 1 | 0 | 6 | 0 | inconclusive |
| reg_h24\|linear\|S\|oot\|mase | timestral | 9 | -4.24 | -5.78 | -9.48 | -2.97 | 1 | 0.0959 | 1 | 0 | 9 | 0 | inconclusive |
| reg_h24\|linear\|S\|val\|mase | timestral | 9 | -5.14 | -6.2 | -9.45 | -3.06 | 1 | 0.0959 | 1 | 0 | 8 | 0 | inconclusive |
| clf_up_h168_q90\|linear\|S\|val\|auc | vae_mbb | 9 | -1.32 | -1.66 | -2.94 | -0.645 | 1 | 0.166 | 1 | 0 | 2 | 0 | inconclusive |
| clf_down_h24_q10\|linear\|S\|oot\|auc | diffusion_ts | 9 | -1.54 | -1.28 | -1.86 | -0.607 | 1 | 0.166 | 0.986 | 0 | 4 | 0 | inconclusive |
| mc3_h24\|linear\|S\|oot\|logloss | vae_greedy | 9 | 1.39 | 1.32 | 0.469 | 2.11 | 0.178 | 1 | 1 | 1 | 0 | 0 | inconclusive |
| vol_h24\|linear\|S\|oot\|mase | vae_greedy | 9 | 1.29 | 1.47 | 0.576 | 2.55 | 0.178 | 1 | 0.969 | 5 | 0 | 0 | inconclusive |
| mc3_h24\|linear\|S\|val\|logloss | vae_knn | 9 | 1.14 | 1.53 | 0.469 | 3.17 | 0.178 | 1 | 0.947 | 1 | 0 | 0 | inconclusive |
| vol_h24\|linear\|S\|oot\|mase | vae_knn | 9 | 0.897 | 1.99 | 0.71 | 3.79 | 0.178 | 1 | 0.975 | 4 | 0 | 1 | inconclusive |
| reg_h168\|linear\|S\|val\|mase | vae_mbb | 9 | 2.75 | 2.34 | 1.59 | 3.04 | 0.178 | 1 | 1 | 4 | 0 | 0 | inconclusive |
| clf_up_h168_q90\|gbdt\|S\|val\|auc | timestral | 9 | 1.4 | 1.45 | 0.98 | 1.94 | 0.178 | 1 | 1 | 5 | 0 | 0 | inconclusive |
| clf_up_h24_q99\|gbdt\|S\|oot\|auc | timestral | 9 | 2.19 | 2.32 | 1.09 | 3.84 | 0.178 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| clf_up_h168_q90\|linear\|S\|oot\|auc | vae_atsp | 9 | -2.77 | -2.72 | -4.35 | -1.27 | 1 | 0.187 | 1 | 0 | 5 | 0 | inconclusive |
| clf_up_h6_q90\|linear\|S\|val\|auc | vae_quilting | 9 | -0.603 | -0.774 | -1.46 | -0.217 | 1 | 0.187 | 0.609 | 0 | 1 | 2 | inconclusive |
| clf_up_h24_q90\|mlp\|S\|val\|auc | diffusion_ts | 9 | -2.49 | -2.62 | -5.09 | -0.788 | 1 | 0.187 | 1 | 0 | 4 | 0 | inconclusive |
| reg_h168\|gbdt\|S\|val\|mase | diffusion_ts | 9 | -1.68 | -2.24 | -3.81 | -0.891 | 1 | 0.187 | 1 | 0 | 5 | 0 | inconclusive |
| reg_h168\|gbdt\|S\|val\|mase | timestral | 9 | -2.53 | -2.9 | -4.65 | -1.33 | 1 | 0.187 | 1 | 0 | 6 | 0 | inconclusive |
| mc3_h24\|linear\|S\|val\|logloss | vae_atsp | 9 | 1.43 | 1.53 | 0.536 | 2.73 | 0.208 | 1 | 0.997 | 1 | 0 | 0 | inconclusive |
| mc3_h24\|linear\|S\|val\|logloss | vae_greedy | 9 | 1.17 | 2.02 | 0.654 | 4.08 | 0.208 | 1 | 1 | 2 | 0 | 0 | inconclusive |
| qreg_h24\|linear\|S\|val\|pinball | vae_greedy | 9 | 1.99 | 1.76 | 0.717 | 2.82 | 0.208 | 1 | 1 | 2 | 0 | 0 | inconclusive |
| vol_h24\|linear\|S\|val\|mase | vae_greedy | 9 | 0.717 | 0.804 | 0.129 | 1.41 | 0.208 | 1 | 0.626 | 3 | 0 | 0 | inconclusive |
| mc3_h24\|linear\|S\|oot\|logloss | vae_knn | 9 | 1.05 | 1.23 | 0.352 | 2.14 | 0.208 | 1 | 0.969 | 2 | 0 | 0 | inconclusive |
| mc3_h24\|linear\|S\|oot\|logloss | vae_pctsp | 9 | 1.04 | 2.3 | 0.392 | 5.52 | 0.208 | 1 | 0.947 | 2 | 0 | 0 | inconclusive |
| mc3_h24\|linear\|S\|val\|logloss | vae_pctsp | 9 | 1.13 | 3.09 | 0.528 | 7.07 | 0.208 | 1 | 0.975 | 2 | 0 | 0 | inconclusive |
| clf_up_h168_q90\|gbdt\|S\|oot\|auc | timestral | 9 | 2.05 | 2.22 | 1 | 3.7 | 0.208 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| mc3_h24\|gbdt\|S\|val\|logloss | timestral | 9 | 16.6 | 16.5 | 8.79 | 24.7 | 0.208 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| mc3_h24\|linear\|S\|oot\|logloss | timestral | 9 | 9.46 | 31 | 7.97 | 59.5 | 0.208 | 1 | 1 | 7 | 1 | 0 | inconclusive |
| mc3_h24\|linear\|S\|val\|logloss | timestral | 9 | 8.84 | 21.6 | 5.84 | 45.6 | 0.208 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| clf_up_h168_q90\|gbdt\|S\|val\|auc | vae_greedy | 9 | -0.642 | -0.83 | -1.42 | -0.277 | 1 | 0.24 | 0.669 | 0 | 2 | 0 | inconclusive |
| clf_down_h24_q10\|gbdt\|S\|val\|auc | vae_herding | 9 | -0.392 | -0.943 | -1.92 | -0.163 | 1 | 0.24 | 0.734 | 0 | 1 | 0 | inconclusive |

_Showing 40 rows of 638 (rows with a better / worse / same verdict first); all of them — `hypotheses/CS10_global.parquet`._

### CS11. The method's effect on TSTR across model classes

| unit | p_friedman | nemenyi_cd | n_blocks | share_blocks_same_sign | tasks |
|---|---|---|---|---|---|
| effect_by_model | 0.717 | 1.1 | 9 | 0.778 | clf_up_h24_q90 |

**avg_rank_of_effect**

| model | 0 |
|---|---|
| gbdt | 1.78 |
| linear | 2.11 |
| mlp | 2.11 |


### CS12. The method's effect on TSTR over time (val vs OOT) and across subgroups

| unit | comparator | n_datasets | median_z | p_equiv_adj |
|---|---|---|---|---|
| oot_minus_val\|gbdt | vae_rand | 9 | -0.0301 | 0.186 |
| oot_minus_val\|linear | vae_rand | 9 | -0.228 | 0.475 |
| oot_minus_val\|mlp | vae_rand | 9 | 0.447 | 0.186 |
| oot_minus_val\|gbdt | diffusion_ts | 9 | 0.366 | 0.186 |
| oot_minus_val\|linear | diffusion_ts | 9 | -0.602 | 0.475 |
| oot_minus_val\|mlp | diffusion_ts | 9 | 0.746 | 0.513 |
| oot_minus_val\|gbdt | chronos | 7 | -0.599 | 0.594 |
| oot_minus_val\|linear | chronos | 7 | 0.478 | 0.513 |
| oot_minus_val\|mlp | chronos | 7 | -0.141 | 0.475 |
| oot_minus_val\|gbdt | timesfm | 6 | 0.315 | 0.475 |
| oot_minus_val\|linear | timesfm | 6 | -0.669 | 0.594 |
| oot_minus_val\|mlp | timesfm | 6 | 0.223 | 0.475 |
| oot_minus_val\|gbdt | timestral | 9 | 0.12 | 0.475 |
| oot_minus_val\|linear | timestral | 9 | -0.669 | 0.577 |
| oot_minus_val\|mlp | timestral | 9 | 0.709 | 0.513 |

**subgroups**

| subgroup | model | split | mean_d_auc | p_two_sided | p_bh |
|---|---|---|---|---|---|
| calm | gbdt | oot | -0.0122 | 0.359 | 0.932 |
| calm | gbdt | val | 0.00189 | 0.91 | 1 |
| calm | linear | oot | -0.0425 | 0.426 | 0.932 |
| calm | linear | val | -0.00302 | 0.652 | 0.932 |
| calm | mlp | oot | -0.0162 | 0.496 | 0.932 |
| calm | mlp | val | -0.01 | 1 | 1 |
| mid | gbdt | oot | -0.0029 | 0.82 | 1 |
| mid | gbdt | val | 0.00109 | 1 | 1 |
| mid | linear | oot | 0.00207 | 0.652 | 0.932 |
| mid | linear | val | -0.0212 | 0.25 | 0.932 |
| mid | mlp | oot | 0.00918 | 0.652 | 0.932 |
| mid | mlp | val | 0.000778 | 1 | 1 |
| turbulent | gbdt | oot | -0.00695 | 0.91 | 1 |
| turbulent | gbdt | val | -0.0106 | 0.652 | 0.932 |
| turbulent | linear | oot | -0.0121 | 0.57 | 0.932 |
| turbulent | linear | val | -0.0343 | 0.301 | 0.932 |
| turbulent | mlp | oot | -0.00376 | 1 | 1 |
| turbulent | mlp | val | -0.024 | 0.57 | 0.932 |
| weekday | gbdt | oot | -0.0165 | 0.652 | 0.932 |
| weekday | gbdt | val | 0.000508 | 1 | 1 |
| weekday | linear | oot | -0.0269 | 0.25 | 0.932 |
| weekday | linear | val | -0.02 | 0.203 | 0.932 |
| weekday | mlp | oot | -0.0193 | 0.652 | 0.932 |
| weekday | mlp | val | -0.00872 | 0.426 | 0.932 |
| weekend | gbdt | oot | 0.0145 | 0.652 | 0.932 |
| weekend | gbdt | val | 0.0265 | 0.301 | 0.932 |
| weekend | linear | oot | 0.0195 | 0.734 | 1 |
| weekend | linear | val | 0.0367 | 0.426 | 0.932 |
| weekend | mlp | oot | 0.0381 | 0.0547 | 0.932 |
| weekend | mlp | val | 0.0186 | 0.496 | 0.932 |


### CS13. TSTR of the method vs TRTR

| unit | comparator | n_datasets | median_z | mean_z | ci_lo | ci_hi | p_better_adj | p_worse_adj | p_equiv_adj | n_better | n_worse | n_same | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| clf_down_h24_q10\|gbdt\|val\|auc | TRTR | 9 | -1.97 | -2.22 | -3.6 | -1.16 | 1 | 0.00333 | 1 | 0 | 6 | 0 | worse |
| clf_up_h168_q90\|gbdt\|oot\|auc | TRTR | 9 | -4.93 | -5.4 | -8.4 | -2.86 | 1 | 0.00333 | 1 | 0 | 7 | 0 | worse |
| clf_up_h1_q90\|gbdt\|oot\|auc | TRTR | 9 | -3 | -3.67 | -5.07 | -2.67 | 1 | 0.00333 | 1 | 0 | 9 | 0 | worse |
| clf_up_h1_q90\|gbdt\|val\|auc | TRTR | 9 | -3.61 | -3.74 | -4.89 | -2.64 | 1 | 0.00333 | 1 | 0 | 9 | 0 | worse |
| clf_up_h1_q90\|linear\|val\|auc | TRTR | 9 | -1.96 | -2.43 | -3.54 | -1.43 | 1 | 0.00333 | 1 | 0 | 7 | 0 | worse |
| clf_up_h24_q90\|linear\|val\|auc | TRTR | 9 | -3.65 | -3.95 | -6.14 | -2.13 | 1 | 0.00333 | 1 | 0 | 8 | 0 | worse |
| clf_up_h24_q90\|mlp\|oot\|auc | TRTR | 9 | -2.72 | -3.96 | -6.32 | -2.1 | 1 | 0.00333 | 1 | 0 | 8 | 0 | worse |
| clf_up_h24_q90\|mlp\|val\|auc | TRTR | 9 | -3.46 | -4.47 | -7.16 | -2.37 | 1 | 0.00333 | 1 | 0 | 8 | 0 | worse |
| clf_up_h24_q95\|gbdt\|val\|auc | TRTR | 9 | -1.83 | -2.06 | -3.03 | -1.18 | 1 | 0.00333 | 1 | 0 | 7 | 0 | worse |
| clf_up_h24_q95\|linear\|val\|auc | TRTR | 9 | -2.38 | -2.78 | -4.09 | -1.68 | 1 | 0.00333 | 1 | 0 | 7 | 0 | worse |
| clf_up_h6_q90\|linear\|val\|auc | TRTR | 9 | -1.48 | -3.25 | -5.36 | -1.48 | 1 | 0.00333 | 1 | 0 | 7 | 0 | worse |
| mc3_h24\|gbdt\|val\|logloss | TRTR | 9 | -4.63 | -4.72 | -6.13 | -3.36 | 1 | 0.00333 | 1 | 0 | 8 | 0 | worse |
| mc3_h24\|linear\|oot\|logloss | TRTR | 9 | -2.78 | -2.89 | -3.51 | -2.35 | 1 | 0.00333 | 1 | 0 | 9 | 0 | worse |
| mc3_h24\|linear\|val\|logloss | TRTR | 9 | -2.53 | -3.06 | -3.97 | -2.28 | 1 | 0.00333 | 1 | 0 | 9 | 0 | worse |
| ms_h24\|gbdt\|oot\|mase | TRTR | 9 | -4.4 | -7.74 | -11.5 | -4.35 | 1 | 0.00333 | 1 | 0 | 9 | 0 | worse |
| ms_h24\|gbdt\|val\|mase | TRTR | 9 | -4.21 | -6.16 | -10.1 | -3.16 | 1 | 0.00333 | 1 | 0 | 9 | 0 | worse |
| ms_h24\|linear\|oot\|mase | TRTR | 9 | -5.4 | -7.42 | -11.8 | -4.66 | 1 | 0.00333 | 1 | 0 | 9 | 0 | worse |
| ms_h24\|linear\|val\|mase | TRTR | 9 | -5.26 | -5.86 | -9.04 | -3.4 | 1 | 0.00333 | 1 | 0 | 9 | 0 | worse |
| qreg_h24\|gbdt\|oot\|pinball | TRTR | 9 | -4.1 | -6.62 | -9.89 | -3.7 | 1 | 0.00333 | 1 | 0 | 9 | 0 | worse |
| qreg_h24\|gbdt\|val\|pinball | TRTR | 9 | -3.18 | -6.81 | -11.1 | -3.41 | 1 | 0.00333 | 1 | 0 | 9 | 0 | worse |
| qreg_h24\|linear\|oot\|pinball | TRTR | 9 | -4.02 | -4.4 | -5.8 | -3.17 | 1 | 0.00333 | 1 | 0 | 9 | 0 | worse |
| qreg_h24\|linear\|val\|pinball | TRTR | 9 | -3.56 | -4.32 | -5.7 | -2.94 | 1 | 0.00333 | 1 | 0 | 9 | 0 | worse |
| reg_h168\|gbdt\|oot\|mase | TRTR | 9 | -3.19 | -3.84 | -5.52 | -2.41 | 1 | 0.00333 | 1 | 0 | 8 | 0 | worse |
| reg_h168\|gbdt\|val\|mase | TRTR | 9 | -1.88 | -2.82 | -4.51 | -1.41 | 1 | 0.00333 | 1 | 0 | 7 | 0 | worse |
| reg_h168\|linear\|oot\|mase | TRTR | 9 | -3.59 | -4.61 | -6.94 | -2.72 | 1 | 0.00333 | 1 | 0 | 9 | 0 | worse |
| reg_h168\|linear\|val\|mase | TRTR | 9 | -2.98 | -3.31 | -4.61 | -2.22 | 1 | 0.00333 | 1 | 0 | 8 | 0 | worse |
| reg_h1\|gbdt\|oot\|mase | TRTR | 9 | -5.41 | -8.59 | -14.4 | -3.2 | 1 | 0.00333 | 1 | 0 | 8 | 0 | worse |
| reg_h1\|gbdt\|val\|mase | TRTR | 9 | -4.5 | -6.64 | -10.9 | -3.49 | 1 | 0.00333 | 1 | 0 | 9 | 0 | worse |
| reg_h1\|linear\|oot\|mase | TRTR | 9 | -3.98 | -4.13 | -6.18 | -2.4 | 1 | 0.00333 | 1 | 0 | 8 | 0 | worse |
| reg_h24\|gbdt\|oot\|mase | TRTR | 9 | -3.61 | -5.24 | -7.79 | -3.09 | 1 | 0.00333 | 1 | 0 | 9 | 0 | worse |
| reg_h24\|gbdt\|val\|mase | TRTR | 9 | -3.07 | -4.29 | -6.32 | -2.58 | 1 | 0.00333 | 1 | 0 | 9 | 0 | worse |
| reg_h24\|linear\|oot\|mase | TRTR | 9 | -7.21 | -7.23 | -10.8 | -4.38 | 1 | 0.00333 | 1 | 0 | 9 | 0 | worse |
| reg_h24\|linear\|val\|mase | TRTR | 9 | -5.72 | -6.4 | -9.71 | -3.3 | 1 | 0.00333 | 1 | 0 | 8 | 0 | worse |
| vol_h24\|gbdt\|oot\|mase | TRTR | 9 | -5.86 | -8.23 | -14.3 | -3.65 | 1 | 0.00333 | 1 | 0 | 8 | 0 | worse |
| clf_down_h24_q10\|gbdt\|oot\|auc | TRTR | 9 | -2.16 | -1.84 | -2.6 | -1.08 | 1 | 0.00566 | 1 | 0 | 6 | 0 | worse |
| clf_up_h24_q90\|gbdt\|oot\|auc | TRTR | 9 | -3.63 | -5.66 | -9.88 | -2.23 | 1 | 0.00566 | 1 | 0 | 8 | 0 | worse |
| clf_up_h24_q90\|gbdt\|val\|auc | TRTR | 9 | -3.5 | -3.69 | -5.41 | -2.11 | 1 | 0.00566 | 1 | 0 | 8 | 0 | worse |
| clf_up_h6_q90\|gbdt\|oot\|auc | TRTR | 9 | -1.91 | -2.78 | -4.98 | -1.16 | 1 | 0.00566 | 1 | 0 | 6 | 0 | worse |
| clf_up_h6_q90\|gbdt\|val\|auc | TRTR | 9 | -1.67 | -1.63 | -2.18 | -1.03 | 1 | 0.00566 | 1 | 0 | 8 | 0 | worse |
| mc3_h24\|gbdt\|oot\|logloss | TRTR | 9 | -4.5 | -3.54 | -4.72 | -2.21 | 1 | 0.00566 | 1 | 0 | 8 | 0 | worse |

_Showing 40 rows of 58 (rows with a better / worse / same verdict first); all of them — `hypotheses/CS13_global.parquet`._

**transfer_ratio_case_cell**

| method | beijing_pm25 | bike | bitcoin | electricity | ett | household | jena | metro | pjm |
|---|---|---|---|---|---|---|---|---|---|
| chronos |  | 0.884 |  |  | 0.085 | 0 | 0.811 | 0.971 | 0.327 |
| diffusion_ts | 1.68 | 0.963 |  | 0.806 | 0.978 | 0.919 | 0.379 | 0.972 | 0.601 |
| timesfm |  | 0.893 |  | 0.94 | 0 |  | 0 | 1.05 | 0.718 |
| timestral | -2.14 | 0.915 |  | 0.548 | 0 | 0 | 0 | 1.07 | 0.486 |
| vae_atsp | -0.012 | 0.498 |  | 0.167 | 0.766 | 0.678 | 1.66 | 0.905 | 0.356 |
| vae_greedy | 1.06 | 0.433 |  | 0.141 | 0.773 | 0.6 | 1.81 | 0.872 | 0.395 |
| vae_herding | -1.01 | 0.613 |  | -0.012 | 0.777 | 0.809 | 1.94 | 0.762 | 0.53 |
| vae_knn | 0.857 | 0.442 |  | 0.131 | 0.772 | 0.632 | 1.79 | 0.89 | 0.343 |
| vae_mbb | 0.16 | 0.514 |  | 0 | 0.815 | 0.8 | 1.83 | 0.858 | 0.2 |
| vae_pctsp | -0.077 | 0.472 |  | 0.159 | 0.741 | 0.706 | 1.92 | 0.888 | 0.423 |
| vae_quilting | 1.47 | 0.529 |  | 0.337 | 0.74 | 0.722 | 1.73 | 0.918 | 0.384 |
| vae_rand | -0.226 | 0.533 |  | -0.007 | 0.857 | 0.786 | 2.01 | 0.844 | 0.259 |
| vae_zseries | -1.14 | 0.489 |  | 0.257 | 0.645 | 0.522 | 1.65 | 0.847 | 0.521 |
| vae_zseries_quilt | -0.147 | 0.226 |  | 0.029 | 0.639 | 0.393 | 1.69 | 0.634 | 0.323 |
| vae_zseries_wsola | -0.249 | 0.309 |  | 0.316 | 0.649 | 0.529 | 1.57 | 0.779 | 0.584 |
| vae_zseries_xfade | -0.108 | 0.232 |  | 0.037 | 0.567 | 0.386 | 1.74 | 0.603 | 0.354 |


**transfer_ratio_by_task**

| method | clf_down_h24_q10 | clf_up_h168_q90 | clf_up_h1_q90 | clf_up_h24_q90 | clf_up_h24_q95 | clf_up_h24_q99 | clf_up_h6_q90 | mc3_h24 | ms_h24 | qreg_h24 | reg_h1 | reg_h168 | reg_h24 | vol_h24 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| chronos | 0.417 | 0.255 | 0.854 | 0.472 | 0.395 | 0.414 | 0.777 | 0.5 | 0.82 | 0.726 | 0.808 | 0.838 | 0.885 | 0.605 |
| diffusion_ts | 0.957 | 0.629 | 0.938 | 0.787 | 0.751 | 0.14 | 0.84 | 0.545 | 0.711 | 0.758 | 0.798 | 0.956 | 0.834 | 0.786 |
| timesfm | 0.722 | 0.56 | 0.935 | 0.648 | 0.745 | 0.381 | 0.922 | 0.379 | 0.879 | 0.81 | 0.827 | 0.988 | 0.964 | 0.717 |
| timestral | 0 | -0.166 | 0.785 | 0 | 0 | -0.005 | 0.323 | 0.326 | 0.824 | 0.677 | 0.752 | 0.977 | 0.941 | 0.67 |
| vae_atsp | 0.83 | 0.394 | 0.89 | 0.586 | 0.612 | 0.663 | 0.827 | 0.626 | 0.642 | 0.558 | 0.83 | 0.592 | 0.608 | 0.479 |
| vae_greedy | 0.802 | 0.355 | 0.9 | 0.654 | 0.606 | 0.779 | 0.85 | 0.597 | 0.618 | 0.536 | 0.825 | 0.647 | 0.563 | 0.473 |
| vae_herding | 0.877 | 0.407 | 0.918 | 0.612 | 0.626 | 0.681 | 0.853 | 0.697 | 0.709 | 0.645 | 0.794 | 0.405 | 0.648 | 0.551 |
| vae_knn | 0.811 | 0.263 | 0.894 | 0.651 | 0.592 | 0.673 | 0.841 | 0.6 | 0.616 | 0.533 | 0.823 | 0.541 | 0.571 | 0.468 |
| vae_mbb | 0.819 | 0.335 | 0.892 | 0.606 | 0.576 | 0.612 | 0.817 | 0.63 | 0.64 | 0.564 | 0.806 | 0.447 | 0.559 | 0.473 |
| vae_pctsp | 0.799 | 0.354 | 0.898 | 0.613 | 0.592 | 0.658 | 0.843 | 0.599 | 0.623 | 0.529 | 0.819 | 0.576 | 0.571 | 0.552 |
| vae_quilting | 0.812 | 0.525 | 0.909 | 0.652 | 0.596 | 0.704 | 0.872 | 0.658 | 0.657 | 0.582 | 0.775 | 0.583 | 0.625 | 0.51 |
| vae_rand | 0.825 | 0.407 | 0.901 | 0.62 | 0.632 | 0.633 | 0.82 | 0.628 | 0.631 | 0.549 | 0.807 | 0.431 | 0.542 | 0.462 |
| vae_zseries | 0.811 | 0.139 | 0.897 | 0.542 | 0.572 | 0.72 | 0.837 | 0.645 | 0.684 | 0.629 | 0.85 | 0.588 | 0.659 | 0.51 |
| vae_zseries_quilt | 0.805 | 0.104 | 0.898 | 0.442 | 0.393 | 0.58 | 0.836 | 0.607 | 0.647 | 0.589 | 0.816 | 0.422 | 0.588 | 0.508 |
| vae_zseries_wsola | 0.761 | 0.328 | 0.91 | 0.526 | 0.515 | 0.68 | 0.829 | 0.642 | 0.654 | 0.626 | 0.778 | 0.533 | 0.653 | 0.617 |
| vae_zseries_xfade | 0.789 | 0.109 | 0.911 | 0.428 | 0.392 | 0.581 | 0.816 | 0.613 | 0.644 | 0.587 | 0.782 | 0.422 | 0.599 | 0.63 |


**rowlevel**

| dataset | model | split | comparator | n_seeds | n_rows | diff | boot_ci_lo | boot_ci_hi | p_boot | p_boot_bh |
|---|---|---|---|---|---|---|---|---|---|---|
| beijing_pm25 | gbdt | oot | real | 10 | 1944 | -0.176 | -0.251 | -0.0301 | 0.012 | 0.0223 |
| beijing_pm25 | gbdt | val | real | 10 | 2083 | -0.184 | -0.372 | 0.236 | 0.292 | 0.385 |
| beijing_pm25 | linear | oot | real | 10 | 1944 | -0.0825 | -0.214 | 0.0883 | 0.404 | 0.506 |
| beijing_pm25 | linear | val | real | 10 | 2083 | -0.166 | -0.341 | 0.297 | 0.36 | 0.463 |
| beijing_pm25 | mlp | oot | real | 10 | 1944 | -0.0929 | -0.217 | 0.0499 | 0.216 | 0.299 |
| beijing_pm25 | mlp | val | real | 10 | 2083 | -0.267 | -0.478 | 0.118 | 0.148 | 0.228 |
| bike | gbdt | oot | real | 10 | 2140 | -0.299 | -0.381 | -0.224 | 0 | 0 |
| bike | gbdt | val | real | 10 | 2140 | -0.26 | -0.302 | -0.212 | 0 | 0 |
| bike | linear | oot | real | 10 | 2140 | -0.131 | -0.167 | -0.0669 | 0 | 0 |
| bike | linear | val | real | 10 | 2140 | -0.105 | -0.149 | -0.0685 | 0 | 0 |
| bike | mlp | oot | real | 10 | 2140 | -0.234 | -0.294 | -0.16 | 0 | 0 |
| bike | mlp | val | real | 10 | 2140 | -0.209 | -0.245 | -0.165 | 0 | 0 |
| bitcoin | gbdt | oot | real | 10 | 2140 | -0.0152 | -0.144 | 0.146 | 0.892 | 0.909 |
| bitcoin | gbdt | val | real | 10 | 2140 | 0.0902 | -0.0873 | 0.227 | 0.432 | 0.518 |
| bitcoin | linear | oot | real | 10 | 2140 | -0.00846 | -0.072 | 0.0498 | 0.548 | 0.617 |
| bitcoin | linear | val | real | 10 | 2140 | 0.0158 | -0.0392 | 0.0967 | 0.528 | 0.607 |
| bitcoin | mlp | oot | real | 10 | 2140 | -0.162 | -0.269 | -0.0588 | 0 | 0 |
| bitcoin | mlp | val | real | 10 | 2140 | -0.0771 | -0.211 | 0.032 | 0.144 | 0.228 |
| electricity | gbdt | oot | real | 10 | 2140 | -0.113 | -0.208 | -0.0472 | 0 | 0 |
| electricity | gbdt | val | real | 10 | 2140 | -0.178 | -0.233 | -0.113 | 0 | 0 |
| electricity | linear | oot | real | 10 | 2140 | -0.178 | -0.279 | -0.0823 | 0 | 0 |
| electricity | linear | val | real | 10 | 2140 | -0.184 | -0.231 | -0.125 | 0 | 0 |
| electricity | mlp | oot | real | 10 | 2140 | -0.184 | -0.288 | -0.0987 | 0 | 0 |
| electricity | mlp | val | real | 10 | 2140 | -0.304 | -0.369 | -0.208 | 0 | 0 |
| ett | gbdt | oot | real | 10 | 2140 | -0.0318 | -0.114 | 0.0153 | 0.216 | 0.299 |
| ett | gbdt | val | real | 10 | 2140 | -0.00559 | -0.0686 | 0.0749 | 0.964 | 0.964 |
| ett | linear | oot | real | 10 | 2140 | -0.0896 | -0.164 | -0.0512 | 0 | 0 |
| ett | linear | val | real | 10 | 2140 | -0.0849 | -0.178 | 0.0227 | 0.112 | 0.195 |
| ett | mlp | oot | real | 10 | 2140 | -0.0746 | -0.175 | -0.0217 | 0.004 | 0.008 |
| ett | mlp | val | real | 10 | 2140 | -0.048 | -0.0987 | 0.0176 | 0.168 | 0.252 |
| household | gbdt | oot | real | 10 | 1867 | -0.116 | -0.171 | -0.0648 | 0 | 0 |
| household | gbdt | val | real | 10 | 2140 | -0.134 | -0.201 | -0.0419 | 0 | 0 |
| household | linear | oot | real | 10 | 1867 | -0.108 | -0.151 | -0.0453 | 0 | 0 |
| household | linear | val | real | 10 | 2140 | -0.164 | -0.243 | -0.0682 | 0 | 0 |
| household | mlp | oot | real | 10 | 1867 | -0.0985 | -0.142 | -0.0372 | 0.004 | 0.008 |
| household | mlp | val | real | 10 | 2140 | -0.181 | -0.259 | -0.0744 | 0 | 0 |
| jena | gbdt | oot | real | 10 | 1922 | 0.0139 | -0.176 | 0.128 | 0.884 | 0.909 |
| jena | gbdt | val | real | 10 | 2140 | -0.0445 | -0.165 | 0.0251 | 0.184 | 0.269 |
| jena | linear | oot | real | 10 | 1922 | 0.0928 | -0.0311 | 0.203 | 0.124 | 0.209 |
| jena | linear | val | real | 10 | 2140 | -0.0784 | -0.199 | 0.0373 | 0.144 | 0.228 |


### CS14. Computational cost of the method vs the others

| unit | comparator | median_ratio_comp_over_method | ci_ratio_lo | ci_ratio_hi | p_method_faster | p_method_slower | p_equiv_10pct | n_datasets | p_method_faster_adj | p_method_slower_adj |
|---|---|---|---|---|---|---|---|---|---|---|
| total_wall_time | chronos | 0.606 | 0.548 | 0.663 | 1 | 0.00781 | 1 | 7 | 1 | 0.0391 |
| total_wall_time | diffusion_ts | 42.9 | 34.9 | 45.6 | 0.00195 | 1 | 1 | 9 | 0.0234 | 1 |
| total_wall_time | timesfm | 0.17 | 0.15 | 0.183 | 1 | 0.0156 | 1 | 6 | 1 | 0.0625 |
| total_wall_time | timestral | 0.052 | 0.0492 | 0.0564 | 1 | 0.00195 | 1 | 9 | 1 | 0.0234 |
| total_wall_time | vae_atsp | 1.12 | 1.11 | 1.2 | 0.00195 | 1 | 0.99 | 9 | 0.0234 | 1 |
| total_wall_time | vae_greedy | 0.965 | 0.963 | 0.967 | 1 | 0.00195 | 0.00195 | 9 | 1 | 0.0234 |
| total_wall_time | vae_herding | 0.966 | 0.963 | 0.967 | 1 | 0.00195 | 0.00195 | 9 | 1 | 0.0234 |
| total_wall_time | vae_knn | 0.965 | 0.963 | 0.967 | 1 | 0.00195 | 0.00195 | 9 | 1 | 0.0234 |
| total_wall_time | vae_mbb | 0.965 | 0.963 | 0.967 | 1 | 0.00195 | 0.00195 | 9 | 1 | 0.0234 |
| total_wall_time | vae_pctsp | 1.41 | 1.39 | 1.45 | 0.00195 | 1 | 1 | 9 | 0.0234 | 1 |
| total_wall_time | vae_quilting | 0.965 | 0.963 | 0.967 | 1 | 0.00195 | 0.00195 | 9 | 1 | 0.0234 |
| total_wall_time | vae_rand | 0.965 | 0.963 | 0.967 | 1 | 0.00195 | 0.00195 | 9 | 1 | 0.0234 |

**hardware**: ['NVIDIA L4']

### CS15. Moderators of the method's effect (exploratory)

| effect | descriptor | spearman | p | n | p_bh |
|---|---|---|---|---|---|
| CS2:vae_rand | acf24 | 0.0167 | 0.966 | 9 | 0.978 |
| CS2:vae_rand | acf168 | 0.15 | 0.7 | 9 | 0.978 |
| CS2:vae_rand | kurt_d24 | 0.35 | 0.356 | 9 | 0.958 |
| CS2:vae_rand | volclust | 0.7 | 0.0358 | 9 | 0.228 |
| CS2:vae_rand | trend | -0.183 | 0.637 | 9 | 0.978 |
| CS2:vae_rand | nan_share | -0.365 | 0.334 | 9 | 0.956 |
| CS4:vae_rand | acf24 | 0.05 | 0.898 | 9 | 0.978 |
| CS4:vae_rand | acf168 | 0.283 | 0.46 | 9 | 0.978 |
| CS4:vae_rand | kurt_d24 | 0.583 | 0.0992 | 9 | 0.433 |
| CS4:vae_rand | volclust | -0.0167 | 0.966 | 9 | 0.978 |
| CS4:vae_rand | trend | -0.0167 | 0.966 | 9 | 0.978 |
| CS4:vae_rand | nan_share | -0.274 | 0.476 | 9 | 0.978 |
| CS7:vae_rand | acf24 | 0.0667 | 0.865 | 9 | 0.978 |
| CS7:vae_rand | acf168 | 0.117 | 0.765 | 9 | 0.978 |
| CS7:vae_rand | kurt_d24 | 0.233 | 0.546 | 9 | 0.978 |
| CS7:vae_rand | volclust | 0.567 | 0.112 | 9 | 0.458 |
| CS7:vae_rand | trend | -0.0667 | 0.865 | 9 | 0.978 |
| CS7:vae_rand | nan_share | -0.228 | 0.555 | 9 | 0.978 |
| CS10:chronos | acf24 | 0.0714 | 0.879 | 7 | 0.978 |
| CS10:chronos | acf168 | -0.75 | 0.0522 | 7 | 0.271 |
| CS10:chronos | kurt_d24 | -0.857 | 0.0137 | 7 | 0.227 |
| CS10:chronos | volclust | 0.107 | 0.819 | 7 | 0.978 |
| CS10:chronos | trend | -0.25 | 0.589 | 7 | 0.978 |
| CS10:chronos | nan_share | 0.408 | 0.363 | 7 | 0.958 |
| CS10:diffusion_ts | acf24 | 0.467 | 0.205 | 9 | 0.656 |
| CS10:diffusion_ts | acf168 | 0 | 1 | 9 | 1 |
| CS10:diffusion_ts | kurt_d24 | -0.617 | 0.0769 | 9 | 0.355 |
| CS10:diffusion_ts | volclust | 0.417 | 0.265 | 9 | 0.813 |
| CS10:diffusion_ts | trend | 0.7 | 0.0358 | 9 | 0.228 |
| CS10:diffusion_ts | nan_share | -0.525 | 0.147 | 9 | 0.508 |
| CS10:timesfm | acf24 | -0.371 | 0.468 | 6 | 0.978 |
| CS10:timesfm | acf168 | -0.943 | 0.0048 | 6 | 0.109 |
| CS10:timesfm | kurt_d24 | -0.943 | 0.0048 | 6 | 0.109 |
| CS10:timesfm | volclust | -0.143 | 0.787 | 6 | 0.978 |
| CS10:timesfm | trend | 0.829 | 0.0416 | 6 | 0.246 |
| CS10:timestral | acf24 | -0.15 | 0.7 | 9 | 0.978 |
| CS10:timestral | acf168 | -0.717 | 0.0298 | 9 | 0.228 |
| CS10:timestral | kurt_d24 | -0.833 | 0.00527 | 9 | 0.109 |
| CS10:timestral | volclust | 0.15 | 0.7 | 9 | 0.978 |
| CS10:timestral | trend | -0.0333 | 0.932 | 9 | 0.978 |

_Showing 40 rows of 83; all of them — `hypotheses/CS15_global.parquet`._
