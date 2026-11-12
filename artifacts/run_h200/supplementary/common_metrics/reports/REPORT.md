# Benchmark report

Datasets: beijing_pm25, bike, bitcoin, electricity, ett, household, jena, metro, pjm. Seeds: 10. α = 0.05. Metrics left out: F5.1_ks_seam_vs_real, F5.2_ks_seam_vs_inside, F5.3_seam_z_mean, F5.3_seam_z_p95, F5.4_seam_local_acf, F5.6_cp_at_seams, F5.7_seam_detect_auc_dev (Config.exclude_metrics). Leakage (Config.leaked): `chronos` on electricity, beijing_pm25; `timesfm` on beijing_pm25, household, bitcoin. Verdict of a comparison "A vs B": better / worse (A better / worse than B) / same (equivalence, TOST) / inconclusive. Effects are in noise units — divided by the smallest effect size of interest (SESOI: the median |vae_rand − vae_rand_b| on one pool — or, where vae_rand_b is not run (min), the between-seed spread of vae_rand — or the method's between-seed spread, see HYPOTHESES.md §2). Utility: TSTR (training on synthetic data only) vs TRTR (training on real data), tested on the real val / OOT; transfer ratio = 1 — synthetic data train the model as well as real data. Overall leaderboard — `OVERALL.md`; ranking of every method in every slice — `LEADERBOARD.md`; values of the metrics by slice — `METRIC_VALUES.md` (this folder). Tables of the tests — `hypotheses/`.

## Overall leaderboard

Fidelity on the core metrics (each criterion against train, val and OOT) and utility (TSTR classification and regression, val and OOT), equal weights; noise-aware ranks; privacy and cost not included. Composition, columns and the robustness checks — `OVERALL.md`.

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon | fidelity_rank | utility_rank | norm_overall | memorisation_flag |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| zedge_quilting | optimised selection | 8.4 | 7.33 | 9.46 | 0.537 | 0.886 |  | True | 8.56 | 8.25 | 0.462 | False |
| zedge_zseries | optimised selection | 8.67 | 8.11 | 9.33 | 0.194 | 0.697 | 0.852 | True | 8.62 | 8.72 | 0.26 | False |
| zedge_ts_ar | long-series generator | 8.85 | 7 | 10.8 | 0.253 | 0.555 | 0.852 | True | 9.02 | 8.69 | 0.783 | False |
| zedge_greedy | optimised selection | 8.91 | 7.88 | 9.95 | 0.006 | 0.503 | 0.852 | True | 8.89 | 8.92 | 0.284 | False |
| zedge_pctsp | optimised selection | 9.09 | 8.01 | 10.2 | 0 | 0.13 | 0.75 | True | 8.93 | 9.26 | 0.251 | False |
| zedge_knn | optimised selection | 9.26 | 8.21 | 10.4 | 0.002 | 0.043 | 0.752 | True | 9.14 | 9.37 | 0.388 | False |
| zedge_atsp | optimised selection | 9.32 | 7.68 | 11 | 0.008 | 0.137 | 0.852 | True | 9 | 9.64 | 0.302 | False |
| zedge_ts_long | long-series generator | 9.51 | 8 | 11.2 | 0 | 0.049 | 0.574 | True | 9.53 | 9.49 | 0.736 | False |
| zedge_herding | optimised selection | 10.2 | 8.93 | 11.5 | 0 | 0 | 0.297 | True | 9.71 | 10.7 | 0.047 | False |
| zedge_mbb | optimised selection | 10.4 | 9 | 12 | 0 | 0 | 0.246 | True | 10.2 | 10.7 | 0.0562 | False |
| zedge_rand | random selection | 10.6 | 9 | 12.2 | 0 | 0 | 0.195 | True | 10.2 | 11 | 0 | False |
| vae_herding | optimised selection | 13.5 | 12.7 | 14.4 | 0 | 0 | 0.0449 | False | 13.1 | 13.9 | 0.302 | False |
| diffusion_ts | long-series generator | 13.5 | 11.6 | 15.2 | 0 | 0 | 0.0449 | False | 13.8 | 13.2 | 0.466 | False |
| vae_zseries | optimised selection | 13.6 | 12 | 15.2 | 0 | 0 | 0.0586 | True | 13.3 | 13.9 | 0.34 | False |
| timesfm | long-series generator | 14.4 | 12.6 | 16.2 | 0 | 0 | 0.172 | True | 15.2 | 13.6 | 0.106 | False |
| vae_quilting | optimised selection | 15.1 | 13.2 | 17 | 0 | 0 | 0.0586 | True | 15.5 | 14.7 | 0.125 | False |
| vae_atsp | optimised selection | 15.2 | 13.3 | 17.1 | 0 | 0 | 0.0586 | True | 15.1 | 15.3 | 0.153 | False |
| vae_pctsp | optimised selection | 15.3 | 13.7 | 16.8 | 0 | 0 | 0.0449 | False | 15 | 15.7 | 0.146 | False |
| vae_greedy | optimised selection | 15.6 | 13.9 | 17.3 | 0 | 0 | 0.0449 | False | 15.5 | 15.7 | 0.0733 | False |
| vae_knn | optimised selection | 16 | 14.1 | 17.9 | 0 | 0 | 0.0449 | False | 16.1 | 16 | 0.0861 | False |
| vae_mbb | optimised selection | 16.4 | 14 | 18.5 | 0 | 0 | 0.0449 | False | 16.4 | 16.3 | 0.0773 | False |
| chronos | long-series generator | 16.4 | 14.7 | 18.1 | 0 | 0 | 0.0938 | True | 17.7 | 15.2 | -0.125 | False |
| vae_rand | random selection | 16.4 | 14.2 | 18.6 | 0 | 0 | 0.0449 | False | 16.5 | 16.4 | 0 | False |
| timestral | long-series generator | 16.8 | 15.5 | 18.1 | 0 | 0 | 0.0449 | False | 17.3 | 16.2 | -0.443 | False |


Sensitivity variants:

| variant | text | first | tau_vs_main | main_first_place |
|---|---|---|---|---|
| main | the leaderboard: core metrics, fidelity against train + val + OOT, noise-aware ranks | zedge_quilting | 1 | 1 |
| plain_ranks | ordinary average ranks (no ties within the noise) | zedge_quilting | 0.957 | 1 |
| fidelity_train | fidelity against train only | zedge_zseries | 0.964 | 2 |
| fidelity_holdout | fidelity against val + OOT only | zedge_quilting | 0.964 | 1 |
| no_unchecked | without F5.7 (seams, no anchor) and F6.1 against val (noise) | zedge_quilting | 0.986 | 1 |
| all_metrics | every fidelity metric instead of the core set | zedge_quilting | 0.971 | 1 |
| common_datasets | only the datasets where every method is ranked | zedge_quilting | 0.949 | 1 |


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
| chronos | long-series generator | 16.4 | 0 | True | 13.9 | 0 | True | 17.6 | 0 | True | 15.1 | 0 | True |  |
| diffusion_ts | long-series generator | 13.8 | 0 | False | 12.2 | 0 | True | 14.5 | 0 | False | 13 | 0 | True |  |
| timesfm | long-series generator | 15.7 | 0 | True | 11.4 | 0.005 | True | 16.8 | 0 | True | 12.5 | 0 | True |  |
| timestral | long-series generator | 18.5 | 0 | False | 13.8 | 0 | True | 20.2 | 0 | False | 15.4 | 0 | True |  |
| zedge_ts_ar | long-series generator | 9.04 | 0.231 | True | 8.82 | 0.4 | True | 7.93 | 0.342 | True | 7.71 | 0.512 | True | train_reg |
| zedge_ts_long | long-series generator | 10 | 0 | True | 9.94 | 0 | True | 9.24 | 0 | True | 9.13 | 0 | True |  |
| vae_atsp | optimised selection | 14.8 | 0 | True | 15.2 | 0 | True | 15.5 | 0 | False | 15.9 | 0 | True |  |
| vae_greedy | optimised selection | 15.2 | 0 | True | 15.5 | 0 | True | 15.9 | 0 | True | 16.2 | 0 | True |  |
| vae_herding | optimised selection | 13.6 | 0 | False | 14.2 | 0 | False | 13.8 | 0 | False | 14.4 | 0 | False |  |
| vae_knn | optimised selection | 15.4 | 0 | True | 16 | 0 | True | 16.3 | 0 | False | 16.8 | 0 | True |  |
| vae_mbb | optimised selection | 15.6 | 0 | False | 16.5 | 0 | True | 16.5 | 0 | False | 17.4 | 0 | True |  |
| vae_pctsp | optimised selection | 14.9 | 0 | True | 15.4 | 0 | False | 15.7 | 0 | False | 16.2 | 0 | True |  |
| vae_quilting | optimised selection | 14.4 | 0 | True | 14.9 | 0 | True | 15 | 0 | True | 15.5 | 0 | True |  |
| vae_zseries | optimised selection | 13.5 | 0 | True | 13.5 | 0 | True | 13.9 | 0 | True | 14 | 0 | True |  |
| zedge_atsp | optimised selection | 9.37 | 0.002 | True | 9.77 | 0 | True | 8.4 | 0 | True | 8.8 | 0 | True |  |
| zedge_greedy | optimised selection | 9.16 | 0.008 | True | 9.36 | 0.004 | True | 8.09 | 0.047 | True | 8.29 | 0.015 | True |  |
| zedge_herding | optimised selection | 10.2 | 0 | True | 11.6 | 0 | True | 9.38 | 0 | True | 10.8 | 0 | False |  |
| zedge_knn | optimised selection | 9.46 | 0 | True | 10 | 0 | True | 8.55 | 0 | True | 9.13 | 0 | True |  |
| zedge_mbb | optimised selection | 10.2 | 0 | True | 11.9 | 0 | True | 9.42 | 0 | True | 11.2 | 0 | False |  |
| zedge_pctsp | optimised selection | 9.21 | 0.02 | True | 9.65 | 0 | True | 8.17 | 0.034 | True | 8.61 | 0.002 | True |  |
| zedge_quilting | optimised selection | 8.56 | 0.676 | True | 8.63 | 0.458 | True | 7.79 | 0.415 | True | 7.86 | 0.235 | True | holdout_clf, holdout_reg, train_clf |
| zedge_zseries | optimised selection | 9.26 | 0.063 | True | 9.12 | 0.133 | True | 8.2 | 0.162 | True | 8.07 | 0.236 | True |  |
| vae_rand | random selection | 15.5 | 0 | False | 16.5 | 0 | True | 16.4 | 0 | False | 17.4 | 0 | False |  |
| zedge_rand | random selection | 10.3 | 0 | True | 12 | 0 | True | 9.58 | 0 | True | 11.3 | 0 | False |  |


### Ranking `holdout_clf`: Fidelity: val + OOT; utility: classification

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| zedge_quilting | optimised selection | 8.56 | 7.44 | 9.76 | 0.676 | 0.953 |  | True |
| zedge_ts_ar | long-series generator | 9.04 | 7.17 | 11 | 0.231 | 0.598 | 0.41 | True |
| zedge_greedy | optimised selection | 9.16 | 8.25 | 10.2 | 0.008 | 0.462 | 0.41 | True |
| zedge_pctsp | optimised selection | 9.21 | 8.3 | 10.1 | 0.02 | 0.358 | 0.41 | True |
| zedge_zseries | optimised selection | 9.26 | 8.76 | 9.83 | 0.063 | 0.38 | 0.41 | True |
| zedge_atsp | optimised selection | 9.37 | 8.03 | 10.7 | 0.002 | 0.223 | 0.41 | True |
| zedge_knn | optimised selection | 9.46 | 8.65 | 10.4 | 0 | 0.025 | 0.293 | True |
| zedge_ts_long | long-series generator | 10 | 8.64 | 11.5 | 0 | 0.001 | 0.0977 | True |
| zedge_mbb | optimised selection | 10.2 | 9 | 11.4 | 0 | 0 | 0.0977 | True |
| zedge_herding | optimised selection | 10.2 | 9.25 | 11.2 | 0 | 0 | 0.0977 | True |
| zedge_rand | random selection | 10.3 | 9.13 | 11.5 | 0 | 0 | 0.0703 | True |
| vae_zseries | optimised selection | 13.5 | 12 | 15 | 0 | 0 | 0.0703 | True |
| vae_herding | optimised selection | 13.6 | 12.7 | 14.5 | 0 | 0 | 0.0449 | False |
| diffusion_ts | long-series generator | 13.8 | 11.8 | 15.4 | 0 | 0 | 0.0449 | False |
| vae_quilting | optimised selection | 14.4 | 12.8 | 16 | 0 | 0 | 0.0703 | True |
| vae_atsp | optimised selection | 14.8 | 13 | 16.5 | 0 | 0 | 0.0703 | True |
| vae_pctsp | optimised selection | 14.9 | 13.4 | 16.3 | 0 | 0 | 0.0703 | True |
| vae_greedy | optimised selection | 15.2 | 13.6 | 16.7 | 0 | 0 | 0.0703 | True |
| vae_knn | optimised selection | 15.4 | 13.5 | 17.2 | 0 | 0 | 0.0703 | True |
| vae_rand | random selection | 15.5 | 13.5 | 17.5 | 0 | 0 | 0.0449 | False |
| vae_mbb | optimised selection | 15.6 | 13.5 | 17.5 | 0 | 0 | 0.0449 | False |
| timesfm | long-series generator | 15.7 | 13.2 | 18.2 | 0 | 0 | 0.109 | True |
| chronos | long-series generator | 16.4 | 14.2 | 18.2 | 0 | 0 | 0.0859 | True |
| timestral | long-series generator | 18.5 | 16.9 | 20 | 0 | 0 | 0.0449 | False |


### Ranking `holdout_reg`: Fidelity: val + OOT; utility: regression

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| zedge_quilting | optimised selection | 8.63 | 7.51 | 9.73 | 0.458 | 0.919 |  | True |
| zedge_ts_ar | long-series generator | 8.82 | 6.67 | 11.1 | 0.4 | 0.813 | 0.539 | True |
| zedge_zseries | optimised selection | 9.12 | 8.15 | 10 | 0.133 | 0.598 | 0.539 | True |
| zedge_greedy | optimised selection | 9.36 | 8.22 | 10.5 | 0.004 | 0.344 | 0.41 | True |
| zedge_pctsp | optimised selection | 9.65 | 8.34 | 10.9 | 0 | 0.075 | 0.223 | True |
| zedge_atsp | optimised selection | 9.77 | 7.89 | 11.8 | 0 | 0.162 | 0.539 | True |
| zedge_ts_long | long-series generator | 9.94 | 8.29 | 11.7 | 0 | 0.054 | 0.41 | True |
| zedge_knn | optimised selection | 10 | 8.78 | 11.4 | 0 | 0.001 | 0.156 | True |
| timesfm | long-series generator | 11.4 | 9.05 | 13.5 | 0.005 | 0.034 | 0.219 | True |
| zedge_herding | optimised selection | 11.6 | 9.71 | 13.5 | 0 | 0 | 0.107 | True |
| zedge_mbb | optimised selection | 11.9 | 9.97 | 14 | 0 | 0 | 0.107 | True |
| zedge_rand | random selection | 12 | 10 | 14.1 | 0 | 0 | 0.082 | True |
| diffusion_ts | long-series generator | 12.2 | 10.6 | 13.7 | 0 | 0 | 0.082 | True |
| vae_zseries | optimised selection | 13.5 | 11.8 | 15.2 | 0 | 0 | 0.107 | True |
| timestral | long-series generator | 13.8 | 12.1 | 15.7 | 0 | 0 | 0.082 | True |
| chronos | long-series generator | 13.9 | 12 | 15.9 | 0 | 0 | 0.0938 | True |
| vae_herding | optimised selection | 14.2 | 13.2 | 15.3 | 0 | 0 | 0.0449 | False |
| vae_quilting | optimised selection | 14.9 | 12.8 | 17 | 0 | 0 | 0.082 | True |
| vae_atsp | optimised selection | 15.2 | 13 | 17.2 | 0 | 0 | 0.082 | True |
| vae_pctsp | optimised selection | 15.4 | 13.6 | 17 | 0 | 0 | 0.0449 | False |
| vae_greedy | optimised selection | 15.5 | 13.6 | 17.4 | 0 | 0 | 0.082 | True |
| vae_knn | optimised selection | 16 | 13.6 | 18.2 | 0 | 0 | 0.082 | True |
| vae_mbb | optimised selection | 16.5 | 14 | 18.7 | 0 | 0 | 0.082 | True |
| vae_rand | random selection | 16.5 | 14.1 | 18.8 | 0 | 0 | 0.082 | True |


### Ranking `train_clf`: Fidelity: train; utility: classification

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| zedge_quilting | optimised selection | 7.79 | 6.52 | 9.19 | 0.415 | 0.807 |  | True |
| zedge_ts_ar | long-series generator | 7.93 | 6.23 | 9.7 | 0.342 | 0.639 | 0.992 | True |
| zedge_greedy | optimised selection | 8.09 | 7.44 | 8.9 | 0.047 | 0.549 | 0.992 | True |
| zedge_pctsp | optimised selection | 8.17 | 7.4 | 8.93 | 0.034 | 0.43 | 0.992 | True |
| zedge_zseries | optimised selection | 8.2 | 7.6 | 8.76 | 0.162 | 0.416 | 0.992 | True |
| zedge_atsp | optimised selection | 8.4 | 7.3 | 9.53 | 0 | 0.133 | 0.609 | True |
| zedge_knn | optimised selection | 8.55 | 8.01 | 9.24 | 0 | 0.026 | 0.609 | True |
| zedge_ts_long | long-series generator | 9.24 | 8.09 | 10.4 | 0 | 0 | 0.107 | True |
| zedge_herding | optimised selection | 9.38 | 8.57 | 10.2 | 0 | 0 | 0.297 | True |
| zedge_mbb | optimised selection | 9.42 | 8.55 | 10.3 | 0 | 0 | 0.297 | True |
| zedge_rand | random selection | 9.58 | 8.69 | 10.4 | 0 | 0 | 0.107 | True |
| vae_herding | optimised selection | 13.8 | 13 | 14.6 | 0 | 0 | 0.0449 | False |
| vae_zseries | optimised selection | 13.9 | 12.6 | 15.3 | 0 | 0 | 0.0586 | True |
| diffusion_ts | long-series generator | 14.5 | 12.6 | 16.1 | 0 | 0 | 0.0449 | False |
| vae_quilting | optimised selection | 15 | 13.5 | 16.5 | 0 | 0 | 0.0586 | True |
| vae_atsp | optimised selection | 15.5 | 14.1 | 16.9 | 0 | 0 | 0.0449 | False |
| vae_pctsp | optimised selection | 15.7 | 14.4 | 16.9 | 0 | 0 | 0.0449 | False |
| vae_greedy | optimised selection | 15.9 | 14.5 | 17.2 | 0 | 0 | 0.0586 | True |
| vae_knn | optimised selection | 16.3 | 14.9 | 17.6 | 0 | 0 | 0.0449 | False |
| vae_rand | random selection | 16.4 | 15 | 17.8 | 0 | 0 | 0.0449 | False |
| vae_mbb | optimised selection | 16.5 | 14.9 | 17.9 | 0 | 0 | 0.0449 | False |
| timesfm | long-series generator | 16.8 | 14.2 | 19.4 | 0 | 0 | 0.141 | True |
| chronos | long-series generator | 17.6 | 15.6 | 19.3 | 0 | 0 | 0.0938 | True |
| timestral | long-series generator | 20.2 | 18.4 | 21.7 | 0 | 0 | 0.0449 | False |


### Ranking `train_reg`: Fidelity: train; utility: regression

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| zedge_ts_ar | long-series generator | 7.71 | 5.74 | 9.82 | 0.512 | 0.83 |  | True |
| zedge_quilting | optimised selection | 7.86 | 6.68 | 9.11 | 0.235 | 0.838 | 0.82 | True |
| zedge_zseries | optimised selection | 8.07 | 7.22 | 8.85 | 0.236 | 0.62 | 0.82 | True |
| zedge_greedy | optimised selection | 8.29 | 7.45 | 9.15 | 0.015 | 0.457 | 0.744 | True |
| zedge_pctsp | optimised selection | 8.61 | 7.5 | 9.65 | 0.002 | 0.086 | 0.5 | True |
| zedge_atsp | optimised selection | 8.8 | 7.19 | 10.5 | 0 | 0.142 | 0.137 | True |
| zedge_ts_long | long-series generator | 9.13 | 7.8 | 10.6 | 0 | 0.026 | 0.137 | True |
| zedge_knn | optimised selection | 9.13 | 8.18 | 10.2 | 0 | 0.001 | 0.137 | True |
| zedge_herding | optimised selection | 10.8 | 9.12 | 12.4 | 0 | 0 | 0.0449 | False |
| zedge_mbb | optimised selection | 11.2 | 9.56 | 12.8 | 0 | 0 | 0.0449 | False |
| zedge_rand | random selection | 11.3 | 9.66 | 12.9 | 0 | 0 | 0.0449 | False |
| timesfm | long-series generator | 12.5 | 10.2 | 14.5 | 0 | 0 | 0.137 | True |
| diffusion_ts | long-series generator | 13 | 11.6 | 14.3 | 0 | 0 | 0.0703 | True |
| vae_zseries | optimised selection | 14 | 12.5 | 15.5 | 0 | 0 | 0.137 | True |
| vae_herding | optimised selection | 14.4 | 13.5 | 15.3 | 0 | 0 | 0.0449 | False |
| chronos | long-series generator | 15.1 | 13.5 | 16.7 | 0 | 0 | 0.137 | True |
| timestral | long-series generator | 15.4 | 13.8 | 17.1 | 0 | 0 | 0.0703 | True |
| vae_quilting | optimised selection | 15.5 | 13.5 | 17.5 | 0 | 0 | 0.107 | True |
| vae_atsp | optimised selection | 15.9 | 14.2 | 17.6 | 0 | 0 | 0.0703 | True |
| vae_greedy | optimised selection | 16.2 | 14.5 | 17.7 | 0 | 0 | 0.0703 | True |
| vae_pctsp | optimised selection | 16.2 | 14.7 | 17.6 | 0 | 0 | 0.0703 | True |
| vae_knn | optimised selection | 16.8 | 15 | 18.5 | 0 | 0 | 0.0703 | True |
| vae_mbb | optimised selection | 17.4 | 15.4 | 19.1 | 0 | 0 | 0.0703 | True |
| vae_rand | random selection | 17.4 | 15.5 | 19.2 | 0 | 0 | 0.0449 | False |



## Core-metric rankings (RQ1)

The four rankings with the fidelity domain restricted to the core metric set, fixed in advance: distribution (F1.2_w1, F2.1_ks_d24); dependence (F3.5_log_psd, F4.1_how_mean); windows (F6.1_disc_score, F6.4_mmd); long structure (F7.1_roll_mean_ks, F7.2_roll_std_ks); target (F11.1_class_share_logratio); seams (F5.7_seam_detect_auc_dev). Utility unchanged. Each core ranking, the normalised scores (random assembly = 0, real data = 1) and the anchor check — `LEADERBOARD.md`.

| method | family | core_holdout_clf:rank | core_holdout_clf:p_first | core_holdout_clf:tier | core_holdout_reg:rank | core_holdout_reg:p_first | core_holdout_reg:tier | core_train_clf:rank | core_train_clf:p_first | core_train_clf:tier | core_train_reg:rank | core_train_reg:p_first | core_train_reg:tier | first_in |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| chronos | long-series generator | 17.1 | 0 | True | 14.7 | 0 | True | 18.8 | 0 | True | 16.4 | 0 | True |  |
| diffusion_ts | long-series generator | 13.9 | 0 | False | 12.4 | 0 | True | 15.2 | 0 | False | 13.7 | 0 | True |  |
| timesfm | long-series generator | 16 | 0 | True | 11.7 | 0 | True | 17.6 | 0 | True | 13.3 | 0 | True |  |
| timestral | long-series generator | 18.4 | 0 | False | 13.6 | 0 | True | 20.9 | 0 | False | 16.1 | 0 | False |  |
| zedge_ts_ar | long-series generator | 8.82 | 0.247 | True | 8.6 | 0.367 | True | 7.73 | 0.269 | True | 7.51 | 0.378 | True |  |
| zedge_ts_long | long-series generator | 9.61 | 0 | True | 9.51 | 0.001 | True | 8.78 | 0 | True | 8.67 | 0 | True |  |
| vae_atsp | optimised selection | 14.9 | 0 | True | 15.4 | 0 | True | 15.8 | 0 | False | 16.2 | 0 | False |  |
| vae_greedy | optimised selection | 15.3 | 0 | True | 15.7 | 0 | True | 16.1 | 0 | False | 16.5 | 0 | False |  |
| vae_herding | optimised selection | 13.6 | 0 | False | 14.2 | 0 | False | 13.3 | 0 | False | 13.9 | 0 | False |  |
| vae_knn | optimised selection | 15.7 | 0 | False | 16.3 | 0 | True | 16.7 | 0 | False | 17.2 | 0 | False |  |
| vae_mbb | optimised selection | 15.9 | 0 | True | 16.8 | 0 | True | 16.9 | 0 | False | 17.8 | 0 | False |  |
| vae_pctsp | optimised selection | 14.8 | 0 | True | 15.4 | 0 | False | 15.8 | 0 | False | 16.4 | 0 | False |  |
| vae_quilting | optimised selection | 14.6 | 0 | True | 15.2 | 0 | True | 15.3 | 0 | True | 15.9 | 0 | True |  |
| vae_zseries | optimised selection | 13.5 | 0 | True | 13.5 | 0 | True | 14 | 0 | True | 14 | 0 | False |  |
| zedge_atsp | optimised selection | 9.22 | 0.006 | True | 9.62 | 0.001 | True | 8.02 | 0.01 | True | 8.42 | 0.001 | True |  |
| zedge_greedy | optimised selection | 9.05 | 0.001 | True | 9.25 | 0.001 | True | 7.75 | 0.012 | True | 7.94 | 0.007 | True |  |
| zedge_herding | optimised selection | 9.91 | 0 | True | 11.3 | 0 | True | 8.71 | 0 | True | 10.1 | 0 | True |  |
| zedge_knn | optimised selection | 9.29 | 0 | True | 9.88 | 0 | True | 8.05 | 0 | True | 8.63 | 0.001 | True |  |
| zedge_mbb | optimised selection | 10 | 0 | True | 11.8 | 0 | True | 9.06 | 0 | True | 10.8 | 0 | True |  |
| zedge_pctsp | optimised selection | 9.07 | 0.006 | True | 9.5 | 0 | True | 7.64 | 0.047 | True | 8.07 | 0.003 | True |  |
| zedge_quilting | optimised selection | 8.25 | 0.67 | True | 8.32 | 0.494 | True | 7.47 | 0.325 | True | 7.54 | 0.232 | True | core_holdout_clf, core_holdout_reg, core_train_clf |
| zedge_zseries | optimised selection | 9.02 | 0.07 | True | 8.88 | 0.136 | True | 7.5 | 0.337 | True | 7.37 | 0.378 | True | core_train_reg |
| vae_rand | random selection | 15.9 | 0 | True | 16.9 | 0 | True | 16.9 | 0 | False | 17.8 | 0 | False |  |
| zedge_rand | random selection | 10.2 | 0 | True | 11.9 | 0 | True | 9.15 | 0 | True | 10.8 | 0 | True |  |


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
| RQ0. Benchmark validity: noise, real-data ceiling, discriminative power and redundancy of the metrics | discriminative metrics: 210 of 276 |
| RQ1. Ranking of every method in every slice | first by ranking: holdout_clf — zedge_quilting (Friedman p = 1.21e-11); holdout_reg — zedge_quilting (Friedman p = 5.37e-08); train_clf — zedge_quilting (Friedman p = 1.46e-20); train_reg — zedge_ts_ar (Friedman p = 1.23e-16) |
| RQ2. Assembly from a window pool vs long-series generators | inconclusive: 2420 |
| RQ3. Within assembly: window selection × seam processing | same: 459, inconclusive: 2369 |
| RQ4. Does fidelity predict utility (which metrics, against which reference) | predictive pairs: 364 of 872 |
| RQ5. Gap to real data (TSTR / TRTR), stability over time and across models | worse than real: 120 |
| RQ6. Speed and cost: training and generation time, memory, Pareto front "quality × time" | fastest: timestral (1 s) |
| RQ7. Moderators: dataset descriptors and the effects of RQ2 / RQ3 (exploratory) | significant after BH: 0 of 176 |
| RQ8. Class balance: do methods preserve class shares (rare events especially) and what does an error cost | inconclusive: 647 |
| RQ9. Outliers and extremes: do methods preserve tails and outliers, and does it matter to the models | inconclusive: 782 |

## Research questions

### RQ0. Benchmark validity: noise, real-data ceiling, discriminative power and redundancy of the metrics

| unit | kind | group | reference | n_datasets | n_methods | p_friedman | spread_over_noise | p_friedman_bh | discriminative |
|---|---|---|---|---|---|---|---|---|---|
| F1.10_hill_err | fidelity | F1_marginal | val | 9 | 28 | 0.283 | 3.47 | 0.324 | False |
| F1.10_hill_err@oot | fidelity | F1_marginal | oot | 9 | 28 | 0.0737 | 2.74 | 0.0921 | False |
| F1.10_hill_err@train | fidelity | F1_marginal | train | 9 | 28 | 1.55e-18 | 3.5 | 1.23e-17 | True |
| F1.1_ks | fidelity | F1_marginal | val | 9 | 28 | 0.0259 | 7.79 | 0.034 | True |
| F1.1_ks@oot | fidelity | F1_marginal | oot | 9 | 28 | 5.22e-05 | 10.8 | 8.78e-05 | True |
| F1.1_ks@train | fidelity | F1_marginal | train | 9 | 28 | 6.05e-28 | 8.38 | 4.18e-26 | True |
| F1.2_w1 | fidelity | F1_marginal | val | 9 | 28 | 0.0271 | 12.5 | 0.0354 | True |
| F1.2_w1@oot | fidelity | F1_marginal | oot | 9 | 28 | 0.000505 | 12.5 | 0.000788 | True |
| F1.2_w1@train | fidelity | F1_marginal | train | 9 | 28 | 9.74e-29 | 11.7 | 8.96e-27 | True |
| F1.3_ad | fidelity | F1_marginal | val | 9 | 28 | 0.0113 | 5.71 | 0.0155 | True |
| F1.3_ad@oot | fidelity | F1_marginal | oot | 9 | 28 | 5e-06 | 10 | 8.96e-06 | True |
| F1.3_ad@train | fidelity | F1_marginal | train | 9 | 28 | 8.62e-30 | 7.76 | 1.19e-27 | True |
| F1.4_qq_corr | fidelity | F1_marginal | val | 9 | 28 | 0.0136 | 1.49 | 0.0184 | True |
| F1.4_qq_corr@oot | fidelity | F1_marginal | oot | 9 | 28 | 8.82e-15 | 2.04 | 4.35e-14 | True |
| F1.4_qq_corr@train | fidelity | F1_marginal | train | 9 | 28 | 9.43e-17 | 3.49 | 5.78e-16 | True |
| F1.5_q01_err | fidelity | F1_marginal | val | 9 | 28 | 0.0749 | 8.72 | 0.0931 | False |
| F1.5_q01_err@oot | fidelity | F1_marginal | oot | 9 | 28 | 0.0173 | 10.7 | 0.0233 | True |
| F1.5_q01_err@train | fidelity | F1_marginal | train | 9 | 28 | 5.12e-12 | 8.72 | 1.81e-11 | True |
| F1.5_q99_err | fidelity | F1_marginal | val | 9 | 28 | 0.555 | 7.16 | 0.603 | False |
| F1.5_q99_err@oot | fidelity | F1_marginal | oot | 9 | 28 | 0.58 | 3.61 | 0.623 | False |
| F1.5_q99_err@train | fidelity | F1_marginal | train | 9 | 28 | 2.79e-14 | 5.67 | 1.28e-13 | True |
| F1.5_quantile_err | fidelity | F1_marginal | val | 9 | 28 | 0.0274 | 9.68 | 0.0357 | True |
| F1.5_quantile_err@oot | fidelity | F1_marginal | oot | 9 | 28 | 0.00102 | 10.3 | 0.00153 | True |
| F1.5_quantile_err@train | fidelity | F1_marginal | train | 9 | 28 | 1.43e-27 | 9.43 | 7.88e-26 | True |
| F1.6_kurt_err | fidelity | F1_marginal | val | 9 | 28 | 0.953 | 2.2 | 0.971 | False |
| F1.6_kurt_err@oot | fidelity | F1_marginal | oot | 9 | 28 | 0.175 | 2.16 | 0.204 | False |
| F1.6_kurt_err@train | fidelity | F1_marginal | train | 9 | 28 | 5.9e-20 | 2.93 | 5.25e-19 | True |
| F1.6_mean_err | fidelity | F1_marginal | val | 9 | 28 | 0.0776 | 12.5 | 0.0957 | False |
| F1.6_mean_err@oot | fidelity | F1_marginal | oot | 9 | 28 | 0.000426 | 12.5 | 0.000671 | True |
| F1.6_mean_err@train | fidelity | F1_marginal | train | 9 | 28 | 1.35e-25 | 9.92 | 4.13e-24 | True |
| F1.6_skew_err | fidelity | F1_marginal | val | 9 | 28 | 0.107 | 2.53 | 0.13 | False |
| F1.6_skew_err@oot | fidelity | F1_marginal | oot | 9 | 28 | 0.0126 | 3.38 | 0.0171 | True |
| F1.6_skew_err@train | fidelity | F1_marginal | train | 9 | 28 | 1.17e-12 | 3.46 | 4.55e-12 | True |
| F1.6_std_err | fidelity | F1_marginal | val | 9 | 28 | 0.842 | 2.89 | 0.877 | False |
| F1.6_std_err@oot | fidelity | F1_marginal | oot | 9 | 28 | 0.555 | 2.89 | 0.603 | False |
| F1.6_std_err@train | fidelity | F1_marginal | train | 9 | 28 | 3.43e-10 | 2.77 | 9.75e-10 | True |
| F1.7_out_of_range | fidelity | F1_marginal | val | 9 | 28 | 0.573 | 4.33 | 0.618 | False |
| F1.7_out_of_range@oot | fidelity | F1_marginal | oot | 9 | 28 | 5.68e-17 | 2.04 | 3.56e-16 | True |
| F1.7_out_of_range@train | fidelity | F1_marginal | train | 9 | 28 | 0.519 |  | 0.576 | False |
| F1.8_coverage | fidelity | F1_marginal | val | 9 | 28 | 2.64e-09 | 4.46 | 6.38e-09 | True |

_Showing 40 rows of 276; all of them — `hypotheses/RQ0_global.parquet`._

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
| fidelity | F5_seams | 0 | 1 | 1 |
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
| ranking:holdout_clf | 1.21e-11 | 11 | 9 | 22 | zedge_quilting |
| with_cost:holdout_clf | 2.79e-11 | 11 | 9 | 22 | zedge_quilting |
| ranking:holdout_reg | 5.37e-08 | 11 | 9 | 22 | zedge_quilting |
| with_cost:holdout_reg | 6.55e-08 | 11 | 9 | 22 | zedge_quilting |
| ranking:train_clf | 1.46e-20 | 11 | 9 | 22 | zedge_quilting |
| with_cost:train_clf | 2.76e-20 | 11 | 9 | 22 | zedge_quilting |
| ranking:train_reg | 1.23e-16 | 11 | 9 | 22 | zedge_ts_ar |
| with_cost:train_reg | 3.5e-14 | 11 | 9 | 22 | zedge_quilting |
| ranking:core_holdout_clf | 3.93e-09 | 11 | 9 | 22 | zedge_quilting |
| ranking:core_holdout_reg | 9.8e-07 | 11 | 9 | 22 | zedge_quilting |
| ranking:core_train_clf | 6.21e-21 | 11 | 9 | 22 | zedge_quilting |
| ranking:core_train_reg | 5.64e-17 | 11 | 9 | 22 | zedge_zseries |
| domain:fidelity@train | 1.17e-21 | 11 | 9 | 22 | zedge_ts_ar |
| domain:fidelity@val | 0.0126 | 11 | 9 | 22 | zedge_ts_ar |
| domain:fidelity@oot | 3.47e-08 | 11 | 9 | 22 | zedge_quilting |
| domain:fidelity@all | 3.7e-13 | 11 | 9 | 22 | zedge_quilting |
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
| fidelity:seams@oot | 0.0497 | 11 | 9 | 22 | zedge_atsp |
| fidelity:seams@train | 0.00084 | 11 | 9 | 22 | zedge_ts_ar |
| fidelity:seams@val | 0.0102 | 11 | 9 | 22 | zedge_ts_ar |
| fidelity:target@oot | 1.96e-09 | 11 | 9 | 22 | zedge_quilting |
| fidelity:target@train | 1.17e-19 | 11 | 9 | 22 | zedge_zseries |
| fidelity:target@val | 1.2e-09 | 11 | 9 | 22 | zedge_atsp |
| fidelity:windows@oot | 1.01e-05 | 11 | 9 | 22 | zedge_quilting |

_Showing 40 rows of 56; all of them — `hypotheses/RQ1_global.parquet`._

**ranking_holdout_clf**

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| zedge_quilting | optimised selection | 8.56 | 7.44 | 9.76 | 0.676 | 0.953 |  | True |
| zedge_ts_ar | long-series generator | 9.04 | 7.17 | 11 | 0.231 | 0.598 | 0.41 | True |
| zedge_greedy | optimised selection | 9.16 | 8.25 | 10.2 | 0.008 | 0.462 | 0.41 | True |
| zedge_pctsp | optimised selection | 9.21 | 8.3 | 10.1 | 0.02 | 0.358 | 0.41 | True |
| zedge_zseries | optimised selection | 9.26 | 8.76 | 9.83 | 0.063 | 0.38 | 0.41 | True |
| zedge_atsp | optimised selection | 9.37 | 8.03 | 10.7 | 0.002 | 0.223 | 0.41 | True |
| zedge_knn | optimised selection | 9.46 | 8.65 | 10.4 | 0 | 0.025 | 0.293 | True |
| zedge_ts_long | long-series generator | 10 | 8.64 | 11.5 | 0 | 0.001 | 0.0977 | True |
| zedge_mbb | optimised selection | 10.2 | 9 | 11.4 | 0 | 0 | 0.0977 | True |
| zedge_herding | optimised selection | 10.2 | 9.25 | 11.2 | 0 | 0 | 0.0977 | True |
| zedge_rand | random selection | 10.3 | 9.13 | 11.5 | 0 | 0 | 0.0703 | True |
| vae_zseries | optimised selection | 13.5 | 12 | 15 | 0 | 0 | 0.0703 | True |
| vae_herding | optimised selection | 13.6 | 12.7 | 14.5 | 0 | 0 | 0.0449 | False |
| diffusion_ts | long-series generator | 13.8 | 11.8 | 15.4 | 0 | 0 | 0.0449 | False |
| vae_quilting | optimised selection | 14.4 | 12.8 | 16 | 0 | 0 | 0.0703 | True |
| vae_atsp | optimised selection | 14.8 | 13 | 16.5 | 0 | 0 | 0.0703 | True |
| vae_pctsp | optimised selection | 14.9 | 13.4 | 16.3 | 0 | 0 | 0.0703 | True |
| vae_greedy | optimised selection | 15.2 | 13.6 | 16.7 | 0 | 0 | 0.0703 | True |
| vae_knn | optimised selection | 15.4 | 13.5 | 17.2 | 0 | 0 | 0.0703 | True |
| vae_rand | random selection | 15.5 | 13.5 | 17.5 | 0 | 0 | 0.0449 | False |
| vae_mbb | optimised selection | 15.6 | 13.5 | 17.5 | 0 | 0 | 0.0449 | False |
| timesfm | long-series generator | 15.7 | 13.2 | 18.2 | 0 | 0 | 0.109 | True |
| chronos | long-series generator | 16.4 | 14.2 | 18.2 | 0 | 0 | 0.0859 | True |
| timestral | long-series generator | 18.5 | 16.9 | 20 | 0 | 0 | 0.0449 | False |


**ranking_holdout_reg**

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| zedge_quilting | optimised selection | 8.63 | 7.51 | 9.73 | 0.458 | 0.919 |  | True |
| zedge_ts_ar | long-series generator | 8.82 | 6.67 | 11.1 | 0.4 | 0.813 | 0.539 | True |
| zedge_zseries | optimised selection | 9.12 | 8.15 | 10 | 0.133 | 0.598 | 0.539 | True |
| zedge_greedy | optimised selection | 9.36 | 8.22 | 10.5 | 0.004 | 0.344 | 0.41 | True |
| zedge_pctsp | optimised selection | 9.65 | 8.34 | 10.9 | 0 | 0.075 | 0.223 | True |
| zedge_atsp | optimised selection | 9.77 | 7.89 | 11.8 | 0 | 0.162 | 0.539 | True |
| zedge_ts_long | long-series generator | 9.94 | 8.29 | 11.7 | 0 | 0.054 | 0.41 | True |
| zedge_knn | optimised selection | 10 | 8.78 | 11.4 | 0 | 0.001 | 0.156 | True |
| timesfm | long-series generator | 11.4 | 9.05 | 13.5 | 0.005 | 0.034 | 0.219 | True |
| zedge_herding | optimised selection | 11.6 | 9.71 | 13.5 | 0 | 0 | 0.107 | True |
| zedge_mbb | optimised selection | 11.9 | 9.97 | 14 | 0 | 0 | 0.107 | True |
| zedge_rand | random selection | 12 | 10 | 14.1 | 0 | 0 | 0.082 | True |
| diffusion_ts | long-series generator | 12.2 | 10.6 | 13.7 | 0 | 0 | 0.082 | True |
| vae_zseries | optimised selection | 13.5 | 11.8 | 15.2 | 0 | 0 | 0.107 | True |
| timestral | long-series generator | 13.8 | 12.1 | 15.7 | 0 | 0 | 0.082 | True |
| chronos | long-series generator | 13.9 | 12 | 15.9 | 0 | 0 | 0.0938 | True |
| vae_herding | optimised selection | 14.2 | 13.2 | 15.3 | 0 | 0 | 0.0449 | False |
| vae_quilting | optimised selection | 14.9 | 12.8 | 17 | 0 | 0 | 0.082 | True |
| vae_atsp | optimised selection | 15.2 | 13 | 17.2 | 0 | 0 | 0.082 | True |
| vae_pctsp | optimised selection | 15.4 | 13.6 | 17 | 0 | 0 | 0.0449 | False |
| vae_greedy | optimised selection | 15.5 | 13.6 | 17.4 | 0 | 0 | 0.082 | True |
| vae_knn | optimised selection | 16 | 13.6 | 18.2 | 0 | 0 | 0.082 | True |
| vae_mbb | optimised selection | 16.5 | 14 | 18.7 | 0 | 0 | 0.082 | True |
| vae_rand | random selection | 16.5 | 14.1 | 18.8 | 0 | 0 | 0.082 | True |


**ranking_train_clf**

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| zedge_quilting | optimised selection | 7.79 | 6.52 | 9.19 | 0.415 | 0.807 |  | True |
| zedge_ts_ar | long-series generator | 7.93 | 6.23 | 9.7 | 0.342 | 0.639 | 0.992 | True |
| zedge_greedy | optimised selection | 8.09 | 7.44 | 8.9 | 0.047 | 0.549 | 0.992 | True |
| zedge_pctsp | optimised selection | 8.17 | 7.4 | 8.93 | 0.034 | 0.43 | 0.992 | True |
| zedge_zseries | optimised selection | 8.2 | 7.6 | 8.76 | 0.162 | 0.416 | 0.992 | True |
| zedge_atsp | optimised selection | 8.4 | 7.3 | 9.53 | 0 | 0.133 | 0.609 | True |
| zedge_knn | optimised selection | 8.55 | 8.01 | 9.24 | 0 | 0.026 | 0.609 | True |
| zedge_ts_long | long-series generator | 9.24 | 8.09 | 10.4 | 0 | 0 | 0.107 | True |
| zedge_herding | optimised selection | 9.38 | 8.57 | 10.2 | 0 | 0 | 0.297 | True |
| zedge_mbb | optimised selection | 9.42 | 8.55 | 10.3 | 0 | 0 | 0.297 | True |
| zedge_rand | random selection | 9.58 | 8.69 | 10.4 | 0 | 0 | 0.107 | True |
| vae_herding | optimised selection | 13.8 | 13 | 14.6 | 0 | 0 | 0.0449 | False |
| vae_zseries | optimised selection | 13.9 | 12.6 | 15.3 | 0 | 0 | 0.0586 | True |
| diffusion_ts | long-series generator | 14.5 | 12.6 | 16.1 | 0 | 0 | 0.0449 | False |
| vae_quilting | optimised selection | 15 | 13.5 | 16.5 | 0 | 0 | 0.0586 | True |
| vae_atsp | optimised selection | 15.5 | 14.1 | 16.9 | 0 | 0 | 0.0449 | False |
| vae_pctsp | optimised selection | 15.7 | 14.4 | 16.9 | 0 | 0 | 0.0449 | False |
| vae_greedy | optimised selection | 15.9 | 14.5 | 17.2 | 0 | 0 | 0.0586 | True |
| vae_knn | optimised selection | 16.3 | 14.9 | 17.6 | 0 | 0 | 0.0449 | False |
| vae_rand | random selection | 16.4 | 15 | 17.8 | 0 | 0 | 0.0449 | False |
| vae_mbb | optimised selection | 16.5 | 14.9 | 17.9 | 0 | 0 | 0.0449 | False |
| timesfm | long-series generator | 16.8 | 14.2 | 19.4 | 0 | 0 | 0.141 | True |
| chronos | long-series generator | 17.6 | 15.6 | 19.3 | 0 | 0 | 0.0938 | True |
| timestral | long-series generator | 20.2 | 18.4 | 21.7 | 0 | 0 | 0.0449 | False |


**ranking_train_reg**

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| zedge_ts_ar | long-series generator | 7.71 | 5.74 | 9.82 | 0.512 | 0.83 |  | True |
| zedge_quilting | optimised selection | 7.86 | 6.68 | 9.11 | 0.235 | 0.838 | 0.82 | True |
| zedge_zseries | optimised selection | 8.07 | 7.22 | 8.85 | 0.236 | 0.62 | 0.82 | True |
| zedge_greedy | optimised selection | 8.29 | 7.45 | 9.15 | 0.015 | 0.457 | 0.744 | True |
| zedge_pctsp | optimised selection | 8.61 | 7.5 | 9.65 | 0.002 | 0.086 | 0.5 | True |
| zedge_atsp | optimised selection | 8.8 | 7.19 | 10.5 | 0 | 0.142 | 0.137 | True |
| zedge_ts_long | long-series generator | 9.13 | 7.8 | 10.6 | 0 | 0.026 | 0.137 | True |
| zedge_knn | optimised selection | 9.13 | 8.18 | 10.2 | 0 | 0.001 | 0.137 | True |
| zedge_herding | optimised selection | 10.8 | 9.12 | 12.4 | 0 | 0 | 0.0449 | False |
| zedge_mbb | optimised selection | 11.2 | 9.56 | 12.8 | 0 | 0 | 0.0449 | False |
| zedge_rand | random selection | 11.3 | 9.66 | 12.9 | 0 | 0 | 0.0449 | False |
| timesfm | long-series generator | 12.5 | 10.2 | 14.5 | 0 | 0 | 0.137 | True |
| diffusion_ts | long-series generator | 13 | 11.6 | 14.3 | 0 | 0 | 0.0703 | True |
| vae_zseries | optimised selection | 14 | 12.5 | 15.5 | 0 | 0 | 0.137 | True |
| vae_herding | optimised selection | 14.4 | 13.5 | 15.3 | 0 | 0 | 0.0449 | False |
| chronos | long-series generator | 15.1 | 13.5 | 16.7 | 0 | 0 | 0.137 | True |
| timestral | long-series generator | 15.4 | 13.8 | 17.1 | 0 | 0 | 0.0703 | True |
| vae_quilting | optimised selection | 15.5 | 13.5 | 17.5 | 0 | 0 | 0.107 | True |
| vae_atsp | optimised selection | 15.9 | 14.2 | 17.6 | 0 | 0 | 0.0703 | True |
| vae_greedy | optimised selection | 16.2 | 14.5 | 17.7 | 0 | 0 | 0.0703 | True |
| vae_pctsp | optimised selection | 16.2 | 14.7 | 17.6 | 0 | 0 | 0.0703 | True |
| vae_knn | optimised selection | 16.8 | 15 | 18.5 | 0 | 0 | 0.0703 | True |
| vae_mbb | optimised selection | 17.4 | 15.4 | 19.1 | 0 | 0 | 0.0703 | True |
| vae_rand | random selection | 17.4 | 15.5 | 19.2 | 0 | 0 | 0.0449 | False |


**ranking_core_holdout_clf**

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| zedge_quilting | optimised selection | 8.25 | 6.97 | 9.5 | 0.67 | 0.931 |  | True |
| zedge_ts_ar | long-series generator | 8.82 | 6.65 | 11 | 0.247 | 0.608 | 0.439 | True |
| zedge_zseries | optimised selection | 9.02 | 8.23 | 9.84 | 0.07 | 0.442 | 0.439 | True |
| zedge_greedy | optimised selection | 9.05 | 7.89 | 10.3 | 0.001 | 0.362 | 0.439 | True |
| zedge_pctsp | optimised selection | 9.07 | 7.92 | 10.3 | 0.006 | 0.318 | 0.439 | True |
| zedge_atsp | optimised selection | 9.22 | 7.58 | 10.9 | 0.006 | 0.214 | 0.439 | True |
| zedge_knn | optimised selection | 9.29 | 8.25 | 10.5 | 0 | 0.071 | 0.439 | True |
| zedge_ts_long | long-series generator | 9.61 | 7.92 | 11.4 | 0 | 0.049 | 0.439 | True |
| zedge_herding | optimised selection | 9.91 | 8.89 | 11 | 0 | 0.001 | 0.195 | True |
| zedge_mbb | optimised selection | 10 | 8.63 | 11.5 | 0 | 0.001 | 0.439 | True |
| zedge_rand | random selection | 10.2 | 8.69 | 11.7 | 0 | 0.003 | 0.439 | True |
| vae_zseries | optimised selection | 13.5 | 11.8 | 15.1 | 0 | 0 | 0.082 | True |
| vae_herding | optimised selection | 13.6 | 12.9 | 14.3 | 0 | 0 | 0.0449 | False |
| diffusion_ts | long-series generator | 13.9 | 11.7 | 15.9 | 0 | 0 | 0.0449 | False |
| vae_quilting | optimised selection | 14.6 | 12.8 | 16.5 | 0 | 0 | 0.0742 | True |
| vae_pctsp | optimised selection | 14.8 | 13 | 16.5 | 0 | 0 | 0.0742 | True |
| vae_atsp | optimised selection | 14.9 | 12.9 | 16.9 | 0 | 0 | 0.0742 | True |
| vae_greedy | optimised selection | 15.3 | 13.6 | 17.1 | 0 | 0 | 0.0742 | True |
| vae_knn | optimised selection | 15.7 | 13.6 | 17.7 | 0 | 0 | 0.0449 | False |
| vae_mbb | optimised selection | 15.9 | 13.4 | 18.1 | 0 | 0 | 0.082 | True |
| vae_rand | random selection | 15.9 | 13.4 | 18.2 | 0 | 0 | 0.0742 | True |
| timesfm | long-series generator | 16 | 13.8 | 18.1 | 0 | 0 | 0.172 | True |
| chronos | long-series generator | 17.1 | 14.9 | 19.1 | 0 | 0 | 0.0938 | True |
| timestral | long-series generator | 18.4 | 17 | 19.8 | 0 | 0 | 0.0449 | False |


**ranking_core_holdout_reg**

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| zedge_quilting | optimised selection | 8.32 | 7.1 | 9.45 | 0.494 | 0.898 |  | True |
| zedge_ts_ar | long-series generator | 8.6 | 6.08 | 11.3 | 0.367 | 0.805 | 0.625 | True |
| zedge_zseries | optimised selection | 8.88 | 7.67 | 10 | 0.136 | 0.616 | 0.625 | True |
| zedge_greedy | optimised selection | 9.25 | 7.83 | 10.7 | 0.001 | 0.247 | 0.625 | True |
| zedge_pctsp | optimised selection | 9.5 | 8 | 11.1 | 0 | 0.057 | 0.387 | True |
| zedge_ts_long | long-series generator | 9.51 | 7.49 | 11.8 | 0.001 | 0.204 | 0.625 | True |
| zedge_atsp | optimised selection | 9.62 | 7.4 | 12 | 0.001 | 0.16 | 0.625 | True |
| zedge_knn | optimised selection | 9.88 | 8.37 | 11.6 | 0 | 0.005 | 0.26 | True |
| zedge_herding | optimised selection | 11.3 | 9.32 | 13.4 | 0 | 0 | 0.156 | True |
| timesfm | long-series generator | 11.7 | 9.72 | 13.5 | 0 | 0.004 | 0.15 | True |
| zedge_mbb | optimised selection | 11.8 | 9.67 | 14.1 | 0 | 0 | 0.15 | True |
| zedge_rand | random selection | 11.9 | 9.63 | 14.3 | 0 | 0 | 0.127 | True |
| diffusion_ts | long-series generator | 12.4 | 10.5 | 14.2 | 0 | 0 | 0.0996 | True |
| vae_zseries | optimised selection | 13.5 | 11.6 | 15.4 | 0 | 0.004 | 0.15 | True |
| timestral | long-series generator | 13.6 | 11.8 | 15.7 | 0 | 0 | 0.082 | True |
| vae_herding | optimised selection | 14.2 | 13.3 | 15.1 | 0 | 0 | 0.0449 | False |
| chronos | long-series generator | 14.7 | 12.7 | 16.7 | 0 | 0 | 0.109 | True |
| vae_quilting | optimised selection | 15.2 | 12.8 | 17.6 | 0 | 0 | 0.127 | True |
| vae_atsp | optimised selection | 15.4 | 13 | 17.7 | 0 | 0 | 0.082 | True |
| vae_pctsp | optimised selection | 15.4 | 13.4 | 17.2 | 0 | 0 | 0.0449 | False |
| vae_greedy | optimised selection | 15.7 | 13.6 | 17.7 | 0 | 0 | 0.082 | True |
| vae_knn | optimised selection | 16.3 | 13.7 | 18.6 | 0 | 0 | 0.0996 | True |
| vae_mbb | optimised selection | 16.8 | 13.9 | 19.4 | 0 | 0 | 0.0996 | True |
| vae_rand | random selection | 16.9 | 14.1 | 19.5 | 0 | 0 | 0.082 | True |


**ranking_core_train_clf**

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| zedge_quilting | optimised selection | 7.47 | 6.14 | 8.92 | 0.325 | 0.682 |  | True |
| zedge_zseries | optimised selection | 7.5 | 6.89 | 8.14 | 0.337 | 0.619 | 1 | True |
| zedge_pctsp | optimised selection | 7.64 | 6.77 | 8.49 | 0.047 | 0.57 | 1 | True |
| zedge_ts_ar | long-series generator | 7.73 | 5.88 | 9.67 | 0.269 | 0.484 | 1 | True |
| zedge_greedy | optimised selection | 7.75 | 7.01 | 8.66 | 0.012 | 0.368 | 1 | True |
| zedge_atsp | optimised selection | 8.02 | 6.74 | 9.41 | 0.01 | 0.181 | 1 | True |
| zedge_knn | optimised selection | 8.05 | 7.46 | 8.69 | 0 | 0.086 | 1 | True |
| zedge_herding | optimised selection | 8.71 | 8.07 | 9.36 | 0 | 0.006 | 1 | True |
| zedge_ts_long | long-series generator | 8.78 | 7.51 | 10.1 | 0 | 0.004 | 0.645 | True |
| zedge_mbb | optimised selection | 9.06 | 8.34 | 9.82 | 0 | 0 | 0.738 | True |
| zedge_rand | random selection | 9.15 | 8.31 | 9.96 | 0 | 0 | 0.738 | True |
| vae_herding | optimised selection | 13.3 | 12.6 | 14.1 | 0 | 0 | 0.0449 | False |
| vae_zseries | optimised selection | 14 | 12.5 | 15.4 | 0 | 0 | 0.0547 | True |
| diffusion_ts | long-series generator | 15.2 | 13 | 17.1 | 0 | 0 | 0.0449 | False |
| vae_quilting | optimised selection | 15.3 | 13.7 | 16.9 | 0 | 0 | 0.0547 | True |
| vae_pctsp | optimised selection | 15.8 | 14.7 | 16.9 | 0 | 0 | 0.0449 | False |
| vae_atsp | optimised selection | 15.8 | 14.5 | 17.2 | 0 | 0 | 0.0449 | False |
| vae_greedy | optimised selection | 16.1 | 14.7 | 17.4 | 0 | 0 | 0.0449 | False |
| vae_knn | optimised selection | 16.7 | 15.3 | 18 | 0 | 0 | 0.0449 | False |
| vae_rand | random selection | 16.9 | 15.2 | 18.5 | 0 | 0 | 0.0449 | False |
| vae_mbb | optimised selection | 16.9 | 15.2 | 18.4 | 0 | 0 | 0.0449 | False |
| timesfm | long-series generator | 17.6 | 15.6 | 19.9 | 0 | 0 | 0.172 | True |
| chronos | long-series generator | 18.8 | 17 | 20.4 | 0 | 0 | 0.0938 | True |
| timestral | long-series generator | 20.9 | 19.4 | 22.1 | 0 | 0 | 0.0449 | False |


**ranking_core_train_reg**

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| zedge_zseries | optimised selection | 7.37 | 6.45 | 8.24 | 0.378 | 0.771 |  | True |
| zedge_ts_ar | long-series generator | 7.51 | 5.28 | 9.83 | 0.378 | 0.721 | 1 | True |
| zedge_quilting | optimised selection | 7.54 | 6.3 | 8.87 | 0.232 | 0.736 | 1 | True |
| zedge_greedy | optimised selection | 7.94 | 7.08 | 8.9 | 0.007 | 0.34 | 1 | True |
| zedge_pctsp | optimised selection | 8.07 | 6.95 | 9.19 | 0.003 | 0.193 | 1 | True |
| zedge_atsp | optimised selection | 8.42 | 6.67 | 10.4 | 0.001 | 0.167 | 1 | True |
| zedge_knn | optimised selection | 8.63 | 7.69 | 9.65 | 0.001 | 0.012 | 0.574 | True |
| zedge_ts_long | long-series generator | 8.67 | 7.04 | 10.5 | 0 | 0.06 | 0.902 | True |
| zedge_herding | optimised selection | 10.1 | 8.6 | 11.6 | 0 | 0 | 0.0879 | True |
| zedge_mbb | optimised selection | 10.8 | 9.37 | 12.3 | 0 | 0 | 0.0703 | True |
| zedge_rand | random selection | 10.8 | 9.25 | 12.4 | 0 | 0 | 0.0703 | True |
| timesfm | long-series generator | 13.3 | 11.4 | 15 | 0 | 0 | 0.125 | True |
| diffusion_ts | long-series generator | 13.7 | 12 | 15.2 | 0 | 0 | 0.0547 | True |
| vae_herding | optimised selection | 13.9 | 13 | 14.7 | 0 | 0 | 0.0449 | False |
| vae_zseries | optimised selection | 14 | 12.3 | 15.7 | 0 | 0 | 0.0449 | False |
| vae_quilting | optimised selection | 15.9 | 13.7 | 18 | 0 | 0 | 0.0547 | True |
| timestral | long-series generator | 16.1 | 14.7 | 17.5 | 0 | 0 | 0.0449 | False |
| vae_atsp | optimised selection | 16.2 | 14.5 | 17.9 | 0 | 0 | 0.0449 | False |
| chronos | long-series generator | 16.4 | 14.9 | 17.8 | 0 | 0 | 0.0781 | True |
| vae_pctsp | optimised selection | 16.4 | 15 | 17.7 | 0 | 0 | 0.0449 | False |
| vae_greedy | optimised selection | 16.5 | 14.7 | 18 | 0 | 0 | 0.0449 | False |
| vae_knn | optimised selection | 17.2 | 15.4 | 18.9 | 0 | 0 | 0.0449 | False |
| vae_mbb | optimised selection | 17.8 | 15.7 | 19.6 | 0 | 0 | 0.0449 | False |
| vae_rand | random selection | 17.8 | 15.8 | 19.8 | 0 | 0 | 0.0449 | False |


**rankings**

| family | holdout_clf:rank | holdout_clf:p_first | holdout_clf:tier | holdout_reg:rank | holdout_reg:p_first | holdout_reg:tier | train_clf:rank | train_clf:p_first | train_clf:tier | train_reg:rank | train_reg:p_first | train_reg:tier | first_in |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| long-series generator | 16.4 | 0 | True | 13.9 | 0 | True | 17.6 | 0 | True | 15.1 | 0 | True |  |
| long-series generator | 13.8 | 0 | False | 12.2 | 0 | True | 14.5 | 0 | False | 13 | 0 | True |  |
| long-series generator | 15.7 | 0 | True | 11.4 | 0.005 | True | 16.8 | 0 | True | 12.5 | 0 | True |  |
| long-series generator | 18.5 | 0 | False | 13.8 | 0 | True | 20.2 | 0 | False | 15.4 | 0 | True |  |
| long-series generator | 9.04 | 0.231 | True | 8.82 | 0.4 | True | 7.93 | 0.342 | True | 7.71 | 0.512 | True | train_reg |
| long-series generator | 10 | 0 | True | 9.94 | 0 | True | 9.24 | 0 | True | 9.13 | 0 | True |  |
| optimised selection | 14.8 | 0 | True | 15.2 | 0 | True | 15.5 | 0 | False | 15.9 | 0 | True |  |
| optimised selection | 15.2 | 0 | True | 15.5 | 0 | True | 15.9 | 0 | True | 16.2 | 0 | True |  |
| optimised selection | 13.6 | 0 | False | 14.2 | 0 | False | 13.8 | 0 | False | 14.4 | 0 | False |  |
| optimised selection | 15.4 | 0 | True | 16 | 0 | True | 16.3 | 0 | False | 16.8 | 0 | True |  |
| optimised selection | 15.6 | 0 | False | 16.5 | 0 | True | 16.5 | 0 | False | 17.4 | 0 | True |  |
| optimised selection | 14.9 | 0 | True | 15.4 | 0 | False | 15.7 | 0 | False | 16.2 | 0 | True |  |
| optimised selection | 14.4 | 0 | True | 14.9 | 0 | True | 15 | 0 | True | 15.5 | 0 | True |  |
| optimised selection | 13.5 | 0 | True | 13.5 | 0 | True | 13.9 | 0 | True | 14 | 0 | True |  |
| optimised selection | 9.37 | 0.002 | True | 9.77 | 0 | True | 8.4 | 0 | True | 8.8 | 0 | True |  |
| optimised selection | 9.16 | 0.008 | True | 9.36 | 0.004 | True | 8.09 | 0.047 | True | 8.29 | 0.015 | True |  |
| optimised selection | 10.2 | 0 | True | 11.6 | 0 | True | 9.38 | 0 | True | 10.8 | 0 | False |  |
| optimised selection | 9.46 | 0 | True | 10 | 0 | True | 8.55 | 0 | True | 9.13 | 0 | True |  |
| optimised selection | 10.2 | 0 | True | 11.9 | 0 | True | 9.42 | 0 | True | 11.2 | 0 | False |  |
| optimised selection | 9.21 | 0.02 | True | 9.65 | 0 | True | 8.17 | 0.034 | True | 8.61 | 0.002 | True |  |
| optimised selection | 8.56 | 0.676 | True | 8.63 | 0.458 | True | 7.79 | 0.415 | True | 7.86 | 0.235 | True | holdout_clf, holdout_reg, train_clf |
| optimised selection | 9.26 | 0.063 | True | 9.12 | 0.133 | True | 8.2 | 0.162 | True | 8.07 | 0.236 | True |  |
| random selection | 15.5 | 0 | False | 16.5 | 0 | True | 16.4 | 0 | False | 17.4 | 0 | False |  |
| random selection | 10.3 | 0 | True | 12 | 0 | True | 9.58 | 0 | True | 11.3 | 0 | False |  |


**rankings_core**

| family | core_holdout_clf:rank | core_holdout_clf:p_first | core_holdout_clf:tier | core_holdout_reg:rank | core_holdout_reg:p_first | core_holdout_reg:tier | core_train_clf:rank | core_train_clf:p_first | core_train_clf:tier | core_train_reg:rank | core_train_reg:p_first | core_train_reg:tier | first_in |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| long-series generator | 17.1 | 0 | True | 14.7 | 0 | True | 18.8 | 0 | True | 16.4 | 0 | True |  |
| long-series generator | 13.9 | 0 | False | 12.4 | 0 | True | 15.2 | 0 | False | 13.7 | 0 | True |  |
| long-series generator | 16 | 0 | True | 11.7 | 0 | True | 17.6 | 0 | True | 13.3 | 0 | True |  |
| long-series generator | 18.4 | 0 | False | 13.6 | 0 | True | 20.9 | 0 | False | 16.1 | 0 | False |  |
| long-series generator | 8.82 | 0.247 | True | 8.6 | 0.367 | True | 7.73 | 0.269 | True | 7.51 | 0.378 | True |  |
| long-series generator | 9.61 | 0 | True | 9.51 | 0.001 | True | 8.78 | 0 | True | 8.67 | 0 | True |  |
| optimised selection | 14.9 | 0 | True | 15.4 | 0 | True | 15.8 | 0 | False | 16.2 | 0 | False |  |
| optimised selection | 15.3 | 0 | True | 15.7 | 0 | True | 16.1 | 0 | False | 16.5 | 0 | False |  |
| optimised selection | 13.6 | 0 | False | 14.2 | 0 | False | 13.3 | 0 | False | 13.9 | 0 | False |  |
| optimised selection | 15.7 | 0 | False | 16.3 | 0 | True | 16.7 | 0 | False | 17.2 | 0 | False |  |
| optimised selection | 15.9 | 0 | True | 16.8 | 0 | True | 16.9 | 0 | False | 17.8 | 0 | False |  |
| optimised selection | 14.8 | 0 | True | 15.4 | 0 | False | 15.8 | 0 | False | 16.4 | 0 | False |  |
| optimised selection | 14.6 | 0 | True | 15.2 | 0 | True | 15.3 | 0 | True | 15.9 | 0 | True |  |
| optimised selection | 13.5 | 0 | True | 13.5 | 0 | True | 14 | 0 | True | 14 | 0 | False |  |
| optimised selection | 9.22 | 0.006 | True | 9.62 | 0.001 | True | 8.02 | 0.01 | True | 8.42 | 0.001 | True |  |
| optimised selection | 9.05 | 0.001 | True | 9.25 | 0.001 | True | 7.75 | 0.012 | True | 7.94 | 0.007 | True |  |
| optimised selection | 9.91 | 0 | True | 11.3 | 0 | True | 8.71 | 0 | True | 10.1 | 0 | True |  |
| optimised selection | 9.29 | 0 | True | 9.88 | 0 | True | 8.05 | 0 | True | 8.63 | 0.001 | True |  |
| optimised selection | 10 | 0 | True | 11.8 | 0 | True | 9.06 | 0 | True | 10.8 | 0 | True |  |
| optimised selection | 9.07 | 0.006 | True | 9.5 | 0 | True | 7.64 | 0.047 | True | 8.07 | 0.003 | True |  |
| optimised selection | 8.25 | 0.67 | True | 8.32 | 0.494 | True | 7.47 | 0.325 | True | 7.54 | 0.232 | True | core_holdout_clf, core_holdout_reg, core_train_clf |
| optimised selection | 9.02 | 0.07 | True | 8.88 | 0.136 | True | 7.5 | 0.337 | True | 7.37 | 0.378 | True | core_train_reg |
| random selection | 15.9 | 0 | True | 16.9 | 0 | True | 16.9 | 0 | False | 17.8 | 0 | False |  |
| random selection | 10.2 | 0 | True | 11.9 | 0 | True | 9.15 | 0 | True | 10.8 | 0 | True |  |


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
| diffusion_ts vs vae_rand | utility | ms_h24\|gbdt\|S\|oot\|mase | 9 | 1.66 | 2.21 | 0.834 | 4.07 | 0.113 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| diffusion_ts vs vae_rand | utility | reg_h168\|gbdt\|S\|oot\|mase | 9 | 5.3 | 5.4 | 3.34 | 7.33 | 0.113 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| diffusion_ts vs vae_rand | utility | reg_h168\|linear\|S\|val\|mase | 9 | 4.86 | 5.47 | 3.21 | 7.96 | 0.113 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| diffusion_ts vs vae_rand | utility | reg_h24\|gbdt\|S\|oot\|mase | 9 | 2.64 | 2.54 | 1.21 | 3.94 | 0.113 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| diffusion_ts vs vae_rand | utility | vol_h24\|gbdt\|S\|oot\|mase | 9 | 0.691 | 3.56 | 0.62 | 8.68 | 0.113 | 1 | 1 | 3 | 0 | 0 | inconclusive |
| diffusion_ts vs vae_rand | utility | vol_h24\|gbdt\|S\|val\|mase | 9 | 0.81 | 1.21 | 0.559 | 1.91 | 0.113 | 1 | 1 | 2 | 0 | 0 | inconclusive |
| diffusion_ts vs assembly_median | utility | reg_h168\|gbdt\|S\|oot\|mase | 9 | 6.09 | 5.41 | 3.28 | 7.55 | 0.113 | 1 | 1 | 8 | 0 | 0 | inconclusive |
| diffusion_ts vs assembly_median | utility | reg_h168\|linear\|S\|val\|mase | 9 | 4.63 | 4.36 | 2.61 | 6.06 | 0.113 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| diffusion_ts vs assembly_median | utility | reg_h24\|gbdt\|S\|oot\|mase | 9 | 1.69 | 2.54 | 1.14 | 4.07 | 0.113 | 1 | 1 | 5 | 0 | 0 | inconclusive |
| timestral vs vae_rand | utility | ms_h24\|gbdt\|S\|val\|mase | 9 | 3.69 | 4.44 | 1.93 | 7.25 | 0.113 | 1 | 1 | 7 | 1 | 0 | inconclusive |
| timestral vs vae_rand | utility | ms_h24\|linear\|S\|val\|mase | 9 | 5.12 | 4.55 | 3.11 | 5.87 | 0.113 | 1 | 1 | 8 | 0 | 0 | inconclusive |
| timestral vs vae_rand | utility | qreg_h24\|gbdt\|S\|val\|pinball | 9 | 4.59 | 7.94 | 2.11 | 17.4 | 0.113 | 1 | 1 | 7 | 1 | 0 | inconclusive |
| timestral vs vae_rand | utility | qreg_h24\|linear\|S\|val\|pinball | 9 | 2.87 | 3.06 | 1.57 | 4.81 | 0.113 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| timestral vs vae_rand | utility | reg_h168\|gbdt\|S\|oot\|mase | 9 | 5.74 | 5.55 | 3.24 | 7.73 | 0.113 | 1 | 1 | 8 | 1 | 0 | inconclusive |
| timestral vs vae_rand | utility | reg_h168\|gbdt\|S\|val\|mase | 9 | 4.19 | 4.73 | 3.14 | 6.54 | 0.113 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| timestral vs vae_rand | utility | reg_h168\|linear\|S\|val\|mase | 9 | 4.85 | 5.67 | 3.52 | 8.17 | 0.113 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| timestral vs vae_rand | utility | reg_h24\|gbdt\|S\|oot\|mase | 9 | 3.94 | 4.74 | 2.28 | 7.64 | 0.113 | 1 | 1 | 8 | 0 | 0 | inconclusive |
| timestral vs vae_rand | utility | reg_h24\|gbdt\|S\|val\|mase | 9 | 4.99 | 5.33 | 2.98 | 7.61 | 0.113 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| timestral vs vae_rand | utility | reg_h24\|linear\|S\|oot\|mase | 9 | 3.35 | 3.9 | 2.22 | 5.65 | 0.113 | 1 | 1 | 8 | 0 | 0 | inconclusive |
| timestral vs vae_rand | utility | reg_h24\|linear\|S\|val\|mase | 9 | 3.62 | 4.4 | 2.89 | 6.17 | 0.113 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| timestral vs assembly_median | utility | ms_h24\|linear\|S\|val\|mase | 9 | 6.28 | 6.84 | 3.84 | 10 | 0.113 | 1 | 1 | 8 | 0 | 0 | inconclusive |
| timestral vs assembly_median | utility | reg_h168\|gbdt\|S\|oot\|mase | 9 | 5.52 | 6.06 | 3.64 | 8.82 | 0.113 | 1 | 1 | 8 | 0 | 0 | inconclusive |
| timestral vs assembly_median | utility | reg_h168\|gbdt\|S\|val\|mase | 9 | 5.43 | 5.46 | 3.8 | 7.05 | 0.113 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| timestral vs assembly_median | utility | reg_h168\|linear\|S\|val\|mase | 9 | 4.84 | 4.77 | 3.2 | 6.36 | 0.113 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| timestral vs assembly_median | utility | reg_h24\|gbdt\|S\|oot\|mase | 9 | 5.76 | 5.47 | 2.63 | 7.98 | 0.113 | 1 | 1 | 8 | 1 | 0 | inconclusive |
| timestral vs assembly_median | utility | reg_h24\|gbdt\|S\|val\|mase | 9 | 9.35 | 8.34 | 4.57 | 11.7 | 0.113 | 1 | 1 | 8 | 1 | 0 | inconclusive |
| timestral vs assembly_median | utility | reg_h24\|linear\|S\|oot\|mase | 9 | 4.68 | 6.45 | 4.32 | 9.09 | 0.113 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| timestral vs assembly_median | utility | reg_h24\|linear\|S\|val\|mase | 9 | 5.65 | 9.47 | 4.02 | 18.4 | 0.113 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| zedge_ts_ar vs vae_rand | utility | clf_down_h24_q10\|gbdt\|S\|oot\|auc | 9 | 3.12 | 3.08 | 1.65 | 4.6 | 0.113 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| zedge_ts_ar vs vae_rand | utility | clf_up_h1_q90\|gbdt\|S\|oot\|auc | 9 | 2.22 | 2.11 | 1.22 | 3.06 | 0.113 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| zedge_ts_ar vs vae_rand | utility | clf_up_h1_q90\|gbdt\|S\|val\|auc | 9 | 1.54 | 1.62 | 0.576 | 2.95 | 0.113 | 1 | 1 | 5 | 0 | 0 | inconclusive |
| zedge_ts_ar vs vae_rand | utility | clf_up_h24_q90\|gbdt\|S\|oot\|auc | 9 | 2.62 | 2.57 | 1.2 | 4.03 | 0.113 | 1 | 1 | 5 | 0 | 0 | inconclusive |
| zedge_ts_ar vs vae_rand | utility | clf_up_h24_q95\|gbdt\|S\|oot\|auc | 9 | 2.7 | 2.2 | 1.24 | 3.23 | 0.113 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| zedge_ts_ar vs vae_rand | utility | clf_up_h24_q95\|linear\|S\|val\|auc | 9 | 2.62 | 3.5 | 1.54 | 5.57 | 0.113 | 1 | 1 | 5 | 0 | 0 | inconclusive |
| zedge_ts_ar vs vae_rand | utility | clf_up_h24_q99\|gbdt\|S\|oot\|auc | 9 | 1.76 | 2 | 0.956 | 3.19 | 0.113 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| zedge_ts_ar vs vae_rand | utility | clf_up_h6_q90\|gbdt\|S\|oot\|auc | 9 | 1.59 | 1.58 | 1.01 | 2.18 | 0.113 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| zedge_ts_ar vs vae_rand | utility | clf_up_h6_q90\|linear\|S\|oot\|auc | 9 | 2.63 | 3.05 | 1.38 | 5.22 | 0.113 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| zedge_ts_ar vs vae_rand | utility | mc3_h24\|linear\|S\|oot\|logloss | 9 | 3.93 | 3.22 | 1.37 | 5.01 | 0.113 | 1 | 1 | 7 | 1 | 0 | inconclusive |
| zedge_ts_ar vs vae_rand | utility | ms_h24\|gbdt\|S\|oot\|mase | 9 | 3.58 | 4.44 | 1.93 | 8.05 | 0.113 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| zedge_ts_ar vs vae_rand | utility | qreg_h24\|gbdt\|S\|oot\|pinball | 9 | 4.72 | 6.35 | 2.56 | 11 | 0.113 | 1 | 1 | 7 | 1 | 0 | inconclusive |

_Showing 40 rows of 2420 (rows with a better / worse / same verdict first); all of them — `hypotheses/RQ2_global.parquet`._

### RQ3. Within assembly: window selection × seam processing

| comparison | kind | unit | n_datasets | median_z | mean_z | ci_lo | ci_hi | p_better_adj | p_worse_adj | p_equiv_adj | n_better | n_worse | n_same | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| seams: vae_zseries_wsola vs vae_zseries | utility | clf_up_h24_q95\|gbdt\|S\|val\|auc | 9 | -0.414 | -0.575 | -0.849 | -0.327 | 1 | 0.0569 | 0.0284 | 0 | 1 | 1 | same |
| main effect: seams wsola vs none | utility | clf_up_h24_q95\|gbdt\|S\|val\|auc | 9 | -0.414 | -0.575 | -0.849 | -0.327 | 1 | 0.0569 | 0.0284 | 0 | 1 | 1 | same |
| selection: vae_mbb vs vae_rand | fidelity | F2.4_big_jump_share_err | 9 | -0.267 | -0.388 | -0.739 | -0.103 | 1 | 0.0569 | 0.0284 | 0 | 0 | 2 | same |
| selection: vae_mbb vs vae_rand | fidelity | F12.2_exceed_magnitude_err@oot | 8 | -0.146 | -0.173 | -0.448 | 0.0806 | 1 | 0.106 | 0.0284 | 0 | 0 | 2 | same |
| seams: vae_zseries_xfade vs vae_zseries | fidelity | F12.4_block_max_ks@oot | 8 | -0.176 | -0.424 | -0.913 | 0.00262 | 1 | 0.106 | 0.0481 | 0 | 0 | 3 | same |
| main effect: seams crossfade vs none | fidelity | F12.4_block_max_ks@oot | 8 | -0.176 | -0.424 | -0.913 | 0.00262 | 1 | 0.106 | 0.0481 | 0 | 0 | 3 | same |
| seams: vae_zseries_quilt vs vae_zseries | fidelity | F1.6_std_err@oot | 9 | -0.228 | -0.336 | -0.697 | -0.0555 | 1 | 0.133 | 0.0284 | 0 | 0 | 4 | same |
| seams: vae_zseries_xfade vs vae_zseries | fidelity | F1.1_ks@oot | 9 | -0.185 | -0.217 | -0.471 | 0.00986 | 1 | 0.133 | 0.0249 | 0 | 0 | 5 | same |
| main effect: seams crossfade vs none | fidelity | F1.1_ks@oot | 9 | -0.185 | -0.217 | -0.471 | 0.00986 | 1 | 0.133 | 0.0249 | 0 | 0 | 5 | same |
| main effect: seams quilt vs none | fidelity | F1.6_std_err@oot | 9 | -0.228 | -0.336 | -0.697 | -0.0555 | 1 | 0.133 | 0.0284 | 0 | 0 | 4 | same |
| selection: vae_mbb vs vae_rand | fidelity | F3.6_peak168_err@oot | 9 | -0.14 | -0.206 | -0.566 | 0.145 | 1 | 0.16 | 0.0249 | 0 | 0 | 1 | same |
| seams: vae_zseries_quilt vs vae_zseries | fidelity | F2.1_ks_d1 | 9 | -0.293 | -0.335 | -0.658 | -0.0203 | 1 | 0.16 | 0.0249 | 0 | 0 | 4 | same |
| seams: vae_zseries_xfade vs vae_zseries | fidelity | F1.1_ks | 9 | -0.169 | -0.201 | -0.524 | 0.0655 | 1 | 0.16 | 0.0249 | 0 | 0 | 4 | same |
| main effect: seams crossfade vs none | fidelity | F1.1_ks | 9 | -0.169 | -0.201 | -0.524 | 0.0655 | 1 | 0.16 | 0.0249 | 0 | 0 | 4 | same |
| main effect: seams quilt vs none | fidelity | F2.1_ks_d1 | 9 | -0.293 | -0.335 | -0.658 | -0.0203 | 1 | 0.16 | 0.0249 | 0 | 0 | 4 | same |
| seams: vae_zseries_quilt vs vae_zseries | utility | clf_up_h6_q90\|gbdt\|S\|oot\|auc | 9 | -0.102 | -0.184 | -0.493 | 0.0355 | 1 | 0.182 | 0.0249 | 0 | 0 | 7 | same |
| seams: vae_zseries_xfade vs vae_zseries | utility | clf_up_h6_q90\|gbdt\|S\|oot\|auc | 9 | -0.222 | -0.219 | -0.497 | 0.0286 | 1 | 0.182 | 0.0249 | 0 | 0 | 5 | same |
| main effect: seams crossfade vs none | utility | clf_up_h6_q90\|gbdt\|S\|oot\|auc | 9 | -0.222 | -0.219 | -0.497 | 0.0286 | 1 | 0.182 | 0.0249 | 0 | 0 | 5 | same |
| main effect: seams quilt vs none | utility | clf_up_h6_q90\|gbdt\|S\|oot\|auc | 9 | -0.102 | -0.184 | -0.493 | 0.0355 | 1 | 0.182 | 0.0249 | 0 | 0 | 7 | same |
| seams: vae_zseries_quilt vs vae_zseries | fidelity | F1.9_js@oot | 9 | -0.319 | -0.28 | -0.554 | 9.43e-05 | 1 | 0.182 | 0.0249 | 0 | 0 | 3 | same |
| seams: vae_zseries_quilt vs vae_zseries | fidelity | F4.2_how_std@oot | 9 | -0.215 | -0.179 | -0.466 | 0.121 | 1 | 0.182 | 0.0249 | 0 | 0 | 4 | same |
| seams: vae_zseries_xfade vs vae_zseries | fidelity | F1.9_js | 9 | -0.274 | -0.236 | -0.525 | 0.0521 | 1 | 0.182 | 0.0249 | 0 | 0 | 1 | same |
| seams: vae_zseries_xfade vs vae_zseries | fidelity | F7.5_drawdown_ks@oot | 9 | -0.203 | -0.237 | -0.471 | -0.0108 | 1 | 0.182 | 0.0249 | 0 | 0 | 4 | same |
| main effect: seams crossfade vs none | fidelity | F1.9_js | 9 | -0.274 | -0.236 | -0.525 | 0.0521 | 1 | 0.182 | 0.0249 | 0 | 0 | 1 | same |
| main effect: seams crossfade vs none | fidelity | F7.5_drawdown_ks@oot | 9 | -0.203 | -0.237 | -0.471 | -0.0108 | 1 | 0.182 | 0.0249 | 0 | 0 | 4 | same |
| main effect: seams quilt vs none | fidelity | F1.9_js@oot | 9 | -0.319 | -0.28 | -0.554 | 9.43e-05 | 1 | 0.182 | 0.0249 | 0 | 0 | 3 | same |
| main effect: seams quilt vs none | fidelity | F4.2_how_std@oot | 9 | -0.215 | -0.179 | -0.466 | 0.121 | 1 | 0.182 | 0.0249 | 0 | 0 | 4 | same |
| seams: vae_zseries_quilt vs vae_zseries | utility | vol_h24\|gbdt\|S\|val\|mase | 9 | -0.169 | -0.202 | -0.517 | 0.0182 | 1 | 0.219 | 0.0249 | 0 | 0 | 5 | same |
| main effect: seams quilt vs none | utility | vol_h24\|gbdt\|S\|val\|mase | 9 | -0.169 | -0.202 | -0.517 | 0.0182 | 1 | 0.219 | 0.0249 | 0 | 0 | 5 | same |
| seams: vae_zseries_quilt vs vae_zseries | fidelity | F1.1_ks@oot | 9 | -0.187 | -0.131 | -0.352 | 0.0778 | 1 | 0.219 | 0.0249 | 0 | 0 | 5 | same |
| seams: vae_zseries_quilt vs vae_zseries | fidelity | F4.3_hod_mean@oot | 9 | -0.214 | -0.34 | -0.793 | 0.088 | 1 | 0.219 | 0.0284 | 0 | 0 | 5 | same |
| seams: vae_zseries_quilt vs vae_zseries | fidelity | F7.5_drawdown_ks@oot | 9 | -0.154 | -0.138 | -0.313 | 0.0422 | 1 | 0.219 | 0.0249 | 0 | 0 | 6 | same |
| seams: vae_zseries_xfade vs vae_zseries | fidelity | F2.1_ks_d1 | 9 | -0.208 | -0.269 | -0.585 | 0.0297 | 1 | 0.219 | 0.0249 | 0 | 0 | 4 | same |
| main effect: seams crossfade vs none | fidelity | F2.1_ks_d1 | 9 | -0.208 | -0.269 | -0.585 | 0.0297 | 1 | 0.219 | 0.0249 | 0 | 0 | 4 | same |
| main effect: seams quilt vs none | fidelity | F1.1_ks@oot | 9 | -0.187 | -0.131 | -0.352 | 0.0778 | 1 | 0.219 | 0.0249 | 0 | 0 | 5 | same |
| main effect: seams quilt vs none | fidelity | F4.3_hod_mean@oot | 9 | -0.214 | -0.34 | -0.793 | 0.088 | 1 | 0.219 | 0.0284 | 0 | 0 | 5 | same |
| main effect: seams quilt vs none | fidelity | F7.5_drawdown_ks@oot | 9 | -0.154 | -0.138 | -0.313 | 0.0422 | 1 | 0.219 | 0.0249 | 0 | 0 | 6 | same |
| seams: vae_zseries_wsola vs vae_zseries | utility | ms_h24\|gbdt\|S\|oot\|mase | 9 | -0.295 | -0.306 | -0.644 | 0.0561 | 1 | 0.257 | 0.0249 | 0 | 0 | 3 | same |
| main effect: seams wsola vs none | utility | ms_h24\|gbdt\|S\|oot\|mase | 9 | -0.295 | -0.306 | -0.644 | 0.0561 | 1 | 0.257 | 0.0249 | 0 | 0 | 3 | same |
| selection: vae_mbb vs vae_rand | fidelity | F2.2_vol_ratio_err_d1 | 9 | -0.201 | -0.207 | -0.577 | 0.178 | 1 | 0.257 | 0.0249 | 0 | 0 | 1 | same |

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
| F8.4_event_by_how@train | F8.4_event_by_how | train | F8_target | regression@oot | 9 | 0.872 | 0.889 | 0.0117 | 0.0352 | True |
| F8.5_cond_event_err@oot | F8.5_cond_event_err | oot | F8_target | regression@oot | 9 | 0.846 | 0.889 | 0.00781 | 0.0291 | True |
| F8.6_cond_future_ks@train | F8.6_cond_future_ks | train | F8_target | regression@oot | 9 | 0.839 | 0.778 | 0.0195 | 0.0465 | True |
| F6.6_feature_fid@oot | F6.6_feature_fid | oot | F6_windows | regression@oot | 9 | 0.837 | 1 | 0.00391 | 0.0237 | True |
| F8.4_event_by_how | F8.4_event_by_how | val | F8_target | regression@val | 9 | 0.835 | 0.778 | 0.0195 | 0.0465 | True |
| F8.5_cond_event_err@train | F8.5_cond_event_err | train | F8_target | regression@oot | 9 | 0.834 | 0.889 | 0.00781 | 0.0291 | True |
| F1.6_mean_err@oot | F1.6_mean_err | oot | F1_marginal | regression@oot | 9 | 0.831 | 1 | 0.00391 | 0.0237 | True |
| F8.4_event_by_how@oot | F8.4_event_by_how | oot | F8_target | regression@oot | 9 | 0.826 | 0.889 | 0.00781 | 0.0291 | True |
| F8.6_cond_future_ks@oot | F8.6_cond_future_ks | oot | F8_target | regression@oot | 9 | 0.823 | 0.889 | 0.00781 | 0.0291 | True |
| F6.4_mmd@oot | F6.4_mmd | oot | F6_windows | regression@oot | 9 | 0.822 | 0.889 | 0.00781 | 0.0291 | True |
| F8.4_event_by_how | F8.4_event_by_how | val | F8_target | regression@oot | 9 | 0.821 | 0.889 | 0.00781 | 0.0291 | True |
| F9.2_coverage@train | F9.2_coverage | train | F9_coverage | regression@oot | 9 | 0.82 | 0.778 | 0.0195 | 0.0465 | True |
| F6.6_feature_fid@train | F6.6_feature_fid | train | F6_windows | classification@oot | 9 | 0.82 | 1 | 0.00391 | 0.0237 | True |
| F9.2_coverage@train | F9.2_coverage | train | F9_coverage | classification@oot | 9 | 0.819 | 1 | 0.00391 | 0.0237 | True |
| F6.8_nn_dist_logratio | F6.8_nn_dist_logratio | val | F6_windows | regression@val | 9 | 0.819 | 1 | 0.00391 | 0.0237 | True |
| F8.5_cond_event_err@train | F8.5_cond_event_err | train | F8_target | classification@val | 9 | 0.818 | 0.778 | 0.0195 | 0.0465 | True |
| F8.6_cond_future_ks@oot | F8.6_cond_future_ks | oot | F8_target | classification@oot | 9 | 0.818 | 0.889 | 0.00781 | 0.0291 | True |
| F1.5_quantile_err@oot | F1.5_quantile_err | oot | F1_marginal | regression@oot | 9 | 0.817 | 1 | 0.00391 | 0.0237 | True |
| F11.3_multiclass_tvd@train | F11.3_multiclass_tvd | train | F11_class_balance | classification@val | 9 | 0.815 | 0.889 | 0.00781 | 0.0291 | True |
| F1.2_w1@oot | F1.2_w1 | oot | F1_marginal | regression@oot | 9 | 0.814 | 1 | 0.00391 | 0.0237 | True |
| F6.6_feature_fid@oot | F6.6_feature_fid | oot | F6_windows | classification@oot | 9 | 0.814 | 0.778 | 0.0273 | 0.0575 | False |
| F8.5_cond_event_err | F8.5_cond_event_err | val | F8_target | regression@oot | 9 | 0.811 | 0.889 | 0.0117 | 0.0352 | True |
| F6.4_mmd | F6.4_mmd | val | F6_windows | regression@oot | 9 | 0.81 | 0.778 | 0.129 | 0.171 | False |
| F8.1_class_tvd | F8.1_class_tvd | val | F8_target | regression@oot | 9 | 0.807 | 0.889 | 0.00781 | 0.0291 | True |
| F8.6_cond_future_ks | F8.6_cond_future_ks | val | F8_target | classification@oot | 9 | 0.803 | 0.778 | 0.0391 | 0.0736 | False |
| F9.2_coverage@oot | F9.2_coverage | oot | F9_coverage | regression@oot | 9 | 0.803 | 1 | 0.00391 | 0.0237 | True |
| F8.4_event_by_how@train | F8.4_event_by_how | train | F8_target | regression@val | 9 | 0.8 | 0.667 | 0.0547 | 0.0915 | False |
| F2.1_w1_d24@train | F2.1_w1_d24 | train | F2_increments | classification@oot | 9 | 0.8 | 1 | 0.00391 | 0.0237 | True |
| F8.4_event_by_how@oot | F8.4_event_by_how | oot | F8_target | regression@val | 9 | 0.8 | 0.889 | 0.0117 | 0.0352 | True |
| F3.8_calendar_corr_err | F3.8_calendar_corr_err | val | F3_dependence | regression@oot | 9 | 0.799 | 0.889 | 0.00781 | 0.0291 | True |
| F8.6_cond_future_ks@train | F8.6_cond_future_ks | train | F8_target | classification@oot | 9 | 0.799 | 1 | 0.00391 | 0.0237 | True |
| F8.1_class_tvd@train | F8.1_class_tvd | train | F8_target | classification@val | 9 | 0.797 | 0.667 | 0.0547 | 0.0915 | False |
| F8.6_cond_future_ks@train | F8.6_cond_future_ks | train | F8_target | classification@val | 9 | 0.796 | 0.889 | 0.00781 | 0.0291 | True |
| F8.6_cond_future_ks@oot | F8.6_cond_future_ks | oot | F8_target | classification@val | 9 | 0.795 | 0.889 | 0.00781 | 0.0291 | True |
| F8.5_cond_event_err@train | F8.5_cond_event_err | train | F8_target | regression@val | 9 | 0.795 | 0.778 | 0.0391 | 0.0736 | False |
| F7.3_crossings_err | F7.3_crossings_err | val | F7_long_structure | classification@oot | 9 | 0.793 | 0.778 | 0.0547 | 0.0915 | False |
| F9.2_coverage@oot | F9.2_coverage | oot | F9_coverage | classification@oot | 9 | 0.792 | 1 | 0.00391 | 0.0237 | True |
| F6.8_nn_dist_logratio@oot | F6.8_nn_dist_logratio | oot | F6_windows | regression@oot | 9 | 0.792 | 0.889 | 0.0195 | 0.0465 | True |
| F8.6_cond_future_ks | F8.6_cond_future_ks | val | F8_target | regression@oot | 9 | 0.791 | 0.778 | 0.0273 | 0.0575 | False |
| F8.1_class_tvd@train | F8.1_class_tvd | train | F8_target | regression@oot | 9 | 0.789 | 0.889 | 0.00781 | 0.0291 | True |

_Showing 40 rows of 872; all of them — `hypotheses/RQ4_global.parquet`._

**by_reference**

| criterion | reference | median_rho | share_predictive |
|---|---|---|---|
| classification@oot | oot | 0.632 | 0.611 |
| classification@oot | train | 0.649 | 0.847 |
| classification@oot | val | 0.489 | 0.311 |
| classification@val | oot | 0.485 | 0.25 |
| classification@val | train | 0.606 | 0.792 |
| classification@val | val | 0.486 | 0.324 |
| regression@oot | oot | 0.643 | 0.569 |
| regression@oot | train | 0.651 | 0.583 |
| regression@oot | val | 0.556 | 0.203 |
| regression@val | oot | 0.39 | 0.069 |
| regression@val | train | 0.525 | 0.069 |
| regression@val | val | 0.53 | 0.392 |


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
| F5_seams | oot | 0.419 | 0.576 | 0.06 | 0.284 |
| F5_seams | train | 0.577 | 0.619 | 0.553 | 0.531 |
| F5_seams | val | 0.29 | 0.394 | 0.412 | 0.456 |
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
| F8.4_event_by_how@train | F8.4_event_by_how | train | F8_target | regression@oot | 9 | 0.872 | 0.889 | 0.0117 | 0.0352 | True |
| F8.5_cond_event_err@oot | F8.5_cond_event_err | oot | F8_target | regression@oot | 9 | 0.846 | 0.889 | 0.00781 | 0.0291 | True |
| F8.6_cond_future_ks@train | F8.6_cond_future_ks | train | F8_target | regression@oot | 9 | 0.839 | 0.778 | 0.0195 | 0.0465 | True |
| F6.6_feature_fid@oot | F6.6_feature_fid | oot | F6_windows | regression@oot | 9 | 0.837 | 1 | 0.00391 | 0.0237 | True |
| F8.4_event_by_how | F8.4_event_by_how | val | F8_target | regression@val | 9 | 0.835 | 0.778 | 0.0195 | 0.0465 | True |
| F8.5_cond_event_err@train | F8.5_cond_event_err | train | F8_target | regression@oot | 9 | 0.834 | 0.889 | 0.00781 | 0.0291 | True |
| F6.6_feature_fid@train | F6.6_feature_fid | train | F6_windows | classification@oot | 9 | 0.82 | 1 | 0.00391 | 0.0237 | True |
| F9.2_coverage@train | F9.2_coverage | train | F9_coverage | classification@oot | 9 | 0.819 | 1 | 0.00391 | 0.0237 | True |
| F6.8_nn_dist_logratio | F6.8_nn_dist_logratio | val | F6_windows | regression@val | 9 | 0.819 | 1 | 0.00391 | 0.0237 | True |
| F8.5_cond_event_err@train | F8.5_cond_event_err | train | F8_target | classification@val | 9 | 0.818 | 0.778 | 0.0195 | 0.0465 | True |
| F8.6_cond_future_ks@oot | F8.6_cond_future_ks | oot | F8_target | classification@oot | 9 | 0.818 | 0.889 | 0.00781 | 0.0291 | True |
| F11.3_multiclass_tvd@train | F11.3_multiclass_tvd | train | F11_class_balance | classification@val | 9 | 0.815 | 0.889 | 0.00781 | 0.0291 | True |
| F6.6_feature_fid@oot | F6.6_feature_fid | oot | F6_windows | classification@oot | 9 | 0.814 | 0.778 | 0.0273 | 0.0575 | False |
| F8.6_cond_future_ks | F8.6_cond_future_ks | val | F8_target | classification@oot | 9 | 0.803 | 0.778 | 0.0391 | 0.0736 | False |
| F8.4_event_by_how@train | F8.4_event_by_how | train | F8_target | regression@val | 9 | 0.8 | 0.667 | 0.0547 | 0.0915 | False |
| F8.4_event_by_how@oot | F8.4_event_by_how | oot | F8_target | regression@val | 9 | 0.8 | 0.889 | 0.0117 | 0.0352 | True |
| F8.1_class_tvd@train | F8.1_class_tvd | train | F8_target | classification@val | 9 | 0.797 | 0.667 | 0.0547 | 0.0915 | False |
| F8.6_cond_future_ks@train | F8.6_cond_future_ks | train | F8_target | classification@val | 9 | 0.796 | 0.889 | 0.00781 | 0.0291 | True |
| F8.6_cond_future_ks@oot | F8.6_cond_future_ks | oot | F8_target | classification@val | 9 | 0.795 | 0.889 | 0.00781 | 0.0291 | True |
| F8.5_cond_event_err@train | F8.5_cond_event_err | train | F8_target | regression@val | 9 | 0.795 | 0.778 | 0.0391 | 0.0736 | False |


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
| val ↔ oot | fidelity:seams | 0.406 |
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
| holdout_clf | timestral | long-series generator | 18.5 | 14.9 | 1.23 | True |
| holdout_clf | timesfm | long-series generator | 15.7 | 13.4 | 2.38 | True |
| holdout_clf | chronos | long-series generator | 16.4 | 13.8 | 33.9 | False |
| holdout_clf | vae_rand | random selection | 15.5 | 13.2 | 131 | True |
| holdout_clf | vae_quilting | optimised selection | 14.4 | 12.6 | 131 | True |
| holdout_clf | vae_greedy | optimised selection | 15.2 | 13.3 | 131 | False |
| holdout_clf | vae_knn | optimised selection | 15.4 | 13.6 | 131 | False |
| holdout_clf | vae_mbb | optimised selection | 15.6 | 13.9 | 131 | False |
| holdout_clf | vae_herding | optimised selection | 13.6 | 12.8 | 131 | True |
| holdout_clf | vae_zseries | optimised selection | 13.5 | 13.4 | 134 | True |
| holdout_clf | vae_atsp | optimised selection | 14.8 | 14.2 | 164 | False |
| holdout_clf | vae_pctsp | optimised selection | 14.9 | 14.2 | 171 | False |
| holdout_clf | zedge_rand | random selection | 10.3 | 10.6 | 798 | True |
| holdout_clf | zedge_quilting | optimised selection | 8.56 | 9.63 | 798 | True |
| holdout_clf | zedge_greedy | optimised selection | 9.16 | 10.2 | 798 | False |
| holdout_clf | zedge_knn | optimised selection | 9.46 | 10.6 | 798 | False |
| holdout_clf | zedge_mbb | optimised selection | 10.2 | 11.2 | 798 | False |
| holdout_clf | zedge_herding | optimised selection | 10.2 | 11.6 | 798 | False |
| holdout_clf | zedge_zseries | optimised selection | 9.26 | 11.2 | 801 | False |
| holdout_clf | zedge_atsp | optimised selection | 9.37 | 11.5 | 822 | False |
| holdout_clf | zedge_pctsp | optimised selection | 9.21 | 11.3 | 839 | False |
| holdout_clf | diffusion_ts | long-series generator | 13.8 | 16.4 | 2.35e+03 | False |
| holdout_clf | zedge_ts_long | long-series generator | 10 | 11.8 | 2.93e+03 | False |
| holdout_clf | zedge_ts_ar | long-series generator | 9.04 | 11.2 | 2.95e+03 | False |
| holdout_reg | timestral | long-series generator | 13.8 | 11.7 | 1.23 | True |
| holdout_reg | timesfm | long-series generator | 11.4 | 10.5 | 2.38 | True |
| holdout_reg | chronos | long-series generator | 13.9 | 12.2 | 33.9 | False |
| holdout_reg | vae_rand | random selection | 16.5 | 13.9 | 131 | False |
| holdout_reg | vae_quilting | optimised selection | 14.9 | 13 | 131 | False |
| holdout_reg | vae_greedy | optimised selection | 15.5 | 13.6 | 131 | False |
| holdout_reg | vae_knn | optimised selection | 16 | 14 | 131 | False |
| holdout_reg | vae_mbb | optimised selection | 16.5 | 14.5 | 131 | False |
| holdout_reg | vae_herding | optimised selection | 14.2 | 13.2 | 131 | False |
| holdout_reg | vae_zseries | optimised selection | 13.5 | 13.4 | 134 | False |
| holdout_reg | vae_atsp | optimised selection | 15.2 | 14.5 | 164 | False |
| holdout_reg | vae_pctsp | optimised selection | 15.4 | 14.5 | 171 | False |
| holdout_reg | zedge_rand | random selection | 12 | 11.8 | 798 | False |
| holdout_reg | zedge_quilting | optimised selection | 8.63 | 9.68 | 798 | True |
| holdout_reg | zedge_greedy | optimised selection | 9.36 | 10.3 | 798 | False |
| holdout_reg | zedge_knn | optimised selection | 10 | 11 | 798 | False |


**hardware**: ['NVIDIA H200']

### RQ7. Moderators: dataset descriptors and the effects of RQ2 / RQ3 (exploratory)

| effect | descriptor | spearman | p | n | p_bh |
|---|---|---|---|---|---|
| RQ2:fidelity:chronos vs assembly_median | acf24 | -0.0714 | 0.879 | 7 | 0.967 |
| RQ2:fidelity:chronos vs assembly_median | acf168 | 0.75 | 0.0522 | 7 | 0.34 |
| RQ2:fidelity:chronos vs assembly_median | kurt_d24 | 0.857 | 0.0137 | 7 | 0.268 |
| RQ2:fidelity:chronos vs assembly_median | volclust | -0.107 | 0.819 | 7 | 0.924 |
| RQ2:fidelity:chronos vs assembly_median | trend | 0.25 | 0.589 | 7 | 0.849 |
| RQ2:fidelity:chronos vs assembly_median | nan_share | -0.408 | 0.363 | 7 | 0.702 |
| RQ2:utility:chronos vs assembly_median | acf24 | 0.179 | 0.702 | 7 | 0.87 |
| RQ2:utility:chronos vs assembly_median | acf168 | 0.75 | 0.0522 | 7 | 0.34 |
| RQ2:utility:chronos vs assembly_median | kurt_d24 | 0.679 | 0.0938 | 7 | 0.397 |
| RQ2:utility:chronos vs assembly_median | volclust | 0.464 | 0.294 | 7 | 0.668 |
| RQ2:utility:chronos vs assembly_median | trend | 0.107 | 0.819 | 7 | 0.924 |
| RQ2:utility:chronos vs assembly_median | nan_share | -0.612 | 0.144 | 7 | 0.496 |
| RQ2:fidelity:chronos vs vae_rand | acf24 | -0.179 | 0.702 | 7 | 0.87 |
| RQ2:fidelity:chronos vs vae_rand | acf168 | 0.643 | 0.119 | 7 | 0.457 |
| RQ2:fidelity:chronos vs vae_rand | kurt_d24 | 0.929 | 0.00252 | 7 | 0.132 |
| RQ2:fidelity:chronos vs vae_rand | volclust | -0.286 | 0.535 | 7 | 0.818 |
| RQ2:fidelity:chronos vs vae_rand | trend | -0.143 | 0.76 | 7 | 0.904 |
| RQ2:fidelity:chronos vs vae_rand | nan_share | 0 | 1 | 7 | 1 |
| RQ2:utility:chronos vs vae_rand | acf24 | 0.179 | 0.702 | 7 | 0.87 |
| RQ2:utility:chronos vs vae_rand | acf168 | 0.75 | 0.0522 | 7 | 0.34 |
| RQ2:utility:chronos vs vae_rand | kurt_d24 | 0.679 | 0.0938 | 7 | 0.397 |
| RQ2:utility:chronos vs vae_rand | volclust | 0.464 | 0.294 | 7 | 0.668 |
| RQ2:utility:chronos vs vae_rand | trend | 0.107 | 0.819 | 7 | 0.924 |
| RQ2:utility:chronos vs vae_rand | nan_share | -0.612 | 0.144 | 7 | 0.496 |
| RQ2:fidelity:diffusion_ts vs assembly_median | acf24 | -0.583 | 0.0992 | 9 | 0.397 |
| RQ2:fidelity:diffusion_ts vs assembly_median | acf168 | -0.2 | 0.606 | 9 | 0.853 |
| RQ2:fidelity:diffusion_ts vs assembly_median | kurt_d24 | 0.4 | 0.286 | 9 | 0.668 |
| RQ2:fidelity:diffusion_ts vs assembly_median | volclust | -0.183 | 0.637 | 9 | 0.862 |
| RQ2:fidelity:diffusion_ts vs assembly_median | trend | -0.85 | 0.0037 | 9 | 0.132 |
| RQ2:fidelity:diffusion_ts vs assembly_median | nan_share | 0.639 | 0.0639 | 9 | 0.369 |
| RQ2:utility:diffusion_ts vs assembly_median | acf24 | -0.4 | 0.286 | 9 | 0.668 |
| RQ2:utility:diffusion_ts vs assembly_median | acf168 | 0.05 | 0.898 | 9 | 0.976 |
| RQ2:utility:diffusion_ts vs assembly_median | kurt_d24 | 0.533 | 0.139 | 9 | 0.496 |
| RQ2:utility:diffusion_ts vs assembly_median | volclust | -0.15 | 0.7 | 9 | 0.87 |
| RQ2:utility:diffusion_ts vs assembly_median | trend | -0.75 | 0.0199 | 9 | 0.292 |
| RQ2:utility:diffusion_ts vs assembly_median | nan_share | 0.456 | 0.217 | 9 | 0.578 |
| RQ2:fidelity:diffusion_ts vs vae_rand | acf24 | -0.6 | 0.0876 | 9 | 0.395 |
| RQ2:fidelity:diffusion_ts vs vae_rand | acf168 | -0.283 | 0.46 | 9 | 0.793 |
| RQ2:fidelity:diffusion_ts vs vae_rand | kurt_d24 | 0.283 | 0.46 | 9 | 0.793 |
| RQ2:fidelity:diffusion_ts vs vae_rand | volclust | -0.167 | 0.668 | 9 | 0.87 |

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

