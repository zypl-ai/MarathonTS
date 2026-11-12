# Benchmark report

Datasets: beijing_pm25, bike, bitcoin, electricity, ett, household, jena, metro, pjm. Seeds: 10. α = 0.05. Metrics left out: F3.8_calendar_corr_err, F4.1_how_mean, F4.2_how_std, F4.3_hod_mean, F4.4_calendar_continuity, F4.5_calendar_seam_breaks, F8.4_event_by_how (Config.exclude_metrics). Leakage (Config.leaked): `chronos` on electricity, beijing_pm25; `timesfm` on beijing_pm25, household, bitcoin. Verdict of a comparison "A vs B": better / worse (A better / worse than B) / same (equivalence, TOST) / inconclusive. Effects are in noise units — divided by the smallest effect size of interest (SESOI: the median |vae_rand − vae_rand_b| on one pool — or, where vae_rand_b is not run (min), the between-seed spread of vae_rand — or the method's between-seed spread, see HYPOTHESES.md §2). Utility: TSTR (training on synthetic data only) vs TRTR (training on real data), tested on the real val / OOT; transfer ratio = 1 — synthetic data train the model as well as real data. Overall leaderboard — `OVERALL.md`; ranking of every method in every slice — `LEADERBOARD.md`; values of the metrics by slice — `METRIC_VALUES.md` (this folder). Tables of the tests — `hypotheses/`.

## Overall leaderboard

Fidelity on the core metrics (each criterion against train, val and OOT) and utility (TSTR classification and regression, val and OOT), equal weights; noise-aware ranks; privacy and cost not included. Composition, columns and the robustness checks — `OVERALL.md`.

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon | fidelity_rank | utility_rank | norm_overall | memorisation_flag |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| zedge_quilting | optimised selection | 8.13 | 7.22 | 9.08 | 0.88 | 0.976 |  | True | 8.01 | 8.25 | 0.5 | False |
| zedge_zseries | optimised selection | 8.72 | 8.23 | 9.36 | 0.065 | 0.713 | 0.328 | True | 8.73 | 8.72 | 0.282 | False |
| zedge_greedy | optimised selection | 8.86 | 7.94 | 9.86 | 0.01 | 0.707 | 0.328 | True | 8.79 | 8.92 | 0.298 | False |
| zedge_pctsp | optimised selection | 9.1 | 8.1 | 10.2 | 0 | 0.146 | 0.26 | True | 8.94 | 9.26 | 0.26 | False |
| zedge_atsp | optimised selection | 9.25 | 7.79 | 10.9 | 0.014 | 0.162 | 0.328 | True | 8.86 | 9.64 | 0.331 | False |
| zedge_ts_long | long-series generator | 9.26 | 7.83 | 10.8 | 0.027 | 0.199 | 0.328 | True | 9.03 | 9.49 | 0.785 | False |
| zedge_knn | optimised selection | 9.3 | 8.33 | 10.4 | 0 | 0.019 | 0.293 | True | 9.23 | 9.37 | 0.387 | False |
| zedge_ts_ar | long-series generator | 9.45 | 8.02 | 11 | 0.004 | 0.078 | 0.293 | True | 10.2 | 8.69 | 0.767 | False |
| zedge_herding | optimised selection | 10.6 | 9.36 | 11.9 | 0 | 0 | 0.0449 | False | 10.5 | 10.7 | 0.057 | False |
| zedge_mbb | optimised selection | 10.7 | 9.3 | 12.2 | 0 | 0 | 0.0508 | True | 10.7 | 10.7 | 0.0553 | False |
| zedge_rand | random selection | 10.9 | 9.33 | 12.4 | 0 | 0 | 0.0508 | True | 10.7 | 11 | 0 | False |
| vae_herding | optimised selection | 13.5 | 12.8 | 14.3 | 0 | 0 | 0.0449 | False | 13.1 | 13.9 | 0.3 | False |
| diffusion_ts | long-series generator | 13.6 | 11.7 | 15.2 | 0 | 0 | 0.0449 | False | 13.9 | 13.2 | 0.503 | False |
| vae_zseries | optimised selection | 13.7 | 12.2 | 15.3 | 0 | 0 | 0.0508 | True | 13.5 | 13.9 | 0.348 | False |
| vae_quilting | optimised selection | 14.5 | 12.7 | 16.2 | 0 | 0 | 0.0508 | True | 14.3 | 14.7 | 0.0849 | False |
| timesfm | long-series generator | 15 | 13.3 | 16.7 | 0 | 0 | 0.125 | True | 16.3 | 13.6 | -0.0365 | False |
| vae_atsp | optimised selection | 15.3 | 13.4 | 17.1 | 0 | 0 | 0.0449 | False | 15.3 | 15.3 | 0.131 | False |
| vae_pctsp | optimised selection | 15.3 | 13.9 | 16.7 | 0 | 0 | 0.0449 | False | 15 | 15.7 | 0.167 | False |
| vae_greedy | optimised selection | 15.6 | 13.9 | 17.2 | 0 | 0 | 0.0449 | False | 15.5 | 15.7 | 0.0507 | False |
| chronos | long-series generator | 15.7 | 14.1 | 17.4 | 0 | 0 | 0.0703 | True | 16.3 | 15.2 | -0.126 | False |
| vae_knn | optimised selection | 16 | 14.2 | 17.6 | 0 | 0 | 0.0449 | False | 16 | 16 | 0.0928 | False |
| vae_mbb | optimised selection | 16.2 | 14.2 | 18 | 0 | 0 | 0.0449 | False | 16 | 16.3 | 0.0724 | False |
| vae_rand | random selection | 16.4 | 14.4 | 18.2 | 0 | 0 | 0.0449 | False | 16.3 | 16.4 | 0 | False |
| timestral | long-series generator | 17.3 | 16.2 | 18.4 | 0 | 0 | 0.0449 | False | 18.3 | 16.2 | -0.548 | False |


Sensitivity variants:

| variant | text | first | tau_vs_main | main_first_place |
|---|---|---|---|---|
| main | the leaderboard: core metrics, fidelity against train + val + OOT, noise-aware ranks | zedge_quilting | 1 | 1 |
| plain_ranks | ordinary average ranks (no ties within the noise) | zedge_quilting | 0.964 | 1 |
| fidelity_train | fidelity against train only | zedge_quilting | 0.964 | 1 |
| fidelity_holdout | fidelity against val + OOT only | zedge_quilting | 0.957 | 1 |
| no_unchecked | without F5.7 (seams, no anchor) and F6.1 against val (noise) | zedge_quilting | 0.942 | 1 |
| all_metrics | every fidelity metric instead of the core set | zedge_quilting | 0.935 | 1 |
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
| chronos | long-series generator | 16.1 | 0 | True | 13.7 | 0 | True | 17.3 | 0 | True | 14.8 | 0 | True |  |
| diffusion_ts | long-series generator | 13.7 | 0 | False | 12.1 | 0 | True | 14.4 | 0 | False | 12.9 | 0 | False |  |
| timesfm | long-series generator | 16.2 | 0 | True | 11.9 | 0.002 | True | 17 | 0 | True | 12.7 | 0 | True |  |
| timestral | long-series generator | 18.3 | 0 | False | 13.5 | 0 | True | 19.5 | 0 | False | 14.7 | 0 | False |  |
| zedge_ts_ar | long-series generator | 9.15 | 0.119 | True | 8.94 | 0.252 | True | 8.27 | 0.162 | True | 8.05 | 0.293 | True |  |
| zedge_ts_long | long-series generator | 9.65 | 0 | True | 9.54 | 0.001 | True | 8.97 | 0 | True | 8.86 | 0.001 | True |  |
| vae_atsp | optimised selection | 14.6 | 0 | True | 15.1 | 0 | False | 15.2 | 0 | False | 15.6 | 0 | False |  |
| vae_greedy | optimised selection | 15 | 0 | True | 15.3 | 0 | True | 15.5 | 0 | False | 15.9 | 0 | False |  |
| vae_herding | optimised selection | 14 | 0 | False | 14.6 | 0 | False | 14.3 | 0 | False | 14.9 | 0 | False |  |
| vae_knn | optimised selection | 15.4 | 0 | False | 15.9 | 0 | False | 16.1 | 0 | False | 16.6 | 0 | False |  |
| vae_mbb | optimised selection | 15.9 | 0 | False | 16.8 | 0 | False | 16.6 | 0 | False | 17.5 | 0 | False |  |
| vae_pctsp | optimised selection | 14.5 | 0 | False | 15 | 0 | False | 15.2 | 0 | False | 15.7 | 0 | False |  |
| vae_quilting | optimised selection | 13.8 | 0 | True | 14.3 | 0 | True | 14.3 | 0 | False | 14.9 | 0 | False |  |
| vae_zseries | optimised selection | 13.6 | 0 | True | 13.7 | 0 | True | 14 | 0 | False | 14 | 0 | False |  |
| zedge_atsp | optimised selection | 9.27 | 0.003 | True | 9.67 | 0.001 | True | 8.37 | 0.001 | True | 8.78 | 0 | True |  |
| zedge_greedy | optimised selection | 9.08 | 0.002 | True | 9.28 | 0.005 | True | 8.17 | 0.011 | True | 8.36 | 0.009 | True |  |
| zedge_herding | optimised selection | 10.6 | 0 | False | 12 | 0 | True | 10.1 | 0 | True | 11.5 | 0 | True |  |
| zedge_knn | optimised selection | 9.51 | 0 | True | 10.1 | 0 | True | 8.68 | 0 | True | 9.27 | 0 | True |  |
| zedge_mbb | optimised selection | 10.6 | 0 | False | 12.3 | 0 | False | 10.1 | 0 | False | 11.9 | 0 | False |  |
| zedge_pctsp | optimised selection | 9.1 | 0.006 | True | 9.54 | 0 | True | 8.13 | 0.038 | True | 8.57 | 0 | True |  |
| zedge_quilting | optimised selection | 8.31 | 0.844 | True | 8.39 | 0.672 | True | 7.6 | 0.701 | True | 7.67 | 0.562 | True | holdout_clf, holdout_reg, train_clf, train_reg |
| zedge_zseries | optimised selection | 9.29 | 0.026 | True | 9.15 | 0.067 | True | 8.37 | 0.087 | True | 8.24 | 0.135 | True |  |
| vae_rand | random selection | 15.8 | 0 | False | 16.8 | 0 | False | 16.6 | 0 | False | 17.6 | 0 | False |  |
| zedge_rand | random selection | 10.8 | 0 | False | 12.5 | 0 | False | 10.3 | 0 | False | 12 | 0 | False |  |


### Ranking `holdout_clf`: Fidelity: val + OOT; utility: classification

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| zedge_quilting | optimised selection | 8.31 | 7.25 | 9.45 | 0.844 | 0.985 |  | True |
| zedge_greedy | optimised selection | 9.08 | 8.18 | 10.1 | 0.002 | 0.479 | 0.117 | True |
| zedge_pctsp | optimised selection | 9.1 | 8.24 | 9.97 | 0.006 | 0.495 | 0.193 | True |
| zedge_ts_ar | long-series generator | 9.15 | 7.52 | 10.8 | 0.119 | 0.464 | 0.193 | True |
| zedge_atsp | optimised selection | 9.27 | 8.01 | 10.6 | 0.003 | 0.255 | 0.193 | True |
| zedge_zseries | optimised selection | 9.29 | 8.88 | 9.74 | 0.026 | 0.302 | 0.148 | True |
| zedge_knn | optimised selection | 9.51 | 8.73 | 10.4 | 0 | 0.007 | 0.0781 | True |
| zedge_ts_long | long-series generator | 9.65 | 8.31 | 11 | 0 | 0.013 | 0.117 | True |
| zedge_mbb | optimised selection | 10.6 | 9.56 | 11.6 | 0 | 0 | 0.0449 | False |
| zedge_herding | optimised selection | 10.6 | 9.74 | 11.4 | 0 | 0 | 0.0449 | False |
| zedge_rand | random selection | 10.8 | 9.65 | 11.9 | 0 | 0 | 0.0449 | False |
| vae_zseries | optimised selection | 13.6 | 12.3 | 14.9 | 0 | 0 | 0.0508 | True |
| diffusion_ts | long-series generator | 13.7 | 11.7 | 15.4 | 0 | 0 | 0.0449 | False |
| vae_quilting | optimised selection | 13.8 | 12.3 | 15.2 | 0 | 0 | 0.0508 | True |
| vae_herding | optimised selection | 14 | 13.3 | 14.7 | 0 | 0 | 0.0449 | False |
| vae_pctsp | optimised selection | 14.5 | 13.2 | 15.7 | 0 | 0 | 0.0449 | False |
| vae_atsp | optimised selection | 14.6 | 13.1 | 16.1 | 0 | 0 | 0.0508 | True |
| vae_greedy | optimised selection | 15 | 13.7 | 16.3 | 0 | 0 | 0.0508 | True |
| vae_knn | optimised selection | 15.4 | 13.9 | 16.8 | 0 | 0 | 0.0449 | False |
| vae_rand | random selection | 15.8 | 14 | 17.6 | 0 | 0 | 0.0449 | False |
| vae_mbb | optimised selection | 15.9 | 14 | 17.6 | 0 | 0 | 0.0449 | False |
| chronos | long-series generator | 16.1 | 14 | 18 | 0 | 0 | 0.0703 | True |
| timesfm | long-series generator | 16.2 | 13.6 | 18.7 | 0 | 0 | 0.109 | True |
| timestral | long-series generator | 18.3 | 17 | 19.5 | 0 | 0 | 0.0449 | False |


### Ranking `holdout_reg`: Fidelity: val + OOT; utility: regression

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| zedge_quilting | optimised selection | 8.39 | 7.35 | 9.38 | 0.672 | 0.952 |  | True |
| zedge_ts_ar | long-series generator | 8.94 | 7 | 11 | 0.252 | 0.757 | 0.41 | True |
| zedge_zseries | optimised selection | 9.15 | 8.32 | 9.89 | 0.067 | 0.52 | 0.328 | True |
| zedge_greedy | optimised selection | 9.28 | 8.15 | 10.4 | 0.005 | 0.368 | 0.191 | True |
| zedge_pctsp | optimised selection | 9.54 | 8.32 | 10.8 | 0 | 0.088 | 0.322 | True |
| zedge_ts_long | long-series generator | 9.54 | 7.98 | 11.3 | 0.001 | 0.151 | 0.375 | True |
| zedge_atsp | optimised selection | 9.67 | 7.87 | 11.6 | 0.001 | 0.156 | 0.375 | True |
| zedge_knn | optimised selection | 10.1 | 8.85 | 11.4 | 0 | 0.001 | 0.0586 | True |
| timesfm | long-series generator | 11.9 | 9.5 | 14.1 | 0.002 | 0.007 | 0.191 | True |
| zedge_herding | optimised selection | 12 | 10.3 | 13.7 | 0 | 0 | 0.0586 | True |
| diffusion_ts | long-series generator | 12.1 | 10.6 | 13.6 | 0 | 0 | 0.0586 | True |
| zedge_mbb | optimised selection | 12.3 | 10.5 | 14.2 | 0 | 0 | 0.0449 | False |
| zedge_rand | random selection | 12.5 | 10.6 | 14.4 | 0 | 0 | 0.0449 | False |
| timestral | long-series generator | 13.5 | 11.9 | 15.2 | 0 | 0 | 0.0586 | True |
| vae_zseries | optimised selection | 13.7 | 12.1 | 15.2 | 0 | 0 | 0.0586 | True |
| chronos | long-series generator | 13.7 | 11.8 | 15.6 | 0 | 0 | 0.0625 | True |
| vae_quilting | optimised selection | 14.3 | 12.3 | 16.3 | 0 | 0 | 0.0586 | True |
| vae_herding | optimised selection | 14.6 | 13.6 | 15.6 | 0 | 0 | 0.0449 | False |
| vae_pctsp | optimised selection | 15 | 13.5 | 16.5 | 0 | 0 | 0.0449 | False |
| vae_atsp | optimised selection | 15.1 | 13.1 | 16.8 | 0 | 0 | 0.0449 | False |
| vae_greedy | optimised selection | 15.3 | 13.6 | 16.9 | 0 | 0 | 0.0586 | True |
| vae_knn | optimised selection | 15.9 | 13.9 | 17.8 | 0 | 0 | 0.0449 | False |
| vae_mbb | optimised selection | 16.8 | 14.4 | 18.8 | 0 | 0 | 0.0449 | False |
| vae_rand | random selection | 16.8 | 14.6 | 18.9 | 0 | 0 | 0.0449 | False |


### Ranking `train_clf`: Fidelity: train; utility: classification

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| zedge_quilting | optimised selection | 7.6 | 6.43 | 8.89 | 0.701 | 0.941 |  | True |
| zedge_pctsp | optimised selection | 8.13 | 7.39 | 8.91 | 0.038 | 0.585 | 0.451 | True |
| zedge_greedy | optimised selection | 8.17 | 7.45 | 8.99 | 0.011 | 0.493 | 0.322 | True |
| zedge_ts_ar | long-series generator | 8.27 | 6.69 | 9.95 | 0.162 | 0.451 | 0.451 | True |
| zedge_atsp | optimised selection | 8.37 | 7.31 | 9.53 | 0.001 | 0.213 | 0.322 | True |
| zedge_zseries | optimised selection | 8.37 | 7.93 | 8.84 | 0.087 | 0.306 | 0.451 | True |
| zedge_knn | optimised selection | 8.68 | 8.12 | 9.31 | 0 | 0.009 | 0.293 | True |
| zedge_ts_long | long-series generator | 8.97 | 7.8 | 10.2 | 0 | 0.002 | 0.109 | True |
| zedge_herding | optimised selection | 10.1 | 9.38 | 10.7 | 0 | 0 | 0.0586 | True |
| zedge_mbb | optimised selection | 10.1 | 9.31 | 10.9 | 0 | 0 | 0.0449 | False |
| zedge_rand | random selection | 10.3 | 9.41 | 11.1 | 0 | 0 | 0.0449 | False |
| vae_zseries | optimised selection | 14 | 12.7 | 15.3 | 0 | 0 | 0.0469 | False |
| vae_herding | optimised selection | 14.3 | 13.5 | 15 | 0 | 0 | 0.0449 | False |
| vae_quilting | optimised selection | 14.3 | 13 | 15.7 | 0 | 0 | 0.0469 | False |
| diffusion_ts | long-series generator | 14.4 | 12.4 | 16.1 | 0 | 0 | 0.0449 | False |
| vae_pctsp | optimised selection | 15.2 | 14.1 | 16.1 | 0 | 0 | 0.0449 | False |
| vae_atsp | optimised selection | 15.2 | 13.9 | 16.5 | 0 | 0 | 0.0449 | False |
| vae_greedy | optimised selection | 15.5 | 14.3 | 16.7 | 0 | 0 | 0.0449 | False |
| vae_knn | optimised selection | 16.1 | 14.9 | 17.2 | 0 | 0 | 0.0449 | False |
| vae_rand | random selection | 16.6 | 15.1 | 18 | 0 | 0 | 0.0449 | False |
| vae_mbb | optimised selection | 16.6 | 15.1 | 18 | 0 | 0 | 0.0449 | False |
| timesfm | long-series generator | 17 | 14.5 | 19.6 | 0 | 0 | 0.109 | True |
| chronos | long-series generator | 17.3 | 15.4 | 18.9 | 0 | 0 | 0.0703 | True |
| timestral | long-series generator | 19.5 | 18 | 20.7 | 0 | 0 | 0.0449 | False |


### Ranking `train_reg`: Fidelity: train; utility: regression

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| zedge_quilting | optimised selection | 7.67 | 6.58 | 8.84 | 0.562 | 0.93 |  | True |
| zedge_ts_ar | long-series generator | 8.05 | 6.19 | 10 | 0.293 | 0.74 | 0.41 | True |
| zedge_zseries | optimised selection | 8.24 | 7.55 | 8.88 | 0.135 | 0.543 | 0.41 | True |
| zedge_greedy | optimised selection | 8.36 | 7.46 | 9.27 | 0.009 | 0.406 | 0.387 | True |
| zedge_pctsp | optimised selection | 8.57 | 7.47 | 9.62 | 0 | 0.137 | 0.41 | True |
| zedge_atsp | optimised selection | 8.78 | 7.2 | 10.5 | 0 | 0.163 | 0.41 | True |
| zedge_ts_long | long-series generator | 8.86 | 7.49 | 10.4 | 0.001 | 0.081 | 0.41 | True |
| zedge_knn | optimised selection | 9.27 | 8.33 | 10.3 | 0 | 0 | 0.109 | True |
| zedge_herding | optimised selection | 11.5 | 9.94 | 13 | 0 | 0 | 0.0586 | True |
| zedge_mbb | optimised selection | 11.9 | 10.3 | 13.4 | 0 | 0 | 0.0449 | False |
| zedge_rand | random selection | 12 | 10.4 | 13.6 | 0 | 0 | 0.0449 | False |
| timesfm | long-series generator | 12.7 | 10.5 | 14.8 | 0 | 0 | 0.109 | True |
| diffusion_ts | long-series generator | 12.9 | 11.4 | 14.2 | 0 | 0 | 0.0449 | False |
| vae_zseries | optimised selection | 14 | 12.5 | 15.5 | 0 | 0 | 0.0449 | False |
| timestral | long-series generator | 14.7 | 13.2 | 16.2 | 0 | 0 | 0.0449 | False |
| chronos | long-series generator | 14.8 | 13.3 | 16.4 | 0 | 0 | 0.0703 | True |
| vae_quilting | optimised selection | 14.9 | 13 | 16.6 | 0 | 0 | 0.0449 | False |
| vae_herding | optimised selection | 14.9 | 14.1 | 15.8 | 0 | 0 | 0.0449 | False |
| vae_atsp | optimised selection | 15.6 | 13.9 | 17.2 | 0 | 0 | 0.0449 | False |
| vae_pctsp | optimised selection | 15.7 | 14.4 | 16.9 | 0 | 0 | 0.0449 | False |
| vae_greedy | optimised selection | 15.9 | 14.3 | 17.3 | 0 | 0 | 0.0449 | False |
| vae_knn | optimised selection | 16.6 | 14.9 | 18.1 | 0 | 0 | 0.0449 | False |
| vae_mbb | optimised selection | 17.5 | 15.6 | 19.2 | 0 | 0 | 0.0449 | False |
| vae_rand | random selection | 17.6 | 15.8 | 19.3 | 0 | 0 | 0.0449 | False |



## Core-metric rankings (RQ1)

The four rankings with the fidelity domain restricted to the core metric set, fixed in advance: distribution (F1.2_w1, F2.1_ks_d24); dependence (F3.5_log_psd, F4.1_how_mean); windows (F6.1_disc_score, F6.4_mmd); long structure (F7.1_roll_mean_ks, F7.2_roll_std_ks); target (F11.1_class_share_logratio); seams (F5.7_seam_detect_auc_dev). Utility unchanged. Each core ranking, the normalised scores (random assembly = 0, real data = 1) and the anchor check — `LEADERBOARD.md`.

| method | family | core_holdout_clf:rank | core_holdout_clf:p_first | core_holdout_clf:tier | core_holdout_reg:rank | core_holdout_reg:p_first | core_holdout_reg:tier | core_train_clf:rank | core_train_clf:p_first | core_train_clf:tier | core_train_reg:rank | core_train_reg:p_first | core_train_reg:tier | first_in |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| chronos | long-series generator | 16.6 | 0 | True | 14.2 | 0 | True | 17.8 | 0 | True | 15.4 | 0 | True |  |
| diffusion_ts | long-series generator | 14.1 | 0 | False | 12.6 | 0 | True | 15.1 | 0 | False | 13.6 | 0 | False |  |
| timesfm | long-series generator | 16.6 | 0 | True | 12.3 | 0 | True | 18 | 0 | True | 13.7 | 0 | True |  |
| timestral | long-series generator | 19.1 | 0 | False | 14.4 | 0 | False | 21.1 | 0 | False | 16.3 | 0 | False |  |
| zedge_ts_ar | long-series generator | 9.31 | 0.036 | True | 9.1 | 0.067 | True | 8.61 | 0.043 | True | 8.39 | 0.089 | True |  |
| zedge_ts_long | long-series generator | 9.22 | 0.007 | True | 9.12 | 0.019 | True | 8.65 | 0 | True | 8.54 | 0.005 | True |  |
| vae_atsp | optimised selection | 15.1 | 0 | True | 15.5 | 0 | False | 15.8 | 0 | False | 16.2 | 0 | False |  |
| vae_greedy | optimised selection | 15.4 | 0 | True | 15.8 | 0 | False | 16 | 0 | False | 16.4 | 0 | False |  |
| vae_herding | optimised selection | 13.5 | 0 | False | 14.2 | 0 | False | 13.4 | 0 | False | 14 | 0 | False |  |
| vae_knn | optimised selection | 15.8 | 0 | False | 16.3 | 0 | False | 16.5 | 0 | False | 17 | 0 | False |  |
| vae_mbb | optimised selection | 15.8 | 0 | False | 16.7 | 0 | False | 16.5 | 0 | False | 17.4 | 0 | False |  |
| vae_pctsp | optimised selection | 15 | 0 | True | 15.5 | 0 | False | 15.7 | 0 | False | 16.3 | 0 | False |  |
| vae_quilting | optimised selection | 14 | 0 | True | 14.6 | 0 | True | 14.7 | 0 | True | 15.2 | 0 | True |  |
| vae_zseries | optimised selection | 13.7 | 0 | True | 13.7 | 0 | True | 14.1 | 0 | True | 14.1 | 0 | False |  |
| zedge_atsp | optimised selection | 9.06 | 0.006 | True | 9.46 | 0.011 | True | 8.13 | 0.013 | True | 8.54 | 0.017 | True |  |
| zedge_greedy | optimised selection | 8.88 | 0.001 | True | 9.07 | 0.001 | True | 7.85 | 0.015 | True | 8.04 | 0.011 | True |  |
| zedge_herding | optimised selection | 10.2 | 0 | True | 11.6 | 0 | False | 9.38 | 0 | True | 10.8 | 0 | True |  |
| zedge_knn | optimised selection | 9.18 | 0 | True | 9.77 | 0 | True | 8.25 | 0 | True | 8.84 | 0 | True |  |
| zedge_mbb | optimised selection | 10.1 | 0 | False | 11.9 | 0 | True | 9.47 | 0 | True | 11.2 | 0 | True |  |
| zedge_pctsp | optimised selection | 8.94 | 0.002 | True | 9.38 | 0.001 | True | 7.82 | 0.042 | True | 8.25 | 0.005 | True |  |
| zedge_quilting | optimised selection | 7.86 | 0.924 | True | 7.93 | 0.824 | True | 7.25 | 0.717 | True | 7.32 | 0.622 | True | core_holdout_clf, core_holdout_reg, core_train_clf, core_train_reg |
| zedge_zseries | optimised selection | 8.92 | 0.024 | True | 8.78 | 0.077 | True | 7.83 | 0.17 | True | 7.7 | 0.251 | True |  |
| vae_rand | random selection | 15.9 | 0 | False | 16.9 | 0 | False | 16.5 | 0 | False | 17.5 | 0 | False |  |
| zedge_rand | random selection | 10.4 | 0 | True | 12 | 0 | False | 9.65 | 0 | True | 11.3 | 0 | True |  |


### Normalised scores on the core metrics (random assembly = 0, real data = 1)

| method | fidelity | utility | dependence | distribution | long_structure | target | windows | classification | regression |
|---|---|---|---|---|---|---|---|---|---|
| chronos | -0.334 | -0.176 | 0.108 | -0.637 | -0.0197 | -0.564 | -0.62 | -0.393 | 0.582 |
| diffusion_ts | 0.441 | 0.414 | 0.585 | 0.914 | 0.606 | 0.697 | 0.292 | 0.293 | 0.48 |
| timesfm | -0.0466 | 0.64 | -1.51 | 0.226 | 0.196 | -2.43 | -0.00282 | 0.392 | 0.873 |
| timestral | -0.186 | -0.0333 | -1.02 | 0.268 | -0 | -5.36 | 0.152 | -0.585 | 0.776 |
| zedge_ts_ar | 0.653 | 0.901 | 0.694 | 0.784 | 0.85 | 0.469 | 0.412 | 0.838 | 0.946 |
| zedge_ts_long | 0.8 | 0.74 | 0.786 | 0.977 | 0.573 | 0.911 | 0.876 | 0.661 | 0.829 |
| vae_atsp | 0.148 | 0.197 | -0.385 | 0.0692 | 0.258 | 0.294 | 0.185 | 0.139 | 0.217 |
| vae_greedy | -0.0413 | 0.141 | -0.314 | -0.0631 | -0.00249 | 0.216 | 0.15 | 0.0481 | 0.161 |
| vae_herding | 0.418 | 0.232 | 0.193 | 0.599 | 0.215 | 0.285 | 0.524 | 0.169 | 0.302 |
| vae_knn | 0.0737 | 0.0125 | -0.0394 | 0.137 | 0.341 | 0.193 | 0.19 | -0.011 | 0.0535 |
| vae_mbb | 0.11 | -0.013 | -0.025 | 0.0781 | 0.238 | 0.19 | 0.196 | -0.00218 | 0.0209 |
| vae_pctsp | 0.197 | 0.102 | 0.311 | 0.0886 | 0.239 | 0.36 | 0.45 | 0.035 | 0.055 |
| vae_quilting | 0.0957 | 0.152 | -0.635 | 0.0978 | 0.252 | 0.048 | 0.311 | 0.0921 | 0.218 |
| vae_zseries | 0.5 | 0.264 | 0.296 | 0.449 | 0.386 | 0.6 | 0.356 | 0.198 | 0.359 |
| zedge_atsp | 0.177 | 0.431 | 0.369 | 0.0454 | 0.141 | 0.286 | 0.691 | 0.363 | 0.347 |
| zedge_greedy | 0.177 | 0.411 | 0.294 | 0.189 | 0.209 | 0.503 | 0.114 | 0.323 | 0.347 |
| zedge_herding | 0.0373 | -0.0433 | 0.204 | 0.00217 | -0.0633 | 0.155 | 0.5 | -0.0301 | -0.061 |
| zedge_knn | 0.321 | 0.368 | 0.449 | 0.203 | 0.124 | 0.871 | 0.422 | 0.323 | 0.396 |
| zedge_mbb | 0.0211 | 0.00209 | 0.0636 | 0.0178 | 0.104 | 0.115 | 0.21 | 0.00565 | 0.0116 |
| zedge_pctsp | 0.0206 | 0.425 | 0.237 | 0.046 | 0.00861 | 0.0174 | 0.334 | 0.415 | 0.369 |
| zedge_quilting | 0.418 | 0.555 | 0.889 | 0.193 | 0.617 | 0.513 | 0.292 | 0.44 | 0.559 |
| zedge_zseries | 0.0411 | 0.474 | 0.463 | 0.142 | 0.105 | 0.108 | 0.0482 | 0.277 | 0.505 |
| vae_rand | -0 | -0 | -0 | -0 | -0 | -0 | -0 | 0 | -0 |
| zedge_rand | -0 | -0 | 0 | 0 | 0 | -0 | -0 | 0 | -0 |



## Summary

| Question | Verdicts by comparison |
|---|---|
| RQ0. Benchmark validity: noise, real-data ceiling, discriminative power and redundancy of the metrics | discriminative metrics: 219 of 282 |
| RQ1. Ranking of every method in every slice | first by ranking: holdout_clf — zedge_quilting (Friedman p = 3.66e-14); holdout_reg — zedge_quilting (Friedman p = 7.24e-10); train_clf — zedge_quilting (Friedman p = 6.47e-22); train_reg — zedge_quilting (Friedman p = 3.46e-17) |
| RQ2. Assembly from a window pool vs long-series generators | inconclusive: 2428 |
| RQ3. Within assembly: window selection × seam processing | same: 413, inconclusive: 2471 |
| RQ4. Does fidelity predict utility (which metrics, against which reference) | predictive pairs: 353 of 896 |
| RQ5. Gap to real data (TSTR / TRTR), stability over time and across models | worse than real: 120 |
| RQ6. Speed and cost: training and generation time, memory, Pareto front "quality × time" | fastest: timestral (1 s) |
| RQ8. Class balance: do methods preserve class shares (rare events especially) and what does an error cost | inconclusive: 647 |
| RQ9. Outliers and extremes: do methods preserve tails and outliers, and does it matter to the models | inconclusive: 782 |

## Research questions

### RQ0. Benchmark validity: noise, real-data ceiling, discriminative power and redundancy of the metrics

| unit | kind | group | reference | n_datasets | n_methods | p_friedman | spread_over_noise | p_friedman_bh | discriminative |
|---|---|---|---|---|---|---|---|---|---|
| F1.10_hill_err | fidelity | F1_marginal | val | 9 | 28 | 0.283 | 3.47 | 0.322 | False |
| F1.10_hill_err@oot | fidelity | F1_marginal | oot | 9 | 28 | 0.0737 | 2.74 | 0.0904 | False |
| F1.10_hill_err@train | fidelity | F1_marginal | train | 9 | 28 | 1.55e-18 | 3.5 | 1.12e-17 | True |
| F1.1_ks | fidelity | F1_marginal | val | 9 | 28 | 0.0259 | 7.79 | 0.0333 | True |
| F1.1_ks@oot | fidelity | F1_marginal | oot | 9 | 28 | 5.22e-05 | 10.8 | 8.41e-05 | True |
| F1.1_ks@train | fidelity | F1_marginal | train | 9 | 28 | 6.05e-28 | 8.38 | 4.27e-26 | True |
| F1.2_w1 | fidelity | F1_marginal | val | 9 | 28 | 0.0271 | 12.5 | 0.0347 | True |
| F1.2_w1@oot | fidelity | F1_marginal | oot | 9 | 28 | 0.000505 | 12.5 | 0.000766 | True |
| F1.2_w1@train | fidelity | F1_marginal | train | 9 | 28 | 9.74e-29 | 11.7 | 9.16e-27 | True |
| F1.3_ad | fidelity | F1_marginal | val | 9 | 28 | 0.0113 | 5.71 | 0.0152 | True |
| F1.3_ad@oot | fidelity | F1_marginal | oot | 9 | 28 | 5e-06 | 10 | 8.54e-06 | True |
| F1.3_ad@train | fidelity | F1_marginal | train | 9 | 28 | 8.62e-30 | 7.76 | 1.22e-27 | True |
| F1.4_qq_corr | fidelity | F1_marginal | val | 9 | 28 | 0.0136 | 1.49 | 0.018 | True |
| F1.4_qq_corr@oot | fidelity | F1_marginal | oot | 9 | 28 | 8.82e-15 | 2.04 | 3.95e-14 | True |
| F1.4_qq_corr@train | fidelity | F1_marginal | train | 9 | 28 | 9.43e-17 | 3.49 | 5.22e-16 | True |
| F1.5_q01_err | fidelity | F1_marginal | val | 9 | 28 | 0.0749 | 8.72 | 0.0914 | False |
| F1.5_q01_err@oot | fidelity | F1_marginal | oot | 9 | 28 | 0.0173 | 10.7 | 0.0228 | True |
| F1.5_q01_err@train | fidelity | F1_marginal | train | 9 | 28 | 5.12e-12 | 8.72 | 1.7e-11 | True |
| F1.5_q99_err | fidelity | F1_marginal | val | 9 | 28 | 0.555 | 7.16 | 0.602 | False |
| F1.5_q99_err@oot | fidelity | F1_marginal | oot | 9 | 28 | 0.58 | 3.61 | 0.622 | False |
| F1.5_q99_err@train | fidelity | F1_marginal | train | 9 | 28 | 2.79e-14 | 5.67 | 1.17e-13 | True |
| F1.5_quantile_err | fidelity | F1_marginal | val | 9 | 28 | 0.0274 | 9.68 | 0.035 | True |
| F1.5_quantile_err@oot | fidelity | F1_marginal | oot | 9 | 28 | 0.00102 | 10.3 | 0.00149 | True |
| F1.5_quantile_err@train | fidelity | F1_marginal | train | 9 | 28 | 1.43e-27 | 9.43 | 8.05e-26 | True |
| F1.6_kurt_err | fidelity | F1_marginal | val | 9 | 28 | 0.953 | 2.2 | 0.971 | False |
| F1.6_kurt_err@oot | fidelity | F1_marginal | oot | 9 | 28 | 0.175 | 2.16 | 0.201 | False |
| F1.6_kurt_err@train | fidelity | F1_marginal | train | 9 | 28 | 5.9e-20 | 2.93 | 5.2e-19 | True |
| F1.6_mean_err | fidelity | F1_marginal | val | 9 | 28 | 0.0776 | 12.5 | 0.094 | False |
| F1.6_mean_err@oot | fidelity | F1_marginal | oot | 9 | 28 | 0.000426 | 12.5 | 0.000652 | True |
| F1.6_mean_err@train | fidelity | F1_marginal | train | 9 | 28 | 1.35e-25 | 9.92 | 4.22e-24 | True |
| F1.6_skew_err | fidelity | F1_marginal | val | 9 | 28 | 0.107 | 2.53 | 0.128 | False |
| F1.6_skew_err@oot | fidelity | F1_marginal | oot | 9 | 28 | 0.0126 | 3.38 | 0.0168 | True |
| F1.6_skew_err@train | fidelity | F1_marginal | train | 9 | 28 | 1.17e-12 | 3.46 | 4.18e-12 | True |
| F1.6_std_err | fidelity | F1_marginal | val | 9 | 28 | 0.842 | 2.89 | 0.876 | False |
| F1.6_std_err@oot | fidelity | F1_marginal | oot | 9 | 28 | 0.555 | 2.89 | 0.602 | False |
| F1.6_std_err@train | fidelity | F1_marginal | train | 9 | 28 | 3.43e-10 | 2.77 | 8.87e-10 | True |
| F1.7_out_of_range | fidelity | F1_marginal | val | 9 | 28 | 0.573 | 4.33 | 0.617 | False |
| F1.7_out_of_range@oot | fidelity | F1_marginal | oot | 9 | 28 | 5.68e-17 | 2.04 | 3.2e-16 | True |
| F1.7_out_of_range@train | fidelity | F1_marginal | train | 9 | 28 | 0.519 |  | 0.574 | False |
| F1.8_coverage | fidelity | F1_marginal | val | 9 | 28 | 2.64e-09 | 4.46 | 5.95e-09 | True |

_Showing 40 rows of 282; all of them — `hypotheses/RQ0_global.parquet`._

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
| fidelity | F3_dependence | 0.89 | 1 | 0.56 |
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
| ranking:holdout_clf | 3.66e-14 | 11 | 9 | 22 | zedge_quilting |
| with_cost:holdout_clf | 7e-13 | 11 | 9 | 22 | zedge_quilting |
| ranking:holdout_reg | 7.24e-10 | 11 | 9 | 22 | zedge_quilting |
| with_cost:holdout_reg | 2.11e-09 | 11 | 9 | 22 | zedge_quilting |
| ranking:train_clf | 6.47e-22 | 11 | 9 | 22 | zedge_quilting |
| with_cost:train_clf | 1.42e-20 | 11 | 9 | 22 | zedge_quilting |
| ranking:train_reg | 3.46e-17 | 11 | 9 | 22 | zedge_quilting |
| with_cost:train_reg | 3.44e-14 | 11 | 9 | 22 | zedge_quilting |
| ranking:core_holdout_clf | 3.31e-12 | 11 | 9 | 22 | zedge_quilting |
| ranking:core_holdout_reg | 2.2e-09 | 11 | 9 | 22 | zedge_quilting |
| ranking:core_train_clf | 2.82e-21 | 11 | 9 | 22 | zedge_quilting |
| ranking:core_train_reg | 2.73e-17 | 11 | 9 | 22 | zedge_quilting |
| domain:fidelity@train | 6.61e-24 | 11 | 9 | 22 | zedge_quilting |
| domain:fidelity@val | 1.96e-06 | 11 | 9 | 22 | zedge_quilting |
| domain:fidelity@oot | 5.73e-12 | 11 | 9 | 22 | zedge_quilting |
| domain:fidelity@all | 8.31e-19 | 11 | 9 | 22 | zedge_quilting |
| domain:utility@val | 7.62e-09 | 11 | 9 | 22 | zedge_ts_ar |
| domain:utility@oot | 7.54e-10 | 11 | 9 | 22 | zedge_quilting |
| domain:utility@all | 9.92e-12 | 11 | 9 | 22 | zedge_quilting |
| cost@generation | 7.75e-29 | 11 | 9 | 22 | vae_rand |
| cost@memory | 5.2e-26 | 11 | 9 | 22 | zedge_ts_ar |
| cost@total | 6.04e-29 | 11 | 9 | 22 | timestral |
| cost@training | 6.04e-29 | 11 | 9 | 22 | timestral |
| fidelity:dependence@oot | 5.98e-08 | 11 | 9 | 22 | zedge_quilting |
| fidelity:dependence@train | 3.53e-19 | 11 | 9 | 22 | zedge_quilting |
| fidelity:dependence@val | 5.79e-07 | 11 | 9 | 22 | zedge_quilting |
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
| fidelity:target@oot | 9.28e-10 | 11 | 9 | 22 | zedge_quilting |
| fidelity:target@train | 2.33e-19 | 11 | 9 | 22 | zedge_zseries |
| fidelity:target@val | 1.09e-09 | 11 | 9 | 22 | zedge_atsp |
| fidelity:windows@oot | 1.01e-05 | 11 | 9 | 22 | zedge_quilting |

_Showing 40 rows of 56; all of them — `hypotheses/RQ1_global.parquet`._

**ranking_holdout_clf**

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| zedge_quilting | optimised selection | 8.31 | 7.25 | 9.45 | 0.844 | 0.985 |  | True |
| zedge_greedy | optimised selection | 9.08 | 8.18 | 10.1 | 0.002 | 0.479 | 0.117 | True |
| zedge_pctsp | optimised selection | 9.1 | 8.24 | 9.97 | 0.006 | 0.495 | 0.193 | True |
| zedge_ts_ar | long-series generator | 9.15 | 7.52 | 10.8 | 0.119 | 0.464 | 0.193 | True |
| zedge_atsp | optimised selection | 9.27 | 8.01 | 10.6 | 0.003 | 0.255 | 0.193 | True |
| zedge_zseries | optimised selection | 9.29 | 8.88 | 9.74 | 0.026 | 0.302 | 0.148 | True |
| zedge_knn | optimised selection | 9.51 | 8.73 | 10.4 | 0 | 0.007 | 0.0781 | True |
| zedge_ts_long | long-series generator | 9.65 | 8.31 | 11 | 0 | 0.013 | 0.117 | True |
| zedge_mbb | optimised selection | 10.6 | 9.56 | 11.6 | 0 | 0 | 0.0449 | False |
| zedge_herding | optimised selection | 10.6 | 9.74 | 11.4 | 0 | 0 | 0.0449 | False |
| zedge_rand | random selection | 10.8 | 9.65 | 11.9 | 0 | 0 | 0.0449 | False |
| vae_zseries | optimised selection | 13.6 | 12.3 | 14.9 | 0 | 0 | 0.0508 | True |
| diffusion_ts | long-series generator | 13.7 | 11.7 | 15.4 | 0 | 0 | 0.0449 | False |
| vae_quilting | optimised selection | 13.8 | 12.3 | 15.2 | 0 | 0 | 0.0508 | True |
| vae_herding | optimised selection | 14 | 13.3 | 14.7 | 0 | 0 | 0.0449 | False |
| vae_pctsp | optimised selection | 14.5 | 13.2 | 15.7 | 0 | 0 | 0.0449 | False |
| vae_atsp | optimised selection | 14.6 | 13.1 | 16.1 | 0 | 0 | 0.0508 | True |
| vae_greedy | optimised selection | 15 | 13.7 | 16.3 | 0 | 0 | 0.0508 | True |
| vae_knn | optimised selection | 15.4 | 13.9 | 16.8 | 0 | 0 | 0.0449 | False |
| vae_rand | random selection | 15.8 | 14 | 17.6 | 0 | 0 | 0.0449 | False |
| vae_mbb | optimised selection | 15.9 | 14 | 17.6 | 0 | 0 | 0.0449 | False |
| chronos | long-series generator | 16.1 | 14 | 18 | 0 | 0 | 0.0703 | True |
| timesfm | long-series generator | 16.2 | 13.6 | 18.7 | 0 | 0 | 0.109 | True |
| timestral | long-series generator | 18.3 | 17 | 19.5 | 0 | 0 | 0.0449 | False |


**ranking_holdout_reg**

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| zedge_quilting | optimised selection | 8.39 | 7.35 | 9.38 | 0.672 | 0.952 |  | True |
| zedge_ts_ar | long-series generator | 8.94 | 7 | 11 | 0.252 | 0.757 | 0.41 | True |
| zedge_zseries | optimised selection | 9.15 | 8.32 | 9.89 | 0.067 | 0.52 | 0.328 | True |
| zedge_greedy | optimised selection | 9.28 | 8.15 | 10.4 | 0.005 | 0.368 | 0.191 | True |
| zedge_pctsp | optimised selection | 9.54 | 8.32 | 10.8 | 0 | 0.088 | 0.322 | True |
| zedge_ts_long | long-series generator | 9.54 | 7.98 | 11.3 | 0.001 | 0.151 | 0.375 | True |
| zedge_atsp | optimised selection | 9.67 | 7.87 | 11.6 | 0.001 | 0.156 | 0.375 | True |
| zedge_knn | optimised selection | 10.1 | 8.85 | 11.4 | 0 | 0.001 | 0.0586 | True |
| timesfm | long-series generator | 11.9 | 9.5 | 14.1 | 0.002 | 0.007 | 0.191 | True |
| zedge_herding | optimised selection | 12 | 10.3 | 13.7 | 0 | 0 | 0.0586 | True |
| diffusion_ts | long-series generator | 12.1 | 10.6 | 13.6 | 0 | 0 | 0.0586 | True |
| zedge_mbb | optimised selection | 12.3 | 10.5 | 14.2 | 0 | 0 | 0.0449 | False |
| zedge_rand | random selection | 12.5 | 10.6 | 14.4 | 0 | 0 | 0.0449 | False |
| timestral | long-series generator | 13.5 | 11.9 | 15.2 | 0 | 0 | 0.0586 | True |
| vae_zseries | optimised selection | 13.7 | 12.1 | 15.2 | 0 | 0 | 0.0586 | True |
| chronos | long-series generator | 13.7 | 11.8 | 15.6 | 0 | 0 | 0.0625 | True |
| vae_quilting | optimised selection | 14.3 | 12.3 | 16.3 | 0 | 0 | 0.0586 | True |
| vae_herding | optimised selection | 14.6 | 13.6 | 15.6 | 0 | 0 | 0.0449 | False |
| vae_pctsp | optimised selection | 15 | 13.5 | 16.5 | 0 | 0 | 0.0449 | False |
| vae_atsp | optimised selection | 15.1 | 13.1 | 16.8 | 0 | 0 | 0.0449 | False |
| vae_greedy | optimised selection | 15.3 | 13.6 | 16.9 | 0 | 0 | 0.0586 | True |
| vae_knn | optimised selection | 15.9 | 13.9 | 17.8 | 0 | 0 | 0.0449 | False |
| vae_mbb | optimised selection | 16.8 | 14.4 | 18.8 | 0 | 0 | 0.0449 | False |
| vae_rand | random selection | 16.8 | 14.6 | 18.9 | 0 | 0 | 0.0449 | False |


**ranking_train_clf**

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| zedge_quilting | optimised selection | 7.6 | 6.43 | 8.89 | 0.701 | 0.941 |  | True |
| zedge_pctsp | optimised selection | 8.13 | 7.39 | 8.91 | 0.038 | 0.585 | 0.451 | True |
| zedge_greedy | optimised selection | 8.17 | 7.45 | 8.99 | 0.011 | 0.493 | 0.322 | True |
| zedge_ts_ar | long-series generator | 8.27 | 6.69 | 9.95 | 0.162 | 0.451 | 0.451 | True |
| zedge_atsp | optimised selection | 8.37 | 7.31 | 9.53 | 0.001 | 0.213 | 0.322 | True |
| zedge_zseries | optimised selection | 8.37 | 7.93 | 8.84 | 0.087 | 0.306 | 0.451 | True |
| zedge_knn | optimised selection | 8.68 | 8.12 | 9.31 | 0 | 0.009 | 0.293 | True |
| zedge_ts_long | long-series generator | 8.97 | 7.8 | 10.2 | 0 | 0.002 | 0.109 | True |
| zedge_herding | optimised selection | 10.1 | 9.38 | 10.7 | 0 | 0 | 0.0586 | True |
| zedge_mbb | optimised selection | 10.1 | 9.31 | 10.9 | 0 | 0 | 0.0449 | False |
| zedge_rand | random selection | 10.3 | 9.41 | 11.1 | 0 | 0 | 0.0449 | False |
| vae_zseries | optimised selection | 14 | 12.7 | 15.3 | 0 | 0 | 0.0469 | False |
| vae_herding | optimised selection | 14.3 | 13.5 | 15 | 0 | 0 | 0.0449 | False |
| vae_quilting | optimised selection | 14.3 | 13 | 15.7 | 0 | 0 | 0.0469 | False |
| diffusion_ts | long-series generator | 14.4 | 12.4 | 16.1 | 0 | 0 | 0.0449 | False |
| vae_pctsp | optimised selection | 15.2 | 14.1 | 16.1 | 0 | 0 | 0.0449 | False |
| vae_atsp | optimised selection | 15.2 | 13.9 | 16.5 | 0 | 0 | 0.0449 | False |
| vae_greedy | optimised selection | 15.5 | 14.3 | 16.7 | 0 | 0 | 0.0449 | False |
| vae_knn | optimised selection | 16.1 | 14.9 | 17.2 | 0 | 0 | 0.0449 | False |
| vae_rand | random selection | 16.6 | 15.1 | 18 | 0 | 0 | 0.0449 | False |
| vae_mbb | optimised selection | 16.6 | 15.1 | 18 | 0 | 0 | 0.0449 | False |
| timesfm | long-series generator | 17 | 14.5 | 19.6 | 0 | 0 | 0.109 | True |
| chronos | long-series generator | 17.3 | 15.4 | 18.9 | 0 | 0 | 0.0703 | True |
| timestral | long-series generator | 19.5 | 18 | 20.7 | 0 | 0 | 0.0449 | False |


**ranking_train_reg**

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| zedge_quilting | optimised selection | 7.67 | 6.58 | 8.84 | 0.562 | 0.93 |  | True |
| zedge_ts_ar | long-series generator | 8.05 | 6.19 | 10 | 0.293 | 0.74 | 0.41 | True |
| zedge_zseries | optimised selection | 8.24 | 7.55 | 8.88 | 0.135 | 0.543 | 0.41 | True |
| zedge_greedy | optimised selection | 8.36 | 7.46 | 9.27 | 0.009 | 0.406 | 0.387 | True |
| zedge_pctsp | optimised selection | 8.57 | 7.47 | 9.62 | 0 | 0.137 | 0.41 | True |
| zedge_atsp | optimised selection | 8.78 | 7.2 | 10.5 | 0 | 0.163 | 0.41 | True |
| zedge_ts_long | long-series generator | 8.86 | 7.49 | 10.4 | 0.001 | 0.081 | 0.41 | True |
| zedge_knn | optimised selection | 9.27 | 8.33 | 10.3 | 0 | 0 | 0.109 | True |
| zedge_herding | optimised selection | 11.5 | 9.94 | 13 | 0 | 0 | 0.0586 | True |
| zedge_mbb | optimised selection | 11.9 | 10.3 | 13.4 | 0 | 0 | 0.0449 | False |
| zedge_rand | random selection | 12 | 10.4 | 13.6 | 0 | 0 | 0.0449 | False |
| timesfm | long-series generator | 12.7 | 10.5 | 14.8 | 0 | 0 | 0.109 | True |
| diffusion_ts | long-series generator | 12.9 | 11.4 | 14.2 | 0 | 0 | 0.0449 | False |
| vae_zseries | optimised selection | 14 | 12.5 | 15.5 | 0 | 0 | 0.0449 | False |
| timestral | long-series generator | 14.7 | 13.2 | 16.2 | 0 | 0 | 0.0449 | False |
| chronos | long-series generator | 14.8 | 13.3 | 16.4 | 0 | 0 | 0.0703 | True |
| vae_quilting | optimised selection | 14.9 | 13 | 16.6 | 0 | 0 | 0.0449 | False |
| vae_herding | optimised selection | 14.9 | 14.1 | 15.8 | 0 | 0 | 0.0449 | False |
| vae_atsp | optimised selection | 15.6 | 13.9 | 17.2 | 0 | 0 | 0.0449 | False |
| vae_pctsp | optimised selection | 15.7 | 14.4 | 16.9 | 0 | 0 | 0.0449 | False |
| vae_greedy | optimised selection | 15.9 | 14.3 | 17.3 | 0 | 0 | 0.0449 | False |
| vae_knn | optimised selection | 16.6 | 14.9 | 18.1 | 0 | 0 | 0.0449 | False |
| vae_mbb | optimised selection | 17.5 | 15.6 | 19.2 | 0 | 0 | 0.0449 | False |
| vae_rand | random selection | 17.6 | 15.8 | 19.3 | 0 | 0 | 0.0449 | False |


**ranking_core_holdout_clf**

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| zedge_quilting | optimised selection | 7.86 | 6.73 | 9.03 | 0.924 | 0.99 |  | True |
| zedge_greedy | optimised selection | 8.88 | 7.84 | 10 | 0.001 | 0.492 | 0.109 | True |
| zedge_zseries | optimised selection | 8.92 | 8.32 | 9.64 | 0.024 | 0.465 | 0.148 | True |
| zedge_pctsp | optimised selection | 8.94 | 7.82 | 10.1 | 0.002 | 0.358 | 0.148 | True |
| zedge_atsp | optimised selection | 9.06 | 7.6 | 10.6 | 0.006 | 0.252 | 0.148 | True |
| zedge_knn | optimised selection | 9.18 | 8.27 | 10.2 | 0 | 0.049 | 0.109 | True |
| zedge_ts_long | long-series generator | 9.22 | 7.69 | 10.9 | 0.007 | 0.196 | 0.137 | True |
| zedge_ts_ar | long-series generator | 9.31 | 7.64 | 11 | 0.036 | 0.198 | 0.148 | True |
| zedge_mbb | optimised selection | 10.1 | 8.94 | 11.5 | 0 | 0 | 0.0449 | False |
| zedge_herding | optimised selection | 10.2 | 9.28 | 11.2 | 0 | 0 | 0.0625 | True |
| zedge_rand | random selection | 10.4 | 9.03 | 11.7 | 0 | 0 | 0.0625 | True |
| vae_herding | optimised selection | 13.5 | 12.9 | 14.2 | 0 | 0 | 0.0449 | False |
| vae_zseries | optimised selection | 13.7 | 12.2 | 15.2 | 0 | 0 | 0.0625 | True |
| vae_quilting | optimised selection | 14 | 12.3 | 15.7 | 0 | 0 | 0.0625 | True |
| diffusion_ts | long-series generator | 14.1 | 11.9 | 16 | 0 | 0 | 0.0449 | False |
| vae_pctsp | optimised selection | 15 | 13.5 | 16.5 | 0 | 0 | 0.0625 | True |
| vae_atsp | optimised selection | 15.1 | 13.1 | 17 | 0 | 0 | 0.0625 | True |
| vae_greedy | optimised selection | 15.4 | 13.8 | 17.1 | 0 | 0 | 0.0625 | True |
| vae_knn | optimised selection | 15.8 | 14 | 17.5 | 0 | 0 | 0.0449 | False |
| vae_mbb | optimised selection | 15.8 | 13.8 | 17.7 | 0 | 0 | 0.0449 | False |
| vae_rand | random selection | 15.9 | 13.9 | 17.7 | 0 | 0 | 0.0449 | False |
| chronos | long-series generator | 16.6 | 14.5 | 18.5 | 0 | 0 | 0.0703 | True |
| timesfm | long-series generator | 16.6 | 14.7 | 18.6 | 0 | 0 | 0.109 | True |
| timestral | long-series generator | 19.1 | 17.8 | 20.4 | 0 | 0 | 0.0449 | False |


**ranking_core_holdout_reg**

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| zedge_quilting | optimised selection | 7.93 | 6.81 | 8.96 | 0.824 | 0.966 |  | True |
| zedge_zseries | optimised selection | 8.78 | 7.82 | 9.7 | 0.077 | 0.589 | 0.375 | True |
| zedge_greedy | optimised selection | 9.07 | 7.88 | 10.3 | 0.001 | 0.37 | 0.164 | True |
| zedge_ts_ar | long-series generator | 9.1 | 7.03 | 11.2 | 0.067 | 0.453 | 0.375 | True |
| zedge_ts_long | long-series generator | 9.12 | 7.3 | 11.2 | 0.019 | 0.388 | 0.375 | True |
| zedge_pctsp | optimised selection | 9.38 | 7.99 | 10.9 | 0.001 | 0.07 | 0.186 | True |
| zedge_atsp | optimised selection | 9.46 | 7.48 | 11.6 | 0.011 | 0.158 | 0.328 | True |
| zedge_knn | optimised selection | 9.77 | 8.47 | 11.3 | 0 | 0.005 | 0.109 | True |
| zedge_herding | optimised selection | 11.6 | 9.79 | 13.5 | 0 | 0 | 0.0449 | False |
| zedge_mbb | optimised selection | 11.9 | 9.9 | 14.1 | 0 | 0 | 0.0508 | True |
| zedge_rand | random selection | 12 | 9.97 | 14.3 | 0 | 0 | 0.0449 | False |
| timesfm | long-series generator | 12.3 | 10.5 | 13.9 | 0 | 0 | 0.109 | True |
| diffusion_ts | long-series generator | 12.6 | 10.7 | 14.4 | 0 | 0 | 0.0508 | True |
| vae_zseries | optimised selection | 13.7 | 11.9 | 15.5 | 0 | 0.001 | 0.0508 | True |
| vae_herding | optimised selection | 14.2 | 13.5 | 15 | 0 | 0 | 0.0449 | False |
| chronos | long-series generator | 14.2 | 12.2 | 16 | 0 | 0 | 0.0703 | True |
| timestral | long-series generator | 14.4 | 12.8 | 16.2 | 0 | 0 | 0.0449 | False |
| vae_quilting | optimised selection | 14.6 | 12.4 | 16.8 | 0 | 0 | 0.0586 | True |
| vae_pctsp | optimised selection | 15.5 | 13.8 | 17.2 | 0 | 0 | 0.0449 | False |
| vae_atsp | optimised selection | 15.5 | 13.2 | 17.6 | 0 | 0 | 0.0449 | False |
| vae_greedy | optimised selection | 15.8 | 13.8 | 17.7 | 0 | 0 | 0.0449 | False |
| vae_knn | optimised selection | 16.3 | 14.1 | 18.4 | 0 | 0 | 0.0449 | False |
| vae_mbb | optimised selection | 16.7 | 14.3 | 18.9 | 0 | 0 | 0.0449 | False |
| vae_rand | random selection | 16.9 | 14.6 | 19 | 0 | 0 | 0.0449 | False |


**ranking_core_train_clf**

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| zedge_quilting | optimised selection | 7.25 | 6.04 | 8.61 | 0.717 | 0.922 |  | True |
| zedge_pctsp | optimised selection | 7.82 | 6.89 | 8.79 | 0.042 | 0.603 | 0.387 | True |
| zedge_zseries | optimised selection | 7.83 | 7.2 | 8.46 | 0.17 | 0.533 | 0.387 | True |
| zedge_greedy | optimised selection | 7.85 | 7.08 | 8.82 | 0.015 | 0.532 | 0.387 | True |
| zedge_atsp | optimised selection | 8.13 | 6.95 | 9.53 | 0.013 | 0.225 | 0.387 | True |
| zedge_knn | optimised selection | 8.25 | 7.59 | 8.97 | 0 | 0.036 | 0.387 | True |
| zedge_ts_ar | long-series generator | 8.61 | 7.02 | 10.3 | 0.043 | 0.127 | 0.387 | True |
| zedge_ts_long | long-series generator | 8.65 | 7.34 | 10 | 0 | 0.022 | 0.26 | True |
| zedge_herding | optimised selection | 9.38 | 8.69 | 10.1 | 0 | 0 | 0.0879 | True |
| zedge_mbb | optimised selection | 9.47 | 8.71 | 10.3 | 0 | 0 | 0.0547 | True |
| zedge_rand | random selection | 9.65 | 8.77 | 10.5 | 0 | 0 | 0.0547 | True |
| vae_herding | optimised selection | 13.4 | 12.9 | 14 | 0 | 0 | 0.0449 | False |
| vae_zseries | optimised selection | 14.1 | 12.5 | 15.6 | 0 | 0 | 0.0547 | True |
| vae_quilting | optimised selection | 14.7 | 13.2 | 16.1 | 0 | 0 | 0.0547 | True |
| diffusion_ts | long-series generator | 15.1 | 13 | 17 | 0 | 0 | 0.0449 | False |
| vae_pctsp | optimised selection | 15.7 | 14.7 | 16.8 | 0 | 0 | 0.0449 | False |
| vae_atsp | optimised selection | 15.8 | 14.3 | 17.2 | 0 | 0 | 0.0449 | False |
| vae_greedy | optimised selection | 16 | 14.6 | 17.3 | 0 | 0 | 0.0449 | False |
| vae_knn | optimised selection | 16.5 | 15.1 | 17.8 | 0 | 0 | 0.0449 | False |
| vae_mbb | optimised selection | 16.5 | 14.9 | 17.9 | 0 | 0 | 0.0449 | False |
| vae_rand | random selection | 16.5 | 15.1 | 18 | 0 | 0 | 0.0449 | False |
| chronos | long-series generator | 17.8 | 16 | 19.4 | 0 | 0 | 0.0781 | True |
| timesfm | long-series generator | 18 | 16.1 | 20.3 | 0 | 0 | 0.125 | True |
| timestral | long-series generator | 21.1 | 19.7 | 22.2 | 0 | 0 | 0.0449 | False |


**ranking_core_train_reg**

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| zedge_quilting | optimised selection | 7.32 | 6.19 | 8.52 | 0.622 | 0.906 |  | True |
| zedge_zseries | optimised selection | 7.7 | 6.85 | 8.48 | 0.251 | 0.72 | 0.492 | True |
| zedge_greedy | optimised selection | 8.04 | 7.23 | 9 | 0.011 | 0.537 | 0.492 | True |
| zedge_pctsp | optimised selection | 8.25 | 7.1 | 9.42 | 0.005 | 0.229 | 0.492 | True |
| zedge_ts_ar | long-series generator | 8.39 | 6.5 | 10.4 | 0.089 | 0.307 | 0.492 | True |
| zedge_atsp | optimised selection | 8.54 | 6.87 | 10.4 | 0.017 | 0.169 | 0.492 | True |
| zedge_ts_long | long-series generator | 8.54 | 6.97 | 10.3 | 0.005 | 0.13 | 0.492 | True |
| zedge_knn | optimised selection | 8.84 | 7.9 | 9.86 | 0 | 0.002 | 0.191 | True |
| zedge_herding | optimised selection | 10.8 | 9.24 | 12.4 | 0 | 0 | 0.0879 | True |
| zedge_mbb | optimised selection | 11.2 | 9.67 | 12.9 | 0 | 0 | 0.0508 | True |
| zedge_rand | random selection | 11.3 | 9.72 | 13.1 | 0 | 0 | 0.0508 | True |
| diffusion_ts | long-series generator | 13.6 | 12 | 15.1 | 0 | 0 | 0.0449 | False |
| timesfm | long-series generator | 13.7 | 12.1 | 15.2 | 0 | 0 | 0.125 | True |
| vae_herding | optimised selection | 14 | 13.3 | 14.7 | 0 | 0 | 0.0449 | False |
| vae_zseries | optimised selection | 14.1 | 12.4 | 15.9 | 0 | 0 | 0.0449 | False |
| vae_quilting | optimised selection | 15.2 | 13.2 | 17.2 | 0 | 0 | 0.0508 | True |
| chronos | long-series generator | 15.4 | 13.7 | 16.9 | 0 | 0 | 0.0781 | True |
| vae_atsp | optimised selection | 16.2 | 14.4 | 17.9 | 0 | 0 | 0.0449 | False |
| timestral | long-series generator | 16.3 | 15 | 17.5 | 0 | 0 | 0.0449 | False |
| vae_pctsp | optimised selection | 16.3 | 15 | 17.5 | 0 | 0 | 0.0449 | False |
| vae_greedy | optimised selection | 16.4 | 14.6 | 17.9 | 0 | 0 | 0.0449 | False |
| vae_knn | optimised selection | 17 | 15.2 | 18.6 | 0 | 0 | 0.0449 | False |
| vae_mbb | optimised selection | 17.4 | 15.4 | 19.2 | 0 | 0 | 0.0449 | False |
| vae_rand | random selection | 17.5 | 15.7 | 19.4 | 0 | 0 | 0.0449 | False |


**rankings**

| family | holdout_clf:rank | holdout_clf:p_first | holdout_clf:tier | holdout_reg:rank | holdout_reg:p_first | holdout_reg:tier | train_clf:rank | train_clf:p_first | train_clf:tier | train_reg:rank | train_reg:p_first | train_reg:tier | first_in |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| long-series generator | 16.1 | 0 | True | 13.7 | 0 | True | 17.3 | 0 | True | 14.8 | 0 | True |  |
| long-series generator | 13.7 | 0 | False | 12.1 | 0 | True | 14.4 | 0 | False | 12.9 | 0 | False |  |
| long-series generator | 16.2 | 0 | True | 11.9 | 0.002 | True | 17 | 0 | True | 12.7 | 0 | True |  |
| long-series generator | 18.3 | 0 | False | 13.5 | 0 | True | 19.5 | 0 | False | 14.7 | 0 | False |  |
| long-series generator | 9.15 | 0.119 | True | 8.94 | 0.252 | True | 8.27 | 0.162 | True | 8.05 | 0.293 | True |  |
| long-series generator | 9.65 | 0 | True | 9.54 | 0.001 | True | 8.97 | 0 | True | 8.86 | 0.001 | True |  |
| optimised selection | 14.6 | 0 | True | 15.1 | 0 | False | 15.2 | 0 | False | 15.6 | 0 | False |  |
| optimised selection | 15 | 0 | True | 15.3 | 0 | True | 15.5 | 0 | False | 15.9 | 0 | False |  |
| optimised selection | 14 | 0 | False | 14.6 | 0 | False | 14.3 | 0 | False | 14.9 | 0 | False |  |
| optimised selection | 15.4 | 0 | False | 15.9 | 0 | False | 16.1 | 0 | False | 16.6 | 0 | False |  |
| optimised selection | 15.9 | 0 | False | 16.8 | 0 | False | 16.6 | 0 | False | 17.5 | 0 | False |  |
| optimised selection | 14.5 | 0 | False | 15 | 0 | False | 15.2 | 0 | False | 15.7 | 0 | False |  |
| optimised selection | 13.8 | 0 | True | 14.3 | 0 | True | 14.3 | 0 | False | 14.9 | 0 | False |  |
| optimised selection | 13.6 | 0 | True | 13.7 | 0 | True | 14 | 0 | False | 14 | 0 | False |  |
| optimised selection | 9.27 | 0.003 | True | 9.67 | 0.001 | True | 8.37 | 0.001 | True | 8.78 | 0 | True |  |
| optimised selection | 9.08 | 0.002 | True | 9.28 | 0.005 | True | 8.17 | 0.011 | True | 8.36 | 0.009 | True |  |
| optimised selection | 10.6 | 0 | False | 12 | 0 | True | 10.1 | 0 | True | 11.5 | 0 | True |  |
| optimised selection | 9.51 | 0 | True | 10.1 | 0 | True | 8.68 | 0 | True | 9.27 | 0 | True |  |
| optimised selection | 10.6 | 0 | False | 12.3 | 0 | False | 10.1 | 0 | False | 11.9 | 0 | False |  |
| optimised selection | 9.1 | 0.006 | True | 9.54 | 0 | True | 8.13 | 0.038 | True | 8.57 | 0 | True |  |
| optimised selection | 8.31 | 0.844 | True | 8.39 | 0.672 | True | 7.6 | 0.701 | True | 7.67 | 0.562 | True | holdout_clf, holdout_reg, train_clf, train_reg |
| optimised selection | 9.29 | 0.026 | True | 9.15 | 0.067 | True | 8.37 | 0.087 | True | 8.24 | 0.135 | True |  |
| random selection | 15.8 | 0 | False | 16.8 | 0 | False | 16.6 | 0 | False | 17.6 | 0 | False |  |
| random selection | 10.8 | 0 | False | 12.5 | 0 | False | 10.3 | 0 | False | 12 | 0 | False |  |


**rankings_core**

| family | core_holdout_clf:rank | core_holdout_clf:p_first | core_holdout_clf:tier | core_holdout_reg:rank | core_holdout_reg:p_first | core_holdout_reg:tier | core_train_clf:rank | core_train_clf:p_first | core_train_clf:tier | core_train_reg:rank | core_train_reg:p_first | core_train_reg:tier | first_in |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| long-series generator | 16.6 | 0 | True | 14.2 | 0 | True | 17.8 | 0 | True | 15.4 | 0 | True |  |
| long-series generator | 14.1 | 0 | False | 12.6 | 0 | True | 15.1 | 0 | False | 13.6 | 0 | False |  |
| long-series generator | 16.6 | 0 | True | 12.3 | 0 | True | 18 | 0 | True | 13.7 | 0 | True |  |
| long-series generator | 19.1 | 0 | False | 14.4 | 0 | False | 21.1 | 0 | False | 16.3 | 0 | False |  |
| long-series generator | 9.31 | 0.036 | True | 9.1 | 0.067 | True | 8.61 | 0.043 | True | 8.39 | 0.089 | True |  |
| long-series generator | 9.22 | 0.007 | True | 9.12 | 0.019 | True | 8.65 | 0 | True | 8.54 | 0.005 | True |  |
| optimised selection | 15.1 | 0 | True | 15.5 | 0 | False | 15.8 | 0 | False | 16.2 | 0 | False |  |
| optimised selection | 15.4 | 0 | True | 15.8 | 0 | False | 16 | 0 | False | 16.4 | 0 | False |  |
| optimised selection | 13.5 | 0 | False | 14.2 | 0 | False | 13.4 | 0 | False | 14 | 0 | False |  |
| optimised selection | 15.8 | 0 | False | 16.3 | 0 | False | 16.5 | 0 | False | 17 | 0 | False |  |
| optimised selection | 15.8 | 0 | False | 16.7 | 0 | False | 16.5 | 0 | False | 17.4 | 0 | False |  |
| optimised selection | 15 | 0 | True | 15.5 | 0 | False | 15.7 | 0 | False | 16.3 | 0 | False |  |
| optimised selection | 14 | 0 | True | 14.6 | 0 | True | 14.7 | 0 | True | 15.2 | 0 | True |  |
| optimised selection | 13.7 | 0 | True | 13.7 | 0 | True | 14.1 | 0 | True | 14.1 | 0 | False |  |
| optimised selection | 9.06 | 0.006 | True | 9.46 | 0.011 | True | 8.13 | 0.013 | True | 8.54 | 0.017 | True |  |
| optimised selection | 8.88 | 0.001 | True | 9.07 | 0.001 | True | 7.85 | 0.015 | True | 8.04 | 0.011 | True |  |
| optimised selection | 10.2 | 0 | True | 11.6 | 0 | False | 9.38 | 0 | True | 10.8 | 0 | True |  |
| optimised selection | 9.18 | 0 | True | 9.77 | 0 | True | 8.25 | 0 | True | 8.84 | 0 | True |  |
| optimised selection | 10.1 | 0 | False | 11.9 | 0 | True | 9.47 | 0 | True | 11.2 | 0 | True |  |
| optimised selection | 8.94 | 0.002 | True | 9.38 | 0.001 | True | 7.82 | 0.042 | True | 8.25 | 0.005 | True |  |
| optimised selection | 7.86 | 0.924 | True | 7.93 | 0.824 | True | 7.25 | 0.717 | True | 7.32 | 0.622 | True | core_holdout_clf, core_holdout_reg, core_train_clf, core_train_reg |
| optimised selection | 8.92 | 0.024 | True | 8.78 | 0.077 | True | 7.83 | 0.17 | True | 7.7 | 0.251 | True |  |
| random selection | 15.9 | 0 | False | 16.9 | 0 | False | 16.5 | 0 | False | 17.5 | 0 | False |  |
| random selection | 10.4 | 0 | True | 12 | 0 | False | 9.65 | 0 | True | 11.3 | 0 | True |  |


**normalized_scores**

| method | fidelity | utility | dependence | distribution | long_structure | target | windows | classification | regression |
|---|---|---|---|---|---|---|---|---|---|
| chronos | -0.334 | -0.176 | 0.108 | -0.637 | -0.0197 | -0.564 | -0.62 | -0.393 | 0.582 |
| diffusion_ts | 0.441 | 0.414 | 0.585 | 0.914 | 0.606 | 0.697 | 0.292 | 0.293 | 0.48 |
| timesfm | -0.0466 | 0.64 | -1.51 | 0.226 | 0.196 | -2.43 | -0.00282 | 0.392 | 0.873 |
| timestral | -0.186 | -0.0333 | -1.02 | 0.268 | -0 | -5.36 | 0.152 | -0.585 | 0.776 |
| zedge_ts_ar | 0.653 | 0.901 | 0.694 | 0.784 | 0.85 | 0.469 | 0.412 | 0.838 | 0.946 |
| zedge_ts_long | 0.8 | 0.74 | 0.786 | 0.977 | 0.573 | 0.911 | 0.876 | 0.661 | 0.829 |
| vae_atsp | 0.148 | 0.197 | -0.385 | 0.0692 | 0.258 | 0.294 | 0.185 | 0.139 | 0.217 |
| vae_greedy | -0.0413 | 0.141 | -0.314 | -0.0631 | -0.00249 | 0.216 | 0.15 | 0.0481 | 0.161 |
| vae_herding | 0.418 | 0.232 | 0.193 | 0.599 | 0.215 | 0.285 | 0.524 | 0.169 | 0.302 |
| vae_knn | 0.0737 | 0.0125 | -0.0394 | 0.137 | 0.341 | 0.193 | 0.19 | -0.011 | 0.0535 |
| vae_mbb | 0.11 | -0.013 | -0.025 | 0.0781 | 0.238 | 0.19 | 0.196 | -0.00218 | 0.0209 |
| vae_pctsp | 0.197 | 0.102 | 0.311 | 0.0886 | 0.239 | 0.36 | 0.45 | 0.035 | 0.055 |
| vae_quilting | 0.0957 | 0.152 | -0.635 | 0.0978 | 0.252 | 0.048 | 0.311 | 0.0921 | 0.218 |
| vae_zseries | 0.5 | 0.264 | 0.296 | 0.449 | 0.386 | 0.6 | 0.356 | 0.198 | 0.359 |
| zedge_atsp | 0.177 | 0.431 | 0.369 | 0.0454 | 0.141 | 0.286 | 0.691 | 0.363 | 0.347 |
| zedge_greedy | 0.177 | 0.411 | 0.294 | 0.189 | 0.209 | 0.503 | 0.114 | 0.323 | 0.347 |
| zedge_herding | 0.0373 | -0.0433 | 0.204 | 0.00217 | -0.0633 | 0.155 | 0.5 | -0.0301 | -0.061 |
| zedge_knn | 0.321 | 0.368 | 0.449 | 0.203 | 0.124 | 0.871 | 0.422 | 0.323 | 0.396 |
| zedge_mbb | 0.0211 | 0.00209 | 0.0636 | 0.0178 | 0.104 | 0.115 | 0.21 | 0.00565 | 0.0116 |
| zedge_pctsp | 0.0206 | 0.425 | 0.237 | 0.046 | 0.00861 | 0.0174 | 0.334 | 0.415 | 0.369 |
| zedge_quilting | 0.418 | 0.555 | 0.889 | 0.193 | 0.617 | 0.513 | 0.292 | 0.44 | 0.559 |
| zedge_zseries | 0.0411 | 0.474 | 0.463 | 0.142 | 0.105 | 0.108 | 0.0482 | 0.277 | 0.505 |
| vae_rand | -0 | -0 | -0 | -0 | -0 | -0 | -0 | 0 | -0 |
| zedge_rand | -0 | -0 | 0 | 0 | 0 | -0 | -0 | 0 | -0 |


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
| diffusion_ts vs vae_rand | utility | reg_h168\|linear\|S\|val\|mase | 9 | 4.86 | 5.47 | 3.21 | 7.96 | 0.0765 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| diffusion_ts vs vae_rand | utility | vol_h24\|gbdt\|S\|oot\|mase | 9 | 0.691 | 3.56 | 0.62 | 8.68 | 0.0765 | 1 | 1 | 3 | 0 | 0 | inconclusive |
| diffusion_ts vs vae_rand | utility | vol_h24\|gbdt\|S\|val\|mase | 9 | 0.81 | 1.21 | 0.559 | 1.91 | 0.0765 | 1 | 1 | 2 | 0 | 0 | inconclusive |
| timestral vs vae_rand | utility | ms_h24\|linear\|S\|val\|mase | 9 | 5.12 | 4.55 | 3.11 | 5.87 | 0.0765 | 1 | 1 | 8 | 0 | 0 | inconclusive |
| timestral vs vae_rand | utility | qreg_h24\|linear\|S\|val\|pinball | 9 | 2.87 | 3.06 | 1.57 | 4.81 | 0.0765 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| timestral vs vae_rand | utility | reg_h168\|gbdt\|S\|val\|mase | 9 | 4.19 | 4.73 | 3.14 | 6.54 | 0.0765 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| timestral vs vae_rand | utility | reg_h168\|linear\|S\|val\|mase | 9 | 4.85 | 5.67 | 3.52 | 8.17 | 0.0765 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| timestral vs vae_rand | utility | reg_h24\|gbdt\|S\|val\|mase | 9 | 4.99 | 5.33 | 2.98 | 7.61 | 0.0765 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| timestral vs vae_rand | utility | reg_h24\|linear\|S\|val\|mase | 9 | 3.62 | 4.4 | 2.89 | 6.17 | 0.0765 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| timestral vs assembly_median | utility | reg_h168\|gbdt\|S\|oot\|mase | 9 | 5.52 | 6.06 | 3.64 | 8.82 | 0.0765 | 1 | 1 | 8 | 0 | 0 | inconclusive |
| timestral vs assembly_median | utility | reg_h168\|gbdt\|S\|val\|mase | 9 | 5.43 | 5.46 | 3.8 | 7.05 | 0.0765 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| timestral vs assembly_median | utility | reg_h168\|linear\|S\|val\|mase | 9 | 4.84 | 4.77 | 3.2 | 6.36 | 0.0765 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| timestral vs assembly_median | utility | reg_h24\|linear\|S\|oot\|mase | 9 | 4.68 | 6.45 | 4.32 | 9.09 | 0.0765 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| timestral vs assembly_median | utility | reg_h24\|linear\|S\|val\|mase | 9 | 5.65 | 9.47 | 4.02 | 18.4 | 0.0765 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| zedge_ts_ar vs vae_rand | utility | clf_up_h24_q95\|gbdt\|S\|oot\|auc | 9 | 2.7 | 2.2 | 1.24 | 3.23 | 0.0765 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| zedge_ts_ar vs assembly_median | utility | clf_down_h24_q10\|gbdt\|S\|oot\|auc | 9 | 2.33 | 3.09 | 1.66 | 4.72 | 0.0765 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| zedge_ts_ar vs assembly_median | utility | clf_up_h1_q90\|gbdt\|S\|oot\|auc | 9 | 1.65 | 2.63 | 1.19 | 4.52 | 0.0765 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| zedge_ts_ar vs assembly_median | utility | clf_up_h24_q99\|gbdt\|S\|oot\|auc | 9 | 2.19 | 2.24 | 1.24 | 3.41 | 0.0765 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| zedge_ts_long vs vae_rand | utility | clf_up_h24_q95\|gbdt\|S\|oot\|auc | 9 | 1.47 | 1.5 | 0.847 | 2.27 | 0.0765 | 1 | 1 | 5 | 0 | 0 | inconclusive |
| zedge_ts_long vs assembly_median | utility | clf_down_h24_q10\|gbdt\|S\|oot\|auc | 9 | 1.51 | 1.95 | 1.33 | 2.71 | 0.0765 | 1 | 1 | 8 | 0 | 0 | inconclusive |
| diffusion_ts vs vae_rand | fidelity | F5.3_seam_z_mean | 9 | 5.3 | 5.93 | 3.7 | 8.75 | 0.0765 | 1 | 1 | 8 | 0 | 0 | inconclusive |
| diffusion_ts vs vae_rand | fidelity | F5.3_seam_z_mean@oot | 9 | 5.3 | 5.93 | 3.7 | 8.75 | 0.0765 | 1 | 1 | 8 | 0 | 0 | inconclusive |
| diffusion_ts vs vae_rand | fidelity | F5.3_seam_z_p95 | 9 | 5.55 | 6.93 | 3.81 | 11.9 | 0.0765 | 1 | 1 | 8 | 0 | 0 | inconclusive |
| diffusion_ts vs vae_rand | fidelity | F5.3_seam_z_p95@oot | 9 | 5.55 | 6.93 | 3.81 | 11.9 | 0.0765 | 1 | 1 | 8 | 0 | 0 | inconclusive |
| diffusion_ts vs vae_rand | fidelity | F5.4_seam_local_acf | 9 | 1.7 | 2.19 | 1.2 | 3.57 | 0.0765 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| diffusion_ts vs vae_rand | fidelity | F5.4_seam_local_acf@oot | 9 | 1.7 | 2.19 | 1.2 | 3.57 | 0.0765 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| diffusion_ts vs vae_rand | fidelity | F8.1_class_tvd | 9 | 4.28 | 7.15 | 2.52 | 12.4 | 0.0765 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| diffusion_ts vs vae_rand | fidelity | F8.5_cond_event_err | 9 | 2.94 | 5.12 | 2.07 | 8.54 | 0.0765 | 1 | 1 | 6 | 0 | 1 | inconclusive |
| diffusion_ts vs assembly_median | fidelity | F5.4_seam_local_acf | 9 | 0.8 | 1.01 | 0.366 | 1.9 | 0.0765 | 1 | 1 | 4 | 0 | 0 | inconclusive |
| diffusion_ts vs assembly_median | fidelity | F5.4_seam_local_acf@oot | 9 | 0.8 | 1.01 | 0.366 | 1.9 | 0.0765 | 1 | 1 | 4 | 0 | 0 | inconclusive |
| timestral vs vae_rand | fidelity | F5.3_seam_z_mean | 9 | 7.31 | 8.12 | 5.37 | 11.2 | 0.0765 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| timestral vs vae_rand | fidelity | F5.3_seam_z_mean@oot | 9 | 7.31 | 8.12 | 5.37 | 11.2 | 0.0765 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| timestral vs vae_rand | fidelity | F5.3_seam_z_p95 | 9 | 7.95 | 9.69 | 6.42 | 14.8 | 0.0765 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| timestral vs vae_rand | fidelity | F5.3_seam_z_p95@oot | 9 | 7.95 | 9.69 | 6.42 | 14.8 | 0.0765 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| zedge_ts_ar vs vae_rand | fidelity | F1.4_qq_corr | 9 | 2.46 | 2.64 | 1.42 | 3.94 | 0.0765 | 1 | 1 | 6 | 0 | 0 | inconclusive |
| zedge_ts_ar vs vae_rand | fidelity | F5.2_ks_seam_vs_inside | 9 | 2.7 | 3.12 | 1.65 | 4.64 | 0.0765 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| zedge_ts_ar vs vae_rand | fidelity | F5.2_ks_seam_vs_inside@oot | 9 | 2.7 | 3.12 | 1.65 | 4.64 | 0.0765 | 1 | 1 | 7 | 0 | 0 | inconclusive |
| zedge_ts_ar vs vae_rand | fidelity | F5.3_seam_z_mean | 9 | 4.44 | 6.15 | 3.86 | 9.24 | 0.0765 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| zedge_ts_ar vs vae_rand | fidelity | F5.3_seam_z_mean@oot | 9 | 4.44 | 6.15 | 3.86 | 9.24 | 0.0765 | 1 | 1 | 9 | 0 | 0 | inconclusive |
| zedge_ts_ar vs vae_rand | fidelity | F5.3_seam_z_p95 | 9 | 5.67 | 6.62 | 4.37 | 9.79 | 0.0765 | 1 | 1 | 9 | 0 | 0 | inconclusive |

_Showing 40 rows of 2428 (rows with a better / worse / same verdict first); all of them — `hypotheses/RQ2_global.parquet`._

### RQ3. Within assembly: window selection × seam processing

| comparison | kind | unit | n_datasets | median_z | mean_z | ci_lo | ci_hi | p_better_adj | p_worse_adj | p_equiv_adj | n_better | n_worse | n_same | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| seams: vae_zseries_wsola vs vae_zseries | utility | clf_up_h24_q95\|gbdt\|S\|val\|auc | 9 | -0.414 | -0.575 | -0.849 | -0.327 | 1 | 0.0581 | 0.0298 | 0 | 1 | 1 | same |
| main effect: seams wsola vs none | utility | clf_up_h24_q95\|gbdt\|S\|val\|auc | 9 | -0.414 | -0.575 | -0.849 | -0.327 | 1 | 0.0581 | 0.0298 | 0 | 1 | 1 | same |
| selection: vae_mbb vs vae_rand | fidelity | F2.4_big_jump_share_err | 9 | -0.267 | -0.388 | -0.739 | -0.103 | 1 | 0.0581 | 0.0298 | 0 | 0 | 2 | same |
| selection: vae_mbb vs vae_rand | fidelity | F12.2_exceed_magnitude_err@oot | 8 | -0.146 | -0.173 | -0.448 | 0.0806 | 1 | 0.111 | 0.0298 | 0 | 0 | 1 | same |
| seams: vae_zseries_quilt vs vae_zseries | fidelity | F1.6_std_err@oot | 9 | -0.228 | -0.336 | -0.697 | -0.0555 | 1 | 0.138 | 0.0298 | 0 | 0 | 3 | same |
| seams: vae_zseries_xfade vs vae_zseries | fidelity | F1.1_ks@oot | 9 | -0.185 | -0.217 | -0.471 | 0.00986 | 1 | 0.138 | 0.0261 | 0 | 0 | 5 | same |
| main effect: seams crossfade vs none | fidelity | F1.1_ks@oot | 9 | -0.185 | -0.217 | -0.471 | 0.00986 | 1 | 0.138 | 0.0261 | 0 | 0 | 5 | same |
| main effect: seams quilt vs none | fidelity | F1.6_std_err@oot | 9 | -0.228 | -0.336 | -0.697 | -0.0555 | 1 | 0.138 | 0.0298 | 0 | 0 | 3 | same |
| selection: vae_mbb vs vae_rand | fidelity | F3.4_acf_sq_d | 9 | 0.407 | 0.39 | -0.0406 | 0.87 | 0.167 | 1 | 0.0298 | 0 | 0 | 0 | same |
| selection: vae_mbb vs vae_rand | fidelity | F3.6_peak168_err@oot | 9 | -0.14 | -0.206 | -0.566 | 0.145 | 1 | 0.167 | 0.0261 | 0 | 0 | 0 | same |
| seams: vae_zseries_quilt vs vae_zseries | fidelity | F2.1_ks_d1 | 9 | -0.293 | -0.335 | -0.658 | -0.0203 | 1 | 0.167 | 0.0261 | 0 | 0 | 3 | same |
| seams: vae_zseries_xfade vs vae_zseries | fidelity | F1.1_ks | 9 | -0.169 | -0.201 | -0.524 | 0.0655 | 1 | 0.167 | 0.0261 | 0 | 0 | 4 | same |
| main effect: seams crossfade vs none | fidelity | F1.1_ks | 9 | -0.169 | -0.201 | -0.524 | 0.0655 | 1 | 0.167 | 0.0261 | 0 | 0 | 4 | same |
| main effect: seams quilt vs none | fidelity | F2.1_ks_d1 | 9 | -0.293 | -0.335 | -0.658 | -0.0203 | 1 | 0.167 | 0.0261 | 0 | 0 | 3 | same |
| seams: vae_zseries_quilt vs vae_zseries | utility | clf_up_h6_q90\|gbdt\|S\|oot\|auc | 9 | -0.102 | -0.184 | -0.493 | 0.0355 | 1 | 0.19 | 0.0261 | 0 | 0 | 6 | same |
| seams: vae_zseries_xfade vs vae_zseries | utility | clf_up_h6_q90\|gbdt\|S\|oot\|auc | 9 | -0.222 | -0.219 | -0.497 | 0.0286 | 1 | 0.19 | 0.0261 | 0 | 0 | 5 | same |
| main effect: seams crossfade vs none | utility | clf_up_h6_q90\|gbdt\|S\|oot\|auc | 9 | -0.222 | -0.219 | -0.497 | 0.0286 | 1 | 0.19 | 0.0261 | 0 | 0 | 5 | same |
| main effect: seams quilt vs none | utility | clf_up_h6_q90\|gbdt\|S\|oot\|auc | 9 | -0.102 | -0.184 | -0.493 | 0.0355 | 1 | 0.19 | 0.0261 | 0 | 0 | 6 | same |
| seams: vae_zseries_quilt vs vae_zseries | fidelity | F1.9_js@oot | 9 | -0.319 | -0.28 | -0.554 | 9.43e-05 | 1 | 0.19 | 0.0261 | 0 | 0 | 3 | same |
| seams: vae_zseries_xfade vs vae_zseries | fidelity | F1.9_js | 9 | -0.274 | -0.236 | -0.525 | 0.0521 | 1 | 0.19 | 0.0261 | 0 | 0 | 1 | same |
| seams: vae_zseries_xfade vs vae_zseries | fidelity | F7.5_drawdown_ks@oot | 9 | -0.203 | -0.237 | -0.471 | -0.0108 | 1 | 0.19 | 0.0261 | 0 | 0 | 4 | same |
| main effect: seams crossfade vs none | fidelity | F1.9_js | 9 | -0.274 | -0.236 | -0.525 | 0.0521 | 1 | 0.19 | 0.0261 | 0 | 0 | 1 | same |
| main effect: seams crossfade vs none | fidelity | F7.5_drawdown_ks@oot | 9 | -0.203 | -0.237 | -0.471 | -0.0108 | 1 | 0.19 | 0.0261 | 0 | 0 | 4 | same |
| main effect: seams quilt vs none | fidelity | F1.9_js@oot | 9 | -0.319 | -0.28 | -0.554 | 9.43e-05 | 1 | 0.19 | 0.0261 | 0 | 0 | 3 | same |
| seams: vae_zseries_quilt vs vae_zseries | utility | vol_h24\|gbdt\|S\|val\|mase | 9 | -0.169 | -0.202 | -0.517 | 0.0182 | 1 | 0.23 | 0.0261 | 0 | 0 | 5 | same |
| main effect: seams quilt vs none | utility | vol_h24\|gbdt\|S\|val\|mase | 9 | -0.169 | -0.202 | -0.517 | 0.0182 | 1 | 0.23 | 0.0261 | 0 | 0 | 5 | same |
| seams: vae_zseries_quilt vs vae_zseries | fidelity | F1.1_ks@oot | 9 | -0.187 | -0.131 | -0.352 | 0.0778 | 1 | 0.23 | 0.0261 | 0 | 0 | 5 | same |
| seams: vae_zseries_quilt vs vae_zseries | fidelity | F7.5_drawdown_ks@oot | 9 | -0.154 | -0.138 | -0.313 | 0.0422 | 1 | 0.23 | 0.0261 | 0 | 0 | 6 | same |
| seams: vae_zseries_xfade vs vae_zseries | fidelity | F2.1_ks_d1 | 9 | -0.208 | -0.269 | -0.585 | 0.0297 | 1 | 0.23 | 0.0261 | 0 | 0 | 4 | same |
| main effect: seams crossfade vs none | fidelity | F2.1_ks_d1 | 9 | -0.208 | -0.269 | -0.585 | 0.0297 | 1 | 0.23 | 0.0261 | 0 | 0 | 4 | same |
| main effect: seams quilt vs none | fidelity | F1.1_ks@oot | 9 | -0.187 | -0.131 | -0.352 | 0.0778 | 1 | 0.23 | 0.0261 | 0 | 0 | 5 | same |
| main effect: seams quilt vs none | fidelity | F7.5_drawdown_ks@oot | 9 | -0.154 | -0.138 | -0.313 | 0.0422 | 1 | 0.23 | 0.0261 | 0 | 0 | 6 | same |
| seams: vae_zseries_xfade vs vae_zseries | utility | clf_up_h1_q90\|gbdt\|S\|oot\|auc | 9 | 0.183 | 0.352 | 0.0318 | 0.731 | 0.235 | 1 | 0.0298 | 0 | 0 | 1 | same |
| main effect: seams crossfade vs none | utility | clf_up_h1_q90\|gbdt\|S\|oot\|auc | 9 | 0.183 | 0.352 | 0.0318 | 0.731 | 0.235 | 1 | 0.0298 | 0 | 0 | 1 | same |
| selection: vae_knn vs vae_rand | fidelity | F1.10_hill_err | 9 | 0.26 | 0.301 | -0.0596 | 0.664 | 0.235 | 1 | 0.0261 | 0 | 0 | 1 | same |
| seams: vae_zseries_wsola vs vae_zseries | utility | ms_h24\|gbdt\|S\|oot\|mase | 9 | -0.295 | -0.306 | -0.644 | 0.0561 | 1 | 0.269 | 0.0261 | 0 | 0 | 3 | same |
| main effect: seams wsola vs none | utility | ms_h24\|gbdt\|S\|oot\|mase | 9 | -0.295 | -0.306 | -0.644 | 0.0561 | 1 | 0.269 | 0.0261 | 0 | 0 | 3 | same |
| selection: vae_mbb vs vae_rand | fidelity | F2.2_vol_ratio_err_d1 | 9 | -0.201 | -0.207 | -0.577 | 0.178 | 1 | 0.269 | 0.0261 | 0 | 0 | 1 | same |
| selection: vae_mbb vs vae_rand | fidelity | F6.6_feature_fid@oot | 9 | -0.192 | -0.266 | -0.653 | 0.103 | 1 | 0.269 | 0.0298 | 0 | 0 | 0 | same |
| selection: vae_mbb vs vae_rand | fidelity | F6.8_nn_dist_logratio@oot | 9 | -0.101 | -0.203 | -0.518 | 0.11 | 1 | 0.269 | 0.0261 | 0 | 0 | 1 | same |

_Showing 40 rows of 2884 (rows with a better / worse / same verdict first); all of them — `hypotheses/RQ3_global.parquet`._

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
| F8.5_cond_event_err@oot | F8.5_cond_event_err | oot | F8_target | regression@oot | 9 | 0.846 | 0.889 | 0.00781 | 0.031 | True |
| F8.6_cond_future_ks@train | F8.6_cond_future_ks | train | F8_target | regression@oot | 9 | 0.839 | 0.778 | 0.0195 | 0.0493 | True |
| F6.6_feature_fid@oot | F6.6_feature_fid | oot | F6_windows | regression@oot | 9 | 0.837 | 1 | 0.00391 | 0.0254 | True |
| F8.5_cond_event_err@train | F8.5_cond_event_err | train | F8_target | regression@oot | 9 | 0.834 | 0.889 | 0.00781 | 0.031 | True |
| F1.6_mean_err@oot | F1.6_mean_err | oot | F1_marginal | regression@oot | 9 | 0.831 | 1 | 0.00391 | 0.0254 | True |
| F8.6_cond_future_ks@oot | F8.6_cond_future_ks | oot | F8_target | regression@oot | 9 | 0.823 | 0.889 | 0.00781 | 0.031 | True |
| F6.4_mmd@oot | F6.4_mmd | oot | F6_windows | regression@oot | 9 | 0.822 | 0.889 | 0.00781 | 0.031 | True |
| F9.2_coverage@train | F9.2_coverage | train | F9_coverage | regression@oot | 9 | 0.82 | 0.778 | 0.0195 | 0.0493 | True |
| F6.6_feature_fid@train | F6.6_feature_fid | train | F6_windows | classification@oot | 9 | 0.82 | 1 | 0.00391 | 0.0254 | True |
| F9.2_coverage@train | F9.2_coverage | train | F9_coverage | classification@oot | 9 | 0.819 | 1 | 0.00391 | 0.0254 | True |
| F6.8_nn_dist_logratio | F6.8_nn_dist_logratio | val | F6_windows | regression@val | 9 | 0.819 | 1 | 0.00391 | 0.0254 | True |
| F8.5_cond_event_err@train | F8.5_cond_event_err | train | F8_target | classification@val | 9 | 0.818 | 0.778 | 0.0195 | 0.0493 | True |
| F8.6_cond_future_ks@oot | F8.6_cond_future_ks | oot | F8_target | classification@oot | 9 | 0.818 | 0.889 | 0.00781 | 0.031 | True |
| F1.5_quantile_err@oot | F1.5_quantile_err | oot | F1_marginal | regression@oot | 9 | 0.817 | 1 | 0.00391 | 0.0254 | True |
| F11.3_multiclass_tvd@train | F11.3_multiclass_tvd | train | F11_class_balance | classification@val | 9 | 0.815 | 0.889 | 0.00781 | 0.031 | True |
| F1.2_w1@oot | F1.2_w1 | oot | F1_marginal | regression@oot | 9 | 0.814 | 1 | 0.00391 | 0.0254 | True |
| F6.6_feature_fid@oot | F6.6_feature_fid | oot | F6_windows | classification@oot | 9 | 0.814 | 0.778 | 0.0273 | 0.06 | False |
| F8.5_cond_event_err | F8.5_cond_event_err | val | F8_target | regression@oot | 9 | 0.811 | 0.889 | 0.0117 | 0.037 | True |
| F6.4_mmd | F6.4_mmd | val | F6_windows | regression@oot | 9 | 0.81 | 0.778 | 0.129 | 0.177 | False |
| F8.1_class_tvd | F8.1_class_tvd | val | F8_target | regression@oot | 9 | 0.807 | 0.889 | 0.00781 | 0.031 | True |
| F8.6_cond_future_ks | F8.6_cond_future_ks | val | F8_target | classification@oot | 9 | 0.803 | 0.778 | 0.0391 | 0.0759 | False |
| F9.2_coverage@oot | F9.2_coverage | oot | F9_coverage | regression@oot | 9 | 0.803 | 1 | 0.00391 | 0.0254 | True |
| F2.1_w1_d24@train | F2.1_w1_d24 | train | F2_increments | classification@oot | 9 | 0.8 | 1 | 0.00391 | 0.0254 | True |
| F8.6_cond_future_ks@train | F8.6_cond_future_ks | train | F8_target | classification@oot | 9 | 0.799 | 1 | 0.00391 | 0.0254 | True |
| F8.1_class_tvd@train | F8.1_class_tvd | train | F8_target | classification@val | 9 | 0.797 | 0.667 | 0.0547 | 0.0951 | False |
| F8.6_cond_future_ks@train | F8.6_cond_future_ks | train | F8_target | classification@val | 9 | 0.796 | 0.889 | 0.00781 | 0.031 | True |
| F8.6_cond_future_ks@oot | F8.6_cond_future_ks | oot | F8_target | classification@val | 9 | 0.795 | 0.889 | 0.00781 | 0.031 | True |
| F8.5_cond_event_err@train | F8.5_cond_event_err | train | F8_target | regression@val | 9 | 0.795 | 0.778 | 0.0391 | 0.0759 | False |
| F7.3_crossings_err | F7.3_crossings_err | val | F7_long_structure | classification@oot | 9 | 0.793 | 0.778 | 0.0547 | 0.0951 | False |
| F9.2_coverage@oot | F9.2_coverage | oot | F9_coverage | classification@oot | 9 | 0.792 | 1 | 0.00391 | 0.0254 | True |
| F6.8_nn_dist_logratio@oot | F6.8_nn_dist_logratio | oot | F6_windows | regression@oot | 9 | 0.792 | 0.889 | 0.0195 | 0.0493 | True |
| F8.6_cond_future_ks | F8.6_cond_future_ks | val | F8_target | regression@oot | 9 | 0.791 | 0.778 | 0.0273 | 0.06 | False |
| F8.1_class_tvd@train | F8.1_class_tvd | train | F8_target | regression@oot | 9 | 0.789 | 0.889 | 0.00781 | 0.031 | True |
| F2.1_w1_d24@train | F2.1_w1_d24 | train | F2_increments | regression@oot | 9 | 0.787 | 0.889 | 0.00781 | 0.031 | True |
| F1.9_js@oot | F1.9_js | oot | F1_marginal | classification@oot | 9 | 0.784 | 0.778 | 0.0195 | 0.0493 | True |
| F8.6_cond_future_ks | F8.6_cond_future_ks | val | F8_target | regression@val | 9 | 0.784 | 0.778 | 0.0195 | 0.0493 | True |
| F11.3_multiclass_tvd@train | F11.3_multiclass_tvd | train | F11_class_balance | regression@oot | 9 | 0.782 | 0.889 | 0.0117 | 0.037 | True |
| F8.6_cond_future_ks | F8.6_cond_future_ks | val | F8_target | classification@val | 9 | 0.781 | 0.889 | 0.0195 | 0.0493 | True |
| F7.1_roll_mean_ks@oot | F7.1_roll_mean_ks | oot | F7_long_structure | regression@oot | 9 | 0.78 | 0.889 | 0.00781 | 0.031 | True |
| F2.1_w1_d24@train | F2.1_w1_d24 | train | F2_increments | classification@val | 9 | 0.778 | 0.889 | 0.00781 | 0.031 | True |

_Showing 40 rows of 896; all of them — `hypotheses/RQ4_global.parquet`._

**by_reference**

| criterion | reference | median_rho | share_predictive |
|---|---|---|---|
| classification@oot | oot | 0.598 | 0.541 |
| classification@oot | train | 0.64 | 0.77 |
| classification@oot | val | 0.46 | 0.303 |
| classification@val | oot | 0.462 | 0.243 |
| classification@val | train | 0.576 | 0.703 |
| classification@val | val | 0.445 | 0.316 |
| regression@oot | oot | 0.568 | 0.514 |
| regression@oot | train | 0.597 | 0.527 |
| regression@oot | val | 0.506 | 0.197 |
| regression@val | oot | 0.372 | 0.095 |
| regression@val | train | 0.477 | 0.135 |
| regression@val | val | 0.438 | 0.395 |


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
| F3_dependence | oot | 0.61 | 0.533 | 0.556 | 0.43 |
| F3_dependence | train | 0.618 | 0.612 | 0.524 | 0.538 |
| F3_dependence | val | 0.579 | 0.497 | 0.484 | 0.423 |
| F5_seams | oot | 0.118 | 0.092 | 0.131 | 0.318 |
| F5_seams | train | 0.124 | 0.121 | 0.163 | 0.327 |
| F5_seams | val | 0.111 | 0.121 | 0.163 | 0.327 |
| F6_windows | oot | 0.693 | 0.433 | 0.728 | 0.416 |
| F6_windows | train | 0.637 | 0.497 | 0.636 | 0.555 |
| F6_windows | val | 0.614 | 0.55 | 0.652 | 0.71 |
| F7_long_structure | oot | 0.416 | 0.27 | 0.454 | 0.024 |
| F7_long_structure | train | 0.639 | 0.51 | 0.528 | 0.266 |
| F7_long_structure | val | 0.155 | 0.229 | 0.355 | 0.352 |
| F8_target | oot | 0.633 | 0.6 | 0.747 | 0.643 |
| F8_target | train | 0.758 | 0.796 | 0.789 | 0.745 |
| F8_target | val | 0.685 | 0.584 | 0.791 | 0.631 |
| F9_coverage | oot | 0.676 | 0.526 | 0.673 | 0.146 |
| F9_coverage | train | 0.769 | 0.716 | 0.709 | 0.612 |
| F9_coverage | val | 0.654 | 0.581 | 0.608 | 0.677 |


**top_predictors**

| unit | metric | reference | group | criterion | n_datasets | median_rho | share_positive | p_two_sided | p_bh | predictive |
|---|---|---|---|---|---|---|---|---|---|---|
| F8.5_cond_event_err@oot | F8.5_cond_event_err | oot | F8_target | regression@oot | 9 | 0.846 | 0.889 | 0.00781 | 0.031 | True |
| F8.6_cond_future_ks@train | F8.6_cond_future_ks | train | F8_target | regression@oot | 9 | 0.839 | 0.778 | 0.0195 | 0.0493 | True |
| F6.6_feature_fid@oot | F6.6_feature_fid | oot | F6_windows | regression@oot | 9 | 0.837 | 1 | 0.00391 | 0.0254 | True |
| F8.5_cond_event_err@train | F8.5_cond_event_err | train | F8_target | regression@oot | 9 | 0.834 | 0.889 | 0.00781 | 0.031 | True |
| F1.6_mean_err@oot | F1.6_mean_err | oot | F1_marginal | regression@oot | 9 | 0.831 | 1 | 0.00391 | 0.0254 | True |
| F6.6_feature_fid@train | F6.6_feature_fid | train | F6_windows | classification@oot | 9 | 0.82 | 1 | 0.00391 | 0.0254 | True |
| F9.2_coverage@train | F9.2_coverage | train | F9_coverage | classification@oot | 9 | 0.819 | 1 | 0.00391 | 0.0254 | True |
| F6.8_nn_dist_logratio | F6.8_nn_dist_logratio | val | F6_windows | regression@val | 9 | 0.819 | 1 | 0.00391 | 0.0254 | True |
| F8.5_cond_event_err@train | F8.5_cond_event_err | train | F8_target | classification@val | 9 | 0.818 | 0.778 | 0.0195 | 0.0493 | True |
| F8.6_cond_future_ks@oot | F8.6_cond_future_ks | oot | F8_target | classification@oot | 9 | 0.818 | 0.889 | 0.00781 | 0.031 | True |
| F11.3_multiclass_tvd@train | F11.3_multiclass_tvd | train | F11_class_balance | classification@val | 9 | 0.815 | 0.889 | 0.00781 | 0.031 | True |
| F6.6_feature_fid@oot | F6.6_feature_fid | oot | F6_windows | classification@oot | 9 | 0.814 | 0.778 | 0.0273 | 0.06 | False |
| F8.6_cond_future_ks | F8.6_cond_future_ks | val | F8_target | classification@oot | 9 | 0.803 | 0.778 | 0.0391 | 0.0759 | False |
| F8.1_class_tvd@train | F8.1_class_tvd | train | F8_target | classification@val | 9 | 0.797 | 0.667 | 0.0547 | 0.0951 | False |
| F8.6_cond_future_ks@train | F8.6_cond_future_ks | train | F8_target | classification@val | 9 | 0.796 | 0.889 | 0.00781 | 0.031 | True |
| F8.6_cond_future_ks@oot | F8.6_cond_future_ks | oot | F8_target | classification@val | 9 | 0.795 | 0.889 | 0.00781 | 0.031 | True |
| F8.5_cond_event_err@train | F8.5_cond_event_err | train | F8_target | regression@val | 9 | 0.795 | 0.778 | 0.0391 | 0.0759 | False |
| F8.6_cond_future_ks | F8.6_cond_future_ks | val | F8_target | regression@val | 9 | 0.784 | 0.778 | 0.0195 | 0.0493 | True |
| F6.4_mmd | F6.4_mmd | val | F6_windows | regression@val | 9 | 0.771 | 1 | 0.00391 | 0.0254 | True |
| F8.6_cond_future_ks@train | F8.6_cond_future_ks | train | F8_target | regression@val | 9 | 0.768 | 0.667 | 0.0547 | 0.0951 | False |


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
| val ↔ oot | fidelity:dependence | 0.833 |
| val ↔ oot | fidelity:distribution | 0.783 |
| val ↔ oot | fidelity:long_structure | 0.609 |
| val ↔ oot | fidelity:seams | 0.971 |
| val ↔ oot | fidelity:target | 0.884 |
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
| holdout_clf | timestral | long-series generator | 18.3 | 14.7 | 1.23 | True |
| holdout_clf | timesfm | long-series generator | 16.2 | 13.7 | 2.38 | True |
| holdout_clf | chronos | long-series generator | 16.1 | 13.7 | 33.9 | True |
| holdout_clf | vae_rand | random selection | 15.8 | 13.4 | 131 | True |
| holdout_clf | vae_quilting | optimised selection | 13.8 | 12.2 | 131 | True |
| holdout_clf | vae_greedy | optimised selection | 15 | 13.2 | 131 | False |
| holdout_clf | vae_knn | optimised selection | 15.4 | 13.6 | 131 | False |
| holdout_clf | vae_mbb | optimised selection | 15.9 | 14.1 | 131 | False |
| holdout_clf | vae_herding | optimised selection | 14 | 13 | 131 | False |
| holdout_clf | vae_zseries | optimised selection | 13.6 | 13.4 | 134 | True |
| holdout_clf | vae_atsp | optimised selection | 14.6 | 14.1 | 164 | False |
| holdout_clf | vae_pctsp | optimised selection | 14.5 | 13.9 | 171 | False |
| holdout_clf | zedge_rand | random selection | 10.8 | 10.9 | 798 | True |
| holdout_clf | zedge_quilting | optimised selection | 8.31 | 9.47 | 798 | True |
| holdout_clf | zedge_greedy | optimised selection | 9.08 | 10.2 | 798 | False |
| holdout_clf | zedge_knn | optimised selection | 9.51 | 10.6 | 798 | False |
| holdout_clf | zedge_mbb | optimised selection | 10.6 | 11.5 | 798 | False |
| holdout_clf | zedge_herding | optimised selection | 10.6 | 11.9 | 798 | False |
| holdout_clf | zedge_zseries | optimised selection | 9.29 | 11.2 | 801 | False |
| holdout_clf | zedge_atsp | optimised selection | 9.27 | 11.4 | 822 | False |
| holdout_clf | zedge_pctsp | optimised selection | 9.1 | 11.2 | 839 | False |
| holdout_clf | diffusion_ts | long-series generator | 13.7 | 16.3 | 2.35e+03 | False |
| holdout_clf | zedge_ts_long | long-series generator | 9.65 | 11.6 | 2.93e+03 | False |
| holdout_clf | zedge_ts_ar | long-series generator | 9.15 | 11.2 | 2.95e+03 | False |
| holdout_reg | timestral | long-series generator | 13.5 | 11.6 | 1.23 | True |
| holdout_reg | timesfm | long-series generator | 11.9 | 10.8 | 2.38 | True |
| holdout_reg | chronos | long-series generator | 13.7 | 12.1 | 33.9 | False |
| holdout_reg | vae_rand | random selection | 16.8 | 14.1 | 131 | False |
| holdout_reg | vae_quilting | optimised selection | 14.3 | 12.6 | 131 | False |
| holdout_reg | vae_greedy | optimised selection | 15.3 | 13.4 | 131 | False |
| holdout_reg | vae_knn | optimised selection | 15.9 | 14 | 131 | False |
| holdout_reg | vae_mbb | optimised selection | 16.8 | 14.7 | 131 | False |
| holdout_reg | vae_herding | optimised selection | 14.6 | 13.5 | 131 | False |
| holdout_reg | vae_zseries | optimised selection | 13.7 | 13.5 | 134 | False |
| holdout_reg | vae_atsp | optimised selection | 15.1 | 14.4 | 164 | False |
| holdout_reg | vae_pctsp | optimised selection | 15 | 14.3 | 171 | False |
| holdout_reg | zedge_rand | random selection | 12.5 | 12.1 | 798 | False |
| holdout_reg | zedge_quilting | optimised selection | 8.39 | 9.52 | 798 | True |
| holdout_reg | zedge_greedy | optimised selection | 9.28 | 10.3 | 798 | False |
| holdout_reg | zedge_knn | optimised selection | 10.1 | 11 | 798 | False |


**hardware**: ['NVIDIA H200']

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

