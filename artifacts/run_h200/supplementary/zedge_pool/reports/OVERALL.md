# Overall leaderboard: fidelity and utility

Methods: 24. Datasets (9): beijing_pm25, bike, bitcoin, electricity, ett, household, jena, metro, pjm. Seeds: 10.

Composition (fixed in advance). Fidelity — the core criteria distribution (F1.2_w1, F2.1_ks_d24); dependence (F3.5_log_psd, F4.1_how_mean); windows (F6.1_disc_score, F6.4_mmd); long structure (F7.1_roll_mean_ks, F7.2_roll_std_ks); target (F11.1_class_share_logratio); seams (F5.7_seam_detect_auc_dev); each criterion the mean of its ranks against train, val and OOT. Utility — TSTR classification and regression with equal weights, each tested on val and OOT. Overall = mean of the two domains. Not included: privacy (memorisation flag next to the rank), time, memory.

Ranks are noise-aware: within a leaf two methods whose scores differ by no more than the noise of the leaf (median over seeds of |random − twin|, or the between-seed spread of the random path where the twin is not run) tie. Uncertainty: two-level bootstrap (datasets, then seeds), 10 seeds; tier — not significantly worse than the first method (one-sided Wilcoxon over datasets, Holm).

Friedman p = 8.8e-13, datasets × methods in the test = 9 × 22.

## Leaderboard

Columns: `method` — method id; `family` — method family: long-series generator, random selection, optimised selection, seam processing (a joiner on a stitcher that also runs without it; joiner in brackets); `avg_rank` — mean rank over datasets (seeds averaged within a dataset); 1 = best; `ci_lo` — lower bound of the 95% bootstrap interval of avg_rank; `ci_hi` — upper bound of the 95% bootstrap interval of avg_rank; `p_first` — share of bootstrap samples in which the method has the lowest avg_rank; `p_top3` — share of bootstrap samples in which the method is among the three lowest; `p_worse_than_best_holm` — p-value of the one-sided Wilcoxon test over datasets "worse than the first method", Holm correction; empty for the first method; `tier_wilcoxon` — True — not significantly worse than the first method (p_worse_than_best_holm ≥ 0.05); `n_datasets` — number of datasets in which the method is ranked.

Rows: sorted by avg_rank.

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon | n_datasets |
|---|---|---|---|---|---|---|---|---|---|
| zedge_quilting | optimised selection | 8.11 | 7.04 | 9.16 | 0.79 | 0.96 |  | True | 9 |
| zedge_zseries | optimised selection | 8.70 | 7.98 | 9.43 | 0.11 | 0.64 | 0.33 | True | 9 |
| zedge_greedy | optimised selection | 8.82 | 7.84 | 9.89 | 0.00 | 0.53 | 0.33 | True | 9 |
| zedge_pctsp | optimised selection | 8.94 | 7.83 | 10.05 | 0.00 | 0.28 | 0.32 | True | 9 |
| zedge_ts_ar | long-series generator | 9.10 | 7.39 | 10.86 | 0.08 | 0.30 | 0.33 | True | 9 |
| zedge_atsp | optimised selection | 9.12 | 7.55 | 10.82 | 0.01 | 0.23 | 0.33 | True | 9 |
| zedge_knn | optimised selection | 9.18 | 8.27 | 10.23 | 0.00 | 0.03 | 0.19 | True | 9 |
| zedge_ts_long | long-series generator | 9.37 | 8.00 | 10.85 | 0.00 | 0.02 | 0.22 | True | 9 |
| zedge_herding | optimised selection | 10.37 | 9.13 | 11.68 | 0.00 | 0.00 | 0.09 | True | 9 |
| zedge_mbb | optimised selection | 10.53 | 9.15 | 12.08 | 0.00 | 0.00 | 0.06 | True | 9 |
| zedge_rand | random selection | 10.68 | 9.15 | 12.28 | 0.00 | 0.00 | 0.05 | True | 9 |
| vae_herding | optimised selection | 13.71 | 13.11 | 14.34 | 0.00 | 0.00 | 0.04 | False | 9 |
| vae_zseries | optimised selection | 13.83 | 12.29 | 15.39 | 0.00 | 0.00 | 0.05 | True | 9 |
| diffusion_ts | long-series generator | 13.90 | 12.04 | 15.52 | 0.00 | 0.00 | 0.04 | False | 9 |
| timesfm | long-series generator | 14.47 | 12.67 | 16.18 | 0.00 | 0.00 | 0.12 | True | 6 |
| vae_quilting | optimised selection | 14.56 | 12.76 | 16.30 | 0.00 | 0.00 | 0.05 | True | 9 |
| vae_pctsp | optimised selection | 15.31 | 13.82 | 16.74 | 0.00 | 0.00 | 0.04 | False | 9 |
| vae_atsp | optimised selection | 15.43 | 13.43 | 17.24 | 0.00 | 0.00 | 0.04 | False | 9 |
| vae_greedy | optimised selection | 15.66 | 13.96 | 17.31 | 0.00 | 0.00 | 0.04 | False | 9 |
| chronos | long-series generator | 15.94 | 14.22 | 17.60 | 0.00 | 0.00 | 0.08 | True | 7 |
| vae_knn | optimised selection | 16.14 | 14.27 | 17.81 | 0.00 | 0.00 | 0.04 | False | 9 |
| vae_mbb | optimised selection | 16.52 | 14.55 | 18.40 | 0.00 | 0.00 | 0.04 | False | 9 |
| vae_rand | random selection | 16.67 | 14.70 | 18.51 | 0.00 | 0.00 | 0.04 | False | 9 |
| timestral | long-series generator | 16.92 | 15.71 | 18.24 | 0.00 | 0.00 | 0.04 | False | 9 |


## Next to the rank

Columns: `method` — method id; `fidelity_rank` — avg_rank in the fidelity domain alone (core criteria against train + val + OOT); `utility_rank` — avg_rank in the utility domain alone (TSTR classification + regression, val + OOT); `pareto_fid_ut` — True — no other method is at least as good in both fidelity_rank and utility_rank and strictly better in one; `norm_fidelity` — normalised fidelity: mean over the core criteria of the median normalised score (random assembly = 0, real = 1; against val and train); `norm_utility` — normalised utility: mean of classification and regression (TSTR, random = 0, TRTR = 1); `norm_overall` — mean of norm_fidelity and norm_utility; `near_copy_share` — median over datasets of F10.2: share of synthetic windows closer to train than the 5th percentile of real-to-real distances; `near_copy_ratio` — median over datasets of near_copy_share / near_copy_real; `memorisation_flag` — True — near_copy_ratio ≥ Config.near_copy_ratio (default 2) and p_more_copies_holm < α; reported, does not change the rank.

| method | fidelity_rank | utility_rank | pareto_fid_ut | norm_fidelity | norm_utility | norm_overall | near_copy_share | near_copy_ratio | memorisation_flag |
|---|---|---|---|---|---|---|---|---|---|
| zedge_quilting | 8.29 | 7.93 | True | 0.42 | 0.50 | 0.46 | 0.23 | 1.00 | False |
| zedge_zseries | 8.78 | 8.62 | False | 0.13 | 0.39 | 0.26 | 0.27 | 0.96 | False |
| zedge_greedy | 9.04 | 8.60 | False | 0.23 | 0.34 | 0.28 | 0.33 | 0.92 | False |
| zedge_pctsp | 9.15 | 8.73 | False | 0.11 | 0.39 | 0.25 | 0.32 | 0.97 | False |
| zedge_ts_ar | 10.08 | 8.12 | False | 0.32 | 0.69 | 0.51 | 0.04 | 0.94 | False |
| zedge_atsp | 9.15 | 9.09 | False | 0.25 | 0.36 | 0.30 | 0.32 | 0.93 | False |
| zedge_knn | 9.30 | 9.06 | False | 0.42 | 0.36 | 0.39 | 0.31 | 0.89 | False |
| zedge_ts_long | 9.46 | 9.27 | False | 0.28 | 0.42 | 0.35 | 0.09 | 0.68 | False |
| zedge_herding | 10.25 | 10.49 | False | 0.14 | -0.05 | 0.05 | 0.21 | 0.86 | False |
| zedge_mbb | 10.49 | 10.56 | False | 0.10 | 0.01 | 0.06 | 0.21 | 0.79 | False |
| zedge_rand | 10.48 | 10.88 | False | 0.00 | 0.00 | 0.00 | 0.20 | 0.85 | False |
| vae_herding | 13.09 | 14.32 | False | 0.37 | 0.24 | 0.30 | 0.08 | 0.64 | False |
| vae_zseries | 13.37 | 14.29 | False | 0.40 | 0.28 | 0.34 | 0.32 | 0.83 | False |
| diffusion_ts | 14.39 | 13.41 | False | 0.57 | -0.26 | 0.15 | 0.20 | 1.00 | False |
| timesfm | 15.26 | 13.69 | False | -0.53 | 0.28 | -0.13 | 0.62 | 0.93 | False |
| vae_quilting | 14.18 | 14.94 | False | 0.10 | 0.16 | 0.13 | 0.20 | 0.79 | False |
| vae_pctsp | 14.81 | 15.81 | False | 0.25 | 0.05 | 0.15 | 0.22 | 0.77 | False |
| vae_atsp | 15.24 | 15.62 | False | 0.13 | 0.18 | 0.15 | 0.22 | 0.82 | False |
| vae_greedy | 15.47 | 15.85 | False | 0.04 | 0.10 | 0.07 | 0.21 | 0.79 | False |
| chronos | 16.39 | 15.48 | False | 1.14 | -0.05 | 0.55 | 0.11 | 0.28 | False |
| vae_knn | 16.01 | 16.27 | False | 0.15 | 0.02 | 0.09 | 0.22 | 0.79 | False |
| vae_mbb | 16.31 | 16.73 | False | 0.15 | 0.01 | 0.08 | 0.16 | 0.55 | False |
| vae_rand | 16.56 | 16.78 | False | 0.00 | 0.00 | 0.00 | 0.12 | 0.60 | False |
| timestral | 17.35 | 16.50 | False | 0.11 | -0.38 | -0.13 | 0.61 | 0.86 | False |


## Criteria

Mean rank of every method in each criterion (references / splits averaged).

| method | fidelity:dependence | fidelity:distribution | fidelity:long_structure | fidelity:seams | fidelity:target | fidelity:windows | utility:classification | utility:regression |
|---|---|---|---|---|---|---|---|---|
| zedge_quilting | 7.36 | 8.86 | 9.23 | 6.73 | 6.56 | 10.99 | 7.77 | 8.10 |
| zedge_zseries | 7.93 | 8.75 | 9.62 | 9.97 | 6.33 | 10.11 | 8.86 | 8.38 |
| zedge_greedy | 8.44 | 9.18 | 9.68 | 9.52 | 6.51 | 10.92 | 8.50 | 8.71 |
| zedge_pctsp | 8.23 | 9.04 | 10.10 | 9.91 | 6.77 | 10.83 | 8.44 | 9.03 |
| zedge_ts_ar | 7.99 | 7.49 | 9.62 | 15.59 | 9.17 | 10.63 | 8.24 | 7.99 |
| zedge_atsp | 8.17 | 9.30 | 10.07 | 9.89 | 6.06 | 11.40 | 8.69 | 9.49 |
| zedge_knn | 8.62 | 9.08 | 9.82 | 9.95 | 7.37 | 10.96 | 8.72 | 9.40 |
| zedge_ts_long | 11.79 | 7.44 | 9.75 | 9.38 | 8.99 | 9.41 | 9.40 | 9.15 |
| zedge_herding | 10.33 | 8.33 | 10.33 | 12.84 | 9.36 | 10.34 | 9.38 | 11.59 |
| zedge_mbb | 10.31 | 9.12 | 10.58 | 11.89 | 10.44 | 10.59 | 9.13 | 11.99 |
| zedge_rand | 10.30 | 9.38 | 10.31 | 12.09 | 10.13 | 10.67 | 9.43 | 12.34 |
| vae_herding | 13.95 | 12.60 | 12.71 | 13.24 | 13.50 | 12.52 | 13.65 | 15.00 |
| vae_zseries | 13.72 | 13.95 | 13.41 | 14.43 | 11.24 | 13.48 | 14.22 | 14.36 |
| diffusion_ts | 14.45 | 12.18 | 14.44 | 17.05 | 15.64 | 12.54 | 14.73 | 12.10 |
| timesfm | 14.32 | 15.02 | 13.44 |  | 21.06 | 12.46 | 17.83 | 9.54 |
| vae_quilting | 17.20 | 15.80 | 14.43 | 7.69 | 15.62 | 14.36 | 14.23 | 15.65 |
| vae_pctsp | 16.06 | 15.61 | 14.57 | 14.36 | 14.18 | 14.05 | 15.31 | 16.31 |
| vae_atsp | 16.18 | 15.94 | 14.32 | 15.78 | 14.86 | 14.34 | 15.20 | 16.05 |
| vae_greedy | 16.29 | 16.53 | 14.85 | 15.44 | 15.27 | 14.45 | 15.51 | 16.19 |
| chronos | 15.86 | 19.52 | 16.83 | 10.22 | 19.04 | 16.86 | 17.67 | 13.29 |
| vae_knn | 16.47 | 17.11 | 15.24 | 16.01 | 16.42 | 14.79 | 15.68 | 16.86 |
| vae_mbb | 15.79 | 17.37 | 15.72 | 15.68 | 18.05 | 15.25 | 15.72 | 17.73 |
| vae_rand | 15.99 | 17.47 | 15.71 | 16.82 | 18.23 | 15.15 | 15.71 | 17.84 |
| timestral | 15.60 | 17.34 | 16.49 |  | 23.47 | 13.85 | 20.91 | 12.09 |


## Sensitivity

Columns: `text` — what the variant changes; `first` — the method with the lowest avg_rank in the variant; `tau_vs_main` — Kendall τ between the method order of the variant and of the leaderboard; `main_first_place` — place of the leaderboard's first method in the variant.

| variant | text | first | tau_vs_main | main_first_place |
|---|---|---|---|---|
| main | the leaderboard: core metrics, fidelity against train + val + OOT, noise-aware ranks | zedge_quilting | 1.00 | 1 |
| plain_ranks | ordinary average ranks (no ties within the noise) | zedge_quilting | 0.99 | 1 |
| fidelity_train | fidelity against train only | zedge_quilting | 0.98 | 1 |
| fidelity_holdout | fidelity against val + OOT only | zedge_quilting | 0.96 | 1 |
| no_unchecked | without F5.7 (seams, no anchor) and F6.1 against val (noise) | zedge_quilting | 0.95 | 1 |
| all_metrics | every fidelity metric instead of the core set | zedge_quilting | 0.93 | 1 |
| common_datasets | only the datasets where every method is ranked | zedge_quilting | 0.94 | 1 |


avg_rank of every method in every variant.

| method | main | plain_ranks | fidelity_train | fidelity_holdout | no_unchecked | all_metrics | common_datasets |
|---|---|---|---|---|---|---|---|
| zedge_quilting | 8.11 | 7.83 | 7.69 | 8.32 | 8.27 | 8.47 | 7.82 |
| zedge_zseries | 8.70 | 8.55 | 7.88 | 9.11 | 8.56 | 9.05 | 8.57 |
| zedge_greedy | 8.82 | 8.75 | 8.11 | 9.18 | 8.78 | 9.00 | 8.75 |
| zedge_pctsp | 8.94 | 8.89 | 8.18 | 9.32 | 8.86 | 9.11 | 8.58 |
| zedge_ts_ar | 9.10 | 8.89 | 8.51 | 9.39 | 8.52 | 8.95 | 9.12 |
| zedge_atsp | 9.12 | 9.10 | 8.48 | 9.44 | 9.07 | 9.32 | 8.63 |
| zedge_knn | 9.18 | 9.22 | 8.52 | 9.51 | 9.11 | 9.46 | 9.03 |
| zedge_ts_long | 9.37 | 9.21 | 8.89 | 9.60 | 9.31 | 9.80 | 9.59 |
| zedge_herding | 10.37 | 10.50 | 9.69 | 10.71 | 10.14 | 10.84 | 10.36 |
| zedge_mbb | 10.53 | 10.69 | 9.93 | 10.82 | 10.41 | 10.97 | 10.69 |
| zedge_rand | 10.68 | 10.85 | 10.09 | 10.98 | 10.53 | 11.15 | 10.80 |
| vae_herding | 13.71 | 13.82 | 13.51 | 13.80 | 13.72 | 14.22 | 13.60 |
| vae_zseries | 13.83 | 13.82 | 14.14 | 13.68 | 13.69 | 13.80 | 13.65 |
| diffusion_ts | 13.90 | 13.86 | 14.65 | 13.52 | 13.62 | 13.30 | 14.40 |
| timesfm | 14.47 | 14.39 | 15.56 | 13.93 | 14.37 | 13.94 | 15.05 |
| vae_quilting | 14.56 | 14.46 | 14.95 | 14.37 | 15.24 | 14.37 | 14.34 |
| vae_pctsp | 15.31 | 15.43 | 15.85 | 15.04 | 15.37 | 14.95 | 15.18 |
| vae_atsp | 15.43 | 15.51 | 15.90 | 15.19 | 15.38 | 15.01 | 15.06 |
| vae_greedy | 15.66 | 15.78 | 16.09 | 15.44 | 15.69 | 15.26 | 15.73 |
| chronos | 15.94 | 15.85 | 16.87 | 15.47 | 16.50 | 15.43 | 16.07 |
| vae_knn | 16.14 | 16.31 | 16.68 | 15.87 | 16.16 | 15.77 | 16.01 |
| vae_mbb | 16.52 | 16.61 | 17.05 | 16.25 | 16.62 | 16.49 | 16.35 |
| vae_rand | 16.67 | 16.72 | 17.21 | 16.40 | 16.69 | 16.54 | 16.40 |
| timestral | 16.92 | 16.86 | 18.51 | 16.13 | 16.90 | 16.03 | 16.89 |


## One method per generator

Kendall τ between the order of the representatives in their field and in the leaderboard: 1.00.

Columns: `method` — method id; `generator` — the generator the method's series come from (pool or long-series generator); `field` — the methods of the field (one per generator); `rank_in_field` — avg_rank of the method in its field; `place_in_field` — place in its field; `field_size` — number of methods in the field; `tier_in_field` — True — not significantly worse than the first method of the field.

| method | generator | field | rank_in_field | place_in_field | field_size | tier_in_field |
|---|---|---|---|---|---|---|
| zedge_quilting | zedge_ts | chronos, diffusion_ts, timesfm, timestral, vae_rand, zedge_quilting, zedge_ts_ar, zedge_ts_long | 3.13 | 1 | 8 | True |
| zedge_zseries | zedge_ts | chronos, diffusion_ts, timesfm, timestral, vae_rand, zedge_ts_ar, zedge_ts_long, zedge_zseries | 3.30 | 1 | 8 | True |
| zedge_greedy | zedge_ts | chronos, diffusion_ts, timesfm, timestral, vae_rand, zedge_greedy, zedge_ts_ar, zedge_ts_long | 3.32 | 1 | 8 | True |
| zedge_pctsp | zedge_ts | chronos, diffusion_ts, timesfm, timestral, vae_rand, zedge_pctsp, zedge_ts_ar, zedge_ts_long | 3.34 | 2 | 8 | True |
| zedge_ts_ar | zedge_ts_ar | chronos, diffusion_ts, timesfm, timestral, vae_rand, zedge_rand, zedge_ts_ar, zedge_ts_long | 3.25 | 1 | 8 | True |
| zedge_atsp | zedge_ts | chronos, diffusion_ts, timesfm, timestral, vae_rand, zedge_atsp, zedge_ts_ar, zedge_ts_long | 3.39 | 3 | 8 | True |
| zedge_knn | zedge_ts | chronos, diffusion_ts, timesfm, timestral, vae_rand, zedge_knn, zedge_ts_ar, zedge_ts_long | 3.42 | 3 | 8 | True |
| zedge_ts_long | zedge_ts_long | chronos, diffusion_ts, timesfm, timestral, vae_rand, zedge_rand, zedge_ts_ar, zedge_ts_long | 3.31 | 2 | 8 | True |
| zedge_herding | zedge_ts | chronos, diffusion_ts, timesfm, timestral, vae_rand, zedge_herding, zedge_ts_ar, zedge_ts_long | 3.67 | 3 | 8 | False |
| zedge_mbb | zedge_ts | chronos, diffusion_ts, timesfm, timestral, vae_rand, zedge_mbb, zedge_ts_ar, zedge_ts_long | 3.69 | 3 | 8 | False |
| zedge_rand | zedge_ts | chronos, diffusion_ts, timesfm, timestral, vae_rand, zedge_rand, zedge_ts_ar, zedge_ts_long | 3.73 | 3 | 8 | False |
| vae_herding | tsgm_vae | chronos, diffusion_ts, timesfm, timestral, vae_herding, zedge_rand, zedge_ts_ar, zedge_ts_long | 4.92 | 5 | 8 | False |
| vae_zseries | tsgm_vae | chronos, diffusion_ts, timesfm, timestral, vae_zseries, zedge_rand, zedge_ts_ar, zedge_ts_long | 4.96 | 5 | 8 | True |
| diffusion_ts | diffusion_ts | chronos, diffusion_ts, timesfm, timestral, vae_rand, zedge_rand, zedge_ts_ar, zedge_ts_long | 4.72 | 4 | 8 | False |
| timesfm | timesfm | chronos, diffusion_ts, timesfm, timestral, vae_rand, zedge_rand, zedge_ts_ar, zedge_ts_long | 4.88 | 5 | 8 | False |
| vae_quilting | tsgm_vae | chronos, diffusion_ts, timesfm, timestral, vae_quilting, zedge_rand, zedge_ts_ar, zedge_ts_long | 4.97 | 6 | 8 | True |
| vae_pctsp | tsgm_vae | chronos, diffusion_ts, timesfm, timestral, vae_pctsp, zedge_rand, zedge_ts_ar, zedge_ts_long | 5.18 | 6 | 8 | False |
| vae_atsp | tsgm_vae | chronos, diffusion_ts, timesfm, timestral, vae_atsp, zedge_rand, zedge_ts_ar, zedge_ts_long | 5.20 | 6 | 8 | True |
| vae_greedy | tsgm_vae | chronos, diffusion_ts, timesfm, timestral, vae_greedy, zedge_rand, zedge_ts_ar, zedge_ts_long | 5.23 | 6 | 8 | False |
| chronos | chronos | chronos, diffusion_ts, timesfm, timestral, vae_rand, zedge_rand, zedge_ts_ar, zedge_ts_long | 5.31 | 6 | 8 | False |
| vae_knn | tsgm_vae | chronos, diffusion_ts, timesfm, timestral, vae_knn, zedge_rand, zedge_ts_ar, zedge_ts_long | 5.28 | 6 | 8 | False |
| vae_mbb | tsgm_vae | chronos, diffusion_ts, timesfm, timestral, vae_mbb, zedge_rand, zedge_ts_ar, zedge_ts_long | 5.38 | 7 | 8 | False |
| vae_rand | tsgm_vae | chronos, diffusion_ts, timesfm, timestral, vae_rand, zedge_rand, zedge_ts_ar, zedge_ts_long | 5.40 | 7 | 8 | False |
| timestral | timestral | chronos, diffusion_ts, timesfm, timestral, vae_rand, zedge_rand, zedge_ts_ar, zedge_ts_long | 5.86 | 8 | 8 | False |


## Leave one dataset out

Columns: `method` — method id; `place` — place in the leaderboard (seeds averaged within a dataset, then the mean over datasets); `place_best` — best place with one dataset left out; `place_worst` — worst place with one dataset left out; `n_first` — number of the leave-one-dataset-out rankings in which the method is first; `n_left_out` — number of leave-one-dataset-out rankings (one per dataset).

| method | place | place_best | place_worst | n_first | n_left_out |
|---|---|---|---|---|---|
| zedge_quilting | 1.00 | 1.00 | 1.00 | 9 | 9 |
| zedge_zseries | 2.00 | 2.00 | 4.00 | 0 | 9 |
| zedge_greedy | 3.00 | 2.00 | 4.00 | 0 | 9 |
| zedge_pctsp | 4.00 | 3.00 | 5.00 | 0 | 9 |
| zedge_ts_ar | 5.00 | 3.00 | 7.00 | 0 | 9 |
| zedge_atsp | 6.00 | 3.00 | 7.00 | 0 | 9 |
| zedge_knn | 7.00 | 5.00 | 8.00 | 0 | 9 |
| zedge_ts_long | 8.00 | 6.00 | 8.00 | 0 | 9 |
| zedge_herding | 9.00 | 9.00 | 9.00 | 0 | 9 |
| zedge_mbb | 10.00 | 10.00 | 10.00 | 0 | 9 |
| zedge_rand | 11.00 | 11.00 | 11.00 | 0 | 9 |
| vae_herding | 12.00 | 12.00 | 13.00 | 0 | 9 |
| vae_zseries | 13.00 | 12.00 | 15.00 | 0 | 9 |
| diffusion_ts | 14.00 | 12.00 | 16.00 | 0 | 9 |
| timesfm | 15.00 | 14.00 | 16.00 | 0 | 9 |
| vae_quilting | 16.00 | 14.00 | 16.00 | 0 | 9 |
| vae_pctsp | 17.00 | 17.00 | 18.00 | 0 | 9 |
| vae_atsp | 18.00 | 17.00 | 20.00 | 0 | 9 |
| vae_greedy | 19.00 | 18.00 | 20.00 | 0 | 9 |
| chronos | 20.00 | 19.00 | 23.00 | 0 | 9 |
| vae_knn | 21.00 | 20.00 | 21.00 | 0 | 9 |
| vae_mbb | 22.00 | 21.00 | 23.00 | 0 | 9 |
| vae_rand | 23.00 | 22.00 | 24.00 | 0 | 9 |
| timestral | 24.00 | 22.00 | 24.00 | 0 | 9 |


## Random criterion weights

Dirichlet(1) weights within each domain, 2000 draws; median Kendall τ with equal weights: 0.91.

Columns: `method` — method id; `equal_weights_rank` — score of the method with equal criterion weights (lower = better); `p_first` — share of the draws in which the method is first; `p_top3` — share of the draws in which the method is among the three first.

| method | equal_weights_rank | p_first | p_top3 |
|---|---|---|---|
| zedge_quilting | 8.11 | 0.98 | 1.00 |
| zedge_zseries | 8.70 | 0.00 | 0.92 |
| zedge_greedy | 8.82 | 0.00 | 0.66 |
| zedge_pctsp | 8.94 | 0.00 | 0.07 |
| zedge_ts_ar | 9.10 | 0.02 | 0.32 |
| zedge_atsp | 9.12 | 0.00 | 0.01 |
| zedge_knn | 9.18 | 0.00 | 0.00 |
| zedge_ts_long | 9.37 | 0.00 | 0.03 |
| zedge_herding | 10.37 | 0.00 | 0.00 |
| zedge_mbb | 10.53 | 0.00 | 0.00 |
| zedge_rand | 10.68 | 0.00 | 0.00 |
| vae_herding | 13.71 | 0.00 | 0.00 |
| vae_zseries | 13.83 | 0.00 | 0.00 |
| diffusion_ts | 13.90 | 0.00 | 0.00 |
| timesfm | 14.25 | 0.00 | 0.00 |
| vae_quilting | 14.56 | 0.00 | 0.00 |
| vae_pctsp | 15.31 | 0.00 | 0.00 |
| vae_atsp | 15.43 | 0.00 | 0.00 |
| vae_greedy | 15.66 | 0.00 | 0.00 |
| chronos | 15.94 | 0.00 | 0.00 |
| vae_knn | 16.14 | 0.00 | 0.00 |
| vae_mbb | 16.52 | 0.00 | 0.00 |
| timestral | 16.53 | 0.00 | 0.00 |
| vae_rand | 16.67 | 0.00 | 0.00 |

