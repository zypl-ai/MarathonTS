# Overall leaderboard: fidelity and utility

Methods: 24. Datasets (9): beijing_pm25, bike, bitcoin, electricity, ett, household, jena, metro, pjm. Seeds: 10.

Composition (fixed in advance). Fidelity — the core criteria distribution (F1.2_w1, F2.1_ks_d24); dependence (F3.5_log_psd, F4.1_how_mean); windows (F6.1_disc_score, F6.4_mmd); long structure (F7.1_roll_mean_ks, F7.2_roll_std_ks); target (F11.1_class_share_logratio); seams (F5.7_seam_detect_auc_dev); each criterion the mean of its ranks against train, val and OOT. Utility — TSTR classification and regression with equal weights, each tested on val and OOT. Overall = mean of the two domains. Not included: privacy (memorisation flag next to the rank), time, memory.

Ranks are noise-aware: within a leaf two methods whose scores differ by no more than the noise of the leaf (median over seeds of |random − twin|, or the between-seed spread of the random path where the twin is not run) tie. Uncertainty: two-level bootstrap (datasets, then seeds), 10 seeds; tier — not significantly worse than the first method (one-sided Wilcoxon over datasets, Holm).

Friedman p = 2.38e-10, datasets × methods in the test = 9 × 22.

## Leaderboard

Columns: `method` — method id; `family` — method family: long-series generator, random selection, optimised selection, seam processing (a joiner on a stitcher that also runs without it; joiner in brackets); `avg_rank` — mean rank over datasets (seeds averaged within a dataset); 1 = best; `ci_lo` — lower bound of the 95% bootstrap interval of avg_rank; `ci_hi` — upper bound of the 95% bootstrap interval of avg_rank; `p_first` — share of bootstrap samples in which the method has the lowest avg_rank; `p_top3` — share of bootstrap samples in which the method is among the three lowest; `p_worse_than_best_holm` — p-value of the one-sided Wilcoxon test over datasets "worse than the first method", Holm correction; empty for the first method; `tier_wilcoxon` — True — not significantly worse than the first method (p_worse_than_best_holm ≥ 0.05); `n_datasets` — number of datasets in which the method is ranked.

Rows: sorted by avg_rank.

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon | n_datasets |
|---|---|---|---|---|---|---|---|---|---|
| zedge_quilting | optimised selection | 8.40 | 7.33 | 9.46 | 0.54 | 0.89 |  | True | 9 |
| zedge_zseries | optimised selection | 8.67 | 8.11 | 9.33 | 0.19 | 0.70 | 0.85 | True | 9 |
| zedge_ts_ar | long-series generator | 8.85 | 7.00 | 10.85 | 0.25 | 0.56 | 0.85 | True | 9 |
| zedge_greedy | optimised selection | 8.91 | 7.88 | 9.95 | 0.01 | 0.50 | 0.85 | True | 9 |
| zedge_pctsp | optimised selection | 9.09 | 8.01 | 10.17 | 0.00 | 0.13 | 0.75 | True | 9 |
| zedge_knn | optimised selection | 9.26 | 8.21 | 10.44 | 0.00 | 0.04 | 0.75 | True | 9 |
| zedge_atsp | optimised selection | 9.32 | 7.68 | 11.02 | 0.01 | 0.14 | 0.85 | True | 9 |
| zedge_ts_long | long-series generator | 9.51 | 8.00 | 11.22 | 0.00 | 0.05 | 0.57 | True | 9 |
| zedge_herding | optimised selection | 10.20 | 8.93 | 11.52 | 0.00 | 0.00 | 0.30 | True | 9 |
| zedge_mbb | optimised selection | 10.44 | 9.00 | 12.03 | 0.00 | 0.00 | 0.25 | True | 9 |
| zedge_rand | random selection | 10.59 | 9.00 | 12.24 | 0.00 | 0.00 | 0.20 | True | 9 |
| vae_herding | optimised selection | 13.50 | 12.67 | 14.38 | 0.00 | 0.00 | 0.04 | False | 9 |
| diffusion_ts | long-series generator | 13.51 | 11.58 | 15.16 | 0.00 | 0.00 | 0.04 | False | 9 |
| vae_zseries | optimised selection | 13.58 | 12.02 | 15.19 | 0.00 | 0.00 | 0.06 | True | 9 |
| timesfm | long-series generator | 14.43 | 12.56 | 16.23 | 0.00 | 0.00 | 0.17 | True | 6 |
| vae_quilting | optimised selection | 15.09 | 13.18 | 16.95 | 0.00 | 0.00 | 0.06 | True | 9 |
| vae_atsp | optimised selection | 15.23 | 13.31 | 17.06 | 0.00 | 0.00 | 0.06 | True | 9 |
| vae_pctsp | optimised selection | 15.32 | 13.71 | 16.85 | 0.00 | 0.00 | 0.04 | False | 9 |
| vae_greedy | optimised selection | 15.60 | 13.90 | 17.29 | 0.00 | 0.00 | 0.04 | False | 9 |
| vae_knn | optimised selection | 16.02 | 14.06 | 17.88 | 0.00 | 0.00 | 0.04 | False | 9 |
| vae_mbb | optimised selection | 16.37 | 14.05 | 18.50 | 0.00 | 0.00 | 0.04 | False | 9 |
| chronos | long-series generator | 16.41 | 14.67 | 18.10 | 0.00 | 0.00 | 0.09 | True | 7 |
| vae_rand | random selection | 16.44 | 14.19 | 18.62 | 0.00 | 0.00 | 0.04 | False | 9 |
| timestral | long-series generator | 16.77 | 15.53 | 18.08 | 0.00 | 0.00 | 0.04 | False | 9 |


## Next to the rank

Columns: `method` — method id; `fidelity_rank` — avg_rank in the fidelity domain alone (core criteria against train + val + OOT); `utility_rank` — avg_rank in the utility domain alone (TSTR classification + regression, val + OOT); `pareto_fid_ut` — True — no other method is at least as good in both fidelity_rank and utility_rank and strictly better in one; `norm_fidelity` — normalised fidelity: mean over the core criteria of the median normalised score (random assembly = 0, real = 1; against val and train); `norm_utility` — normalised utility: mean of classification and regression (TSTR, random = 0, TRTR = 1); `norm_overall` — mean of norm_fidelity and norm_utility; `near_copy_share` — median over datasets of F10.2: share of synthetic windows closer to train than the 5th percentile of real-to-real distances; `near_copy_ratio` — median over datasets of near_copy_share / near_copy_real; `memorisation_flag` — True — near_copy_ratio ≥ Config.near_copy_ratio (default 2) and p_more_copies_holm < α; reported, does not change the rank.

| method | fidelity_rank | utility_rank | pareto_fid_ut | norm_fidelity | norm_utility | norm_overall | near_copy_share | near_copy_ratio | memorisation_flag |
|---|---|---|---|---|---|---|---|---|---|
| zedge_quilting | 8.56 | 8.25 | True | 0.42 | 0.50 | 0.46 | 0.23 | 1.00 | False |
| zedge_zseries | 8.62 | 8.72 | False | 0.13 | 0.39 | 0.26 | 0.27 | 0.96 | False |
| zedge_ts_ar | 9.02 | 8.69 | False | 0.67 | 0.89 | 0.78 | 0.04 | 0.94 | False |
| zedge_greedy | 8.89 | 8.92 | False | 0.23 | 0.34 | 0.28 | 0.33 | 0.92 | False |
| zedge_pctsp | 8.93 | 9.26 | False | 0.11 | 0.39 | 0.25 | 0.32 | 0.97 | False |
| zedge_knn | 9.14 | 9.37 | False | 0.42 | 0.36 | 0.39 | 0.31 | 0.89 | False |
| zedge_atsp | 9.00 | 9.64 | False | 0.25 | 0.36 | 0.30 | 0.32 | 0.93 | False |
| zedge_ts_long | 9.53 | 9.49 | False | 0.73 | 0.74 | 0.74 | 0.09 | 0.68 | False |
| zedge_herding | 9.71 | 10.69 | False | 0.14 | -0.05 | 0.05 | 0.21 | 0.86 | False |
| zedge_mbb | 10.18 | 10.69 | False | 0.10 | 0.01 | 0.06 | 0.21 | 0.79 | False |
| zedge_rand | 10.17 | 11.01 | False | 0.00 | 0.00 | 0.00 | 0.20 | 0.85 | False |
| vae_herding | 13.06 | 13.95 | False | 0.37 | 0.24 | 0.30 | 0.08 | 0.64 | False |
| diffusion_ts | 13.80 | 13.22 | False | 0.55 | 0.39 | 0.47 | 0.20 | 1.00 | False |
| vae_zseries | 13.26 | 13.91 | False | 0.40 | 0.28 | 0.34 | 0.32 | 0.83 | False |
| timesfm | 15.21 | 13.64 | False | -0.42 | 0.63 | 0.11 | 0.62 | 0.93 | False |
| vae_quilting | 15.49 | 14.69 | False | 0.10 | 0.16 | 0.13 | 0.20 | 0.79 | False |
| vae_atsp | 15.13 | 15.33 | False | 0.13 | 0.18 | 0.15 | 0.22 | 0.82 | False |
| vae_pctsp | 14.96 | 15.69 | False | 0.25 | 0.05 | 0.15 | 0.22 | 0.77 | False |
| vae_greedy | 15.54 | 15.65 | False | 0.04 | 0.10 | 0.07 | 0.21 | 0.79 | False |
| vae_knn | 16.07 | 15.98 | False | 0.15 | 0.02 | 0.09 | 0.22 | 0.79 | False |
| vae_mbb | 16.39 | 16.35 | False | 0.15 | 0.01 | 0.08 | 0.16 | 0.55 | False |
| chronos | 17.65 | 15.17 | False | -0.34 | 0.09 | -0.12 | 0.11 | 0.28 | False |
| vae_rand | 16.45 | 16.43 | False | 0.00 | 0.00 | 0.00 | 0.12 | 0.60 | False |
| timestral | 17.30 | 16.24 | False | -0.98 | 0.10 | -0.44 | 0.61 | 0.86 | False |


## Criteria

Mean rank of every method in each criterion (references / splits averaged).

| method | fidelity:dependence | fidelity:distribution | fidelity:long_structure | fidelity:target | fidelity:windows | utility:classification | utility:regression |
|---|---|---|---|---|---|---|---|
| zedge_quilting | 7.33 | 8.70 | 9.24 | 6.74 | 10.78 | 8.09 | 8.41 |
| zedge_zseries | 7.96 | 8.61 | 9.78 | 6.34 | 10.40 | 8.86 | 8.57 |
| zedge_ts_ar | 7.95 | 7.77 | 9.56 | 9.18 | 10.62 | 8.76 | 8.61 |
| zedge_greedy | 8.34 | 9.07 | 9.55 | 6.66 | 10.82 | 8.74 | 9.11 |
| zedge_pctsp | 8.11 | 9.02 | 9.84 | 6.85 | 10.80 | 8.78 | 9.74 |
| zedge_knn | 8.66 | 9.09 | 9.66 | 7.38 | 10.94 | 8.93 | 9.81 |
| zedge_atsp | 8.17 | 9.30 | 9.85 | 6.22 | 11.48 | 9.04 | 10.23 |
| zedge_ts_long | 11.60 | 7.73 | 9.65 | 8.97 | 9.68 | 9.61 | 9.38 |
| zedge_herding | 10.37 | 8.42 | 10.01 | 9.29 | 10.48 | 9.66 | 11.72 |
| zedge_mbb | 10.44 | 9.24 | 10.34 | 10.22 | 10.69 | 9.39 | 12.00 |
| zedge_rand | 10.46 | 9.55 | 10.11 | 9.95 | 10.76 | 9.74 | 12.27 |
| vae_herding | 13.92 | 12.52 | 12.81 | 13.36 | 12.69 | 13.31 | 14.59 |
| diffusion_ts | 14.28 | 12.15 | 14.39 | 15.64 | 12.52 | 14.66 | 11.78 |
| vae_zseries | 13.83 | 14.01 | 13.49 | 11.42 | 13.52 | 13.71 | 14.11 |
| timesfm | 14.39 | 15.01 | 13.21 | 21.02 | 12.43 | 17.82 | 9.46 |
| vae_quilting | 17.24 | 15.71 | 14.61 | 15.58 | 14.29 | 13.96 | 15.42 |
| vae_atsp | 16.28 | 15.92 | 14.53 | 14.78 | 14.16 | 14.85 | 15.82 |
| vae_pctsp | 16.15 | 15.68 | 14.73 | 14.23 | 14.01 | 15.05 | 16.32 |
| vae_greedy | 16.33 | 16.52 | 15.15 | 15.27 | 14.43 | 15.21 | 16.10 |
| vae_knn | 16.52 | 17.00 | 15.53 | 16.54 | 14.74 | 15.41 | 16.54 |
| vae_mbb | 15.66 | 17.31 | 15.88 | 17.99 | 15.14 | 15.45 | 17.25 |
| chronos | 15.88 | 19.50 | 17.04 | 19.02 | 16.83 | 17.57 | 12.77 |
| vae_rand | 15.89 | 17.40 | 15.89 | 18.19 | 14.88 | 15.44 | 17.42 |
| timestral | 15.63 | 17.15 | 16.39 | 23.45 | 13.85 | 20.86 | 11.63 |


## Sensitivity

Columns: `text` — what the variant changes; `first` — the method with the lowest avg_rank in the variant; `tau_vs_main` — Kendall τ between the method order of the variant and of the leaderboard; `main_first_place` — place of the leaderboard's first method in the variant.

| variant | text | first | tau_vs_main | main_first_place |
|---|---|---|---|---|
| main | the leaderboard: core metrics, fidelity against train + val + OOT, noise-aware ranks | zedge_quilting | 1.00 | 1 |
| plain_ranks | ordinary average ranks (no ties within the noise) | zedge_quilting | 0.96 | 1 |
| fidelity_train | fidelity against train only | zedge_zseries | 0.96 | 2 |
| fidelity_holdout | fidelity against val + OOT only | zedge_quilting | 0.96 | 1 |
| no_unchecked | without F5.7 (seams, no anchor) and F6.1 against val (noise) | zedge_quilting | 0.99 | 1 |
| all_metrics | every fidelity metric instead of the core set | zedge_quilting | 0.97 | 1 |
| common_datasets | only the datasets where every method is ranked | zedge_quilting | 0.95 | 1 |


avg_rank of every method in every variant.

| method | main | plain_ranks | fidelity_train | fidelity_holdout | no_unchecked | all_metrics | common_datasets |
|---|---|---|---|---|---|---|---|
| zedge_quilting | 8.40 | 8.02 | 7.87 | 8.67 | 8.39 | 8.76 | 8.16 |
| zedge_zseries | 8.67 | 8.45 | 7.70 | 9.15 | 8.64 | 9.04 | 8.46 |
| zedge_ts_ar | 8.85 | 8.35 | 8.23 | 9.16 | 8.83 | 9.13 | 8.82 |
| zedge_greedy | 8.91 | 8.72 | 8.10 | 9.31 | 8.91 | 9.13 | 8.94 |
| zedge_pctsp | 9.09 | 8.81 | 8.20 | 9.54 | 9.08 | 9.38 | 8.89 |
| zedge_knn | 9.26 | 9.17 | 8.46 | 9.65 | 9.24 | 9.55 | 9.16 |
| zedge_atsp | 9.32 | 9.02 | 8.60 | 9.68 | 9.33 | 9.60 | 9.02 |
| zedge_ts_long | 9.51 | 9.28 | 9.01 | 9.76 | 9.46 | 9.95 | 9.74 |
| zedge_herding | 10.20 | 10.21 | 9.43 | 10.59 | 10.22 | 10.62 | 10.35 |
| zedge_mbb | 10.44 | 10.58 | 9.74 | 10.79 | 10.45 | 10.69 | 10.75 |
| zedge_rand | 10.59 | 10.69 | 9.91 | 10.92 | 10.59 | 10.83 | 10.83 |
| vae_herding | 13.50 | 13.78 | 13.31 | 13.60 | 13.54 | 13.63 | 13.43 |
| diffusion_ts | 13.51 | 13.59 | 14.36 | 13.08 | 13.50 | 13.17 | 13.96 |
| vae_zseries | 13.58 | 13.67 | 13.90 | 13.42 | 13.55 | 13.54 | 13.26 |
| timesfm | 14.43 | 14.39 | 15.52 | 13.88 | 14.31 | 13.92 | 15.03 |
| vae_quilting | 15.09 | 15.16 | 15.52 | 14.87 | 15.12 | 14.77 | 14.79 |
| vae_atsp | 15.23 | 15.45 | 15.74 | 14.98 | 15.25 | 15.06 | 14.80 |
| vae_pctsp | 15.32 | 15.43 | 15.90 | 15.04 | 15.35 | 15.24 | 15.07 |
| vae_greedy | 15.60 | 15.77 | 16.05 | 15.37 | 15.63 | 15.39 | 15.52 |
| vae_knn | 16.02 | 16.30 | 16.59 | 15.74 | 16.05 | 15.72 | 15.69 |
| vae_mbb | 16.37 | 16.66 | 16.98 | 16.07 | 16.42 | 16.03 | 16.03 |
| chronos | 16.41 | 16.48 | 17.53 | 15.85 | 16.37 | 15.49 | 16.42 |
| vae_rand | 16.44 | 16.70 | 17.05 | 16.13 | 16.49 | 16.08 | 16.08 |
| timestral | 16.77 | 16.86 | 18.43 | 15.94 | 16.75 | 16.51 | 16.82 |


## One method per generator

Kendall τ between the order of the representatives in their field and in the leaderboard: 0.93.

Columns: `method` — method id; `generator` — the generator the method's series come from (pool or long-series generator); `field` — the methods of the field (one per generator); `rank_in_field` — avg_rank of the method in its field; `place_in_field` — place in its field; `field_size` — number of methods in the field; `tier_in_field` — True — not significantly worse than the first method of the field.

| method | generator | field | rank_in_field | place_in_field | field_size | tier_in_field |
|---|---|---|---|---|---|---|
| zedge_quilting | zedge_ts | chronos, diffusion_ts, timesfm, timestral, vae_rand, zedge_quilting, zedge_ts_ar, zedge_ts_long | 3.23 | 1 | 8 | True |
| zedge_zseries | zedge_ts | chronos, diffusion_ts, timesfm, timestral, vae_rand, zedge_ts_ar, zedge_ts_long, zedge_zseries | 3.32 | 2 | 8 | True |
| zedge_ts_ar | zedge_ts_ar | chronos, diffusion_ts, timesfm, timestral, vae_rand, zedge_rand, zedge_ts_ar, zedge_ts_long | 3.17 | 1 | 8 | True |
| zedge_greedy | zedge_ts | chronos, diffusion_ts, timesfm, timestral, vae_rand, zedge_greedy, zedge_ts_ar, zedge_ts_long | 3.35 | 2 | 8 | True |
| zedge_pctsp | zedge_ts | chronos, diffusion_ts, timesfm, timestral, vae_rand, zedge_pctsp, zedge_ts_ar, zedge_ts_long | 3.40 | 2 | 8 | True |
| zedge_knn | zedge_ts | chronos, diffusion_ts, timesfm, timestral, vae_rand, zedge_knn, zedge_ts_ar, zedge_ts_long | 3.43 | 2 | 8 | True |
| zedge_atsp | zedge_ts | chronos, diffusion_ts, timesfm, timestral, vae_rand, zedge_atsp, zedge_ts_ar, zedge_ts_long | 3.44 | 3 | 8 | True |
| zedge_ts_long | zedge_ts_long | chronos, diffusion_ts, timesfm, timestral, vae_rand, zedge_rand, zedge_ts_ar, zedge_ts_long | 3.38 | 2 | 8 | True |
| zedge_herding | zedge_ts | chronos, diffusion_ts, timesfm, timestral, vae_rand, zedge_herding, zedge_ts_ar, zedge_ts_long | 3.61 | 3 | 8 | True |
| zedge_mbb | zedge_ts | chronos, diffusion_ts, timesfm, timestral, vae_rand, zedge_mbb, zedge_ts_ar, zedge_ts_long | 3.66 | 3 | 8 | False |
| zedge_rand | zedge_ts | chronos, diffusion_ts, timesfm, timestral, vae_rand, zedge_rand, zedge_ts_ar, zedge_ts_long | 3.70 | 3 | 8 | False |
| vae_herding | tsgm_vae | chronos, diffusion_ts, timesfm, timestral, vae_herding, zedge_rand, zedge_ts_ar, zedge_ts_long | 4.83 | 5 | 8 | False |
| diffusion_ts | diffusion_ts | chronos, diffusion_ts, timesfm, timestral, vae_rand, zedge_rand, zedge_ts_ar, zedge_ts_long | 4.58 | 4 | 8 | False |
| vae_zseries | tsgm_vae | chronos, diffusion_ts, timesfm, timestral, vae_zseries, zedge_rand, zedge_ts_ar, zedge_ts_long | 4.86 | 5 | 8 | True |
| timesfm | timesfm | chronos, diffusion_ts, timesfm, timestral, vae_rand, zedge_rand, zedge_ts_ar, zedge_ts_long | 4.88 | 5 | 8 | True |
| vae_quilting | tsgm_vae | chronos, diffusion_ts, timesfm, timestral, vae_quilting, zedge_rand, zedge_ts_ar, zedge_ts_long | 5.11 | 6 | 8 | True |
| vae_atsp | tsgm_vae | chronos, diffusion_ts, timesfm, timestral, vae_atsp, zedge_rand, zedge_ts_ar, zedge_ts_long | 5.14 | 6 | 8 | True |
| vae_pctsp | tsgm_vae | chronos, diffusion_ts, timesfm, timestral, vae_pctsp, zedge_rand, zedge_ts_ar, zedge_ts_long | 5.17 | 6 | 8 | True |
| vae_greedy | tsgm_vae | chronos, diffusion_ts, timesfm, timestral, vae_greedy, zedge_rand, zedge_ts_ar, zedge_ts_long | 5.19 | 6 | 8 | True |
| vae_knn | tsgm_vae | chronos, diffusion_ts, timesfm, timestral, vae_knn, zedge_rand, zedge_ts_ar, zedge_ts_long | 5.24 | 6 | 8 | True |
| vae_mbb | tsgm_vae | chronos, diffusion_ts, timesfm, timestral, vae_mbb, zedge_rand, zedge_ts_ar, zedge_ts_long | 5.34 | 6 | 8 | True |
| chronos | chronos | chronos, diffusion_ts, timesfm, timestral, vae_rand, zedge_rand, zedge_ts_ar, zedge_ts_long | 5.48 | 7 | 8 | True |
| vae_rand | tsgm_vae | chronos, diffusion_ts, timesfm, timestral, vae_rand, zedge_rand, zedge_ts_ar, zedge_ts_long | 5.33 | 6 | 8 | True |
| timestral | timestral | chronos, diffusion_ts, timesfm, timestral, vae_rand, zedge_rand, zedge_ts_ar, zedge_ts_long | 5.82 | 8 | 8 | False |


## Leave one dataset out

Columns: `method` — method id; `place` — place in the leaderboard (seeds averaged within a dataset, then the mean over datasets); `place_best` — best place with one dataset left out; `place_worst` — worst place with one dataset left out; `n_first` — number of the leave-one-dataset-out rankings in which the method is first; `n_left_out` — number of leave-one-dataset-out rankings (one per dataset).

| method | place | place_best | place_worst | n_first | n_left_out |
|---|---|---|---|---|---|
| zedge_quilting | 1.00 | 1.00 | 2.00 | 8 | 9 |
| zedge_zseries | 2.00 | 2.00 | 4.00 | 0 | 9 |
| zedge_ts_ar | 3.00 | 1.00 | 5.00 | 1 | 9 |
| zedge_greedy | 4.00 | 3.00 | 5.00 | 0 | 9 |
| zedge_pctsp | 5.00 | 4.00 | 6.00 | 0 | 9 |
| zedge_knn | 6.00 | 6.00 | 7.00 | 0 | 9 |
| zedge_atsp | 7.00 | 5.00 | 8.00 | 0 | 9 |
| zedge_ts_long | 8.00 | 6.00 | 8.00 | 0 | 9 |
| zedge_herding | 9.00 | 9.00 | 9.00 | 0 | 9 |
| zedge_mbb | 10.00 | 10.00 | 10.00 | 0 | 9 |
| zedge_rand | 11.00 | 11.00 | 11.00 | 0 | 9 |
| vae_herding | 12.00 | 12.00 | 14.00 | 0 | 9 |
| diffusion_ts | 13.00 | 12.00 | 14.00 | 0 | 9 |
| vae_zseries | 14.00 | 12.00 | 15.00 | 0 | 9 |
| timesfm | 15.00 | 14.00 | 17.00 | 0 | 9 |
| vae_quilting | 16.00 | 15.00 | 17.00 | 0 | 9 |
| vae_atsp | 17.00 | 15.00 | 18.00 | 0 | 9 |
| vae_pctsp | 18.00 | 16.00 | 18.00 | 0 | 9 |
| vae_greedy | 19.00 | 19.00 | 19.00 | 0 | 9 |
| vae_knn | 20.00 | 20.00 | 22.00 | 0 | 9 |
| vae_mbb | 21.00 | 21.00 | 23.00 | 0 | 9 |
| chronos | 22.00 | 20.00 | 24.00 | 0 | 9 |
| vae_rand | 23.00 | 22.00 | 24.00 | 0 | 9 |
| timestral | 24.00 | 21.00 | 24.00 | 0 | 9 |


## Random criterion weights

Dirichlet(1) weights within each domain, 2000 draws; median Kendall τ with equal weights: 0.93.

Columns: `method` — method id; `equal_weights_rank` — score of the method with equal criterion weights (lower = better); `p_first` — share of the draws in which the method is first; `p_top3` — share of the draws in which the method is among the three first.

| method | equal_weights_rank | p_first | p_top3 |
|---|---|---|---|
| zedge_quilting | 8.40 | 0.97 | 1.00 |
| zedge_zseries | 8.67 | 0.01 | 0.99 |
| zedge_ts_ar | 8.85 | 0.02 | 0.61 |
| zedge_greedy | 8.91 | 0.00 | 0.40 |
| zedge_pctsp | 9.09 | 0.00 | 0.00 |
| zedge_knn | 9.26 | 0.00 | 0.00 |
| zedge_atsp | 9.32 | 0.00 | 0.00 |
| zedge_ts_long | 9.51 | 0.00 | 0.00 |
| zedge_herding | 10.20 | 0.00 | 0.00 |
| zedge_mbb | 10.44 | 0.00 | 0.00 |
| zedge_rand | 10.59 | 0.00 | 0.00 |
| vae_herding | 13.50 | 0.00 | 0.00 |
| diffusion_ts | 13.51 | 0.00 | 0.00 |
| vae_zseries | 13.58 | 0.00 | 0.00 |
| timesfm | 14.43 | 0.00 | 0.00 |
| vae_quilting | 15.09 | 0.00 | 0.00 |
| vae_atsp | 15.23 | 0.00 | 0.00 |
| vae_pctsp | 15.32 | 0.00 | 0.00 |
| vae_greedy | 15.60 | 0.00 | 0.00 |
| vae_knn | 16.02 | 0.00 | 0.00 |
| vae_mbb | 16.37 | 0.00 | 0.00 |
| chronos | 16.41 | 0.00 | 0.00 |
| vae_rand | 16.44 | 0.00 | 0.00 |
| timestral | 16.77 | 0.00 | 0.00 |

