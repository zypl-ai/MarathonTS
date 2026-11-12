# Overall leaderboard: fidelity and utility

Methods: 13. Datasets (9): beijing_pm25, bike, bitcoin, electricity, ett, household, jena, metro, pjm. Seeds: 10.

Composition (fixed in advance). Fidelity — the core criteria distribution (F1.2_w1, F2.1_ks_d24); dependence (F3.5_log_psd, F4.1_how_mean); windows (F6.1_disc_score, F6.4_mmd); long structure (F7.1_roll_mean_ks, F7.2_roll_std_ks); target (F11.1_class_share_logratio); seams (F5.7_seam_detect_auc_dev); each criterion the mean of its ranks against train, val and OOT. Utility — TSTR classification and regression with equal weights, each tested on val and OOT. Overall = mean of the two domains. Not included: privacy (memorisation flag next to the rank), time, memory.

Ranks are noise-aware: within a leaf two methods whose scores differ by no more than the noise of the leaf (median over seeds of |random − twin|, or the between-seed spread of the random path where the twin is not run) tie. Uncertainty: two-level bootstrap (datasets, then seeds), 10 seeds; tier — not significantly worse than the first method (one-sided Wilcoxon over datasets, Holm).

Friedman p = 0.012, datasets × methods in the test = 9 × 11.

## Leaderboard

Columns: `method` — method id; `family` — method family: long-series generator, random selection, optimised selection, seam processing (a joiner on a stitcher that also runs without it; joiner in brackets); `avg_rank` — mean rank over datasets (seeds averaged within a dataset); 1 = best; `ci_lo` — lower bound of the 95% bootstrap interval of avg_rank; `ci_hi` — upper bound of the 95% bootstrap interval of avg_rank; `p_first` — share of bootstrap samples in which the method has the lowest avg_rank; `p_top3` — share of bootstrap samples in which the method is among the three lowest; `p_worse_than_best_holm` — p-value of the one-sided Wilcoxon test over datasets "worse than the first method", Holm correction; empty for the first method; `tier_wilcoxon` — True — not significantly worse than the first method (p_worse_than_best_holm ≥ 0.05); `n_datasets` — number of datasets in which the method is ranked.

Rows: sorted by avg_rank.

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon | n_datasets |
|---|---|---|---|---|---|---|---|---|---|
| vae_herding | optimised selection | 5.44 | 4.72 | 6.11 | 0.79 | 1.00 |  | True | 9 |
| diffusion_ts | long-series generator | 6.13 | 4.57 | 7.48 | 0.10 | 0.67 | 0.38 | True | 9 |
| vae_zseries | optimised selection | 6.31 | 5.54 | 7.14 | 0.08 | 0.59 | 0.38 | True | 9 |
| vae_quilting | optimised selection | 6.68 | 6.07 | 7.32 | 0.00 | 0.23 | 0.33 | True | 9 |
| timesfm | long-series generator | 6.72 | 5.29 | 8.27 | 0.03 | 0.38 | 0.38 | True | 6 |
| vae_atsp | optimised selection | 7.04 | 6.48 | 7.71 | 0.00 | 0.02 | 0.14 | True | 9 |
| vae_rand | random selection | 7.11 | 6.22 | 7.92 | 0.00 | 0.07 | 0.14 | True | 9 |
| vae_mbb | optimised selection | 7.12 | 6.31 | 7.87 | 0.00 | 0.03 | 0.09 | True | 9 |
| vae_pctsp | optimised selection | 7.28 | 6.74 | 7.80 | 0.00 | 0.00 | 0.06 | True | 9 |
| vae_knn | optimised selection | 7.44 | 6.89 | 8.02 | 0.00 | 0.00 | 0.09 | True | 9 |
| vae_greedy | optimised selection | 7.44 | 6.99 | 7.97 | 0.00 | 0.00 | 0.06 | True | 9 |
| chronos | long-series generator | 7.84 | 6.41 | 9.08 | 0.00 | 0.01 | 0.14 | True | 7 |
| timestral | long-series generator | 8.56 | 7.46 | 9.50 | 0.00 | 0.00 | 0.05 | False | 9 |


## Next to the rank

Columns: `method` — method id; `fidelity_rank` — avg_rank in the fidelity domain alone (core criteria against train + val + OOT); `utility_rank` — avg_rank in the utility domain alone (TSTR classification + regression, val + OOT); `pareto_fid_ut` — True — no other method is at least as good in both fidelity_rank and utility_rank and strictly better in one; `norm_fidelity` — normalised fidelity: mean over the core criteria of the median normalised score (random assembly = 0, real = 1; against val and train); `norm_utility` — normalised utility: mean of classification and regression (TSTR, random = 0, TRTR = 1); `norm_overall` — mean of norm_fidelity and norm_utility; `near_copy_share` — median over datasets of F10.2: share of synthetic windows closer to train than the 5th percentile of real-to-real distances; `near_copy_ratio` — median over datasets of near_copy_share / near_copy_real; `memorisation_flag` — True — near_copy_ratio ≥ Config.near_copy_ratio (default 2) and p_more_copies_holm < α; reported, does not change the rank.

| method | fidelity_rank | utility_rank | pareto_fid_ut | norm_fidelity | norm_utility | norm_overall | near_copy_share | near_copy_ratio | memorisation_flag |
|---|---|---|---|---|---|---|---|---|---|
| vae_herding | 4.99 | 5.90 | True | 0.36 | 0.17 | 0.27 | 0.11 | 0.63 | False |
| diffusion_ts | 6.54 | 5.71 | True | 0.06 | 0.26 | 0.16 | 0.14 | 0.96 | False |
| vae_zseries | 5.79 | 6.84 | False | 0.04 | 0.09 | 0.07 | 0.31 | 0.66 | False |
| vae_quilting | 6.85 | 6.50 | False | 0.06 | 0.15 | 0.10 | 0.22 | 0.50 | False |
| timesfm | 7.37 | 6.06 | False | -0.59 | 0.61 | 0.01 | 0.62 | 0.93 | False |
| vae_atsp | 6.73 | 7.35 | False | -0.02 | 0.06 | 0.02 | 0.26 | 0.65 | False |
| vae_rand | 6.85 | 7.37 | False | 0.00 | 0.00 | 0.00 | 0.18 | 0.57 | False |
| vae_mbb | 6.92 | 7.32 | False | 0.10 | -0.01 | 0.04 | 0.17 | 0.55 | False |
| vae_pctsp | 6.96 | 7.60 | False | -0.17 | 0.10 | -0.03 | 0.34 | 0.60 | False |
| vae_knn | 7.36 | 7.52 | False | -0.04 | 0.10 | 0.03 | 0.13 | 0.44 | False |
| vae_greedy | 7.32 | 7.56 | False | -0.05 | 0.06 | 0.01 | 0.16 | 0.55 | False |
| chronos | 8.69 | 6.98 | False | -0.27 | 0.20 | -0.03 | 0.26 | 0.31 | False |
| timestral | 9.14 | 7.98 | False | -1.55 | -0.17 | -0.86 | 0.61 | 0.86 | False |


## Criteria

Mean rank of every method in each criterion (references / splits averaged).

| method | fidelity:dependence | fidelity:distribution | fidelity:long_structure | fidelity:target | fidelity:windows | utility:classification | utility:regression |
|---|---|---|---|---|---|---|---|
| vae_herding | 5.28 | 4.15 | 4.89 | 4.77 | 5.84 | 5.33 | 6.46 |
| diffusion_ts | 6.48 | 5.14 | 7.31 | 7.18 | 6.60 | 6.17 | 5.25 |
| vae_zseries | 6.33 | 6.24 | 6.58 | 3.71 | 6.08 | 6.69 | 6.98 |
| vae_quilting | 8.21 | 7.07 | 6.67 | 5.54 | 6.76 | 5.89 | 7.11 |
| timesfm | 6.94 | 6.75 | 6.33 | 9.98 | 6.83 | 8.23 | 3.89 |
| vae_atsp | 7.23 | 6.79 | 6.90 | 5.52 | 7.19 | 6.89 | 7.82 |
| vae_rand | 6.42 | 7.20 | 6.49 | 7.00 | 7.12 | 6.51 | 8.23 |
| vae_mbb | 6.58 | 7.25 | 6.45 | 7.39 | 6.93 | 6.57 | 8.07 |
| vae_pctsp | 7.11 | 7.11 | 7.39 | 6.16 | 7.01 | 7.02 | 8.19 |
| vae_knn | 7.75 | 7.69 | 7.19 | 7.08 | 7.08 | 6.97 | 8.06 |
| vae_greedy | 8.03 | 7.58 | 7.17 | 6.91 | 6.94 | 7.00 | 8.11 |
| chronos | 6.77 | 9.80 | 9.15 | 8.53 | 9.21 | 7.93 | 6.03 |
| timestral | 7.80 | 8.76 | 8.74 | 12.56 | 7.86 | 10.42 | 5.54 |


## Sensitivity

Columns: `text` — what the variant changes; `first` — the method with the lowest avg_rank in the variant; `tau_vs_main` — Kendall τ between the method order of the variant and of the leaderboard; `main_first_place` — place of the leaderboard's first method in the variant.

| variant | text | first | tau_vs_main | main_first_place |
|---|---|---|---|---|
| main | the leaderboard: core metrics, fidelity against train + val + OOT, noise-aware ranks | vae_herding | 1.00 | 1 |
| plain_ranks | ordinary average ranks (no ties within the noise) | vae_herding | 0.97 | 1 |
| fidelity_train | fidelity against train only | vae_herding | 0.92 | 1 |
| fidelity_holdout | fidelity against val + OOT only | vae_herding | 0.97 | 1 |
| no_unchecked | without F5.7 (seams, no anchor) and F6.1 against val (noise) | vae_herding | 0.95 | 1 |
| all_metrics | every fidelity metric instead of the core set | vae_herding | 0.87 | 1 |
| common_datasets | only the datasets where every method is ranked | vae_herding | 0.82 | 1 |


avg_rank of every method in every variant.

| method | main | plain_ranks | fidelity_train | fidelity_holdout | no_unchecked | all_metrics | common_datasets |
|---|---|---|---|---|---|---|---|
| vae_herding | 5.44 | 5.32 | 4.83 | 5.75 | 5.44 | 5.91 | 5.74 |
| diffusion_ts | 6.13 | 6.05 | 6.09 | 6.14 | 6.13 | 5.98 | 6.32 |
| vae_zseries | 6.31 | 6.26 | 6.07 | 6.44 | 6.30 | 6.55 | 6.14 |
| vae_quilting | 6.68 | 6.60 | 6.82 | 6.60 | 6.67 | 6.65 | 6.38 |
| timesfm | 6.72 | 6.61 | 6.70 | 6.72 | 6.66 | 6.52 | 7.02 |
| vae_atsp | 7.04 | 7.08 | 6.87 | 7.13 | 7.05 | 7.15 | 7.21 |
| vae_rand | 7.11 | 7.17 | 6.97 | 7.18 | 7.12 | 7.19 | 7.30 |
| vae_mbb | 7.12 | 7.17 | 7.01 | 7.18 | 7.12 | 7.18 | 7.29 |
| vae_pctsp | 7.28 | 7.32 | 7.21 | 7.31 | 7.29 | 7.24 | 7.07 |
| vae_knn | 7.44 | 7.54 | 7.56 | 7.37 | 7.44 | 7.41 | 7.40 |
| vae_greedy | 7.44 | 7.52 | 7.53 | 7.40 | 7.45 | 7.45 | 7.30 |
| chronos | 7.84 | 7.83 | 8.27 | 7.62 | 7.82 | 7.39 | 7.49 |
| timestral | 8.56 | 8.58 | 9.26 | 8.21 | 8.57 | 8.34 | 8.33 |


## One method per generator

Kendall τ between the order of the representatives in their field and in the leaderboard: 1.00.

Columns: `method` — method id; `generator` — the generator the method's series come from (pool or long-series generator); `field` — the methods of the field (one per generator); `rank_in_field` — avg_rank of the method in its field; `place_in_field` — place in its field; `field_size` — number of methods in the field; `tier_in_field` — True — not significantly worse than the first method of the field.

| method | generator | field | rank_in_field | place_in_field | field_size | tier_in_field |
|---|---|---|---|---|---|---|
| vae_herding | tsgm_vae | chronos, diffusion_ts, timesfm, timestral, vae_herding | 2.68 | 2 | 5 | True |
| diffusion_ts | diffusion_ts | chronos, diffusion_ts, timesfm, timestral, vae_rand | 2.53 | 1 | 5 | True |
| vae_zseries | tsgm_vae | chronos, diffusion_ts, timesfm, timestral, vae_zseries | 2.80 | 2 | 5 | True |
| vae_quilting | tsgm_vae | chronos, diffusion_ts, timesfm, timestral, vae_quilting | 2.83 | 3 | 5 | True |
| timesfm | timesfm | chronos, diffusion_ts, timesfm, timestral, vae_rand | 2.78 | 2 | 5 | True |
| vae_atsp | tsgm_vae | chronos, diffusion_ts, timesfm, timestral, vae_atsp | 2.90 | 3 | 5 | True |
| vae_rand | tsgm_vae | chronos, diffusion_ts, timesfm, timestral, vae_rand | 2.90 | 3 | 5 | True |
| vae_mbb | tsgm_vae | chronos, diffusion_ts, timesfm, timestral, vae_mbb | 2.90 | 3 | 5 | True |
| vae_pctsp | tsgm_vae | chronos, diffusion_ts, timesfm, timestral, vae_pctsp | 2.92 | 3 | 5 | True |
| vae_knn | tsgm_vae | chronos, diffusion_ts, timesfm, timestral, vae_knn | 2.93 | 3 | 5 | True |
| vae_greedy | tsgm_vae | chronos, diffusion_ts, timesfm, timestral, vae_greedy | 2.92 | 3 | 5 | True |
| chronos | chronos | chronos, diffusion_ts, timesfm, timestral, vae_rand | 3.17 | 4 | 5 | True |
| timestral | timestral | chronos, diffusion_ts, timesfm, timestral, vae_rand | 3.59 | 5 | 5 | False |


## Leave one dataset out

Columns: `method` — method id; `place` — place in the leaderboard (seeds averaged within a dataset, then the mean over datasets); `place_best` — best place with one dataset left out; `place_worst` — worst place with one dataset left out; `n_first` — number of the leave-one-dataset-out rankings in which the method is first; `n_left_out` — number of leave-one-dataset-out rankings (one per dataset).

| method | place | place_best | place_worst | n_first | n_left_out |
|---|---|---|---|---|---|
| vae_herding | 1.00 | 1.00 | 1.00 | 9 | 9 |
| diffusion_ts | 2.00 | 2.00 | 4.00 | 0 | 9 |
| vae_zseries | 3.00 | 2.00 | 4.00 | 0 | 9 |
| vae_quilting | 4.00 | 3.00 | 5.00 | 0 | 9 |
| timesfm | 5.00 | 3.00 | 8.00 | 0 | 9 |
| vae_atsp | 6.00 | 5.00 | 8.00 | 0 | 9 |
| vae_rand | 7.00 | 6.00 | 9.00 | 0 | 9 |
| vae_mbb | 8.00 | 7.00 | 9.00 | 0 | 9 |
| vae_pctsp | 9.00 | 7.00 | 9.00 | 0 | 9 |
| vae_knn | 10.00 | 10.00 | 11.00 | 0 | 9 |
| vae_greedy | 11.00 | 10.00 | 11.00 | 0 | 9 |
| chronos | 12.00 | 12.00 | 12.00 | 0 | 9 |
| timestral | 13.00 | 13.00 | 13.00 | 0 | 9 |


## Random criterion weights

Dirichlet(1) weights within each domain, 2000 draws; median Kendall τ with equal weights: 0.85.

Columns: `method` — method id; `equal_weights_rank` — score of the method with equal criterion weights (lower = better); `p_first` — share of the draws in which the method is first; `p_top3` — share of the draws in which the method is among the three first.

| method | equal_weights_rank | p_first | p_top3 |
|---|---|---|---|
| vae_herding | 5.44 | 0.94 | 1.00 |
| diffusion_ts | 6.13 | 0.00 | 0.89 |
| vae_zseries | 6.31 | 0.00 | 0.65 |
| vae_quilting | 6.68 | 0.00 | 0.13 |
| timesfm | 6.72 | 0.05 | 0.33 |
| vae_atsp | 7.04 | 0.00 | 0.00 |
| vae_rand | 7.11 | 0.00 | 0.00 |
| vae_mbb | 7.12 | 0.00 | 0.00 |
| vae_pctsp | 7.28 | 0.00 | 0.00 |
| vae_knn | 7.44 | 0.00 | 0.00 |
| vae_greedy | 7.44 | 0.00 | 0.00 |
| chronos | 7.84 | 0.00 | 0.00 |
| timestral | 8.56 | 0.00 | 0.00 |

