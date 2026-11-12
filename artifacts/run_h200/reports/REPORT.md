# Benchmark report

Datasets: beijing_pm25, bike, bitcoin, electricity, ett, household, jena, metro, pjm. Seeds: 10. α = 0.05. Leakage (Config.leaked): `chronos` on electricity, beijing_pm25; `timesfm` on beijing_pm25, household, bitcoin. Verdict of a comparison "A vs B": better / worse (A better / worse than B) / same (equivalence, TOST) / inconclusive. Effects are in noise units — divided by the smallest effect size of interest (SESOI: the median |vae_rand − vae_rand_b| on one pool — or, where vae_rand_b is not run (min), the between-seed spread of vae_rand — or the method's between-seed spread, see HYPOTHESES.md §2). Utility: TSTR (training on synthetic data only) vs TRTR (training on real data), tested on the real val / OOT; transfer ratio = 1 — synthetic data train the model as well as real data. Overall leaderboard — `OVERALL.md`; ranking of every method in every slice — `LEADERBOARD.md`; values of the metrics by slice — `METRIC_VALUES.md` (this folder). Tables of the tests — `hypotheses/`.

## Overall leaderboard

Fidelity on the core metrics (each criterion against train, val and OOT) and utility (TSTR classification and regression, val and OOT), equal weights; noise-aware ranks; privacy and cost not included. Composition, columns and the robustness checks — `OVERALL.md`.

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon | fidelity_rank | utility_rank | norm_overall | memorisation_flag |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| zedge_quilting | optimised selection | 8.27 | 7.35 | 9.2 | 0.85 | 0.966 |  | True | 8.29 | 8.25 | 0.462 | False |
| zedge_zseries | optimised selection | 8.79 | 8.28 | 9.47 | 0.084 | 0.753 | 0.41 | True | 8.86 | 8.72 | 0.26 | False |
| zedge_greedy | optimised selection | 8.95 | 7.97 | 10 | 0.013 | 0.717 | 0.41 | True | 8.98 | 8.92 | 0.284 | False |
| zedge_pctsp | optimised selection | 9.18 | 8.13 | 10.2 | 0.001 | 0.175 | 0.293 | True | 9.09 | 9.26 | 0.251 | False |
| zedge_knn | optimised selection | 9.33 | 8.32 | 10.5 | 0.001 | 0.044 | 0.41 | True | 9.3 | 9.37 | 0.388 | False |
| zedge_atsp | optimised selection | 9.39 | 7.83 | 11.1 | 0.029 | 0.162 | 0.41 | True | 9.13 | 9.64 | 0.302 | False |
| zedge_ts_ar | long-series generator | 9.4 | 7.99 | 10.9 | 0.021 | 0.149 | 0.41 | True | 10.1 | 8.69 | 0.783 | False |
| zedge_ts_long | long-series generator | 9.5 | 8.25 | 10.9 | 0.001 | 0.034 | 0.191 | True | 9.51 | 9.49 | 0.736 | False |
| zedge_herding | optimised selection | 10.5 | 9.15 | 11.9 | 0 | 0 | 0.107 | True | 10.3 | 10.7 | 0.047 | False |
| zedge_mbb | optimised selection | 10.6 | 9.1 | 12.3 | 0 | 0 | 0.123 | True | 10.5 | 10.7 | 0.0562 | False |
| zedge_rand | random selection | 10.7 | 9.12 | 12.5 | 0 | 0 | 0.107 | True | 10.5 | 11 | 0 | False |
| vae_herding | optimised selection | 13.5 | 12.8 | 14.3 | 0 | 0 | 0.0449 | False | 13.1 | 13.9 | 0.302 | False |
| vae_zseries | optimised selection | 13.7 | 12.1 | 15.2 | 0 | 0 | 0.0547 | True | 13.4 | 13.9 | 0.34 | False |
| diffusion_ts | long-series generator | 13.8 | 12 | 15.4 | 0 | 0 | 0.0449 | False | 14.3 | 13.2 | 0.466 | False |
| timesfm | long-series generator | 14.4 | 12.6 | 16.2 | 0 | 0 | 0.125 | True | 15.2 | 13.6 | 0.106 | False |
| vae_quilting | optimised selection | 14.4 | 12.6 | 16.2 | 0 | 0 | 0.0547 | True | 14.2 | 14.7 | 0.125 | False |
| vae_pctsp | optimised selection | 15.3 | 13.8 | 16.7 | 0 | 0 | 0.0449 | False | 14.9 | 15.7 | 0.146 | False |
| vae_atsp | optimised selection | 15.3 | 13.3 | 17.1 | 0 | 0 | 0.0449 | False | 15.2 | 15.3 | 0.153 | False |
| vae_greedy | optimised selection | 15.6 | 13.9 | 17.2 | 0 | 0 | 0.0449 | False | 15.5 | 15.7 | 0.0733 | False |
| chronos | long-series generator | 15.8 | 14 | 17.5 | 0 | 0 | 0.0938 | True | 16.4 | 15.2 | -0.125 | False |
| vae_knn | optimised selection | 16 | 14.2 | 17.7 | 0 | 0 | 0.0449 | False | 16 | 16 | 0.0861 | False |
| vae_mbb | optimised selection | 16.3 | 14.2 | 18.2 | 0 | 0 | 0.0449 | False | 16.3 | 16.3 | 0.0773 | False |
| vae_rand | random selection | 16.5 | 14.4 | 18.4 | 0 | 0 | 0.0449 | False | 16.5 | 16.4 | 0 | False |
| timestral | long-series generator | 16.8 | 15.5 | 18.1 | 0 | 0 | 0.0449 | False | 17.3 | 16.2 | -0.443 | False |


Sensitivity variants:

| variant | text | first | tau_vs_main | main_first_place |
|---|---|---|---|---|
| main | the leaderboard: core metrics, fidelity against train + val + OOT, noise-aware ranks | zedge_quilting | 1 | 1 |
| plain_ranks | ordinary average ranks (no ties within the noise) | zedge_quilting | 0.971 | 1 |
| fidelity_train | fidelity against train only | zedge_quilting | 0.978 | 1 |
| fidelity_holdout | fidelity against val + OOT only | zedge_quilting | 0.942 | 1 |
| no_unchecked | without F5.7 (seams, no anchor) and F6.1 against val (noise) | zedge_quilting | 0.942 | 1 |
| all_metrics | every fidelity metric instead of the core set | zedge_quilting | 0.92 | 1 |
| common_datasets | only the datasets where every method is ranked | zedge_quilting | 0.942 | 1 |


## Confirmatory inference (C1–C4; TSTR, linear model, OOT; one classification and regression task; Holm over the whole family)

| test | cell | comparison | n_datasets | median_z | ci_lo | ci_hi | p_two_sided | p_holm | p_equiv_holm | n_better | n_worse | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C1 methods differ | clf_up_h24_q90\|linear\|oot | Friedman, all methods | 9 |  |  |  | 0.00138 | 0.0124 | 1 |  |  | differ |
| C2 long vs assembly | clf_up_h24_q90\|linear\|oot | diffusion_ts vs assembly_median | 9 | 1.89 | -0.63 | 4.85 | 0.164 | 0.492 | 1 | 5 | 2 | inconclusive |
| C2 long vs assembly | clf_up_h24_q90\|linear\|oot | chronos vs assembly_median | 7 | 0.0768 | -4.96 | 0.953 | 1 | 1 | 1 | 2 | 2 | inconclusive |
| C3 selection | clf_up_h24_q90\|linear\|oot | optimised selection (mean) vs random | 9 | 0.0569 | -0.311 | 1.01 | 0.57 | 1 | 0.488 | 2 | 0 | inconclusive |
| C4 seam processing | clf_up_h24_q90\|linear\|oot | any joiner vs none (all paths) | 9 | -0.917 | -3.47 | -0.468 | 0.0195 | 0.137 | 1 | 0 | 4 | inconclusive |
| C1 methods differ | reg_h24\|linear\|oot | Friedman, all methods | 9 |  |  |  | 1.4e-08 | 1.4e-07 | 1 |  |  | differ |
| C2 long vs assembly | reg_h24\|linear\|oot | diffusion_ts vs assembly_median | 9 | 3.03 | 0.734 | 8.59 | 0.0547 | 0.273 | 1 | 6 | 1 | inconclusive |
| C2 long vs assembly | reg_h24\|linear\|oot | chronos vs assembly_median | 7 | 2.47 | 1.58 | 5.53 | 0.0312 | 0.188 | 1 | 5 | 0 | inconclusive |
| C3 selection | reg_h24\|linear\|oot | optimised selection (mean) vs random | 9 | 0.609 | 0.0158 | 1.41 | 0.0977 | 0.391 | 1 | 3 | 1 | inconclusive |
| C4 seam processing | reg_h24\|linear\|oot | any joiner vs none (all paths) | 9 | -0.765 | -1.32 | -0.271 | 0.00391 | 0.0312 | 1 | 0 | 2 | inconclusive |


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
| chronos | -0.303 | -0.176 | 0.122 | -0.637 | -0.0197 | -0.564 | -0.62 | -0.393 | 0.582 |
| diffusion_ts | 0.455 | 0.414 | 0.22 | 0.914 | 0.606 | 0.697 | 0.292 | 0.293 | 0.48 |
| timesfm | 0.0358 | 0.64 | -0.0911 | 0.226 | 0.196 | -2.43 | -0.00282 | 0.392 | 0.873 |
| timestral | -0.00099 | -0.0333 | 0.035 | 0.268 | -0 | -5.36 | 0.152 | -0.585 | 0.776 |
| zedge_ts_ar | 0.728 | 0.901 | 0.856 | 0.784 | 0.85 | 0.469 | 0.412 | 0.838 | 0.946 |
| zedge_ts_long | 0.75 | 0.74 | 0.294 | 0.977 | 0.573 | 0.911 | 0.876 | 0.661 | 0.829 |
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
| RQ0. Benchmark validity: noise, real-data ceiling, discriminative power and redundancy of the metrics | discriminative metrics: 231 of 297 |
| RQ1. Ranking of every method in every slice | first by ranking: holdout_clf — zedge_quilting (Friedman p = 5.31e-13); holdout_reg — zedge_quilting (Friedman p = 4.28e-09); train_clf — zedge_quilting (Friedman p = 3.64e-22); train_reg — zedge_quilting (Friedman p = 1.12e-17) |
| RQ2. Assembly from a window pool vs long-series generators | inconclusive: 2548 |
| RQ3. Within assembly: window selection × seam processing | same: 435, inconclusive: 2589 |
| RQ4. Does fidelity predict utility (which metrics, against which reference) | predictive pairs: 388 of 956 |
| RQ5. Gap to real data (TSTR / TRTR), stability over time and across models | worse than real: 120 |
| RQ6. Speed and cost: training and generation time, memory, Pareto front "quality × time" | fastest: timestral (1 s) |
| RQ7. Moderators: dataset descriptors and the effects of RQ2 / RQ3 (exploratory) | significant after BH: 0 of 176 |
| RQ8. Class balance: do methods preserve class shares (rare events especially) and what does an error cost | inconclusive: 647 |
| RQ9. Outliers and extremes: do methods preserve tails and outliers, and does it matter to the models | inconclusive: 782 |

## Research questions

### RQ0. Benchmark validity: noise, real-data ceiling, discriminative power and redundancy of the metrics

| unit | kind | group | reference | n_datasets | n_methods | p_friedman | spread_over_noise | p_friedman_bh | discriminative |
|---|---|---|---|---|---|---|---|---|---|
| F1.10_hill_err | fidelity | F1_marginal | val | 9 | 28 | 0.283 | 3.47 | 0.321 | False |
| F1.10_hill_err@oot | fidelity | F1_marginal | oot | 9 | 28 | 0.0737 | 2.74 | 0.0905 | False |
| F1.10_hill_err@train | fidelity | F1_marginal | train | 9 | 28 | 1.55e-18 | 3.5 | 1.05e-17 | True |
| F1.1_ks | fidelity | F1_marginal | val | 9 | 28 | 0.0259 | 7.79 | 0.0333 | True |
| F1.1_ks@oot | fidelity | F1_marginal | oot | 9 | 28 | 5.22e-05 | 10.8 | 8.38e-05 | True |
| F1.1_ks@train | fidelity | F1_marginal | train | 9 | 28 | 6.05e-28 | 8.38 | 4.49e-26 | True |
| F1.2_w1 | fidelity | F1_marginal | val | 9 | 28 | 0.0271 | 12.5 | 0.0347 | True |
| F1.2_w1@oot | fidelity | F1_marginal | oot | 9 | 28 | 0.000505 | 12.5 | 0.000758 | True |
| F1.2_w1@train | fidelity | F1_marginal | train | 9 | 28 | 9.74e-29 | 11.7 | 9.65e-27 | True |
| F1.3_ad | fidelity | F1_marginal | val | 9 | 28 | 0.0113 | 5.71 | 0.0151 | True |
| F1.3_ad@oot | fidelity | F1_marginal | oot | 9 | 28 | 5e-06 | 10 | 8.48e-06 | True |
| F1.3_ad@train | fidelity | F1_marginal | train | 9 | 28 | 8.62e-30 | 7.76 | 1.28e-27 | True |
| F1.4_qq_corr | fidelity | F1_marginal | val | 9 | 28 | 0.0136 | 1.49 | 0.0179 | True |
| F1.4_qq_corr@oot | fidelity | F1_marginal | oot | 9 | 28 | 8.82e-15 | 2.04 | 3.85e-14 | True |
| F1.4_qq_corr@train | fidelity | F1_marginal | train | 9 | 28 | 9.43e-17 | 3.49 | 5e-16 | True |
| F1.5_q01_err | fidelity | F1_marginal | val | 9 | 28 | 0.0749 | 8.72 | 0.0915 | False |
| F1.5_q01_err@oot | fidelity | F1_marginal | oot | 9 | 28 | 0.0173 | 10.7 | 0.0227 | True |
| F1.5_q01_err@train | fidelity | F1_marginal | train | 9 | 28 | 5.12e-12 | 8.72 | 1.63e-11 | True |
| F1.5_q99_err | fidelity | F1_marginal | val | 9 | 28 | 0.555 | 7.16 | 0.599 | False |
| F1.5_q99_err@oot | fidelity | F1_marginal | oot | 9 | 28 | 0.58 | 3.61 | 0.62 | False |
| F1.5_q99_err@train | fidelity | F1_marginal | train | 9 | 28 | 2.79e-14 | 5.67 | 1.15e-13 | True |
| F1.5_quantile_err | fidelity | F1_marginal | val | 9 | 28 | 0.0274 | 9.68 | 0.0349 | True |
| F1.5_quantile_err@oot | fidelity | F1_marginal | oot | 9 | 28 | 0.00102 | 10.3 | 0.00148 | True |
| F1.5_quantile_err@train | fidelity | F1_marginal | train | 9 | 28 | 1.43e-27 | 9.43 | 8.48e-26 | True |
| F1.6_kurt_err | fidelity | F1_marginal | val | 9 | 28 | 0.953 | 2.2 | 0.97 | False |
| F1.6_kurt_err@oot | fidelity | F1_marginal | oot | 9 | 28 | 0.175 | 2.16 | 0.201 | False |
| F1.6_kurt_err@train | fidelity | F1_marginal | train | 9 | 28 | 5.9e-20 | 2.93 | 4.74e-19 | True |
| F1.6_mean_err | fidelity | F1_marginal | val | 9 | 28 | 0.0776 | 12.5 | 0.0941 | False |
| F1.6_mean_err@oot | fidelity | F1_marginal | oot | 9 | 28 | 0.000426 | 12.5 | 0.000645 | True |
| F1.6_mean_err@train | fidelity | F1_marginal | train | 9 | 28 | 1.35e-25 | 9.92 | 4.44e-24 | True |
| F1.6_skew_err | fidelity | F1_marginal | val | 9 | 28 | 0.107 | 2.53 | 0.128 | False |
| F1.6_skew_err@oot | fidelity | F1_marginal | oot | 9 | 28 | 0.0126 | 3.38 | 0.0167 | True |
| F1.6_skew_err@train | fidelity | F1_marginal | train | 9 | 28 | 1.17e-12 | 3.46 | 4.04e-12 | True |
| F1.6_std_err | fidelity | F1_marginal | val | 9 | 28 | 0.842 | 2.89 | 0.875 | False |
| F1.6_std_err@oot | fidelity | F1_marginal | oot | 9 | 28 | 0.555 | 2.89 | 0.599 | False |
| F1.6_std_err@train | fidelity | F1_marginal | train | 9 | 28 | 3.43e-10 | 2.77 | 8.63e-10 | True |
| F1.7_out_of_range | fidelity | F1_marginal | val | 9 | 28 | 0.573 | 4.33 | 0.615 | False |
| F1.7_out_of_range@oot | fidelity | F1_marginal | oot | 9 | 28 | 5.68e-17 | 2.04 | 3.07e-16 | True |
| F1.7_out_of_range@train | fidelity | F1_marginal | train | 9 | 28 | 0.519 |  | 0.571 | False |
| F1.8_coverage | fidelity | F1_marginal | val | 9 | 28 | 2.64e-09 | 4.46 | 5.8e-09 | True |

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
| fidelity | F5_seams | 0.88 | 1 | 1 |
| fidelity | F6_windows | 0.57 | 0.71 | 0.43 |
| fidelity | F7_long_structure | 0.38 | 0.75 | 0.25 |
| fidelity | F8_target | 1 | 1 | 1 |
| fidelity | F9_coverage | 0.5 | 1 | 1 |
| utility | clf_down_h24_q10 | 1 |  | 1 |
| utility | clf_up_h168_q90 | 1 |  | 1 |
| utility | clf_up_h1_q90 | 1 |  | 1 |
| utility | clf_up_h24_q90 | 1 |  | 0.67 |
| utility | clf_up_h24_q95 | 1 |  | 0.5 |
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
| chronos | -0.303 | -0.176 | 0.122 | -0.637 | -0.0197 | -0.564 | -0.62 | -0.393 | 0.582 |
| diffusion_ts | 0.455 | 0.414 | 0.22 | 0.914 | 0.606 | 0.697 | 0.292 | 0.293 | 0.48 |
| timesfm | 0.0358 | 0.64 | -0.0911 | 0.226 | 0.196 | -2.43 | -0.00282 | 0.392 | 0.873 |
| timestral | -0.00099 | -0.0333 | 0.035 | 0.268 | -0 | -5.36 | 0.152 | -0.585 | 0.776 |
| zedge_ts_ar | 0.728 | 0.901 | 0.856 | 0.784 | 0.85 | 0.469 | 0.412 | 0.838 | 0.946 |
| zedge_ts_long | 0.75 | 0.74 | 0.294 | 0.977 | 0.573 | 0.911 | 0.876 | 0.661 | 0.829 |
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
| F1.10_hill_err | fidelity | fidelity:distribution | False | 9 | 3.77 | True | 3.13 | 3.53 | True | True | False |
| F1.10_hill_err@train | fidelity | fidelity:distribution | False | 9 | 3.77 | True | 3.13 | 3.53 | True | True | False |
| F1.1_ks | fidelity | fidelity:distribution | False | 9 | 9.28 | True | 8.37 | 13 | True | True | False |
| F1.1_ks@train | fidelity | fidelity:distribution | False | 9 | 9.98 | True | 6.94 | 9.37 | True | True | False |
| F1.2_w1 | fidelity | fidelity:distribution | True | 9 | 16.1 | True | 34.5 | 13.6 | True | True | False |
| F1.2_w1@train | fidelity | fidelity:distribution | True | 9 | 11.8 | True | 14.1 | 8.8 | True | True | False |
| F1.3_ad | fidelity | fidelity:distribution | False | 9 | 12.8 | True | 8.99 | 8.29 | True | True | False |
| F1.3_ad@train | fidelity | fidelity:distribution | False | 9 | 4.55 | True | 4.7 | 4.47 | True | True | False |
| F1.4_qq_corr | fidelity | fidelity:distribution | False | 9 | 4.06 | True | 3.25 | 3.41 | True | True | False |
| F1.4_qq_corr@train | fidelity | fidelity:distribution | False | 9 | 3.6 | True | 4.03 | 2.17 | True | True | False |
| F1.5_q01_err | fidelity | fidelity:distribution | False | 9 | 8.63 | True | 4.85 | 8.11 | True | True | False |
| F1.5_q01_err@train | fidelity | fidelity:distribution | False | 9 | 5.02 | True | 3.13 | 3.52 | True | True | False |
| F1.5_q99_err | fidelity | fidelity:distribution | False | 9 | 5.82 | True | 6.5 | 12.3 | True | True | False |
| F1.5_q99_err@train | fidelity | fidelity:distribution | False | 9 | 1.91 | True | 3.32 | 3.59 | True | True | False |
| F1.5_quantile_err | fidelity | fidelity:distribution | False | 9 | 13.6 | True | 34.9 | 13.2 | True | True | False |
| F1.5_quantile_err@train | fidelity | fidelity:distribution | False | 9 | 8.77 | True | 9.27 | 6.82 | True | True | False |
| F1.6_kurt_err | fidelity | fidelity:distribution | False | 9 | 1.68 | True | 4.94 | 2.78 | True | True | False |
| F1.6_kurt_err@train | fidelity | fidelity:distribution | False | 9 | 1.22 | True | 3.12 | 1.41 | True | True | False |
| F1.6_mean_err | fidelity | fidelity:distribution | False | 9 | 18.7 | True | 34.5 | 13.9 | True | True | False |
| F1.6_mean_err@train | fidelity | fidelity:distribution | False | 9 | 12.3 | True | 20.7 | 8.82 | True | True | False |
| F1.6_skew_err | fidelity | fidelity:distribution | False | 9 | 2.45 | True | 2.12 | 2.73 | True | True | False |
| F1.6_skew_err@train | fidelity | fidelity:distribution | False | 9 | 4.33 | True | 3.7 | 3.96 | True | True | False |
| F1.6_std_err | fidelity | fidelity:distribution | False | 9 | 4.22 | True | 5.16 | 5.09 | True | True | False |
| F1.6_std_err@train | fidelity | fidelity:distribution | False | 9 | 2.28 | True | 3.3 | 1.99 | True | True | False |
| F1.7_out_of_range | fidelity | fidelity:distribution | False | 9 | 6.73 | True | 7.2 | 4.57 | True | True | False |
| F1.7_out_of_range@train | fidelity | fidelity:distribution | False | 9 |  | False |  |  | False | False | False |
| F1.8_coverage | fidelity | fidelity:distribution | False | 9 | 3.4 | True | 1.6 | 4.5 | True | True | False |
| F1.8_coverage@train | fidelity | fidelity:distribution | False | 9 | 2.37 | True | 3 | 2.4 | True | True | False |
| F1.9_js | fidelity | fidelity:distribution | False | 9 | 7.58 | True | 8.41 | 12.9 | True | True | False |
| F1.9_js@train | fidelity | fidelity:distribution | False | 9 | 6.54 | True | 9.03 | 9.8 | True | True | False |
| F11.1_class_share_logratio | fidelity | fidelity:target | True | 9 | 10.3 | True | 6.58 | 7.18 | True | True | False |
| F11.1_class_share_logratio@train | fidelity | fidelity:target | True | 9 | 9.69 | True | 7.06 | 6.38 | True | True | False |
| F11.2_rare_share_logratio | fidelity | fidelity:target | False | 9 | 5.83 | True | 8.5 | 5.05 | True | True | False |
| F11.2_rare_share_logratio@train | fidelity | fidelity:target | False | 9 | 7.66 | True | 6.84 | 5.3 | True | True | False |
| F11.3_multiclass_tvd | fidelity | fidelity:target | False | 9 | 4.59 | True | 6.76 | 3.8 | True | True | False |
| F11.3_multiclass_tvd@train | fidelity | fidelity:target | False | 9 | 4.83 | True | 7.1 | 4.37 | True | True | False |
| F11.4_minority_lost | fidelity | fidelity:target | False | 9 |  | False |  |  | False | False | False |
| F11.4_minority_lost@train | fidelity | fidelity:target | False | 9 |  | False |  |  | False | False | False |
| F12.1_exceed_rate_err | fidelity | fidelity:distribution | False | 9 | 10.2 | True | 12.3 | 8.98 | True | True | False |
| F12.1_exceed_rate_err@train | fidelity | fidelity:distribution | False | 9 | 1.77 | True | 3.58 | 2.74 | True | True | False |


**note**: full ranking by slice — reports/LEADERBOARD.md

### RQ2. Assembly from a window pool vs long-series generators

| comparison | kind | unit | n_datasets | median_z | mean_z | ci_lo | ci_hi | p_better_adj | p_worse_adj | p_equiv_adj | n_better | n_worse | n_same | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| diffusion_ts vs vae_rand | utility | reg_h168\|linear\|S\|val\|mase | 9 | 4.86 | 5.47 | 3.21 | 7.96 | 0.0754 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| diffusion_ts vs vae_rand | utility | vol_h24\|gbdt\|S\|oot\|mase | 9 | 0.691 | 3.56 | 0.62 | 8.68 | 0.0754 | 1 | 1 | 3 | 0 | 0 | inconclusive |
| diffusion_ts vs vae_rand | utility | vol_h24\|gbdt\|S\|val\|mase | 9 | 0.81 | 1.21 | 0.559 | 1.91 | 0.0754 | 1 | 1 | 2 | 0 | 0 | inconclusive |
| timestral vs vae_rand | utility | ms_h24\|linear\|S\|val\|mase | 9 | 5.12 | 4.55 | 3.11 | 5.87 | 0.0754 | 1 | 1 | 8 | 0 | 0 | inconclusive |
| timestral vs vae_rand | utility | qreg_h24\|linear\|S\|val\|pinball | 9 | 2.87 | 3.06 | 1.57 | 4.81 | 0.0754 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| timestral vs vae_rand | utility | reg_h168\|gbdt\|S\|val\|mase | 9 | 4.19 | 4.73 | 3.14 | 6.54 | 0.0754 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| timestral vs vae_rand | utility | reg_h168\|linear\|S\|val\|mase | 9 | 4.85 | 5.67 | 3.52 | 8.17 | 0.0754 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| timestral vs vae_rand | utility | reg_h24\|gbdt\|S\|val\|mase | 9 | 4.99 | 5.33 | 2.98 | 7.61 | 0.0754 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| timestral vs vae_rand | utility | reg_h24\|linear\|S\|val\|mase | 9 | 3.62 | 4.4 | 2.89 | 6.17 | 0.0754 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| timestral vs assembly_median | utility | reg_h168\|gbdt\|S\|oot\|mase | 9 | 5.52 | 6.06 | 3.64 | 8.82 | 0.0754 | 1 | 1 | 8 | 0 | 0 | inconclusive |
| timestral vs assembly_median | utility | reg_h168\|gbdt\|S\|val\|mase | 9 | 5.43 | 5.46 | 3.8 | 7.05 | 0.0754 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| timestral vs assembly_median | utility | reg_h168\|linear\|S\|val\|mase | 9 | 4.84 | 4.77 | 3.2 | 6.36 | 0.0754 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| timestral vs assembly_median | utility | reg_h24\|linear\|S\|oot\|mase | 9 | 4.68 | 6.45 | 4.32 | 9.09 | 0.0754 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| timestral vs assembly_median | utility | reg_h24\|linear\|S\|val\|mase | 9 | 5.65 | 9.47 | 4.02 | 18.4 | 0.0754 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| zedge_ts_ar vs vae_rand | utility | clf_up_h24_q95\|gbdt\|S\|oot\|auc | 9 | 2.7 | 2.2 | 1.24 | 3.23 | 0.0754 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| zedge_ts_ar vs assembly_median | utility | clf_down_h24_q10\|gbdt\|S\|oot\|auc | 9 | 2.33 | 3.09 | 1.66 | 4.72 | 0.0754 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| zedge_ts_ar vs assembly_median | utility | clf_up_h1_q90\|gbdt\|S\|oot\|auc | 9 | 1.65 | 2.63 | 1.19 | 4.52 | 0.0754 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| zedge_ts_ar vs assembly_median | utility | clf_up_h24_q99\|gbdt\|S\|oot\|auc | 9 | 2.19 | 2.24 | 1.24 | 3.41 | 0.0754 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| zedge_ts_long vs vae_rand | utility | clf_up_h24_q95\|gbdt\|S\|oot\|auc | 9 | 1.47 | 1.5 | 0.847 | 2.27 | 0.0754 | 1 | 1 | 5 | 0 | 0 | inconclusive |
| zedge_ts_long vs assembly_median | utility | clf_down_h24_q10\|gbdt\|S\|oot\|auc | 9 | 1.51 | 1.95 | 1.33 | 2.71 | 0.0754 | 1 | 1 | 8 | 0 | 0 | inconclusive |
| diffusion_ts vs vae_rand | fidelity | F5.3_seam_z_mean | 9 | 5.3 | 5.93 | 3.7 | 8.75 | 0.0754 | 1 | 1 | 8 | 0 | 0 | inconclusive |
| diffusion_ts vs vae_rand | fidelity | F5.3_seam_z_mean@oot | 9 | 5.3 | 5.93 | 3.7 | 8.75 | 0.0754 | 1 | 1 | 8 | 0 | 0 | inconclusive |
| diffusion_ts vs vae_rand | fidelity | F5.3_seam_z_p95 | 9 | 5.55 | 6.93 | 3.81 | 11.9 | 0.0754 | 1 | 1 | 8 | 0 | 0 | inconclusive |
| diffusion_ts vs vae_rand | fidelity | F5.3_seam_z_p95@oot | 9 | 5.55 | 6.93 | 3.81 | 11.9 | 0.0754 | 1 | 1 | 8 | 0 | 0 | inconclusive |
| diffusion_ts vs vae_rand | fidelity | F5.4_seam_local_acf | 9 | 1.7 | 2.19 | 1.2 | 3.57 | 0.0754 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| diffusion_ts vs vae_rand | fidelity | F5.4_seam_local_acf@oot | 9 | 1.7 | 2.19 | 1.2 | 3.57 | 0.0754 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| diffusion_ts vs vae_rand | fidelity | F8.1_class_tvd | 9 | 4.28 | 7.15 | 2.52 | 12.4 | 0.0754 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| diffusion_ts vs vae_rand | fidelity | F8.5_cond_event_err | 9 | 2.94 | 5.12 | 2.07 | 8.54 | 0.0754 | 1 | 1 | 6 | 0 | 1 | inconclusive |
| diffusion_ts vs assembly_median | fidelity | F5.4_seam_local_acf | 9 | 0.8 | 1.01 | 0.366 | 1.9 | 0.0754 | 1 | 1 | 4 | 0 | 0 | inconclusive |
| diffusion_ts vs assembly_median | fidelity | F5.4_seam_local_acf@oot | 9 | 0.8 | 1.01 | 0.366 | 1.9 | 0.0754 | 1 | 1 | 4 | 0 | 0 | inconclusive |
| timestral vs vae_rand | fidelity | F3.8_calendar_corr_err@oot | 9 | 4.17 | 6.95 | 2.59 | 12.1 | 0.0754 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| timestral vs vae_rand | fidelity | F5.3_seam_z_mean | 9 | 7.31 | 8.12 | 5.37 | 11.2 | 0.0754 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| timestral vs vae_rand | fidelity | F5.3_seam_z_mean@oot | 9 | 7.31 | 8.12 | 5.37 | 11.2 | 0.0754 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| timestral vs vae_rand | fidelity | F5.3_seam_z_p95 | 9 | 7.95 | 9.69 | 6.42 | 14.8 | 0.0754 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| timestral vs vae_rand | fidelity | F5.3_seam_z_p95@oot | 9 | 7.95 | 9.69 | 6.42 | 14.8 | 0.0754 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| timestral vs vae_rand | fidelity | F8.4_event_by_how | 9 | 6.28 | 8.23 | 4.68 | 12 | 0.0754 | 1 | 1 | 8 | 0 | 0 | inconclusive |
| timestral vs assembly_median | fidelity | F3.8_calendar_corr_err@oot | 9 | 4.23 | 6.1 | 2.8 | 9.62 | 0.0754 | 1 | 1 | 8 | 0 | 0 | inconclusive |
| timestral vs assembly_median | fidelity | F8.4_event_by_how | 9 | 9.11 | 8.88 | 4.58 | 13.9 | 0.0754 | 1 | 1 | 8 | 0 | 0 | inconclusive |
| zedge_ts_ar vs vae_rand | fidelity | F1.4_qq_corr | 9 | 2.46 | 2.64 | 1.42 | 3.94 | 0.0754 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| zedge_ts_ar vs vae_rand | fidelity | F5.2_ks_seam_vs_inside | 9 | 2.7 | 3.12 | 1.65 | 4.64 | 0.0754 | 1 | 1 | 7 | 0 | 0 | inconclusive |

_Showing 40 rows of 2548 (rows with a better / worse / same verdict first); all of them — `hypotheses/RQ2_global.parquet`._

### RQ3. Within assembly: window selection × seam processing

| comparison | kind | unit | n_datasets | median_z | mean_z | ci_lo | ci_hi | p_better_adj | p_worse_adj | p_equiv_adj | n_better | n_worse | n_same | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| seams: vae_zseries_wsola vs vae_zseries | utility | clf_up_h24_q95\|gbdt\|S\|val\|auc | 9 | -0.414 | -0.575 | -0.849 | -0.327 | 1 | 0.0609 | 0.0298 | 0 | 1 | 1 | same |
| main effect: seams wsola vs none | utility | clf_up_h24_q95\|gbdt\|S\|val\|auc | 9 | -0.414 | -0.575 | -0.849 | -0.327 | 1 | 0.0609 | 0.0298 | 0 | 1 | 1 | same |
| selection: vae_mbb vs vae_rand | fidelity | F2.4_big_jump_share_err | 9 | -0.267 | -0.388 | -0.739 | -0.103 | 1 | 0.0609 | 0.0298 | 0 | 0 | 2 | same |
| selection: vae_mbb vs vae_rand | fidelity | F12.2_exceed_magnitude_err@oot | 8 | -0.146 | -0.173 | -0.448 | 0.0806 | 1 | 0.112 | 0.0298 | 0 | 0 | 1 | same |
| selection: vae_mbb vs vae_rand | fidelity | F4.2_how_std | 9 | 0.162 | 0.256 | -0.0347 | 0.564 | 0.136 | 1 | 0.0262 | 0 | 0 | 1 | same |
| seams: vae_zseries_quilt vs vae_zseries | fidelity | F1.6_std_err@oot | 9 | -0.228 | -0.336 | -0.697 | -0.0555 | 1 | 0.14 | 0.0298 | 0 | 0 | 3 | same |
| seams: vae_zseries_xfade vs vae_zseries | fidelity | F1.1_ks@oot | 9 | -0.185 | -0.217 | -0.471 | 0.00986 | 1 | 0.14 | 0.0262 | 0 | 0 | 5 | same |
| main effect: seams crossfade vs none | fidelity | F1.1_ks@oot | 9 | -0.185 | -0.217 | -0.471 | 0.00986 | 1 | 0.14 | 0.0262 | 0 | 0 | 5 | same |
| main effect: seams quilt vs none | fidelity | F1.6_std_err@oot | 9 | -0.228 | -0.336 | -0.697 | -0.0555 | 1 | 0.14 | 0.0298 | 0 | 0 | 3 | same |
| selection: vae_mbb vs vae_rand | fidelity | F3.6_peak168_err@oot | 9 | -0.14 | -0.206 | -0.566 | 0.145 | 1 | 0.167 | 0.0262 | 0 | 0 | 0 | same |
| seams: vae_zseries_quilt vs vae_zseries | fidelity | F2.1_ks_d1 | 9 | -0.293 | -0.335 | -0.658 | -0.0203 | 1 | 0.167 | 0.0262 | 0 | 0 | 4 | same |
| seams: vae_zseries_xfade vs vae_zseries | fidelity | F1.1_ks | 9 | -0.169 | -0.201 | -0.524 | 0.0655 | 1 | 0.167 | 0.0262 | 0 | 0 | 4 | same |
| main effect: seams crossfade vs none | fidelity | F1.1_ks | 9 | -0.169 | -0.201 | -0.524 | 0.0655 | 1 | 0.167 | 0.0262 | 0 | 0 | 4 | same |
| main effect: seams quilt vs none | fidelity | F2.1_ks_d1 | 9 | -0.293 | -0.335 | -0.658 | -0.0203 | 1 | 0.167 | 0.0262 | 0 | 0 | 4 | same |
| selection: vae_mbb vs vae_rand | fidelity | F3.4_acf_sq_d | 9 | 0.407 | 0.39 | -0.0406 | 0.87 | 0.17 | 1 | 0.0298 | 0 | 0 | 0 | same |
| seams: vae_zseries_quilt vs vae_zseries | utility | clf_up_h6_q90\|gbdt\|S\|oot\|auc | 9 | -0.102 | -0.184 | -0.493 | 0.0355 | 1 | 0.19 | 0.0262 | 0 | 0 | 7 | same |
| seams: vae_zseries_xfade vs vae_zseries | utility | clf_up_h6_q90\|gbdt\|S\|oot\|auc | 9 | -0.222 | -0.219 | -0.497 | 0.0286 | 1 | 0.19 | 0.0262 | 0 | 0 | 5 | same |
| main effect: seams crossfade vs none | utility | clf_up_h6_q90\|gbdt\|S\|oot\|auc | 9 | -0.222 | -0.219 | -0.497 | 0.0286 | 1 | 0.19 | 0.0262 | 0 | 0 | 5 | same |
| main effect: seams quilt vs none | utility | clf_up_h6_q90\|gbdt\|S\|oot\|auc | 9 | -0.102 | -0.184 | -0.493 | 0.0355 | 1 | 0.19 | 0.0262 | 0 | 0 | 7 | same |
| seams: vae_zseries_quilt vs vae_zseries | fidelity | F1.9_js@oot | 9 | -0.319 | -0.28 | -0.554 | 9.43e-05 | 1 | 0.19 | 0.0262 | 0 | 0 | 3 | same |
| seams: vae_zseries_quilt vs vae_zseries | fidelity | F4.2_how_std@oot | 9 | -0.215 | -0.179 | -0.466 | 0.121 | 1 | 0.19 | 0.0262 | 0 | 0 | 4 | same |
| seams: vae_zseries_xfade vs vae_zseries | fidelity | F1.9_js | 9 | -0.274 | -0.236 | -0.525 | 0.0521 | 1 | 0.19 | 0.0262 | 0 | 0 | 1 | same |
| seams: vae_zseries_xfade vs vae_zseries | fidelity | F7.5_drawdown_ks@oot | 9 | -0.203 | -0.237 | -0.471 | -0.0108 | 1 | 0.19 | 0.0262 | 0 | 0 | 4 | same |
| main effect: seams crossfade vs none | fidelity | F1.9_js | 9 | -0.274 | -0.236 | -0.525 | 0.0521 | 1 | 0.19 | 0.0262 | 0 | 0 | 1 | same |
| main effect: seams crossfade vs none | fidelity | F7.5_drawdown_ks@oot | 9 | -0.203 | -0.237 | -0.471 | -0.0108 | 1 | 0.19 | 0.0262 | 0 | 0 | 4 | same |
| main effect: seams quilt vs none | fidelity | F1.9_js@oot | 9 | -0.319 | -0.28 | -0.554 | 9.43e-05 | 1 | 0.19 | 0.0262 | 0 | 0 | 3 | same |
| main effect: seams quilt vs none | fidelity | F4.2_how_std@oot | 9 | -0.215 | -0.179 | -0.466 | 0.121 | 1 | 0.19 | 0.0262 | 0 | 0 | 4 | same |
| seams: vae_zseries_quilt vs vae_zseries | utility | vol_h24\|gbdt\|S\|val\|mase | 9 | -0.169 | -0.202 | -0.517 | 0.0182 | 1 | 0.228 | 0.0262 | 0 | 0 | 5 | same |
| main effect: seams quilt vs none | utility | vol_h24\|gbdt\|S\|val\|mase | 9 | -0.169 | -0.202 | -0.517 | 0.0182 | 1 | 0.228 | 0.0262 | 0 | 0 | 5 | same |
| seams: vae_zseries_quilt vs vae_zseries | fidelity | F1.1_ks@oot | 9 | -0.187 | -0.131 | -0.352 | 0.0778 | 1 | 0.228 | 0.0262 | 0 | 0 | 5 | same |
| seams: vae_zseries_quilt vs vae_zseries | fidelity | F4.3_hod_mean@oot | 9 | -0.214 | -0.34 | -0.793 | 0.088 | 1 | 0.228 | 0.0298 | 0 | 0 | 4 | same |
| seams: vae_zseries_quilt vs vae_zseries | fidelity | F7.5_drawdown_ks@oot | 9 | -0.154 | -0.138 | -0.313 | 0.0422 | 1 | 0.228 | 0.0262 | 0 | 0 | 6 | same |
| seams: vae_zseries_xfade vs vae_zseries | fidelity | F2.1_ks_d1 | 9 | -0.208 | -0.269 | -0.585 | 0.0297 | 1 | 0.228 | 0.0262 | 0 | 0 | 4 | same |
| main effect: seams crossfade vs none | fidelity | F2.1_ks_d1 | 9 | -0.208 | -0.269 | -0.585 | 0.0297 | 1 | 0.228 | 0.0262 | 0 | 0 | 4 | same |
| main effect: seams quilt vs none | fidelity | F1.1_ks@oot | 9 | -0.187 | -0.131 | -0.352 | 0.0778 | 1 | 0.228 | 0.0262 | 0 | 0 | 5 | same |
| main effect: seams quilt vs none | fidelity | F4.3_hod_mean@oot | 9 | -0.214 | -0.34 | -0.793 | 0.088 | 1 | 0.228 | 0.0298 | 0 | 0 | 4 | same |
| main effect: seams quilt vs none | fidelity | F7.5_drawdown_ks@oot | 9 | -0.154 | -0.138 | -0.313 | 0.0422 | 1 | 0.228 | 0.0262 | 0 | 0 | 6 | same |
| seams: vae_zseries_xfade vs vae_zseries | utility | clf_up_h1_q90\|gbdt\|S\|oot\|auc | 9 | 0.183 | 0.352 | 0.0318 | 0.731 | 0.242 | 1 | 0.0298 | 0 | 0 | 1 | same |
| main effect: seams crossfade vs none | utility | clf_up_h1_q90\|gbdt\|S\|oot\|auc | 9 | 0.183 | 0.352 | 0.0318 | 0.731 | 0.242 | 1 | 0.0298 | 0 | 0 | 1 | same |
| selection: vae_knn vs vae_rand | fidelity | F1.10_hill_err | 9 | 0.26 | 0.301 | -0.0596 | 0.664 | 0.242 | 1 | 0.0262 | 0 | 0 | 1 | same |

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

### RQ7. Moderators: dataset descriptors and the effects of RQ2 / RQ3 (exploratory)

| effect | descriptor | spearman | p | n | p_bh |
|---|---|---|---|---|---|
| RQ2:fidelity:chronos vs assembly_median | acf24 | -0.143 | 0.76 | 7 | 0.926 |
| RQ2:fidelity:chronos vs assembly_median | acf168 | 0.714 | 0.0713 | 7 | 0.397 |
| RQ2:fidelity:chronos vs assembly_median | kurt_d24 | 0.929 | 0.00252 | 7 | 0.132 |
| RQ2:fidelity:chronos vs assembly_median | volclust | -0.286 | 0.535 | 7 | 0.833 |
| RQ2:fidelity:chronos vs assembly_median | trend | 0.107 | 0.819 | 7 | 0.926 |
| RQ2:fidelity:chronos vs assembly_median | nan_share | -0.204 | 0.661 | 7 | 0.895 |
| RQ2:utility:chronos vs assembly_median | acf24 | 0.179 | 0.702 | 7 | 0.895 |
| RQ2:utility:chronos vs assembly_median | acf168 | 0.75 | 0.0522 | 7 | 0.367 |
| RQ2:utility:chronos vs assembly_median | kurt_d24 | 0.679 | 0.0938 | 7 | 0.397 |
| RQ2:utility:chronos vs assembly_median | volclust | 0.464 | 0.294 | 7 | 0.69 |
| RQ2:utility:chronos vs assembly_median | trend | 0.107 | 0.819 | 7 | 0.926 |
| RQ2:utility:chronos vs assembly_median | nan_share | -0.612 | 0.144 | 7 | 0.506 |
| RQ2:fidelity:chronos vs vae_rand | acf24 | -0.357 | 0.432 | 7 | 0.785 |
| RQ2:fidelity:chronos vs vae_rand | acf168 | 0.536 | 0.215 | 7 | 0.596 |
| RQ2:fidelity:chronos vs vae_rand | kurt_d24 | 0.786 | 0.0362 | 7 | 0.34 |
| RQ2:fidelity:chronos vs vae_rand | volclust | -0.179 | 0.702 | 7 | 0.895 |
| RQ2:fidelity:chronos vs vae_rand | trend | -0.107 | 0.819 | 7 | 0.926 |
| RQ2:fidelity:chronos vs vae_rand | nan_share | 0 | 1 | 7 | 1 |
| RQ2:utility:chronos vs vae_rand | acf24 | 0.179 | 0.702 | 7 | 0.895 |
| RQ2:utility:chronos vs vae_rand | acf168 | 0.75 | 0.0522 | 7 | 0.367 |
| RQ2:utility:chronos vs vae_rand | kurt_d24 | 0.679 | 0.0938 | 7 | 0.397 |
| RQ2:utility:chronos vs vae_rand | volclust | 0.464 | 0.294 | 7 | 0.69 |
| RQ2:utility:chronos vs vae_rand | trend | 0.107 | 0.819 | 7 | 0.926 |
| RQ2:utility:chronos vs vae_rand | nan_share | -0.612 | 0.144 | 7 | 0.506 |
| RQ2:fidelity:diffusion_ts vs assembly_median | acf24 | -0.583 | 0.0992 | 9 | 0.397 |
| RQ2:fidelity:diffusion_ts vs assembly_median | acf168 | -0.2 | 0.606 | 9 | 0.895 |
| RQ2:fidelity:diffusion_ts vs assembly_median | kurt_d24 | 0.4 | 0.286 | 9 | 0.69 |
| RQ2:fidelity:diffusion_ts vs assembly_median | volclust | -0.183 | 0.637 | 9 | 0.895 |
| RQ2:fidelity:diffusion_ts vs assembly_median | trend | -0.85 | 0.0037 | 9 | 0.132 |
| RQ2:fidelity:diffusion_ts vs assembly_median | nan_share | 0.639 | 0.0639 | 9 | 0.397 |
| RQ2:utility:diffusion_ts vs assembly_median | acf24 | -0.4 | 0.286 | 9 | 0.69 |
| RQ2:utility:diffusion_ts vs assembly_median | acf168 | 0.05 | 0.898 | 9 | 0.977 |
| RQ2:utility:diffusion_ts vs assembly_median | kurt_d24 | 0.533 | 0.139 | 9 | 0.506 |
| RQ2:utility:diffusion_ts vs assembly_median | volclust | -0.15 | 0.7 | 9 | 0.895 |
| RQ2:utility:diffusion_ts vs assembly_median | trend | -0.75 | 0.0199 | 9 | 0.292 |
| RQ2:utility:diffusion_ts vs assembly_median | nan_share | 0.456 | 0.217 | 9 | 0.596 |
| RQ2:fidelity:diffusion_ts vs vae_rand | acf24 | -0.6 | 0.0876 | 9 | 0.397 |
| RQ2:fidelity:diffusion_ts vs vae_rand | acf168 | -0.283 | 0.46 | 9 | 0.801 |
| RQ2:fidelity:diffusion_ts vs vae_rand | kurt_d24 | 0.283 | 0.46 | 9 | 0.801 |
| RQ2:fidelity:diffusion_ts vs vae_rand | volclust | -0.167 | 0.668 | 9 | 0.895 |

_Showing 40 rows of 176; all of them — `hypotheses/RQ7_global.parquet`._

### RQ8. Class balance: do methods preserve class shares (rare events especially) and what does an error cost

| comparison | kind | unit | n_datasets | median_z | mean_z | ci_lo | ci_hi | p_better_adj | p_worse_adj | p_equiv_adj | n_better | n_worse | n_same | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| vae_atsp vs vae_rand | fidelity | F11.1_class_share_logratio | 9 | 2.49 | 2.43 | 1.2 | 3.76 | 0.117 | 1 | 1 | 5 | 0 | 0 | inconclusive |
| vae_atsp vs vae_rand | fidelity | F11.1_class_share_logratio@oot | 9 | 1.32 | 2.27 | 0.953 | 3.65 | 0.117 | 1 | 1 | 4 | 0 | 0 | inconclusive |
| vae_greedy vs vae_rand | fidelity | F11.1_class_share_logratio | 9 | 1.64 | 1.99 | 0.881 | 3.22 | 0.117 | 1 | 1 | 5 | 0 | 0 | inconclusive |
| vae_greedy vs vae_rand | fidelity | F11.1_class_share_logratio@oot | 9 | 1.71 | 1.97 | 0.891 | 3.22 | 0.117 | 1 | 1 | 5 | 0 | 0 | inconclusive |
| vae_herding vs vae_rand | fidelity | F11.1_class_share_logratio@oot | 9 | 1.94 | 3.63 | 1.2 | 5.98 | 0.117 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| vae_knn vs vae_rand | fidelity | F11.1_class_share_logratio | 9 | 0.793 | 1.16 | 0.439 | 1.98 | 0.117 | 1 | 0.974 | 3 | 0 | 0 | inconclusive |
| vae_knn vs vae_rand | fidelity | F11.1_class_share_logratio@oot | 9 | 1.01 | 1.26 | 0.505 | 2.16 | 0.117 | 1 | 1 | 3 | 0 | 0 | inconclusive |
| vae_pctsp vs vae_rand | fidelity | F11.1_class_share_logratio | 9 | 2.45 | 2.59 | 1.48 | 3.76 | 0.117 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| vae_pctsp vs vae_rand | fidelity | F11.1_class_share_logratio@oot | 9 | 1.7 | 2.55 | 1.33 | 3.78 | 0.117 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| vae_zseries vs vae_rand | fidelity | F11.1_class_share_logratio | 9 | 3.52 | 4.77 | 2.75 | 6.97 | 0.117 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| vae_zseries vs vae_rand | fidelity | F11.1_class_share_logratio@oot | 9 | 3.15 | 4.75 | 2.69 | 7.05 | 0.117 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| vae_zseries vs vae_rand | fidelity | F11.2_rare_share_logratio | 9 | 5.42 | 5.82 | 2.41 | 9.73 | 0.117 | 1 | 1 | 6 | 1 | 0 | inconclusive |
| vae_zseries vs vae_rand | fidelity | F11.2_rare_share_logratio@oot | 9 | 6.73 | 6.33 | 3.04 | 9.65 | 0.117 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| vae_zseries vs vae_rand | fidelity | F11.3_multiclass_tvd | 9 | 2.66 | 3.19 | 1.4 | 5.08 | 0.117 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| vae_zseries vs vae_rand | fidelity | F11.3_multiclass_tvd@oot | 9 | 2.65 | 3.1 | 1.32 | 5 | 0.117 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| vae_zseries vs vae_rand | fidelity | F8.1_class_tvd | 9 | 4.34 | 4.22 | 1.89 | 6.95 | 0.117 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| vae_zseries vs vae_rand | fidelity | F8.1_class_tvd@oot | 9 | 4.34 | 4.15 | 1.82 | 6.88 | 0.117 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| vae_zseries_wsola vs vae_rand | fidelity | F11.1_class_share_logratio | 9 | 2.75 | 3.91 | 1.84 | 6.5 | 0.117 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| vae_zseries_wsola vs vae_rand | fidelity | F11.1_class_share_logratio@oot | 9 | 3.13 | 4.14 | 2 | 6.74 | 0.117 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| vae_zseries_wsola vs vae_rand | fidelity | F11.2_rare_share_logratio@oot | 9 | 6.28 | 6.99 | 2.65 | 12.1 | 0.117 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| vae_greedy vs vae_rand | utility | clf_up_h168_q90\|gbdt\|S\|oot\|ece | 9 | 1.95 | 2.65 | 0.725 | 5.35 | 0.117 | 1 | 1 | 5 | 0 | 0 | inconclusive |
| vae_herding vs vae_rand | utility | clf_up_h6_q90\|gbdt\|S\|oot\|ece | 9 | 1.11 | 1.45 | 0.762 | 2.25 | 0.117 | 1 | 1 | 4 | 0 | 0 | inconclusive |
| vae_knn vs vae_rand | utility | clf_up_h168_q90\|gbdt\|S\|oot\|ece | 9 | 1.46 | 2.09 | 0.586 | 4.25 | 0.117 | 1 | 1 | 5 | 0 | 0 | inconclusive |
| vae_pctsp vs vae_rand | utility | clf_up_h168_q90\|gbdt\|S\|oot\|ece | 9 | 1.92 | 2.54 | 0.766 | 4.94 | 0.117 | 1 | 1 | 5 | 0 | 0 | inconclusive |
| vae_quilting vs vae_rand | utility | clf_up_h168_q90\|gbdt\|S\|oot\|ece | 9 | 1.09 | 2.79 | 0.684 | 5.59 | 0.117 | 1 | 1 | 4 | 0 | 0 | inconclusive |
| vae_quilting vs vae_rand | utility | clf_up_h168_q90\|gbdt\|S\|val\|ece | 9 | 0.867 | 2.04 | 0.727 | 3.68 | 0.117 | 1 | 1 | 3 | 0 | 0 | inconclusive |
| vae_quilting vs vae_rand | utility | clf_up_h168_q90\|linear\|S\|oot\|ece | 9 | 1.94 | 2.12 | 0.842 | 3.51 | 0.117 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| vae_quilting vs vae_rand | utility | clf_up_h168_q90\|linear\|S\|val\|ece | 9 | 1.45 | 2.45 | 0.687 | 5 | 0.117 | 1 | 1 | 4 | 0 | 0 | inconclusive |
| vae_quilting vs vae_rand | utility | clf_up_h24_q90\|mlp\|S\|oot\|ece | 9 | 1.19 | 1.39 | 0.555 | 2.24 | 0.117 | 1 | 1 | 3 | 0 | 0 | inconclusive |
| vae_quilting vs vae_rand | utility | clf_up_h6_q90\|gbdt\|S\|val\|ece | 9 | 0.836 | 1.13 | 0.224 | 2.28 | 0.117 | 1 | 0.844 | 2 | 0 | 0 | inconclusive |
| vae_zseries vs vae_rand | utility | clf_up_h24_q90\|gbdt\|S\|oot\|ece | 9 | 0.745 | 1.66 | 0.357 | 3.56 | 0.117 | 1 | 0.953 | 3 | 0 | 0 | inconclusive |
| vae_zseries vs vae_rand | utility | clf_up_h24_q90\|linear\|S\|oot\|ece | 9 | 1.65 | 2.18 | 0.838 | 3.58 | 0.117 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| vae_zseries vs vae_rand | utility | clf_up_h24_q95\|gbdt\|S\|oot\|ece | 9 | 1.13 | 1.15 | 0.49 | 1.81 | 0.117 | 1 | 1 | 4 | 0 | 0 | inconclusive |
| vae_zseries vs vae_rand | utility | clf_up_h24_q95\|linear\|S\|oot\|ece | 9 | 2.73 | 2.27 | 1.11 | 3.51 | 0.117 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| vae_zseries vs vae_rand | utility | clf_up_h24_q99\|linear\|S\|oot\|ece | 9 | 2.93 | 2.68 | 1.4 | 4.01 | 0.117 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| vae_zseries vs vae_rand | utility | clf_up_h6_q90\|gbdt\|S\|val\|ece | 9 | 1.64 | 1.41 | 0.332 | 2.5 | 0.117 | 1 | 1 | 5 | 0 | 0 | inconclusive |
| zedge_ts_ar vs assembly_median | utility | clf_down_h24_q10\|gbdt\|S\|oot\|ece | 9 | 1.33 | 3.57 | 1.39 | 6.73 | 0.117 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| zedge_ts_ar vs assembly_median | utility | clf_down_h24_q10\|linear\|S\|oot\|ece | 9 | 4.99 | 5.12 | 2.87 | 7.64 | 0.117 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| zedge_ts_ar vs assembly_median | utility | clf_down_h24_q10\|linear\|S\|val\|ece | 9 | 3.24 | 3.51 | 2.14 | 5.09 | 0.117 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| zedge_ts_ar vs assembly_median | utility | clf_up_h168_q90\|gbdt\|S\|oot\|ece | 9 | 4.21 | 3.96 | 1.74 | 6.42 | 0.117 | 1 | 1 | 6 | 0 | 0 | inconclusive |

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
| fidelity | zedge_ts_ar vs assembly_median | 8 |
| fidelity | zedge_ts_long vs assembly_median | 8 |
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
| utility | zedge_ts_ar vs assembly_median | 30 |
| utility | zedge_ts_long vs assembly_median | 30 |


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
| vae_atsp vs vae_rand | fidelity | F1.5_q99_err | 9 | 0.884 | 1.63 | 0.518 | 3.48 | 0.0402 | 1 | 0.929 | 4 | 0 | 0 | inconclusive |
| vae_atsp vs vae_rand | utility | reg_h168\|gbdt\|S\|val\|mae_extreme | 9 | 1.59 | 1.98 | 1.21 | 2.99 | 0.0402 | 1 | 1 | 5 | 0 | 0 | inconclusive |
| vae_atsp vs vae_rand | utility | reg_h168\|linear\|S\|oot\|mae_extreme | 9 | 4.14 | 4.75 | 2.57 | 7.55 | 0.0402 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| vae_atsp vs vae_rand | utility | reg_h168\|linear\|S\|val\|mae_extreme | 9 | 3.42 | 4.96 | 2.61 | 7.85 | 0.0402 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| vae_greedy vs vae_rand | utility | reg_h168\|gbdt\|S\|val\|mae_extreme | 9 | 1.13 | 2.05 | 1.01 | 3.46 | 0.0402 | 1 | 1 | 4 | 0 | 0 | inconclusive |
| vae_greedy vs vae_rand | utility | reg_h168\|linear\|S\|oot\|mae_extreme | 9 | 3.91 | 5.61 | 2.83 | 9.32 | 0.0402 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| vae_greedy vs vae_rand | utility | reg_h168\|linear\|S\|val\|mae_extreme | 9 | 3.2 | 5.46 | 2.52 | 9.39 | 0.0402 | 1 | 1 | 8 | 0 | 0 | inconclusive |
| vae_herding vs vae_rand | utility | reg_h1\|gbdt\|S\|oot\|mae_extreme | 9 | 1.57 | 1.71 | 1.01 | 2.55 | 0.0402 | 1 | 1 | 5 | 0 | 0 | inconclusive |
| vae_knn vs vae_rand | utility | reg_h168\|gbdt\|S\|val\|mae_extreme | 9 | 0.869 | 1.5 | 0.757 | 2.42 | 0.0402 | 1 | 1 | 3 | 0 | 0 | inconclusive |
| vae_knn vs vae_rand | utility | reg_h168\|linear\|S\|val\|mae_extreme | 9 | 2.59 | 4.11 | 2.08 | 6.66 | 0.0402 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| vae_pctsp vs vae_rand | utility | reg_h168\|gbdt\|S\|val\|mae_extreme | 9 | 1.36 | 1.94 | 0.99 | 3.11 | 0.0402 | 1 | 1 | 4 | 0 | 0 | inconclusive |
| vae_pctsp vs vae_rand | utility | reg_h168\|linear\|S\|oot\|mae_extreme | 9 | 4.08 | 4.89 | 2.37 | 8.04 | 0.0402 | 1 | 1 | 5 | 0 | 0 | inconclusive |
| vae_pctsp vs vae_rand | utility | reg_h168\|linear\|S\|val\|mae_extreme | 9 | 3.39 | 5.19 | 2.42 | 8.7 | 0.0402 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| vae_quilting vs vae_rand | utility | reg_h168\|linear\|S\|oot\|mae_extreme | 9 | 2.57 | 4.44 | 1.89 | 7.74 | 0.0402 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| vae_quilting vs vae_rand | utility | reg_h168\|linear\|S\|val\|mae_extreme | 9 | 2.47 | 4.19 | 1.71 | 7.52 | 0.0402 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| vae_quilting vs vae_rand | utility | reg_h24\|linear\|S\|val\|mae_extreme | 9 | 1.56 | 1.84 | 0.998 | 2.71 | 0.0402 | 1 | 1 | 4 | 0 | 0 | inconclusive |
| vae_zseries vs vae_rand | utility | reg_h168\|gbdt\|S\|val\|mae_extreme | 9 | 1.78 | 1.87 | 1.11 | 2.8 | 0.0402 | 1 | 1 | 5 | 0 | 0 | inconclusive |
| vae_zseries vs vae_rand | utility | reg_h168\|linear\|S\|oot\|mae_extreme | 9 | 4.26 | 4.54 | 2.37 | 7.4 | 0.0402 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| vae_zseries vs vae_rand | utility | reg_h168\|linear\|S\|val\|mae_extreme | 9 | 2.93 | 4.58 | 2.15 | 7.72 | 0.0402 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| vae_zseries vs vae_rand | utility | reg_h24\|gbdt\|S\|val\|mae_extreme | 9 | 2.28 | 1.96 | 1.11 | 2.91 | 0.0402 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| vae_zseries vs vae_rand | utility | reg_h24\|linear\|S\|oot\|mae_extreme | 9 | 2.44 | 2.69 | 1.56 | 4.14 | 0.0402 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| vae_zseries_wsola vs vae_rand | utility | reg_h168\|gbdt\|S\|val\|mae_extreme | 9 | 1.57 | 1.45 | 0.832 | 2.09 | 0.0402 | 1 | 1 | 3 | 0 | 0 | inconclusive |
| vae_zseries_wsola vs vae_rand | utility | reg_h168\|linear\|S\|val\|mae_extreme | 9 | 1.87 | 2.55 | 1.03 | 4.4 | 0.0402 | 1 | 1 | 3 | 0 | 0 | inconclusive |
| vae_zseries_wsola vs vae_rand | utility | reg_h24\|gbdt\|S\|oot\|mae_extreme | 9 | 1.19 | 1.68 | 0.646 | 2.94 | 0.0402 | 1 | 1 | 5 | 0 | 0 | inconclusive |
| vae_zseries_wsola vs vae_rand | utility | reg_h24\|linear\|S\|oot\|mae_extreme | 9 | 1.97 | 3 | 1.42 | 4.96 | 0.0402 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| vae_zseries_wsola vs vae_rand | utility | reg_h24\|linear\|S\|val\|mae_extreme | 9 | 2.06 | 2.69 | 1.69 | 3.86 | 0.0402 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| timestral vs assembly_median | utility | reg_h168\|gbdt\|S\|oot\|mae_extreme | 9 | 3.92 | 5.96 | 3.22 | 9.22 | 0.0402 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| timestral vs assembly_median | utility | reg_h168\|gbdt\|S\|val\|mae_extreme | 9 | 5 | 5.79 | 3.87 | 7.93 | 0.0402 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| timestral vs assembly_median | utility | reg_h24\|linear\|S\|oot\|mae_extreme | 9 | 10.7 | 12.1 | 8.02 | 17.1 | 0.0402 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| timestral vs assembly_median | utility | reg_h24\|linear\|S\|val\|mae_extreme | 9 | 12.9 | 11.9 | 7.51 | 16.7 | 0.0402 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| zedge_ts_ar vs assembly_median | utility | clf_up_h24_q95\|gbdt\|S\|oot\|pr_auc | 9 | 3.05 | 3.39 | 2.27 | 4.87 | 0.0402 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| zedge_ts_ar vs assembly_median | utility | clf_up_h24_q95\|gbdt\|S\|val\|pr_auc | 9 | 1.62 | 1.9 | 0.759 | 3.33 | 0.0402 | 1 | 1 | 5 | 0 | 0 | inconclusive |
| zedge_ts_ar vs assembly_median | utility | clf_up_h24_q95\|linear\|S\|oot\|pr_auc | 9 | 1.61 | 6.04 | 2.11 | 10.9 | 0.0402 | 1 | 1 | 5 | 0 | 0 | inconclusive |
| zedge_ts_ar vs assembly_median | utility | clf_up_h24_q99\|gbdt\|S\|oot\|pr_auc | 9 | 2.65 | 3 | 2.03 | 4.07 | 0.0402 | 1 | 1 | 5 | 0 | 0 | inconclusive |
| zedge_ts_ar vs assembly_median | utility | reg_h1\|gbdt\|S\|val\|mae_extreme | 9 | 4.57 | 6.86 | 2.38 | 12.8 | 0.0402 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| zedge_ts_long vs assembly_median | utility | clf_up_h24_q95\|gbdt\|S\|oot\|pr_auc | 9 | 1.06 | 1.57 | 0.923 | 2.3 | 0.0402 | 1 | 1 | 4 | 0 | 0 | inconclusive |
| zedge_ts_long vs assembly_median | utility | clf_up_h24_q99\|gbdt\|S\|oot\|pr_auc | 9 | 1.12 | 2.17 | 0.883 | 4.54 | 0.0402 | 1 | 1 | 3 | 0 | 0 | inconclusive |
| zedge_ts_long vs assembly_median | utility | reg_h168\|linear\|S\|oot\|mae_extreme | 9 | 2.81 | 3.26 | 1.76 | 5.01 | 0.0402 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| vae_atsp vs vae_rand | utility | reg_h168\|gbdt\|S\|oot\|mae_extreme | 9 | 1.54 | 2.07 | 0.991 | 3.27 | 0.0555 | 1 | 1 | 5 | 0 | 0 | inconclusive |
| vae_greedy vs vae_rand | utility | reg_h168\|gbdt\|S\|oot\|mae_extreme | 9 | 1.62 | 2.36 | 1.06 | 3.83 | 0.0555 | 1 | 1 | 5 | 0 | 0 | inconclusive |

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
| fidelity | zedge_ts_ar vs assembly_median | 22 |
| fidelity | zedge_ts_long vs assembly_median | 22 |
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
| utility | zedge_ts_ar vs assembly_median | 24 |
| utility | zedge_ts_long vs assembly_median | 24 |


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


## Case study: method `vae_zseries` (secondary, BH within a hypothesis)

Method `vae_zseries` vs the controls on its own pool, alternative stitchers and long-series generators. Sign of the effect: > 0 — the method is better than the comparator. Pre-specified cell (TSTR, task clf_up_h24_q90, linear model, OOT; Holm over CS7 and CS10):

| hypothesis | comparator | n_datasets | median_z | ci_lo | ci_hi | p_better_holm | p_worse_holm | p_equiv_holm | n_better | n_worse | n_same | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CS7 | vae_rand | 9 | 1.14 | -0.588 | 2.08 | 0.639 | 1 | 1 | 2 | 0 | 0 | inconclusive |
| CS10 | diffusion_ts | 9 | -0.923 | -3.69 | 0.961 | 0.936 | 0.246 | 1 | 1 | 3 | 0 | inconclusive |
| CS10 | chronos | 7 | -0.354 | -1.16 | 4.06 | 0.812 | 1 | 1 | 1 | 0 | 0 | inconclusive |


| Hypothesis | Verdicts |
|---|---|
| CS1. Distribution and dependence against train | better: 9, inconclusive: 23 |
| CS2. Distribution and dependence against val | inconclusive: 33 |
| CS3. Seam artefacts | better: 4, inconclusive: 4 |
| CS4. Structure longer than a window | inconclusive: 10 |
| CS5. Target structure | better: 4, inconclusive: 2 |
| CS6. Realism of single windows and memorisation | inconclusive: 11 |
| CS7. TSTR of the method vs the random path (case-study task) | inconclusive: 6 |
| CS8. The same on the other tasks | inconclusive: 52 |
| CS9. Fidelity vs other stitchers of the same pool and the long-series generators | inconclusive: 1027 |
| CS10. TSTR vs other stitchers of the same pool and the long-series generators | inconclusive: 754 |
| CS11. The method's effect on TSTR across model classes |  |
| CS12. The method's effect on TSTR over time (val vs OOT) and across subgroups |  |
| CS13. TSTR of the method vs TRTR | worse: 47, inconclusive: 11 |
| CS14. Computational cost of the method vs the others |  |
| CS15. Moderators of the method's effect (exploratory) | significant after BH: 0 of 95 |

### CS1. Distribution and dependence against train

| unit | comparator | n_datasets | median_z | mean_z | ci_lo | ci_hi | p_better_adj | p_worse_adj | p_equiv_adj | n_better | n_worse | n_same | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F1.1_ks@train | vae_rand | 9 | 2.61 | 3.01 | 2.17 | 4.06 | 0.0139 | 1 | 1 | 8 | 0 | 0 | better |
| F1.2_w1@train | vae_rand | 9 | 3.53 | 3.41 | 1.76 | 4.76 | 0.0139 | 1 | 1 | 8 | 1 | 0 | better |
| F1.3_ad@train | vae_rand | 9 | 3.88 | 3.72 | 2.61 | 4.8 | 0.0139 | 1 | 1 | 8 | 0 | 0 | better |
| F1.5_q99_err@train | vae_rand | 9 | 1.11 | 1.97 | 0.785 | 3.58 | 0.0139 | 1 | 1 | 4 | 0 | 0 | better |
| F1.5_quantile_err@train | vae_rand | 9 | 2.3 | 3.26 | 1.53 | 5.04 | 0.0139 | 1 | 1 | 8 | 0 | 0 | better |
| F1.9_js@train | vae_rand | 9 | 3.21 | 3.3 | 1.98 | 4.58 | 0.0139 | 1 | 1 | 8 | 0 | 0 | better |
| F2.2_vol_ratio_err_d24@train | vae_rand | 9 | 2.85 | 4.49 | 1.68 | 8.01 | 0.0139 | 1 | 1 | 6 | 0 | 0 | better |
| F3.1_acf_in_window@train | vae_rand | 9 | 3.54 | 4.45 | 3.07 | 6 | 0.0139 | 1 | 1 | 9 | 0 | 0 | better |
| F3.6_peak24_err@train | vae_rand | 9 | 5.51 | 7.75 | 3.42 | 13 | 0.0139 | 1 | 1 | 6 | 0 | 0 | better |
| F1.6_mean_err@train | vae_rand | 9 | 3.61 | 3.53 | 1.42 | 5.27 | 0.0312 | 1 | 1 | 8 | 1 | 0 | inconclusive |
| F2.1_w1_d24@train | vae_rand | 9 | 2.27 | 3.24 | 1.28 | 5.46 | 0.0398 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| F2.1_ks_d168@train | vae_rand | 9 | 3.87 | 4.51 | 1.51 | 7.63 | 0.0481 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| F2.1_ks_d24@train | vae_rand | 9 | 1.53 | 2.39 | 0.752 | 4.05 | 0.0481 | 1 | 1 | 5 | 0 | 0 | inconclusive |
| F2.4_big_jump_share_err@train | vae_rand | 9 | -3.2 | -4.36 | -7.55 | -2.29 | 1 | 0.0625 | 1 | 0 | 6 | 0 | inconclusive |
| F3.6_peak168_err@train | vae_rand | 9 | 1.23 | 1.47 | 0.0967 | 2.86 | 0.112 | 1 | 1 | 5 | 1 | 0 | inconclusive |
| F1.10_hill_err@train | vae_rand | 9 | 0.551 | 1.17 | -0.0124 | 2.47 | 0.115 | 1 | 1 | 4 | 1 | 0 | inconclusive |
| F1.8_coverage@train | vae_rand | 4 | 1.07 | 1.08 | 0.248 | 2.23 | 0.115 | 1 | 1 | 1 | 0 | 0 | inconclusive |
| F2.1_ks_d6@train | vae_rand | 9 | 1.12 | 0.59 | -3.85 | 3.79 | 0.115 | 1 | 1 | 4 | 1 | 0 | inconclusive |
| F3.8_calendar_corr_err@train | vae_rand | 9 | 0.603 | 2.24 | 0.0982 | 5.4 | 0.115 | 1 | 1 | 3 | 0 | 0 | inconclusive |
| F1.6_skew_err@train | vae_rand | 9 | 1.63 | 1.52 | 0.00349 | 3.14 | 0.131 | 1 | 1 | 5 | 1 | 0 | inconclusive |
| F3.7_dfa_err@train | vae_rand | 9 | 0.621 | 2.32 | 0.278 | 4.92 | 0.131 | 1 | 1 | 3 | 0 | 0 | inconclusive |
| F1.5_q01_err@train | vae_rand | 9 | 0.623 | 1.49 | 0.0217 | 3.2 | 0.155 | 1 | 1 | 3 | 0 | 0 | inconclusive |
| F3.4_acf_abs_d@train | vae_rand | 9 | 1.91 | -1.16 | -8.34 | 2.94 | 0.182 | 1 | 1 | 5 | 1 | 0 | inconclusive |
| F1.4_qq_corr@train | vae_rand | 9 | 2.01 | 1.1 | -1.12 | 3.09 | 0.193 | 1 | 1 | 5 | 1 | 0 | inconclusive |
| F1.6_std_err@train | vae_rand | 9 | 1.49 | 1.08 | -1.14 | 3 | 0.193 | 1 | 1 | 5 | 1 | 0 | inconclusive |
| F2.3_up_share_err@train | vae_rand | 9 | 1.41 | 2.43 | -0.4 | 6.5 | 0.193 | 1 | 1 | 5 | 0 | 0 | inconclusive |
| F2.1_ks_d1@train | vae_rand | 9 | 1.23 | -0.356 | -3.89 | 2.55 | 0.338 | 1 | 1 | 5 | 2 | 0 | inconclusive |
| F3.4_acf_sq_d@train | vae_rand | 9 | 3.34 | -1.02 | -10.9 | 7.21 | 0.338 | 1 | 1 | 6 | 2 | 0 | inconclusive |
| F2.2_vol_ratio_err_d1@train | vae_rand | 9 | 2.1 | 0.63 | -1.84 | 2.93 | 0.373 | 1 | 1 | 4 | 2 | 0 | inconclusive |
| F1.6_kurt_err@train | vae_rand | 9 | 0.28 | 0.102 | -1.5 | 1.69 | 0.601 | 1 | 1 | 4 | 3 | 0 | inconclusive |
| F3.3_pacf@train | vae_rand | 9 | -3.7 | -3.37 | -6.42 | -0.259 | 0.994 | 0.781 | 1 | 2 | 5 | 0 | inconclusive |
| F3.5_log_psd@train | vae_rand | 9 | -0.923 | -1.15 | -3.98 | 1.73 | 0.875 | 1 | 1 | 3 | 2 | 0 | inconclusive |

### CS2. Distribution and dependence against val

| unit | comparator | n_datasets | median_z | mean_z | ci_lo | ci_hi | p_better_adj | p_worse_adj | p_equiv_adj | n_better | n_worse | n_same | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F2.1_w1_d24 | vae_rand | 9 | 2.17 | 3.29 | 1.35 | 5.63 | 0.0322 | 1 | 0.996 | 6 | 0 | 0 | inconclusive |
| F2.2_vol_ratio_err_d24 | vae_rand | 9 | 2.85 | 4.64 | 1.95 | 8.05 | 0.0322 | 1 | 0.996 | 6 | 0 | 0 | inconclusive |
| F2.1_ks_d168 | vae_rand | 9 | 5.2 | 5.26 | 2.83 | 7.63 | 0.043 | 1 | 0.996 | 8 | 0 | 0 | inconclusive |
| F1.5_q01_err | vae_rand | 9 | 1.26 | 2.58 | 0.83 | 4.78 | 0.129 | 1 | 0.996 | 4 | 0 | 0 | inconclusive |
| F2.1_ks_d24 | vae_rand | 9 | 1.16 | 2.08 | 0.509 | 3.63 | 0.129 | 1 | 0.996 | 5 | 0 | 0 | inconclusive |
| F1.10_hill_err | vae_rand | 9 | 0.551 | 1.34 | 0.313 | 2.6 | 0.175 | 1 | 0.908 | 3 | 0 | 0 | inconclusive |
| F1.9_js | vae_rand | 9 | 1.35 | 1.66 | 0.336 | 3.22 | 0.175 | 1 | 0.996 | 5 | 1 | 0 | inconclusive |
| F1.6_skew_err | vae_rand | 9 | 2.46 | 1.69 | 0.102 | 3.27 | 0.201 | 1 | 0.996 | 4 | 1 | 0 | inconclusive |
| F2.3_up_share_err | vae_rand | 9 | 1.65 | 2.15 | 0.0342 | 5.02 | 0.213 | 1 | 0.908 | 4 | 1 | 0 | inconclusive |
| F3.8_calendar_corr_err | vae_rand | 9 | 0.566 | 2.33 | 0.153 | 5.48 | 0.213 | 1 | 0.908 | 3 | 0 | 0 | inconclusive |
| F3.1_acf_in_window | vae_rand | 9 | 2.18 | 1.26 | -1.23 | 3.4 | 0.279 | 1 | 0.908 | 6 | 1 | 0 | inconclusive |
| F3.6_peak24_err | vae_rand | 9 | 2.7 | 3.95 | -1.53 | 9.54 | 0.279 | 1 | 0.996 | 5 | 1 | 0 | inconclusive |
| F1.6_kurt_err | vae_rand | 9 | 1.55 | 0.779 | -0.625 | 2.19 | 0.317 | 1 | 0.908 | 5 | 3 | 0 | inconclusive |
| F2.4_big_jump_share_err | vae_rand | 9 | -1.45 | -2.27 | -3.94 | -0.849 | 0.994 | 0.322 | 0.996 | 1 | 5 | 0 | inconclusive |
| F1.5_q99_err | vae_rand | 9 | 0.818 | 2.34 | -0.517 | 6.82 | 0.354 | 1 | 0.908 | 3 | 1 | 0 | inconclusive |
| F1.5_quantile_err | vae_rand | 9 | 2.11 | 1.77 | -1.09 | 4.92 | 0.371 | 1 | 0.908 | 5 | 4 | 0 | inconclusive |
| F3.7_dfa_err | vae_rand | 9 | 0.494 | 0.911 | -2.32 | 4.06 | 0.371 | 1 | 0.908 | 3 | 1 | 0 | inconclusive |
| F1.1_ks | vae_rand | 9 | 1.76 | 1.03 | -1.27 | 3.39 | 0.372 | 1 | 0.908 | 4 | 3 | 0 | inconclusive |
| F1.3_ad | vae_rand | 9 | -1.21 | 0.758 | -0.987 | 2.72 | 0.372 | 1 | 0.908 | 4 | 3 | 0 | inconclusive |
| F1.6_std_err | vae_rand | 9 | 1.5 | 1.27 | -1.26 | 3.91 | 0.372 | 1 | 0.908 | 5 | 2 | 0 | inconclusive |
| F1.7_out_of_range | vae_rand | 8 | 1.06 | 1.37 | -1.68 | 4.63 | 0.372 | 1 | 0.908 | 4 | 4 | 0 | inconclusive |
| F1.8_coverage | vae_rand | 5 | 0.2 | 0.775 | -0.63 | 2.48 | 0.372 | 1 | 0.908 | 0 | 0 | 0 | inconclusive |
| F2.2_vol_ratio_err_d1 | vae_rand | 9 | 2.1 | 1.14 | -1.23 | 3.61 | 0.372 | 1 | 0.908 | 4 | 2 | 0 | inconclusive |
| F1.4_qq_corr | vae_rand | 9 | 1.75 | 0.682 | -1.4 | 2.6 | 0.392 | 1 | 0.908 | 3 | 2 | 0 | inconclusive |
| F3.6_peak168_err | vae_rand | 9 | 1.1 | 0.763 | -0.67 | 2.23 | 0.392 | 1 | 0.908 | 3 | 1 | 0 | inconclusive |
| F1.2_w1 | vae_rand | 9 | 2.55 | 0.664 | -2.27 | 3.69 | 0.399 | 1 | 0.908 | 5 | 4 | 0 | inconclusive |
| F1.6_mean_err | vae_rand | 9 | 1.68 | 0.567 | -2.33 | 3.55 | 0.399 | 1 | 0.908 | 5 | 4 | 0 | inconclusive |
| F2.1_ks_d1 | vae_rand | 9 | 1.05 | -0.172 | -3.59 | 2.5 | 0.399 | 1 | 0.908 | 4 | 3 | 0 | inconclusive |
| F2.1_ks_d6 | vae_rand | 9 | 0.227 | -0.0951 | -2.36 | 2.13 | 0.536 | 1 | 0.908 | 3 | 3 | 0 | inconclusive |
| F3.4_acf_sq_d | vae_rand | 9 | 1.75 | -0.133 | -10.7 | 9.97 | 0.569 | 1 | 0.908 | 4 | 3 | 0 | inconclusive |
| F3.3_pacf | vae_rand | 9 | -3.23 | -2.73 | -5.46 | -0.249 | 0.994 | 0.612 | 0.996 | 2 | 5 | 0 | inconclusive |
| F3.5_log_psd | vae_rand | 9 | -0.229 | 0.0976 | -2.93 | 3.36 | 0.649 | 1 | 0.908 | 2 | 3 | 0 | inconclusive |
| F3.4_acf_abs_d | vae_rand | 9 | -0.235 | -1.09 | -4.36 | 1.37 | 0.674 | 1 | 0.908 | 3 | 3 | 0 | inconclusive |

### CS3. Seam artefacts

| unit | comparator | n_datasets | median_z | mean_z | ci_lo | ci_hi | p_better_adj | p_worse_adj | p_equiv_adj | n_better | n_worse | n_same | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F5.3_seam_z_mean | vae_rand | 9 | 5.52 | 6.25 | 4.31 | 8.38 | 0.00391 | 1 | 1 | 9 | 0 | 0 | better |
| F5.3_seam_z_p95 | vae_rand | 9 | 4.83 | 6.6 | 3.89 | 10.1 | 0.00391 | 1 | 1 | 9 | 0 | 0 | better |
| F5.6_cp_at_seams | vae_rand | 9 | 2.59 | 2.52 | 1.82 | 3.16 | 0.00391 | 1 | 1 | 7 | 0 | 0 | better |
| F5.1_ks_seam_vs_real | vae_rand | 9 | 1.84 | 1.94 | 0.707 | 3.29 | 0.00937 | 1 | 1 | 5 | 0 | 0 | better |
| F5.4_seam_local_acf | vae_rand | 9 | 0.996 | 1.7 | 0.649 | 3.37 | 0.00391 | 1 | 1 | 5 | 0 | 0 | inconclusive |
| F5.2_ks_seam_vs_inside | vae_rand | 9 | 1.86 | 2.22 | 0.532 | 4.32 | 0.026 | 1 | 1 | 5 | 0 | 0 | inconclusive |
| F5.7_seam_detect_auc_dev | vae_rand | 9 | 0.859 | 1.16 | -0.0418 | 2.65 | 0.0938 | 1 | 1 | 3 | 1 | 0 | inconclusive |
| F5.5_cp_rate_err | vae_rand | 9 | 2.29 | 1.8 | -1.07 | 4.65 | 0.125 | 1 | 1 | 4 | 1 | 0 | inconclusive |

### CS4. Structure longer than a window

| unit | comparator | n_datasets | median_z | mean_z | ci_lo | ci_hi | p_better_adj | p_worse_adj | p_equiv_adj | n_better | n_worse | n_same | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F6.4_mmd_2T | vae_rand | 9 | 2.22 | 2.18 | 0.713 | 3.73 | 0.0977 | 0.994 | 0.918 | 5 | 2 | 0 | inconclusive |
| F7.6_trend_err | vae_rand | 9 | -0.882 | -1.59 | -3.24 | -0.306 | 0.98 | 0.273 | 0.749 | 0 | 3 | 1 | inconclusive |
| F7.1_roll_mean_ks | vae_rand | 8 | 0.639 | 1.75 | -0.0857 | 3.85 | 0.383 | 0.972 | 0.749 | 3 | 1 | 0 | inconclusive |
| F7.2_roll_std_ks | vae_rand | 8 | 0.567 | 1.03 | -0.461 | 2.69 | 0.383 | 0.972 | 0.749 | 3 | 1 | 1 | inconclusive |
| F7.3_crossings_err | vae_rand | 9 | 1.65 | 2.63 | -0.442 | 7.16 | 0.383 | 0.972 | 0.749 | 4 | 1 | 0 | inconclusive |
| F7.7_regime_dur_err | vae_rand | 9 | 1.23 | 1.07 | -0.989 | 3.14 | 0.383 | 0.972 | 0.749 | 4 | 1 | 0 | inconclusive |
| F7.5_drawdown_ks | vae_rand | 9 | 0.179 | 0.0499 | -1.7 | 1.72 | 0.413 | 0.972 | 0.749 | 2 | 2 | 0 | inconclusive |
| F7.6_weekly_level_std_err | vae_rand | 9 | -0.219 | -0.939 | -2.11 | 0.211 | 0.98 | 0.625 | 0.749 | 1 | 4 | 2 | inconclusive |
| F3.2_acf_beyond_window | vae_rand | 9 | 0.228 | 0.818 | -2.92 | 4.91 | 0.65 | 0.972 | 0.749 | 2 | 2 | 0 | inconclusive |
| F7.4_excursion_ks | vae_rand | 9 | -0.175 | -0.285 | -1.5 | 0.831 | 0.737 | 0.972 | 0.749 | 1 | 1 | 1 | inconclusive |

### CS5. Target structure

| unit | comparator | n_datasets | median_z | mean_z | ci_lo | ci_hi | p_better_adj | p_worse_adj | p_equiv_adj | n_better | n_worse | n_same | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F8.1_class_tvd | vae_rand | 9 | 4.34 | 4.22 | 1.89 | 6.95 | 0.0146 | 0.998 | 0.98 | 6 | 0 | 0 | better |
| F8.4_event_by_how | vae_rand | 9 | 2.57 | 2.41 | 1.3 | 3.47 | 0.0146 | 0.998 | 0.98 | 6 | 0 | 0 | better |
| F8.5_cond_event_err | vae_rand | 9 | 3.59 | 3.25 | 1.4 | 5.19 | 0.0146 | 0.998 | 0.98 | 6 | 0 | 0 | better |
| F8.6_cond_future_ks | vae_rand | 9 | 1.22 | 2.31 | 0.861 | 4.19 | 0.0146 | 0.998 | 0.98 | 4 | 0 | 0 | better |
| F8.2_event_dur_ks | vae_rand | 9 | 1 | 1.33 | 0.381 | 2.45 | 0.0328 | 0.998 | 0.98 | 4 | 0 | 1 | inconclusive |
| F8.3_interarrival_ks | vae_rand | 9 | 0.097 | 0.541 | -0.403 | 1.89 | 0.326 | 0.998 | 0.492 | 2 | 0 | 0 | inconclusive |

### CS6. Realism of single windows and memorisation

| unit | comparator | n_datasets | median_z | mean_z | ci_lo | ci_hi | p_better_adj | p_worse_adj | p_equiv_adj | n_better | n_worse | n_same | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F6.4_mmd | vae_rand | 9 | 2.1 | 1.94 | 0.523 | 3.4 | 0.15 | 0.986 | 0.918 | 6 | 2 | 0 | inconclusive |
| F6.8_nn_dist_logratio | vae_rand | 9 | 3.67 | 2.78 | 0.607 | 5.09 | 0.15 | 0.986 | 0.918 | 5 | 1 | 0 | inconclusive |
| F6.1_disc_score | vae_rand | 9 | -0.4 | -0.594 | -1.13 | -0.0889 | 0.986 | 0.215 | 0.655 | 0 | 2 | 2 | inconclusive |
| F9.1_precision | vae_rand | 5 | 0.7 | 1.99 | 0.0532 | 4.5 | 0.344 | 0.986 | 0.918 | 2 | 0 | 0 | inconclusive |
| F10.2_near_copy_share | vae_rand | 6 | -1.84 | -1.92 | -3.85 | -0.117 | 0.986 | 0.43 | 0.918 | 0 | 3 | 0 | inconclusive |
| F10.1_dcr_logratio | vae_rand | 9 | 0.338 | 3.15 | -1.15 | 9.48 | 0.513 | 0.986 | 0.918 | 3 | 3 | 0 | inconclusive |
| F6.6_feature_fid | vae_rand | 9 | 2.75 | 0.313 | -3.85 | 3.81 | 0.513 | 0.986 | 0.918 | 6 | 3 | 0 | inconclusive |
| F9.2_coverage | vae_rand | 4 | 1.25 | 1.31 | -0.175 | 2.9 | 0.513 | 0.986 | 0.918 | 2 | 0 | 0 | inconclusive |
| F9.2_density_logdev | vae_rand | 5 | 1.91 | 0.5 | -2.49 | 3 | 0.513 | 0.986 | 0.918 | 2 | 0 | 0 | inconclusive |
| F6.2_c2st_auc_dev | vae_rand | 8 | -0.177 | -0.101 | -0.909 | 0.777 | 0.955 | 0.881 | 0.301 | 0 | 0 | 0 | inconclusive |
| F9.1_recall | vae_rand | 6 | -0.49 | 1.6 | -0.965 | 7.07 | 0.955 | 0.881 | 0.802 | 0 | 1 | 0 | inconclusive |

### CS7. TSTR of the method vs the random path (case-study task)

| unit | comparator | n_datasets | median_z | mean_z | ci_lo | ci_hi | p_better_adj | p_worse_adj | p_equiv_adj | n_better | n_worse | n_same | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| clf_up_h24_q90\|gbdt\|S\|oot\|auc | vae_rand | 9 | 0.611 | 1 | 0.29 | 1.87 | 0.0586 | 1 | 1 | 3 | 0 | 1 | inconclusive |
| clf_up_h24_q90\|gbdt\|S\|val\|auc | vae_rand | 9 | 0.611 | 1.45 | 0.352 | 2.78 | 0.0977 | 1 | 1 | 2 | 0 | 0 | inconclusive |
| clf_up_h24_q90\|mlp\|S\|oot\|auc | vae_rand | 9 | 1.18 | 1.36 | 0.218 | 2.67 | 0.148 | 1 | 1 | 3 | 0 | 0 | inconclusive |
| clf_up_h24_q90\|mlp\|S\|val\|auc | vae_rand | 9 | 1.03 | 1.49 | 0.0515 | 3.21 | 0.148 | 1 | 1 | 2 | 0 | 0 | inconclusive |
| clf_up_h24_q90\|linear\|S\|val\|auc | vae_rand | 9 | 1.1 | 1.87 | 0.0896 | 3.97 | 0.203 | 1 | 1 | 2 | 1 | 0 | inconclusive |
| clf_up_h24_q90\|linear\|S\|oot\|auc | vae_rand | 9 | 1.14 | 0.745 | -0.588 | 2.08 | 0.213 | 1 | 1 | 2 | 0 | 0 | inconclusive |

### CS8. The same on the other tasks

| unit | comparator | n_datasets | median_z | mean_z | ci_lo | ci_hi | p_better_adj | p_worse_adj | p_equiv_adj | n_better | n_worse | n_same | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| qreg_h24\|linear\|S\|val\|pinball | vae_rand | 9 | 1.76 | 2.21 | 1.28 | 3.63 | 0.0339 | 1 | 0.996 | 7 | 0 | 0 | inconclusive |
| reg_h168\|gbdt\|S\|val\|mase | vae_rand | 9 | 1.87 | 2.19 | 1.12 | 3.38 | 0.0339 | 1 | 0.996 | 6 | 0 | 0 | inconclusive |
| reg_h168\|linear\|S\|val\|mase | vae_rand | 9 | 2.96 | 3.86 | 2.29 | 5.58 | 0.0339 | 1 | 0.996 | 7 | 0 | 0 | inconclusive |
| clf_up_h24_q95\|gbdt\|S\|val\|auc | vae_rand | 9 | 0.793 | 0.943 | 0.363 | 1.57 | 0.0423 | 1 | 0.771 | 3 | 0 | 0 | inconclusive |
| clf_up_h6_q90\|gbdt\|S\|oot\|auc | vae_rand | 9 | 0.663 | 0.982 | 0.33 | 1.85 | 0.0423 | 1 | 0.679 | 2 | 0 | 0 | inconclusive |
| clf_up_h6_q90\|gbdt\|S\|val\|auc | vae_rand | 9 | 0.847 | 0.841 | 0.323 | 1.42 | 0.0423 | 1 | 0.679 | 3 | 0 | 0 | inconclusive |
| ms_h24\|gbdt\|S\|val\|mase | vae_rand | 9 | 1.66 | 1.26 | 0.54 | 1.91 | 0.0423 | 1 | 0.996 | 5 | 0 | 0 | inconclusive |
| reg_h168\|gbdt\|S\|oot\|mase | vae_rand | 9 | 3.12 | 2.74 | 0.984 | 4.36 | 0.0423 | 1 | 0.996 | 7 | 1 | 0 | inconclusive |
| reg_h1\|gbdt\|S\|oot\|mase | vae_rand | 9 | 1.83 | 1.69 | 0.748 | 2.59 | 0.0423 | 1 | 0.996 | 6 | 0 | 0 | inconclusive |
| reg_h1\|gbdt\|S\|val\|mase | vae_rand | 9 | 1.49 | 1.29 | 0.534 | 2 | 0.0423 | 1 | 0.996 | 4 | 0 | 0 | inconclusive |
| reg_h24\|gbdt\|S\|val\|mase | vae_rand | 9 | 1.37 | 1.66 | 0.673 | 2.68 | 0.0423 | 1 | 0.996 | 5 | 0 | 0 | inconclusive |
| reg_h24\|linear\|S\|val\|mase | vae_rand | 9 | 1.44 | 1.89 | 1 | 3.04 | 0.0423 | 1 | 0.996 | 7 | 0 | 0 | inconclusive |
| clf_up_h24_q95\|gbdt\|S\|oot\|auc | vae_rand | 9 | 0.592 | 0.717 | 0.114 | 1.36 | 0.0781 | 1 | 0.679 | 3 | 0 | 0 | inconclusive |
| mc3_h24\|linear\|S\|val\|logloss | vae_rand | 9 | 1.15 | 1.07 | 0.0543 | 2.03 | 0.0889 | 1 | 0.989 | 5 | 0 | 0 | inconclusive |
| qreg_h24\|linear\|S\|oot\|pinball | vae_rand | 9 | 1.32 | 1.81 | 0.264 | 3.82 | 0.0889 | 1 | 0.996 | 5 | 1 | 0 | inconclusive |
| reg_h24\|gbdt\|S\|oot\|mase | vae_rand | 9 | 1.93 | 1.59 | 0.305 | 2.69 | 0.0889 | 1 | 0.996 | 7 | 1 | 0 | inconclusive |
| clf_up_h1_q90\|gbdt\|S\|val\|auc | vae_rand | 9 | 0.255 | 0.317 | -0.00737 | 0.666 | 0.114 | 1 | 0.203 | 0 | 0 | 0 | inconclusive |
| clf_up_h1_q90\|gbdt\|S\|oot\|auc | vae_rand | 9 | 0.588 | 0.687 | 0.0143 | 1.49 | 0.121 | 1 | 0.67 | 1 | 0 | 0 | inconclusive |
| clf_up_h24_q95\|linear\|S\|val\|auc | vae_rand | 9 | 1.95 | 1.39 | -0.128 | 2.97 | 0.121 | 1 | 0.996 | 5 | 0 | 0 | inconclusive |
| clf_up_h6_q90\|linear\|S\|oot\|auc | vae_rand | 9 | 0.374 | 1.28 | -0.0716 | 3.28 | 0.121 | 1 | 0.679 | 2 | 0 | 0 | inconclusive |
| qreg_h24\|gbdt\|S\|oot\|pinball | vae_rand | 9 | 1.92 | 1.42 | -0.0242 | 2.9 | 0.121 | 1 | 0.996 | 5 | 1 | 0 | inconclusive |
| clf_up_h24_q99\|gbdt\|S\|oot\|auc | vae_rand | 9 | 0.758 | 1.16 | 0.0077 | 2.64 | 0.129 | 1 | 0.771 | 3 | 0 | 0 | inconclusive |
| ms_h24\|linear\|S\|val\|mase | vae_rand | 9 | 1.58 | 1.56 | -0.226 | 3.38 | 0.129 | 1 | 0.996 | 7 | 1 | 0 | inconclusive |
| reg_h168\|linear\|S\|oot\|mase | vae_rand | 9 | 3.23 | 1.85 | -1.83 | 4.45 | 0.129 | 1 | 0.996 | 6 | 1 | 0 | inconclusive |
| reg_h24\|linear\|S\|oot\|mase | vae_rand | 9 | 1.17 | 1.59 | 0.0733 | 3.33 | 0.129 | 1 | 0.996 | 5 | 2 | 0 | inconclusive |
| vol_h24\|gbdt\|S\|val\|mase | vae_rand | 9 | 0.71 | 0.594 | -0.386 | 1.42 | 0.129 | 1 | 0.679 | 1 | 1 | 0 | inconclusive |
| ms_h24\|gbdt\|S\|oot\|mase | vae_rand | 9 | 1.85 | 1.16 | -0.664 | 2.57 | 0.152 | 1 | 0.996 | 7 | 1 | 0 | inconclusive |
| vol_h24\|linear\|S\|val\|mase | vae_rand | 9 | 0.942 | 1.18 | -0.039 | 2.47 | 0.152 | 1 | 0.989 | 3 | 0 | 0 | inconclusive |
| vol_h24\|linear\|S\|oot\|mase | vae_rand | 9 | 0.747 | 1.15 | -0.432 | 2.85 | 0.182 | 1 | 0.989 | 4 | 1 | 0 | inconclusive |
| mc3_h24\|gbdt\|S\|val\|logloss | vae_rand | 9 | 0.804 | 0.432 | -0.789 | 1.36 | 0.21 | 1 | 0.679 | 3 | 0 | 0 | inconclusive |
| mc3_h24\|linear\|S\|oot\|logloss | vae_rand | 9 | 1.03 | 0.768 | -0.272 | 1.8 | 0.21 | 1 | 0.889 | 5 | 1 | 0 | inconclusive |
| clf_up_h1_q90\|linear\|S\|oot\|auc | vae_rand | 9 | 0.439 | 1.6 | -0.302 | 3.93 | 0.275 | 1 | 0.947 | 3 | 1 | 0 | inconclusive |
| clf_up_h1_q90\|linear\|S\|val\|auc | vae_rand | 9 | 0.165 | 0.385 | -0.544 | 1.42 | 0.275 | 1 | 0.679 | 2 | 0 | 0 | inconclusive |
| qreg_h24\|gbdt\|S\|val\|pinball | vae_rand | 9 | 1.92 | 0.26 | -2.23 | 2.02 | 0.275 | 1 | 0.963 | 5 | 0 | 0 | inconclusive |
| clf_up_h24_q95\|linear\|S\|oot\|auc | vae_rand | 9 | 0.94 | 0.558 | -1.23 | 2.11 | 0.316 | 1 | 0.989 | 4 | 0 | 0 | inconclusive |
| ms_h24\|linear\|S\|oot\|mase | vae_rand | 9 | 1.09 | 1.08 | -0.596 | 2.83 | 0.349 | 1 | 0.996 | 5 | 2 | 0 | inconclusive |
| vol_h24\|gbdt\|S\|oot\|mase | vae_rand | 9 | 1.06 | 0.0447 | -1.76 | 1.55 | 0.349 | 1 | 0.83 | 3 | 2 | 0 | inconclusive |
| clf_down_h24_q10\|gbdt\|S\|oot\|auc | vae_rand | 9 | 0.466 | 0.168 | -0.677 | 0.887 | 0.371 | 1 | 0.474 | 0 | 0 | 0 | inconclusive |
| clf_up_h24_q99\|linear\|S\|val\|auc | vae_rand | 6 | 0.281 | 0.33 | -1.06 | 1.66 | 0.371 | 1 | 0.679 | 2 | 0 | 0 | inconclusive |
| clf_up_h6_q90\|linear\|S\|val\|auc | vae_rand | 9 | 0.383 | 0.0708 | -1.07 | 1.06 | 0.371 | 1 | 0.635 | 2 | 0 | 0 | inconclusive |

_Showing 40 rows of 52 (rows with a better / worse / same verdict first); all of them — `hypotheses/CS8_global.parquet`._

### CS9. Fidelity vs other stitchers of the same pool and the long-series generators

| unit | comparator | n_datasets | median_z | mean_z | ci_lo | ci_hi | p_better_adj | p_worse_adj | p_equiv_adj | n_better | n_worse | n_same | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F11.2_rare_share_logratio | vae_atsp | 9 | 3.12 | 3.9 | 1.91 | 6.22 | 0.106 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| F3.5_log_psd | vae_atsp | 9 | 1.48 | 1.75 | 0.763 | 2.77 | 0.106 | 1 | 1 | 4 | 0 | 0 | inconclusive |
| F8.4_event_by_how | vae_atsp | 9 | 2.27 | 2.16 | 1.28 | 3.05 | 0.106 | 1 | 1 | 5 | 0 | 0 | inconclusive |
| F1.5_q01_err | vae_greedy | 9 | 1.59 | 2.28 | 0.824 | 3.87 | 0.106 | 1 | 1 | 2 | 0 | 0 | inconclusive |
| F11.1_class_share_logratio | vae_greedy | 9 | 1.77 | 2.78 | 1.43 | 4.25 | 0.106 | 1 | 1 | 5 | 0 | 0 | inconclusive |
| F11.2_rare_share_logratio | vae_greedy | 9 | 4.26 | 4.24 | 2.14 | 6.52 | 0.106 | 1 | 1 | 5 | 0 | 0 | inconclusive |
| F2.1_ks_d24 | vae_greedy | 9 | 2.25 | 2.26 | 1.1 | 3.61 | 0.106 | 1 | 1 | 2 | 0 | 0 | inconclusive |
| F3.5_log_psd | vae_greedy | 9 | 1.48 | 1.91 | 0.767 | 3.25 | 0.106 | 1 | 1 | 4 | 0 | 0 | inconclusive |
| F3.8_calendar_corr_err | vae_greedy | 9 | 1.18 | 2.73 | 0.911 | 4.88 | 0.106 | 1 | 1 | 3 | 0 | 0 | inconclusive |
| F8.1_class_tvd | vae_greedy | 9 | 2.95 | 3.39 | 1.66 | 5.3 | 0.106 | 1 | 1 | 5 | 0 | 0 | inconclusive |
| F8.4_event_by_how | vae_greedy | 9 | 2.6 | 2.42 | 1.33 | 3.39 | 0.106 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| F2.1_ks_d168 | vae_herding | 9 | 5.45 | 4.72 | 2.52 | 6.79 | 0.106 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| F5.3_seam_z_mean | vae_herding | 9 | 5.52 | 5.2 | 4.5 | 5.9 | 0.106 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| F5.3_seam_z_p95 | vae_herding | 9 | 5.41 | 5.81 | 4.25 | 7.61 | 0.106 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| F5.6_cp_at_seams | vae_herding | 9 | 2.71 | 2.88 | 2.13 | 3.68 | 0.106 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| F11.1_class_share_logratio | vae_knn | 9 | 2.66 | 3.61 | 1.96 | 5.55 | 0.106 | 1 | 1 | 8 | 0 | 0 | inconclusive |
| F11.2_rare_share_logratio | vae_knn | 9 | 4.88 | 4.98 | 2.43 | 7.79 | 0.106 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| F2.1_ks_d24 | vae_knn | 9 | 2.67 | 2.35 | 1.12 | 3.59 | 0.106 | 1 | 1 | 3 | 0 | 0 | inconclusive |
| F8.4_event_by_how | vae_knn | 9 | 2.39 | 2.5 | 1.35 | 3.59 | 0.106 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| F11.1_class_share_logratio | vae_mbb | 9 | 3.3 | 4.7 | 2.64 | 6.94 | 0.106 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| F2.1_ks_d168 | vae_mbb | 9 | 5.32 | 4.93 | 2.62 | 7.12 | 0.106 | 1 | 1 | 8 | 0 | 0 | inconclusive |
| F2.1_w1_d24 | vae_mbb | 9 | 2.46 | 3.28 | 1.33 | 5.51 | 0.106 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| F2.2_vol_ratio_err_d24 | vae_mbb | 9 | 2.59 | 4.53 | 1.88 | 7.77 | 0.106 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| F5.3_seam_z_mean | vae_mbb | 9 | 5.49 | 5.64 | 4.02 | 7.52 | 0.106 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| F5.3_seam_z_p95 | vae_mbb | 9 | 4.66 | 6.3 | 3.75 | 9.61 | 0.106 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| F5.4_seam_local_acf | vae_mbb | 9 | 0.772 | 1.5 | 0.385 | 3.31 | 0.106 | 1 | 1 | 1 | 0 | 0 | inconclusive |
| F5.6_cp_at_seams | vae_mbb | 9 | 2.45 | 2.45 | 1.82 | 3.11 | 0.106 | 1 | 1 | 8 | 0 | 0 | inconclusive |
| F3.5_log_psd | vae_pctsp | 9 | 1.99 | 2.31 | 1.12 | 3.56 | 0.106 | 1 | 1 | 5 | 0 | 0 | inconclusive |
| F3.8_calendar_corr_err | vae_pctsp | 9 | 1.26 | 2.72 | 1.11 | 4.67 | 0.106 | 1 | 1 | 3 | 0 | 0 | inconclusive |
| F8.4_event_by_how | vae_pctsp | 9 | 2.2 | 2.14 | 1.06 | 3.18 | 0.106 | 1 | 1 | 5 | 0 | 0 | inconclusive |
| F1.5_q01_err | vae_quilting | 9 | 1.79 | 2.95 | 1.28 | 5 | 0.106 | 1 | 1 | 3 | 0 | 0 | inconclusive |
| F11.1_class_share_logratio | vae_quilting | 9 | 2.72 | 3.19 | 1.7 | 4.86 | 0.106 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| F3.3_pacf | vae_quilting | 9 | 2.59 | 3.36 | 1.98 | 4.78 | 0.106 | 1 | 1 | 5 | 0 | 0 | inconclusive |
| F11.1_class_share_logratio | timestral | 9 | 42.6 | 39.3 | 22.8 | 54.5 | 0.106 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| F11.2_rare_share_logratio | timestral | 9 | 18.1 | 19.9 | 9.99 | 32.2 | 0.106 | 1 | 1 | 8 | 1 | 0 | inconclusive |
| F2.1_ks_d168 | timestral | 9 | 11.1 | 11.2 | 8.33 | 14 | 0.106 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| F2.2_vol_ratio_err_d24 | timestral | 9 | 11.5 | 28.6 | 11.9 | 49.4 | 0.106 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| F3.5_log_psd | timestral | 9 | 9.4 | 15.8 | 7.05 | 25.1 | 0.106 | 1 | 1 | 8 | 0 | 0 | inconclusive |
| F3.8_calendar_corr_err | vae_atsp | 9 | 1.15 | 2.08 | 0.723 | 3.73 | 0.118 | 1 | 1 | 3 | 0 | 0 | inconclusive |
| F11.3_multiclass_tvd | vae_greedy | 9 | 1.44 | 2.33 | 1.04 | 3.75 | 0.118 | 1 | 1 | 5 | 0 | 0 | inconclusive |

_Showing 40 rows of 1027 (rows with a better / worse / same verdict first); all of them — `hypotheses/CS9_global.parquet`._

### CS10. TSTR vs other stitchers of the same pool and the long-series generators

| unit | comparator | n_datasets | median_z | mean_z | ci_lo | ci_hi | p_better_adj | p_worse_adj | p_equiv_adj | n_better | n_worse | n_same | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| reg_h1\|gbdt\|S\|oot\|mase | vae_atsp | 9 | 0.311 | 0.685 | 0.174 | 1.31 | 0.105 | 1 | 0.604 | 1 | 0 | 1 | inconclusive |
| qreg_h24\|linear\|S\|val\|pinball | vae_greedy | 9 | 0.823 | 1.98 | 0.759 | 3.81 | 0.105 | 1 | 1 | 3 | 0 | 0 | inconclusive |
| vol_h24\|linear\|S\|val\|mase | vae_greedy | 9 | 1.23 | 1.2 | 0.597 | 1.81 | 0.105 | 1 | 1 | 2 | 0 | 1 | inconclusive |
| clf_up_h6_q90\|linear\|S\|val\|auc | vae_knn | 9 | 0.473 | 0.956 | 0.357 | 1.82 | 0.105 | 1 | 0.754 | 1 | 0 | 1 | inconclusive |
| qreg_h24\|linear\|S\|val\|pinball | vae_knn | 9 | 1.16 | 2.34 | 1 | 4.49 | 0.105 | 1 | 1 | 5 | 0 | 0 | inconclusive |
| reg_h24\|gbdt\|S\|val\|mase | vae_knn | 9 | 0.523 | 1.1 | 0.347 | 1.98 | 0.105 | 1 | 0.964 | 3 | 0 | 1 | inconclusive |
| qreg_h24\|linear\|S\|val\|pinball | vae_mbb | 9 | 2.05 | 2.33 | 1.41 | 3.67 | 0.105 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| reg_h168\|gbdt\|S\|val\|mase | vae_mbb | 9 | 1.91 | 2.12 | 1.24 | 3.18 | 0.105 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| reg_h168\|linear\|S\|val\|mase | vae_mbb | 9 | 2.66 | 3.74 | 2.3 | 5.33 | 0.105 | 1 | 1 | 8 | 0 | 0 | inconclusive |
| reg_h24\|linear\|S\|val\|mase | vae_mbb | 9 | 1.64 | 1.93 | 1.11 | 3.07 | 0.105 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| reg_h1\|linear\|S\|oot\|mase | vae_pctsp | 9 | 2.32 | 2.97 | 1.42 | 4.81 | 0.105 | 1 | 1 | 4 | 0 | 0 | inconclusive |
| clf_up_h168_q90\|gbdt\|S\|val\|auc | timestral | 9 | 1.62 | 2 | 1.14 | 3.01 | 0.105 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| mc3_h24\|gbdt\|S\|oot\|logloss | timestral | 9 | 8.48 | 15.8 | 5.95 | 30.7 | 0.105 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| mc3_h24\|gbdt\|S\|val\|logloss | timestral | 9 | 12.1 | 18.9 | 8.69 | 33.3 | 0.105 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| clf_up_h6_q90\|gbdt\|S\|val\|auc | vae_atsp | 9 | 0.441 | 0.518 | 0.143 | 0.968 | 0.109 | 1 | 0.368 | 0 | 0 | 2 | inconclusive |
| mc3_h24\|linear\|S\|val\|logloss | vae_atsp | 9 | 0.76 | 1.1 | 0.346 | 1.88 | 0.109 | 1 | 1 | 3 | 0 | 0 | inconclusive |
| qreg_h24\|linear\|S\|val\|pinball | vae_atsp | 9 | 0.955 | 1.41 | 0.575 | 2.6 | 0.109 | 1 | 0.964 | 4 | 0 | 0 | inconclusive |
| vol_h24\|linear\|S\|oot\|mase | vae_greedy | 9 | 1.41 | 1.35 | 0.719 | 1.98 | 0.109 | 1 | 1 | 3 | 0 | 1 | inconclusive |
| reg_h24\|gbdt\|S\|val\|mase | vae_mbb | 9 | 1.32 | 1.58 | 0.812 | 2.38 | 0.109 | 1 | 1 | 4 | 0 | 0 | inconclusive |
| qreg_h24\|linear\|S\|val\|pinball | vae_pctsp | 9 | 1.13 | 2.05 | 0.649 | 4.39 | 0.109 | 1 | 1 | 4 | 0 | 0 | inconclusive |
| clf_up_h24_q95\|gbdt\|S\|val\|auc | vae_quilting | 9 | 0.346 | 0.364 | 0.0504 | 0.709 | 0.109 | 1 | 0.105 | 0 | 0 | 0 | inconclusive |
| clf_up_h6_q90\|gbdt\|S\|val\|auc | vae_quilting | 9 | 0.858 | 0.784 | 0.349 | 1.3 | 0.109 | 1 | 0.604 | 1 | 0 | 0 | inconclusive |
| clf_up_h6_q90\|linear\|S\|val\|auc | vae_quilting | 9 | 0.773 | 1.1 | 0.294 | 1.99 | 0.109 | 1 | 1 | 3 | 0 | 1 | inconclusive |
| clf_up_h168_q90\|gbdt\|S\|oot\|auc | timestral | 9 | 2.45 | 1.96 | 1.12 | 2.74 | 0.109 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| clf_up_h1_q90\|linear\|S\|oot\|auc | timestral | 9 | 1.82 | 13.3 | 3.75 | 24.9 | 0.109 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| mc3_h24\|linear\|S\|oot\|logloss | timestral | 9 | 10.6 | 33.7 | 8.68 | 65.3 | 0.109 | 1 | 1 | 8 | 0 | 0 | inconclusive |
| mc3_h24\|linear\|S\|val\|logloss | timestral | 9 | 10.4 | 23.3 | 7.07 | 47.2 | 0.109 | 1 | 1 | 8 | 0 | 0 | inconclusive |
| clf_up_h168_q90\|gbdt\|S\|oot\|auc | vae_quilting | 9 | -1.37 | -2.3 | -4.28 | -0.845 | 1 | 0.123 | 1 | 0 | 5 | 0 | inconclusive |
| clf_up_h168_q90\|linear\|S\|oot\|auc | vae_quilting | 9 | -3.6 | -6.23 | -12.3 | -2.51 | 1 | 0.123 | 1 | 0 | 6 | 0 | inconclusive |
| reg_h168\|gbdt\|S\|oot\|mase | timestral | 9 | -3.67 | -2.84 | -3.89 | -1.7 | 1 | 0.123 | 1 | 0 | 6 | 0 | inconclusive |
| reg_h168\|linear\|S\|val\|mase | timestral | 9 | -2.1 | -1.99 | -2.73 | -1.25 | 1 | 0.123 | 1 | 0 | 7 | 0 | inconclusive |
| reg_h24\|linear\|S\|oot\|mase | timestral | 9 | -2.24 | -4.08 | -6.93 | -2.03 | 1 | 0.123 | 1 | 0 | 9 | 0 | inconclusive |
| reg_h24\|linear\|S\|val\|mase | timestral | 9 | -3.09 | -5.52 | -11.1 | -2.3 | 1 | 0.123 | 1 | 0 | 9 | 0 | inconclusive |
| clf_down_h24_q10\|gbdt\|S\|oot\|auc | zedge_ts_long | 9 | -1.23 | -1.66 | -2.42 | -1.04 | 1 | 0.123 | 1 | 0 | 3 | 0 | inconclusive |
| clf_down_h24_q10\|linear\|S\|oot\|auc | zedge_ts_long | 9 | -1.95 | -3.9 | -6.49 | -1.69 | 1 | 0.123 | 1 | 0 | 5 | 0 | inconclusive |
| clf_up_h168_q90\|gbdt\|S\|val\|auc | zedge_ts_long | 9 | -1.35 | -1.7 | -2.44 | -1.04 | 1 | 0.123 | 1 | 0 | 2 | 0 | inconclusive |
| clf_down_h24_q10\|gbdt\|S\|oot\|auc | zedge_ts_ar | 9 | -1.36 | -2.3 | -3.47 | -1.29 | 1 | 0.123 | 1 | 0 | 5 | 0 | inconclusive |
| clf_up_h1_q90\|gbdt\|S\|oot\|auc | zedge_ts_ar | 9 | -1.51 | -2.69 | -4.42 | -1.24 | 1 | 0.123 | 1 | 0 | 4 | 0 | inconclusive |
| clf_up_h24_q99\|gbdt\|S\|oot\|auc | zedge_ts_ar | 9 | -1.98 | -1.95 | -2.96 | -0.969 | 1 | 0.123 | 1 | 0 | 3 | 0 | inconclusive |
| mc3_h24\|linear\|S\|oot\|logloss | vae_atsp | 9 | 0.752 | 0.876 | 0.206 | 1.49 | 0.125 | 1 | 0.878 | 3 | 0 | 0 | inconclusive |

_Showing 40 rows of 754 (rows with a better / worse / same verdict first); all of them — `hypotheses/CS10_global.parquet`._

### CS11. The method's effect on TSTR across model classes

| unit | p_friedman | nemenyi_cd | n_blocks | share_blocks_same_sign | tasks |
|---|---|---|---|---|---|
| effect_by_model | 0.368 | 1.1 | 9 | 0.667 | clf_up_h24_q90 |

**avg_rank_of_effect**

| model | 0 |
|---|---|
| gbdt | 1.67 |
| mlp | 2 |
| linear | 2.33 |


### CS12. The method's effect on TSTR over time (val vs OOT) and across subgroups

| unit | comparator | n_datasets | median_z | p_equiv_adj |
|---|---|---|---|---|
| oot_minus_val\|gbdt | vae_rand | 9 | -0.653 | 0.395 |
| oot_minus_val\|linear | vae_rand | 9 | -0.801 | 0.708 |
| oot_minus_val\|mlp | vae_rand | 9 | -0.687 | 0.395 |
| oot_minus_val\|gbdt | diffusion_ts | 9 | -0.442 | 0.554 |
| oot_minus_val\|linear | diffusion_ts | 9 | 0.202 | 0.554 |
| oot_minus_val\|mlp | diffusion_ts | 9 | 0.632 | 0.395 |
| oot_minus_val\|gbdt | chronos | 7 | -0.502 | 0.395 |
| oot_minus_val\|linear | chronos | 7 | -1.01 | 0.656 |
| oot_minus_val\|mlp | chronos | 7 | -0.189 | 0.395 |
| oot_minus_val\|gbdt | timesfm | 6 | 0.646 | 0.554 |
| oot_minus_val\|linear | timesfm | 6 | -0.184 | 0.554 |
| oot_minus_val\|mlp | timesfm | 6 | 1.26 | 0.719 |
| oot_minus_val\|gbdt | timestral | 9 | 0.442 | 0.395 |
| oot_minus_val\|linear | timestral | 9 | -1.07 | 0.583 |
| oot_minus_val\|mlp | timestral | 9 | 0.549 | 0.554 |
| oot_minus_val\|gbdt | zedge_ts_long | 9 | -1.02 | 0.554 |
| oot_minus_val\|linear | zedge_ts_long | 9 | -0.337 | 0.554 |
| oot_minus_val\|mlp | zedge_ts_long | 9 | -0.0214 | 0.395 |
| oot_minus_val\|gbdt | zedge_ts_ar | 9 | -1 | 0.562 |
| oot_minus_val\|linear | zedge_ts_ar | 9 | -0.753 | 0.554 |
| oot_minus_val\|mlp | zedge_ts_ar | 9 | -0.0701 | 0.395 |

### CS13. TSTR of the method vs TRTR

| unit | comparator | n_datasets | median_z | mean_z | ci_lo | ci_hi | p_better_adj | p_worse_adj | p_equiv_adj | n_better | n_worse | n_same | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| clf_up_h1_q90\|gbdt\|val\|auc | TRTR | 9 | -3.45 | -4.29 | -6.13 | -2.51 | 1 | 0.00453 | 1 | 0 | 8 | 0 | worse |
| clf_up_h24_q90\|mlp\|oot\|auc | TRTR | 9 | -3.17 | -4.75 | -7.43 | -2.44 | 1 | 0.00453 | 1 | 0 | 7 | 0 | worse |
| clf_up_h6_q90\|linear\|val\|auc | TRTR | 9 | -1.92 | -3.25 | -6.11 | -1.46 | 1 | 0.00453 | 1 | 0 | 8 | 0 | worse |
| mc3_h24\|gbdt\|val\|logloss | TRTR | 9 | -2.75 | -3.22 | -4.6 | -2.3 | 1 | 0.00453 | 1 | 0 | 9 | 0 | worse |
| mc3_h24\|linear\|oot\|logloss | TRTR | 9 | -2.53 | -3.86 | -6.18 | -2.14 | 1 | 0.00453 | 1 | 0 | 8 | 0 | worse |
| mc3_h24\|linear\|val\|logloss | TRTR | 9 | -3.02 | -3.78 | -5.11 | -2.58 | 1 | 0.00453 | 1 | 0 | 8 | 0 | worse |
| ms_h24\|gbdt\|oot\|mase | TRTR | 9 | -3.6 | -5.09 | -7.02 | -3.46 | 1 | 0.00453 | 1 | 0 | 9 | 0 | worse |
| ms_h24\|gbdt\|val\|mase | TRTR | 9 | -4.38 | -6.44 | -11.5 | -3.23 | 1 | 0.00453 | 1 | 0 | 9 | 0 | worse |
| ms_h24\|linear\|oot\|mase | TRTR | 9 | -3.86 | -5.16 | -7.84 | -3.19 | 1 | 0.00453 | 1 | 0 | 9 | 0 | worse |
| ms_h24\|linear\|val\|mase | TRTR | 9 | -3.66 | -5.56 | -8.4 | -3.16 | 1 | 0.00453 | 1 | 0 | 9 | 0 | worse |
| qreg_h24\|gbdt\|oot\|pinball | TRTR | 9 | -4.11 | -4.8 | -5.95 | -3.76 | 1 | 0.00453 | 1 | 0 | 9 | 0 | worse |
| qreg_h24\|gbdt\|val\|pinball | TRTR | 9 | -4.45 | -6.25 | -10.4 | -3.7 | 1 | 0.00453 | 1 | 0 | 9 | 0 | worse |
| qreg_h24\|linear\|oot\|pinball | TRTR | 9 | -3.25 | -4.06 | -5.16 | -3.02 | 1 | 0.00453 | 1 | 0 | 9 | 0 | worse |
| qreg_h24\|linear\|val\|pinball | TRTR | 9 | -2.9 | -3.76 | -5.19 | -2.67 | 1 | 0.00453 | 1 | 0 | 9 | 0 | worse |
| reg_h168\|gbdt\|oot\|mase | TRTR | 9 | -3.73 | -3.37 | -4.17 | -2.55 | 1 | 0.00453 | 1 | 0 | 9 | 0 | worse |
| reg_h168\|gbdt\|val\|mase | TRTR | 9 | -3.06 | -2.79 | -3.73 | -1.89 | 1 | 0.00453 | 1 | 0 | 8 | 0 | worse |
| reg_h168\|linear\|oot\|mase | TRTR | 9 | -3.78 | -5.27 | -9.6 | -2.62 | 1 | 0.00453 | 1 | 0 | 9 | 0 | worse |
| reg_h168\|linear\|val\|mase | TRTR | 9 | -2 | -2.43 | -3.19 | -1.77 | 1 | 0.00453 | 1 | 0 | 9 | 0 | worse |
| reg_h1\|gbdt\|oot\|mase | TRTR | 9 | -4.21 | -8.66 | -15.1 | -3.72 | 1 | 0.00453 | 1 | 0 | 9 | 0 | worse |
| reg_h24\|gbdt\|oot\|mase | TRTR | 9 | -3.81 | -5.1 | -8 | -3.14 | 1 | 0.00453 | 1 | 0 | 9 | 0 | worse |
| reg_h24\|gbdt\|val\|mase | TRTR | 9 | -4.11 | -4.91 | -6.36 | -3.6 | 1 | 0.00453 | 1 | 0 | 9 | 0 | worse |
| reg_h24\|linear\|oot\|mase | TRTR | 9 | -3.44 | -5.02 | -7.85 | -3.04 | 1 | 0.00453 | 1 | 0 | 9 | 0 | worse |
| reg_h24\|linear\|val\|mase | TRTR | 9 | -3.89 | -5.75 | -11.2 | -2.61 | 1 | 0.00453 | 1 | 0 | 9 | 0 | worse |
| vol_h24\|gbdt\|oot\|mase | TRTR | 9 | -6.22 | -4.89 | -6.95 | -2.84 | 1 | 0.00453 | 1 | 0 | 7 | 0 | worse |
| clf_down_h24_q10\|gbdt\|oot\|auc | TRTR | 9 | -2.73 | -2.69 | -3.92 | -1.5 | 1 | 0.00708 | 1 | 0 | 7 | 0 | worse |
| clf_up_h168_q90\|gbdt\|oot\|auc | TRTR | 9 | -3.35 | -3.57 | -5.36 | -1.94 | 1 | 0.00708 | 1 | 0 | 7 | 0 | worse |
| clf_up_h1_q90\|gbdt\|oot\|auc | TRTR | 9 | -3.13 | -3.78 | -5.56 | -2.24 | 1 | 0.00708 | 1 | 0 | 8 | 0 | worse |
| clf_up_h24_q95\|gbdt\|oot\|auc | TRTR | 9 | -2.96 | -3.19 | -4.9 | -1.65 | 1 | 0.00708 | 1 | 0 | 7 | 0 | worse |
| clf_up_h24_q95\|linear\|val\|auc | TRTR | 9 | -1.75 | -3.58 | -7.09 | -1.29 | 1 | 0.00708 | 1 | 0 | 7 | 0 | worse |
| reg_h1\|gbdt\|val\|mase | TRTR | 9 | -3.55 | -5.41 | -8.74 | -2.76 | 1 | 0.00708 | 1 | 0 | 8 | 0 | worse |
| reg_h1\|linear\|oot\|mase | TRTR | 9 | -2.4 | -3.35 | -5.5 | -1.57 | 1 | 0.00708 | 1 | 0 | 8 | 0 | worse |
| clf_up_h168_q90\|gbdt\|val\|auc | TRTR | 9 | -3.32 | -3.35 | -5.27 | -1.63 | 1 | 0.00871 | 1 | 0 | 7 | 0 | worse |
| clf_up_h24_q90\|gbdt\|oot\|auc | TRTR | 9 | -4.27 | -3.72 | -5.64 | -1.81 | 1 | 0.00871 | 1 | 0 | 7 | 0 | worse |
| clf_up_h24_q90\|linear\|val\|auc | TRTR | 9 | -1.78 | -2.89 | -4.95 | -1.18 | 1 | 0.00871 | 1 | 0 | 7 | 0 | worse |
| clf_up_h24_q90\|mlp\|val\|auc | TRTR | 9 | -2.3 | -3.78 | -5.92 | -1.8 | 1 | 0.00871 | 1 | 0 | 7 | 0 | worse |
| clf_up_h6_q90\|gbdt\|oot\|auc | TRTR | 9 | -2.36 | -2.64 | -4.45 | -1.22 | 1 | 0.00871 | 1 | 1 | 7 | 0 | worse |
| clf_up_h6_q90\|gbdt\|val\|auc | TRTR | 9 | -2.24 | -2.06 | -2.94 | -0.932 | 1 | 0.00871 | 1 | 0 | 8 | 0 | worse |
| mc3_h24\|gbdt\|oot\|logloss | TRTR | 9 | -2.94 | -3 | -4.79 | -1.32 | 1 | 0.00871 | 1 | 0 | 7 | 0 | worse |
| clf_up_h24_q90\|gbdt\|val\|auc | TRTR | 9 | -1.5 | -3.04 | -5.16 | -1.28 | 1 | 0.0135 | 1 | 1 | 8 | 0 | worse |
| clf_up_h24_q95\|linear\|oot\|auc | TRTR | 9 | -3.22 | -3.48 | -6.17 | -1.19 | 1 | 0.0135 | 1 | 0 | 6 | 0 | worse |

_Showing 40 rows of 58 (rows with a better / worse / same verdict first); all of them — `hypotheses/CS13_global.parquet`._

**transfer_ratio_case_cell**

| method | beijing_pm25 | bike | bitcoin | electricity | ett | household | jena | metro | pjm |
|---|---|---|---|---|---|---|---|---|---|
| chronos |  | 0.822 |  |  | 0.13 | 0 | 1.02 | 0.857 | 0.291 |
| diffusion_ts | 1.68 | 0.881 |  | 0.768 | 1.04 | 1 | 0.241 | 0.953 | 0.595 |
| timesfm |  | 0.893 |  | 0.94 | 0 |  | -0.071 | 1.05 | 0.718 |
| timestral | -2.37 | 0.915 |  | 0.548 | 0 | 0 | -0.071 | 1.07 | 0.486 |
| vae_atsp | 0.978 | 0.85 |  | 0.261 | 0.891 | 0.4 | 0.74 | 0.592 | 0.277 |
| vae_greedy | 1.15 | 0.812 |  | 0.264 | 0.886 | 0.379 | 1.26 | 0.571 | 0.176 |
| vae_herding | 0.68 | 0.71 |  | -0.058 | 0.886 | 0.715 | 1.83 | 0.742 | 0.373 |
| vae_knn | 1.26 | 0.841 |  | 0.212 | 0.948 | 0.372 | 0.855 | 0.734 | 0.201 |
| vae_mbb | 0.913 | 0.763 |  | 0.099 | 0.971 | 0.379 | 1.17 | 0.669 | 0.182 |
| vae_pctsp | 1.24 | 0.847 |  | 0.217 | 0.956 | 0.499 | 1.13 | 0.594 | 0.162 |
| vae_quilting | 0.654 | 0.844 |  | 0.438 | 0.83 | 0.503 | 0.582 | 0.896 | 0.33 |
| vae_rand | 0.951 | 0.737 |  | 0.092 | 0.966 | 0.373 | 1.19 | 0.666 | 0.26 |
| vae_zseries | 0.625 | 0.808 |  | 0.292 | 0.806 | 0.68 | 0.786 | 0.753 | 0.449 |
| vae_zseries_quilt | 1.01 | 0.398 |  | -0.01 | 0.777 | 0.578 | 0.979 | 0.47 | 0.172 |
| vae_zseries_wsola | 0.479 | 0.503 |  | 0.546 | 0.693 | 0.631 | 0.696 | 0.687 | 0.485 |
| vae_zseries_xfade | 0.953 | 0.422 |  | 0.018 | 0.743 | 0.59 | 1.04 | 0.466 | 0.187 |
| zedge_atsp | 0.55 | 0.902 |  | 0.689 | 0.976 | 0.937 | 1.58 | 0.966 | 0.905 |
| zedge_greedy | 0.741 | 0.885 |  | 0.616 | 1.04 | 0.946 | 1.61 | 0.89 | 0.868 |
| zedge_herding | -0.224 | 0.826 |  | 0.199 | 1.01 | 0.868 | 1.74 | 0.761 | 0.663 |
| zedge_knn | -0.304 | 0.851 |  | 0.449 | 0.948 | 0.919 | 1.4 | 0.898 | 0.849 |
| zedge_mbb | 0.619 | 0.921 |  | 0.277 | 0.985 | 0.87 | 1.88 | 0.81 | 0.715 |
| zedge_pctsp | 0.304 | 0.895 |  | 0.69 | 0.968 | 0.936 | 1.55 | 0.944 | 0.931 |
| zedge_quilting | 0.386 | 0.895 |  | 0.95 | 1.02 | 0.966 | 1.51 | 0.987 | 0.935 |
| zedge_rand | 0.214 | 0.798 |  | 0.106 | 0.959 | 0.895 | 1.83 | 0.774 | 0.75 |
| zedge_ts_ar | 1.96 | 0.974 |  | 0.887 | 0.711 | 1 | 1.23 | 1.01 | 0.963 |
| zedge_ts_long | 1.19 | 0.917 |  | 0.545 | 0.936 | 0.985 | 1.23 | 0.998 | 0.9 |
| zedge_zseries | -0.509 | 0.896 |  | 0.635 | 0.86 | 0.923 | 1.53 | 0.815 | 0.899 |
| zedge_zseries_quilt | 0.381 | 0.419 |  | 0.052 | 0.808 | 0.812 | 1.55 | 0.403 | 0.504 |
| zedge_zseries_wsola | 0.849 | 0.819 |  | 0.48 | 0.884 | 0.896 | 1.6 | 0.797 | 0.806 |
| zedge_zseries_xfade | 0.738 | 0.4 |  | -0.04 | 0.795 | 0.834 | 1.58 | 0.408 | 0.528 |


**transfer_ratio_by_task**

| method | clf_down_h24_q10 | clf_up_h168_q90 | clf_up_h1_q90 | clf_up_h24_q90 | clf_up_h24_q95 | clf_up_h24_q99 | clf_up_h6_q90 | mc3_h24 | ms_h24 | qreg_h24 | reg_h1 | reg_h168 | reg_h24 | vol_h24 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| chronos | 0.514 | 0.265 | 0.848 | 0.549 | 0.428 | 0.517 | 0.744 | 0.439 | 0.806 | 0.719 | 0.822 | 0.858 | 0.867 | 0.616 |
| diffusion_ts | 0.922 | 0.573 | 0.915 | 0.812 | 0.755 | 0.514 | 0.877 | 0.549 | 0.728 | 0.741 | 0.792 | 0.951 | 0.815 | 0.867 |
| timesfm | 0.714 | 0.56 | 0.935 | 0.648 | 0.745 | 0.381 | 0.922 | 0.35 | 0.879 | 0.81 | 0.827 | 0.988 | 0.964 | 0.717 |
| timestral | 0 | -0.313 | 0.833 | 0 | 0 | -0.108 | 0.336 | 0.29 | 0.824 | 0.676 | 0.75 | 0.977 | 0.941 | 0.67 |
| vae_atsp | 0.821 | 0.418 | 0.915 | 0.642 | 0.661 | 0.65 | 0.848 | 0.628 | 0.583 | 0.516 | 0.79 | 0.563 | 0.538 | 0.537 |
| vae_greedy | 0.795 | 0.382 | 0.92 | 0.615 | 0.682 | 0.708 | 0.828 | 0.627 | 0.585 | 0.516 | 0.809 | 0.568 | 0.519 | 0.546 |
| vae_herding | 0.892 | 0.352 | 0.92 | 0.616 | 0.616 | 0.593 | 0.84 | 0.718 | 0.679 | 0.614 | 0.75 | 0.414 | 0.609 | 0.613 |
| vae_knn | 0.789 | 0.36 | 0.924 | 0.619 | 0.626 | 0.632 | 0.841 | 0.615 | 0.583 | 0.493 | 0.801 | 0.52 | 0.51 | 0.535 |
| vae_mbb | 0.823 | 0.415 | 0.909 | 0.533 | 0.516 | 0.539 | 0.808 | 0.624 | 0.572 | 0.468 | 0.773 | 0.404 | 0.463 | 0.52 |
| vae_pctsp | 0.823 | 0.334 | 0.929 | 0.646 | 0.692 | 0.638 | 0.863 | 0.622 | 0.576 | 0.493 | 0.786 | 0.544 | 0.515 | 0.605 |
| vae_quilting | 0.817 | 0.51 | 0.924 | 0.621 | 0.63 | 0.725 | 0.811 | 0.675 | 0.62 | 0.563 | 0.781 | 0.531 | 0.571 | 0.589 |
| vae_rand | 0.824 | 0.422 | 0.901 | 0.573 | 0.532 | 0.536 | 0.802 | 0.62 | 0.565 | 0.478 | 0.765 | 0.393 | 0.465 | 0.498 |
| vae_zseries | 0.824 | 0.211 | 0.921 | 0.667 | 0.69 | 0.627 | 0.887 | 0.69 | 0.635 | 0.619 | 0.825 | 0.591 | 0.637 | 0.579 |
| vae_zseries_quilt | 0.783 | 0.071 | 0.913 | 0.526 | 0.512 | 0.508 | 0.864 | 0.645 | 0.601 | 0.574 | 0.8 | 0.427 | 0.575 | 0.572 |
| vae_zseries_wsola | 0.805 | 0.336 | 0.925 | 0.608 | 0.576 | 0.554 | 0.878 | 0.669 | 0.637 | 0.607 | 0.778 | 0.515 | 0.617 | 0.661 |
| vae_zseries_xfade | 0.783 | 0.074 | 0.924 | 0.518 | 0.501 | 0.475 | 0.868 | 0.645 | 0.606 | 0.578 | 0.779 | 0.428 | 0.573 | 0.642 |
| zedge_atsp | 0.974 | 0.608 | 0.983 | 0.892 | 0.896 | 0.905 | 0.991 | 0.895 | 0.89 | 0.92 | 0.919 | 0.611 | 0.918 | 0.919 |
| zedge_greedy | 0.965 | 0.519 | 0.984 | 0.875 | 0.904 | 0.948 | 0.996 | 0.888 | 0.889 | 0.905 | 0.933 | 0.647 | 0.908 | 0.922 |
| zedge_herding | 0.966 | 0.269 | 0.978 | 0.777 | 0.732 | 0.709 | 0.978 | 0.9 | 0.863 | 0.891 | 0.871 | 0.374 | 0.835 | 0.869 |
| zedge_knn | 0.968 | 0.571 | 0.986 | 0.852 | 0.85 | 0.89 | 0.986 | 0.893 | 0.885 | 0.906 | 0.918 | 0.571 | 0.887 | 0.897 |
| zedge_mbb | 0.968 | 0.255 | 0.984 | 0.809 | 0.768 | 0.763 | 0.985 | 0.893 | 0.857 | 0.879 | 0.877 | 0.361 | 0.824 | 0.846 |
| zedge_pctsp | 0.978 | 0.545 | 0.978 | 0.876 | 0.894 | 0.891 | 0.992 | 0.906 | 0.889 | 0.925 | 0.923 | 0.582 | 0.923 | 0.919 |
| zedge_quilting | 0.981 | 0.732 | 0.985 | 0.908 | 0.92 | 0.965 | 0.994 | 0.921 | 0.914 | 0.934 | 0.929 | 0.765 | 0.94 | 0.921 |
| zedge_rand | 0.977 | 0.337 | 0.981 | 0.789 | 0.75 | 0.788 | 0.981 | 0.89 | 0.865 | 0.876 | 0.867 | 0.339 | 0.82 | 0.838 |
| zedge_ts_ar | 0.987 | 0.88 | 0.973 | 0.949 | 0.956 | 0.997 | 0.981 | 0.898 | 0.919 | 0.947 | 0.923 | 0.93 | 0.938 | 0.925 |
| zedge_ts_long | 0.962 | 0.722 | 0.963 | 0.853 | 0.889 | 0.961 | 0.954 | 0.887 | 0.858 | 0.904 | 0.899 | 0.836 | 0.894 | 0.857 |
| zedge_zseries | 0.954 | 0.234 | 0.98 | 0.833 | 0.841 | 0.868 | 0.983 | 0.896 | 0.905 | 0.918 | 0.927 | 0.592 | 0.914 | 0.926 |
| zedge_zseries_quilt | 0.923 | 0.105 | 0.981 | 0.637 | 0.649 | 0.733 | 0.98 | 0.831 | 0.831 | 0.834 | 0.9 | 0.38 | 0.777 | 0.906 |
| zedge_zseries_wsola | 0.938 | 0.371 | 0.984 | 0.779 | 0.806 | 0.837 | 0.987 | 0.876 | 0.879 | 0.908 | 0.916 | 0.544 | 0.898 | 0.912 |
| zedge_zseries_xfade | 0.912 | 0.088 | 0.979 | 0.624 | 0.618 | 0.685 | 0.974 | 0.828 | 0.835 | 0.835 | 0.894 | 0.376 | 0.779 | 0.919 |


### CS14. Computational cost of the method vs the others

| unit | comparator | median_ratio_comp_over_method | ci_ratio_lo | ci_ratio_hi | p_method_faster | p_method_slower | p_equiv_10pct | n_datasets | p_method_faster_adj | p_method_slower_adj |
|---|---|---|---|---|---|---|---|---|---|---|
| total_wall_time | chronos | 0.244 | 0.233 | 0.282 | 1 | 0.00781 | 1 | 7 | 1 | 0.117 |
| total_wall_time | diffusion_ts | 20.7 | 14.9 | 22.1 | 0.00195 | 1 | 1 | 9 | 0.043 | 1 |
| total_wall_time | timesfm | 0.0165 | 0.0148 | 0.0187 | 1 | 0.0156 | 1 | 6 | 1 | 0.219 |
| total_wall_time | timestral | 0.00906 | 0.00817 | 0.0104 | 1 | 0.00195 | 1 | 9 | 1 | 0.043 |
| total_wall_time | vae_atsp | 1.21 | 1.19 | 1.29 | 0.00195 | 1 | 1 | 9 | 0.043 | 1 |
| total_wall_time | vae_greedy | 0.984 | 0.981 | 0.985 | 1 | 0.00195 | 0.00195 | 9 | 1 | 0.043 |
| total_wall_time | vae_herding | 0.984 | 0.981 | 0.985 | 1 | 0.00195 | 0.00195 | 9 | 1 | 0.043 |
| total_wall_time | vae_knn | 0.984 | 0.981 | 0.985 | 1 | 0.00195 | 0.00195 | 9 | 1 | 0.043 |
| total_wall_time | vae_mbb | 0.984 | 0.981 | 0.985 | 1 | 0.00195 | 0.00195 | 9 | 1 | 0.043 |
| total_wall_time | vae_pctsp | 1.32 | 1.31 | 1.39 | 0.00195 | 1 | 1 | 9 | 0.043 | 1 |
| total_wall_time | vae_quilting | 0.984 | 0.981 | 0.985 | 1 | 0.00195 | 0.00195 | 9 | 1 | 0.043 |
| total_wall_time | vae_rand | 0.984 | 0.981 | 0.985 | 1 | 0.00195 | 0.00195 | 9 | 1 | 0.043 |
| total_wall_time | zedge_atsp | 6 | 5.33 | 7.38 | 0.00195 | 1 | 1 | 9 | 0.043 | 1 |
| total_wall_time | zedge_greedy | 5.77 | 5.11 | 7.15 | 0.00195 | 1 | 1 | 9 | 0.043 | 1 |
| total_wall_time | zedge_herding | 5.77 | 5.11 | 7.16 | 0.00195 | 1 | 1 | 9 | 0.043 | 1 |
| total_wall_time | zedge_knn | 5.77 | 5.11 | 7.15 | 0.00195 | 1 | 1 | 9 | 0.043 | 1 |
| total_wall_time | zedge_mbb | 5.77 | 5.11 | 7.15 | 0.00195 | 1 | 1 | 9 | 0.043 | 1 |
| total_wall_time | zedge_pctsp | 6.2 | 5.44 | 7.54 | 0.00195 | 1 | 1 | 9 | 0.043 | 1 |
| total_wall_time | zedge_quilting | 5.77 | 5.11 | 7.15 | 0.00195 | 1 | 1 | 9 | 0.043 | 1 |
| total_wall_time | zedge_rand | 5.77 | 5.11 | 7.15 | 0.00195 | 1 | 1 | 9 | 0.043 | 1 |
| total_wall_time | zedge_ts_ar | 19.7 | 17.8 | 27 | 0.00195 | 1 | 1 | 9 | 0.043 | 1 |
| total_wall_time | zedge_ts_long | 19.6 | 17.6 | 26.9 | 0.00195 | 1 | 1 | 9 | 0.043 | 1 |

**hardware**: ['NVIDIA H200']

### CS15. Moderators of the method's effect (exploratory)

| effect | descriptor | spearman | p | n | p_bh |
|---|---|---|---|---|---|
| CS2:vae_rand | acf24 | -0.55 | 0.125 | 9 | 0.36 |
| CS2:vae_rand | acf168 | -0.333 | 0.381 | 9 | 0.646 |
| CS2:vae_rand | kurt_d24 | -0.0833 | 0.831 | 9 | 0.897 |
| CS2:vae_rand | volclust | -0.0667 | 0.865 | 9 | 0.903 |
| CS2:vae_rand | trend | -0.467 | 0.205 | 9 | 0.465 |
| CS2:vae_rand | nan_share | 0.456 | 0.217 | 9 | 0.468 |
| CS4:vae_rand | acf24 | -0.0167 | 0.966 | 9 | 0.966 |
| CS4:vae_rand | acf168 | 0.333 | 0.381 | 9 | 0.646 |
| CS4:vae_rand | kurt_d24 | 0.717 | 0.0298 | 9 | 0.282 |
| CS4:vae_rand | volclust | -0.117 | 0.765 | 9 | 0.855 |
| CS4:vae_rand | trend | -0.0667 | 0.865 | 9 | 0.903 |
| CS4:vae_rand | nan_share | -0.16 | 0.681 | 9 | 0.855 |
| CS7:vae_rand | acf24 | -0.133 | 0.732 | 9 | 0.855 |
| CS7:vae_rand | acf168 | 0.283 | 0.46 | 9 | 0.741 |
| CS7:vae_rand | kurt_d24 | 0.583 | 0.0992 | 9 | 0.314 |
| CS7:vae_rand | volclust | 0.133 | 0.732 | 9 | 0.855 |
| CS7:vae_rand | trend | -0.567 | 0.112 | 9 | 0.331 |
| CS7:vae_rand | nan_share | 0.251 | 0.515 | 9 | 0.815 |
| CS10:chronos | acf24 | 0.143 | 0.76 | 7 | 0.855 |
| CS10:chronos | acf168 | -0.679 | 0.0938 | 7 | 0.314 |
| CS10:chronos | kurt_d24 | -0.75 | 0.0522 | 7 | 0.303 |
| CS10:chronos | volclust | -0.0357 | 0.939 | 7 | 0.966 |
| CS10:chronos | trend | -0.214 | 0.645 | 7 | 0.855 |
| CS10:chronos | nan_share | 0.408 | 0.363 | 7 | 0.639 |
| CS10:diffusion_ts | acf24 | 0.433 | 0.244 | 9 | 0.483 |
| CS10:diffusion_ts | acf168 | -0.117 | 0.765 | 9 | 0.855 |
| CS10:diffusion_ts | kurt_d24 | -0.6 | 0.0876 | 9 | 0.314 |
| CS10:diffusion_ts | volclust | 0.4 | 0.286 | 9 | 0.555 |
| CS10:diffusion_ts | trend | 0.6 | 0.0876 | 9 | 0.314 |
| CS10:diffusion_ts | nan_share | -0.456 | 0.217 | 9 | 0.468 |
| CS10:timesfm | acf24 | -0.257 | 0.623 | 6 | 0.855 |
| CS10:timesfm | acf168 | -0.829 | 0.0416 | 6 | 0.282 |
| CS10:timesfm | kurt_d24 | -0.829 | 0.0416 | 6 | 0.282 |
| CS10:timesfm | volclust | -0.314 | 0.544 | 6 | 0.836 |
| CS10:timesfm | trend | 0.886 | 0.0188 | 6 | 0.282 |
| CS10:timestral | acf24 | -0.2 | 0.606 | 9 | 0.855 |
| CS10:timestral | acf168 | -0.733 | 0.0246 | 9 | 0.282 |
| CS10:timestral | kurt_d24 | -0.583 | 0.0992 | 9 | 0.314 |
| CS10:timestral | volclust | -0.15 | 0.7 | 9 | 0.855 |
| CS10:timestral | trend | -0.167 | 0.668 | 9 | 0.855 |

_Showing 40 rows of 95; all of them — `hypotheses/CS15_global.parquet`._
