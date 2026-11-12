# Benchmark report

Datasets: beijing_pm25, bike, bitcoin, electricity, ett, household, jena, metro, pjm. Seeds: 10. α = 0.05. Leakage (Config.leaked): `chronos` on electricity, beijing_pm25; `timesfm` on beijing_pm25, household, bitcoin. Verdict of a comparison "A vs B": better / worse (A better / worse than B) / same (equivalence, TOST) / inconclusive. Effects are in noise units — divided by the smallest effect size of interest (SESOI: the median |zedge_rand − zedge_rand_b| on one pool — or, where zedge_rand_b is not run (min), the between-seed spread of zedge_rand — or the method's between-seed spread, see HYPOTHESES.md §2). Utility: TSTR (training on synthetic data only) vs TRTR (training on real data), tested on the real val / OOT; transfer ratio = 1 — synthetic data train the model as well as real data. Overall leaderboard — `OVERALL.md`; ranking of every method in every slice — `LEADERBOARD.md`; values of the metrics by slice — `METRIC_VALUES.md` (this folder). Tables of the tests — `hypotheses/`.

## Overall leaderboard

Fidelity on the core metrics (each criterion against train, val and OOT) and utility (TSTR classification and regression, val and OOT), equal weights; noise-aware ranks; privacy and cost not included. Composition, columns and the robustness checks — `OVERALL.md`.

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon | fidelity_rank | utility_rank | norm_overall | memorisation_flag |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| zedge_quilting | optimised selection | 8.11 | 7.04 | 9.16 | 0.787 | 0.963 |  | True | 8.29 | 7.93 | 0.462 | False |
| zedge_zseries | optimised selection | 8.7 | 7.98 | 9.43 | 0.114 | 0.641 | 0.328 | True | 8.78 | 8.62 | 0.26 | False |
| zedge_greedy | optimised selection | 8.82 | 7.84 | 9.89 | 0.001 | 0.533 | 0.328 | True | 9.04 | 8.6 | 0.284 | False |
| zedge_pctsp | optimised selection | 8.94 | 7.83 | 10.1 | 0.003 | 0.282 | 0.322 | True | 9.15 | 8.73 | 0.251 | False |
| zedge_ts_ar | long-series generator | 9.1 | 7.39 | 10.9 | 0.08 | 0.303 | 0.328 | True | 10.1 | 8.12 | 0.506 | False |
| zedge_atsp | optimised selection | 9.12 | 7.55 | 10.8 | 0.015 | 0.229 | 0.328 | True | 9.15 | 9.09 | 0.302 | False |
| zedge_knn | optimised selection | 9.18 | 8.27 | 10.2 | 0 | 0.025 | 0.191 | True | 9.3 | 9.06 | 0.388 | False |
| zedge_ts_long | long-series generator | 9.37 | 8 | 10.8 | 0 | 0.024 | 0.223 | True | 9.46 | 9.27 | 0.348 | False |
| zedge_herding | optimised selection | 10.4 | 9.13 | 11.7 | 0 | 0 | 0.0879 | True | 10.3 | 10.5 | 0.047 | False |
| zedge_mbb | optimised selection | 10.5 | 9.15 | 12.1 | 0 | 0 | 0.0645 | True | 10.5 | 10.6 | 0.0562 | False |
| zedge_rand | random selection | 10.7 | 9.15 | 12.3 | 0 | 0 | 0.0547 | True | 10.5 | 10.9 | 0 | False |
| vae_herding | optimised selection | 13.7 | 13.1 | 14.3 | 0 | 0 | 0.0449 | False | 13.1 | 14.3 | 0.302 | False |
| vae_zseries | optimised selection | 13.8 | 12.3 | 15.4 | 0 | 0 | 0.0547 | True | 13.4 | 14.3 | 0.34 | False |
| diffusion_ts | long-series generator | 13.9 | 12 | 15.5 | 0 | 0 | 0.0449 | False | 14.4 | 13.4 | 0.153 | False |
| timesfm | long-series generator | 14.5 | 12.7 | 16.2 | 0 | 0 | 0.125 | True | 15.3 | 13.7 | -0.125 | False |
| vae_quilting | optimised selection | 14.6 | 12.8 | 16.3 | 0 | 0 | 0.0547 | True | 14.2 | 14.9 | 0.125 | False |
| vae_pctsp | optimised selection | 15.3 | 13.8 | 16.7 | 0 | 0 | 0.0449 | False | 14.8 | 15.8 | 0.146 | False |
| vae_atsp | optimised selection | 15.4 | 13.4 | 17.2 | 0 | 0 | 0.0449 | False | 15.2 | 15.6 | 0.153 | False |
| vae_greedy | optimised selection | 15.7 | 14 | 17.3 | 0 | 0 | 0.0449 | False | 15.5 | 15.8 | 0.0733 | False |
| chronos | long-series generator | 15.9 | 14.2 | 17.6 | 0 | 0 | 0.0781 | True | 16.4 | 15.5 | 0.545 | False |
| vae_knn | optimised selection | 16.1 | 14.3 | 17.8 | 0 | 0 | 0.0449 | False | 16 | 16.3 | 0.0861 | False |
| vae_mbb | optimised selection | 16.5 | 14.6 | 18.4 | 0 | 0 | 0.0449 | False | 16.3 | 16.7 | 0.0773 | False |
| vae_rand | random selection | 16.7 | 14.7 | 18.5 | 0 | 0 | 0.0449 | False | 16.6 | 16.8 | 0 | False |
| timestral | long-series generator | 16.9 | 15.7 | 18.2 | 0 | 0 | 0.0449 | False | 17.4 | 16.5 | -0.132 | False |


Sensitivity variants:

| variant | text | first | tau_vs_main | main_first_place |
|---|---|---|---|---|
| main | the leaderboard: core metrics, fidelity against train + val + OOT, noise-aware ranks | zedge_quilting | 1 | 1 |
| plain_ranks | ordinary average ranks (no ties within the noise) | zedge_quilting | 0.993 | 1 |
| fidelity_train | fidelity against train only | zedge_quilting | 0.978 | 1 |
| fidelity_holdout | fidelity against val + OOT only | zedge_quilting | 0.964 | 1 |
| no_unchecked | without F5.7 (seams, no anchor) and F6.1 against val (noise) | zedge_quilting | 0.949 | 1 |
| all_metrics | every fidelity metric instead of the core set | zedge_quilting | 0.928 | 1 |
| common_datasets | only the datasets where every method is ranked | zedge_quilting | 0.942 | 1 |


## Confirmatory inference (C1–C4; TSTR, linear model, OOT; one classification and regression task; Holm over the whole family)

| test | cell | comparison | n_datasets | median_z | ci_lo | ci_hi | p_two_sided | p_holm | p_equiv_holm | n_better | n_worse | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C1 methods differ | clf_up_h24_q90\|linear\|oot | Friedman, all methods | 9 |  |  |  | 0.00138 | 0.0124 | 1 |  |  | differ |
| C2 long vs assembly | clf_up_h24_q90\|linear\|oot | diffusion_ts vs assembly_median | 9 | 0.815 | -1.1 | 2.55 | 0.57 | 1 | 1 | 4 | 3 | inconclusive |
| C2 long vs assembly | clf_up_h24_q90\|linear\|oot | chronos vs assembly_median | 7 | -0.698 | -25.5 | -0.0234 | 0.0781 | 0.391 | 1 | 0 | 3 | inconclusive |
| C3 selection | clf_up_h24_q90\|linear\|oot | optimised selection (mean) vs random | 9 | 0.682 | 0.014 | 1.37 | 0.0977 | 0.391 | 1 | 3 | 0 | inconclusive |
| C4 seam processing | clf_up_h24_q90\|linear\|oot | any joiner vs none (all paths) | 9 | -1.73 | -2.53 | -0.548 | 0.0547 | 0.383 | 1 | 0 | 5 | inconclusive |
| C1 methods differ | reg_h24\|linear\|oot | Friedman, all methods | 9 |  |  |  | 1.4e-08 | 1.4e-07 | 1 |  |  | differ |
| C2 long vs assembly | reg_h24\|linear\|oot | diffusion_ts vs assembly_median | 9 | -0.662 | -1.76 | 3.78 | 0.652 | 1 | 1 | 2 | 2 | inconclusive |
| C2 long vs assembly | reg_h24\|linear\|oot | chronos vs assembly_median | 7 | -0.551 | -2.57 | 2.5 | 0.688 | 1 | 1 | 1 | 2 | inconclusive |
| C3 selection | reg_h24\|linear\|oot | optimised selection (mean) vs random | 9 | 1.31 | 0.89 | 2.44 | 0.00391 | 0.0312 | 1 | 5 | 0 | better |
| C4 seam processing | reg_h24\|linear\|oot | any joiner vs none (all paths) | 9 | -3.02 | -5.14 | -1.02 | 0.0547 | 0.383 | 1 | 0 | 5 | inconclusive |


## The four rankings (RQ1)

Composition of each ranking, the meaning of every column and the privacy and cost tables — `LEADERBOARD.md`.

- `holdout_clf` — **Fidelity: val + OOT; utility: classification**. Fidelity domain — the criteria distribution (F1, F2, F12), dependence (F3, F4), windows (F6, F9), long structure (F7), target (F8, F11), seams (F5), each against val and OOT (each criterion is the mean of the two). Utility domain — TSTR classification (binary and multiclass tasks), primary metric of each task type, tested on val and OOT. Rank = mean of the two domains with equal weight. Not included: privacy (F10), time, memory.
- `holdout_reg` — **Fidelity: val + OOT; utility: regression**. Fidelity domain — the criteria distribution (F1, F2, F12), dependence (F3, F4), windows (F6, F9), long structure (F7), target (F8, F11), seams (F5), each against val and OOT (each criterion is the mean of the two). Utility domain — TSTR regression (point, quantile, multi-step and volatility tasks), primary metric of each task type, tested on val and OOT. Rank = mean of the two domains with equal weight. Not included: privacy (F10), time, memory.
- `train_clf` — **Fidelity: train; utility: classification**. Fidelity domain — the criteria distribution (F1, F2, F12), dependence (F3, F4), windows (F6, F9), long structure (F7), target (F8, F11), seams (F5), each against train. Utility domain — TSTR classification (binary and multiclass tasks), primary metric of each task type, tested on val and OOT. Rank = mean of the two domains with equal weight. Not included: privacy (F10), time, memory.
- `train_reg` — **Fidelity: train; utility: regression**. Fidelity domain — the criteria distribution (F1, F2, F12), dependence (F3, F4), windows (F6, F9), long structure (F7), target (F8, F11), seams (F5), each against train. Utility domain — TSTR regression (point, quantile, multi-step and volatility tasks), primary metric of each task type, tested on val and OOT. Rank = mean of the two domains with equal weight. Not included: privacy (F10), time, memory.

| method | family | holdout_clf:rank | holdout_clf:p_first | holdout_clf:tier | holdout_reg:rank | holdout_reg:p_first | holdout_reg:tier | train_clf:rank | train_clf:p_first | train_clf:tier | train_reg:rank | train_reg:p_first | train_reg:tier | first_in |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| chronos | long-series generator | 16.1 | 0 | True | 13.7 | 0 | True | 17.4 | 0 | True | 14.9 | 0 | True |  |
| diffusion_ts | long-series generator | 13.7 | 0 | False | 12.2 | 0 | True | 14.5 | 0 | False | 13 | 0 | False |  |
| timesfm | long-series generator | 15.7 | 0 | True | 11.4 | 0.004 | True | 16.8 | 0 | True | 12.5 | 0 | True |  |
| timestral | long-series generator | 17.8 | 0 | False | 13.1 | 0 | True | 19.4 | 0 | False | 14.6 | 0 | False |  |
| zedge_ts_ar | long-series generator | 9.13 | 0.148 | True | 8.91 | 0.281 | True | 8.13 | 0.22 | True | 7.91 | 0.376 | True |  |
| zedge_ts_long | long-series generator | 9.97 | 0 | True | 9.86 | 0 | True | 9.23 | 0 | True | 9.12 | 0 | True |  |
| vae_atsp | optimised selection | 14.7 | 0 | True | 15.1 | 0 | False | 15.3 | 0 | False | 15.7 | 0 | False |  |
| vae_greedy | optimised selection | 15 | 0 | True | 15.3 | 0 | True | 15.6 | 0 | False | 16 | 0 | False |  |
| vae_herding | optimised selection | 14 | 0 | False | 14.6 | 0 | False | 14.2 | 0 | False | 14.8 | 0 | False |  |
| vae_knn | optimised selection | 15.4 | 0 | False | 15.9 | 0 | False | 16.2 | 0 | False | 16.7 | 0 | False |  |
| vae_mbb | optimised selection | 15.9 | 0 | False | 16.8 | 0 | True | 16.7 | 0 | False | 17.6 | 0 | False |  |
| vae_pctsp | optimised selection | 14.5 | 0 | True | 15 | 0 | False | 15.3 | 0 | False | 15.8 | 0 | False |  |
| vae_quilting | optimised selection | 13.8 | 0 | True | 14.4 | 0 | True | 14.4 | 0 | True | 14.9 | 0 | False |  |
| vae_zseries | optimised selection | 13.6 | 0 | True | 13.7 | 0 | True | 14 | 0 | True | 14.1 | 0 | False |  |
| zedge_atsp | optimised selection | 9.37 | 0.002 | True | 9.77 | 0.001 | True | 8.42 | 0.002 | True | 8.83 | 0 | True |  |
| zedge_greedy | optimised selection | 9.16 | 0.003 | True | 9.36 | 0.004 | True | 8.18 | 0.01 | True | 8.37 | 0.006 | True |  |
| zedge_herding | optimised selection | 10.6 | 0 | False | 11.9 | 0 | True | 9.77 | 0 | True | 11.2 | 0 | True |  |
| zedge_knn | optimised selection | 9.55 | 0 | True | 10.1 | 0 | True | 8.63 | 0 | True | 9.22 | 0 | True |  |
| zedge_mbb | optimised selection | 10.5 | 0 | True | 12.3 | 0 | False | 9.85 | 0 | True | 11.6 | 0 | False |  |
| zedge_pctsp | optimised selection | 9.15 | 0.008 | True | 9.59 | 0 | True | 8.15 | 0.04 | True | 8.58 | 0 | True |  |
| zedge_quilting | optimised selection | 8.39 | 0.813 | True | 8.46 | 0.637 | True | 7.67 | 0.615 | True | 7.74 | 0.44 | True | holdout_clf, holdout_reg, train_clf, train_reg |
| zedge_zseries | optimised selection | 9.35 | 0.026 | True | 9.21 | 0.073 | True | 8.3 | 0.113 | True | 8.17 | 0.178 | True |  |
| vae_rand | random selection | 15.9 | 0 | False | 16.9 | 0 | False | 16.7 | 0 | False | 17.7 | 0 | False |  |
| zedge_rand | random selection | 10.7 | 0 | False | 12.4 | 0 | False | 10 | 0 | False | 11.7 | 0 | False |  |


### Ranking `holdout_clf`: Fidelity: val + OOT; utility: classification

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| zedge_quilting | optimised selection | 8.39 | 7.3 | 9.52 | 0.813 | 0.974 |  | True |
| zedge_ts_ar | long-series generator | 9.13 | 7.41 | 10.9 | 0.148 | 0.539 | 0.213 | True |
| zedge_pctsp | optimised selection | 9.15 | 8.24 | 10.1 | 0.008 | 0.512 | 0.195 | True |
| zedge_greedy | optimised selection | 9.16 | 8.17 | 10.2 | 0.003 | 0.447 | 0.0977 | True |
| zedge_zseries | optimised selection | 9.35 | 8.86 | 9.88 | 0.026 | 0.299 | 0.195 | True |
| zedge_atsp | optimised selection | 9.37 | 8.01 | 10.8 | 0.002 | 0.217 | 0.195 | True |
| zedge_knn | optimised selection | 9.55 | 8.73 | 10.5 | 0 | 0.011 | 0.0957 | True |
| zedge_ts_long | long-series generator | 9.97 | 8.74 | 11.3 | 0 | 0.001 | 0.0781 | True |
| zedge_mbb | optimised selection | 10.5 | 9.46 | 11.7 | 0 | 0 | 0.0586 | True |
| zedge_herding | optimised selection | 10.6 | 9.68 | 11.4 | 0 | 0 | 0.0449 | False |
| zedge_rand | random selection | 10.7 | 9.52 | 11.9 | 0 | 0 | 0.0449 | False |
| vae_zseries | optimised selection | 13.6 | 12.3 | 15 | 0 | 0 | 0.0586 | True |
| diffusion_ts | long-series generator | 13.7 | 11.8 | 15.3 | 0 | 0 | 0.0449 | False |
| vae_quilting | optimised selection | 13.8 | 12.3 | 15.4 | 0 | 0 | 0.0586 | True |
| vae_herding | optimised selection | 14 | 13.2 | 14.8 | 0 | 0 | 0.0449 | False |
| vae_pctsp | optimised selection | 14.5 | 13.2 | 15.7 | 0 | 0 | 0.0586 | True |
| vae_atsp | optimised selection | 14.7 | 13 | 16.2 | 0 | 0 | 0.0586 | True |
| vae_greedy | optimised selection | 15 | 13.6 | 16.4 | 0 | 0 | 0.0586 | True |
| vae_knn | optimised selection | 15.4 | 13.8 | 16.9 | 0 | 0 | 0.0449 | False |
| timesfm | long-series generator | 15.7 | 13.2 | 18.2 | 0 | 0 | 0.0957 | True |
| vae_rand | random selection | 15.9 | 13.8 | 17.7 | 0 | 0 | 0.0449 | False |
| vae_mbb | optimised selection | 15.9 | 13.9 | 17.7 | 0 | 0 | 0.0449 | False |
| chronos | long-series generator | 16.1 | 14 | 17.9 | 0 | 0 | 0.0703 | True |
| timestral | long-series generator | 17.8 | 16.6 | 19.1 | 0 | 0 | 0.0449 | False |


### Ranking `holdout_reg`: Fidelity: val + OOT; utility: regression

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| zedge_quilting | optimised selection | 8.46 | 7.38 | 9.48 | 0.637 | 0.946 |  | True |
| zedge_ts_ar | long-series generator | 8.91 | 6.88 | 11.1 | 0.281 | 0.791 | 0.41 | True |
| zedge_zseries | optimised selection | 9.21 | 8.26 | 10 | 0.073 | 0.546 | 0.322 | True |
| zedge_greedy | optimised selection | 9.36 | 8.14 | 10.6 | 0.004 | 0.352 | 0.223 | True |
| zedge_pctsp | optimised selection | 9.59 | 8.31 | 10.9 | 0 | 0.109 | 0.322 | True |
| zedge_atsp | optimised selection | 9.77 | 7.88 | 11.8 | 0.001 | 0.169 | 0.322 | True |
| zedge_ts_long | long-series generator | 9.86 | 8.34 | 11.5 | 0 | 0.055 | 0.322 | True |
| zedge_knn | optimised selection | 10.1 | 8.84 | 11.6 | 0 | 0.001 | 0.0703 | True |
| timesfm | long-series generator | 11.4 | 9.05 | 13.5 | 0.004 | 0.031 | 0.219 | True |
| zedge_herding | optimised selection | 11.9 | 10.2 | 13.8 | 0 | 0 | 0.0703 | True |
| diffusion_ts | long-series generator | 12.2 | 10.7 | 13.6 | 0 | 0 | 0.0703 | True |
| zedge_mbb | optimised selection | 12.3 | 10.4 | 14.3 | 0 | 0 | 0.0449 | False |
| zedge_rand | random selection | 12.4 | 10.5 | 14.4 | 0 | 0 | 0.0449 | False |
| timestral | long-series generator | 13.1 | 11.5 | 14.8 | 0 | 0 | 0.0625 | True |
| chronos | long-series generator | 13.7 | 11.7 | 15.6 | 0 | 0 | 0.0703 | True |
| vae_zseries | optimised selection | 13.7 | 12.1 | 15.2 | 0 | 0 | 0.0625 | True |
| vae_quilting | optimised selection | 14.4 | 12.3 | 16.4 | 0 | 0 | 0.0703 | True |
| vae_herding | optimised selection | 14.6 | 13.7 | 15.5 | 0 | 0 | 0.0449 | False |
| vae_pctsp | optimised selection | 15 | 13.4 | 16.5 | 0 | 0 | 0.0449 | False |
| vae_atsp | optimised selection | 15.1 | 13.1 | 16.9 | 0 | 0 | 0.0449 | False |
| vae_greedy | optimised selection | 15.3 | 13.6 | 16.9 | 0 | 0 | 0.0625 | True |
| vae_knn | optimised selection | 15.9 | 13.9 | 17.8 | 0 | 0 | 0.0449 | False |
| vae_mbb | optimised selection | 16.8 | 14.3 | 19 | 0 | 0 | 0.0625 | True |
| vae_rand | random selection | 16.9 | 14.5 | 19.1 | 0 | 0 | 0.0449 | False |


### Ranking `train_clf`: Fidelity: train; utility: classification

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| zedge_quilting | optimised selection | 7.67 | 6.51 | 8.98 | 0.615 | 0.913 |  | True |
| zedge_ts_ar | long-series generator | 8.13 | 6.57 | 9.75 | 0.22 | 0.553 | 0.602 | True |
| zedge_pctsp | optimised selection | 8.15 | 7.36 | 8.95 | 0.04 | 0.535 | 0.602 | True |
| zedge_greedy | optimised selection | 8.18 | 7.43 | 9.07 | 0.01 | 0.452 | 0.602 | True |
| zedge_zseries | optimised selection | 8.3 | 7.85 | 8.77 | 0.113 | 0.359 | 0.602 | True |
| zedge_atsp | optimised selection | 8.42 | 7.3 | 9.69 | 0.002 | 0.172 | 0.387 | True |
| zedge_knn | optimised selection | 8.63 | 8.06 | 9.29 | 0 | 0.016 | 0.387 | True |
| zedge_ts_long | long-series generator | 9.23 | 8.28 | 10.2 | 0 | 0 | 0.0645 | True |
| zedge_herding | optimised selection | 9.77 | 9.12 | 10.4 | 0 | 0 | 0.109 | True |
| zedge_mbb | optimised selection | 9.85 | 9.07 | 10.6 | 0 | 0 | 0.0879 | True |
| zedge_rand | random selection | 10 | 9.14 | 10.8 | 0 | 0 | 0.0449 | False |
| vae_zseries | optimised selection | 14 | 12.8 | 15.3 | 0 | 0 | 0.0508 | True |
| vae_herding | optimised selection | 14.2 | 13.4 | 15 | 0 | 0 | 0.0449 | False |
| vae_quilting | optimised selection | 14.4 | 13 | 15.7 | 0 | 0 | 0.0508 | True |
| diffusion_ts | long-series generator | 14.5 | 12.6 | 16.2 | 0 | 0 | 0.0449 | False |
| vae_pctsp | optimised selection | 15.3 | 14.3 | 16.2 | 0 | 0 | 0.0449 | False |
| vae_atsp | optimised selection | 15.3 | 14.1 | 16.5 | 0 | 0 | 0.0449 | False |
| vae_greedy | optimised selection | 15.6 | 14.4 | 16.8 | 0 | 0 | 0.0449 | False |
| vae_knn | optimised selection | 16.2 | 15 | 17.3 | 0 | 0 | 0.0449 | False |
| vae_mbb | optimised selection | 16.7 | 15.2 | 18.1 | 0 | 0 | 0.0449 | False |
| vae_rand | random selection | 16.7 | 15.2 | 18.1 | 0 | 0 | 0.0449 | False |
| timesfm | long-series generator | 16.8 | 14.2 | 19.4 | 0 | 0 | 0.109 | True |
| chronos | long-series generator | 17.4 | 15.5 | 19 | 0 | 0 | 0.0781 | True |
| timestral | long-series generator | 19.4 | 18 | 20.5 | 0 | 0 | 0.0449 | False |


### Ranking `train_reg`: Fidelity: train; utility: regression

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| zedge_quilting | optimised selection | 7.74 | 6.64 | 8.93 | 0.44 | 0.907 |  | True |
| zedge_ts_ar | long-series generator | 7.91 | 6.12 | 9.82 | 0.376 | 0.81 | 0.496 | True |
| zedge_zseries | optimised selection | 8.17 | 7.45 | 8.86 | 0.178 | 0.593 | 0.496 | True |
| zedge_greedy | optimised selection | 8.37 | 7.45 | 9.31 | 0.006 | 0.373 | 0.41 | True |
| zedge_pctsp | optimised selection | 8.58 | 7.45 | 9.66 | 0 | 0.133 | 0.41 | True |
| zedge_atsp | optimised selection | 8.83 | 7.17 | 10.7 | 0 | 0.16 | 0.451 | True |
| zedge_ts_long | long-series generator | 9.12 | 7.89 | 10.4 | 0 | 0.024 | 0.387 | True |
| zedge_knn | optimised selection | 9.22 | 8.24 | 10.3 | 0 | 0 | 0.191 | True |
| zedge_herding | optimised selection | 11.2 | 9.68 | 12.7 | 0 | 0 | 0.0586 | True |
| zedge_mbb | optimised selection | 11.6 | 10.1 | 13.1 | 0 | 0 | 0.0449 | False |
| zedge_rand | random selection | 11.7 | 10.2 | 13.3 | 0 | 0 | 0.0449 | False |
| timesfm | long-series generator | 12.5 | 10.2 | 14.5 | 0 | 0 | 0.125 | True |
| diffusion_ts | long-series generator | 13 | 11.6 | 14.3 | 0 | 0 | 0.0449 | False |
| vae_zseries | optimised selection | 14.1 | 12.6 | 15.6 | 0 | 0 | 0.0449 | False |
| timestral | long-series generator | 14.6 | 13.2 | 16.1 | 0 | 0 | 0.0449 | False |
| vae_herding | optimised selection | 14.8 | 13.9 | 15.7 | 0 | 0 | 0.0449 | False |
| chronos | long-series generator | 14.9 | 13.4 | 16.5 | 0 | 0 | 0.0703 | True |
| vae_quilting | optimised selection | 14.9 | 13.1 | 16.7 | 0 | 0 | 0.0449 | False |
| vae_atsp | optimised selection | 15.7 | 14.1 | 17.3 | 0 | 0 | 0.0449 | False |
| vae_pctsp | optimised selection | 15.8 | 14.5 | 17 | 0 | 0 | 0.0449 | False |
| vae_greedy | optimised selection | 16 | 14.5 | 17.3 | 0 | 0 | 0.0449 | False |
| vae_knn | optimised selection | 16.7 | 15.1 | 18.2 | 0 | 0 | 0.0449 | False |
| vae_mbb | optimised selection | 17.6 | 15.7 | 19.3 | 0 | 0 | 0.0449 | False |
| vae_rand | random selection | 17.7 | 15.9 | 19.4 | 0 | 0 | 0.0449 | False |



## Core-metric rankings (RQ1)

The four rankings with the fidelity domain restricted to the core metric set, fixed in advance: distribution (F1.2_w1, F2.1_ks_d24); dependence (F3.5_log_psd, F4.1_how_mean); windows (F6.1_disc_score, F6.4_mmd); long structure (F7.1_roll_mean_ks, F7.2_roll_std_ks); target (F11.1_class_share_logratio); seams (F5.7_seam_detect_auc_dev). Utility unchanged. Each core ranking, the normalised scores (random assembly = 0, real data = 1) and the anchor check — `LEADERBOARD.md`.

| method | family | core_holdout_clf:rank | core_holdout_clf:p_first | core_holdout_clf:tier | core_holdout_reg:rank | core_holdout_reg:p_first | core_holdout_reg:tier | core_train_clf:rank | core_train_clf:p_first | core_train_clf:tier | core_train_reg:rank | core_train_reg:p_first | core_train_reg:tier | first_in |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| chronos | long-series generator | 16.6 | 0 | True | 14.2 | 0 | True | 18 | 0 | True | 15.5 | 0 | True |  |
| diffusion_ts | long-series generator | 14.3 | 0 | False | 12.7 | 0 | True | 15.4 | 0 | False | 13.8 | 0 | False |  |
| timesfm | long-series generator | 16 | 0 | True | 11.7 | 0 | True | 17.6 | 0 | True | 13.3 | 0 | True |  |
| timestral | long-series generator | 18.4 | 0 | False | 13.6 | 0 | True | 20.9 | 0 | False | 16.1 | 0 | False |  |
| zedge_ts_ar | long-series generator | 9.3 | 0.056 | True | 9.09 | 0.12 | True | 8.39 | 0.077 | True | 8.18 | 0.142 | True |  |
| zedge_ts_long | long-series generator | 9.5 | 0 | True | 9.39 | 0.005 | True | 8.8 | 0 | True | 8.7 | 0 | True |  |
| vae_atsp | optimised selection | 15.1 | 0 | True | 15.5 | 0 | False | 15.8 | 0 | False | 16.2 | 0 | False |  |
| vae_greedy | optimised selection | 15.4 | 0 | True | 15.7 | 0 | False | 16.1 | 0 | False | 16.4 | 0 | False |  |
| vae_herding | optimised selection | 13.6 | 0 | False | 14.2 | 0 | False | 13.3 | 0 | False | 14 | 0 | False |  |
| vae_knn | optimised selection | 15.8 | 0 | False | 16.3 | 0 | False | 16.6 | 0 | False | 17.1 | 0 | False |  |
| vae_mbb | optimised selection | 15.9 | 0 | False | 16.8 | 0 | True | 16.7 | 0 | False | 17.6 | 0 | False |  |
| vae_pctsp | optimised selection | 14.9 | 0 | True | 15.4 | 0 | False | 15.7 | 0 | False | 16.2 | 0 | False |  |
| vae_quilting | optimised selection | 14 | 0 | True | 14.5 | 0 | True | 14.6 | 0 | True | 15.1 | 0 | True |  |
| vae_zseries | optimised selection | 13.7 | 0 | True | 13.7 | 0 | True | 14.1 | 0 | True | 14.1 | 0 | False |  |
| zedge_atsp | optimised selection | 9.24 | 0.008 | True | 9.64 | 0.012 | True | 8.24 | 0.015 | True | 8.64 | 0.016 | True |  |
| zedge_greedy | optimised selection | 9.02 | 0.001 | True | 9.21 | 0 | True | 7.93 | 0.004 | True | 8.12 | 0.01 | True |  |
| zedge_herding | optimised selection | 10.1 | 0 | True | 11.5 | 0 | True | 9.14 | 0 | True | 10.5 | 0 | True |  |
| zedge_knn | optimised selection | 9.27 | 0 | True | 9.86 | 0 | True | 8.24 | 0 | True | 8.82 | 0 | True |  |
| zedge_mbb | optimised selection | 10.1 | 0 | True | 11.8 | 0 | True | 9.28 | 0 | True | 11 | 0 | True |  |
| zedge_pctsp | optimised selection | 9.07 | 0.003 | True | 9.51 | 0.001 | True | 7.88 | 0.038 | True | 8.31 | 0.004 | True |  |
| zedge_quilting | optimised selection | 8.01 | 0.91 | True | 8.08 | 0.775 | True | 7.36 | 0.638 | True | 7.44 | 0.524 | True | core_holdout_clf, core_holdout_reg, core_train_clf, core_train_reg |
| zedge_zseries | optimised selection | 9.04 | 0.022 | True | 8.91 | 0.087 | True | 7.78 | 0.228 | True | 7.65 | 0.304 | True |  |
| vae_rand | random selection | 16 | 0 | False | 16.9 | 0 | False | 16.8 | 0 | False | 17.8 | 0 | False |  |
| zedge_rand | random selection | 10.3 | 0 | True | 12 | 0 | False | 9.43 | 0 | True | 11.1 | 0 | True |  |


### Normalised scores on the core metrics (random assembly = 0, real data = 1)

| method | fidelity | utility | dependence | distribution | long_structure | target | windows | classification | regression |
|---|---|---|---|---|---|---|---|---|---|
| chronos | 1.78 | -0.0984 | 1.93 | 1.48 | 1.91 | -1.9 | 2.27 | -0.324 | 0.225 |
| diffusion_ts | 0.73 | 0.155 | 0.619 | 0.404 | 0.656 | 0.42 | 0.752 | 0.0326 | -0.56 |
| timesfm | 1.04 | 0.364 | 0.197 | 0.82 | 1.3 | -6.18 | 1.19 | -0.296 | 0.861 |
| timestral | 0.974 | -0.453 | 1.07 | 1.08 | 1.8 | -4.28 | 0.882 | -1.14 | 0.387 |
| zedge_ts_ar | 0.167 | 0.643 | 0.521 | 0.379 | 0.467 | -0.151 | 0.406 | 0.631 | 0.744 |
| zedge_ts_long | 0.231 | 0.451 | 0.257 | 0.329 | 0.0544 | 0.303 | 0.445 | 0.31 | 0.526 |
| vae_atsp | 0.174 | 0.197 | -0.162 | 0.0692 | 0.258 | 0.294 | 0.185 | 0.139 | 0.217 |
| vae_greedy | 0.0101 | 0.141 | -0.0884 | -0.0631 | -0.00249 | 0.216 | 0.15 | 0.0481 | 0.161 |
| vae_herding | 0.418 | 0.232 | 0.213 | 0.599 | 0.215 | 0.285 | 0.524 | 0.169 | 0.302 |
| vae_knn | 0.0562 | 0.0125 | -0.107 | 0.137 | 0.341 | 0.193 | 0.19 | -0.011 | 0.0535 |
| vae_mbb | 0.0993 | -0.013 | 0.0234 | 0.0781 | 0.238 | 0.19 | 0.196 | -0.00218 | 0.0209 |
| vae_pctsp | 0.23 | 0.102 | 0.0989 | 0.0886 | 0.239 | 0.36 | 0.45 | 0.035 | 0.055 |
| vae_quilting | 0.0554 | 0.152 | -0.229 | 0.0978 | 0.252 | 0.048 | 0.311 | 0.0921 | 0.218 |
| vae_zseries | 0.362 | 0.264 | 0.216 | 0.449 | 0.386 | 0.6 | 0.356 | 0.198 | 0.359 |
| zedge_atsp | 0.177 | 0.431 | 0.0833 | 0.0454 | 0.141 | 0.286 | 0.691 | 0.363 | 0.347 |
| zedge_greedy | 0.177 | 0.411 | 0.148 | 0.189 | 0.209 | 0.503 | 0.114 | 0.323 | 0.347 |
| zedge_herding | -0 | -0.0433 | 0.104 | 0.00217 | -0.0633 | 0.155 | 0.5 | -0.0301 | -0.061 |
| zedge_knn | 0.199 | 0.368 | 0.465 | 0.203 | 0.124 | 0.871 | 0.422 | 0.323 | 0.396 |
| zedge_mbb | 0.0211 | 0.00209 | 0.0726 | 0.0178 | 0.104 | 0.115 | 0.21 | 0.00565 | 0.0116 |
| zedge_pctsp | 0.011 | 0.425 | 0.138 | 0.046 | 0.00861 | 0.0174 | 0.334 | 0.415 | 0.369 |
| zedge_quilting | 0.386 | 0.555 | 0.505 | 0.193 | 0.617 | 0.513 | 0.292 | 0.44 | 0.559 |
| zedge_zseries | 0.0411 | 0.474 | 0.246 | 0.142 | 0.105 | 0.108 | 0.0482 | 0.277 | 0.505 |
| vae_rand | -0 | -0 | -0 | -0 | -0 | -0 | -0 | 0 | -0 |
| zedge_rand | -0 | -0 | -0 | 0 | 0 | -0 | -0 | 0 | -0 |



## Summary

| Question | Verdicts by comparison |
|---|---|
| RQ0. Benchmark validity: noise, real-data ceiling, discriminative power and redundancy of the metrics | discriminative metrics: 229 of 297 |
| RQ1. Ranking of every method in every slice | first by ranking: holdout_clf — zedge_quilting (Friedman p = 5.31e-13); holdout_reg — zedge_quilting (Friedman p = 4.28e-09); train_clf — zedge_quilting (Friedman p = 3.64e-22); train_reg — zedge_quilting (Friedman p = 1.12e-17) |
| RQ2. Assembly from a window pool vs long-series generators | inconclusive: 2545 |
| RQ3. Within assembly: window selection × seam processing | same: 902, inconclusive: 2108 |
| RQ4. Does fidelity predict utility (which metrics, against which reference) | predictive pairs: 388 of 956 |
| RQ5. Gap to real data (TSTR / TRTR), stability over time and across models | worse than real: 120 |
| RQ6. Speed and cost: training and generation time, memory, Pareto front "quality × time" | fastest: timestral (1 s) |
| RQ8. Class balance: do methods preserve class shares (rare events especially) and what does an error cost | inconclusive: 647 |
| RQ9. Outliers and extremes: do methods preserve tails and outliers, and does it matter to the models | better: 58, same: 32, inconclusive: 692 |

## Research questions

### RQ0. Benchmark validity: noise, real-data ceiling, discriminative power and redundancy of the metrics

| unit | kind | group | reference | n_datasets | n_methods | p_friedman | spread_over_noise | p_friedman_bh | discriminative |
|---|---|---|---|---|---|---|---|---|---|
| F1.10_hill_err | fidelity | F1_marginal | val | 9 | 28 | 0.283 | 1.95 | 0.321 | False |
| F1.10_hill_err@oot | fidelity | F1_marginal | oot | 9 | 28 | 0.0737 | 2.07 | 0.0905 | False |
| F1.10_hill_err@train | fidelity | F1_marginal | train | 9 | 28 | 1.55e-18 | 5.03 | 1.05e-17 | True |
| F1.1_ks | fidelity | F1_marginal | val | 9 | 28 | 0.0259 | 12.7 | 0.0333 | True |
| F1.1_ks@oot | fidelity | F1_marginal | oot | 9 | 28 | 5.22e-05 | 7.01 | 8.38e-05 | True |
| F1.1_ks@train | fidelity | F1_marginal | train | 9 | 28 | 6.05e-28 | 12.6 | 4.49e-26 | True |
| F1.2_w1 | fidelity | F1_marginal | val | 9 | 28 | 0.0271 | 14.8 | 0.0347 | True |
| F1.2_w1@oot | fidelity | F1_marginal | oot | 9 | 28 | 0.000505 | 14.8 | 0.000758 | True |
| F1.2_w1@train | fidelity | F1_marginal | train | 9 | 28 | 9.74e-29 | 9.94 | 9.65e-27 | True |
| F1.3_ad | fidelity | F1_marginal | val | 9 | 28 | 0.0113 | 18.1 | 0.0151 | True |
| F1.3_ad@oot | fidelity | F1_marginal | oot | 9 | 28 | 5e-06 | 15.2 | 8.48e-06 | True |
| F1.3_ad@train | fidelity | F1_marginal | train | 9 | 28 | 8.62e-30 | 25.4 | 1.28e-27 | True |
| F1.4_qq_corr | fidelity | F1_marginal | val | 9 | 28 | 0.0136 | 2.06 | 0.0179 | True |
| F1.4_qq_corr@oot | fidelity | F1_marginal | oot | 9 | 28 | 8.82e-15 | 5.35 | 3.85e-14 | True |
| F1.4_qq_corr@train | fidelity | F1_marginal | train | 9 | 28 | 9.43e-17 | 9.31 | 5e-16 | True |
| F1.5_q01_err | fidelity | F1_marginal | val | 9 | 28 | 0.0749 | 4.55 | 0.0915 | False |
| F1.5_q01_err@oot | fidelity | F1_marginal | oot | 9 | 28 | 0.0173 | 3.71 | 0.0227 | True |
| F1.5_q01_err@train | fidelity | F1_marginal | train | 9 | 28 | 5.12e-12 | 6.49 | 1.63e-11 | True |
| F1.5_q99_err | fidelity | F1_marginal | val | 9 | 28 | 0.555 | 3.74 | 0.599 | False |
| F1.5_q99_err@oot | fidelity | F1_marginal | oot | 9 | 28 | 0.58 | 3.11 | 0.62 | False |
| F1.5_q99_err@train | fidelity | F1_marginal | train | 9 | 28 | 2.79e-14 | 3.2 | 1.15e-13 | True |
| F1.5_quantile_err | fidelity | F1_marginal | val | 9 | 28 | 0.0274 | 8.26 | 0.0349 | True |
| F1.5_quantile_err@oot | fidelity | F1_marginal | oot | 9 | 28 | 0.00102 | 9.49 | 0.00148 | True |
| F1.5_quantile_err@train | fidelity | F1_marginal | train | 9 | 28 | 1.43e-27 | 7.86 | 8.48e-26 | True |
| F1.6_kurt_err | fidelity | F1_marginal | val | 9 | 28 | 0.953 | 2.39 | 0.97 | False |
| F1.6_kurt_err@oot | fidelity | F1_marginal | oot | 9 | 28 | 0.175 | 2.39 | 0.201 | False |
| F1.6_kurt_err@train | fidelity | F1_marginal | train | 9 | 28 | 5.9e-20 | 2.9 | 4.74e-19 | True |
| F1.6_mean_err | fidelity | F1_marginal | val | 9 | 28 | 0.0776 | 11 | 0.0941 | False |
| F1.6_mean_err@oot | fidelity | F1_marginal | oot | 9 | 28 | 0.000426 | 11.7 | 0.000645 | True |
| F1.6_mean_err@train | fidelity | F1_marginal | train | 9 | 28 | 1.35e-25 | 5.1 | 4.44e-24 | True |
| F1.6_skew_err | fidelity | F1_marginal | val | 9 | 28 | 0.107 | 2.07 | 0.128 | False |
| F1.6_skew_err@oot | fidelity | F1_marginal | oot | 9 | 28 | 0.0126 | 3.91 | 0.0167 | True |
| F1.6_skew_err@train | fidelity | F1_marginal | train | 9 | 28 | 1.17e-12 | 3.91 | 4.04e-12 | True |
| F1.6_std_err | fidelity | F1_marginal | val | 9 | 28 | 0.842 | 4.4 | 0.875 | False |
| F1.6_std_err@oot | fidelity | F1_marginal | oot | 9 | 28 | 0.555 | 4.4 | 0.599 | False |
| F1.6_std_err@train | fidelity | F1_marginal | train | 9 | 28 | 3.43e-10 | 2.2 | 8.63e-10 | True |
| F1.7_out_of_range | fidelity | F1_marginal | val | 9 | 28 | 0.573 | 8.4 | 0.615 | False |
| F1.7_out_of_range@oot | fidelity | F1_marginal | oot | 9 | 28 | 5.68e-17 | 1.78 | 3.07e-16 | True |
| F1.7_out_of_range@train | fidelity | F1_marginal | train | 9 | 28 | 0.519 |  | 0.571 | False |
| F1.8_coverage | fidelity | F1_marginal | val | 9 | 28 | 2.64e-09 | 3.7 | 5.8e-09 | True |

_Showing 40 rows of 297; all of them — `hypotheses/RQ0_global.parquet`._

**ceiling_share_real_better**

| unit | chronos | diffusion_ts | timesfm | timestral | vae_atsp | vae_greedy | vae_herding | vae_knn | vae_mbb | vae_pctsp | vae_quilting | vae_rand | zedge_atsp | zedge_greedy | zedge_herding | zedge_knn | zedge_mbb | zedge_pctsp | zedge_quilting | zedge_rand | zedge_ts_ar | zedge_ts_long |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F1.10_hill_err | 0.429 | 0.667 | 0.5 | 0.889 | 0.667 | 0.778 | 0.444 | 0.778 | 0.667 | 0.556 | 0.778 | 0.889 | 0.778 | 0.444 | 0.444 | 0.667 | 0.444 | 0.444 | 0.556 | 0.889 | 0.333 | 0.556 |
| F1.10_hill_err@train | 0.857 | 0.667 | 0.833 | 0.889 | 0.889 | 0.889 | 0.667 | 0.889 | 0.889 | 0.889 | 0.778 | 0.889 | 0.333 | 0.556 | 0.667 | 0.333 | 0.667 | 0.444 | 0.333 | 0.556 | 0.333 | 0.556 |
| F1.1_ks | 0.571 | 0.667 | 0.333 | 0.556 | 0.889 | 0.889 | 0.889 | 0.778 | 0.889 | 0.778 | 0.889 | 0.889 | 0.667 | 0.667 | 0.778 | 0.667 | 0.778 | 0.667 | 0.889 | 0.667 | 0.667 | 0.667 |
| F1.1_ks@train | 1 | 0.667 | 1 | 1 | 0.667 | 0.667 | 0.667 | 0.778 | 0.778 | 0.778 | 0.667 | 0.667 | 0.556 | 0.222 | 0.333 | 0.333 | 0.444 | 0.333 | 0.556 | 0.333 | 0.333 | 0.111 |
| F1.2_w1 | 0.571 | 0.667 | 0.167 | 0.333 | 0.889 | 0.889 | 0.889 | 0.778 | 0.778 | 0.667 | 0.889 | 0.889 | 0.667 | 0.778 | 0.667 | 0.667 | 0.778 | 0.667 | 0.778 | 0.667 | 0.778 | 0.778 |
| F1.2_w1@train | 1 | 0.556 | 0.833 | 0.889 | 0.556 | 0.556 | 0.556 | 0.667 | 0.778 | 0.778 | 0.667 | 0.667 | 0.222 | 0.111 | 0.222 | 0.222 | 0.222 | 0.222 | 0.333 | 0.222 | 0.333 | 0.111 |
| F1.3_ad | 0.571 | 0.667 | 0.333 | 0.667 | 0.889 | 0.889 | 0.889 | 0.778 | 0.889 | 0.778 | 0.889 | 0.889 | 0.667 | 0.667 | 0.778 | 0.778 | 0.778 | 0.667 | 0.889 | 0.667 | 0.889 | 0.667 |
| F1.3_ad@train | 1 | 0.667 | 0.833 | 0.889 | 0.667 | 0.667 | 0.667 | 0.667 | 0.778 | 0.778 | 0.667 | 0.667 | 0.444 | 0.222 | 0.222 | 0.333 | 0.333 | 0.333 | 0.556 | 0.333 | 0.333 | 0.111 |
| F1.4_qq_corr | 0.714 | 0.333 | 0.667 | 0.667 | 0.556 | 0.778 | 0.444 | 0.556 | 0.556 | 0.556 | 0.667 | 0.667 | 0.444 | 0.333 | 0.444 | 0.444 | 0.333 | 0.444 | 0.444 | 0.444 | 0.333 | 0.444 |
| F1.4_qq_corr@train | 0.714 | 0.667 | 0.833 | 0.889 | 0.667 | 0.667 | 0.444 | 0.667 | 0.778 | 0.778 | 0.778 | 0.667 | 0.222 | 0.222 | 0.111 | 0.333 | 0.222 | 0 | 0.333 | 0.222 | 0.111 | 0.111 |
| F1.5_q01_err | 0.714 | 0.667 | 0.333 | 0.778 | 0.778 | 0.667 | 0.778 | 0.778 | 0.778 | 0.778 | 0.778 | 0.778 | 0.667 | 0.556 | 0.556 | 0.444 | 0.778 | 0.556 | 0.444 | 0.667 | 0.556 | 0.444 |
| F1.5_q01_err@train | 0.857 | 0.222 | 0.5 | 0.778 | 0.778 | 0.667 | 0.556 | 0.778 | 0.667 | 0.889 | 0.889 | 0.667 | 0.333 | 0.333 | 0.333 | 0.333 | 0.444 | 0.222 | 0.333 | 0.444 | 0.222 | 0.111 |
| F1.5_q99_err | 0.429 | 0.778 | 0.5 | 0.667 | 0.778 | 0.889 | 0.889 | 0.778 | 0.778 | 0.778 | 0.889 | 0.889 | 0.667 | 0.667 | 0.778 | 0.778 | 0.778 | 0.778 | 0.778 | 0.778 | 0.778 | 0.778 |
| F1.5_q99_err@train | 0.857 | 0.444 | 0.5 | 0.667 | 0.444 | 0.333 | 0.333 | 0.556 | 0.444 | 0.444 | 0.333 | 0.556 | 0.333 | 0 | 0.222 | 0.222 | 0.222 | 0.111 | 0.222 | 0.111 | 0.222 | 0.111 |
| F1.5_quantile_err | 0.571 | 0.667 | 0.667 | 0.556 | 0.889 | 0.889 | 0.889 | 0.778 | 0.778 | 0.778 | 0.889 | 0.889 | 0.667 | 0.667 | 0.667 | 0.667 | 0.778 | 0.778 | 0.778 | 0.667 | 0.778 | 0.778 |
| F1.5_quantile_err@train | 1 | 0.667 | 0.833 | 1 | 0.556 | 0.556 | 0.556 | 0.667 | 0.778 | 0.667 | 0.556 | 0.667 | 0.333 | 0 | 0.222 | 0.222 | 0.222 | 0.222 | 0.222 | 0.111 | 0.333 | 0.111 |
| F1.6_kurt_err | 0.714 | 0.444 | 0.5 | 0.667 | 0.556 | 0.778 | 0.333 | 0.667 | 0.778 | 0.667 | 0.556 | 0.667 | 0.667 | 0.556 | 0.556 | 0.667 | 0.667 | 0.667 | 0.556 | 0.556 | 0.556 | 0.556 |
| F1.6_kurt_err@train | 0.714 | 0.778 | 0.833 | 0.778 | 0.667 | 0.778 | 0.444 | 0.667 | 0.667 | 0.778 | 0.778 | 0.667 | 0.444 | 0.222 | 0.444 | 0.333 | 0.444 | 0.333 | 0.222 | 0.333 | 0.111 | 0.222 |
| F1.6_mean_err | 0.571 | 0.667 | 0.333 | 0.333 | 0.889 | 0.889 | 0.889 | 0.778 | 0.778 | 0.667 | 0.889 | 0.889 | 0.667 | 0.778 | 0.667 | 0.778 | 0.778 | 0.778 | 0.889 | 0.667 | 1 | 0.778 |
| F1.6_mean_err@train | 1 | 0.667 | 0.833 | 0.889 | 0.556 | 0.556 | 0.444 | 0.667 | 0.778 | 0.778 | 0.556 | 0.667 | 0.556 | 0.333 | 0.333 | 0.222 | 0.444 | 0.333 | 0.444 | 0.444 | 0.444 | 0.333 |
| F1.6_skew_err | 0.286 | 0.333 | 0.5 | 0.556 | 0.444 | 0.444 | 0.222 | 0.556 | 0.444 | 0.444 | 0.444 | 0.667 | 0.667 | 0.444 | 0.444 | 0.667 | 0.333 | 0.556 | 0.667 | 0.667 | 0.333 | 0.444 |
| F1.6_skew_err@train | 0.714 | 0.444 | 0.667 | 0.778 | 0.778 | 0.778 | 0.556 | 0.889 | 0.444 | 0.667 | 0.667 | 0.778 | 0.444 | 0.222 | 0.444 | 0.444 | 0.333 | 0.333 | 0.333 | 0.444 | 0.222 | 0.222 |
| F1.6_std_err | 0.857 | 0.444 | 0.667 | 0.667 | 0.444 | 0.889 | 0.667 | 0.778 | 0.556 | 0.889 | 0.778 | 0.667 | 0.556 | 0.556 | 0.556 | 0.667 | 0.556 | 0.667 | 0.556 | 0.444 | 0.778 | 0.778 |
| F1.6_std_err@train | 1 | 0.778 | 0.5 | 0.778 | 0.556 | 0.444 | 0.333 | 0.667 | 0.667 | 0.556 | 0.444 | 0.556 | 0.444 | 0.111 | 0.111 | 0.444 | 0.444 | 0.222 | 0.333 | 0.222 | 0.222 | 0.111 |
| F1.7_out_of_range | 0.571 | 0.667 | 0.167 | 0.111 | 0.667 | 0.778 | 0.778 | 0.556 | 0.667 | 0.444 | 0.667 | 0.778 | 0.667 | 0.556 | 0.556 | 0.556 | 0.667 | 0.556 | 0.556 | 0.556 | 0.667 | 0.667 |
| F1.7_out_of_range@train | 0.571 | 0 | 0.167 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| F1.8_coverage | 0.714 | 0.444 | 1 | 1 | 0.889 | 0.889 | 0.667 | 0.889 | 0.778 | 0.778 | 0.778 | 0.889 | 0.556 | 0.333 | 0.444 | 0.444 | 0.556 | 0.556 | 0.333 | 0.444 | 0.333 | 0.444 |
| F1.8_coverage@train | 1 | 0.333 | 0.667 | 1 | 0.667 | 0.444 | 0.333 | 0.667 | 0.667 | 0.778 | 0.556 | 0.444 | 0.222 | 0.111 | 0.333 | 0.222 | 0.222 | 0.222 | 0.222 | 0.222 | 0.111 | 0.111 |
| F1.9_js | 0.571 | 0.556 | 0.667 | 0.778 | 0.778 | 0.889 | 0.667 | 0.778 | 0.889 | 0.889 | 0.889 | 0.778 | 0.556 | 0.444 | 0.778 | 0.778 | 0.778 | 0.556 | 0.667 | 0.556 | 0.444 | 0.444 |
| F1.9_js@train | 0.857 | 0.778 | 1 | 1 | 0.889 | 0.778 | 0.667 | 0.889 | 0.889 | 0.889 | 0.667 | 0.778 | 0.444 | 0.111 | 0.444 | 0.222 | 0.333 | 0.333 | 0.444 | 0.333 | 0.222 | 0.111 |
| F10.1_dcr_logratio | 0.714 | 0.556 | 0.5 | 0.444 | 0.556 | 0.444 | 0.444 | 0.556 | 0.556 | 0.556 | 0.556 | 0.556 | 0.667 | 0.444 | 0.556 | 0.556 | 0.556 | 0.444 | 0.667 | 0.444 | 0.444 | 0.556 |
| F10.2_near_copy_share | 0.286 | 0.222 | 0.333 | 0.333 | 0.222 | 0.222 | 0.111 | 0.222 | 0.111 | 0.222 | 0.222 | 0.222 | 0.222 | 0.333 | 0.222 | 0.222 | 0.222 | 0.444 | 0.333 | 0.111 | 0.111 | 0.111 |
| F11.1_class_share_logratio | 0.857 | 0.556 | 1 | 1 | 0.889 | 0.889 | 0.889 | 1 | 1 | 1 | 0.889 | 1 | 0.556 | 0.556 | 0.556 | 0.556 | 0.778 | 0.667 | 0.667 | 0.889 | 0.778 | 0.667 |
| F11.1_class_share_logratio@train | 1 | 0.889 | 1 | 1 | 0.889 | 0.889 | 0.889 | 1 | 1 | 0.889 | 1 | 1 | 0.444 | 0.333 | 0.444 | 0.556 | 0.667 | 0.222 | 0.222 | 0.667 | 0.556 | 0.444 |
| F11.2_rare_share_logratio | 0.857 | 0.556 | 1 | 0.889 | 0.889 | 0.889 | 0.889 | 0.889 | 0.889 | 0.778 | 1 | 1 | 0.444 | 0.556 | 0.667 | 0.333 | 0.667 | 0.444 | 0.667 | 0.667 | 0.556 | 0.556 |
| F11.2_rare_share_logratio@train | 1 | 0.889 | 0.833 | 1 | 1 | 0.778 | 0.667 | 1 | 1 | 0.778 | 1 | 0.889 | 0.667 | 0.444 | 0.556 | 0.556 | 0.556 | 0.222 | 0.222 | 0.556 | 0.556 | 0.333 |
| F11.3_multiclass_tvd | 0.857 | 0.556 | 1 | 0.889 | 0.778 | 0.889 | 0.889 | 0.889 | 1 | 0.889 | 0.778 | 1 | 0.667 | 0.556 | 0.556 | 0.556 | 0.556 | 0.556 | 0.667 | 0.667 | 0.778 | 0.667 |
| F11.3_multiclass_tvd@train | 0.714 | 0.556 | 1 | 1 | 0.889 | 0.778 | 0.778 | 1 | 0.889 | 0.778 | 0.667 | 0.889 | 0.111 | 0.111 | 0.222 | 0.222 | 0.333 | 0.111 | 0.222 | 0.333 | 0.556 | 0.556 |
| F11.4_minority_lost | 0.286 | 0.222 | 0.833 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0.111 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| F11.4_minority_lost@train | 0.286 | 0.222 | 0.833 | 1 | 0.111 | 0.111 | 0 | 0.111 | 0.111 | 0.111 | 0.222 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |


**uninformative_metrics**: F1.4_qq_corr, F1.5_q01_err@train, F1.5_q99_err@train, F1.6_skew_err, F1.6_skew_err@train, F1.6_std_err@train, F1.7_out_of_range@train, F1.8_coverage@train, F10.2_near_copy_share, F11.4_minority_lost, F11.4_minority_lost@train, F12.1_exceed_rate_err@train, F12.2_exceed_magnitude_err@train, F6.1_disc_score, F6.1_disc_score@train, F7.5_drawdown_ks@train, F7.6_trend_err, F7.6_trend_err@train, F7.7_regime_dur_err, F7.7_regime_dur_err@train

**discriminative_share_by_group**

| kind | group | oot | train | val |
|---|---|---|---|---|
| fidelity | F10_memorisation |  |  | 0.5 |
| fidelity | F11_class_balance | 0.75 | 0.75 | 0.75 |
| fidelity | F12_extremes | 0.6 | 1 | 0 |
| fidelity | F1_marginal | 0.73 | 0.93 | 0.47 |
| fidelity | F2_increments | 0.89 | 0.89 | 0.56 |
| fidelity | F3_dependence | 0.9 | 1 | 0.6 |
| fidelity | F4_seasonality | 1 | 1 | 0 |
| fidelity | F5_seams | 0.75 | 0.88 | 0.88 |
| fidelity | F6_windows | 0.57 | 0.71 | 0.29 |
| fidelity | F7_long_structure | 0.38 | 0.88 | 0.25 |
| fidelity | F8_target | 1 | 1 | 1 |
| fidelity | F9_coverage | 0.5 | 1 | 1 |
| utility | clf_down_h24_q10 | 1 |  | 1 |
| utility | clf_up_h168_q90 | 1 |  | 1 |
| utility | clf_up_h1_q90 | 1 |  | 1 |
| utility | clf_up_h24_q90 | 1 |  | 0.67 |
| utility | clf_up_h24_q95 | 1 |  | 1 |
| utility | clf_up_h24_q99 | 1 |  | 1 |
| utility | clf_up_h6_q90 | 1 |  | 1 |
| utility | mc3_h24 | 1 |  | 1 |
| utility | ms_h24 | 1 |  | 1 |
| utility | qreg_h24 | 1 |  | 1 |
| utility | reg_h1 | 1 |  | 0.5 |
| utility | reg_h168 | 1 |  | 1 |
| utility | reg_h24 | 1 |  | 1 |
| utility | vol_h24 | 1 |  | 1 |


**redundant_pairs**

| metric_a | metric_b | rho |
|---|---|---|
| F4.1_how_mean | F4.3_hod_mean | 0.991 |
| F1.2_w1 | F1.6_mean_err | 0.984 |
| F1.2_w1 | F1.5_quantile_err | 0.981 |
| F1.5_quantile_err | F1.6_mean_err | 0.966 |
| F8.1_class_tvd | F8.5_cond_event_err | 0.955 |
| F6.4_mmd | F6.4_mmd_2T | 0.955 |
| F1.1_ks | F1.3_ad | 0.954 |
| F9.1_precision | F9.2_density_logdev | 0.953 |
| F5.3_seam_z_mean | F5.3_seam_z_p95 | 0.949 |
| F11.3_multiclass_tvd | F8.1_class_tvd | 0.934 |
| F11.1_class_share_logratio | F11.2_rare_share_logratio | 0.921 |
| F9.2_coverage | F9.2_density_logdev | 0.916 |
| F11.3_multiclass_tvd | F8.5_cond_event_err | 0.908 |


**reference_agreement**

| metric | rho_val_train | rho_val_oot |
|---|---|---|
| F1.10_hill_err | 0.41 | 0.539 |
| F1.1_ks | 0.269 | 0.645 |
| F1.2_w1 | 0.249 | 0.662 |
| F1.3_ad | 0.282 | 0.663 |
| F1.4_qq_corr | 0.616 | 0.528 |
| F1.5_q01_err | 0.532 | 0.401 |
| F1.5_q99_err | 0.325 | 0.577 |
| F1.5_quantile_err | 0.257 | 0.667 |
| F1.6_kurt_err | 0.18 | 0.544 |
| F1.6_mean_err | 0.269 | 0.677 |
| F1.6_skew_err | 0.603 | 0.394 |
| F1.6_std_err | 0.288 | 0.445 |
| F1.7_out_of_range | -0.00352 | 0.265 |
| F1.8_coverage | 0.514 | 0.626 |
| F1.9_js | 0.363 | 0.523 |
| F10.1_dcr_logratio |  |  |
| F10.2_near_copy_share |  |  |
| F11.1_class_share_logratio | 0.797 | 0.786 |
| F11.2_rare_share_logratio | 0.755 | 0.804 |
| F11.3_multiclass_tvd | 0.749 | 0.74 |
| F11.4_minority_lost | 0.833 | 0.833 |
| F12.1_exceed_rate_err | 0.25 | 0.456 |
| F12.2_exceed_magnitude_err | -0.185 | 0.473 |
| F12.3_spike_rate_err | 0.223 | 0.237 |
| F12.4_block_max_ks | 0.153 | 0.223 |
| F12.5_block_min_ks | 0.186 | 0.254 |
| F2.1_ks_d1 | 0.763 | 0.617 |
| F2.1_ks_d168 | 0.836 | 0.672 |
| F2.1_ks_d24 | 0.852 | 0.846 |
| F2.1_ks_d6 | 0.36 | 0.521 |
| F2.1_w1_d24 | 0.865 | 0.826 |
| F2.2_vol_ratio_err_d1 | 0.585 | 0.556 |
| F2.2_vol_ratio_err_d24 | 0.829 | 0.763 |
| F2.3_up_share_err | 0.736 | 0.475 |
| F2.4_big_jump_share_err | 0.346 | 0.369 |
| F3.1_acf_in_window | 0.444 | 0.675 |
| F3.2_acf_beyond_window | 0.354 | 0.653 |
| F3.3_pacf | 0.926 | 0.922 |
| F3.4_acf_abs_d | 0.753 | 0.653 |
| F3.4_acf_sq_d | 0.684 | 0.593 |


### RQ1. Ranking of every method in every slice

| column | p_friedman | nemenyi_cd | n_blocks | n_methods_friedman | best |
|---|---|---|---|---|---|
| ranking:holdout_clf | 5.31e-13 | 11 | 9 | 22 | zedge_quilting |
| with_cost:holdout_clf | 5.53e-12 | 11 | 9 | 22 | zedge_quilting |
| ranking:holdout_reg | 4.28e-09 | 11 | 9 | 22 | zedge_quilting |
| with_cost:holdout_reg | 4.47e-09 | 11 | 9 | 22 | zedge_quilting |
| ranking:train_clf | 3.64e-22 | 11 | 9 | 22 | zedge_quilting |
| with_cost:train_clf | 8.5e-21 | 11 | 9 | 22 | zedge_quilting |
| ranking:train_reg | 1.12e-17 | 11 | 9 | 22 | zedge_quilting |
| with_cost:train_reg | 2.92e-14 | 11 | 9 | 22 | zedge_quilting |
| ranking:core_holdout_clf | 9.65e-11 | 11 | 9 | 22 | zedge_quilting |
| ranking:core_holdout_reg | 2.87e-08 | 11 | 9 | 22 | zedge_quilting |
| ranking:core_train_clf | 1.63e-21 | 11 | 9 | 22 | zedge_quilting |
| ranking:core_train_reg | 6.39e-18 | 11 | 9 | 22 | zedge_quilting |
| domain:fidelity@train | 6.46e-25 | 11 | 9 | 22 | zedge_quilting |
| domain:fidelity@val | 0.000804 | 11 | 9 | 22 | zedge_quilting |
| domain:fidelity@oot | 1.15e-09 | 11 | 9 | 22 | zedge_quilting |
| domain:fidelity@all | 3.33e-16 | 11 | 9 | 22 | zedge_quilting |
| domain:utility@val | 7.62e-09 | 11 | 9 | 22 | zedge_ts_ar |
| domain:utility@oot | 7.54e-10 | 11 | 9 | 22 | zedge_quilting |
| domain:utility@all | 9.92e-12 | 11 | 9 | 22 | zedge_quilting |
| cost@generation | 7.75e-29 | 11 | 9 | 22 | vae_rand |
| cost@memory | 5.2e-26 | 11 | 9 | 22 | zedge_ts_ar |
| cost@total | 6.04e-29 | 11 | 9 | 22 | timestral |
| cost@training | 6.04e-29 | 11 | 9 | 22 | timestral |
| fidelity:dependence@oot | 1.17e-05 | 11 | 9 | 22 | zedge_quilting |
| fidelity:dependence@train | 1.21e-21 | 11 | 9 | 22 | zedge_ts_ar |
| fidelity:dependence@val | 0.179 | 11 | 9 | 22 | zedge_quilting |
| fidelity:distribution@oot | 0.000309 | 11 | 9 | 22 | zedge_ts_long |
| fidelity:distribution@train | 1.62e-23 | 11 | 9 | 22 | zedge_ts_ar |
| fidelity:distribution@val | 0.256 | 11 | 9 | 22 | zedge_ts_long |
| fidelity:long_structure@oot | 2.01e-06 | 11 | 9 | 22 | zedge_rand |
| fidelity:long_structure@train | 3.17e-20 | 11 | 9 | 22 | zedge_zseries |
| fidelity:long_structure@val | 0.474 | 11 | 9 | 22 | zedge_ts_long |
| fidelity:privacy@— | 0.915 | 11 | 9 | 22 | vae_herding |
| fidelity:seams@oot | 1.57e-20 | 11 | 9 | 22 | zedge_quilting |
| fidelity:seams@train | 3.78e-20 | 11 | 9 | 22 | zedge_quilting |
| fidelity:seams@val | 1.07e-20 | 11 | 9 | 22 | zedge_quilting |
| fidelity:target@oot | 1.96e-09 | 11 | 9 | 22 | zedge_quilting |
| fidelity:target@train | 1.17e-19 | 11 | 9 | 22 | zedge_zseries |
| fidelity:target@val | 1.2e-09 | 11 | 9 | 22 | zedge_atsp |
| fidelity:windows@oot | 1.01e-05 | 11 | 9 | 22 | zedge_quilting |

_Showing 40 rows of 56; all of them — `hypotheses/RQ1_global.parquet`._

**ranking_holdout_clf**

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| zedge_quilting | optimised selection | 8.39 | 7.3 | 9.52 | 0.813 | 0.974 |  | True |
| zedge_ts_ar | long-series generator | 9.13 | 7.41 | 10.9 | 0.148 | 0.539 | 0.213 | True |
| zedge_pctsp | optimised selection | 9.15 | 8.24 | 10.1 | 0.008 | 0.512 | 0.195 | True |
| zedge_greedy | optimised selection | 9.16 | 8.17 | 10.2 | 0.003 | 0.447 | 0.0977 | True |
| zedge_zseries | optimised selection | 9.35 | 8.86 | 9.88 | 0.026 | 0.299 | 0.195 | True |
| zedge_atsp | optimised selection | 9.37 | 8.01 | 10.8 | 0.002 | 0.217 | 0.195 | True |
| zedge_knn | optimised selection | 9.55 | 8.73 | 10.5 | 0 | 0.011 | 0.0957 | True |
| zedge_ts_long | long-series generator | 9.97 | 8.74 | 11.3 | 0 | 0.001 | 0.0781 | True |
| zedge_mbb | optimised selection | 10.5 | 9.46 | 11.7 | 0 | 0 | 0.0586 | True |
| zedge_herding | optimised selection | 10.6 | 9.68 | 11.4 | 0 | 0 | 0.0449 | False |
| zedge_rand | random selection | 10.7 | 9.52 | 11.9 | 0 | 0 | 0.0449 | False |
| vae_zseries | optimised selection | 13.6 | 12.3 | 15 | 0 | 0 | 0.0586 | True |
| diffusion_ts | long-series generator | 13.7 | 11.8 | 15.3 | 0 | 0 | 0.0449 | False |
| vae_quilting | optimised selection | 13.8 | 12.3 | 15.4 | 0 | 0 | 0.0586 | True |
| vae_herding | optimised selection | 14 | 13.2 | 14.8 | 0 | 0 | 0.0449 | False |
| vae_pctsp | optimised selection | 14.5 | 13.2 | 15.7 | 0 | 0 | 0.0586 | True |
| vae_atsp | optimised selection | 14.7 | 13 | 16.2 | 0 | 0 | 0.0586 | True |
| vae_greedy | optimised selection | 15 | 13.6 | 16.4 | 0 | 0 | 0.0586 | True |
| vae_knn | optimised selection | 15.4 | 13.8 | 16.9 | 0 | 0 | 0.0449 | False |
| timesfm | long-series generator | 15.7 | 13.2 | 18.2 | 0 | 0 | 0.0957 | True |
| vae_rand | random selection | 15.9 | 13.8 | 17.7 | 0 | 0 | 0.0449 | False |
| vae_mbb | optimised selection | 15.9 | 13.9 | 17.7 | 0 | 0 | 0.0449 | False |
| chronos | long-series generator | 16.1 | 14 | 17.9 | 0 | 0 | 0.0703 | True |
| timestral | long-series generator | 17.8 | 16.6 | 19.1 | 0 | 0 | 0.0449 | False |


**ranking_holdout_reg**

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| zedge_quilting | optimised selection | 8.46 | 7.38 | 9.48 | 0.637 | 0.946 |  | True |
| zedge_ts_ar | long-series generator | 8.91 | 6.88 | 11.1 | 0.281 | 0.791 | 0.41 | True |
| zedge_zseries | optimised selection | 9.21 | 8.26 | 10 | 0.073 | 0.546 | 0.322 | True |
| zedge_greedy | optimised selection | 9.36 | 8.14 | 10.6 | 0.004 | 0.352 | 0.223 | True |
| zedge_pctsp | optimised selection | 9.59 | 8.31 | 10.9 | 0 | 0.109 | 0.322 | True |
| zedge_atsp | optimised selection | 9.77 | 7.88 | 11.8 | 0.001 | 0.169 | 0.322 | True |
| zedge_ts_long | long-series generator | 9.86 | 8.34 | 11.5 | 0 | 0.055 | 0.322 | True |
| zedge_knn | optimised selection | 10.1 | 8.84 | 11.6 | 0 | 0.001 | 0.0703 | True |
| timesfm | long-series generator | 11.4 | 9.05 | 13.5 | 0.004 | 0.031 | 0.219 | True |
| zedge_herding | optimised selection | 11.9 | 10.2 | 13.8 | 0 | 0 | 0.0703 | True |
| diffusion_ts | long-series generator | 12.2 | 10.7 | 13.6 | 0 | 0 | 0.0703 | True |
| zedge_mbb | optimised selection | 12.3 | 10.4 | 14.3 | 0 | 0 | 0.0449 | False |
| zedge_rand | random selection | 12.4 | 10.5 | 14.4 | 0 | 0 | 0.0449 | False |
| timestral | long-series generator | 13.1 | 11.5 | 14.8 | 0 | 0 | 0.0625 | True |
| chronos | long-series generator | 13.7 | 11.7 | 15.6 | 0 | 0 | 0.0703 | True |
| vae_zseries | optimised selection | 13.7 | 12.1 | 15.2 | 0 | 0 | 0.0625 | True |
| vae_quilting | optimised selection | 14.4 | 12.3 | 16.4 | 0 | 0 | 0.0703 | True |
| vae_herding | optimised selection | 14.6 | 13.7 | 15.5 | 0 | 0 | 0.0449 | False |
| vae_pctsp | optimised selection | 15 | 13.4 | 16.5 | 0 | 0 | 0.0449 | False |
| vae_atsp | optimised selection | 15.1 | 13.1 | 16.9 | 0 | 0 | 0.0449 | False |
| vae_greedy | optimised selection | 15.3 | 13.6 | 16.9 | 0 | 0 | 0.0625 | True |
| vae_knn | optimised selection | 15.9 | 13.9 | 17.8 | 0 | 0 | 0.0449 | False |
| vae_mbb | optimised selection | 16.8 | 14.3 | 19 | 0 | 0 | 0.0625 | True |
| vae_rand | random selection | 16.9 | 14.5 | 19.1 | 0 | 0 | 0.0449 | False |


**ranking_train_clf**

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| zedge_quilting | optimised selection | 7.67 | 6.51 | 8.98 | 0.615 | 0.913 |  | True |
| zedge_ts_ar | long-series generator | 8.13 | 6.57 | 9.75 | 0.22 | 0.553 | 0.602 | True |
| zedge_pctsp | optimised selection | 8.15 | 7.36 | 8.95 | 0.04 | 0.535 | 0.602 | True |
| zedge_greedy | optimised selection | 8.18 | 7.43 | 9.07 | 0.01 | 0.452 | 0.602 | True |
| zedge_zseries | optimised selection | 8.3 | 7.85 | 8.77 | 0.113 | 0.359 | 0.602 | True |
| zedge_atsp | optimised selection | 8.42 | 7.3 | 9.69 | 0.002 | 0.172 | 0.387 | True |
| zedge_knn | optimised selection | 8.63 | 8.06 | 9.29 | 0 | 0.016 | 0.387 | True |
| zedge_ts_long | long-series generator | 9.23 | 8.28 | 10.2 | 0 | 0 | 0.0645 | True |
| zedge_herding | optimised selection | 9.77 | 9.12 | 10.4 | 0 | 0 | 0.109 | True |
| zedge_mbb | optimised selection | 9.85 | 9.07 | 10.6 | 0 | 0 | 0.0879 | True |
| zedge_rand | random selection | 10 | 9.14 | 10.8 | 0 | 0 | 0.0449 | False |
| vae_zseries | optimised selection | 14 | 12.8 | 15.3 | 0 | 0 | 0.0508 | True |
| vae_herding | optimised selection | 14.2 | 13.4 | 15 | 0 | 0 | 0.0449 | False |
| vae_quilting | optimised selection | 14.4 | 13 | 15.7 | 0 | 0 | 0.0508 | True |
| diffusion_ts | long-series generator | 14.5 | 12.6 | 16.2 | 0 | 0 | 0.0449 | False |
| vae_pctsp | optimised selection | 15.3 | 14.3 | 16.2 | 0 | 0 | 0.0449 | False |
| vae_atsp | optimised selection | 15.3 | 14.1 | 16.5 | 0 | 0 | 0.0449 | False |
| vae_greedy | optimised selection | 15.6 | 14.4 | 16.8 | 0 | 0 | 0.0449 | False |
| vae_knn | optimised selection | 16.2 | 15 | 17.3 | 0 | 0 | 0.0449 | False |
| vae_mbb | optimised selection | 16.7 | 15.2 | 18.1 | 0 | 0 | 0.0449 | False |
| vae_rand | random selection | 16.7 | 15.2 | 18.1 | 0 | 0 | 0.0449 | False |
| timesfm | long-series generator | 16.8 | 14.2 | 19.4 | 0 | 0 | 0.109 | True |
| chronos | long-series generator | 17.4 | 15.5 | 19 | 0 | 0 | 0.0781 | True |
| timestral | long-series generator | 19.4 | 18 | 20.5 | 0 | 0 | 0.0449 | False |


**ranking_train_reg**

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| zedge_quilting | optimised selection | 7.74 | 6.64 | 8.93 | 0.44 | 0.907 |  | True |
| zedge_ts_ar | long-series generator | 7.91 | 6.12 | 9.82 | 0.376 | 0.81 | 0.496 | True |
| zedge_zseries | optimised selection | 8.17 | 7.45 | 8.86 | 0.178 | 0.593 | 0.496 | True |
| zedge_greedy | optimised selection | 8.37 | 7.45 | 9.31 | 0.006 | 0.373 | 0.41 | True |
| zedge_pctsp | optimised selection | 8.58 | 7.45 | 9.66 | 0 | 0.133 | 0.41 | True |
| zedge_atsp | optimised selection | 8.83 | 7.17 | 10.7 | 0 | 0.16 | 0.451 | True |
| zedge_ts_long | long-series generator | 9.12 | 7.89 | 10.4 | 0 | 0.024 | 0.387 | True |
| zedge_knn | optimised selection | 9.22 | 8.24 | 10.3 | 0 | 0 | 0.191 | True |
| zedge_herding | optimised selection | 11.2 | 9.68 | 12.7 | 0 | 0 | 0.0586 | True |
| zedge_mbb | optimised selection | 11.6 | 10.1 | 13.1 | 0 | 0 | 0.0449 | False |
| zedge_rand | random selection | 11.7 | 10.2 | 13.3 | 0 | 0 | 0.0449 | False |
| timesfm | long-series generator | 12.5 | 10.2 | 14.5 | 0 | 0 | 0.125 | True |
| diffusion_ts | long-series generator | 13 | 11.6 | 14.3 | 0 | 0 | 0.0449 | False |
| vae_zseries | optimised selection | 14.1 | 12.6 | 15.6 | 0 | 0 | 0.0449 | False |
| timestral | long-series generator | 14.6 | 13.2 | 16.1 | 0 | 0 | 0.0449 | False |
| vae_herding | optimised selection | 14.8 | 13.9 | 15.7 | 0 | 0 | 0.0449 | False |
| chronos | long-series generator | 14.9 | 13.4 | 16.5 | 0 | 0 | 0.0703 | True |
| vae_quilting | optimised selection | 14.9 | 13.1 | 16.7 | 0 | 0 | 0.0449 | False |
| vae_atsp | optimised selection | 15.7 | 14.1 | 17.3 | 0 | 0 | 0.0449 | False |
| vae_pctsp | optimised selection | 15.8 | 14.5 | 17 | 0 | 0 | 0.0449 | False |
| vae_greedy | optimised selection | 16 | 14.5 | 17.3 | 0 | 0 | 0.0449 | False |
| vae_knn | optimised selection | 16.7 | 15.1 | 18.2 | 0 | 0 | 0.0449 | False |
| vae_mbb | optimised selection | 17.6 | 15.7 | 19.3 | 0 | 0 | 0.0449 | False |
| vae_rand | random selection | 17.7 | 15.9 | 19.4 | 0 | 0 | 0.0449 | False |


**ranking_core_holdout_clf**

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| zedge_quilting | optimised selection | 8.01 | 6.87 | 9.2 | 0.91 | 0.984 |  | True |
| zedge_greedy | optimised selection | 9.02 | 7.9 | 10.2 | 0.001 | 0.483 | 0.186 | True |
| zedge_zseries | optimised selection | 9.04 | 8.39 | 9.78 | 0.022 | 0.477 | 0.186 | True |
| zedge_pctsp | optimised selection | 9.07 | 7.91 | 10.2 | 0.003 | 0.393 | 0.186 | True |
| zedge_atsp | optimised selection | 9.24 | 7.67 | 10.8 | 0.008 | 0.256 | 0.186 | True |
| zedge_knn | optimised selection | 9.27 | 8.32 | 10.4 | 0 | 0.073 | 0.123 | True |
| zedge_ts_ar | long-series generator | 9.3 | 7.6 | 11 | 0.056 | 0.285 | 0.186 | True |
| zedge_ts_long | long-series generator | 9.5 | 8.08 | 11 | 0 | 0.049 | 0.123 | True |
| zedge_mbb | optimised selection | 10.1 | 8.72 | 11.6 | 0 | 0 | 0.123 | True |
| zedge_herding | optimised selection | 10.1 | 9.07 | 11.3 | 0 | 0 | 0.0703 | True |
| zedge_rand | random selection | 10.3 | 8.78 | 11.9 | 0 | 0 | 0.0977 | True |
| vae_herding | optimised selection | 13.6 | 12.9 | 14.2 | 0 | 0 | 0.0449 | False |
| vae_zseries | optimised selection | 13.7 | 12.1 | 15.2 | 0 | 0 | 0.0664 | True |
| vae_quilting | optimised selection | 14 | 12.3 | 15.7 | 0 | 0 | 0.0664 | True |
| diffusion_ts | long-series generator | 14.3 | 12.2 | 16.1 | 0 | 0 | 0.0449 | False |
| vae_pctsp | optimised selection | 14.9 | 13.3 | 16.4 | 0 | 0 | 0.0664 | True |
| vae_atsp | optimised selection | 15.1 | 13 | 17 | 0 | 0 | 0.0664 | True |
| vae_greedy | optimised selection | 15.4 | 13.6 | 17.1 | 0 | 0 | 0.0664 | True |
| vae_knn | optimised selection | 15.8 | 13.8 | 17.5 | 0 | 0 | 0.0449 | False |
| vae_mbb | optimised selection | 15.9 | 13.7 | 17.9 | 0 | 0 | 0.0449 | False |
| vae_rand | random selection | 16 | 13.8 | 17.9 | 0 | 0 | 0.0449 | False |
| timesfm | long-series generator | 16 | 13.8 | 18.1 | 0 | 0 | 0.123 | True |
| chronos | long-series generator | 16.6 | 14.4 | 18.5 | 0 | 0 | 0.0859 | True |
| timestral | long-series generator | 18.4 | 17 | 19.8 | 0 | 0 | 0.0449 | False |


**ranking_core_holdout_reg**

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| zedge_quilting | optimised selection | 8.08 | 6.91 | 9.13 | 0.775 | 0.958 |  | True |
| zedge_zseries | optimised selection | 8.91 | 7.83 | 9.92 | 0.087 | 0.617 | 0.406 | True |
| zedge_ts_ar | long-series generator | 9.09 | 7.01 | 11.2 | 0.12 | 0.592 | 0.406 | True |
| zedge_greedy | optimised selection | 9.21 | 7.92 | 10.5 | 0 | 0.35 | 0.293 | True |
| zedge_ts_long | long-series generator | 9.39 | 7.67 | 11.3 | 0.005 | 0.219 | 0.406 | True |
| zedge_pctsp | optimised selection | 9.51 | 8.05 | 11 | 0.001 | 0.086 | 0.322 | True |
| zedge_atsp | optimised selection | 9.64 | 7.53 | 11.9 | 0.012 | 0.16 | 0.406 | True |
| zedge_knn | optimised selection | 9.86 | 8.48 | 11.4 | 0 | 0.01 | 0.137 | True |
| zedge_herding | optimised selection | 11.5 | 9.56 | 13.6 | 0 | 0 | 0.0977 | True |
| timesfm | long-series generator | 11.7 | 9.72 | 13.5 | 0 | 0.006 | 0.125 | True |
| zedge_mbb | optimised selection | 11.8 | 9.67 | 14.2 | 0 | 0 | 0.0625 | True |
| zedge_rand | random selection | 12 | 9.71 | 14.4 | 0 | 0 | 0.0449 | False |
| diffusion_ts | long-series generator | 12.7 | 10.9 | 14.5 | 0 | 0 | 0.0703 | True |
| timestral | long-series generator | 13.6 | 11.8 | 15.7 | 0 | 0 | 0.0625 | True |
| vae_zseries | optimised selection | 13.7 | 11.9 | 15.5 | 0 | 0.002 | 0.0625 | True |
| chronos | long-series generator | 14.2 | 12.1 | 16.2 | 0 | 0 | 0.0859 | True |
| vae_herding | optimised selection | 14.2 | 13.4 | 15 | 0 | 0 | 0.0449 | False |
| vae_quilting | optimised selection | 14.5 | 12.3 | 16.8 | 0 | 0 | 0.0977 | True |
| vae_pctsp | optimised selection | 15.4 | 13.6 | 17.2 | 0 | 0 | 0.0449 | False |
| vae_atsp | optimised selection | 15.5 | 13.2 | 17.7 | 0 | 0 | 0.0449 | False |
| vae_greedy | optimised selection | 15.7 | 13.7 | 17.7 | 0 | 0 | 0.0449 | False |
| vae_knn | optimised selection | 16.3 | 13.9 | 18.5 | 0 | 0 | 0.0449 | False |
| vae_mbb | optimised selection | 16.8 | 14.2 | 19.1 | 0 | 0 | 0.0625 | True |
| vae_rand | random selection | 16.9 | 14.5 | 19.3 | 0 | 0 | 0.0449 | False |


**ranking_core_train_clf**

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| zedge_quilting | optimised selection | 7.36 | 6.16 | 8.7 | 0.638 | 0.884 |  | True |
| zedge_zseries | optimised selection | 7.78 | 7.17 | 8.39 | 0.228 | 0.607 | 0.5 | True |
| zedge_pctsp | optimised selection | 7.88 | 6.93 | 8.84 | 0.038 | 0.553 | 0.5 | True |
| zedge_greedy | optimised selection | 7.93 | 7.15 | 8.93 | 0.004 | 0.452 | 0.5 | True |
| zedge_atsp | optimised selection | 8.24 | 6.99 | 9.71 | 0.015 | 0.209 | 0.492 | True |
| zedge_knn | optimised selection | 8.24 | 7.6 | 8.93 | 0 | 0.072 | 0.492 | True |
| zedge_ts_ar | long-series generator | 8.39 | 6.91 | 9.9 | 0.077 | 0.217 | 0.5 | True |
| zedge_ts_long | long-series generator | 8.8 | 7.72 | 9.89 | 0 | 0.006 | 0.219 | True |
| zedge_herding | optimised selection | 9.14 | 8.43 | 9.86 | 0 | 0 | 0.219 | True |
| zedge_mbb | optimised selection | 9.28 | 8.47 | 10.2 | 0 | 0 | 0.107 | True |
| zedge_rand | random selection | 9.43 | 8.48 | 10.4 | 0 | 0 | 0.107 | True |
| vae_herding | optimised selection | 13.3 | 12.8 | 14 | 0 | 0 | 0.0449 | False |
| vae_zseries | optimised selection | 14.1 | 12.6 | 15.5 | 0 | 0 | 0.0547 | True |
| vae_quilting | optimised selection | 14.6 | 13 | 16.1 | 0 | 0 | 0.0547 | True |
| diffusion_ts | long-series generator | 15.4 | 13.3 | 17.1 | 0 | 0 | 0.0449 | False |
| vae_pctsp | optimised selection | 15.7 | 14.6 | 16.7 | 0 | 0 | 0.0449 | False |
| vae_atsp | optimised selection | 15.8 | 14.3 | 17.2 | 0 | 0 | 0.0449 | False |
| vae_greedy | optimised selection | 16.1 | 14.6 | 17.4 | 0 | 0 | 0.0449 | False |
| vae_knn | optimised selection | 16.6 | 15.2 | 17.8 | 0 | 0 | 0.0449 | False |
| vae_mbb | optimised selection | 16.7 | 15.2 | 18.2 | 0 | 0 | 0.0449 | False |
| vae_rand | random selection | 16.8 | 15.3 | 18.2 | 0 | 0 | 0.0449 | False |
| timesfm | long-series generator | 17.6 | 15.6 | 19.9 | 0 | 0 | 0.141 | True |
| chronos | long-series generator | 18 | 16.2 | 19.5 | 0 | 0 | 0.0938 | True |
| timestral | long-series generator | 20.9 | 19.4 | 22.1 | 0 | 0 | 0.0449 | False |


**ranking_core_train_reg**

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| zedge_quilting | optimised selection | 7.44 | 6.3 | 8.63 | 0.524 | 0.873 |  | True |
| zedge_zseries | optimised selection | 7.65 | 6.77 | 8.45 | 0.304 | 0.765 | 0.602 | True |
| zedge_greedy | optimised selection | 8.12 | 7.27 | 9.12 | 0.01 | 0.45 | 0.602 | True |
| zedge_ts_ar | long-series generator | 8.18 | 6.4 | 10.1 | 0.142 | 0.461 | 0.602 | True |
| zedge_pctsp | optimised selection | 8.31 | 7.15 | 9.48 | 0.004 | 0.219 | 0.508 | True |
| zedge_atsp | optimised selection | 8.64 | 6.91 | 10.6 | 0.016 | 0.167 | 0.602 | True |
| zedge_ts_long | long-series generator | 8.7 | 7.32 | 10.2 | 0 | 0.056 | 0.492 | True |
| zedge_knn | optimised selection | 8.82 | 7.86 | 9.84 | 0 | 0.009 | 0.26 | True |
| zedge_herding | optimised selection | 10.5 | 8.97 | 12.2 | 0 | 0 | 0.0879 | True |
| zedge_mbb | optimised selection | 11 | 9.48 | 12.7 | 0 | 0 | 0.0508 | True |
| zedge_rand | random selection | 11.1 | 9.44 | 12.9 | 0 | 0 | 0.0508 | True |
| timesfm | long-series generator | 13.3 | 11.4 | 15 | 0 | 0 | 0.125 | True |
| diffusion_ts | long-series generator | 13.8 | 12.3 | 15.3 | 0 | 0 | 0.0449 | False |
| vae_herding | optimised selection | 14 | 13.2 | 14.7 | 0 | 0 | 0.0449 | False |
| vae_zseries | optimised selection | 14.1 | 12.4 | 15.8 | 0 | 0 | 0.0449 | False |
| vae_quilting | optimised selection | 15.1 | 13 | 17.1 | 0 | 0 | 0.0508 | True |
| chronos | long-series generator | 15.5 | 14 | 17 | 0 | 0 | 0.0781 | True |
| timestral | long-series generator | 16.1 | 14.7 | 17.5 | 0 | 0 | 0.0449 | False |
| vae_atsp | optimised selection | 16.2 | 14.4 | 17.9 | 0 | 0 | 0.0449 | False |
| vae_pctsp | optimised selection | 16.2 | 14.9 | 17.5 | 0 | 0 | 0.0449 | False |
| vae_greedy | optimised selection | 16.4 | 14.6 | 17.9 | 0 | 0 | 0.0449 | False |
| vae_knn | optimised selection | 17.1 | 15.4 | 18.7 | 0 | 0 | 0.0449 | False |
| vae_mbb | optimised selection | 17.6 | 15.7 | 19.4 | 0 | 0 | 0.0449 | False |
| vae_rand | random selection | 17.8 | 15.9 | 19.6 | 0 | 0 | 0.0449 | False |


**rankings**

| family | holdout_clf:rank | holdout_clf:p_first | holdout_clf:tier | holdout_reg:rank | holdout_reg:p_first | holdout_reg:tier | train_clf:rank | train_clf:p_first | train_clf:tier | train_reg:rank | train_reg:p_first | train_reg:tier | first_in |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| long-series generator | 16.1 | 0 | True | 13.7 | 0 | True | 17.4 | 0 | True | 14.9 | 0 | True |  |
| long-series generator | 13.7 | 0 | False | 12.2 | 0 | True | 14.5 | 0 | False | 13 | 0 | False |  |
| long-series generator | 15.7 | 0 | True | 11.4 | 0.004 | True | 16.8 | 0 | True | 12.5 | 0 | True |  |
| long-series generator | 17.8 | 0 | False | 13.1 | 0 | True | 19.4 | 0 | False | 14.6 | 0 | False |  |
| long-series generator | 9.13 | 0.148 | True | 8.91 | 0.281 | True | 8.13 | 0.22 | True | 7.91 | 0.376 | True |  |
| long-series generator | 9.97 | 0 | True | 9.86 | 0 | True | 9.23 | 0 | True | 9.12 | 0 | True |  |
| optimised selection | 14.7 | 0 | True | 15.1 | 0 | False | 15.3 | 0 | False | 15.7 | 0 | False |  |
| optimised selection | 15 | 0 | True | 15.3 | 0 | True | 15.6 | 0 | False | 16 | 0 | False |  |
| optimised selection | 14 | 0 | False | 14.6 | 0 | False | 14.2 | 0 | False | 14.8 | 0 | False |  |
| optimised selection | 15.4 | 0 | False | 15.9 | 0 | False | 16.2 | 0 | False | 16.7 | 0 | False |  |
| optimised selection | 15.9 | 0 | False | 16.8 | 0 | True | 16.7 | 0 | False | 17.6 | 0 | False |  |
| optimised selection | 14.5 | 0 | True | 15 | 0 | False | 15.3 | 0 | False | 15.8 | 0 | False |  |
| optimised selection | 13.8 | 0 | True | 14.4 | 0 | True | 14.4 | 0 | True | 14.9 | 0 | False |  |
| optimised selection | 13.6 | 0 | True | 13.7 | 0 | True | 14 | 0 | True | 14.1 | 0 | False |  |
| optimised selection | 9.37 | 0.002 | True | 9.77 | 0.001 | True | 8.42 | 0.002 | True | 8.83 | 0 | True |  |
| optimised selection | 9.16 | 0.003 | True | 9.36 | 0.004 | True | 8.18 | 0.01 | True | 8.37 | 0.006 | True |  |
| optimised selection | 10.6 | 0 | False | 11.9 | 0 | True | 9.77 | 0 | True | 11.2 | 0 | True |  |
| optimised selection | 9.55 | 0 | True | 10.1 | 0 | True | 8.63 | 0 | True | 9.22 | 0 | True |  |
| optimised selection | 10.5 | 0 | True | 12.3 | 0 | False | 9.85 | 0 | True | 11.6 | 0 | False |  |
| optimised selection | 9.15 | 0.008 | True | 9.59 | 0 | True | 8.15 | 0.04 | True | 8.58 | 0 | True |  |
| optimised selection | 8.39 | 0.813 | True | 8.46 | 0.637 | True | 7.67 | 0.615 | True | 7.74 | 0.44 | True | holdout_clf, holdout_reg, train_clf, train_reg |
| optimised selection | 9.35 | 0.026 | True | 9.21 | 0.073 | True | 8.3 | 0.113 | True | 8.17 | 0.178 | True |  |
| random selection | 15.9 | 0 | False | 16.9 | 0 | False | 16.7 | 0 | False | 17.7 | 0 | False |  |
| random selection | 10.7 | 0 | False | 12.4 | 0 | False | 10 | 0 | False | 11.7 | 0 | False |  |


**rankings_core**

| family | core_holdout_clf:rank | core_holdout_clf:p_first | core_holdout_clf:tier | core_holdout_reg:rank | core_holdout_reg:p_first | core_holdout_reg:tier | core_train_clf:rank | core_train_clf:p_first | core_train_clf:tier | core_train_reg:rank | core_train_reg:p_first | core_train_reg:tier | first_in |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| long-series generator | 16.6 | 0 | True | 14.2 | 0 | True | 18 | 0 | True | 15.5 | 0 | True |  |
| long-series generator | 14.3 | 0 | False | 12.7 | 0 | True | 15.4 | 0 | False | 13.8 | 0 | False |  |
| long-series generator | 16 | 0 | True | 11.7 | 0 | True | 17.6 | 0 | True | 13.3 | 0 | True |  |
| long-series generator | 18.4 | 0 | False | 13.6 | 0 | True | 20.9 | 0 | False | 16.1 | 0 | False |  |
| long-series generator | 9.3 | 0.056 | True | 9.09 | 0.12 | True | 8.39 | 0.077 | True | 8.18 | 0.142 | True |  |
| long-series generator | 9.5 | 0 | True | 9.39 | 0.005 | True | 8.8 | 0 | True | 8.7 | 0 | True |  |
| optimised selection | 15.1 | 0 | True | 15.5 | 0 | False | 15.8 | 0 | False | 16.2 | 0 | False |  |
| optimised selection | 15.4 | 0 | True | 15.7 | 0 | False | 16.1 | 0 | False | 16.4 | 0 | False |  |
| optimised selection | 13.6 | 0 | False | 14.2 | 0 | False | 13.3 | 0 | False | 14 | 0 | False |  |
| optimised selection | 15.8 | 0 | False | 16.3 | 0 | False | 16.6 | 0 | False | 17.1 | 0 | False |  |
| optimised selection | 15.9 | 0 | False | 16.8 | 0 | True | 16.7 | 0 | False | 17.6 | 0 | False |  |
| optimised selection | 14.9 | 0 | True | 15.4 | 0 | False | 15.7 | 0 | False | 16.2 | 0 | False |  |
| optimised selection | 14 | 0 | True | 14.5 | 0 | True | 14.6 | 0 | True | 15.1 | 0 | True |  |
| optimised selection | 13.7 | 0 | True | 13.7 | 0 | True | 14.1 | 0 | True | 14.1 | 0 | False |  |
| optimised selection | 9.24 | 0.008 | True | 9.64 | 0.012 | True | 8.24 | 0.015 | True | 8.64 | 0.016 | True |  |
| optimised selection | 9.02 | 0.001 | True | 9.21 | 0 | True | 7.93 | 0.004 | True | 8.12 | 0.01 | True |  |
| optimised selection | 10.1 | 0 | True | 11.5 | 0 | True | 9.14 | 0 | True | 10.5 | 0 | True |  |
| optimised selection | 9.27 | 0 | True | 9.86 | 0 | True | 8.24 | 0 | True | 8.82 | 0 | True |  |
| optimised selection | 10.1 | 0 | True | 11.8 | 0 | True | 9.28 | 0 | True | 11 | 0 | True |  |
| optimised selection | 9.07 | 0.003 | True | 9.51 | 0.001 | True | 7.88 | 0.038 | True | 8.31 | 0.004 | True |  |
| optimised selection | 8.01 | 0.91 | True | 8.08 | 0.775 | True | 7.36 | 0.638 | True | 7.44 | 0.524 | True | core_holdout_clf, core_holdout_reg, core_train_clf, core_train_reg |
| optimised selection | 9.04 | 0.022 | True | 8.91 | 0.087 | True | 7.78 | 0.228 | True | 7.65 | 0.304 | True |  |
| random selection | 16 | 0 | False | 16.9 | 0 | False | 16.8 | 0 | False | 17.8 | 0 | False |  |
| random selection | 10.3 | 0 | True | 12 | 0 | False | 9.43 | 0 | True | 11.1 | 0 | True |  |


**normalized_scores**

| method | fidelity | utility | dependence | distribution | long_structure | target | windows | classification | regression |
|---|---|---|---|---|---|---|---|---|---|
| chronos | 1.78 | -0.0984 | 1.93 | 1.48 | 1.91 | -1.9 | 2.27 | -0.324 | 0.225 |
| diffusion_ts | 0.73 | 0.155 | 0.619 | 0.404 | 0.656 | 0.42 | 0.752 | 0.0326 | -0.56 |
| timesfm | 1.04 | 0.364 | 0.197 | 0.82 | 1.3 | -6.18 | 1.19 | -0.296 | 0.861 |
| timestral | 0.974 | -0.453 | 1.07 | 1.08 | 1.8 | -4.28 | 0.882 | -1.14 | 0.387 |
| zedge_ts_ar | 0.167 | 0.643 | 0.521 | 0.379 | 0.467 | -0.151 | 0.406 | 0.631 | 0.744 |
| zedge_ts_long | 0.231 | 0.451 | 0.257 | 0.329 | 0.0544 | 0.303 | 0.445 | 0.31 | 0.526 |
| vae_atsp | 0.174 | 0.197 | -0.162 | 0.0692 | 0.258 | 0.294 | 0.185 | 0.139 | 0.217 |
| vae_greedy | 0.0101 | 0.141 | -0.0884 | -0.0631 | -0.00249 | 0.216 | 0.15 | 0.0481 | 0.161 |
| vae_herding | 0.418 | 0.232 | 0.213 | 0.599 | 0.215 | 0.285 | 0.524 | 0.169 | 0.302 |
| vae_knn | 0.0562 | 0.0125 | -0.107 | 0.137 | 0.341 | 0.193 | 0.19 | -0.011 | 0.0535 |
| vae_mbb | 0.0993 | -0.013 | 0.0234 | 0.0781 | 0.238 | 0.19 | 0.196 | -0.00218 | 0.0209 |
| vae_pctsp | 0.23 | 0.102 | 0.0989 | 0.0886 | 0.239 | 0.36 | 0.45 | 0.035 | 0.055 |
| vae_quilting | 0.0554 | 0.152 | -0.229 | 0.0978 | 0.252 | 0.048 | 0.311 | 0.0921 | 0.218 |
| vae_zseries | 0.362 | 0.264 | 0.216 | 0.449 | 0.386 | 0.6 | 0.356 | 0.198 | 0.359 |
| zedge_atsp | 0.177 | 0.431 | 0.0833 | 0.0454 | 0.141 | 0.286 | 0.691 | 0.363 | 0.347 |
| zedge_greedy | 0.177 | 0.411 | 0.148 | 0.189 | 0.209 | 0.503 | 0.114 | 0.323 | 0.347 |
| zedge_herding | -0 | -0.0433 | 0.104 | 0.00217 | -0.0633 | 0.155 | 0.5 | -0.0301 | -0.061 |
| zedge_knn | 0.199 | 0.368 | 0.465 | 0.203 | 0.124 | 0.871 | 0.422 | 0.323 | 0.396 |
| zedge_mbb | 0.0211 | 0.00209 | 0.0726 | 0.0178 | 0.104 | 0.115 | 0.21 | 0.00565 | 0.0116 |
| zedge_pctsp | 0.011 | 0.425 | 0.138 | 0.046 | 0.00861 | 0.0174 | 0.334 | 0.415 | 0.369 |
| zedge_quilting | 0.386 | 0.555 | 0.505 | 0.193 | 0.617 | 0.513 | 0.292 | 0.44 | 0.559 |
| zedge_zseries | 0.0411 | 0.474 | 0.246 | 0.142 | 0.105 | 0.108 | 0.0482 | 0.277 | 0.505 |
| vae_rand | -0 | -0 | -0 | -0 | -0 | -0 | -0 | 0 | -0 |
| zedge_rand | -0 | -0 | -0 | 0 | 0 | -0 | -0 | 0 | -0 |


**anchor_check**

| leaf | kind | criterion | core | n_datasets | ratio_all | separated_all | ratio_even | ratio_odd | separated_even | separated_odd | flip |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F1.10_hill_err | fidelity | fidelity:distribution | False | 9 | 0.542 | False | 0.861 | 0.351 | False | False | False |
| F1.10_hill_err@train | fidelity | fidelity:distribution | False | 9 | 0.928 | False | 1.41 | 0.763 | True | False | True |
| F1.1_ks | fidelity | fidelity:distribution | False | 9 | 7.26 | True | 4.32 | 7.17 | True | True | False |
| F1.1_ks@train | fidelity | fidelity:distribution | False | 9 | 2.44 | True | 3.24 | 2.26 | True | True | False |
| F1.2_w1 | fidelity | fidelity:distribution | True | 9 | 5.85 | True | 7.07 | 6.55 | True | True | False |
| F1.2_w1@train | fidelity | fidelity:distribution | True | 9 | 4.03 | True | 3.31 | 3.74 | True | True | False |
| F1.3_ad | fidelity | fidelity:distribution | False | 9 | 7.98 | True | 8.34 | 10.6 | True | True | False |
| F1.3_ad@train | fidelity | fidelity:distribution | False | 9 | 4.18 | True | 2.63 | 2.65 | True | True | False |
| F1.4_qq_corr | fidelity | fidelity:distribution | False | 9 | 3.09 | True | 2.54 | 1.95 | True | True | False |
| F1.4_qq_corr@train | fidelity | fidelity:distribution | False | 9 | 4.47 | True | 2.68 | 2.82 | True | True | False |
| F1.5_q01_err | fidelity | fidelity:distribution | False | 9 | 4.77 | True | 3.13 | 3.56 | True | True | False |
| F1.5_q01_err@train | fidelity | fidelity:distribution | False | 9 | 3.8 | True | 2.74 | 3.6 | True | True | False |
| F1.5_q99_err | fidelity | fidelity:distribution | False | 9 | 7.75 | True | 5.58 | 6.03 | True | True | False |
| F1.5_q99_err@train | fidelity | fidelity:distribution | False | 9 | 5.04 | True | 3.07 | 5.57 | True | True | False |
| F1.5_quantile_err | fidelity | fidelity:distribution | False | 9 | 7.32 | True | 4.86 | 4.16 | True | True | False |
| F1.5_quantile_err@train | fidelity | fidelity:distribution | False | 9 | 4.87 | True | 3.12 | 3.78 | True | True | False |
| F1.6_kurt_err | fidelity | fidelity:distribution | False | 9 | 1.44 | True | 3.05 | 1.39 | True | True | False |
| F1.6_kurt_err@train | fidelity | fidelity:distribution | False | 9 | 1.35 | True | 1.14 | 1.43 | True | True | False |
| F1.6_mean_err | fidelity | fidelity:distribution | False | 9 | 5.85 | True | 7.07 | 6.57 | True | True | False |
| F1.6_mean_err@train | fidelity | fidelity:distribution | False | 9 | 3.71 | True | 3.92 | 3.26 | True | True | False |
| F1.6_skew_err | fidelity | fidelity:distribution | False | 9 | 1.72 | True | 1.16 | 1.28 | True | True | False |
| F1.6_skew_err@train | fidelity | fidelity:distribution | False | 9 | 1.97 | True | 1.92 | 1.28 | True | True | False |
| F1.6_std_err | fidelity | fidelity:distribution | False | 9 | 2.22 | True | 2.16 | 2.86 | True | True | False |
| F1.6_std_err@train | fidelity | fidelity:distribution | False | 9 | 1.66 | True | 2.49 | 2.17 | True | True | False |
| F1.7_out_of_range | fidelity | fidelity:distribution | False | 9 | 4.75 | True | 3.55 | 5.05 | True | True | False |
| F1.7_out_of_range@train | fidelity | fidelity:distribution | False | 9 |  | False |  |  | False | False | False |
| F1.8_coverage | fidelity | fidelity:distribution | False | 9 | 5.3 | True | 3.35 | 1.38 | True | True | False |
| F1.8_coverage@train | fidelity | fidelity:distribution | False | 9 | 6.22 | True | 4.85 | 6.17 | True | True | False |
| F1.9_js | fidelity | fidelity:distribution | False | 9 | 4.49 | True | 3.72 | 1.34 | True | True | False |
| F1.9_js@train | fidelity | fidelity:distribution | False | 9 | 2.76 | True | 1.69 | 2.32 | True | True | False |
| F11.1_class_share_logratio | fidelity | fidelity:target | True | 9 | 1.72 | True | 4.27 | 2.79 | True | True | False |
| F11.1_class_share_logratio@train | fidelity | fidelity:target | True | 9 | 2.49 | True | 2.34 | 2.9 | True | True | False |
| F11.2_rare_share_logratio | fidelity | fidelity:target | False | 9 | 1.88 | True | 4.06 | 1.35 | True | True | False |
| F11.2_rare_share_logratio@train | fidelity | fidelity:target | False | 9 | 3 | True | 3.45 | 2.28 | True | True | False |
| F11.3_multiclass_tvd | fidelity | fidelity:target | False | 9 | 1.47 | True | 1.35 | 0.889 | True | False | True |
| F11.3_multiclass_tvd@train | fidelity | fidelity:target | False | 9 | 1.08 | True | 0.764 | 1.16 | False | True | True |
| F11.4_minority_lost | fidelity | fidelity:target | False | 9 |  | False |  |  | False | False | False |
| F11.4_minority_lost@train | fidelity | fidelity:target | False | 9 |  | False |  |  | False | False | False |
| F12.1_exceed_rate_err | fidelity | fidelity:distribution | False | 9 | 7.54 | True | 10.4 | 6.68 | True | True | False |
| F12.1_exceed_rate_err@train | fidelity | fidelity:distribution | False | 9 | 3.66 | True | 1.48 | 2.42 | True | True | False |


**note**: full ranking by slice — reports/LEADERBOARD.md

### RQ2. Assembly from a window pool vs long-series generators

| comparison | kind | unit | n_datasets | median_z | mean_z | ci_lo | ci_hi | p_better_adj | p_worse_adj | p_equiv_adj | n_better | n_worse | n_same | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| diffusion_ts vs zedge_rand | utility | clf_up_h1_q90\|gbdt\|S\|oot\|auc | 9 | -1.35 | -1.52 | -2.45 | -0.792 | 1 | 0.0731 | 1 | 0 | 5 | 0 | inconclusive |
| diffusion_ts vs zedge_rand | utility | clf_up_h6_q90\|gbdt\|S\|oot\|auc | 9 | -1.79 | -1.83 | -2.69 | -1.12 | 1 | 0.0731 | 1 | 0 | 6 | 0 | inconclusive |
| diffusion_ts vs zedge_rand | utility | clf_up_h6_q90\|linear\|S\|oot\|auc | 9 | -1.15 | -1.25 | -2.12 | -0.588 | 1 | 0.0731 | 1 | 0 | 3 | 0 | inconclusive |
| diffusion_ts vs zedge_rand | utility | mc3_h24\|gbdt\|S\|oot\|logloss | 9 | -2.21 | -2.99 | -4.34 | -1.91 | 1 | 0.0731 | 1 | 0 | 9 | 0 | inconclusive |
| diffusion_ts vs assembly_median | utility | clf_up_h1_q90\|gbdt\|S\|oot\|auc | 9 | -1.26 | -1.52 | -2.32 | -0.906 | 1 | 0.0731 | 1 | 0 | 5 | 0 | inconclusive |
| diffusion_ts vs assembly_median | utility | clf_up_h24_q99\|gbdt\|S\|oot\|auc | 9 | -0.853 | -1.12 | -1.7 | -0.604 | 1 | 0.0731 | 1 | 0 | 2 | 0 | inconclusive |
| diffusion_ts vs assembly_median | utility | clf_up_h6_q90\|gbdt\|S\|oot\|auc | 9 | -1.84 | -1.93 | -2.88 | -1.17 | 1 | 0.0731 | 1 | 0 | 6 | 0 | inconclusive |
| diffusion_ts vs assembly_median | utility | clf_up_h6_q90\|gbdt\|S\|val\|auc | 9 | -1.83 | -1.8 | -2.64 | -1.02 | 1 | 0.0731 | 1 | 0 | 4 | 0 | inconclusive |
| diffusion_ts vs assembly_median | utility | clf_up_h6_q90\|linear\|S\|oot\|auc | 9 | -1.24 | -1.41 | -2.32 | -0.643 | 1 | 0.0731 | 1 | 0 | 5 | 0 | inconclusive |
| diffusion_ts vs assembly_median | utility | mc3_h24\|gbdt\|S\|oot\|logloss | 9 | -1.93 | -2.98 | -4.35 | -1.93 | 1 | 0.0731 | 1 | 0 | 9 | 0 | inconclusive |
| diffusion_ts vs assembly_median | utility | reg_h1\|linear\|S\|val\|mase | 9 | -0.959 | -1.73 | -3.05 | -0.64 | 1 | 0.0731 | 1 | 0 | 2 | 1 | inconclusive |
| timestral vs zedge_rand | utility | clf_down_h24_q10\|gbdt\|S\|oot\|auc | 9 | -4.64 | -23 | -51.3 | -3.77 | 1 | 0.0731 | 1 | 0 | 9 | 0 | inconclusive |
| timestral vs zedge_rand | utility | clf_up_h1_q90\|gbdt\|S\|oot\|auc | 9 | -10.6 | -24.2 | -55.2 | -6.28 | 1 | 0.0731 | 1 | 0 | 8 | 0 | inconclusive |
| timestral vs zedge_rand | utility | clf_up_h24_q90\|mlp\|S\|val\|auc | 9 | -0.784 | -2.14 | -4.64 | -0.571 | 1 | 0.0731 | 1 | 0 | 3 | 0 | inconclusive |
| timestral vs zedge_rand | utility | clf_up_h6_q90\|gbdt\|S\|oot\|auc | 9 | -8.63 | -12.5 | -23.1 | -5.38 | 1 | 0.0731 | 1 | 0 | 8 | 0 | inconclusive |
| timestral vs zedge_rand | utility | mc3_h24\|gbdt\|S\|oot\|logloss | 9 | -4.6 | -26.6 | -46.1 | -9.04 | 1 | 0.0731 | 1 | 0 | 9 | 0 | inconclusive |
| timestral vs zedge_rand | utility | mc3_h24\|gbdt\|S\|val\|logloss | 9 | -42.4 | -42.6 | -72.6 | -18.8 | 1 | 0.0731 | 1 | 0 | 9 | 0 | inconclusive |
| timestral vs zedge_rand | utility | mc3_h24\|linear\|S\|oot\|logloss | 9 | -4.15 | -50.3 | -110 | -5.85 | 1 | 0.0731 | 1 | 0 | 8 | 0 | inconclusive |
| timestral vs zedge_rand | utility | mc3_h24\|linear\|S\|val\|logloss | 9 | -11 | -27.5 | -58.2 | -7.48 | 1 | 0.0731 | 1 | 0 | 9 | 0 | inconclusive |
| timestral vs assembly_median | utility | clf_down_h24_q10\|gbdt\|S\|oot\|auc | 9 | -7.63 | -40.3 | -84.3 | -7.8 | 1 | 0.0731 | 1 | 0 | 9 | 0 | inconclusive |
| timestral vs assembly_median | utility | clf_up_h168_q90\|gbdt\|S\|val\|auc | 9 | -5.89 | -5.09 | -6.44 | -3.6 | 1 | 0.0731 | 1 | 0 | 8 | 0 | inconclusive |
| timestral vs assembly_median | utility | clf_up_h1_q90\|gbdt\|S\|oot\|auc | 9 | -13 | -48.5 | -123 | -9.43 | 1 | 0.0731 | 1 | 0 | 8 | 0 | inconclusive |
| timestral vs assembly_median | utility | clf_up_h1_q90\|gbdt\|S\|val\|auc | 9 | -7.76 | -8.59 | -12.8 | -4.95 | 1 | 0.0731 | 1 | 0 | 8 | 0 | inconclusive |
| timestral vs assembly_median | utility | clf_up_h24_q90\|gbdt\|S\|oot\|auc | 9 | -4.65 | -7.68 | -14.5 | -3.23 | 1 | 0.0731 | 1 | 0 | 8 | 0 | inconclusive |
| timestral vs assembly_median | utility | clf_up_h24_q90\|mlp\|S\|val\|auc | 9 | -1.83 | -3.2 | -6.32 | -1.16 | 1 | 0.0731 | 1 | 0 | 5 | 0 | inconclusive |
| timestral vs assembly_median | utility | clf_up_h24_q99\|gbdt\|S\|oot\|auc | 9 | -4.3 | -4.32 | -5.72 | -3.05 | 1 | 0.0731 | 1 | 0 | 9 | 0 | inconclusive |
| timestral vs assembly_median | utility | clf_up_h6_q90\|gbdt\|S\|oot\|auc | 9 | -9.27 | -28.5 | -57.1 | -8.91 | 1 | 0.0731 | 1 | 0 | 9 | 0 | inconclusive |
| timestral vs assembly_median | utility | mc3_h24\|gbdt\|S\|oot\|logloss | 9 | -17.5 | -38.4 | -74.2 | -10.3 | 1 | 0.0731 | 1 | 0 | 9 | 0 | inconclusive |
| timestral vs assembly_median | utility | mc3_h24\|gbdt\|S\|val\|logloss | 9 | -29.8 | -50.5 | -82.8 | -22.4 | 1 | 0.0731 | 1 | 0 | 9 | 0 | inconclusive |
| timestral vs assembly_median | utility | mc3_h24\|linear\|S\|oot\|logloss | 9 | -14.7 | -76.2 | -150 | -19.1 | 1 | 0.0731 | 1 | 0 | 8 | 0 | inconclusive |
| timestral vs assembly_median | utility | mc3_h24\|linear\|S\|val\|logloss | 9 | -17.3 | -46.3 | -80.4 | -17 | 1 | 0.0731 | 1 | 0 | 9 | 0 | inconclusive |
| timestral vs assembly_median | utility | qreg_h24\|linear\|S\|val\|pinball | 9 | -4.45 | -10.1 | -17.1 | -4.03 | 1 | 0.0731 | 1 | 0 | 6 | 0 | inconclusive |
| zedge_ts_long vs zedge_rand | utility | mc3_h24\|gbdt\|S\|oot\|logloss | 9 | -1.16 | -1.24 | -1.85 | -0.641 | 1 | 0.0731 | 1 | 0 | 4 | 0 | inconclusive |
| diffusion_ts vs zedge_rand | fidelity | F2.1_ks_d6@oot | 9 | -2.39 | -2.63 | -3.83 | -1.52 | 1 | 0.0731 | 1 | 0 | 7 | 0 | inconclusive |
| diffusion_ts vs zedge_rand | fidelity | F3.6_peak168_err@oot | 9 | -1.46 | -2.26 | -3.67 | -1.12 | 1 | 0.0731 | 1 | 0 | 6 | 0 | inconclusive |
| diffusion_ts vs zedge_rand | fidelity | F9.1_recall@oot | 9 | -3.05 | -2.93 | -4.32 | -1.79 | 1 | 0.0731 | 1 | 0 | 8 | 0 | inconclusive |
| diffusion_ts vs assembly_median | fidelity | F1.4_qq_corr@oot | 9 | -0.859 | -1.82 | -3.1 | -0.774 | 1 | 0.0731 | 1 | 0 | 3 | 0 | inconclusive |
| diffusion_ts vs assembly_median | fidelity | F2.1_ks_d6@oot | 9 | -2.34 | -2.7 | -3.87 | -1.63 | 1 | 0.0731 | 1 | 0 | 7 | 0 | inconclusive |
| diffusion_ts vs assembly_median | fidelity | F3.4_acf_abs_d@oot | 9 | -1.42 | -2.27 | -3.33 | -1.34 | 1 | 0.0731 | 1 | 0 | 7 | 0 | inconclusive |
| diffusion_ts vs assembly_median | fidelity | F3.6_peak168_err@oot | 9 | -1.63 | -3.36 | -6.04 | -1.29 | 1 | 0.0731 | 1 | 0 | 6 | 0 | inconclusive |

_Showing 40 rows of 2545 (rows with a better / worse / same verdict first); all of them — `hypotheses/RQ2_global.parquet`._

### RQ3. Within assembly: window selection × seam processing

| comparison | kind | unit | n_datasets | median_z | mean_z | ci_lo | ci_hi | p_better_adj | p_worse_adj | p_equiv_adj | n_better | n_worse | n_same | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| selection: zedge_herding vs zedge_rand | fidelity | F3.6_peak24_err@oot | 9 | 0.416 | 0.462 | 0.125 | 0.801 | 0.0708 | 1 | 0.0158 | 0 | 0 | 0 | same |
| selection: zedge_knn vs zedge_rand | fidelity | F6.2_c2st_auc_dev@oot | 9 | 0.273 | 0.39 | 0.00586 | 0.826 | 0.0708 | 1 | 0.0158 | 0 | 0 | 0 | same |
| seams: zedge_zseries_wsola vs zedge_zseries | fidelity | F5.7_seam_detect_auc_dev | 9 | 0.496 | 0.6 | 0.201 | 0.935 | 0.102 | 1 | 0.0456 | 1 | 0 | 0 | same |
| seams: zedge_zseries_wsola vs zedge_zseries | fidelity | F5.7_seam_detect_auc_dev@oot | 9 | 0.496 | 0.6 | 0.201 | 0.935 | 0.102 | 1 | 0.0456 | 1 | 0 | 0 | same |
| main effect: seams wsola vs none | fidelity | F5.7_seam_detect_auc_dev | 9 | 0.496 | 0.6 | 0.201 | 0.935 | 0.102 | 1 | 0.0456 | 1 | 0 | 0 | same |
| main effect: seams wsola vs none | fidelity | F5.7_seam_detect_auc_dev@oot | 9 | 0.496 | 0.6 | 0.201 | 0.935 | 0.102 | 1 | 0.0456 | 1 | 0 | 0 | same |
| seams: zedge_zseries_quilt vs zedge_zseries | fidelity | F1.6_std_err | 9 | -0.204 | -0.277 | -0.676 | 0.0278 | 1 | 0.118 | 0.0158 | 0 | 0 | 4 | same |
| main effect: seams quilt vs none | fidelity | F1.6_std_err | 9 | -0.204 | -0.277 | -0.676 | 0.0278 | 1 | 0.118 | 0.0158 | 0 | 0 | 4 | same |
| selection: zedge_herding vs zedge_rand | fidelity | F7.3_crossings_err@oot | 9 | -0.4 | -0.478 | -0.825 | -0.157 | 1 | 0.121 | 0.0199 | 0 | 0 | 1 | same |
| seams: zedge_zseries_wsola vs zedge_zseries | fidelity | F4.2_how_std | 9 | -0.294 | -0.449 | -0.89 | -0.0983 | 1 | 0.121 | 0.0258 | 0 | 0 | 3 | same |
| main effect: seams wsola vs none | fidelity | F4.2_how_std | 9 | -0.294 | -0.449 | -0.89 | -0.0983 | 1 | 0.121 | 0.0258 | 0 | 0 | 3 | same |
| selection: zedge_knn vs zedge_rand | utility | reg_h1\|gbdt\|S\|oot\|mase | 9 | 0.471 | 0.414 | 0.0436 | 0.781 | 0.128 | 1 | 0.0158 | 0 | 0 | 0 | same |
| seams: zedge_zseries_xfade vs zedge_zseries | fidelity | F1.5_quantile_err@oot | 9 | -0.297 | -0.255 | -0.548 | 0.0359 | 1 | 0.145 | 0.0158 | 0 | 0 | 3 | same |
| seams: zedge_zseries_xfade vs zedge_zseries | fidelity | F3.7_dfa_err | 9 | -0.107 | -0.502 | -0.999 | -0.115 | 1 | 0.145 | 0.0456 | 0 | 0 | 4 | same |
| main effect: seams crossfade vs none | fidelity | F1.5_quantile_err@oot | 9 | -0.297 | -0.255 | -0.548 | 0.0359 | 1 | 0.145 | 0.0158 | 0 | 0 | 3 | same |
| main effect: seams crossfade vs none | fidelity | F3.7_dfa_err | 9 | -0.107 | -0.502 | -0.999 | -0.115 | 1 | 0.145 | 0.0456 | 0 | 0 | 4 | same |
| seams: zedge_zseries_wsola vs zedge_zseries | utility | clf_up_h1_q90\|gbdt\|S\|oot\|auc | 9 | 0.264 | 0.361 | -0.0764 | 0.809 | 0.156 | 1 | 0.0158 | 0 | 0 | 0 | same |
| main effect: seams wsola vs none | utility | clf_up_h1_q90\|gbdt\|S\|oot\|auc | 9 | 0.264 | 0.361 | -0.0764 | 0.809 | 0.156 | 1 | 0.0158 | 0 | 0 | 0 | same |
| selection: zedge_herding vs zedge_rand | fidelity | F8.6_cond_future_ks@oot | 9 | 0.437 | 0.391 | 0.0331 | 0.754 | 0.156 | 1 | 0.0158 | 0 | 0 | 0 | same |
| selection: zedge_mbb vs zedge_rand | fidelity | F1.4_qq_corr | 9 | 0.161 | 0.407 | -0.0614 | 0.901 | 0.156 | 1 | 0.0358 | 0 | 0 | 0 | same |
| selection: zedge_mbb vs zedge_rand | fidelity | F1.6_skew_err | 9 | 0.303 | 0.333 | -0.0775 | 0.765 | 0.156 | 1 | 0.0158 | 0 | 0 | 1 | same |
| selection: zedge_greedy vs zedge_rand | fidelity | F1.10_hill_err | 9 | -0.423 | -0.48 | -1 | -0.0764 | 1 | 0.177 | 0.0358 | 0 | 0 | 0 | same |
| seams: zedge_zseries_xfade vs zedge_zseries | fidelity | F2.1_ks_d6@oot | 9 | -0.209 | -0.365 | -0.853 | -0.0138 | 1 | 0.177 | 0.0456 | 0 | 0 | 3 | same |
| seams: zedge_zseries_xfade vs zedge_zseries | fidelity | F7.7_regime_dur_err@oot | 9 | -0.155 | -0.354 | -0.737 | -0.0362 | 1 | 0.177 | 0.0258 | 0 | 0 | 3 | same |
| main effect: seams crossfade vs none | fidelity | F2.1_ks_d6@oot | 9 | -0.209 | -0.365 | -0.853 | -0.0138 | 1 | 0.177 | 0.0456 | 0 | 0 | 3 | same |
| main effect: seams crossfade vs none | fidelity | F7.7_regime_dur_err@oot | 9 | -0.155 | -0.354 | -0.737 | -0.0362 | 1 | 0.177 | 0.0258 | 0 | 0 | 3 | same |
| selection: zedge_herding vs zedge_rand | utility | vol_h24\|linear\|S\|oot\|mase | 9 | 0.48 | 0.549 | 0.149 | 0.918 | 0.186 | 1 | 0.0456 | 0 | 0 | 0 | same |
| selection: zedge_knn vs zedge_rand | fidelity | F8.2_event_dur_ks@oot | 9 | 0.566 | 0.475 | 0.0408 | 0.896 | 0.186 | 1 | 0.0258 | 0 | 0 | 0 | same |
| selection: zedge_mbb vs zedge_rand | fidelity | F1.6_kurt_err | 9 | 0.376 | 0.323 | -0.127 | 0.766 | 0.186 | 1 | 0.0158 | 0 | 0 | 1 | same |
| selection: zedge_mbb vs zedge_rand | utility | clf_down_h24_q10\|linear\|S\|oot\|auc | 9 | -0.307 | -0.363 | -0.812 | 0.107 | 1 | 0.2 | 0.0158 | 0 | 0 | 1 | same |
| selection: zedge_mbb vs zedge_rand | fidelity | F9.2_density_logdev@oot | 9 | -0.332 | -0.323 | -0.712 | 0.0758 | 1 | 0.2 | 0.0158 | 0 | 0 | 0 | same |
| seams: zedge_zseries_wsola vs zedge_zseries | fidelity | F1.6_std_err@oot | 9 | -0.338 | -0.339 | -0.806 | 0.102 | 1 | 0.2 | 0.0199 | 0 | 0 | 3 | same |
| main effect: seams wsola vs none | fidelity | F1.6_std_err@oot | 9 | -0.338 | -0.339 | -0.806 | 0.102 | 1 | 0.2 | 0.0199 | 0 | 0 | 3 | same |
| selection: zedge_herding vs zedge_rand | utility | clf_up_h24_q90\|gbdt\|S\|oot\|auc | 9 | -0.318 | -0.357 | -0.828 | 0.0909 | 1 | 0.227 | 0.0258 | 0 | 0 | 0 | same |
| selection: zedge_pctsp vs zedge_rand | fidelity | F1.6_skew_err@oot | 9 | -0.273 | -0.363 | -0.912 | 0.179 | 1 | 0.227 | 0.0199 | 0 | 0 | 1 | same |
| seams: zedge_zseries_wsola vs zedge_zseries | fidelity | F4.2_how_std@oot | 9 | -0.165 | -0.187 | -0.663 | 0.236 | 1 | 0.227 | 0.0158 | 0 | 0 | 3 | same |
| seams: zedge_zseries_xfade vs zedge_zseries | fidelity | F4.3_hod_mean@oot | 9 | -0.262 | -0.304 | -0.629 | 0.00785 | 1 | 0.227 | 0.0158 | 0 | 0 | 3 | same |
| main effect: seams crossfade vs none | fidelity | F4.3_hod_mean@oot | 9 | -0.262 | -0.304 | -0.629 | 0.00785 | 1 | 0.227 | 0.0158 | 0 | 0 | 3 | same |
| main effect: seams wsola vs none | fidelity | F4.2_how_std@oot | 9 | -0.165 | -0.187 | -0.663 | 0.236 | 1 | 0.227 | 0.0158 | 0 | 0 | 3 | same |
| selection: zedge_mbb vs zedge_rand | utility | vol_h24\|gbdt\|S\|val\|mase | 9 | 0.133 | 0.231 | -0.114 | 0.568 | 0.229 | 1 | 0.0158 | 0 | 0 | 1 | same |

_Showing 40 rows of 3010 (rows with a better / worse / same verdict first); all of them — `hypotheses/RQ3_global.parquet`._

**grid**

| assembler | joiner | method |
|---|---|---|
| atsp | none | zedge_atsp |
| greedy | none | zedge_greedy |
| herding | none | zedge_herding |
| knn | none | zedge_knn |
| mbb | none | zedge_mbb |
| pctsp | none | zedge_pctsp |
| quilt_sel | quilt | zedge_quilting |
| random | none | zedge_rand |
| zseries | crossfade | zedge_zseries_xfade |
| zseries | quilt | zedge_zseries_quilt |
| zseries | wsola | zedge_zseries_wsola |
| zseries | none | zedge_zseries |


### RQ4. Does fidelity predict utility (which metrics, against which reference)

| unit | metric | reference | group | criterion | n_datasets | median_rho | share_positive | p_two_sided | p_bh | predictive |
|---|---|---|---|---|---|---|---|---|---|---|
| F8.4_event_by_how@train | F8.4_event_by_how | train | F8_target | regression@oot | 9 | 0.872 | 0.889 | 0.0117 | 0.0363 | True |
| F8.5_cond_event_err@oot | F8.5_cond_event_err | oot | F8_target | regression@oot | 9 | 0.846 | 0.889 | 0.00781 | 0.0304 | True |
| F8.6_cond_future_ks@train | F8.6_cond_future_ks | train | F8_target | regression@oot | 9 | 0.839 | 0.778 | 0.0195 | 0.0479 | True |
| F6.6_feature_fid@oot | F6.6_feature_fid | oot | F6_windows | regression@oot | 9 | 0.837 | 1 | 0.00391 | 0.0249 | True |
| F8.4_event_by_how | F8.4_event_by_how | val | F8_target | regression@val | 9 | 0.835 | 0.778 | 0.0195 | 0.0479 | True |
| F8.5_cond_event_err@train | F8.5_cond_event_err | train | F8_target | regression@oot | 9 | 0.834 | 0.889 | 0.00781 | 0.0304 | True |
| F1.6_mean_err@oot | F1.6_mean_err | oot | F1_marginal | regression@oot | 9 | 0.831 | 1 | 0.00391 | 0.0249 | True |
| F8.4_event_by_how@oot | F8.4_event_by_how | oot | F8_target | regression@oot | 9 | 0.826 | 0.889 | 0.00781 | 0.0304 | True |
| F8.6_cond_future_ks@oot | F8.6_cond_future_ks | oot | F8_target | regression@oot | 9 | 0.823 | 0.889 | 0.00781 | 0.0304 | True |
| F6.4_mmd@oot | F6.4_mmd | oot | F6_windows | regression@oot | 9 | 0.822 | 0.889 | 0.00781 | 0.0304 | True |
| F8.4_event_by_how | F8.4_event_by_how | val | F8_target | regression@oot | 9 | 0.821 | 0.889 | 0.00781 | 0.0304 | True |
| F9.2_coverage@train | F9.2_coverage | train | F9_coverage | regression@oot | 9 | 0.82 | 0.778 | 0.0195 | 0.0479 | True |
| F6.6_feature_fid@train | F6.6_feature_fid | train | F6_windows | classification@oot | 9 | 0.82 | 1 | 0.00391 | 0.0249 | True |
| F9.2_coverage@train | F9.2_coverage | train | F9_coverage | classification@oot | 9 | 0.819 | 1 | 0.00391 | 0.0249 | True |
| F6.8_nn_dist_logratio | F6.8_nn_dist_logratio | val | F6_windows | regression@val | 9 | 0.819 | 1 | 0.00391 | 0.0249 | True |
| F8.5_cond_event_err@train | F8.5_cond_event_err | train | F8_target | classification@val | 9 | 0.818 | 0.778 | 0.0195 | 0.0479 | True |
| F8.6_cond_future_ks@oot | F8.6_cond_future_ks | oot | F8_target | classification@oot | 9 | 0.818 | 0.889 | 0.00781 | 0.0304 | True |
| F1.5_quantile_err@oot | F1.5_quantile_err | oot | F1_marginal | regression@oot | 9 | 0.817 | 1 | 0.00391 | 0.0249 | True |
| F11.3_multiclass_tvd@train | F11.3_multiclass_tvd | train | F11_class_balance | classification@val | 9 | 0.815 | 0.889 | 0.00781 | 0.0304 | True |
| F1.2_w1@oot | F1.2_w1 | oot | F1_marginal | regression@oot | 9 | 0.814 | 1 | 0.00391 | 0.0249 | True |
| F6.6_feature_fid@oot | F6.6_feature_fid | oot | F6_windows | classification@oot | 9 | 0.814 | 0.778 | 0.0273 | 0.0587 | False |
| F8.5_cond_event_err | F8.5_cond_event_err | val | F8_target | regression@oot | 9 | 0.811 | 0.889 | 0.0117 | 0.0363 | True |
| F6.4_mmd | F6.4_mmd | val | F6_windows | regression@oot | 9 | 0.81 | 0.778 | 0.129 | 0.174 | False |
| F8.1_class_tvd | F8.1_class_tvd | val | F8_target | regression@oot | 9 | 0.807 | 0.889 | 0.00781 | 0.0304 | True |
| F8.6_cond_future_ks | F8.6_cond_future_ks | val | F8_target | classification@oot | 9 | 0.803 | 0.778 | 0.0391 | 0.0747 | False |
| F9.2_coverage@oot | F9.2_coverage | oot | F9_coverage | regression@oot | 9 | 0.803 | 1 | 0.00391 | 0.0249 | True |
| F8.4_event_by_how@train | F8.4_event_by_how | train | F8_target | regression@val | 9 | 0.8 | 0.667 | 0.0547 | 0.0937 | False |
| F2.1_w1_d24@train | F2.1_w1_d24 | train | F2_increments | classification@oot | 9 | 0.8 | 1 | 0.00391 | 0.0249 | True |
| F8.4_event_by_how@oot | F8.4_event_by_how | oot | F8_target | regression@val | 9 | 0.8 | 0.889 | 0.0117 | 0.0363 | True |
| F3.8_calendar_corr_err | F3.8_calendar_corr_err | val | F3_dependence | regression@oot | 9 | 0.799 | 0.889 | 0.00781 | 0.0304 | True |
| F8.6_cond_future_ks@train | F8.6_cond_future_ks | train | F8_target | classification@oot | 9 | 0.799 | 1 | 0.00391 | 0.0249 | True |
| F8.1_class_tvd@train | F8.1_class_tvd | train | F8_target | classification@val | 9 | 0.797 | 0.667 | 0.0547 | 0.0937 | False |
| F8.6_cond_future_ks@train | F8.6_cond_future_ks | train | F8_target | classification@val | 9 | 0.796 | 0.889 | 0.00781 | 0.0304 | True |
| F8.6_cond_future_ks@oot | F8.6_cond_future_ks | oot | F8_target | classification@val | 9 | 0.795 | 0.889 | 0.00781 | 0.0304 | True |
| F8.5_cond_event_err@train | F8.5_cond_event_err | train | F8_target | regression@val | 9 | 0.795 | 0.778 | 0.0391 | 0.0747 | False |
| F7.3_crossings_err | F7.3_crossings_err | val | F7_long_structure | classification@oot | 9 | 0.793 | 0.778 | 0.0547 | 0.0937 | False |
| F9.2_coverage@oot | F9.2_coverage | oot | F9_coverage | classification@oot | 9 | 0.792 | 1 | 0.00391 | 0.0249 | True |
| F6.8_nn_dist_logratio@oot | F6.8_nn_dist_logratio | oot | F6_windows | regression@oot | 9 | 0.792 | 0.889 | 0.0195 | 0.0479 | True |
| F8.6_cond_future_ks | F8.6_cond_future_ks | val | F8_target | regression@oot | 9 | 0.791 | 0.778 | 0.0273 | 0.0587 | False |
| F8.1_class_tvd@train | F8.1_class_tvd | train | F8_target | regression@oot | 9 | 0.789 | 0.889 | 0.00781 | 0.0304 | True |

_Showing 40 rows of 956; all of them — `hypotheses/RQ4_global.parquet`._

**by_reference**

| criterion | reference | median_rho | share_predictive |
|---|---|---|---|
| classification@oot | oot | 0.613 | 0.57 |
| classification@oot | train | 0.64 | 0.785 |
| classification@oot | val | 0.471 | 0.296 |
| classification@val | oot | 0.471 | 0.228 |
| classification@val | train | 0.576 | 0.722 |
| classification@val | val | 0.47 | 0.296 |
| regression@oot | oot | 0.599 | 0.544 |
| regression@oot | train | 0.628 | 0.557 |
| regression@oot | val | 0.528 | 0.21 |
| regression@val | oot | 0.383 | 0.127 |
| regression@val | train | 0.493 | 0.127 |
| regression@val | val | 0.456 | 0.42 |


**by_group**

| group | reference | classification@oot | classification@val | regression@oot | regression@val |
|---|---|---|---|---|---|
| F10_memorisation | val | -0.154 | 0.058 | -0.283 | -0.156 |
| F11_class_balance | oot | 0.614 | 0.492 | 0.656 | 0.342 |
| F11_class_balance | train | 0.711 | 0.728 | 0.668 | 0.569 |
| F11_class_balance | val | 0.597 | 0.514 | 0.713 | 0.401 |
| F12_extremes | oot | 0.376 | 0.307 | 0.452 | 0.379 |
| F12_extremes | train | 0.595 | 0.548 | 0.568 | 0.367 |
| F12_extremes | val | 0.234 | 0.274 | 0.528 | 0.617 |
| F1_marginal | oot | 0.613 | 0.432 | 0.658 | 0.515 |
| F1_marginal | train | 0.655 | 0.625 | 0.595 | 0.484 |
| F1_marginal | val | 0.483 | 0.509 | 0.56 | 0.631 |
| F2_increments | oot | 0.58 | 0.486 | 0.659 | 0.297 |
| F2_increments | train | 0.644 | 0.633 | 0.65 | 0.58 |
| F2_increments | val | 0.421 | 0.44 | 0.452 | 0.345 |
| F3_dependence | oot | 0.623 | 0.54 | 0.558 | 0.439 |
| F3_dependence | train | 0.611 | 0.59 | 0.596 | 0.557 |
| F3_dependence | val | 0.6 | 0.502 | 0.519 | 0.424 |
| F4_seasonality | oot | 0.666 | 0.475 | 0.729 | 0.649 |
| F4_seasonality | train | 0.617 | 0.576 | 0.703 | 0.498 |
| F4_seasonality | val | 0.413 | 0.47 | 0.645 | 0.685 |
| F5_seams | oot | 0.118 | 0.092 | 0.131 | 0.318 |
| F5_seams | train | 0.124 | 0.121 | 0.163 | 0.327 |
| F5_seams | val | 0.111 | 0.121 | 0.163 | 0.327 |
| F6_windows | oot | 0.693 | 0.433 | 0.728 | 0.416 |
| F6_windows | train | 0.637 | 0.497 | 0.636 | 0.555 |
| F6_windows | val | 0.614 | 0.55 | 0.652 | 0.71 |
| F7_long_structure | oot | 0.416 | 0.27 | 0.454 | 0.024 |
| F7_long_structure | train | 0.639 | 0.51 | 0.528 | 0.266 |
| F7_long_structure | val | 0.155 | 0.229 | 0.355 | 0.352 |
| F8_target | oot | 0.697 | 0.638 | 0.785 | 0.654 |
| F8_target | train | 0.753 | 0.775 | 0.812 | 0.757 |
| F8_target | val | 0.66 | 0.585 | 0.799 | 0.689 |
| F9_coverage | oot | 0.676 | 0.526 | 0.673 | 0.146 |
| F9_coverage | train | 0.769 | 0.716 | 0.709 | 0.612 |
| F9_coverage | val | 0.654 | 0.581 | 0.608 | 0.677 |


**top_predictors**

| unit | metric | reference | group | criterion | n_datasets | median_rho | share_positive | p_two_sided | p_bh | predictive |
|---|---|---|---|---|---|---|---|---|---|---|
| F8.4_event_by_how@train | F8.4_event_by_how | train | F8_target | regression@oot | 9 | 0.872 | 0.889 | 0.0117 | 0.0363 | True |
| F8.5_cond_event_err@oot | F8.5_cond_event_err | oot | F8_target | regression@oot | 9 | 0.846 | 0.889 | 0.00781 | 0.0304 | True |
| F8.6_cond_future_ks@train | F8.6_cond_future_ks | train | F8_target | regression@oot | 9 | 0.839 | 0.778 | 0.0195 | 0.0479 | True |
| F6.6_feature_fid@oot | F6.6_feature_fid | oot | F6_windows | regression@oot | 9 | 0.837 | 1 | 0.00391 | 0.0249 | True |
| F8.4_event_by_how | F8.4_event_by_how | val | F8_target | regression@val | 9 | 0.835 | 0.778 | 0.0195 | 0.0479 | True |
| F8.5_cond_event_err@train | F8.5_cond_event_err | train | F8_target | regression@oot | 9 | 0.834 | 0.889 | 0.00781 | 0.0304 | True |
| F6.6_feature_fid@train | F6.6_feature_fid | train | F6_windows | classification@oot | 9 | 0.82 | 1 | 0.00391 | 0.0249 | True |
| F9.2_coverage@train | F9.2_coverage | train | F9_coverage | classification@oot | 9 | 0.819 | 1 | 0.00391 | 0.0249 | True |
| F6.8_nn_dist_logratio | F6.8_nn_dist_logratio | val | F6_windows | regression@val | 9 | 0.819 | 1 | 0.00391 | 0.0249 | True |
| F8.5_cond_event_err@train | F8.5_cond_event_err | train | F8_target | classification@val | 9 | 0.818 | 0.778 | 0.0195 | 0.0479 | True |
| F8.6_cond_future_ks@oot | F8.6_cond_future_ks | oot | F8_target | classification@oot | 9 | 0.818 | 0.889 | 0.00781 | 0.0304 | True |
| F11.3_multiclass_tvd@train | F11.3_multiclass_tvd | train | F11_class_balance | classification@val | 9 | 0.815 | 0.889 | 0.00781 | 0.0304 | True |
| F6.6_feature_fid@oot | F6.6_feature_fid | oot | F6_windows | classification@oot | 9 | 0.814 | 0.778 | 0.0273 | 0.0587 | False |
| F8.6_cond_future_ks | F8.6_cond_future_ks | val | F8_target | classification@oot | 9 | 0.803 | 0.778 | 0.0391 | 0.0747 | False |
| F8.4_event_by_how@train | F8.4_event_by_how | train | F8_target | regression@val | 9 | 0.8 | 0.667 | 0.0547 | 0.0937 | False |
| F8.4_event_by_how@oot | F8.4_event_by_how | oot | F8_target | regression@val | 9 | 0.8 | 0.889 | 0.0117 | 0.0363 | True |
| F8.1_class_tvd@train | F8.1_class_tvd | train | F8_target | classification@val | 9 | 0.797 | 0.667 | 0.0547 | 0.0937 | False |
| F8.6_cond_future_ks@train | F8.6_cond_future_ks | train | F8_target | classification@val | 9 | 0.796 | 0.889 | 0.00781 | 0.0304 | True |
| F8.6_cond_future_ks@oot | F8.6_cond_future_ks | oot | F8_target | classification@val | 9 | 0.795 | 0.889 | 0.00781 | 0.0304 | True |
| F8.5_cond_event_err@train | F8.5_cond_event_err | train | F8_target | regression@val | 9 | 0.795 | 0.778 | 0.0391 | 0.0747 | False |


### RQ5. Gap to real data (TSTR / TRTR), stability over time and across models

| method | unit | n_datasets | median_ratio | ci_lo | ci_hi | p_below_real | p_below_real_bh | verdict |
|---|---|---|---|---|---|---|---|---|
| chronos | classification@oot | 7 | 0.441 | 0.141 | 0.828 | 0.00781 | 0.0083 | worse than real |
| chronos | classification@val | 7 | 0.457 | 0.208 | 0.892 | 0.00781 | 0.0083 | worse than real |
| chronos | regression@oot | 7 | 0.69 | 0.631 | 0.812 | 0.00781 | 0.0083 | worse than real |
| chronos | regression@val | 7 | 0.819 | 0.672 | 0.954 | 0.0156 | 0.0158 | worse than real |
| diffusion_ts | classification@oot | 9 | 0.715 | 0.468 | 0.952 | 0.00195 | 0.00249 | worse than real |
| diffusion_ts | classification@val | 9 | 0.658 | 0.521 | 0.895 | 0.00195 | 0.00249 | worse than real |
| diffusion_ts | regression@oot | 9 | 0.792 | 0.705 | 0.933 | 0.00195 | 0.00249 | worse than real |
| diffusion_ts | regression@val | 9 | 0.769 | 0.536 | 0.924 | 0.00195 | 0.00249 | worse than real |
| timesfm | classification@oot | 6 | 0.677 | 0 | 0.964 | 0.0156 | 0.0158 | worse than real |
| timesfm | classification@val | 6 | 0.786 | 0 | 0.918 | 0.0156 | 0.0158 | worse than real |
| timesfm | regression@oot | 6 | 0.871 | 0.839 | 0.937 | 0.0156 | 0.0158 | worse than real |
| timesfm | regression@val | 6 | 0.892 | 0.768 | 0.991 | 0.0312 | 0.0312 | worse than real |
| timestral | classification@oot | 9 | 0 | -0.121 | 0.826 | 0.00195 | 0.00249 | worse than real |
| timestral | classification@val | 9 | 0 | -0.0623 | 0.277 | 0.00195 | 0.00249 | worse than real |
| timestral | regression@oot | 9 | 0.782 | 0.669 | 0.856 | 0.00195 | 0.00249 | worse than real |
| timestral | regression@val | 9 | 0.835 | 0.721 | 0.966 | 0.00195 | 0.00249 | worse than real |
| vae_atsp | classification@oot | 9 | 0.715 | 0.486 | 0.798 | 0.00195 | 0.00249 | worse than real |
| vae_atsp | classification@val | 9 | 0.714 | 0.349 | 0.85 | 0.00195 | 0.00249 | worse than real |
| vae_atsp | regression@oot | 9 | 0.563 | 0.454 | 0.607 | 0.00195 | 0.00249 | worse than real |
| vae_atsp | regression@val | 9 | 0.546 | 0.427 | 0.663 | 0.00195 | 0.00249 | worse than real |
| vae_greedy | classification@oot | 9 | 0.682 | 0.453 | 0.743 | 0.00195 | 0.00249 | worse than real |
| vae_greedy | classification@val | 9 | 0.691 | 0.411 | 0.823 | 0.00195 | 0.00249 | worse than real |
| vae_greedy | regression@oot | 9 | 0.562 | 0.517 | 0.744 | 0.00195 | 0.00249 | worse than real |
| vae_greedy | regression@val | 9 | 0.571 | 0.495 | 0.65 | 0.00195 | 0.00249 | worse than real |
| vae_herding | classification@oot | 9 | 0.673 | 0.551 | 0.833 | 0.00195 | 0.00249 | worse than real |
| vae_herding | classification@val | 9 | 0.718 | 0.562 | 0.835 | 0.00195 | 0.00249 | worse than real |
| vae_herding | regression@oot | 9 | 0.673 | 0.47 | 0.698 | 0.00195 | 0.00249 | worse than real |
| vae_herding | regression@val | 9 | 0.594 | 0.509 | 0.663 | 0.00195 | 0.00249 | worse than real |
| vae_knn | classification@oot | 9 | 0.677 | 0.491 | 0.826 | 0.00195 | 0.00249 | worse than real |
| vae_knn | classification@val | 9 | 0.649 | 0.608 | 0.836 | 0.00195 | 0.00249 | worse than real |
| vae_knn | regression@oot | 9 | 0.532 | 0.431 | 0.708 | 0.00195 | 0.00249 | worse than real |
| vae_knn | regression@val | 9 | 0.545 | 0.486 | 0.659 | 0.00195 | 0.00249 | worse than real |
| vae_mbb | classification@oot | 9 | 0.65 | 0.497 | 0.811 | 0.00195 | 0.00249 | worse than real |
| vae_mbb | classification@val | 9 | 0.656 | 0.315 | 0.785 | 0.00195 | 0.00249 | worse than real |
| vae_mbb | regression@oot | 9 | 0.538 | 0.398 | 0.569 | 0.00195 | 0.00249 | worse than real |
| vae_mbb | regression@val | 9 | 0.474 | 0.381 | 0.647 | 0.00195 | 0.00249 | worse than real |
| vae_pctsp | classification@oot | 9 | 0.702 | 0.498 | 0.768 | 0.00195 | 0.00249 | worse than real |
| vae_pctsp | classification@val | 9 | 0.695 | 0.636 | 0.843 | 0.00195 | 0.00249 | worse than real |
| vae_pctsp | regression@oot | 9 | 0.572 | 0.455 | 0.749 | 0.00195 | 0.00249 | worse than real |
| vae_pctsp | regression@val | 9 | 0.572 | 0.36 | 0.672 | 0.00195 | 0.00249 | worse than real |

_Showing 40 rows of 120 (rows with a better / worse / same verdict first); all of them — `hypotheses/RQ5_global.parquet`._

**rank_stability**

| comparison | criterion | tau |
|---|---|---|
| val ↔ oot | fidelity:dependence | 0.725 |
| val ↔ oot | fidelity:distribution | 0.783 |
| val ↔ oot | fidelity:long_structure | 0.609 |
| val ↔ oot | fidelity:seams | 0.971 |
| val ↔ oot | fidelity:target | 0.899 |
| val ↔ oot | fidelity:windows | 0.514 |
| val ↔ oot | theme:class_balance:fidelity | 0.833 |
| val ↔ oot | theme:class_balance:utility | 0.804 |
| val ↔ oot | theme:extremes:fidelity | 0.623 |
| val ↔ oot | theme:extremes:utility | 0.819 |
| val ↔ oot | utility:classification | 0.833 |
| val ↔ oot | utility:regression | 0.804 |
| linear ↔ gbdt | utility:classification@oot | 0.754 |
| linear ↔ gbdt | utility:classification@val | 0.79 |
| linear ↔ gbdt | utility:regression@oot | 0.855 |
| linear ↔ gbdt | utility:regression@val | 0.812 |


**rank_shift_oot_minus_val**

| method | utility:classification | utility:regression |
|---|---|---|
| chronos | 1.01 | 4.97 |
| diffusion_ts | 1.79 | 1 |
| timesfm | 0.69 | 1.01 |
| timestral | 0.19 | 3.19 |
| vae_atsp | 0.38 | 0.73 |
| vae_greedy | 0.12 | 0.61 |
| vae_herding | 0.39 | -0.26 |
| vae_knn | 0.18 | 0.74 |
| vae_mbb | -0.06 | 0.25 |
| vae_pctsp | 0.4 | 0.9 |
| vae_quilting | -0.54 | 0.38 |
| vae_rand | -0.09 | 0.12 |
| vae_zseries | 1.18 | 1.02 |
| zedge_atsp | -0.53 | -1.2 |
| zedge_greedy | -0.76 | -1.33 |
| zedge_herding | -0.82 | -1.29 |
| zedge_knn | -0.18 | -1.19 |
| zedge_mbb | -0.91 | -1.33 |
| zedge_pctsp | -0.23 | -1.45 |
| zedge_quilting | -1.3 | -2.51 |
| zedge_rand | -1.25 | -1.56 |
| zedge_ts_ar | -0.11 | -0.47 |
| zedge_ts_long | 0.5 | 0.16 |
| zedge_zseries | 0.39 | -1.04 |


**decision_transfer**: no model grid: profile max (decision_transfer=True)

### RQ6. Speed and cost: training and generation time, memory, Pareto front "quality × time"

| method | median_time_s | ci_lo | ci_hi | n_datasets | x_fastest |
|---|---|---|---|---|---|
| timestral | 1.24 | 1.23 | 1.24 | 9 | 1 |
| timesfm | 2.41 | 2.36 | 2.43 | 6 | 1.95 |
| chronos | 32.6 | 31.8 | 38.4 | 7 | 26.3 |
| vae_rand | 131 | 105 | 165 | 9 | 106 |
| vae_quilting | 131 | 105 | 165 | 9 | 106 |
| vae_greedy | 131 | 105 | 148 | 9 | 106 |
| vae_knn | 131 | 105 | 165 | 9 | 106 |
| vae_mbb | 131 | 105 | 165 | 9 | 106 |
| vae_herding | 131 | 105 | 165 | 9 | 106 |
| vae_zseries | 134 | 108 | 150 | 9 | 108 |
| vae_zseries_xfade | 134 | 110 | 168 | 9 | 108 |
| vae_zseries_quilt | 134 | 108 | 168 | 9 | 108 |
| vae_zseries_wsola | 134 | 108 | 168 | 9 | 108 |
| vae_atsp | 162 | 139 | 198 | 9 | 131 |
| vae_pctsp | 171 | 152 | 217 | 9 | 138 |
| zedge_rand | 798 | 654 | 1.01e+03 | 9 | 644 |
| zedge_quilting | 798 | 664 | 806 | 9 | 644 |
| zedge_greedy | 798 | 654 | 1.01e+03 | 9 | 644 |
| zedge_knn | 798 | 654 | 1.01e+03 | 9 | 644 |
| zedge_mbb | 798 | 654 | 1.01e+03 | 9 | 644 |
| zedge_herding | 798 | 654 | 1.01e+03 | 9 | 644 |
| zedge_zseries_quilt | 800 | 656 | 1.01e+03 | 9 | 646 |
| zedge_zseries_xfade | 800 | 656 | 1.01e+03 | 9 | 646 |
| zedge_zseries | 801 | 655 | 1.01e+03 | 9 | 646 |
| zedge_zseries_wsola | 801 | 656 | 1.01e+03 | 9 | 646 |
| zedge_atsp | 825 | 674 | 1.03e+03 | 9 | 665 |
| zedge_pctsp | 841 | 702 | 1.05e+03 | 9 | 679 |
| diffusion_ts | 2.35e+03 | 1.87e+03 | 3.1e+03 | 9 | 1.9e+03 |
| zedge_ts_long | 2.93e+03 | 2.61e+03 | 3.42e+03 | 9 | 2.37e+03 |
| zedge_ts_ar | 2.95e+03 | 2.63e+03 | 3.44e+03 | 9 | 2.38e+03 |

**cost_parts**

| method | total:wall_time | training:wall_time | generation:wall_time | memory:gpu_peak_mb | memory:rss_delta_mb |
|---|---|---|---|---|---|
| timestral | 1.2 | 0.9 | 0.3 | 2.24e+03 | 0 |
| timesfm | 2.4 | 2 | 0.5 | 2.25e+03 | 0 |
| chronos | 32.6 | 1.1 | 31.5 | 2.24e+03 | 0 |
| vae_rand | 131 | 131 | 0 | 2.23e+03 | 0 |
| vae_quilting | 131 | 131 | 0 | 2.23e+03 | 0 |
| vae_greedy | 131 | 131 | 0 | 2.23e+03 | 0 |
| vae_knn | 131 | 131 | 0 | 2.23e+03 | 0 |
| vae_mbb | 131 | 131 | 0 | 2.23e+03 | 0 |
| vae_herding | 131 | 131 | 0 | 2.23e+03 | 0 |
| vae_zseries | 134 | 131 | 2.3 | 2.38e+03 | 0 |
| vae_zseries_xfade | 134 | 131 | 2.5 | 2.38e+03 | 0 |
| vae_zseries_quilt | 134 | 131 | 2.6 | 2.38e+03 | 0 |
| vae_zseries_wsola | 134 | 131 | 2.7 | 2.38e+03 | 0 |
| vae_atsp | 162 | 131 | 31 | 2.23e+03 | 0 |
| vae_pctsp | 171 | 131 | 46.2 | 2.23e+03 | 0 |
| zedge_rand | 798 | 789 | 8.6 | 575 | 0 |
| zedge_quilting | 798 | 789 | 8.6 | 575 | 0 |
| zedge_greedy | 798 | 789 | 8.6 | 575 | 0 |
| zedge_knn | 798 | 789 | 8.6 | 575 | 0 |
| zedge_mbb | 798 | 789 | 8.6 | 575 | 0 |
| zedge_herding | 798 | 789 | 8.6 | 575 | 0 |
| zedge_zseries_quilt | 800 | 789 | 11.6 | 591 | 0 |
| zedge_zseries_xfade | 800 | 789 | 11.5 | 591 | 0 |
| zedge_zseries | 800 | 789 | 11.3 | 591 | 0 |
| zedge_zseries_wsola | 801 | 789 | 11.7 | 592 | 0 |
| zedge_atsp | 825 | 789 | 35.9 | 575 | 0 |
| zedge_pctsp | 841 | 789 | 53.3 | 575 | 0 |
| diffusion_ts | 2.35e+03 | 2.18e+03 | 165 | 2.24e+03 | 7.3 |
| zedge_ts_long | 2.93e+03 | 2.93e+03 | 2 | 531 | 0 |
| zedge_ts_ar | 2.95e+03 | 2.93e+03 | 13.9 | 472 | 0 |


**cost_ranks**

| method | cost@generation | cost@memory | cost@total | cost@training |
|---|---|---|---|---|
| timestral | 7.09 | 14.2 | 1 | 1 |
| timesfm | 7.95 | 15.7 | 2.01 | 2.84 |
| chronos | 20 | 14.9 | 2.73 | 2.01 |
| vae_rand | 1.02 | 13.7 | 3.49 | 7.59 |
| vae_quilting | 2.08 | 13.7 | 4.54 | 7.59 |
| vae_greedy | 3.18 | 13.8 | 5.64 | 7.59 |
| vae_knn | 4.05 | 13.7 | 6.52 | 7.59 |
| vae_mbb | 5.05 | 13.7 | 7.51 | 7.59 |
| vae_herding | 6.14 | 13.8 | 8.6 | 7.59 |
| vae_zseries | 9.47 | 16.6 | 9.64 | 7.59 |
| vae_zseries_xfade |  |  |  |  |
| vae_zseries_quilt |  |  |  |  |
| vae_zseries_wsola |  |  |  |  |
| vae_atsp | 19.9 | 15.4 | 10.8 | 7.59 |
| vae_pctsp | 21.8 | 14.1 | 11.5 | 7.59 |
| zedge_rand | 11 | 9.78 | 12.7 | 16.8 |
| zedge_quilting | 12.1 | 9.78 | 13.8 | 16.8 |
| zedge_greedy | 13.1 | 9.78 | 14.8 | 16.8 |
| zedge_knn | 14 | 9.78 | 15.8 | 16.8 |
| zedge_mbb | 15.1 | 9.78 | 16.8 | 16.8 |
| zedge_herding | 16.1 | 11 | 17.9 | 16.8 |
| zedge_zseries_quilt |  |  |  |  |
| zedge_zseries_xfade |  |  |  |  |
| zedge_zseries | 17.2 | 11 | 18.9 | 16.8 |
| zedge_zseries_wsola |  |  |  |  |
| zedge_atsp | 20.6 | 11.3 | 19.9 | 16.8 |
| zedge_pctsp | 22.6 | 9.95 | 20.9 | 16.8 |
| diffusion_ts | 24 | 20.8 | 22.6 | 22.6 |
| zedge_ts_long | 9.26 | 8.26 | 22.6 | 23.1 |
| zedge_ts_ar | 17.3 | 7.09 | 23.7 | 23.1 |


**pareto**

| ranking | method | family | avg_rank | rank_with_cost | median_time_s | pareto |
|---|---|---|---|---|---|---|
| holdout_clf | timestral | long-series generator | 17.8 | 14.4 | 1.23 | True |
| holdout_clf | timesfm | long-series generator | 15.7 | 13.4 | 2.38 | True |
| holdout_clf | chronos | long-series generator | 16.1 | 13.7 | 33.9 | False |
| holdout_clf | vae_rand | random selection | 15.9 | 13.4 | 131 | False |
| holdout_clf | vae_quilting | optimised selection | 13.8 | 12.3 | 131 | True |
| holdout_clf | vae_greedy | optimised selection | 15 | 13.2 | 131 | False |
| holdout_clf | vae_knn | optimised selection | 15.4 | 13.6 | 131 | False |
| holdout_clf | vae_mbb | optimised selection | 15.9 | 14.1 | 131 | False |
| holdout_clf | vae_herding | optimised selection | 14 | 13 | 131 | False |
| holdout_clf | vae_zseries | optimised selection | 13.6 | 13.5 | 134 | True |
| holdout_clf | vae_atsp | optimised selection | 14.7 | 14.2 | 164 | False |
| holdout_clf | vae_pctsp | optimised selection | 14.5 | 13.9 | 171 | False |
| holdout_clf | zedge_rand | random selection | 10.7 | 10.9 | 798 | True |
| holdout_clf | zedge_quilting | optimised selection | 8.39 | 9.52 | 798 | True |
| holdout_clf | zedge_greedy | optimised selection | 9.16 | 10.2 | 798 | False |
| holdout_clf | zedge_knn | optimised selection | 9.55 | 10.6 | 798 | False |
| holdout_clf | zedge_mbb | optimised selection | 10.5 | 11.4 | 798 | False |
| holdout_clf | zedge_herding | optimised selection | 10.6 | 11.8 | 798 | False |
| holdout_clf | zedge_zseries | optimised selection | 9.35 | 11.2 | 801 | False |
| holdout_clf | zedge_atsp | optimised selection | 9.37 | 11.5 | 822 | False |
| holdout_clf | zedge_pctsp | optimised selection | 9.15 | 11.2 | 839 | False |
| holdout_clf | diffusion_ts | long-series generator | 13.7 | 16.4 | 2.35e+03 | False |
| holdout_clf | zedge_ts_long | long-series generator | 9.97 | 11.8 | 2.93e+03 | False |
| holdout_clf | zedge_ts_ar | long-series generator | 9.13 | 11.2 | 2.95e+03 | False |
| holdout_reg | timestral | long-series generator | 13.1 | 11.2 | 1.23 | True |
| holdout_reg | timesfm | long-series generator | 11.4 | 10.5 | 2.38 | True |
| holdout_reg | chronos | long-series generator | 13.7 | 12 | 33.9 | False |
| holdout_reg | vae_rand | random selection | 16.9 | 14.1 | 131 | False |
| holdout_reg | vae_quilting | optimised selection | 14.4 | 12.6 | 131 | False |
| holdout_reg | vae_greedy | optimised selection | 15.3 | 13.4 | 131 | False |
| holdout_reg | vae_knn | optimised selection | 15.9 | 14 | 131 | False |
| holdout_reg | vae_mbb | optimised selection | 16.8 | 14.7 | 131 | False |
| holdout_reg | vae_herding | optimised selection | 14.6 | 13.5 | 131 | False |
| holdout_reg | vae_zseries | optimised selection | 13.7 | 13.5 | 134 | False |
| holdout_reg | vae_atsp | optimised selection | 15.1 | 14.4 | 164 | False |
| holdout_reg | vae_pctsp | optimised selection | 15 | 14.3 | 171 | False |
| holdout_reg | zedge_rand | random selection | 12.4 | 12 | 798 | False |
| holdout_reg | zedge_quilting | optimised selection | 8.46 | 9.57 | 798 | True |
| holdout_reg | zedge_greedy | optimised selection | 9.36 | 10.3 | 798 | False |
| holdout_reg | zedge_knn | optimised selection | 10.1 | 11 | 798 | False |


**hardware**: ['NVIDIA H200']

### RQ8. Class balance: do methods preserve class shares (rare events especially) and what does an error cost

| comparison | kind | unit | n_datasets | median_z | mean_z | ci_lo | ci_hi | p_better_adj | p_worse_adj | p_equiv_adj | n_better | n_worse | n_same | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| timestral vs assembly_median | fidelity | F11.1_class_share_logratio | 9 | -130 | -118 | -169 | -71 | 1 | 0.0903 | 1 | 0 | 9 | 0 | inconclusive |
| timestral vs assembly_median | fidelity | F11.1_class_share_logratio@oot | 9 | -133 | -146 | -228 | -76.6 | 1 | 0.0903 | 1 | 0 | 9 | 0 | inconclusive |
| zedge_atsp vs zedge_rand | utility | clf_up_h1_q90\|gbdt\|S\|oot\|ece | 9 | -0.282 | -0.727 | -1.69 | -0.0996 | 1 | 0.0903 | 0.4 | 0 | 0 | 0 | inconclusive |
| zedge_pctsp vs zedge_rand | utility | clf_up_h1_q90\|gbdt\|S\|oot\|ece | 9 | -0.585 | -0.641 | -1.21 | -0.193 | 1 | 0.0903 | 0.188 | 0 | 1 | 0 | inconclusive |
| diffusion_ts vs assembly_median | utility | clf_down_h24_q10\|gbdt\|S\|oot\|ece | 9 | -2.79 | -3.57 | -4.55 | -2.68 | 1 | 0.0903 | 1 | 0 | 9 | 0 | inconclusive |
| diffusion_ts vs assembly_median | utility | clf_up_h1_q90\|gbdt\|S\|oot\|ece | 9 | -2.8 | -2.96 | -4.1 | -1.84 | 1 | 0.0903 | 1 | 0 | 8 | 0 | inconclusive |
| diffusion_ts vs assembly_median | utility | clf_up_h24_q95\|gbdt\|S\|oot\|ece | 9 | -3.19 | -3.11 | -4.34 | -1.97 | 1 | 0.0903 | 1 | 0 | 6 | 0 | inconclusive |
| diffusion_ts vs assembly_median | utility | clf_up_h24_q99\|gbdt\|S\|oot\|ece | 9 | -2.1 | -2.59 | -4.36 | -1.38 | 1 | 0.0903 | 1 | 0 | 5 | 0 | inconclusive |
| diffusion_ts vs assembly_median | utility | clf_up_h6_q90\|gbdt\|S\|oot\|ece | 9 | -2.75 | -2.62 | -3.84 | -1.59 | 1 | 0.0903 | 1 | 0 | 8 | 0 | inconclusive |
| timestral vs assembly_median | utility | clf_down_h24_q10\|gbdt\|S\|oot\|ece | 9 | -6.38 | -7.58 | -11 | -4.57 | 1 | 0.0903 | 1 | 0 | 9 | 0 | inconclusive |
| timestral vs assembly_median | utility | clf_down_h24_q10\|gbdt\|S\|val\|ece | 9 | -8.43 | -7.55 | -9.63 | -5.54 | 1 | 0.0903 | 1 | 0 | 9 | 0 | inconclusive |
| timestral vs assembly_median | utility | clf_up_h1_q90\|gbdt\|S\|oot\|ece | 9 | -9.06 | -12.2 | -19.4 | -5.95 | 1 | 0.0903 | 1 | 0 | 9 | 0 | inconclusive |
| timestral vs assembly_median | utility | clf_up_h24_q90\|linear\|S\|val\|ece | 9 | -7.23 | -9.29 | -15 | -4.89 | 1 | 0.0903 | 1 | 0 | 8 | 0 | inconclusive |
| zedge_ts_long vs assembly_median | utility | clf_up_h24_q95\|gbdt\|S\|oot\|ece | 9 | -0.776 | -1.02 | -1.77 | -0.485 | 1 | 0.0903 | 0.453 | 0 | 2 | 0 | inconclusive |
| zedge_herding vs zedge_rand | fidelity | F11.2_rare_share_logratio@oot | 9 | 0.648 | 0.789 | 0.337 | 1.35 | 0.0972 | 1 | 0.303 | 1 | 0 | 0 | inconclusive |
| zedge_atsp vs zedge_rand | utility | clf_up_h168_q90\|linear\|S\|val\|ece | 9 | 3.94 | 4.02 | 2.21 | 5.88 | 0.0972 | 1 | 1 | 5 | 0 | 0 | inconclusive |
| zedge_greedy vs zedge_rand | utility | clf_up_h168_q90\|gbdt\|S\|val\|ece | 9 | 3.32 | 4.27 | 2.17 | 6.84 | 0.0972 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| zedge_greedy vs zedge_rand | utility | clf_up_h168_q90\|linear\|S\|oot\|ece | 9 | 5.1 | 4.25 | 2.31 | 6.18 | 0.0972 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| zedge_greedy vs zedge_rand | utility | clf_up_h24_q95\|linear\|S\|val\|ece | 9 | 0.763 | 1.15 | 0.578 | 1.74 | 0.0972 | 1 | 0.978 | 4 | 0 | 0 | inconclusive |
| zedge_knn vs zedge_rand | utility | clf_up_h168_q90\|linear\|S\|oot\|ece | 9 | 4.02 | 3.9 | 2.2 | 5.95 | 0.0972 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| zedge_zseries vs zedge_rand | utility | clf_up_h168_q90\|linear\|S\|oot\|ece | 9 | 2.69 | 3.23 | 1.76 | 4.66 | 0.0972 | 1 | 1 | 5 | 0 | 0 | inconclusive |
| zedge_zseries vs zedge_rand | utility | clf_up_h168_q90\|linear\|S\|val\|ece | 9 | 3.12 | 4.75 | 2.11 | 8.58 | 0.0972 | 1 | 1 | 5 | 0 | 0 | inconclusive |
| zedge_zseries_wsola vs zedge_rand | utility | clf_up_h168_q90\|linear\|S\|oot\|ece | 9 | 2.99 | 2.87 | 1.69 | 4.02 | 0.0972 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| zedge_zseries_wsola vs zedge_rand | utility | clf_up_h168_q90\|linear\|S\|val\|ece | 9 | 3.18 | 3.97 | 1.75 | 7.12 | 0.0972 | 1 | 1 | 5 | 0 | 0 | inconclusive |
| zedge_ts_ar vs assembly_median | utility | clf_up_h168_q90\|linear\|S\|val\|ece | 9 | 2.88 | 6.59 | 2.41 | 11.4 | 0.0972 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| zedge_ts_long vs assembly_median | utility | clf_up_h168_q90\|gbdt\|S\|val\|ece | 9 | 2.16 | 3.5 | 1.6 | 5.92 | 0.0972 | 1 | 1 | 5 | 0 | 0 | inconclusive |
| zedge_ts_long vs assembly_median | utility | clf_up_h168_q90\|linear\|S\|val\|ece | 9 | 3.42 | 3.56 | 2.23 | 4.9 | 0.0972 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| timestral vs assembly_median | fidelity | F11.2_rare_share_logratio | 9 | -33.6 | -44.7 | -78.9 | -21.3 | 1 | 0.11 | 1 | 0 | 8 | 0 | inconclusive |
| timestral vs assembly_median | fidelity | F11.2_rare_share_logratio@oot | 9 | -56.6 | -50.1 | -75.4 | -25.8 | 1 | 0.11 | 1 | 1 | 8 | 0 | inconclusive |
| zedge_zseries_wsola vs zedge_rand | utility | clf_up_h1_q90\|gbdt\|S\|oot\|ece | 9 | -0.935 | -0.767 | -1.31 | -0.309 | 1 | 0.11 | 0.569 | 0 | 0 | 0 | inconclusive |
| diffusion_ts vs assembly_median | utility | clf_up_h24_q90\|gbdt\|S\|oot\|ece | 9 | -1.67 | -2.33 | -3.8 | -1.17 | 1 | 0.11 | 1 | 0 | 7 | 0 | inconclusive |
| timestral vs assembly_median | utility | clf_up_h24_q90\|gbdt\|S\|oot\|ece | 9 | -4.24 | -4.65 | -7.25 | -2.42 | 1 | 0.11 | 1 | 0 | 8 | 0 | inconclusive |
| timestral vs assembly_median | utility | clf_up_h24_q90\|gbdt\|S\|val\|ece | 9 | -5.11 | -5.16 | -7.89 | -2.49 | 1 | 0.11 | 1 | 0 | 8 | 0 | inconclusive |
| timestral vs assembly_median | utility | clf_up_h24_q95\|gbdt\|S\|oot\|ece | 9 | -2.05 | -3.54 | -6.38 | -1.43 | 1 | 0.11 | 1 | 0 | 8 | 0 | inconclusive |
| zedge_ts_long vs assembly_median | utility | clf_up_h24_q90\|gbdt\|S\|oot\|ece | 9 | -0.676 | -1.11 | -2.09 | -0.411 | 1 | 0.11 | 0.62 | 0 | 3 | 0 | inconclusive |
| zedge_ts_long vs assembly_median | utility | clf_up_h6_q90\|gbdt\|S\|oot\|ece | 9 | -1.08 | -1.18 | -1.74 | -0.672 | 1 | 0.11 | 0.931 | 0 | 4 | 0 | inconclusive |
| zedge_atsp vs zedge_rand | utility | clf_up_h168_q90\|gbdt\|S\|val\|ece | 9 | 3.33 | 4.59 | 2.11 | 7.45 | 0.115 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| zedge_atsp vs zedge_rand | utility | clf_up_h168_q90\|linear\|S\|oot\|ece | 9 | 2.77 | 3.77 | 1.88 | 5.75 | 0.115 | 1 | 1 | 5 | 0 | 0 | inconclusive |
| zedge_greedy vs zedge_rand | utility | clf_up_h168_q90\|gbdt\|S\|oot\|ece | 9 | 3.9 | 2.95 | 1.72 | 4.12 | 0.115 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| zedge_knn vs zedge_rand | utility | clf_up_h168_q90\|gbdt\|S\|val\|ece | 9 | 2.4 | 3.81 | 1.63 | 6.61 | 0.115 | 1 | 1 | 6 | 0 | 0 | inconclusive |

_Showing 40 rows of 647 (rows with a better / worse / same verdict first); all of them — `hypotheses/RQ8_global.parquet`._

**ranking**

| theme:class_balance:fidelity@oot | theme:class_balance:fidelity@train | theme:class_balance:fidelity@val | theme:class_balance:utility@oot | theme:class_balance:utility@val |
|---|---|---|---|---|
| 15.7 | 17.1 | 14.9 | 15.8 | 14.1 |
| 14.3 | 15.5 | 11.9 | 14.5 | 12.3 |
| 18.3 | 18.8 | 18.9 | 16.5 | 15.8 |
| 20 | 20.9 | 19.4 | 19.5 | 18.7 |
| 11.7 | 9.47 | 10.6 | 9.98 | 9.16 |
| 11.8 | 9.99 | 10.3 | 10.2 | 9.37 |
| 14.6 | 15.5 | 14.9 | 15.2 | 14.5 |
| 14.6 | 16.1 | 15.3 | 15.5 | 14.5 |
| 13 | 12.4 | 13 | 13.8 | 13.6 |
| 15.5 | 16.9 | 16 | 15.9 | 14.7 |
| 16.8 | 17.1 | 17.1 | 16.2 | 15.3 |
| 13.8 | 15.1 | 14.3 | 15.9 | 15 |
| 13.9 | 15.3 | 14.6 | 14.4 | 14.2 |
| 10.8 | 12 | 11.8 | 13.1 | 12.9 |
| 8.31 | 6.72 | 8.11 | 8.91 | 10.1 |
| 8.67 | 7.35 | 8.29 | 8.2 | 9.27 |
| 9.39 | 9.25 | 10.1 | 9.61 | 11.3 |
| 8.64 | 8.3 | 8.96 | 8.72 | 10.1 |
| 10.2 | 10.7 | 10.8 | 9.66 | 11.1 |
| 8.86 | 7.2 | 8.53 | 8.71 | 9.95 |
| 8.19 | 7.37 | 9.05 | 7.31 | 9.5 |
| 8.6 | 6.32 | 8.09 | 8.3 | 8.85 |
| 16.9 | 17.2 | 17 | 16.4 | 15.5 |
| 10.1 | 10.8 | 10.8 | 9.93 | 11.7 |


**ranking_tests**

| column | p_friedman | nemenyi_cd | n_blocks | n_methods_friedman | best |
|---|---|---|---|---|---|
| theme:class_balance:fidelity@oot | 8.78e-08 | 11 | 9 | 22 | zedge_quilting |
| theme:class_balance:fidelity@train | 6.1e-16 | 11 | 9 | 22 | zedge_zseries |
| theme:class_balance:fidelity@val | 6.49e-09 | 11 | 9 | 22 | zedge_zseries |
| theme:class_balance:utility@oot | 3.87e-12 | 11 | 9 | 22 | zedge_quilting |
| theme:class_balance:utility@val | 1.51e-09 | 11 | 9 | 22 | zedge_zseries |


**verdicts_by_comparison**

| kind | comparison | inconclusive |
|---|---|---|
| fidelity | chronos vs assembly_median | 9 |
| fidelity | diffusion_ts vs assembly_median | 8 |
| fidelity | timesfm vs assembly_median | 8 |
| fidelity | timestral vs assembly_median | 8 |
| fidelity | zedge_atsp vs zedge_rand | 8 |
| fidelity | zedge_greedy vs zedge_rand | 8 |
| fidelity | zedge_herding vs zedge_rand | 8 |
| fidelity | zedge_knn vs zedge_rand | 8 |
| fidelity | zedge_mbb vs zedge_rand | 8 |
| fidelity | zedge_pctsp vs zedge_rand | 8 |
| fidelity | zedge_quilting vs zedge_rand | 8 |
| fidelity | zedge_ts_ar vs assembly_median | 8 |
| fidelity | zedge_ts_long vs assembly_median | 8 |
| fidelity | zedge_zseries vs zedge_rand | 8 |
| fidelity | zedge_zseries_quilt vs zedge_rand | 8 |
| fidelity | zedge_zseries_wsola vs zedge_rand | 8 |
| fidelity | zedge_zseries_xfade vs zedge_rand | 8 |
| utility | chronos vs assembly_median | 30 |
| utility | diffusion_ts vs assembly_median | 30 |
| utility | timesfm vs assembly_median | 30 |
| utility | timestral vs assembly_median | 30 |
| utility | zedge_atsp vs zedge_rand | 30 |
| utility | zedge_greedy vs zedge_rand | 30 |
| utility | zedge_herding vs zedge_rand | 30 |
| utility | zedge_knn vs zedge_rand | 30 |
| utility | zedge_mbb vs zedge_rand | 30 |
| utility | zedge_pctsp vs zedge_rand | 30 |
| utility | zedge_quilting vs zedge_rand | 30 |
| utility | zedge_ts_ar vs assembly_median | 30 |
| utility | zedge_ts_long vs assembly_median | 30 |
| utility | zedge_zseries vs zedge_rand | 30 |
| utility | zedge_zseries_quilt vs zedge_rand | 30 |
| utility | zedge_zseries_wsola vs zedge_rand | 30 |
| utility | zedge_zseries_xfade vs zedge_rand | 30 |


**fidelity_predicts_utility**

| unit | reference | n_datasets | median_rho | share_positive | p_two_sided | p_bh |
|---|---|---|---|---|---|---|
| F11.1_class_share_logratio@oot | oot | 9 | 0.8 | 1 | 0.00391 | 0.00488 |
| F11.2_rare_share_logratio@oot | oot | 9 | 0.747 | 1 | 0.00391 | 0.00488 |
| F11.1_class_share_logratio | val | 9 | 0.744 | 1 | 0.00391 | 0.00488 |
| F8.1_class_tvd | val | 9 | 0.717 | 1 | 0.00391 | 0.00488 |
| F11.2_rare_share_logratio | val | 9 | 0.708 | 1 | 0.00391 | 0.00488 |
| F11.3_multiclass_tvd | val | 9 | 0.688 | 1 | 0.00391 | 0.00488 |
| F11.3_multiclass_tvd@oot | oot | 9 | 0.675 | 1 | 0.00391 | 0.00488 |
| F8.1_class_tvd@oot | oot | 9 | 0.593 | 1 | 0.00391 | 0.00488 |
| F11.4_minority_lost | val | 8 | 0.334 | 1 | 0.00781 | 0.00781 |
| F11.4_minority_lost@oot | oot | 8 | 0.313 | 1 | 0.00781 | 0.00781 |


### RQ9. Outliers and extremes: do methods preserve tails and outliers, and does it matter to the models

| comparison | kind | unit | n_datasets | median_z | mean_z | ci_lo | ci_hi | p_better_adj | p_worse_adj | p_equiv_adj | n_better | n_worse | n_same | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| zedge_atsp vs zedge_rand | utility | clf_up_h24_q95\|gbdt\|S\|val\|pr_auc | 9 | 1.21 | 1.99 | 0.633 | 3.95 | 0.0246 | 1 | 1 | 1 | 0 | 0 | better |
| zedge_atsp vs zedge_rand | utility | reg_h168\|linear\|S\|oot\|mae_extreme | 9 | 4.63 | 5.54 | 3.14 | 8.35 | 0.0246 | 1 | 1 | 8 | 0 | 0 | better |
| zedge_atsp vs zedge_rand | utility | reg_h168\|linear\|S\|val\|mae_extreme | 9 | 2.67 | 5.11 | 2.24 | 8.47 | 0.0246 | 1 | 1 | 6 | 0 | 0 | better |
| zedge_greedy vs zedge_rand | utility | reg_h168\|gbdt\|S\|oot\|mae_extreme | 9 | 1.86 | 3.11 | 1.68 | 4.67 | 0.0246 | 1 | 1 | 6 | 0 | 0 | better |
| zedge_greedy vs zedge_rand | utility | reg_h168\|gbdt\|S\|val\|mae_extreme | 9 | 1.88 | 2.3 | 1.22 | 3.61 | 0.0246 | 1 | 1 | 6 | 0 | 0 | better |
| zedge_greedy vs zedge_rand | utility | reg_h168\|linear\|S\|oot\|mae_extreme | 9 | 3.29 | 4.82 | 2.9 | 7.21 | 0.0246 | 1 | 1 | 7 | 0 | 0 | better |
| zedge_greedy vs zedge_rand | utility | reg_h168\|linear\|S\|val\|mae_extreme | 9 | 3.03 | 4.55 | 2.12 | 7.31 | 0.0246 | 1 | 1 | 7 | 0 | 0 | better |
| zedge_greedy vs zedge_rand | utility | reg_h1\|linear\|S\|oot\|mae_extreme | 9 | 2.53 | 2.78 | 1.24 | 4.6 | 0.0246 | 1 | 1 | 4 | 0 | 0 | better |
| zedge_greedy vs zedge_rand | utility | reg_h1\|linear\|S\|val\|mae_extreme | 9 | 3.62 | 3.93 | 1.82 | 6.22 | 0.0246 | 1 | 1 | 5 | 0 | 0 | better |
| zedge_greedy vs zedge_rand | utility | reg_h24\|gbdt\|S\|oot\|mae_extreme | 9 | 1.49 | 1.32 | 0.797 | 1.87 | 0.0246 | 1 | 0.972 | 4 | 0 | 0 | better |
| zedge_greedy vs zedge_rand | utility | reg_h24\|linear\|S\|oot\|mae_extreme | 9 | 2.59 | 2.43 | 1.56 | 3.32 | 0.0246 | 1 | 1 | 6 | 0 | 0 | better |
| zedge_greedy vs zedge_rand | utility | reg_h24\|linear\|S\|val\|mae_extreme | 9 | 2.31 | 2.32 | 1.49 | 3.1 | 0.0246 | 1 | 1 | 7 | 0 | 0 | better |
| zedge_knn vs zedge_rand | utility | clf_up_h24_q95\|gbdt\|S\|val\|pr_auc | 9 | 1.17 | 1.86 | 0.741 | 3.85 | 0.0246 | 1 | 1 | 1 | 0 | 0 | better |
| zedge_knn vs zedge_rand | utility | reg_h168\|gbdt\|S\|oot\|mae_extreme | 9 | 1.42 | 2.13 | 1.17 | 3.2 | 0.0246 | 1 | 1 | 6 | 0 | 0 | better |
| zedge_knn vs zedge_rand | utility | reg_h168\|gbdt\|S\|val\|mae_extreme | 9 | 1.34 | 1.89 | 1.18 | 2.84 | 0.0246 | 1 | 1 | 6 | 0 | 0 | better |
| zedge_knn vs zedge_rand | utility | reg_h168\|linear\|S\|oot\|mae_extreme | 9 | 3.19 | 3.77 | 2.32 | 5.64 | 0.0246 | 1 | 1 | 7 | 0 | 0 | better |
| zedge_knn vs zedge_rand | utility | reg_h168\|linear\|S\|val\|mae_extreme | 9 | 3.22 | 3.99 | 2.29 | 5.95 | 0.0246 | 1 | 1 | 7 | 0 | 0 | better |
| zedge_knn vs zedge_rand | utility | reg_h1\|linear\|S\|oot\|mae_extreme | 9 | 2.53 | 2.58 | 1.4 | 3.84 | 0.0246 | 1 | 1 | 5 | 0 | 0 | better |
| zedge_knn vs zedge_rand | utility | reg_h1\|linear\|S\|val\|mae_extreme | 9 | 3.43 | 3.45 | 1.74 | 5.25 | 0.0246 | 1 | 1 | 5 | 0 | 0 | better |
| zedge_knn vs zedge_rand | utility | reg_h24\|linear\|S\|oot\|mae_extreme | 9 | 1.63 | 1.86 | 1.12 | 2.61 | 0.0246 | 1 | 1 | 6 | 0 | 0 | better |
| zedge_knn vs zedge_rand | utility | reg_h24\|linear\|S\|val\|mae_extreme | 9 | 2.09 | 1.91 | 1.26 | 2.55 | 0.0246 | 1 | 1 | 6 | 0 | 0 | better |
| zedge_pctsp vs zedge_rand | utility | clf_up_h24_q95\|gbdt\|S\|val\|pr_auc | 9 | 1.29 | 2.08 | 0.73 | 4.04 | 0.0246 | 1 | 1 | 1 | 0 | 0 | better |
| zedge_pctsp vs zedge_rand | utility | reg_h168\|gbdt\|S\|oot\|mae_extreme | 9 | 1.84 | 3.37 | 1.85 | 5.04 | 0.0246 | 1 | 1 | 6 | 0 | 0 | better |
| zedge_pctsp vs zedge_rand | utility | reg_h168\|gbdt\|S\|val\|mae_extreme | 9 | 1.68 | 2.47 | 1.26 | 3.94 | 0.0246 | 1 | 1 | 6 | 0 | 0 | better |
| zedge_pctsp vs zedge_rand | utility | reg_h168\|linear\|S\|oot\|mae_extreme | 9 | 4.39 | 5.37 | 3.34 | 7.84 | 0.0246 | 1 | 1 | 8 | 0 | 0 | better |
| zedge_pctsp vs zedge_rand | utility | reg_h168\|linear\|S\|val\|mae_extreme | 9 | 3.21 | 5.19 | 2.7 | 8.21 | 0.0246 | 1 | 1 | 7 | 0 | 0 | better |
| zedge_pctsp vs zedge_rand | utility | reg_h1\|linear\|S\|oot\|mae_extreme | 9 | 2.46 | 3.16 | 1.26 | 5.58 | 0.0246 | 1 | 1 | 4 | 0 | 0 | better |
| zedge_pctsp vs zedge_rand | utility | reg_h1\|linear\|S\|val\|mae_extreme | 9 | 3.65 | 4.46 | 1.97 | 7.4 | 0.0246 | 1 | 1 | 6 | 0 | 0 | better |
| zedge_pctsp vs zedge_rand | utility | reg_h24\|gbdt\|S\|oot\|mae_extreme | 9 | 1.5 | 1.54 | 0.854 | 2.28 | 0.0246 | 1 | 1 | 4 | 0 | 0 | better |
| zedge_pctsp vs zedge_rand | utility | reg_h24\|gbdt\|S\|val\|mae_extreme | 9 | 1.47 | 1.52 | 0.898 | 2.29 | 0.0246 | 1 | 1 | 3 | 0 | 0 | better |
| zedge_pctsp vs zedge_rand | utility | reg_h24\|linear\|S\|oot\|mae_extreme | 9 | 2.54 | 2.66 | 1.72 | 3.66 | 0.0246 | 1 | 1 | 6 | 0 | 0 | better |
| zedge_pctsp vs zedge_rand | utility | reg_h24\|linear\|S\|val\|mae_extreme | 9 | 2.5 | 2.66 | 1.7 | 3.62 | 0.0246 | 1 | 1 | 7 | 0 | 0 | better |
| zedge_quilting vs zedge_rand | utility | clf_up_h24_q95\|gbdt\|S\|val\|pr_auc | 9 | 1.63 | 1.85 | 0.767 | 3.62 | 0.0246 | 1 | 1 | 2 | 0 | 0 | better |
| zedge_quilting vs zedge_rand | utility | reg_h168\|gbdt\|S\|oot\|mae_extreme | 9 | 2.16 | 3.82 | 2.13 | 5.75 | 0.0246 | 1 | 1 | 8 | 0 | 0 | better |
| zedge_quilting vs zedge_rand | utility | reg_h168\|gbdt\|S\|val\|mae_extreme | 9 | 1.81 | 2.98 | 1.65 | 4.69 | 0.0246 | 1 | 1 | 7 | 0 | 0 | better |
| zedge_quilting vs zedge_rand | utility | reg_h168\|linear\|S\|val\|mae_extreme | 9 | 3.68 | 5.79 | 3 | 9.19 | 0.0246 | 1 | 1 | 8 | 0 | 0 | better |
| zedge_quilting vs zedge_rand | utility | reg_h1\|linear\|S\|val\|mae_extreme | 9 | 1.89 | 2.54 | 1.27 | 4.18 | 0.0246 | 1 | 1 | 5 | 0 | 0 | better |
| zedge_quilting vs zedge_rand | utility | reg_h24\|gbdt\|S\|oot\|mae_extreme | 9 | 1.55 | 1.78 | 1.19 | 2.45 | 0.0246 | 1 | 1 | 5 | 0 | 0 | better |
| zedge_quilting vs zedge_rand | utility | reg_h24\|linear\|S\|oot\|mae_extreme | 9 | 3.1 | 3.05 | 1.97 | 4.24 | 0.0246 | 1 | 1 | 8 | 0 | 0 | better |
| zedge_quilting vs zedge_rand | utility | reg_h24\|linear\|S\|val\|mae_extreme | 9 | 2.48 | 3 | 1.88 | 4.18 | 0.0246 | 1 | 1 | 8 | 0 | 0 | better |

_Showing 40 rows of 782 (rows with a better / worse / same verdict first); all of them — `hypotheses/RQ9_global.parquet`._

**ranking**

| theme:extremes:fidelity@oot | theme:extremes:fidelity@train | theme:extremes:fidelity@val | theme:extremes:utility@oot | theme:extremes:utility@val |
|---|---|---|---|---|
| 17 | 19 | 13.5 | 14.9 | 13.1 |
| 12.9 | 14.8 | 11.8 | 12.6 | 11.8 |
| 14.3 | 14.9 | 11.7 | 9.97 | 10.6 |
| 16.4 | 19 | 12.9 | 14.6 | 13.6 |
| 10.9 | 5.55 | 10.8 | 7.16 | 7.99 |
| 10.8 | 6.09 | 10.8 | 8.95 | 9.71 |
| 13.3 | 16.6 | 13.6 | 14.9 | 14.4 |
| 13.7 | 16.8 | 13.9 | 14.8 | 14.5 |
| 11.6 | 13.7 | 11.9 | 15.7 | 15.2 |
| 13.7 | 16.7 | 13.7 | 15.8 | 15 |
| 12.8 | 16 | 13.8 | 17 | 16.6 |
| 13.4 | 17.2 | 13.6 | 15.1 | 14.4 |
| 14.1 | 17.1 | 14.4 | 14.5 | 14.5 |
| 12.5 | 15.8 | 12.9 | 13.9 | 13.5 |
| 12 | 9.37 | 12.4 | 9.45 | 9.64 |
| 11.2 | 8.6 | 12.2 | 8.69 | 9.25 |
| 10.4 | 7.81 | 11.1 | 12.8 | 13.1 |
| 11.4 | 8.66 | 12 | 10.6 | 10.4 |
| 11.2 | 8.04 | 11.7 | 12.4 | 13.1 |
| 12.2 | 9.37 | 12.6 | 8.8 | 9.11 |
| 11.2 | 9.51 | 11.7 | 8.12 | 9.58 |
| 11 | 8.21 | 11.8 | 9.7 | 9.69 |
| 12.6 | 15.9 | 13.4 | 16.8 | 16.7 |
| 11.2 | 8.05 | 11.9 | 12.6 | 13.9 |


**ranking_tests**

| column | p_friedman | nemenyi_cd | n_blocks | n_methods_friedman | best |
|---|---|---|---|---|---|
| theme:extremes:fidelity@oot | 0.0572 | 11 | 9 | 22 | zedge_herding |
| theme:extremes:fidelity@train | 2.33e-23 | 11 | 9 | 22 | zedge_ts_ar |
| theme:extremes:fidelity@val | 0.736 | 11 | 9 | 22 | zedge_ts_long |
| theme:extremes:utility@oot | 2.86e-12 | 11 | 9 | 22 | zedge_ts_ar |
| theme:extremes:utility@val | 4.42e-08 | 11 | 9 | 22 | zedge_ts_ar |


**verdicts_by_comparison**

| kind | comparison | better | inconclusive | same |
|---|---|---|---|---|
| fidelity | chronos vs assembly_median | 0 | 22 | 0 |
| fidelity | diffusion_ts vs assembly_median | 0 | 22 | 0 |
| fidelity | timesfm vs assembly_median | 0 | 22 | 0 |
| fidelity | timestral vs assembly_median | 0 | 22 | 0 |
| fidelity | zedge_atsp vs zedge_rand | 0 | 22 | 0 |
| fidelity | zedge_greedy vs zedge_rand | 0 | 21 | 1 |
| fidelity | zedge_herding vs zedge_rand | 0 | 19 | 3 |
| fidelity | zedge_knn vs zedge_rand | 0 | 19 | 3 |
| fidelity | zedge_mbb vs zedge_rand | 0 | 14 | 8 |
| fidelity | zedge_pctsp vs zedge_rand | 0 | 22 | 0 |
| fidelity | zedge_quilting vs zedge_rand | 0 | 21 | 1 |
| fidelity | zedge_ts_ar vs assembly_median | 0 | 22 | 0 |
| fidelity | zedge_ts_long vs assembly_median | 0 | 22 | 0 |
| fidelity | zedge_zseries vs zedge_rand | 0 | 21 | 1 |
| fidelity | zedge_zseries_quilt vs zedge_rand | 0 | 21 | 1 |
| fidelity | zedge_zseries_wsola vs zedge_rand | 0 | 21 | 1 |
| fidelity | zedge_zseries_xfade vs zedge_rand | 0 | 21 | 1 |
| utility | chronos vs assembly_median | 0 | 24 | 0 |
| utility | diffusion_ts vs assembly_median | 0 | 24 | 0 |
| utility | timesfm vs assembly_median | 0 | 24 | 0 |
| utility | timestral vs assembly_median | 1 | 23 | 0 |
| utility | zedge_atsp vs zedge_rand | 3 | 21 | 0 |
| utility | zedge_greedy vs zedge_rand | 9 | 15 | 0 |
| utility | zedge_herding vs zedge_rand | 0 | 19 | 5 |
| utility | zedge_knn vs zedge_rand | 9 | 15 | 0 |
| utility | zedge_mbb vs zedge_rand | 0 | 17 | 7 |
| utility | zedge_pctsp vs zedge_rand | 11 | 13 | 0 |
| utility | zedge_quilting vs zedge_rand | 8 | 16 | 0 |
| utility | zedge_ts_ar vs assembly_median | 0 | 24 | 0 |
| utility | zedge_ts_long vs assembly_median | 1 | 23 | 0 |
| utility | zedge_zseries vs zedge_rand | 9 | 15 | 0 |
| utility | zedge_zseries_quilt vs zedge_rand | 0 | 24 | 0 |
| utility | zedge_zseries_wsola vs zedge_rand | 7 | 17 | 0 |
| utility | zedge_zseries_xfade vs zedge_rand | 0 | 24 | 0 |


**fidelity_predicts_utility**

| unit | reference | n_datasets | median_rho | share_positive | p_two_sided | p_bh |
|---|---|---|---|---|---|---|
| F12.1_exceed_rate_err@oot | oot | 9 | 0.515 | 1 | 0.00391 | 0.0573 |
| F1.5_q99_err | val | 9 | 0.501 | 0.889 | 0.00781 | 0.0573 |
| F1.5_q99_err@oot | oot | 9 | 0.496 | 0.889 | 0.00781 | 0.0573 |
| F1.10_hill_err | val | 9 | 0.431 | 0.667 | 0.203 | 0.319 |
| F12.4_block_max_ks@oot | oot | 9 | 0.407 | 0.778 | 0.0547 | 0.15 |
| F12.5_block_min_ks@oot | oot | 9 | 0.392 | 0.889 | 0.0547 | 0.15 |
| F1.10_hill_err@oot | oot | 9 | 0.391 | 0.667 | 0.203 | 0.319 |
| F1.5_q01_err | val | 9 | 0.357 | 0.778 | 0.0977 | 0.179 |
| F1.5_q01_err@oot | oot | 9 | 0.34 | 0.778 | 0.0742 | 0.163 |
| F12.4_block_max_ks | val | 8 | 0.33 | 0.875 | 0.0234 | 0.129 |
| F2.4_big_jump_share_err@oot | oot | 9 | 0.329 | 0.778 | 0.0391 | 0.15 |
| F12.1_exceed_rate_err | val | 9 | 0.321 | 0.778 | 0.0742 | 0.163 |
| F12.3_spike_rate_err | val | 9 | 0.318 | 0.778 | 0.0977 | 0.179 |
| F12.5_block_min_ks | val | 9 | 0.298 | 0.556 | 0.301 | 0.441 |
| F12.2_exceed_magnitude_err | val | 9 | 0.274 | 0.667 | 0.426 | 0.585 |
| F12.3_spike_rate_err@oot | oot | 9 | 0.24 | 0.889 | 0.0547 | 0.15 |
| F2.4_big_jump_share_err | val | 9 | 0.234 | 0.556 | 0.82 | 0.82 |
| F7.4_excursion_ks@oot | oot | 6 | 0.194 | 0.5 | 0.688 | 0.808 |
| F7.4_excursion_ks | val | 6 | 0.161 | 0.5 | 0.562 | 0.728 |
| F1.6_kurt_err@oot | oot | 9 | 0.134 | 0.556 | 0.734 | 0.808 |
| F1.6_kurt_err | val | 9 | 0.133 | 0.556 | 0.734 | 0.808 |
| F12.2_exceed_magnitude_err@oot | oot | 9 | 0.0508 | 0.556 | 0.82 | 0.82 |

