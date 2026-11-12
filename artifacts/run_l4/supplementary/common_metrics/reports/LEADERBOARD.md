# Method ranking

Methods: 13. Datasets (9): beijing_pm25, bike, bitcoin, electricity, ett, household, jena, metro, pjm. Seeds: 10.

Not ranked (they take part in every research question and in the case study): `vae_zseries_quilt`, `vae_zseries_wsola`, `vae_zseries_xfade` — the seam-processing variants: they exist for some stitchers only (`smooth_paths`), so those would enter the ranking several times and every other stitcher once (`Config.rank_exclude`, `--rank-exclude`; `smooth_paths="all"` runs every seam processing over every stitcher and ranks them).

Left out of the analysis: `chronos` on electricity, beijing_pm25; `timesfm` on beijing_pm25, household, bitcoin — the dataset, or the same object at other stations, years or resolution, is in the method's training corpus, so its results there are not out-of-sample (`Config.leaked`; DATASETS.md).

Procedure. Within every leaf (one fidelity metric against one real reference, or one utility task × model × test split × metric) the methods are ranked per (dataset, seed); rank 1 = the best value. Ranks are averaged leaf → metric group → criterion → domain with equal weights at every level; a ranking is the mean of its domains with equal weights. The rank of a method in a ranking is the mean over datasets (seeds averaged within a dataset). Uncertainty: two-level bootstrap (datasets, then seeds within a dataset), 1000 samples.

## The four rankings

Fidelity criteria in every ranking: distribution (F1, F2, F12), dependence (F3, F4), windows (F6, F9), long structure (F7), target (F8, F11), seams (F5). Not part of any of the four rankings: privacy (F10; its own table below), time and memory (cost tables below), the thematic slices.

- `holdout_clf` — **Fidelity: val + OOT; utility: classification**. Fidelity domain — the criteria distribution (F1, F2, F12), dependence (F3, F4), windows (F6, F9), long structure (F7), target (F8, F11), seams (F5), each against val and OOT (each criterion is the mean of the two). Utility domain — TSTR classification (binary and multiclass tasks), primary metric of each task type, tested on val and OOT. Rank = mean of the two domains with equal weight. Not included: privacy (F10), time, memory.
- `holdout_reg` — **Fidelity: val + OOT; utility: regression**. Fidelity domain — the criteria distribution (F1, F2, F12), dependence (F3, F4), windows (F6, F9), long structure (F7), target (F8, F11), seams (F5), each against val and OOT (each criterion is the mean of the two). Utility domain — TSTR regression (point, quantile, multi-step and volatility tasks), primary metric of each task type, tested on val and OOT. Rank = mean of the two domains with equal weight. Not included: privacy (F10), time, memory.
- `train_clf` — **Fidelity: train; utility: classification**. Fidelity domain — the criteria distribution (F1, F2, F12), dependence (F3, F4), windows (F6, F9), long structure (F7), target (F8, F11), seams (F5), each against train. Utility domain — TSTR classification (binary and multiclass tasks), primary metric of each task type, tested on val and OOT. Rank = mean of the two domains with equal weight. Not included: privacy (F10), time, memory.
- `train_reg` — **Fidelity: train; utility: regression**. Fidelity domain — the criteria distribution (F1, F2, F12), dependence (F3, F4), windows (F6, F9), long structure (F7), target (F8, F11), seams (F5), each against train. Utility domain — TSTR regression (point, quantile, multi-step and volatility tasks), primary metric of each task type, tested on val and OOT. Rank = mean of the two domains with equal weight. Not included: privacy (F10), time, memory.

### Summary of the four rankings

Columns: `method` — method id; `family` — method family: long-series generator, random selection, optimised selection, seam processing (a joiner on a stitcher that also runs without it; joiner in brackets); `first_in` — the rankings in which the method has the lowest avg_rank; `<ranking>:rank` — avg_rank of the method in that ranking (1 = best); `<ranking>:p_first` — share of bootstrap samples in which the method is first in that ranking; `<ranking>:tier` — True — not significantly worse than the first method of that ranking (one-sided Wilcoxon over datasets, Holm, α = 0.05).

Rows: methods ordered by family, then name.

| method | family | holdout_clf:rank | holdout_clf:p_first | holdout_clf:tier | holdout_reg:rank | holdout_reg:p_first | holdout_reg:tier | train_clf:rank | train_clf:p_first | train_clf:tier | train_reg:rank | train_reg:p_first | train_reg:tier | first_in |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| chronos | long-series generator | 7.74 | 0.01 | True | 6.74 | 0.01 | True | 8.09 | 0.00 | True | 7.08 | 0.00 | True |  |
| diffusion_ts | long-series generator | 6.19 | 0.21 | True | 5.75 | 0.20 | True | 6.04 | 0.13 | True | 5.60 | 0.25 | True |  |
| timesfm | long-series generator | 7.57 | 0.01 | True | 5.32 | 0.70 | True | 7.56 | 0.00 | True | 5.31 | 0.56 | True | holdout_reg, train_reg |
| timestral | long-series generator | 9.45 | 0.00 | True | 6.90 | 0.00 | True | 10.07 | 0.00 | False | 7.52 | 0.00 | True |  |
| vae_atsp | optimised selection | 6.95 | 0.00 | True | 7.45 | 0.00 | True | 6.87 | 0.00 | False | 7.37 | 0.00 | True |  |
| vae_greedy | optimised selection | 7.19 | 0.00 | True | 7.76 | 0.00 | True | 7.31 | 0.00 | False | 7.87 | 0.00 | True |  |
| vae_herding | optimised selection | 5.70 | 0.63 | True | 6.30 | 0.03 | True | 5.13 | 0.86 | True | 5.74 | 0.12 | True | holdout_clf, train_clf |
| vae_knn | optimised selection | 7.14 | 0.00 | True | 7.71 | 0.00 | True | 7.29 | 0.00 | False | 7.86 | 0.00 | True |  |
| vae_mbb | optimised selection | 6.90 | 0.00 | True | 7.66 | 0.00 | True | 6.88 | 0.00 | False | 7.64 | 0.00 | True |  |
| vae_pctsp | optimised selection | 6.96 | 0.00 | True | 7.56 | 0.00 | True | 6.97 | 0.00 | False | 7.56 | 0.00 | True |  |
| vae_quilting | optimised selection | 6.22 | 0.12 | True | 6.89 | 0.00 | True | 6.28 | 0.01 | True | 6.95 | 0.00 | True |  |
| vae_zseries | optimised selection | 6.54 | 0.02 | True | 6.66 | 0.06 | True | 6.21 | 0.00 | True | 6.34 | 0.07 | True |  |
| vae_rand | random selection | 6.83 | 0.00 | True | 7.72 | 0.00 | True | 6.80 | 0.00 | False | 7.69 | 0.00 | True |  |


## Ranking 1. Fidelity: val + OOT; utility: classification (`holdout_clf`)

Composition: Fidelity domain — the criteria distribution (F1, F2, F12), dependence (F3, F4), windows (F6, F9), long structure (F7), target (F8, F11), seams (F5), each against val and OOT (each criterion is the mean of the two). Utility domain — TSTR classification (binary and multiclass tasks), primary metric of each task type, tested on val and OOT. Rank = mean of the two domains with equal weight. Not included: privacy (F10), time, memory.

Friedman p = 0.023, Nemenyi CD = 5.03, datasets × methods in the test = 9 × 11.

Columns: `method` — method id; `family` — method family: long-series generator, random selection, optimised selection, seam processing (a joiner on a stitcher that also runs without it; joiner in brackets); `avg_rank` — mean rank over datasets (seeds averaged within a dataset); 1 = best; `ci_lo` — lower bound of the 95% bootstrap interval of avg_rank; `ci_hi` — upper bound of the 95% bootstrap interval of avg_rank; `p_first` — share of bootstrap samples in which the method has the lowest avg_rank; `p_top3` — share of bootstrap samples in which the method is among the three lowest; `p_worse_than_best_holm` — p-value of the one-sided Wilcoxon test over datasets "worse than the first method", Holm correction; empty for the first method; `tier_wilcoxon` — True — not significantly worse than the first method (p_worse_than_best_holm ≥ 0.05).

Rows: sorted by avg_rank.

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| vae_herding | optimised selection | 5.70 | 5.11 | 6.21 | 0.63 | 0.99 |  | True |
| diffusion_ts | long-series generator | 6.19 | 4.69 | 7.54 | 0.21 | 0.61 | 0.66 | True |
| vae_quilting | optimised selection | 6.22 | 5.66 | 6.83 | 0.12 | 0.74 | 0.66 | True |
| vae_zseries | optimised selection | 6.54 | 5.87 | 7.21 | 0.02 | 0.36 | 0.41 | True |
| vae_rand | random selection | 6.83 | 6.04 | 7.61 | 0.00 | 0.10 | 0.26 | True |
| vae_mbb | optimised selection | 6.90 | 6.12 | 7.62 | 0.00 | 0.05 | 0.26 | True |
| vae_atsp | optimised selection | 6.95 | 6.36 | 7.67 | 0.00 | 0.01 | 0.18 | True |
| vae_pctsp | optimised selection | 6.96 | 6.45 | 7.50 | 0.00 | 0.00 | 0.14 | True |
| vae_knn | optimised selection | 7.14 | 6.58 | 7.70 | 0.00 | 0.00 | 0.18 | True |
| vae_greedy | optimised selection | 7.19 | 6.73 | 7.73 | 0.00 | 0.00 | 0.11 | True |
| timesfm | long-series generator | 7.57 | 5.74 | 9.41 | 0.01 | 0.09 | 0.66 | True |
| chronos | long-series generator | 7.74 | 6.10 | 9.18 | 0.01 | 0.05 | 0.44 | True |
| timestral | long-series generator | 9.45 | 8.19 | 10.58 | 0.00 | 0.00 | 0.07 | True |


## Ranking 2. Fidelity: val + OOT; utility: regression (`holdout_reg`)

Composition: Fidelity domain — the criteria distribution (F1, F2, F12), dependence (F3, F4), windows (F6, F9), long structure (F7), target (F8, F11), seams (F5), each against val and OOT (each criterion is the mean of the two). Utility domain — TSTR regression (point, quantile, multi-step and volatility tasks), primary metric of each task type, tested on val and OOT. Rank = mean of the two domains with equal weight. Not included: privacy (F10), time, memory.

Friedman p = 0.106, Nemenyi CD = 5.03, datasets × methods in the test = 9 × 11.

Columns: `method` — method id; `family` — method family: long-series generator, random selection, optimised selection, seam processing (a joiner on a stitcher that also runs without it; joiner in brackets); `avg_rank` — mean rank over datasets (seeds averaged within a dataset); 1 = best; `ci_lo` — lower bound of the 95% bootstrap interval of avg_rank; `ci_hi` — upper bound of the 95% bootstrap interval of avg_rank; `p_first` — share of bootstrap samples in which the method has the lowest avg_rank; `p_top3` — share of bootstrap samples in which the method is among the three lowest; `p_worse_than_best_holm` — p-value of the one-sided Wilcoxon test over datasets "worse than the first method", Holm correction; empty for the first method; `tier_wilcoxon` — True — not significantly worse than the first method (p_worse_than_best_holm ≥ 0.05).

Rows: sorted by avg_rank.

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| timesfm | long-series generator | 5.32 | 3.83 | 7.08 | 0.70 | 0.93 |  | True |
| diffusion_ts | long-series generator | 5.75 | 4.52 | 6.90 | 0.20 | 0.88 | 0.78 | True |
| vae_herding | optimised selection | 6.30 | 5.33 | 7.24 | 0.03 | 0.54 | 0.78 | True |
| vae_zseries | optimised selection | 6.66 | 5.86 | 7.45 | 0.06 | 0.22 | 0.78 | True |
| chronos | long-series generator | 6.74 | 5.35 | 7.93 | 0.01 | 0.23 | 0.78 | True |
| vae_quilting | optimised selection | 6.89 | 6.39 | 7.47 | 0.00 | 0.05 | 0.78 | True |
| timestral | long-series generator | 6.90 | 5.74 | 8.01 | 0.00 | 0.13 | 0.56 | True |
| vae_atsp | optimised selection | 7.45 | 6.87 | 8.13 | 0.00 | 0.00 | 0.78 | True |
| vae_pctsp | optimised selection | 7.56 | 7.09 | 8.05 | 0.00 | 0.00 | 0.78 | True |
| vae_mbb | optimised selection | 7.66 | 6.85 | 8.36 | 0.00 | 0.01 | 0.78 | True |
| vae_knn | optimised selection | 7.71 | 7.08 | 8.30 | 0.00 | 0.00 | 0.78 | True |
| vae_rand | random selection | 7.72 | 6.80 | 8.52 | 0.00 | 0.01 | 0.56 | True |
| vae_greedy | optimised selection | 7.76 | 7.24 | 8.33 | 0.00 | 0.00 | 0.78 | True |


## Ranking 3. Fidelity: train; utility: classification (`train_clf`)

Composition: Fidelity domain — the criteria distribution (F1, F2, F12), dependence (F3, F4), windows (F6, F9), long structure (F7), target (F8, F11), seams (F5), each against train. Utility domain — TSTR classification (binary and multiclass tasks), primary metric of each task type, tested on val and OOT. Rank = mean of the two domains with equal weight. Not included: privacy (F10), time, memory.

Friedman p = 0.002, Nemenyi CD = 5.03, datasets × methods in the test = 9 × 11.

Columns: `method` — method id; `family` — method family: long-series generator, random selection, optimised selection, seam processing (a joiner on a stitcher that also runs without it; joiner in brackets); `avg_rank` — mean rank over datasets (seeds averaged within a dataset); 1 = best; `ci_lo` — lower bound of the 95% bootstrap interval of avg_rank; `ci_hi` — upper bound of the 95% bootstrap interval of avg_rank; `p_first` — share of bootstrap samples in which the method has the lowest avg_rank; `p_top3` — share of bootstrap samples in which the method is among the three lowest; `p_worse_than_best_holm` — p-value of the one-sided Wilcoxon test over datasets "worse than the first method", Holm correction; empty for the first method; `tier_wilcoxon` — True — not significantly worse than the first method (p_worse_than_best_holm ≥ 0.05).

Rows: sorted by avg_rank.

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| vae_herding | optimised selection | 5.13 | 4.67 | 5.59 | 0.86 | 1.00 |  | True |
| diffusion_ts | long-series generator | 6.04 | 4.48 | 7.43 | 0.13 | 0.62 | 0.22 | True |
| vae_zseries | optimised selection | 6.21 | 5.43 | 7.02 | 0.00 | 0.58 | 0.10 | True |
| vae_quilting | optimised selection | 6.28 | 5.53 | 7.01 | 0.01 | 0.56 | 0.11 | True |
| vae_rand | random selection | 6.80 | 6.03 | 7.53 | 0.00 | 0.08 | 0.04 | False |
| vae_atsp | optimised selection | 6.87 | 6.22 | 7.62 | 0.00 | 0.02 | 0.04 | False |
| vae_mbb | optimised selection | 6.88 | 6.09 | 7.58 | 0.00 | 0.03 | 0.04 | False |
| vae_pctsp | optimised selection | 6.97 | 6.33 | 7.60 | 0.00 | 0.00 | 0.04 | False |
| vae_knn | optimised selection | 7.29 | 6.85 | 7.79 | 0.00 | 0.00 | 0.02 | False |
| vae_greedy | optimised selection | 7.31 | 6.83 | 7.81 | 0.00 | 0.00 | 0.02 | False |
| timesfm | long-series generator | 7.56 | 5.82 | 9.44 | 0.00 | 0.09 | 0.22 | True |
| chronos | long-series generator | 8.09 | 6.48 | 9.50 | 0.00 | 0.01 | 0.12 | True |
| timestral | long-series generator | 10.07 | 8.72 | 11.21 | 0.00 | 0.00 | 0.02 | False |


## Ranking 4. Fidelity: train; utility: regression (`train_reg`)

Composition: Fidelity domain — the criteria distribution (F1, F2, F12), dependence (F3, F4), windows (F6, F9), long structure (F7), target (F8, F11), seams (F5), each against train. Utility domain — TSTR regression (point, quantile, multi-step and volatility tasks), primary metric of each task type, tested on val and OOT. Rank = mean of the two domains with equal weight. Not included: privacy (F10), time, memory.

Friedman p = 0.016, Nemenyi CD = 5.03, datasets × methods in the test = 9 × 11.

Columns: `method` — method id; `family` — method family: long-series generator, random selection, optimised selection, seam processing (a joiner on a stitcher that also runs without it; joiner in brackets); `avg_rank` — mean rank over datasets (seeds averaged within a dataset); 1 = best; `ci_lo` — lower bound of the 95% bootstrap interval of avg_rank; `ci_hi` — upper bound of the 95% bootstrap interval of avg_rank; `p_first` — share of bootstrap samples in which the method has the lowest avg_rank; `p_top3` — share of bootstrap samples in which the method is among the three lowest; `p_worse_than_best_holm` — p-value of the one-sided Wilcoxon test over datasets "worse than the first method", Holm correction; empty for the first method; `tier_wilcoxon` — True — not significantly worse than the first method (p_worse_than_best_holm ≥ 0.05).

Rows: sorted by avg_rank.

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| timesfm | long-series generator | 5.31 | 3.89 | 6.85 | 0.56 | 0.90 |  | True |
| diffusion_ts | long-series generator | 5.60 | 4.30 | 6.76 | 0.25 | 0.83 | 0.70 | True |
| vae_herding | optimised selection | 5.74 | 4.99 | 6.51 | 0.12 | 0.90 | 0.70 | True |
| vae_zseries | optimised selection | 6.34 | 5.47 | 7.25 | 0.07 | 0.30 | 0.70 | True |
| vae_quilting | optimised selection | 6.95 | 6.29 | 7.63 | 0.00 | 0.01 | 0.70 | True |
| chronos | long-series generator | 7.08 | 5.77 | 8.24 | 0.00 | 0.05 | 0.70 | True |
| vae_atsp | optimised selection | 7.37 | 6.67 | 8.07 | 0.00 | 0.00 | 0.52 | True |
| timestral | long-series generator | 7.52 | 6.37 | 8.61 | 0.00 | 0.00 | 0.19 | True |
| vae_pctsp | optimised selection | 7.56 | 6.96 | 8.12 | 0.00 | 0.00 | 0.70 | True |
| vae_mbb | optimised selection | 7.64 | 6.88 | 8.29 | 0.00 | 0.00 | 0.70 | True |
| vae_rand | random selection | 7.69 | 6.82 | 8.44 | 0.00 | 0.00 | 0.52 | True |
| vae_knn | optimised selection | 7.86 | 7.38 | 8.35 | 0.00 | 0.00 | 0.70 | True |
| vae_greedy | optimised selection | 7.87 | 7.44 | 8.35 | 0.00 | 0.00 | 0.70 | True |


## Core-metric rankings

The four rankings with the fidelity domain restricted to the core metric set — one or two canonical metrics per criterion, fixed in advance by what they measure: distribution (F1.2_w1, F2.1_ks_d24); dependence (F3.5_log_psd, F4.1_how_mean); windows (F6.1_disc_score, F6.4_mmd); long structure (F7.1_roll_mean_ks, F7.2_roll_std_ks); target (F11.1_class_share_logratio); seams (F5.7_seam_detect_auc_dev). Utility is the same as in the four rankings. The full rankings above use every metric.

Columns: `method` — method id; `family` — method family: long-series generator, random selection, optimised selection, seam processing (a joiner on a stitcher that also runs without it; joiner in brackets); `first_in` — the core rankings in which the method has the lowest avg_rank; `<ranking>:rank` — avg_rank of the method in that core ranking (1 = best); `<ranking>:p_first` — share of bootstrap samples in which the method is first; `<ranking>:tier` — True — not significantly worse than the first method (one-sided Wilcoxon over datasets, Holm, α = 0.05).

Rows: methods ordered by family, then name.

| method | family | core_holdout_clf:rank | core_holdout_clf:p_first | core_holdout_clf:tier | core_holdout_reg:rank | core_holdout_reg:p_first | core_holdout_reg:tier | core_train_clf:rank | core_train_clf:p_first | core_train_clf:tier | core_train_reg:rank | core_train_reg:p_first | core_train_reg:tier | first_in |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| chronos | long-series generator | 8.12 | 0.00 | True | 7.12 | 0.01 | True | 8.76 | 0.00 | False | 7.75 | 0.00 | True |  |
| diffusion_ts | long-series generator | 6.29 | 0.07 | True | 5.85 | 0.18 | True | 6.24 | 0.01 | True | 5.80 | 0.05 | True |  |
| timesfm | long-series generator | 7.76 | 0.00 | True | 5.51 | 0.57 | True | 7.70 | 0.00 | True | 5.44 | 0.25 | True | core_holdout_reg |
| timestral | long-series generator | 9.50 | 0.00 | False | 6.95 | 0.00 | True | 10.56 | 0.00 | False | 8.01 | 0.00 | False |  |
| vae_atsp | optimised selection | 6.93 | 0.00 | True | 7.42 | 0.00 | True | 6.66 | 0.00 | False | 7.15 | 0.00 | False |  |
| vae_greedy | optimised selection | 7.19 | 0.00 | True | 7.76 | 0.00 | True | 7.32 | 0.00 | False | 7.88 | 0.00 | False |  |
| vae_herding | optimised selection | 5.35 | 0.81 | True | 5.95 | 0.13 | True | 4.37 | 0.98 | True | 4.98 | 0.63 | True | core_holdout_clf, core_train_clf, core_train_reg |
| vae_knn | optimised selection | 7.18 | 0.00 | True | 7.75 | 0.00 | True | 7.41 | 0.00 | False | 7.97 | 0.00 | False |  |
| vae_mbb | optimised selection | 6.84 | 0.00 | True | 7.60 | 0.00 | True | 6.70 | 0.00 | False | 7.46 | 0.00 | False |  |
| vae_pctsp | optimised selection | 7.06 | 0.00 | True | 7.65 | 0.00 | True | 6.94 | 0.00 | False | 7.53 | 0.00 | False |  |
| vae_quilting | optimised selection | 6.18 | 0.07 | True | 6.85 | 0.00 | True | 6.42 | 0.00 | True | 7.10 | 0.00 | False |  |
| vae_zseries | optimised selection | 6.32 | 0.04 | True | 6.45 | 0.11 | True | 5.95 | 0.00 | True | 6.07 | 0.07 | True |  |
| vae_rand | random selection | 6.78 | 0.00 | True | 7.67 | 0.00 | True | 6.60 | 0.00 | False | 7.49 | 0.00 | False |  |


### Core metrics. Fidelity: val + OOT; utility: classification (`core_holdout_clf`)

Friedman p = 0.004, Nemenyi CD = 5.03, datasets × methods in the test = 9 × 11. Rows: sorted by avg_rank.

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| vae_herding | optimised selection | 5.35 | 4.60 | 6.04 | 0.81 | 0.99 |  | True |
| vae_quilting | optimised selection | 6.18 | 5.54 | 6.89 | 0.07 | 0.69 | 0.30 | True |
| diffusion_ts | long-series generator | 6.29 | 4.62 | 7.74 | 0.07 | 0.53 | 0.30 | True |
| vae_zseries | optimised selection | 6.32 | 5.54 | 7.15 | 0.04 | 0.52 | 0.30 | True |
| vae_rand | random selection | 6.78 | 5.89 | 7.64 | 0.00 | 0.13 | 0.24 | True |
| vae_mbb | optimised selection | 6.84 | 5.97 | 7.67 | 0.00 | 0.06 | 0.24 | True |
| vae_atsp | optimised selection | 6.93 | 6.37 | 7.61 | 0.00 | 0.00 | 0.14 | True |
| vae_pctsp | optimised selection | 7.06 | 6.47 | 7.63 | 0.00 | 0.00 | 0.06 | True |
| vae_knn | optimised selection | 7.18 | 6.57 | 7.81 | 0.00 | 0.00 | 0.10 | True |
| vae_greedy | optimised selection | 7.19 | 6.68 | 7.80 | 0.00 | 0.00 | 0.10 | True |
| timesfm | long-series generator | 7.76 | 6.10 | 9.54 | 0.00 | 0.05 | 0.12 | True |
| chronos | long-series generator | 8.12 | 6.50 | 9.60 | 0.00 | 0.02 | 0.14 | True |
| timestral | long-series generator | 9.50 | 8.26 | 10.56 | 0.00 | 0.00 | 0.02 | False |


### Core metrics. Fidelity: val + OOT; utility: regression (`core_holdout_reg`)

Friedman p = 0.142, Nemenyi CD = 5.03, datasets × methods in the test = 9 × 11. Rows: sorted by avg_rank.

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| timesfm | long-series generator | 5.51 | 4.12 | 7.19 | 0.57 | 0.90 |  | True |
| diffusion_ts | long-series generator | 5.85 | 4.39 | 7.19 | 0.18 | 0.76 | 0.78 | True |
| vae_herding | optimised selection | 5.95 | 4.82 | 7.08 | 0.13 | 0.75 | 0.78 | True |
| vae_zseries | optimised selection | 6.45 | 5.58 | 7.40 | 0.11 | 0.32 | 0.78 | True |
| vae_quilting | optimised selection | 6.85 | 6.26 | 7.53 | 0.00 | 0.07 | 0.78 | True |
| timestral | long-series generator | 6.95 | 5.81 | 8.05 | 0.00 | 0.09 | 0.56 | True |
| chronos | long-series generator | 7.12 | 5.78 | 8.34 | 0.01 | 0.07 | 0.78 | True |
| vae_atsp | optimised selection | 7.42 | 6.87 | 8.07 | 0.00 | 0.00 | 0.78 | True |
| vae_mbb | optimised selection | 7.60 | 6.67 | 8.39 | 0.00 | 0.01 | 0.56 | True |
| vae_pctsp | optimised selection | 7.65 | 7.08 | 8.17 | 0.00 | 0.00 | 0.78 | True |
| vae_rand | random selection | 7.67 | 6.63 | 8.58 | 0.00 | 0.02 | 0.78 | True |
| vae_knn | optimised selection | 7.75 | 7.08 | 8.37 | 0.00 | 0.00 | 0.78 | True |
| vae_greedy | optimised selection | 7.76 | 7.15 | 8.39 | 0.00 | 0.00 | 0.78 | True |


### Core metrics. Fidelity: train; utility: classification (`core_train_clf`)

Friedman p = 0.000, Nemenyi CD = 5.03, datasets × methods in the test = 9 × 11. Rows: sorted by avg_rank.

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| vae_herding | optimised selection | 4.37 | 3.93 | 4.78 | 0.98 | 1.00 |  | True |
| vae_zseries | optimised selection | 5.95 | 5.05 | 6.89 | 0.00 | 0.76 | 0.06 | True |
| diffusion_ts | long-series generator | 6.24 | 4.47 | 7.81 | 0.01 | 0.50 | 0.06 | True |
| vae_quilting | optimised selection | 6.42 | 5.59 | 7.29 | 0.00 | 0.36 | 0.06 | True |
| vae_rand | random selection | 6.60 | 5.78 | 7.45 | 0.00 | 0.17 | 0.03 | False |
| vae_atsp | optimised selection | 6.66 | 5.92 | 7.44 | 0.00 | 0.12 | 0.02 | False |
| vae_mbb | optimised selection | 6.70 | 5.93 | 7.46 | 0.00 | 0.04 | 0.03 | False |
| vae_pctsp | optimised selection | 6.94 | 6.25 | 7.61 | 0.00 | 0.00 | 0.02 | False |
| vae_greedy | optimised selection | 7.32 | 6.82 | 7.84 | 0.00 | 0.00 | 0.02 | False |
| vae_knn | optimised selection | 7.41 | 6.90 | 7.98 | 0.00 | 0.00 | 0.02 | False |
| timesfm | long-series generator | 7.70 | 6.07 | 9.52 | 0.00 | 0.05 | 0.06 | True |
| chronos | long-series generator | 8.76 | 7.17 | 10.20 | 0.00 | 0.00 | 0.04 | False |
| timestral | long-series generator | 10.56 | 9.21 | 11.62 | 0.00 | 0.00 | 0.02 | False |


### Core metrics. Fidelity: train; utility: regression (`core_train_reg`)

Friedman p = 0.001, Nemenyi CD = 5.03, datasets × methods in the test = 9 × 11. Rows: sorted by avg_rank.

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| vae_herding | optimised selection | 4.98 | 4.22 | 5.69 | 0.63 | 1.00 |  | True |
| timesfm | long-series generator | 5.44 | 4.16 | 6.89 | 0.25 | 0.85 | 0.42 | True |
| diffusion_ts | long-series generator | 5.80 | 4.26 | 7.21 | 0.05 | 0.66 | 0.30 | True |
| vae_zseries | optimised selection | 6.07 | 5.08 | 7.16 | 0.07 | 0.45 | 0.30 | True |
| vae_quilting | optimised selection | 7.10 | 6.35 | 7.85 | 0.00 | 0.01 | 0.04 | False |
| vae_atsp | optimised selection | 7.15 | 6.34 | 7.90 | 0.00 | 0.01 | 0.05 | False |
| vae_mbb | optimised selection | 7.46 | 6.64 | 8.19 | 0.00 | 0.00 | 0.04 | False |
| vae_rand | random selection | 7.49 | 6.46 | 8.43 | 0.00 | 0.01 | 0.04 | False |
| vae_pctsp | optimised selection | 7.53 | 6.91 | 8.12 | 0.00 | 0.00 | 0.02 | False |
| chronos | long-series generator | 7.75 | 6.54 | 8.93 | 0.00 | 0.00 | 0.06 | True |
| vae_greedy | optimised selection | 7.88 | 7.47 | 8.33 | 0.00 | 0.00 | 0.02 | False |
| vae_knn | optimised selection | 7.97 | 7.46 | 8.53 | 0.00 | 0.00 | 0.02 | False |
| timestral | long-series generator | 8.01 | 6.88 | 8.97 | 0.00 | 0.00 | 0.04 | False |


## Normalised scores on the core metrics

Composition: every core metric on the scale random assembly (`noise_pair[0]`) = 0, real data = 1: (x − x_random) / (x_real − x_random); above 1 — closer to the reference than the real data, below 0 — worse than a random assembly. Fidelity against val and train, on the series cut to the length of the real reference (seed 0); utility — TSTR against TRTR, seeds averaged, models fitted on every task. A dataset is left out of a metric when its anchors differ by no more than the noise. Median over the metrics of a criterion within a dataset, then over datasets. Not used in the rankings: the size of the effect next to them. Per metric and dataset — `leaderboard/normalized.parquet`.

Columns: `method` — method id; `family` — method family: long-series generator, random selection, optimised selection, seam processing (a joiner on a stitcher that also runs without it; joiner in brackets); `fidelity` — median normalised score over every core fidelity metric; `utility` — median normalised score over every utility cell; `<criterion>` — median normalised score over the core metrics of the criterion.

Rows: methods ordered by family, then name.

| method | family | fidelity | utility | dependence | distribution | long_structure | target | windows | classification | regression |
|---|---|---|---|---|---|---|---|---|---|---|
| chronos | long-series generator | -0.67 | 0.16 | 0.18 | -0.63 | 0.14 | -0.71 | -0.33 | -0.20 | 0.61 |
| diffusion_ts | long-series generator | 0.55 | 0.30 | 0.02 | 0.98 | 0.60 | -1.06 | -0.24 | 0.11 | 0.41 |
| timesfm | long-series generator | 0.05 | 0.61 | -0.05 | 0.35 | 0.25 | -2.96 | -0.52 | 0.39 | 0.83 |
| timestral | long-series generator | -0.00 | 0.07 | -0.31 | 0.66 | 0.10 | -8.46 | 0.28 | -1.02 | 0.69 |
| vae_atsp | optimised selection | -0.00 | 0.06 | -0.26 | -0.14 | 0.02 | 0.11 | 0.19 | -0.02 | 0.14 |
| vae_greedy | optimised selection | 0.10 | 0.08 | -0.64 | -0.03 | 0.33 | 0.12 | -0.03 | 0.06 | 0.07 |
| vae_herding | optimised selection | 0.61 | 0.15 | 0.04 | 0.63 | 0.43 | 0.35 | 0.35 | 0.13 | 0.21 |
| vae_knn | optimised selection | 0.11 | 0.09 | -0.15 | 0.02 | 0.13 | -0.02 | -0.18 | 0.10 | 0.10 |
| vae_mbb | optimised selection | 0.08 | -0.00 | 0.04 | 0.11 | 0.15 | 0.02 | 0.17 | -0.02 | -0.01 |
| vae_pctsp | optimised selection | 0.08 | 0.10 | -0.36 | -0.10 | 0.00 | -0.40 | 0.00 | 0.13 | 0.08 |
| vae_quilting | optimised selection | 0.24 | 0.19 | -0.32 | 0.36 | 0.01 | 0.10 | 0.16 | 0.07 | 0.22 |
| vae_zseries | optimised selection | 0.07 | 0.10 | -0.22 | -0.20 | 0.01 | 0.53 | 0.10 | 0.04 | 0.14 |
| vae_rand | random selection | 0.00 | -0.00 | -0.00 | 0.00 | -0.00 | -0.00 | -0.00 | 0.00 | -0.00 |


## Anchor check: does a metric tell real data from a random assembly

Composition: per dataset, gap = |real − random assembly| (assembly averaged over seeds) and noise = median over seeds of |random − its twin| (without the twin, as in min: the between-seed spread of the random path); ratio = gap / noise, median over datasets; separated — ratio > 1. The competing methods are not used, so the check does not depend on who wins. Computed on all seeds and separately on even and odd seeds: a flip — the verdict differs between the two halves. Fidelity against val and train; `real` is a piece of OOT, shorter than the synthetic series, so for distance metrics the gap is underestimated (conservative). Every leaf — `leaderboard/anchor_check.parquet`.

Columns: `n` — number of leaves; `separated` — separated on all seeds; `separated_even`, `separated_odd` — on each half; `flips` — leaves whose verdict differs between the halves.

| leaves | n | separated | separated_even | separated_odd | flips |
|---|---|---|---|---|---|
| every fidelity metric | 144 | 139 | 138 | 139 | 3 |
| core fidelity metrics | 18 | 17 | 17 | 18 | 1 |
| utility cells | 58 | 58 | 57 | 58 | 1 |


### Core fidelity metrics

Columns: `leaf` — metric (fidelity: `<metric>@<reference>`, val without suffix; utility: `task|model|metric@split`); `criterion` — the criterion whose two slices are compared; `n_datasets` — number of datasets in which the method is ranked; `ratio_all` — median over datasets of |real − random assembly| / noise (median |random − twin| over seeds, or the between-seed spread of the random path where the twin is not run); all seeds; `separated_all` — True — ratio_all > 1: the metric tells real data from a random assembly beyond the noise; `ratio_even` — ratio on the even seeds; `ratio_odd` — ratio on the odd seeds; `separated_even` — ratio_even > 1; `separated_odd` — ratio_odd > 1; `flip` — True — the verdict differs between even and odd seeds.

| leaf | criterion | n_datasets | ratio_all | separated_all | ratio_even | ratio_odd | separated_even | separated_odd | flip |
|---|---|---|---|---|---|---|---|---|---|
| F1.2_w1 | fidelity:distribution | 9 | 7.14 | True | 8.31 | 4.80 | True | True | False |
| F1.2_w1@train | fidelity:distribution | 9 | 5.77 | True | 9.44 | 4.38 | True | True | False |
| F11.1_class_share_logratio | fidelity:target | 9 | 5.72 | True | 4.38 | 4.76 | True | True | False |
| F11.1_class_share_logratio@train | fidelity:target | 9 | 7.61 | True | 7.46 | 6.65 | True | True | False |
| F2.1_ks_d24 | fidelity:distribution | 9 | 7.24 | True | 2.92 | 5.62 | True | True | False |
| F2.1_ks_d24@train | fidelity:distribution | 9 | 2.88 | True | 1.23 | 1.78 | True | True | False |
| F3.5_log_psd | fidelity:dependence | 9 | 9.27 | True | 8.08 | 4.29 | True | True | False |
| F3.5_log_psd@train | fidelity:dependence | 9 | 9.12 | True | 9.18 | 5.88 | True | True | False |
| F4.1_how_mean | fidelity:dependence | 9 | 9.52 | True | 8.08 | 6.69 | True | True | False |
| F4.1_how_mean@train | fidelity:dependence | 9 | 6.83 | True | 9.31 | 6.66 | True | True | False |
| F6.1_disc_score | fidelity:windows | 9 | 1.00 | False | 0.60 | 1.04 | False | True | True |
| F6.1_disc_score@train | fidelity:windows | 9 | 1.01 | True | 1.00 | 1.69 | True | True | False |
| F6.4_mmd | fidelity:windows | 9 | 5.31 | True | 2.45 | 2.84 | True | True | False |
| F6.4_mmd@train | fidelity:windows | 9 | 7.54 | True | 6.12 | 4.17 | True | True | False |
| F7.1_roll_mean_ks | fidelity:long_structure | 9 | 4.43 | True | 9.06 | 8.96 | True | True | False |
| F7.1_roll_mean_ks@train | fidelity:long_structure | 9 | 5.25 | True | 5.19 | 3.82 | True | True | False |
| F7.2_roll_std_ks | fidelity:long_structure | 9 | 2.13 | True | 2.11 | 2.84 | True | True | False |
| F7.2_roll_std_ks@train | fidelity:long_structure | 9 | 2.42 | True | 2.12 | 2.57 | True | True | False |


## Privacy (F10, memorisation)

Composition: F10.1 DCR — distance from a synthetic window to the nearest train window, relative to the same distance for held-out windows (|log ratio|); F10.2 — share of synthetic windows closer to train than the 5th percentile of real-to-real distances. Computed once, against train. Not part of the four rankings.

Columns: `method` — method id; `avg_rank` — mean rank over datasets (seeds averaged within a dataset); 1 = best; `ci_lo` — lower bound of the 95% bootstrap interval of avg_rank; `ci_hi` — upper bound of the 95% bootstrap interval of avg_rank; `p_first` — share of bootstrap samples in which the method has the lowest avg_rank; `p_top3` — share of bootstrap samples in which the method is among the three lowest; `p_worse_than_best_holm` — p-value of the one-sided Wilcoxon test over datasets "worse than the first method", Holm correction; empty for the first method; `tier_wilcoxon` — True — not significantly worse than the first method (p_worse_than_best_holm ≥ 0.05).

Rows: sorted by avg_rank.

| method | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|
| vae_knn | 5.63 | 4.72 | 6.58 | 0.36 | 0.77 |  | True |
| vae_mbb | 5.64 | 4.11 | 7.23 | 0.31 | 0.73 | 0.74 | True |
| vae_rand | 5.87 | 4.23 | 7.60 | 0.10 | 0.55 | 0.74 | True |
| vae_greedy | 6.13 | 5.29 | 7.01 | 0.02 | 0.28 | 0.09 | True |
| vae_herding | 6.55 | 4.71 | 8.44 | 0.10 | 0.25 | 0.74 | True |
| vae_quilting | 6.93 | 5.53 | 8.41 | 0.02 | 0.12 | 0.62 | True |
| vae_atsp | 6.99 | 6.10 | 8.17 | 0.01 | 0.04 | 0.52 | True |
| diffusion_ts | 7.14 | 5.56 | 8.88 | 0.03 | 0.08 | 0.61 | True |
| chronos | 7.20 | 5.40 | 8.91 | 0.02 | 0.08 | 0.23 | True |
| vae_zseries | 7.23 | 6.37 | 8.12 | 0.00 | 0.02 | 0.52 | True |
| vae_pctsp | 7.39 | 5.95 | 8.97 | 0.02 | 0.07 | 0.62 | True |
| timestral | 9.19 | 7.72 | 10.61 | 0.00 | 0.00 | 0.07 | True |
| timesfm | 10.22 | 7.08 | 12.21 | 0.01 | 0.01 | 0.42 | True |


## Cost next to the rankings

Composition: for each of the four rankings, its quality rank, the same ranking with cost added as a third domain of equal weight (cost: total wall time of a series and peak memory), and the median total time. Times from different hardware are not comparable.

### `holdout_clf` — Fidelity: val + OOT; utility: classification

Columns: `method` — method id; `family` — method family: long-series generator, random selection, optimised selection, seam processing (a joiner on a stitcher that also runs without it; joiner in brackets); `avg_rank` — mean rank over datasets (seeds averaged within a dataset); 1 = best; `rank_with_cost` — avg_rank of the same ranking with cost (total time, peak memory) as a third domain of equal weight; `median_time_s` — median total wall time of one series (training + generation), seconds; `pareto` — True — no other method has both a lower-or-equal avg_rank and a lower-or-equal median_time_s (one of them strictly lower); False otherwise or without timing.

Rows: sorted by median_time_s.

| method | family | avg_rank | rank_with_cost | median_time_s | pareto |
|---|---|---|---|---|---|
| timestral | long-series generator | 9.45 | 7.67 | 6.84 | True |
| timesfm | long-series generator | 7.57 | 6.79 | 21.80 | True |
| chronos | long-series generator | 7.74 | 6.18 | 79.86 | False |
| vae_rand | random selection | 6.83 | 6.05 | 126.91 | True |
| vae_quilting | optimised selection | 6.22 | 6.07 | 126.91 | True |
| vae_greedy | optimised selection | 7.19 | 6.90 | 126.91 | False |
| vae_knn | optimised selection | 7.14 | 7.03 | 126.92 | False |
| vae_mbb | optimised selection | 6.90 | 7.05 | 126.92 | False |
| vae_herding | optimised selection | 5.70 | 6.21 | 126.95 | True |
| vae_zseries | optimised selection | 6.54 | 7.01 | 131.47 | False |
| vae_atsp | optimised selection | 6.95 | 7.95 | 148.01 | False |
| vae_pctsp | optimised selection | 6.96 | 7.80 | 184.42 | False |
| diffusion_ts | long-series generator | 6.19 | 8.06 | 5829.99 | False |


### `holdout_reg` — Fidelity: val + OOT; utility: regression

Columns: `method` — method id; `family` — method family: long-series generator, random selection, optimised selection, seam processing (a joiner on a stitcher that also runs without it; joiner in brackets); `avg_rank` — mean rank over datasets (seeds averaged within a dataset); 1 = best; `rank_with_cost` — avg_rank of the same ranking with cost (total time, peak memory) as a third domain of equal weight; `median_time_s` — median total wall time of one series (training + generation), seconds; `pareto` — True — no other method has both a lower-or-equal avg_rank and a lower-or-equal median_time_s (one of them strictly lower); False otherwise or without timing.

Rows: sorted by median_time_s.

| method | family | avg_rank | rank_with_cost | median_time_s | pareto |
|---|---|---|---|---|---|
| timestral | long-series generator | 6.90 | 5.97 | 6.84 | True |
| timesfm | long-series generator | 5.32 | 5.29 | 21.80 | True |
| chronos | long-series generator | 6.74 | 5.51 | 79.86 | False |
| vae_rand | random selection | 7.72 | 6.64 | 126.91 | False |
| vae_quilting | optimised selection | 6.89 | 6.52 | 126.91 | False |
| vae_greedy | optimised selection | 7.76 | 7.28 | 126.91 | False |
| vae_knn | optimised selection | 7.71 | 7.41 | 126.92 | False |
| vae_mbb | optimised selection | 7.66 | 7.56 | 126.92 | False |
| vae_herding | optimised selection | 6.30 | 6.61 | 126.95 | False |
| vae_zseries | optimised selection | 6.66 | 7.09 | 131.47 | False |
| vae_atsp | optimised selection | 7.45 | 8.28 | 148.01 | False |
| vae_pctsp | optimised selection | 7.56 | 8.19 | 184.42 | False |
| diffusion_ts | long-series generator | 5.75 | 7.77 | 5829.99 | False |


### `train_clf` — Fidelity: train; utility: classification

Columns: `method` — method id; `family` — method family: long-series generator, random selection, optimised selection, seam processing (a joiner on a stitcher that also runs without it; joiner in brackets); `avg_rank` — mean rank over datasets (seeds averaged within a dataset); 1 = best; `rank_with_cost` — avg_rank of the same ranking with cost (total time, peak memory) as a third domain of equal weight; `median_time_s` — median total wall time of one series (training + generation), seconds; `pareto` — True — no other method has both a lower-or-equal avg_rank and a lower-or-equal median_time_s (one of them strictly lower); False otherwise or without timing.

Rows: sorted by median_time_s.

| method | family | avg_rank | rank_with_cost | median_time_s | pareto |
|---|---|---|---|---|---|
| timestral | long-series generator | 10.07 | 8.08 | 6.84 | True |
| timesfm | long-series generator | 7.56 | 6.79 | 21.80 | True |
| chronos | long-series generator | 8.09 | 6.41 | 79.86 | False |
| vae_rand | random selection | 6.80 | 6.02 | 126.91 | True |
| vae_quilting | optimised selection | 6.28 | 6.11 | 126.91 | True |
| vae_greedy | optimised selection | 7.31 | 6.98 | 126.91 | False |
| vae_knn | optimised selection | 7.29 | 7.13 | 126.92 | False |
| vae_mbb | optimised selection | 6.88 | 7.04 | 126.92 | False |
| vae_herding | optimised selection | 5.13 | 5.83 | 126.95 | True |
| vae_zseries | optimised selection | 6.21 | 6.79 | 131.47 | False |
| vae_atsp | optimised selection | 6.87 | 7.90 | 148.01 | False |
| vae_pctsp | optimised selection | 6.97 | 7.80 | 184.42 | False |
| diffusion_ts | long-series generator | 6.04 | 7.96 | 5829.99 | False |


### `train_reg` — Fidelity: train; utility: regression

Columns: `method` — method id; `family` — method family: long-series generator, random selection, optimised selection, seam processing (a joiner on a stitcher that also runs without it; joiner in brackets); `avg_rank` — mean rank over datasets (seeds averaged within a dataset); 1 = best; `rank_with_cost` — avg_rank of the same ranking with cost (total time, peak memory) as a third domain of equal weight; `median_time_s` — median total wall time of one series (training + generation), seconds; `pareto` — True — no other method has both a lower-or-equal avg_rank and a lower-or-equal median_time_s (one of them strictly lower); False otherwise or without timing.

Rows: sorted by median_time_s.

| method | family | avg_rank | rank_with_cost | median_time_s | pareto |
|---|---|---|---|---|---|
| timestral | long-series generator | 7.52 | 6.38 | 6.84 | True |
| timesfm | long-series generator | 5.31 | 5.28 | 21.80 | True |
| chronos | long-series generator | 7.08 | 5.74 | 79.86 | False |
| vae_rand | random selection | 7.69 | 6.62 | 126.91 | False |
| vae_quilting | optimised selection | 6.95 | 6.56 | 126.91 | False |
| vae_greedy | optimised selection | 7.87 | 7.35 | 126.91 | False |
| vae_knn | optimised selection | 7.86 | 7.51 | 126.92 | False |
| vae_mbb | optimised selection | 7.64 | 7.54 | 126.92 | False |
| vae_herding | optimised selection | 5.74 | 6.23 | 126.95 | False |
| vae_zseries | optimised selection | 6.34 | 6.87 | 131.47 | False |
| vae_atsp | optimised selection | 7.37 | 8.23 | 148.01 | False |
| vae_pctsp | optimised selection | 7.56 | 8.19 | 184.42 | False |
| diffusion_ts | long-series generator | 5.60 | 7.67 | 5829.99 | False |


## Ranks by criterion and slice

Composition: the mean rank of every method in one criterion against one reference or on one test split. The four rankings are built from the fidelity columns against train / val / oot and the utility columns; `@—` (privacy) and cost are not part of them.

### Domains

Composition: one domain alone, the mean of its criteria (fidelity without privacy).

Columns: `method` — method id; `fidelity@<ref>` — mean rank over the fidelity criteria against train / val / oot; @all — against all three; `utility@<split>` — mean rank over the utility criteria tested on val / oot; @all — both.

| method | fidelity@train | fidelity@val | fidelity@oot | fidelity@all | utility@val | utility@oot | utility@all |
|---|---|---|---|---|---|---|---|
| chronos | 8.25 | 6.87 | 8.26 | 7.80 | 6.21 | 7.62 | 6.92 |
| diffusion_ts | 6.05 | 5.94 | 6.75 | 6.24 | 5.46 | 5.72 | 5.59 |
| timesfm | 6.93 | 6.64 | 7.25 | 6.94 | 5.90 | 5.99 | 5.94 |
| timestral | 9.57 | 7.65 | 9.01 | 8.74 | 7.72 | 8.33 | 8.03 |
| vae_atsp | 6.82 | 7.23 | 6.74 | 6.93 | 7.54 | 7.29 | 7.42 |
| vae_greedy | 7.53 | 7.40 | 7.22 | 7.38 | 7.59 | 7.70 | 7.65 |
| vae_herding | 5.14 | 6.53 | 6.01 | 5.89 | 6.27 | 5.20 | 5.73 |
| vae_knn | 7.53 | 7.34 | 7.11 | 7.33 | 7.49 | 7.75 | 7.62 |
| vae_mbb | 7.09 | 7.37 | 6.89 | 7.12 | 7.53 | 7.33 | 7.43 |
| vae_pctsp | 6.87 | 7.10 | 6.64 | 6.87 | 7.76 | 7.54 | 7.65 |
| vae_quilting | 6.83 | 6.86 | 6.56 | 6.75 | 6.56 | 6.24 | 6.40 |
| vae_zseries | 5.76 | 6.65 | 6.18 | 6.20 | 6.80 | 6.77 | 6.78 |
| vae_rand | 7.01 | 7.32 | 6.83 | 7.05 | 7.63 | 7.33 | 7.48 |


### Fidelity

Columns: `method` — method id; `<criterion>@<slice>` — mean rank of the method: fidelity criterion against train / val / oot; `@—` — computed once (privacy).

| method | dependence@oot | dependence@train | dependence@val | distribution@oot | distribution@train | distribution@val | long_structure@oot | long_structure@train | long_structure@val | privacy@— | seams@oot | seams@train | seams@val | target@oot | target@train | target@val | windows@oot | windows@train | windows@val |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| chronos | 8.08 | 8.17 | 6.72 | 9.42 | 9.63 | 7.88 | 9.18 | 9.38 | 7.81 | 7.20 | 5.76 | 4.90 | 5.60 | 7.82 | 8.27 | 7.19 | 9.32 | 9.17 | 6.04 |
| diffusion_ts | 7.49 | 7.47 | 7.37 | 6.84 | 5.90 | 6.01 | 7.25 | 6.69 | 6.58 | 7.14 | 6.79 | 4.99 | 4.55 | 6.11 | 5.93 | 5.48 | 6.01 | 5.29 | 5.62 |
| timesfm | 6.05 | 4.98 | 5.63 | 7.17 | 6.62 | 6.72 | 6.75 | 6.96 | 6.92 | 10.22 | 7.26 | 8.16 | 7.80 | 8.00 | 7.99 | 8.19 | 8.27 | 6.90 | 4.59 |
| timestral | 6.92 | 7.70 | 5.92 | 9.20 | 10.06 | 7.86 | 9.07 | 9.86 | 8.53 | 9.19 | 9.32 | 9.31 | 7.55 | 9.47 | 9.83 | 8.90 | 10.10 | 10.65 | 7.14 |
| vae_atsp | 6.71 | 6.54 | 6.85 | 6.68 | 6.86 | 7.16 | 6.57 | 6.61 | 6.93 | 6.99 | 7.08 | 7.63 | 7.83 | 6.71 | 6.58 | 6.67 | 6.68 | 6.70 | 7.91 |
| vae_greedy | 7.44 | 7.72 | 7.48 | 6.95 | 7.43 | 7.14 | 7.13 | 7.28 | 6.99 | 6.13 | 7.34 | 7.67 | 7.84 | 7.60 | 7.69 | 7.71 | 6.85 | 7.39 | 7.22 |
| vae_herding | 6.64 | 5.78 | 7.64 | 5.76 | 4.59 | 6.64 | 5.67 | 4.81 | 6.71 | 6.55 | 6.98 | 5.13 | 5.75 | 5.30 | 5.17 | 5.25 | 5.71 | 5.33 | 7.19 |
| vae_knn | 7.31 | 7.61 | 7.18 | 6.99 | 7.39 | 7.04 | 7.11 | 7.32 | 6.80 | 5.63 | 6.62 | 7.86 | 7.97 | 7.67 | 7.73 | 7.84 | 6.96 | 7.28 | 7.20 |
| vae_mbb | 7.27 | 7.64 | 7.53 | 6.67 | 6.59 | 6.97 | 6.62 | 6.42 | 6.52 | 5.64 | 6.68 | 7.62 | 7.91 | 7.48 | 7.36 | 7.99 | 6.62 | 6.91 | 7.33 |
| vae_pctsp | 6.84 | 6.59 | 7.15 | 6.68 | 7.04 | 7.23 | 6.89 | 7.48 | 7.25 | 7.39 | 6.14 | 6.48 | 6.43 | 6.75 | 7.01 | 6.50 | 6.55 | 6.65 | 8.06 |
| vae_quilting | 6.47 | 7.09 | 6.92 | 6.50 | 7.07 | 7.06 | 6.64 | 6.73 | 6.59 | 6.93 | 7.17 | 6.93 | 6.99 | 6.19 | 6.40 | 6.56 | 6.42 | 6.79 | 7.02 |
| vae_zseries | 6.32 | 5.67 | 6.66 | 6.20 | 5.71 | 6.51 | 6.28 | 5.89 | 6.90 | 7.23 | 7.07 | 7.00 | 7.35 | 5.51 | 5.01 | 5.36 | 5.68 | 5.30 | 7.12 |
| vae_rand | 7.38 | 7.64 | 7.43 | 6.54 | 6.56 | 6.88 | 6.47 | 6.36 | 6.83 | 5.87 | 6.59 | 7.24 | 7.37 | 7.20 | 7.18 | 7.88 | 6.78 | 7.07 | 7.56 |


### Utility

Columns: `method` — method id; `<criterion>@<slice>` — mean rank of the method: TSTR utility criterion (classification, regression) tested on val / oot.

| method | classification@oot | classification@val | regression@oot | regression@val |
|---|---|---|---|---|
| chronos | 8.13 | 7.71 | 7.11 | 4.72 |
| diffusion_ts | 6.34 | 5.72 | 5.10 | 5.21 |
| timesfm | 8.35 | 8.04 | 3.63 | 3.76 |
| timestral | 10.39 | 10.77 | 6.27 | 4.68 |
| vae_atsp | 6.92 | 6.92 | 7.66 | 8.16 |
| vae_greedy | 7.11 | 7.05 | 8.29 | 8.13 |
| vae_herding | 4.82 | 5.44 | 5.59 | 7.09 |
| vae_knn | 7.15 | 6.95 | 8.34 | 8.03 |
| vae_mbb | 6.67 | 6.67 | 7.98 | 8.39 |
| vae_pctsp | 6.99 | 7.12 | 8.08 | 8.39 |
| vae_quilting | 5.56 | 5.89 | 6.93 | 7.23 |
| vae_zseries | 6.77 | 6.55 | 6.77 | 7.05 |
| vae_rand | 6.50 | 6.68 | 8.15 | 8.58 |


### Cost

Columns: `method` — method id; `<criterion>@<slice>` — mean rank of the method: cost slice: total — total wall time of a series, training — training of the generator (a shared generator is charged to every method and seed using it), generation — sampling + assembly of a new series, memory — peak GPU memory and RSS increase; lower = better rank.

| method | cost@generation | cost@memory | cost@total | cost@training |
|---|---|---|---|---|
| chronos | 11.97 | 3.37 | 2.74 | 2.03 |
| diffusion_ts | 13.00 | 10.62 | 13.00 | 13.00 |
| timesfm | 8.11 | 8.44 | 2.02 | 2.85 |
| timestral | 7.32 | 7.22 | 1.00 | 1.00 |
| vae_atsp | 10.12 | 9.00 | 10.92 | 7.74 |
| vae_greedy | 3.12 | 6.98 | 5.64 | 7.74 |
| vae_herding | 6.26 | 5.67 | 8.79 | 7.74 |
| vae_knn | 4.14 | 6.96 | 6.66 | 7.74 |
| vae_mbb | 5.21 | 6.98 | 7.74 | 7.74 |
| vae_pctsp | 11.13 | 7.00 | 11.93 | 7.74 |
| vae_quilting | 2.06 | 6.96 | 4.59 | 7.74 |
| vae_zseries | 9.04 | 6.05 | 9.84 | 7.74 |
| vae_rand | 1.00 | 5.42 | 3.53 | 7.74 |


### Theme: Class balance

Composition. Fidelity: F8.1 and F11 (class shares of every classification task, rare events separately, multiclass, loss of the minority class). Utility: ECE of the classifiers. Not part of the rankings.

Columns: `method` — method id; `fidelity@<ref>` — mean rank over the theme's fidelity metrics against that reference; `utility@<split>` — mean rank over the theme's utility metrics on that test split.

| method | fidelity@oot | fidelity@train | fidelity@val | utility@oot | utility@val |
|---|---|---|---|---|---|
| chronos | 8.02 | 8.16 | 7.54 | 7.27 | 6.59 |
| diffusion_ts | 6.97 | 6.63 | 6.05 | 5.99 | 5.70 |
| timesfm | 8.65 | 8.27 | 9.15 | 7.13 | 7.02 |
| timestral | 10.45 | 10.61 | 10.04 | 9.40 | 9.23 |
| vae_atsp | 6.18 | 5.93 | 6.06 | 6.83 | 6.97 |
| vae_greedy | 7.24 | 7.41 | 7.35 | 7.38 | 7.07 |
| vae_herding | 5.38 | 5.17 | 5.22 | 5.67 | 6.41 |
| vae_knn | 7.48 | 7.65 | 7.68 | 7.37 | 7.07 |
| vae_mbb | 7.07 | 7.23 | 7.84 | 7.28 | 7.24 |
| vae_pctsp | 6.50 | 6.83 | 6.11 | 7.00 | 6.93 |
| vae_quilting | 5.94 | 6.26 | 6.44 | 6.43 | 6.92 |
| vae_zseries | 5.01 | 4.41 | 4.59 | 6.03 | 6.42 |
| vae_rand | 6.90 | 7.13 | 7.77 | 7.31 | 7.35 |


### Theme: Outliers and extremes

Composition. Fidelity: tail quantiles and the Hill index (F1.5, F1.10), kurtosis (F1.6), large jumps (F2.4), excursion durations (F7.4), F12 (frequency and size of exceedances of the real 0.5/99.5%, local spikes, block maxima and minima). Utility: regression error on the extreme 10% of the target and PR AUC of rare events. Not part of the rankings.

Columns: `method` — method id; `fidelity@<ref>` — mean rank over the theme's fidelity metrics against that reference; `utility@<split>` — mean rank over the theme's utility metrics on that test split.

| method | fidelity@oot | fidelity@train | fidelity@val | utility@oot | utility@val |
|---|---|---|---|---|---|
| chronos | 9.13 | 9.12 | 7.61 | 7.24 | 6.53 |
| diffusion_ts | 7.55 | 6.27 | 6.60 | 5.85 | 5.07 |
| timesfm | 7.96 | 6.67 | 7.28 | 4.77 | 4.96 |
| timestral | 9.22 | 9.72 | 7.88 | 7.42 | 6.94 |
| vae_atsp | 6.62 | 7.22 | 7.28 | 7.03 | 7.26 |
| vae_greedy | 6.77 | 7.41 | 7.03 | 7.25 | 7.45 |
| vae_herding | 5.79 | 4.68 | 6.63 | 6.86 | 7.31 |
| vae_knn | 6.63 | 7.16 | 6.83 | 7.62 | 7.62 |
| vae_mbb | 6.00 | 6.10 | 6.39 | 8.13 | 8.09 |
| vae_pctsp | 6.98 | 7.45 | 7.45 | 6.85 | 7.12 |
| vae_quilting | 6.86 | 7.47 | 7.43 | 6.46 | 6.88 |
| vae_zseries | 6.68 | 6.12 | 6.58 | 6.88 | 6.87 |
| vae_rand | 5.75 | 6.06 | 6.37 | 7.96 | 8.12 |


### Tests by column

Columns: `column` — the ranked column (ranking, domain, criterion@slice); `p_friedman` — p-value of the Friedman test (blocks = datasets); `nemenyi_cd` — Nemenyi critical difference of Friedman ranks; `n_blocks` — number of datasets in the Friedman test (complete blocks; a method missing on a dataset is left out of the test, or the dataset is — whichever keeps more cells); `n_methods_friedman` — number of methods in the Friedman test; `best` — method with the lowest avg_rank in the column.

| column | p_friedman | nemenyi_cd | n_blocks | n_methods_friedman | best |
|---|---|---|---|---|---|
| ranking:holdout_clf | 0.023 | 5.032 | 9 | 11 | vae_herding |
| with_cost:holdout_clf | 0.000 | 5.032 | 9 | 11 | vae_rand |
| ranking:holdout_reg | 0.106 | 5.032 | 9 | 11 | timesfm |
| with_cost:holdout_reg | 0.000 | 5.032 | 9 | 11 | timesfm |
| ranking:train_clf | 0.002 | 5.032 | 9 | 11 | vae_herding |
| with_cost:train_clf | 0.000 | 5.032 | 9 | 11 | vae_herding |
| ranking:train_reg | 0.016 | 5.032 | 9 | 11 | timesfm |
| with_cost:train_reg | 0.000 | 5.032 | 9 | 11 | timesfm |
| ranking:core_holdout_clf | 0.004 | 5.032 | 9 | 11 | vae_herding |
| ranking:core_holdout_reg | 0.142 | 5.032 | 9 | 11 | timesfm |
| ranking:core_train_clf | 0.000 | 5.032 | 9 | 11 | vae_herding |
| ranking:core_train_reg | 0.001 | 5.032 | 9 | 11 | vae_herding |
| domain:fidelity@train | 0.000 | 5.032 | 9 | 11 | vae_herding |
| domain:fidelity@val | 0.121 | 5.032 | 9 | 11 | diffusion_ts |
| domain:fidelity@oot | 0.063 | 5.032 | 9 | 11 | vae_herding |
| domain:fidelity@all | 0.006 | 5.032 | 9 | 11 | vae_herding |
| domain:utility@val | 0.091 | 5.032 | 9 | 11 | diffusion_ts |
| domain:utility@oot | 0.207 | 5.032 | 9 | 11 | vae_herding |
| domain:utility@all | 0.154 | 5.032 | 9 | 11 | diffusion_ts |
| cost@generation | 0.000 | 5.032 | 9 | 11 | vae_rand |
| cost@memory | 0.000 | 5.032 | 9 | 11 | chronos |
| cost@total | 0.000 | 5.032 | 9 | 11 | timestral |
| cost@training | 0.000 | 5.032 | 9 | 11 | timestral |
| fidelity:dependence@oot | 0.875 | 5.032 | 9 | 11 | timesfm |
| fidelity:dependence@train | 0.027 | 5.032 | 9 | 11 | timesfm |
| fidelity:dependence@val | 0.948 | 5.032 | 9 | 11 | timesfm |
| fidelity:distribution@oot | 0.004 | 5.032 | 9 | 11 | vae_herding |
| fidelity:distribution@train | 0.000 | 5.032 | 9 | 11 | vae_herding |
| fidelity:distribution@val | 0.486 | 5.032 | 9 | 11 | diffusion_ts |
| fidelity:long_structure@oot | 0.008 | 5.032 | 9 | 11 | vae_herding |
| fidelity:long_structure@train | 0.000 | 5.032 | 9 | 11 | vae_herding |
| fidelity:long_structure@val | 0.205 | 5.032 | 9 | 11 | vae_mbb |
| fidelity:privacy@— | 0.430 | 5.032 | 9 | 11 | vae_knn |
| fidelity:seams@oot | 0.922 | 5.032 | 9 | 11 | chronos |
| fidelity:seams@train | 0.355 | 5.032 | 9 | 11 | chronos |
| fidelity:seams@val | 0.640 | 5.032 | 9 | 11 | diffusion_ts |
| fidelity:target@oot | 0.010 | 5.032 | 9 | 11 | vae_herding |
| fidelity:target@train | 0.001 | 5.032 | 9 | 11 | vae_zseries |
| fidelity:target@val | 0.001 | 5.032 | 9 | 11 | vae_herding |
| fidelity:windows@oot | 0.009 | 5.032 | 9 | 11 | vae_zseries |
| fidelity:windows@train | 0.000 | 5.032 | 9 | 11 | diffusion_ts |
| fidelity:windows@val | 0.263 | 5.032 | 9 | 11 | timesfm |
| utility:classification@oot | 0.007 | 5.032 | 9 | 11 | vae_herding |
| utility:classification@val | 0.007 | 5.032 | 9 | 11 | vae_herding |
| utility:regression@oot | 0.086 | 5.032 | 9 | 11 | timesfm |
| utility:regression@val | 0.001 | 5.032 | 9 | 11 | timesfm |
| theme:class_balance:fidelity@oot | 0.019 | 5.032 | 9 | 11 | vae_zseries |
| theme:class_balance:fidelity@train | 0.000 | 5.032 | 9 | 11 | vae_zseries |
| theme:class_balance:fidelity@val | 0.000 | 5.032 | 9 | 11 | vae_zseries |
| theme:class_balance:utility@oot | 0.079 | 5.032 | 9 | 11 | vae_herding |
| theme:class_balance:utility@val | 0.272 | 5.032 | 9 | 11 | diffusion_ts |
| theme:extremes:fidelity@oot | 0.028 | 5.032 | 9 | 11 | vae_rand |
| theme:extremes:fidelity@train | 0.000 | 5.032 | 9 | 11 | vae_herding |
| theme:extremes:fidelity@val | 0.645 | 5.032 | 9 | 11 | vae_rand |
| theme:extremes:utility@oot | 0.297 | 5.032 | 9 | 11 | timesfm |
| theme:extremes:utility@val | 0.063 | 5.032 | 9 | 11 | timesfm |


## Effect size: median transfer ratio

Columns: `method` — method id; `<criterion>@<split>` — median over datasets, seeds, tasks and models of TSTR / TRTR (quality of a model trained on synthetic data / trained on real data, both tested on real data); 1 = as on real data.

| method | utility:classification@oot | utility:classification@val | utility:regression@oot | utility:regression@val |
|---|---|---|---|---|
| chronos | 0.45 | 0.57 | 0.73 | 0.86 |
| diffusion_ts | 0.77 | 0.80 | 0.81 | 0.80 |
| timesfm | 0.70 | 0.74 | 0.87 | 0.91 |
| timestral | 0.00 | 0.00 | 0.76 | 0.84 |
| vae_atsp | 0.68 | 0.67 | 0.67 | 0.59 |
| vae_greedy | 0.67 | 0.67 | 0.65 | 0.59 |
| vae_herding | 0.74 | 0.72 | 0.71 | 0.56 |
| vae_knn | 0.67 | 0.66 | 0.63 | 0.58 |
| vae_mbb | 0.68 | 0.68 | 0.63 | 0.55 |
| vae_pctsp | 0.69 | 0.64 | 0.66 | 0.57 |
| vae_quilting | 0.74 | 0.68 | 0.66 | 0.59 |
| vae_zseries | 0.67 | 0.65 | 0.70 | 0.62 |
| vae_rand | 0.70 | 0.69 | 0.61 | 0.55 |


## Ranking stability (Kendall τ between the rankings of slices)

Columns: `comparison` — pair of slice types compared (e.g. train ↔ val); `count` — number of compared pairs of rankings; `mean` — mean Kendall τ (1 — the same order, 0 — unrelated, −1 — reversed); `min` — lowest Kendall τ; `max` — highest Kendall τ.

| comparison | count | mean | min | max |
|---|---|---|---|---|
| fidelity ↔ utility | 24.00 | 0.24 | -0.46 | 0.74 |
| linear ↔ gbdt | 4.00 | 0.61 | 0.46 | 0.74 |
| train ↔ oot | 8.00 | 0.72 | 0.49 | 0.95 |
| train ↔ val | 8.00 | 0.54 | 0.00 | 0.77 |
| val ↔ oot | 12.00 | 0.50 | -0.10 | 0.82 |


Columns: `method` — method id; `comparison` — the two kinds of slices compared; `criterion` — the criterion whose two slices are compared; `tau` — Kendall τ between the method orders of the two slices.

| comparison | criterion | tau |
|---|---|---|
| train ↔ val | fidelity:dependence | 0.23 |
| val ↔ oot | fidelity:dependence | 0.28 |
| train ↔ oot | fidelity:dependence | 0.69 |
| train ↔ val | fidelity:distribution | 0.67 |
| val ↔ oot | fidelity:distribution | 0.41 |
| train ↔ oot | fidelity:distribution | 0.59 |
| train ↔ val | fidelity:long_structure | 0.54 |
| val ↔ oot | fidelity:long_structure | 0.33 |
| train ↔ oot | fidelity:long_structure | 0.74 |
| train ↔ val | fidelity:seams | 0.69 |
| val ↔ oot | fidelity:seams | 0.23 |
| train ↔ oot | fidelity:seams | 0.49 |
| train ↔ val | fidelity:target | 0.69 |
| val ↔ oot | fidelity:target | 0.74 |
| train ↔ oot | fidelity:target | 0.95 |
| train ↔ val | fidelity:windows | 0.00 |
| val ↔ oot | fidelity:windows | -0.10 |
| train ↔ oot | fidelity:windows | 0.74 |
| train ↔ val | theme:class_balance:fidelity | 0.74 |
| val ↔ oot | theme:class_balance:fidelity | 0.67 |
| train ↔ oot | theme:class_balance:fidelity | 0.92 |
| val ↔ oot | theme:class_balance:utility | 0.74 |
| train ↔ val | theme:extremes:fidelity | 0.77 |
| val ↔ oot | theme:extremes:fidelity | 0.64 |
| train ↔ oot | theme:extremes:fidelity | 0.62 |
| val ↔ oot | theme:extremes:utility | 0.64 |
| val ↔ oot | utility:classification | 0.82 |
| val ↔ oot | utility:regression | 0.59 |
| linear ↔ gbdt | utility:classification@oot | 0.74 |
| linear ↔ gbdt | utility:classification@val | 0.51 |
| linear ↔ gbdt | utility:regression@oot | 0.46 |
| linear ↔ gbdt | utility:regression@val | 0.72 |


## Sensitivity to the criterion weights: `holdout_clf`

Composition: the ranking `holdout_clf` under 2000 random criterion weights (Dirichlet(1) within each domain). Median Kendall τ with equal weighting: 0.97.

Columns: `method` — method id; `equal_weights_rank` — score of the method with equal criterion weights (lower = better); `p_first` — share of the weight draws in which the method is first; `p_top3` — share of the weight draws in which the method is among the three first.

| method | equal_weights_rank | p_first | p_top3 |
|---|---|---|---|
| vae_herding | 5.70 | 1.00 | 1.00 |
| diffusion_ts | 6.19 | 0.00 | 1.00 |
| vae_quilting | 6.22 | 0.00 | 1.00 |
| vae_zseries | 6.54 | 0.00 | 0.00 |
| vae_rand | 6.83 | 0.00 | 0.00 |
| vae_mbb | 6.90 | 0.00 | 0.00 |
| vae_atsp | 6.95 | 0.00 | 0.00 |
| vae_pctsp | 6.96 | 0.00 | 0.00 |
| vae_knn | 7.14 | 0.00 | 0.00 |
| vae_greedy | 7.19 | 0.00 | 0.00 |
| timesfm | 7.57 | 0.00 | 0.00 |
| chronos | 7.74 | 0.00 | 0.00 |
| timestral | 9.45 | 0.00 | 0.00 |


## Sensitivity to the criterion weights: `holdout_reg`

Composition: the ranking `holdout_reg` under 2000 random criterion weights (Dirichlet(1) within each domain). Median Kendall τ with equal weighting: 0.95.

Columns: `method` — method id; `equal_weights_rank` — score of the method with equal criterion weights (lower = better); `p_first` — share of the weight draws in which the method is first; `p_top3` — share of the weight draws in which the method is among the three first.

| method | equal_weights_rank | p_first | p_top3 |
|---|---|---|---|
| timesfm | 5.32 | 0.97 | 1.00 |
| diffusion_ts | 5.75 | 0.03 | 1.00 |
| vae_herding | 6.30 | 0.00 | 0.93 |
| vae_zseries | 6.66 | 0.00 | 0.00 |
| chronos | 6.74 | 0.00 | 0.04 |
| vae_quilting | 6.89 | 0.00 | 0.00 |
| timestral | 6.90 | 0.00 | 0.03 |
| vae_atsp | 7.45 | 0.00 | 0.00 |
| vae_pctsp | 7.56 | 0.00 | 0.00 |
| vae_mbb | 7.66 | 0.00 | 0.00 |
| vae_knn | 7.71 | 0.00 | 0.00 |
| vae_rand | 7.72 | 0.00 | 0.00 |
| vae_greedy | 7.76 | 0.00 | 0.00 |


## Sensitivity to the criterion weights: `train_clf`

Composition: the ranking `train_clf` under 2000 random criterion weights (Dirichlet(1) within each domain). Median Kendall τ with equal weighting: 0.95.

Columns: `method` — method id; `equal_weights_rank` — score of the method with equal criterion weights (lower = better); `p_first` — share of the weight draws in which the method is first; `p_top3` — share of the weight draws in which the method is among the three first.

| method | equal_weights_rank | p_first | p_top3 |
|---|---|---|---|
| vae_herding | 5.13 | 1.00 | 1.00 |
| diffusion_ts | 6.04 | 0.00 | 0.95 |
| vae_zseries | 6.21 | 0.00 | 0.74 |
| vae_quilting | 6.28 | 0.00 | 0.31 |
| vae_rand | 6.80 | 0.00 | 0.00 |
| vae_atsp | 6.87 | 0.00 | 0.00 |
| vae_mbb | 6.88 | 0.00 | 0.00 |
| vae_pctsp | 6.97 | 0.00 | 0.00 |
| vae_knn | 7.29 | 0.00 | 0.00 |
| vae_greedy | 7.31 | 0.00 | 0.00 |
| timesfm | 7.56 | 0.00 | 0.00 |
| chronos | 8.09 | 0.00 | 0.00 |
| timestral | 10.07 | 0.00 | 0.00 |


## Sensitivity to the criterion weights: `train_reg`

Composition: the ranking `train_reg` under 2000 random criterion weights (Dirichlet(1) within each domain). Median Kendall τ with equal weighting: 0.92.

Columns: `method` — method id; `equal_weights_rank` — score of the method with equal criterion weights (lower = better); `p_first` — share of the weight draws in which the method is first; `p_top3` — share of the weight draws in which the method is among the three first.

| method | equal_weights_rank | p_first | p_top3 |
|---|---|---|---|
| timesfm | 5.31 | 0.81 | 1.00 |
| diffusion_ts | 5.60 | 0.19 | 1.00 |
| vae_herding | 5.74 | 0.00 | 1.00 |
| vae_zseries | 6.34 | 0.00 | 0.00 |
| vae_quilting | 6.95 | 0.00 | 0.00 |
| chronos | 7.08 | 0.00 | 0.00 |
| vae_atsp | 7.37 | 0.00 | 0.00 |
| timestral | 7.52 | 0.00 | 0.00 |
| vae_pctsp | 7.56 | 0.00 | 0.00 |
| vae_mbb | 7.64 | 0.00 | 0.00 |
| vae_rand | 7.69 | 0.00 | 0.00 |
| vae_knn | 7.86 | 0.00 | 0.00 |
| vae_greedy | 7.87 | 0.00 | 0.00 |


## Details

Tables in `leaderboard/`: ranks by metric group and task — `by_group.parquet`, by every leaf — `leaves.parquet`, full summaries by column with CI — `by_column.parquet` (`ranking:<name>` — the four rankings, `with_cost:<name>` — with cost, `domain:<name>`, criteria), the rankings — `rankings.parquet`, their summary — `rankings_summary.parquet`, cost next to them — `rankings_cost.parquet`; core-metric rankings — `rankings_core.parquet`, `rankings_core_summary.parquet`; normalised scores — `normalized.parquet`, `normalized_summary.parquet`; anchor check — `anchor_check.parquet`.
