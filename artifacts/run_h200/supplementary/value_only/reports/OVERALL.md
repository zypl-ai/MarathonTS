# Overall leaderboard: fidelity and utility

Methods: 24. Datasets (9): beijing_pm25, bike, bitcoin, electricity, ett, household, jena, metro, pjm. Seeds: 10.

Composition (fixed in advance). Fidelity — the core criteria distribution (F1.2_w1, F2.1_ks_d24); dependence (F3.5_log_psd, F4.1_how_mean); windows (F6.1_disc_score, F6.4_mmd); long structure (F7.1_roll_mean_ks, F7.2_roll_std_ks); target (F11.1_class_share_logratio); seams (F5.7_seam_detect_auc_dev); each criterion the mean of its ranks against train, val and OOT. Utility — TSTR classification and regression with equal weights, each tested on val and OOT. Overall = mean of the two domains. Not included: privacy (memorisation flag next to the rank), time, memory.

Ranks are noise-aware: within a leaf two methods whose scores differ by no more than the noise of the leaf (median over seeds of |random − twin|, or the between-seed spread of the random path where the twin is not run) tie. Uncertainty: two-level bootstrap (datasets, then seeds), 10 seeds; tier — not significantly worse than the first method (one-sided Wilcoxon over datasets, Holm).

Friedman p = 7.52e-13, datasets × methods in the test = 9 × 22.

## Leaderboard

Columns: `method` — method id; `family` — method family: long-series generator, random selection, optimised selection, seam processing (a joiner on a stitcher that also runs without it; joiner in brackets); `avg_rank` — mean rank over datasets (seeds averaged within a dataset); 1 = best; `ci_lo` — lower bound of the 95% bootstrap interval of avg_rank; `ci_hi` — upper bound of the 95% bootstrap interval of avg_rank; `p_first` — share of bootstrap samples in which the method has the lowest avg_rank; `p_top3` — share of bootstrap samples in which the method is among the three lowest; `p_worse_than_best_holm` — p-value of the one-sided Wilcoxon test over datasets "worse than the first method", Holm correction; empty for the first method; `tier_wilcoxon` — True — not significantly worse than the first method (p_worse_than_best_holm ≥ 0.05); `n_datasets` — number of datasets in which the method is ranked.

Rows: sorted by avg_rank.

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon | n_datasets |
|---|---|---|---|---|---|---|---|---|---|
| zedge_quilting | optimised selection | 8.13 | 7.22 | 9.08 | 0.88 | 0.98 |  | True | 9 |
| zedge_zseries | optimised selection | 8.72 | 8.23 | 9.36 | 0.07 | 0.71 | 0.33 | True | 9 |
| zedge_greedy | optimised selection | 8.86 | 7.94 | 9.86 | 0.01 | 0.71 | 0.33 | True | 9 |
| zedge_pctsp | optimised selection | 9.10 | 8.10 | 10.18 | 0.00 | 0.15 | 0.26 | True | 9 |
| zedge_atsp | optimised selection | 9.25 | 7.79 | 10.85 | 0.01 | 0.16 | 0.33 | True | 9 |
| zedge_ts_long | long-series generator | 9.26 | 7.83 | 10.83 | 0.03 | 0.20 | 0.33 | True | 9 |
| zedge_knn | optimised selection | 9.30 | 8.33 | 10.39 | 0.00 | 0.02 | 0.29 | True | 9 |
| zedge_ts_ar | long-series generator | 9.45 | 8.02 | 11.00 | 0.00 | 0.08 | 0.29 | True | 9 |
| zedge_herding | optimised selection | 10.59 | 9.36 | 11.86 | 0.00 | 0.00 | 0.04 | False | 9 |
| zedge_mbb | optimised selection | 10.69 | 9.30 | 12.17 | 0.00 | 0.00 | 0.05 | True | 9 |
| zedge_rand | random selection | 10.87 | 9.33 | 12.44 | 0.00 | 0.00 | 0.05 | True | 9 |
| vae_herding | optimised selection | 13.53 | 12.81 | 14.28 | 0.00 | 0.00 | 0.04 | False | 9 |
| diffusion_ts | long-series generator | 13.57 | 11.72 | 15.24 | 0.00 | 0.00 | 0.04 | False | 9 |
| vae_zseries | optimised selection | 13.69 | 12.18 | 15.27 | 0.00 | 0.00 | 0.05 | True | 9 |
| vae_quilting | optimised selection | 14.52 | 12.74 | 16.21 | 0.00 | 0.00 | 0.05 | True | 9 |
| timesfm | long-series generator | 14.97 | 13.28 | 16.66 | 0.00 | 0.00 | 0.12 | True | 6 |
| vae_atsp | optimised selection | 15.30 | 13.37 | 17.07 | 0.00 | 0.00 | 0.04 | False | 9 |
| vae_pctsp | optimised selection | 15.33 | 13.90 | 16.69 | 0.00 | 0.00 | 0.04 | False | 9 |
| vae_greedy | optimised selection | 15.59 | 13.93 | 17.15 | 0.00 | 0.00 | 0.04 | False | 9 |
| chronos | long-series generator | 15.73 | 14.06 | 17.37 | 0.00 | 0.00 | 0.07 | True | 7 |
| vae_knn | optimised selection | 15.99 | 14.21 | 17.63 | 0.00 | 0.00 | 0.04 | False | 9 |
| vae_mbb | optimised selection | 16.17 | 14.20 | 18.00 | 0.00 | 0.00 | 0.04 | False | 9 |
| vae_rand | random selection | 16.35 | 14.42 | 18.16 | 0.00 | 0.00 | 0.04 | False | 9 |
| timestral | long-series generator | 17.29 | 16.17 | 18.40 | 0.00 | 0.00 | 0.04 | False | 9 |


## Next to the rank

Columns: `method` — method id; `fidelity_rank` — avg_rank in the fidelity domain alone (core criteria against train + val + OOT); `utility_rank` — avg_rank in the utility domain alone (TSTR classification + regression, val + OOT); `pareto_fid_ut` — True — no other method is at least as good in both fidelity_rank and utility_rank and strictly better in one; `norm_fidelity` — normalised fidelity: mean over the core criteria of the median normalised score (random assembly = 0, real = 1; against val and train); `norm_utility` — normalised utility: mean of classification and regression (TSTR, random = 0, TRTR = 1); `norm_overall` — mean of norm_fidelity and norm_utility; `near_copy_share` — median over datasets of F10.2: share of synthetic windows closer to train than the 5th percentile of real-to-real distances; `near_copy_ratio` — median over datasets of near_copy_share / near_copy_real; `memorisation_flag` — True — near_copy_ratio ≥ Config.near_copy_ratio (default 2) and p_more_copies_holm < α; reported, does not change the rank.

| method | fidelity_rank | utility_rank | pareto_fid_ut | norm_fidelity | norm_utility | norm_overall | near_copy_share | near_copy_ratio | memorisation_flag |
|---|---|---|---|---|---|---|---|---|---|
| zedge_quilting | 8.01 | 8.25 | True | 0.50 | 0.50 | 0.50 | 0.23 | 1.00 | False |
| zedge_zseries | 8.73 | 8.72 | False | 0.17 | 0.39 | 0.28 | 0.27 | 0.96 | False |
| zedge_greedy | 8.79 | 8.92 | False | 0.26 | 0.34 | 0.30 | 0.33 | 0.92 | False |
| zedge_pctsp | 8.94 | 9.26 | False | 0.13 | 0.39 | 0.26 | 0.32 | 0.97 | False |
| zedge_atsp | 8.86 | 9.64 | False | 0.31 | 0.36 | 0.33 | 0.32 | 0.93 | False |
| zedge_ts_long | 9.03 | 9.49 | False | 0.82 | 0.74 | 0.78 | 0.09 | 0.68 | False |
| zedge_knn | 9.23 | 9.37 | False | 0.41 | 0.36 | 0.39 | 0.31 | 0.89 | False |
| zedge_ts_ar | 10.21 | 8.69 | False | 0.64 | 0.89 | 0.77 | 0.04 | 0.94 | False |
| zedge_herding | 10.49 | 10.69 | False | 0.16 | -0.05 | 0.06 | 0.21 | 0.86 | False |
| zedge_mbb | 10.68 | 10.69 | False | 0.10 | 0.01 | 0.06 | 0.21 | 0.79 | False |
| zedge_rand | 10.73 | 11.01 | False | 0.00 | 0.00 | 0.00 | 0.20 | 0.85 | False |
| vae_herding | 13.11 | 13.95 | False | 0.36 | 0.24 | 0.30 | 0.08 | 0.64 | False |
| diffusion_ts | 13.92 | 13.22 | False | 0.62 | 0.39 | 0.50 | 0.20 | 1.00 | False |
| vae_zseries | 13.47 | 13.91 | False | 0.42 | 0.28 | 0.35 | 0.32 | 0.83 | False |
| vae_quilting | 14.34 | 14.69 | False | 0.01 | 0.16 | 0.08 | 0.20 | 0.79 | False |
| timesfm | 16.29 | 13.64 | False | -0.71 | 0.63 | -0.04 | 0.62 | 0.93 | False |
| vae_atsp | 15.27 | 15.33 | False | 0.08 | 0.18 | 0.13 | 0.22 | 0.82 | False |
| vae_pctsp | 14.98 | 15.69 | False | 0.29 | 0.05 | 0.17 | 0.22 | 0.77 | False |
| vae_greedy | 15.52 | 15.65 | False | -0.00 | 0.10 | 0.05 | 0.21 | 0.79 | False |
| chronos | 16.29 | 15.17 | False | -0.35 | 0.09 | -0.13 | 0.11 | 0.28 | False |
| vae_knn | 16.00 | 15.98 | False | 0.16 | 0.02 | 0.09 | 0.22 | 0.79 | False |
| vae_mbb | 16.00 | 16.35 | False | 0.14 | 0.01 | 0.07 | 0.16 | 0.55 | False |
| vae_rand | 16.27 | 16.43 | False | 0.00 | 0.00 | 0.00 | 0.12 | 0.60 | False |
| timestral | 18.34 | 16.24 | False | -1.19 | 0.10 | -0.55 | 0.61 | 0.86 | False |


## Criteria

Mean rank of every method in each criterion (references / splits averaged).

| method | fidelity:dependence | fidelity:distribution | fidelity:long_structure | fidelity:seams | fidelity:target | fidelity:windows | utility:classification | utility:regression |
|---|---|---|---|---|---|---|---|---|
| zedge_quilting | 5.68 | 8.70 | 9.24 | 6.93 | 6.74 | 10.78 | 8.09 | 8.41 |
| zedge_zseries | 7.21 | 8.61 | 9.78 | 10.06 | 6.34 | 10.40 | 8.86 | 8.57 |
| zedge_greedy | 7.21 | 9.07 | 9.55 | 9.43 | 6.66 | 10.82 | 8.74 | 9.11 |
| zedge_pctsp | 7.20 | 9.02 | 9.84 | 9.91 | 6.85 | 10.80 | 8.78 | 9.74 |
| zedge_atsp | 6.50 | 9.30 | 9.85 | 9.78 | 6.22 | 11.48 | 9.04 | 10.23 |
| zedge_ts_long | 8.68 | 7.73 | 9.65 | 9.45 | 8.97 | 9.68 | 9.61 | 9.38 |
| zedge_knn | 8.24 | 9.09 | 9.66 | 10.06 | 7.38 | 10.94 | 8.93 | 9.81 |
| zedge_ts_ar | 8.52 | 7.77 | 9.56 | 15.58 | 9.18 | 10.62 | 8.76 | 8.61 |
| zedge_herding | 11.75 | 8.42 | 10.01 | 13.00 | 9.29 | 10.48 | 9.66 | 11.72 |
| zedge_mbb | 11.69 | 9.24 | 10.34 | 11.90 | 10.22 | 10.69 | 9.39 | 12.00 |
| zedge_rand | 11.90 | 9.55 | 10.11 | 12.12 | 9.95 | 10.76 | 9.74 | 12.27 |
| vae_herding | 13.89 | 12.52 | 12.81 | 13.38 | 13.36 | 12.69 | 13.31 | 14.59 |
| diffusion_ts | 11.79 | 12.15 | 14.39 | 17.05 | 15.64 | 12.52 | 14.66 | 11.78 |
| vae_zseries | 13.98 | 14.01 | 13.49 | 14.39 | 11.42 | 13.52 | 13.71 | 14.11 |
| vae_quilting | 18.11 | 15.71 | 14.61 | 7.74 | 15.58 | 14.29 | 13.96 | 15.42 |
| timesfm | 19.78 | 15.01 | 13.21 |  | 21.02 | 12.43 | 17.82 | 9.46 |
| vae_atsp | 16.52 | 15.92 | 14.53 | 15.71 | 14.78 | 14.16 | 14.85 | 15.82 |
| vae_pctsp | 16.94 | 15.68 | 14.73 | 14.30 | 14.23 | 14.01 | 15.05 | 16.32 |
| vae_greedy | 16.53 | 16.52 | 15.15 | 15.25 | 15.27 | 14.43 | 15.21 | 16.10 |
| chronos | 15.25 | 19.50 | 17.04 | 10.13 | 19.02 | 16.83 | 17.57 | 12.77 |
| vae_knn | 16.28 | 17.00 | 15.53 | 15.90 | 16.54 | 14.74 | 15.41 | 16.54 |
| vae_mbb | 14.07 | 17.31 | 15.88 | 15.59 | 17.99 | 15.14 | 15.45 | 17.25 |
| vae_rand | 14.46 | 17.40 | 15.89 | 16.82 | 18.19 | 14.88 | 15.44 | 17.42 |
| timestral | 20.83 | 17.15 | 16.39 |  | 23.45 | 13.85 | 20.86 | 11.63 |


## Sensitivity

Columns: `text` — what the variant changes; `first` — the method with the lowest avg_rank in the variant; `tau_vs_main` — Kendall τ between the method order of the variant and of the leaderboard; `main_first_place` — place of the leaderboard's first method in the variant.

| variant | text | first | tau_vs_main | main_first_place |
|---|---|---|---|---|
| main | the leaderboard: core metrics, fidelity against train + val + OOT, noise-aware ranks | zedge_quilting | 1.00 | 1 |
| plain_ranks | ordinary average ranks (no ties within the noise) | zedge_quilting | 0.96 | 1 |
| fidelity_train | fidelity against train only | zedge_quilting | 0.96 | 1 |
| fidelity_holdout | fidelity against val + OOT only | zedge_quilting | 0.96 | 1 |
| no_unchecked | without F5.7 (seams, no anchor) and F6.1 against val (noise) | zedge_quilting | 0.94 | 1 |
| all_metrics | every fidelity metric instead of the core set | zedge_quilting | 0.93 | 1 |
| common_datasets | only the datasets where every method is ranked | zedge_quilting | 0.95 | 1 |


avg_rank of every method in every variant.

| method | main | plain_ranks | fidelity_train | fidelity_holdout | no_unchecked | all_metrics | common_datasets |
|---|---|---|---|---|---|---|---|
| zedge_quilting | 8.13 | 7.69 | 7.71 | 8.34 | 8.23 | 8.55 | 7.84 |
| zedge_zseries | 8.72 | 8.49 | 8.03 | 9.07 | 8.56 | 9.12 | 8.50 |
| zedge_greedy | 8.86 | 8.63 | 8.22 | 9.17 | 8.80 | 9.11 | 8.77 |
| zedge_pctsp | 9.10 | 8.78 | 8.40 | 9.45 | 8.99 | 9.32 | 8.70 |
| zedge_atsp | 9.25 | 8.95 | 8.68 | 9.53 | 9.16 | 9.51 | 8.77 |
| zedge_ts_long | 9.26 | 8.98 | 8.94 | 9.42 | 9.16 | 9.61 | 9.28 |
| zedge_knn | 9.30 | 9.16 | 8.70 | 9.60 | 9.20 | 9.63 | 9.17 |
| zedge_ts_ar | 9.45 | 8.97 | 9.06 | 9.64 | 8.89 | 9.29 | 9.50 |
| zedge_herding | 10.59 | 10.63 | 10.05 | 10.86 | 10.36 | 11.09 | 10.71 |
| zedge_mbb | 10.69 | 10.79 | 10.19 | 10.93 | 10.58 | 11.16 | 10.96 |
| zedge_rand | 10.87 | 10.97 | 10.40 | 11.10 | 10.74 | 11.35 | 11.08 |
| vae_herding | 13.53 | 13.81 | 13.43 | 13.58 | 13.53 | 14.04 | 13.61 |
| diffusion_ts | 13.57 | 13.66 | 14.26 | 13.23 | 13.25 | 13.09 | 13.95 |
| vae_zseries | 13.69 | 13.83 | 13.94 | 13.56 | 13.56 | 13.60 | 13.49 |
| vae_quilting | 14.52 | 14.54 | 14.90 | 14.32 | 15.21 | 14.20 | 14.26 |
| timesfm | 14.97 | 14.95 | 15.90 | 14.50 | 14.85 | 14.29 | 15.50 |
| vae_atsp | 15.30 | 15.54 | 15.67 | 15.11 | 15.27 | 14.80 | 14.88 |
| vae_pctsp | 15.33 | 15.50 | 15.78 | 15.11 | 15.43 | 14.85 | 15.17 |
| vae_greedy | 15.59 | 15.81 | 15.92 | 15.42 | 15.65 | 15.14 | 15.66 |
| chronos | 15.73 | 15.79 | 16.53 | 15.33 | 16.31 | 15.27 | 15.83 |
| vae_knn | 15.99 | 16.29 | 16.38 | 15.79 | 16.02 | 15.59 | 15.85 |
| vae_mbb | 16.17 | 16.47 | 16.58 | 15.97 | 16.26 | 16.26 | 16.03 |
| vae_rand | 16.35 | 16.61 | 16.76 | 16.15 | 16.35 | 16.32 | 16.07 |
| timestral | 17.29 | 17.38 | 18.60 | 16.63 | 17.27 | 16.19 | 17.19 |


## One method per generator

Kendall τ between the order of the representatives in their field and in the leaderboard: 1.00.

Columns: `method` — method id; `generator` — the generator the method's series come from (pool or long-series generator); `field` — the methods of the field (one per generator); `rank_in_field` — avg_rank of the method in its field; `place_in_field` — place in its field; `field_size` — number of methods in the field; `tier_in_field` — True — not significantly worse than the first method of the field.

| method | generator | field | rank_in_field | place_in_field | field_size | tier_in_field |
|---|---|---|---|---|---|---|
| zedge_quilting | zedge_ts | chronos, diffusion_ts, timesfm, timestral, vae_rand, zedge_quilting, zedge_ts_ar, zedge_ts_long | 3.13 | 1 | 8 | True |
| zedge_zseries | zedge_ts | chronos, diffusion_ts, timesfm, timestral, vae_rand, zedge_ts_ar, zedge_ts_long, zedge_zseries | 3.29 | 1 | 8 | True |
| zedge_greedy | zedge_ts | chronos, diffusion_ts, timesfm, timestral, vae_rand, zedge_greedy, zedge_ts_ar, zedge_ts_long | 3.31 | 1 | 8 | True |
| zedge_pctsp | zedge_ts | chronos, diffusion_ts, timesfm, timestral, vae_rand, zedge_pctsp, zedge_ts_ar, zedge_ts_long | 3.37 | 2 | 8 | True |
| zedge_atsp | zedge_ts | chronos, diffusion_ts, timesfm, timestral, vae_rand, zedge_atsp, zedge_ts_ar, zedge_ts_long | 3.39 | 3 | 8 | True |
| zedge_ts_long | zedge_ts_long | chronos, diffusion_ts, timesfm, timestral, vae_rand, zedge_rand, zedge_ts_ar, zedge_ts_long | 3.27 | 1 | 8 | True |
| zedge_knn | zedge_ts | chronos, diffusion_ts, timesfm, timestral, vae_rand, zedge_knn, zedge_ts_ar, zedge_ts_long | 3.41 | 3 | 8 | True |
| zedge_ts_ar | zedge_ts_ar | chronos, diffusion_ts, timesfm, timestral, vae_rand, zedge_rand, zedge_ts_ar, zedge_ts_long | 3.32 | 2 | 8 | True |
| zedge_herding | zedge_ts | chronos, diffusion_ts, timesfm, timestral, vae_rand, zedge_herding, zedge_ts_ar, zedge_ts_long | 3.67 | 3 | 8 | False |
| zedge_mbb | zedge_ts | chronos, diffusion_ts, timesfm, timestral, vae_rand, zedge_mbb, zedge_ts_ar, zedge_ts_long | 3.69 | 3 | 8 | False |
| zedge_rand | zedge_ts | chronos, diffusion_ts, timesfm, timestral, vae_rand, zedge_rand, zedge_ts_ar, zedge_ts_long | 3.73 | 3 | 8 | False |
| vae_herding | tsgm_vae | chronos, diffusion_ts, timesfm, timestral, vae_herding, zedge_rand, zedge_ts_ar, zedge_ts_long | 4.82 | 5 | 8 | False |
| diffusion_ts | diffusion_ts | chronos, diffusion_ts, timesfm, timestral, vae_rand, zedge_rand, zedge_ts_ar, zedge_ts_long | 4.60 | 4 | 8 | False |
| vae_zseries | tsgm_vae | chronos, diffusion_ts, timesfm, timestral, vae_zseries, zedge_rand, zedge_ts_ar, zedge_ts_long | 4.86 | 5 | 8 | False |
| vae_quilting | tsgm_vae | chronos, diffusion_ts, timesfm, timestral, vae_quilting, zedge_rand, zedge_ts_ar, zedge_ts_long | 4.94 | 5 | 8 | False |
| timesfm | timesfm | chronos, diffusion_ts, timesfm, timestral, vae_rand, zedge_rand, zedge_ts_ar, zedge_ts_long | 5.05 | 5 | 8 | False |
| vae_atsp | tsgm_vae | chronos, diffusion_ts, timesfm, timestral, vae_atsp, zedge_rand, zedge_ts_ar, zedge_ts_long | 5.16 | 6 | 8 | False |
| vae_pctsp | tsgm_vae | chronos, diffusion_ts, timesfm, timestral, vae_pctsp, zedge_rand, zedge_ts_ar, zedge_ts_long | 5.15 | 6 | 8 | False |
| vae_greedy | tsgm_vae | chronos, diffusion_ts, timesfm, timestral, vae_greedy, zedge_rand, zedge_ts_ar, zedge_ts_long | 5.18 | 6 | 8 | False |
| chronos | chronos | chronos, diffusion_ts, timesfm, timestral, vae_rand, zedge_rand, zedge_ts_ar, zedge_ts_long | 5.25 | 6 | 8 | False |
| vae_knn | tsgm_vae | chronos, diffusion_ts, timesfm, timestral, vae_knn, zedge_rand, zedge_ts_ar, zedge_ts_long | 5.25 | 6 | 8 | False |
| vae_mbb | tsgm_vae | chronos, diffusion_ts, timesfm, timestral, vae_mbb, zedge_rand, zedge_ts_ar, zedge_ts_long | 5.32 | 7 | 8 | False |
| vae_rand | tsgm_vae | chronos, diffusion_ts, timesfm, timestral, vae_rand, zedge_rand, zedge_ts_ar, zedge_ts_long | 5.34 | 7 | 8 | False |
| timestral | timestral | chronos, diffusion_ts, timesfm, timestral, vae_rand, zedge_rand, zedge_ts_ar, zedge_ts_long | 5.99 | 8 | 8 | False |


## Leave one dataset out

Columns: `method` — method id; `place` — place in the leaderboard (seeds averaged within a dataset, then the mean over datasets); `place_best` — best place with one dataset left out; `place_worst` — worst place with one dataset left out; `n_first` — number of the leave-one-dataset-out rankings in which the method is first; `n_left_out` — number of leave-one-dataset-out rankings (one per dataset).

| method | place | place_best | place_worst | n_first | n_left_out |
|---|---|---|---|---|---|
| zedge_quilting | 1.00 | 1.00 | 1.00 | 9 | 9 |
| zedge_zseries | 2.00 | 2.00 | 3.00 | 0 | 9 |
| zedge_greedy | 3.00 | 2.00 | 3.00 | 0 | 9 |
| zedge_pctsp | 4.00 | 4.00 | 6.00 | 0 | 9 |
| zedge_atsp | 5.00 | 4.00 | 7.00 | 0 | 9 |
| zedge_ts_long | 6.00 | 4.00 | 7.00 | 0 | 9 |
| zedge_knn | 7.00 | 5.00 | 8.00 | 0 | 9 |
| zedge_ts_ar | 8.00 | 6.00 | 8.00 | 0 | 9 |
| zedge_herding | 9.00 | 9.00 | 10.00 | 0 | 9 |
| zedge_mbb | 10.00 | 9.00 | 10.00 | 0 | 9 |
| zedge_rand | 11.00 | 11.00 | 11.00 | 0 | 9 |
| vae_herding | 12.00 | 12.00 | 14.00 | 0 | 9 |
| diffusion_ts | 13.00 | 12.00 | 15.00 | 0 | 9 |
| vae_zseries | 14.00 | 12.00 | 14.00 | 0 | 9 |
| vae_quilting | 15.00 | 14.00 | 16.00 | 0 | 9 |
| timesfm | 16.00 | 15.00 | 19.00 | 0 | 9 |
| vae_atsp | 17.00 | 16.00 | 20.00 | 0 | 9 |
| vae_pctsp | 18.00 | 17.00 | 18.00 | 0 | 9 |
| vae_greedy | 19.00 | 18.00 | 20.00 | 0 | 9 |
| chronos | 20.00 | 18.00 | 23.00 | 0 | 9 |
| vae_knn | 21.00 | 20.00 | 21.00 | 0 | 9 |
| vae_mbb | 22.00 | 21.00 | 22.00 | 0 | 9 |
| vae_rand | 23.00 | 22.00 | 23.00 | 0 | 9 |
| timestral | 24.00 | 24.00 | 24.00 | 0 | 9 |


## Random criterion weights

Dirichlet(1) weights within each domain, 2000 draws; median Kendall τ with equal weights: 0.91.

Columns: `method` — method id; `equal_weights_rank` — score of the method with equal criterion weights (lower = better); `p_first` — share of the draws in which the method is first; `p_top3` — share of the draws in which the method is among the three first.

| method | equal_weights_rank | p_first | p_top3 |
|---|---|---|---|
| zedge_quilting | 8.13 | 1.00 | 1.00 |
| zedge_zseries | 8.72 | 0.00 | 0.99 |
| zedge_greedy | 8.86 | 0.00 | 0.89 |
| zedge_pctsp | 9.10 | 0.00 | 0.00 |
| zedge_atsp | 9.25 | 0.00 | 0.00 |
| zedge_ts_long | 9.26 | 0.00 | 0.03 |
| zedge_knn | 9.30 | 0.00 | 0.00 |
| zedge_ts_ar | 9.45 | 0.00 | 0.08 |
| zedge_herding | 10.59 | 0.00 | 0.00 |
| zedge_mbb | 10.69 | 0.00 | 0.00 |
| zedge_rand | 10.87 | 0.00 | 0.00 |
| vae_herding | 13.53 | 0.00 | 0.00 |
| diffusion_ts | 13.57 | 0.00 | 0.00 |
| vae_zseries | 13.69 | 0.00 | 0.00 |
| vae_quilting | 14.52 | 0.00 | 0.00 |
| timesfm | 14.66 | 0.00 | 0.00 |
| vae_atsp | 15.30 | 0.00 | 0.00 |
| vae_pctsp | 15.33 | 0.00 | 0.00 |
| vae_greedy | 15.59 | 0.00 | 0.00 |
| chronos | 15.73 | 0.00 | 0.00 |
| vae_knn | 15.99 | 0.00 | 0.00 |
| vae_mbb | 16.17 | 0.00 | 0.00 |
| vae_rand | 16.35 | 0.00 | 0.00 |
| timestral | 16.81 | 0.00 | 0.00 |

