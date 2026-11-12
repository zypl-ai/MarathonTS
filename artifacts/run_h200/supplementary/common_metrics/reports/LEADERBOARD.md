# Method ranking

Methods: 24. Datasets (9): beijing_pm25, bike, bitcoin, electricity, ett, household, jena, metro, pjm. Seeds: 10.

Not ranked (they take part in every research question and in the case study): `vae_zseries_quilt`, `vae_zseries_wsola`, `vae_zseries_xfade`, `zedge_zseries_quilt`, `zedge_zseries_wsola`, `zedge_zseries_xfade` — the seam-processing variants: they exist for some stitchers only (`smooth_paths`), so those would enter the ranking several times and every other stitcher once (`Config.rank_exclude`, `--rank-exclude`; `smooth_paths="all"` runs every seam processing over every stitcher and ranks them).

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
| chronos | long-series generator | 16.36 | 0.00 | True | 13.94 | 0.00 | True | 17.56 | 0.00 | True | 15.14 | 0.00 | True |  |
| diffusion_ts | long-series generator | 13.75 | 0.00 | False | 12.22 | 0.00 | True | 14.54 | 0.00 | False | 13.01 | 0.00 | True |  |
| timesfm | long-series generator | 15.70 | 0.00 | True | 11.39 | 0.01 | True | 16.77 | 0.00 | True | 12.46 | 0.00 | True |  |
| timestral | long-series generator | 18.53 | 0.00 | False | 13.76 | 0.00 | True | 20.17 | 0.00 | False | 15.41 | 0.00 | True |  |
| zedge_ts_ar | long-series generator | 9.04 | 0.23 | True | 8.82 | 0.40 | True | 7.93 | 0.34 | True | 7.71 | 0.51 | True | train_reg |
| zedge_ts_long | long-series generator | 10.05 | 0.00 | True | 9.94 | 0.00 | True | 9.24 | 0.00 | True | 9.13 | 0.00 | True |  |
| vae_atsp | optimised selection | 14.81 | 0.00 | True | 15.22 | 0.00 | True | 15.53 | 0.00 | False | 15.94 | 0.00 | True |  |
| vae_greedy | optimised selection | 15.15 | 0.00 | True | 15.49 | 0.00 | True | 15.87 | 0.00 | True | 16.20 | 0.00 | True |  |
| vae_herding | optimised selection | 13.60 | 0.00 | False | 14.23 | 0.00 | False | 13.78 | 0.00 | False | 14.41 | 0.00 | False |  |
| vae_knn | optimised selection | 15.40 | 0.00 | True | 15.96 | 0.00 | True | 16.27 | 0.00 | False | 16.82 | 0.00 | True |  |
| vae_mbb | optimised selection | 15.59 | 0.00 | False | 16.50 | 0.00 | True | 16.46 | 0.00 | False | 17.37 | 0.00 | True |  |
| vae_pctsp | optimised selection | 14.85 | 0.00 | True | 15.40 | 0.00 | False | 15.69 | 0.00 | False | 16.24 | 0.00 | True |  |
| vae_quilting | optimised selection | 14.37 | 0.00 | True | 14.94 | 0.00 | True | 14.97 | 0.00 | True | 15.53 | 0.00 | True |  |
| vae_zseries | optimised selection | 13.47 | 0.00 | True | 13.53 | 0.00 | True | 13.93 | 0.00 | True | 13.99 | 0.00 | True |  |
| zedge_atsp | optimised selection | 9.37 | 0.00 | True | 9.77 | 0.00 | True | 8.40 | 0.00 | True | 8.80 | 0.00 | True |  |
| zedge_greedy | optimised selection | 9.16 | 0.01 | True | 9.36 | 0.00 | True | 8.09 | 0.05 | True | 8.29 | 0.01 | True |  |
| zedge_herding | optimised selection | 10.22 | 0.00 | True | 11.61 | 0.00 | True | 9.38 | 0.00 | True | 10.77 | 0.00 | False |  |
| zedge_knn | optimised selection | 9.46 | 0.00 | True | 10.05 | 0.00 | True | 8.55 | 0.00 | True | 9.13 | 0.00 | True |  |
| zedge_mbb | optimised selection | 10.18 | 0.00 | True | 11.92 | 0.00 | True | 9.42 | 0.00 | True | 11.16 | 0.00 | False |  |
| zedge_pctsp | optimised selection | 9.21 | 0.02 | True | 9.65 | 0.00 | True | 8.17 | 0.03 | True | 8.61 | 0.00 | True |  |
| zedge_quilting | optimised selection | 8.56 | 0.68 | True | 8.63 | 0.46 | True | 7.79 | 0.41 | True | 7.86 | 0.23 | True | holdout_clf, holdout_reg, train_clf |
| zedge_zseries | optimised selection | 9.26 | 0.06 | True | 9.12 | 0.13 | True | 8.20 | 0.16 | True | 8.07 | 0.24 | True |  |
| vae_rand | random selection | 15.55 | 0.00 | False | 16.54 | 0.00 | True | 16.43 | 0.00 | False | 17.42 | 0.00 | False |  |
| zedge_rand | random selection | 10.35 | 0.00 | True | 12.04 | 0.00 | True | 9.58 | 0.00 | True | 11.27 | 0.00 | False |  |


## Ranking 1. Fidelity: val + OOT; utility: classification (`holdout_clf`)

Composition: Fidelity domain — the criteria distribution (F1, F2, F12), dependence (F3, F4), windows (F6, F9), long structure (F7), target (F8, F11), seams (F5), each against val and OOT (each criterion is the mean of the two). Utility domain — TSTR classification (binary and multiclass tasks), primary metric of each task type, tested on val and OOT. Rank = mean of the two domains with equal weight. Not included: privacy (F10), time, memory.

Friedman p = 0.000, Nemenyi CD = 11.00, datasets × methods in the test = 9 × 22.

Columns: `method` — method id; `family` — method family: long-series generator, random selection, optimised selection, seam processing (a joiner on a stitcher that also runs without it; joiner in brackets); `avg_rank` — mean rank over datasets (seeds averaged within a dataset); 1 = best; `ci_lo` — lower bound of the 95% bootstrap interval of avg_rank; `ci_hi` — upper bound of the 95% bootstrap interval of avg_rank; `p_first` — share of bootstrap samples in which the method has the lowest avg_rank; `p_top3` — share of bootstrap samples in which the method is among the three lowest; `p_worse_than_best_holm` — p-value of the one-sided Wilcoxon test over datasets "worse than the first method", Holm correction; empty for the first method; `tier_wilcoxon` — True — not significantly worse than the first method (p_worse_than_best_holm ≥ 0.05).

Rows: sorted by avg_rank.

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| zedge_quilting | optimised selection | 8.56 | 7.44 | 9.76 | 0.68 | 0.95 |  | True |
| zedge_ts_ar | long-series generator | 9.04 | 7.17 | 10.95 | 0.23 | 0.60 | 0.41 | True |
| zedge_greedy | optimised selection | 9.16 | 8.25 | 10.15 | 0.01 | 0.46 | 0.41 | True |
| zedge_pctsp | optimised selection | 9.21 | 8.30 | 10.11 | 0.02 | 0.36 | 0.41 | True |
| zedge_zseries | optimised selection | 9.26 | 8.76 | 9.83 | 0.06 | 0.38 | 0.41 | True |
| zedge_atsp | optimised selection | 9.37 | 8.03 | 10.75 | 0.00 | 0.22 | 0.41 | True |
| zedge_knn | optimised selection | 9.46 | 8.65 | 10.35 | 0.00 | 0.03 | 0.29 | True |
| zedge_ts_long | long-series generator | 10.05 | 8.64 | 11.51 | 0.00 | 0.00 | 0.10 | True |
| zedge_mbb | optimised selection | 10.18 | 9.00 | 11.42 | 0.00 | 0.00 | 0.10 | True |
| zedge_herding | optimised selection | 10.22 | 9.25 | 11.16 | 0.00 | 0.00 | 0.10 | True |
| zedge_rand | random selection | 10.35 | 9.13 | 11.54 | 0.00 | 0.00 | 0.07 | True |
| vae_zseries | optimised selection | 13.47 | 12.03 | 14.95 | 0.00 | 0.00 | 0.07 | True |
| vae_herding | optimised selection | 13.60 | 12.74 | 14.49 | 0.00 | 0.00 | 0.04 | False |
| diffusion_ts | long-series generator | 13.75 | 11.78 | 15.45 | 0.00 | 0.00 | 0.04 | False |
| vae_quilting | optimised selection | 14.37 | 12.78 | 15.96 | 0.00 | 0.00 | 0.07 | True |
| vae_atsp | optimised selection | 14.81 | 13.03 | 16.48 | 0.00 | 0.00 | 0.07 | True |
| vae_pctsp | optimised selection | 14.85 | 13.38 | 16.27 | 0.00 | 0.00 | 0.07 | True |
| vae_greedy | optimised selection | 15.15 | 13.61 | 16.73 | 0.00 | 0.00 | 0.07 | True |
| vae_knn | optimised selection | 15.40 | 13.54 | 17.16 | 0.00 | 0.00 | 0.07 | True |
| vae_rand | random selection | 15.55 | 13.47 | 17.48 | 0.00 | 0.00 | 0.04 | False |
| vae_mbb | optimised selection | 15.59 | 13.50 | 17.54 | 0.00 | 0.00 | 0.04 | False |
| timesfm | long-series generator | 15.70 | 13.19 | 18.21 | 0.00 | 0.00 | 0.11 | True |
| chronos | long-series generator | 16.36 | 14.17 | 18.21 | 0.00 | 0.00 | 0.09 | True |
| timestral | long-series generator | 18.53 | 16.94 | 20.00 | 0.00 | 0.00 | 0.04 | False |


## Ranking 2. Fidelity: val + OOT; utility: regression (`holdout_reg`)

Composition: Fidelity domain — the criteria distribution (F1, F2, F12), dependence (F3, F4), windows (F6, F9), long structure (F7), target (F8, F11), seams (F5), each against val and OOT (each criterion is the mean of the two). Utility domain — TSTR regression (point, quantile, multi-step and volatility tasks), primary metric of each task type, tested on val and OOT. Rank = mean of the two domains with equal weight. Not included: privacy (F10), time, memory.

Friedman p = 0.000, Nemenyi CD = 11.00, datasets × methods in the test = 9 × 22.

Columns: `method` — method id; `family` — method family: long-series generator, random selection, optimised selection, seam processing (a joiner on a stitcher that also runs without it; joiner in brackets); `avg_rank` — mean rank over datasets (seeds averaged within a dataset); 1 = best; `ci_lo` — lower bound of the 95% bootstrap interval of avg_rank; `ci_hi` — upper bound of the 95% bootstrap interval of avg_rank; `p_first` — share of bootstrap samples in which the method has the lowest avg_rank; `p_top3` — share of bootstrap samples in which the method is among the three lowest; `p_worse_than_best_holm` — p-value of the one-sided Wilcoxon test over datasets "worse than the first method", Holm correction; empty for the first method; `tier_wilcoxon` — True — not significantly worse than the first method (p_worse_than_best_holm ≥ 0.05).

Rows: sorted by avg_rank.

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| zedge_quilting | optimised selection | 8.63 | 7.51 | 9.73 | 0.46 | 0.92 |  | True |
| zedge_ts_ar | long-series generator | 8.82 | 6.67 | 11.06 | 0.40 | 0.81 | 0.54 | True |
| zedge_zseries | optimised selection | 9.12 | 8.15 | 10.01 | 0.13 | 0.60 | 0.54 | True |
| zedge_greedy | optimised selection | 9.36 | 8.22 | 10.50 | 0.00 | 0.34 | 0.41 | True |
| zedge_pctsp | optimised selection | 9.65 | 8.34 | 10.91 | 0.00 | 0.07 | 0.22 | True |
| zedge_atsp | optimised selection | 9.77 | 7.89 | 11.77 | 0.00 | 0.16 | 0.54 | True |
| zedge_ts_long | long-series generator | 9.94 | 8.29 | 11.74 | 0.00 | 0.05 | 0.41 | True |
| zedge_knn | optimised selection | 10.05 | 8.78 | 11.41 | 0.00 | 0.00 | 0.16 | True |
| timesfm | long-series generator | 11.39 | 9.05 | 13.52 | 0.01 | 0.03 | 0.22 | True |
| zedge_herding | optimised selection | 11.61 | 9.71 | 13.51 | 0.00 | 0.00 | 0.11 | True |
| zedge_mbb | optimised selection | 11.92 | 9.97 | 13.97 | 0.00 | 0.00 | 0.11 | True |
| zedge_rand | random selection | 12.04 | 10.05 | 14.14 | 0.00 | 0.00 | 0.08 | True |
| diffusion_ts | long-series generator | 12.22 | 10.63 | 13.68 | 0.00 | 0.00 | 0.08 | True |
| vae_zseries | optimised selection | 13.53 | 11.82 | 15.22 | 0.00 | 0.00 | 0.11 | True |
| timestral | long-series generator | 13.76 | 12.06 | 15.66 | 0.00 | 0.00 | 0.08 | True |
| chronos | long-series generator | 13.94 | 11.96 | 15.86 | 0.00 | 0.00 | 0.09 | True |
| vae_herding | optimised selection | 14.23 | 13.18 | 15.28 | 0.00 | 0.00 | 0.04 | False |
| vae_quilting | optimised selection | 14.94 | 12.82 | 16.99 | 0.00 | 0.00 | 0.08 | True |
| vae_atsp | optimised selection | 15.22 | 13.05 | 17.19 | 0.00 | 0.00 | 0.08 | True |
| vae_pctsp | optimised selection | 15.40 | 13.63 | 17.03 | 0.00 | 0.00 | 0.04 | False |
| vae_greedy | optimised selection | 15.49 | 13.62 | 17.35 | 0.00 | 0.00 | 0.08 | True |
| vae_knn | optimised selection | 15.96 | 13.62 | 18.17 | 0.00 | 0.00 | 0.08 | True |
| vae_mbb | optimised selection | 16.50 | 13.96 | 18.72 | 0.00 | 0.00 | 0.08 | True |
| vae_rand | random selection | 16.54 | 14.06 | 18.83 | 0.00 | 0.00 | 0.08 | True |


## Ranking 3. Fidelity: train; utility: classification (`train_clf`)

Composition: Fidelity domain — the criteria distribution (F1, F2, F12), dependence (F3, F4), windows (F6, F9), long structure (F7), target (F8, F11), seams (F5), each against train. Utility domain — TSTR classification (binary and multiclass tasks), primary metric of each task type, tested on val and OOT. Rank = mean of the two domains with equal weight. Not included: privacy (F10), time, memory.

Friedman p = 0.000, Nemenyi CD = 11.00, datasets × methods in the test = 9 × 22.

Columns: `method` — method id; `family` — method family: long-series generator, random selection, optimised selection, seam processing (a joiner on a stitcher that also runs without it; joiner in brackets); `avg_rank` — mean rank over datasets (seeds averaged within a dataset); 1 = best; `ci_lo` — lower bound of the 95% bootstrap interval of avg_rank; `ci_hi` — upper bound of the 95% bootstrap interval of avg_rank; `p_first` — share of bootstrap samples in which the method has the lowest avg_rank; `p_top3` — share of bootstrap samples in which the method is among the three lowest; `p_worse_than_best_holm` — p-value of the one-sided Wilcoxon test over datasets "worse than the first method", Holm correction; empty for the first method; `tier_wilcoxon` — True — not significantly worse than the first method (p_worse_than_best_holm ≥ 0.05).

Rows: sorted by avg_rank.

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| zedge_quilting | optimised selection | 7.79 | 6.52 | 9.19 | 0.41 | 0.81 |  | True |
| zedge_ts_ar | long-series generator | 7.93 | 6.23 | 9.70 | 0.34 | 0.64 | 0.99 | True |
| zedge_greedy | optimised selection | 8.09 | 7.44 | 8.90 | 0.05 | 0.55 | 0.99 | True |
| zedge_pctsp | optimised selection | 8.17 | 7.40 | 8.93 | 0.03 | 0.43 | 0.99 | True |
| zedge_zseries | optimised selection | 8.20 | 7.60 | 8.76 | 0.16 | 0.42 | 0.99 | True |
| zedge_atsp | optimised selection | 8.40 | 7.30 | 9.53 | 0.00 | 0.13 | 0.61 | True |
| zedge_knn | optimised selection | 8.55 | 8.01 | 9.24 | 0.00 | 0.03 | 0.61 | True |
| zedge_ts_long | long-series generator | 9.24 | 8.09 | 10.44 | 0.00 | 0.00 | 0.11 | True |
| zedge_herding | optimised selection | 9.38 | 8.57 | 10.19 | 0.00 | 0.00 | 0.30 | True |
| zedge_mbb | optimised selection | 9.42 | 8.55 | 10.29 | 0.00 | 0.00 | 0.30 | True |
| zedge_rand | random selection | 9.58 | 8.69 | 10.43 | 0.00 | 0.00 | 0.11 | True |
| vae_herding | optimised selection | 13.78 | 12.99 | 14.61 | 0.00 | 0.00 | 0.04 | False |
| vae_zseries | optimised selection | 13.93 | 12.60 | 15.26 | 0.00 | 0.00 | 0.06 | True |
| diffusion_ts | long-series generator | 14.54 | 12.59 | 16.15 | 0.00 | 0.00 | 0.04 | False |
| vae_quilting | optimised selection | 14.97 | 13.46 | 16.49 | 0.00 | 0.00 | 0.06 | True |
| vae_atsp | optimised selection | 15.53 | 14.11 | 16.89 | 0.00 | 0.00 | 0.04 | False |
| vae_pctsp | optimised selection | 15.69 | 14.41 | 16.87 | 0.00 | 0.00 | 0.04 | False |
| vae_greedy | optimised selection | 15.87 | 14.50 | 17.19 | 0.00 | 0.00 | 0.06 | True |
| vae_knn | optimised selection | 16.27 | 14.90 | 17.62 | 0.00 | 0.00 | 0.04 | False |
| vae_rand | random selection | 16.43 | 14.95 | 17.84 | 0.00 | 0.00 | 0.04 | False |
| vae_mbb | optimised selection | 16.46 | 14.91 | 17.92 | 0.00 | 0.00 | 0.04 | False |
| timesfm | long-series generator | 16.77 | 14.19 | 19.37 | 0.00 | 0.00 | 0.14 | True |
| chronos | long-series generator | 17.56 | 15.62 | 19.30 | 0.00 | 0.00 | 0.09 | True |
| timestral | long-series generator | 20.17 | 18.44 | 21.66 | 0.00 | 0.00 | 0.04 | False |


## Ranking 4. Fidelity: train; utility: regression (`train_reg`)

Composition: Fidelity domain — the criteria distribution (F1, F2, F12), dependence (F3, F4), windows (F6, F9), long structure (F7), target (F8, F11), seams (F5), each against train. Utility domain — TSTR regression (point, quantile, multi-step and volatility tasks), primary metric of each task type, tested on val and OOT. Rank = mean of the two domains with equal weight. Not included: privacy (F10), time, memory.

Friedman p = 0.000, Nemenyi CD = 11.00, datasets × methods in the test = 9 × 22.

Columns: `method` — method id; `family` — method family: long-series generator, random selection, optimised selection, seam processing (a joiner on a stitcher that also runs without it; joiner in brackets); `avg_rank` — mean rank over datasets (seeds averaged within a dataset); 1 = best; `ci_lo` — lower bound of the 95% bootstrap interval of avg_rank; `ci_hi` — upper bound of the 95% bootstrap interval of avg_rank; `p_first` — share of bootstrap samples in which the method has the lowest avg_rank; `p_top3` — share of bootstrap samples in which the method is among the three lowest; `p_worse_than_best_holm` — p-value of the one-sided Wilcoxon test over datasets "worse than the first method", Holm correction; empty for the first method; `tier_wilcoxon` — True — not significantly worse than the first method (p_worse_than_best_holm ≥ 0.05).

Rows: sorted by avg_rank.

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| zedge_ts_ar | long-series generator | 7.71 | 5.74 | 9.82 | 0.51 | 0.83 |  | True |
| zedge_quilting | optimised selection | 7.86 | 6.68 | 9.11 | 0.23 | 0.84 | 0.82 | True |
| zedge_zseries | optimised selection | 8.07 | 7.22 | 8.85 | 0.24 | 0.62 | 0.82 | True |
| zedge_greedy | optimised selection | 8.29 | 7.45 | 9.15 | 0.01 | 0.46 | 0.74 | True |
| zedge_pctsp | optimised selection | 8.61 | 7.50 | 9.65 | 0.00 | 0.09 | 0.50 | True |
| zedge_atsp | optimised selection | 8.80 | 7.19 | 10.51 | 0.00 | 0.14 | 0.14 | True |
| zedge_ts_long | long-series generator | 9.13 | 7.80 | 10.56 | 0.00 | 0.03 | 0.14 | True |
| zedge_knn | optimised selection | 9.13 | 8.18 | 10.16 | 0.00 | 0.00 | 0.14 | True |
| zedge_herding | optimised selection | 10.77 | 9.12 | 12.43 | 0.00 | 0.00 | 0.04 | False |
| zedge_mbb | optimised selection | 11.16 | 9.56 | 12.78 | 0.00 | 0.00 | 0.04 | False |
| zedge_rand | random selection | 11.27 | 9.66 | 12.88 | 0.00 | 0.00 | 0.04 | False |
| timesfm | long-series generator | 12.46 | 10.25 | 14.54 | 0.00 | 0.00 | 0.14 | True |
| diffusion_ts | long-series generator | 13.01 | 11.56 | 14.34 | 0.00 | 0.00 | 0.07 | True |
| vae_zseries | optimised selection | 13.99 | 12.47 | 15.49 | 0.00 | 0.00 | 0.14 | True |
| vae_herding | optimised selection | 14.41 | 13.52 | 15.31 | 0.00 | 0.00 | 0.04 | False |
| chronos | long-series generator | 15.14 | 13.54 | 16.73 | 0.00 | 0.00 | 0.14 | True |
| timestral | long-series generator | 15.41 | 13.78 | 17.11 | 0.00 | 0.00 | 0.07 | True |
| vae_quilting | optimised selection | 15.53 | 13.48 | 17.46 | 0.00 | 0.00 | 0.11 | True |
| vae_atsp | optimised selection | 15.94 | 14.16 | 17.59 | 0.00 | 0.00 | 0.07 | True |
| vae_greedy | optimised selection | 16.20 | 14.54 | 17.71 | 0.00 | 0.00 | 0.07 | True |
| vae_pctsp | optimised selection | 16.24 | 14.74 | 17.60 | 0.00 | 0.00 | 0.07 | True |
| vae_knn | optimised selection | 16.82 | 15.03 | 18.53 | 0.00 | 0.00 | 0.07 | True |
| vae_mbb | optimised selection | 17.37 | 15.42 | 19.10 | 0.00 | 0.00 | 0.07 | True |
| vae_rand | random selection | 17.42 | 15.55 | 19.16 | 0.00 | 0.00 | 0.04 | False |


## Core-metric rankings

The four rankings with the fidelity domain restricted to the core metric set — one or two canonical metrics per criterion, fixed in advance by what they measure: distribution (F1.2_w1, F2.1_ks_d24); dependence (F3.5_log_psd, F4.1_how_mean); windows (F6.1_disc_score, F6.4_mmd); long structure (F7.1_roll_mean_ks, F7.2_roll_std_ks); target (F11.1_class_share_logratio); seams (F5.7_seam_detect_auc_dev). Utility is the same as in the four rankings. The full rankings above use every metric.

Columns: `method` — method id; `family` — method family: long-series generator, random selection, optimised selection, seam processing (a joiner on a stitcher that also runs without it; joiner in brackets); `first_in` — the core rankings in which the method has the lowest avg_rank; `<ranking>:rank` — avg_rank of the method in that core ranking (1 = best); `<ranking>:p_first` — share of bootstrap samples in which the method is first; `<ranking>:tier` — True — not significantly worse than the first method (one-sided Wilcoxon over datasets, Holm, α = 0.05).

Rows: methods ordered by family, then name.

| method | family | core_holdout_clf:rank | core_holdout_clf:p_first | core_holdout_clf:tier | core_holdout_reg:rank | core_holdout_reg:p_first | core_holdout_reg:tier | core_train_clf:rank | core_train_clf:p_first | core_train_clf:tier | core_train_reg:rank | core_train_reg:p_first | core_train_reg:tier | first_in |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| chronos | long-series generator | 17.15 | 0.00 | True | 14.73 | 0.00 | True | 18.78 | 0.00 | True | 16.36 | 0.00 | True |  |
| diffusion_ts | long-series generator | 13.91 | 0.00 | False | 12.38 | 0.00 | True | 15.22 | 0.00 | False | 13.70 | 0.00 | True |  |
| timesfm | long-series generator | 16.00 | 0.00 | True | 11.68 | 0.00 | True | 17.63 | 0.00 | True | 13.32 | 0.00 | True |  |
| timestral | long-series generator | 18.42 | 0.00 | False | 13.65 | 0.00 | True | 20.90 | 0.00 | False | 16.13 | 0.00 | False |  |
| zedge_ts_ar | long-series generator | 8.82 | 0.25 | True | 8.60 | 0.37 | True | 7.73 | 0.27 | True | 7.51 | 0.38 | True |  |
| zedge_ts_long | long-series generator | 9.61 | 0.00 | True | 9.51 | 0.00 | True | 8.78 | 0.00 | True | 8.67 | 0.00 | True |  |
| vae_atsp | optimised selection | 14.94 | 0.00 | True | 15.36 | 0.00 | True | 15.82 | 0.00 | False | 16.24 | 0.00 | False |  |
| vae_greedy | optimised selection | 15.34 | 0.00 | True | 15.67 | 0.00 | True | 16.13 | 0.00 | False | 16.46 | 0.00 | False |  |
| vae_herding | optimised selection | 13.56 | 0.00 | False | 14.19 | 0.00 | False | 13.27 | 0.00 | False | 13.90 | 0.00 | False |  |
| vae_knn | optimised selection | 15.70 | 0.00 | False | 16.26 | 0.00 | True | 16.66 | 0.00 | False | 17.21 | 0.00 | False |  |
| vae_mbb | optimised selection | 15.87 | 0.00 | True | 16.78 | 0.00 | True | 16.86 | 0.00 | False | 17.77 | 0.00 | False |  |
| vae_pctsp | optimised selection | 14.84 | 0.00 | True | 15.38 | 0.00 | False | 15.82 | 0.00 | False | 16.36 | 0.00 | False |  |
| vae_quilting | optimised selection | 14.64 | 0.00 | True | 15.21 | 0.00 | True | 15.34 | 0.00 | True | 15.90 | 0.00 | True |  |
| vae_zseries | optimised selection | 13.48 | 0.00 | True | 13.54 | 0.00 | True | 13.97 | 0.00 | True | 14.03 | 0.00 | False |  |
| zedge_atsp | optimised selection | 9.22 | 0.01 | True | 9.62 | 0.00 | True | 8.02 | 0.01 | True | 8.42 | 0.00 | True |  |
| zedge_greedy | optimised selection | 9.05 | 0.00 | True | 9.25 | 0.00 | True | 7.75 | 0.01 | True | 7.94 | 0.01 | True |  |
| zedge_herding | optimised selection | 9.91 | 0.00 | True | 11.30 | 0.00 | True | 8.71 | 0.00 | True | 10.10 | 0.00 | True |  |
| zedge_knn | optimised selection | 9.29 | 0.00 | True | 9.88 | 0.00 | True | 8.05 | 0.00 | True | 8.63 | 0.00 | True |  |
| zedge_mbb | optimised selection | 10.04 | 0.00 | True | 11.78 | 0.00 | True | 9.06 | 0.00 | True | 10.80 | 0.00 | True |  |
| zedge_pctsp | optimised selection | 9.07 | 0.01 | True | 9.50 | 0.00 | True | 7.64 | 0.05 | True | 8.07 | 0.00 | True |  |
| zedge_quilting | optimised selection | 8.25 | 0.67 | True | 8.32 | 0.49 | True | 7.47 | 0.33 | True | 7.54 | 0.23 | True | core_holdout_clf, core_holdout_reg, core_train_clf |
| zedge_zseries | optimised selection | 9.02 | 0.07 | True | 8.88 | 0.14 | True | 7.50 | 0.34 | True | 7.37 | 0.38 | True | core_train_reg |
| vae_rand | random selection | 15.88 | 0.00 | True | 16.87 | 0.00 | True | 16.85 | 0.00 | False | 17.84 | 0.00 | False |  |
| zedge_rand | random selection | 10.19 | 0.00 | True | 11.88 | 0.00 | True | 9.15 | 0.00 | True | 10.84 | 0.00 | True |  |


### Core metrics. Fidelity: val + OOT; utility: classification (`core_holdout_clf`)

Friedman p = 0.000, Nemenyi CD = 11.00, datasets × methods in the test = 9 × 22. Rows: sorted by avg_rank.

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| zedge_quilting | optimised selection | 8.25 | 6.97 | 9.50 | 0.67 | 0.93 |  | True |
| zedge_ts_ar | long-series generator | 8.82 | 6.65 | 11.04 | 0.25 | 0.61 | 0.44 | True |
| zedge_zseries | optimised selection | 9.02 | 8.23 | 9.84 | 0.07 | 0.44 | 0.44 | True |
| zedge_greedy | optimised selection | 9.05 | 7.89 | 10.28 | 0.00 | 0.36 | 0.44 | True |
| zedge_pctsp | optimised selection | 9.07 | 7.92 | 10.27 | 0.01 | 0.32 | 0.44 | True |
| zedge_atsp | optimised selection | 9.22 | 7.58 | 10.88 | 0.01 | 0.21 | 0.44 | True |
| zedge_knn | optimised selection | 9.29 | 8.25 | 10.47 | 0.00 | 0.07 | 0.44 | True |
| zedge_ts_long | long-series generator | 9.61 | 7.92 | 11.45 | 0.00 | 0.05 | 0.44 | True |
| zedge_herding | optimised selection | 9.91 | 8.89 | 11.00 | 0.00 | 0.00 | 0.20 | True |
| zedge_mbb | optimised selection | 10.04 | 8.63 | 11.54 | 0.00 | 0.00 | 0.44 | True |
| zedge_rand | random selection | 10.19 | 8.69 | 11.71 | 0.00 | 0.00 | 0.44 | True |
| vae_zseries | optimised selection | 13.48 | 11.81 | 15.11 | 0.00 | 0.00 | 0.08 | True |
| vae_herding | optimised selection | 13.56 | 12.87 | 14.31 | 0.00 | 0.00 | 0.04 | False |
| diffusion_ts | long-series generator | 13.91 | 11.70 | 15.88 | 0.00 | 0.00 | 0.04 | False |
| vae_quilting | optimised selection | 14.64 | 12.78 | 16.46 | 0.00 | 0.00 | 0.07 | True |
| vae_pctsp | optimised selection | 14.84 | 13.04 | 16.55 | 0.00 | 0.00 | 0.07 | True |
| vae_atsp | optimised selection | 14.94 | 12.87 | 16.92 | 0.00 | 0.00 | 0.07 | True |
| vae_greedy | optimised selection | 15.34 | 13.56 | 17.11 | 0.00 | 0.00 | 0.07 | True |
| vae_knn | optimised selection | 15.70 | 13.57 | 17.69 | 0.00 | 0.00 | 0.04 | False |
| vae_mbb | optimised selection | 15.87 | 13.38 | 18.14 | 0.00 | 0.00 | 0.08 | True |
| vae_rand | random selection | 15.88 | 13.44 | 18.16 | 0.00 | 0.00 | 0.07 | True |
| timesfm | long-series generator | 16.00 | 13.84 | 18.05 | 0.00 | 0.00 | 0.17 | True |
| chronos | long-series generator | 17.15 | 14.95 | 19.09 | 0.00 | 0.00 | 0.09 | True |
| timestral | long-series generator | 18.42 | 16.97 | 19.83 | 0.00 | 0.00 | 0.04 | False |


### Core metrics. Fidelity: val + OOT; utility: regression (`core_holdout_reg`)

Friedman p = 0.000, Nemenyi CD = 11.00, datasets × methods in the test = 9 × 22. Rows: sorted by avg_rank.

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| zedge_quilting | optimised selection | 8.32 | 7.10 | 9.45 | 0.49 | 0.90 |  | True |
| zedge_ts_ar | long-series generator | 8.60 | 6.08 | 11.32 | 0.37 | 0.81 | 0.62 | True |
| zedge_zseries | optimised selection | 8.88 | 7.67 | 10.01 | 0.14 | 0.62 | 0.62 | True |
| zedge_greedy | optimised selection | 9.25 | 7.83 | 10.70 | 0.00 | 0.25 | 0.62 | True |
| zedge_pctsp | optimised selection | 9.50 | 8.00 | 11.09 | 0.00 | 0.06 | 0.39 | True |
| zedge_ts_long | long-series generator | 9.51 | 7.49 | 11.81 | 0.00 | 0.20 | 0.62 | True |
| zedge_atsp | optimised selection | 9.62 | 7.40 | 12.00 | 0.00 | 0.16 | 0.62 | True |
| zedge_knn | optimised selection | 9.88 | 8.37 | 11.57 | 0.00 | 0.01 | 0.26 | True |
| zedge_herding | optimised selection | 11.30 | 9.32 | 13.40 | 0.00 | 0.00 | 0.16 | True |
| timesfm | long-series generator | 11.68 | 9.72 | 13.48 | 0.00 | 0.00 | 0.15 | True |
| zedge_mbb | optimised selection | 11.78 | 9.67 | 14.10 | 0.00 | 0.00 | 0.15 | True |
| zedge_rand | random selection | 11.88 | 9.63 | 14.26 | 0.00 | 0.00 | 0.13 | True |
| diffusion_ts | long-series generator | 12.38 | 10.51 | 14.15 | 0.00 | 0.00 | 0.10 | True |
| vae_zseries | optimised selection | 13.54 | 11.59 | 15.44 | 0.00 | 0.00 | 0.15 | True |
| timestral | long-series generator | 13.65 | 11.84 | 15.71 | 0.00 | 0.00 | 0.08 | True |
| vae_herding | optimised selection | 14.19 | 13.32 | 15.06 | 0.00 | 0.00 | 0.04 | False |
| chronos | long-series generator | 14.73 | 12.68 | 16.70 | 0.00 | 0.00 | 0.11 | True |
| vae_quilting | optimised selection | 15.21 | 12.83 | 17.58 | 0.00 | 0.00 | 0.13 | True |
| vae_atsp | optimised selection | 15.36 | 12.99 | 17.66 | 0.00 | 0.00 | 0.08 | True |
| vae_pctsp | optimised selection | 15.38 | 13.38 | 17.24 | 0.00 | 0.00 | 0.04 | False |
| vae_greedy | optimised selection | 15.67 | 13.55 | 17.73 | 0.00 | 0.00 | 0.08 | True |
| vae_knn | optimised selection | 16.26 | 13.67 | 18.63 | 0.00 | 0.00 | 0.10 | True |
| vae_mbb | optimised selection | 16.78 | 13.93 | 19.36 | 0.00 | 0.00 | 0.10 | True |
| vae_rand | random selection | 16.87 | 14.13 | 19.49 | 0.00 | 0.00 | 0.08 | True |


### Core metrics. Fidelity: train; utility: classification (`core_train_clf`)

Friedman p = 0.000, Nemenyi CD = 11.00, datasets × methods in the test = 9 × 22. Rows: sorted by avg_rank.

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| zedge_quilting | optimised selection | 7.47 | 6.14 | 8.92 | 0.33 | 0.68 |  | True |
| zedge_zseries | optimised selection | 7.50 | 6.89 | 8.14 | 0.34 | 0.62 | 1.00 | True |
| zedge_pctsp | optimised selection | 7.64 | 6.77 | 8.49 | 0.05 | 0.57 | 1.00 | True |
| zedge_ts_ar | long-series generator | 7.73 | 5.88 | 9.67 | 0.27 | 0.48 | 1.00 | True |
| zedge_greedy | optimised selection | 7.75 | 7.01 | 8.66 | 0.01 | 0.37 | 1.00 | True |
| zedge_atsp | optimised selection | 8.02 | 6.74 | 9.41 | 0.01 | 0.18 | 1.00 | True |
| zedge_knn | optimised selection | 8.05 | 7.46 | 8.69 | 0.00 | 0.09 | 1.00 | True |
| zedge_herding | optimised selection | 8.71 | 8.07 | 9.36 | 0.00 | 0.01 | 1.00 | True |
| zedge_ts_long | long-series generator | 8.78 | 7.51 | 10.10 | 0.00 | 0.00 | 0.64 | True |
| zedge_mbb | optimised selection | 9.06 | 8.34 | 9.82 | 0.00 | 0.00 | 0.74 | True |
| zedge_rand | random selection | 9.15 | 8.31 | 9.96 | 0.00 | 0.00 | 0.74 | True |
| vae_herding | optimised selection | 13.27 | 12.57 | 14.07 | 0.00 | 0.00 | 0.04 | False |
| vae_zseries | optimised selection | 13.97 | 12.48 | 15.43 | 0.00 | 0.00 | 0.05 | True |
| diffusion_ts | long-series generator | 15.22 | 13.03 | 17.10 | 0.00 | 0.00 | 0.04 | False |
| vae_quilting | optimised selection | 15.34 | 13.72 | 16.93 | 0.00 | 0.00 | 0.05 | True |
| vae_pctsp | optimised selection | 15.82 | 14.71 | 16.87 | 0.00 | 0.00 | 0.04 | False |
| vae_atsp | optimised selection | 15.82 | 14.46 | 17.16 | 0.00 | 0.00 | 0.04 | False |
| vae_greedy | optimised selection | 16.13 | 14.70 | 17.42 | 0.00 | 0.00 | 0.04 | False |
| vae_knn | optimised selection | 16.66 | 15.28 | 17.99 | 0.00 | 0.00 | 0.04 | False |
| vae_rand | random selection | 16.85 | 15.23 | 18.46 | 0.00 | 0.00 | 0.04 | False |
| vae_mbb | optimised selection | 16.86 | 15.16 | 18.40 | 0.00 | 0.00 | 0.04 | False |
| timesfm | long-series generator | 17.63 | 15.60 | 19.90 | 0.00 | 0.00 | 0.17 | True |
| chronos | long-series generator | 18.78 | 17.02 | 20.37 | 0.00 | 0.00 | 0.09 | True |
| timestral | long-series generator | 20.90 | 19.40 | 22.09 | 0.00 | 0.00 | 0.04 | False |


### Core metrics. Fidelity: train; utility: regression (`core_train_reg`)

Friedman p = 0.000, Nemenyi CD = 11.00, datasets × methods in the test = 9 × 22. Rows: sorted by avg_rank.

| method | family | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|---|
| zedge_zseries | optimised selection | 7.37 | 6.45 | 8.24 | 0.38 | 0.77 |  | True |
| zedge_ts_ar | long-series generator | 7.51 | 5.28 | 9.83 | 0.38 | 0.72 | 1.00 | True |
| zedge_quilting | optimised selection | 7.54 | 6.30 | 8.87 | 0.23 | 0.74 | 1.00 | True |
| zedge_greedy | optimised selection | 7.94 | 7.08 | 8.90 | 0.01 | 0.34 | 1.00 | True |
| zedge_pctsp | optimised selection | 8.07 | 6.95 | 9.19 | 0.00 | 0.19 | 1.00 | True |
| zedge_atsp | optimised selection | 8.42 | 6.67 | 10.35 | 0.00 | 0.17 | 1.00 | True |
| zedge_knn | optimised selection | 8.63 | 7.69 | 9.65 | 0.00 | 0.01 | 0.57 | True |
| zedge_ts_long | long-series generator | 8.67 | 7.04 | 10.48 | 0.00 | 0.06 | 0.90 | True |
| zedge_herding | optimised selection | 10.10 | 8.60 | 11.63 | 0.00 | 0.00 | 0.09 | True |
| zedge_mbb | optimised selection | 10.80 | 9.37 | 12.31 | 0.00 | 0.00 | 0.07 | True |
| zedge_rand | random selection | 10.84 | 9.25 | 12.45 | 0.00 | 0.00 | 0.07 | True |
| timesfm | long-series generator | 13.32 | 11.42 | 15.05 | 0.00 | 0.00 | 0.12 | True |
| diffusion_ts | long-series generator | 13.70 | 11.96 | 15.21 | 0.00 | 0.00 | 0.05 | True |
| vae_herding | optimised selection | 13.90 | 12.97 | 14.72 | 0.00 | 0.00 | 0.04 | False |
| vae_zseries | optimised selection | 14.03 | 12.34 | 15.71 | 0.00 | 0.00 | 0.04 | False |
| vae_quilting | optimised selection | 15.90 | 13.75 | 17.95 | 0.00 | 0.00 | 0.05 | True |
| timestral | long-series generator | 16.13 | 14.71 | 17.54 | 0.00 | 0.00 | 0.04 | False |
| vae_atsp | optimised selection | 16.24 | 14.52 | 17.91 | 0.00 | 0.00 | 0.04 | False |
| chronos | long-series generator | 16.36 | 14.94 | 17.78 | 0.00 | 0.00 | 0.08 | True |
| vae_pctsp | optimised selection | 16.36 | 14.98 | 17.66 | 0.00 | 0.00 | 0.04 | False |
| vae_greedy | optimised selection | 16.46 | 14.72 | 17.99 | 0.00 | 0.00 | 0.04 | False |
| vae_knn | optimised selection | 17.21 | 15.41 | 18.87 | 0.00 | 0.00 | 0.04 | False |
| vae_mbb | optimised selection | 17.77 | 15.66 | 19.64 | 0.00 | 0.00 | 0.04 | False |
| vae_rand | random selection | 17.84 | 15.79 | 19.76 | 0.00 | 0.00 | 0.04 | False |


## Normalised scores on the core metrics

Composition: every core metric on the scale random assembly (`noise_pair[0]`) = 0, real data = 1: (x − x_random) / (x_real − x_random); above 1 — closer to the reference than the real data, below 0 — worse than a random assembly. Fidelity against val and train, on the series cut to the length of the real reference (seed 0); utility — TSTR against TRTR, seeds averaged, models fitted on every task. A dataset is left out of a metric when its anchors differ by no more than the noise. Median over the metrics of a criterion within a dataset, then over datasets. Not used in the rankings: the size of the effect next to them. Per metric and dataset — `leaderboard/normalized.parquet`.

Columns: `method` — method id; `family` — method family: long-series generator, random selection, optimised selection, seam processing (a joiner on a stitcher that also runs without it; joiner in brackets); `fidelity` — median normalised score over every core fidelity metric; `utility` — median normalised score over every utility cell; `<criterion>` — median normalised score over the core metrics of the criterion.

Rows: methods ordered by family, then name.

| method | family | fidelity | utility | dependence | distribution | long_structure | target | windows | classification | regression |
|---|---|---|---|---|---|---|---|---|---|---|
| chronos | long-series generator | -0.30 | -0.18 | 0.12 | -0.64 | -0.02 | -0.56 | -0.62 | -0.39 | 0.58 |
| diffusion_ts | long-series generator | 0.45 | 0.41 | 0.22 | 0.91 | 0.61 | 0.70 | 0.29 | 0.29 | 0.48 |
| timesfm | long-series generator | 0.04 | 0.64 | -0.09 | 0.23 | 0.20 | -2.43 | -0.00 | 0.39 | 0.87 |
| timestral | long-series generator | -0.00 | -0.03 | 0.03 | 0.27 | -0.00 | -5.36 | 0.15 | -0.58 | 0.78 |
| zedge_ts_ar | long-series generator | 0.73 | 0.90 | 0.86 | 0.78 | 0.85 | 0.47 | 0.41 | 0.84 | 0.95 |
| zedge_ts_long | long-series generator | 0.75 | 0.74 | 0.29 | 0.98 | 0.57 | 0.91 | 0.88 | 0.66 | 0.83 |
| vae_atsp | optimised selection | 0.17 | 0.20 | -0.16 | 0.07 | 0.26 | 0.29 | 0.19 | 0.14 | 0.22 |
| vae_greedy | optimised selection | 0.01 | 0.14 | -0.09 | -0.06 | -0.00 | 0.22 | 0.15 | 0.05 | 0.16 |
| vae_herding | optimised selection | 0.42 | 0.23 | 0.21 | 0.60 | 0.21 | 0.29 | 0.52 | 0.17 | 0.30 |
| vae_knn | optimised selection | 0.06 | 0.01 | -0.11 | 0.14 | 0.34 | 0.19 | 0.19 | -0.01 | 0.05 |
| vae_mbb | optimised selection | 0.10 | -0.01 | 0.02 | 0.08 | 0.24 | 0.19 | 0.20 | -0.00 | 0.02 |
| vae_pctsp | optimised selection | 0.23 | 0.10 | 0.10 | 0.09 | 0.24 | 0.36 | 0.45 | 0.04 | 0.06 |
| vae_quilting | optimised selection | 0.06 | 0.15 | -0.23 | 0.10 | 0.25 | 0.05 | 0.31 | 0.09 | 0.22 |
| vae_zseries | optimised selection | 0.36 | 0.26 | 0.22 | 0.45 | 0.39 | 0.60 | 0.36 | 0.20 | 0.36 |
| zedge_atsp | optimised selection | 0.18 | 0.43 | 0.08 | 0.05 | 0.14 | 0.29 | 0.69 | 0.36 | 0.35 |
| zedge_greedy | optimised selection | 0.18 | 0.41 | 0.15 | 0.19 | 0.21 | 0.50 | 0.11 | 0.32 | 0.35 |
| zedge_herding | optimised selection | -0.00 | -0.04 | 0.10 | 0.00 | -0.06 | 0.16 | 0.50 | -0.03 | -0.06 |
| zedge_knn | optimised selection | 0.20 | 0.37 | 0.46 | 0.20 | 0.12 | 0.87 | 0.42 | 0.32 | 0.40 |
| zedge_mbb | optimised selection | 0.02 | 0.00 | 0.07 | 0.02 | 0.10 | 0.11 | 0.21 | 0.01 | 0.01 |
| zedge_pctsp | optimised selection | 0.01 | 0.43 | 0.14 | 0.05 | 0.01 | 0.02 | 0.33 | 0.42 | 0.37 |
| zedge_quilting | optimised selection | 0.39 | 0.55 | 0.51 | 0.19 | 0.62 | 0.51 | 0.29 | 0.44 | 0.56 |
| zedge_zseries | optimised selection | 0.04 | 0.47 | 0.25 | 0.14 | 0.10 | 0.11 | 0.05 | 0.28 | 0.50 |
| vae_rand | random selection | -0.00 | -0.00 | -0.00 | -0.00 | -0.00 | -0.00 | -0.00 | 0.00 | -0.00 |
| zedge_rand | random selection | -0.00 | -0.00 | -0.00 | 0.00 | 0.00 | -0.00 | -0.00 | 0.00 | -0.00 |


## Anchor check: does a metric tell real data from a random assembly

Composition: per dataset, gap = |real − random assembly| (assembly averaged over seeds) and noise = median over seeds of |random − its twin| (without the twin, as in min: the between-seed spread of the random path); ratio = gap / noise, median over datasets; separated — ratio > 1. The competing methods are not used, so the check does not depend on who wins. Computed on all seeds and separately on even and odd seeds: a flip — the verdict differs between the two halves. Fidelity against val and train; `real` is a piece of OOT, shorter than the synthetic series, so for distance metrics the gap is underestimated (conservative). Every leaf — `leaderboard/anchor_check.parquet`.

Columns: `n` — number of leaves; `separated` — separated on all seeds; `separated_even`, `separated_odd` — on each half; `flips` — leaves whose verdict differs between the halves.

| leaves | n | separated | separated_even | separated_odd | flips |
|---|---|---|---|---|---|
| every fidelity metric | 144 | 141 | 138 | 139 | 3 |
| core fidelity metrics | 18 | 18 | 16 | 17 | 1 |
| utility cells | 58 | 58 | 58 | 58 | 0 |


### Core fidelity metrics

Columns: `leaf` — metric (fidelity: `<metric>@<reference>`, val without suffix; utility: `task|model|metric@split`); `criterion` — the criterion whose two slices are compared; `n_datasets` — number of datasets in which the method is ranked; `ratio_all` — median over datasets of |real − random assembly| / noise (median |random − twin| over seeds, or the between-seed spread of the random path where the twin is not run); all seeds; `separated_all` — True — ratio_all > 1: the metric tells real data from a random assembly beyond the noise; `ratio_even` — ratio on the even seeds; `ratio_odd` — ratio on the odd seeds; `separated_even` — ratio_even > 1; `separated_odd` — ratio_odd > 1; `flip` — True — the verdict differs between even and odd seeds.

| leaf | criterion | n_datasets | ratio_all | separated_all | ratio_even | ratio_odd | separated_even | separated_odd | flip |
|---|---|---|---|---|---|---|---|---|---|
| F1.2_w1 | fidelity:distribution | 9 | 16.06 | True | 34.46 | 13.63 | True | True | False |
| F1.2_w1@train | fidelity:distribution | 9 | 11.80 | True | 14.10 | 8.80 | True | True | False |
| F11.1_class_share_logratio | fidelity:target | 9 | 10.31 | True | 6.58 | 7.18 | True | True | False |
| F11.1_class_share_logratio@train | fidelity:target | 9 | 9.69 | True | 7.06 | 6.38 | True | True | False |
| F2.1_ks_d24 | fidelity:distribution | 9 | 9.13 | True | 5.78 | 3.79 | True | True | False |
| F2.1_ks_d24@train | fidelity:distribution | 9 | 5.25 | True | 8.31 | 3.43 | True | True | False |
| F3.5_log_psd | fidelity:dependence | 9 | 5.76 | True | 2.96 | 5.06 | True | True | False |
| F3.5_log_psd@train | fidelity:dependence | 9 | 11.32 | True | 5.49 | 7.33 | True | True | False |
| F4.1_how_mean | fidelity:dependence | 9 | 18.23 | True | 37.10 | 8.99 | True | True | False |
| F4.1_how_mean@train | fidelity:dependence | 9 | 12.41 | True | 21.70 | 10.45 | True | True | False |
| F6.1_disc_score | fidelity:windows | 9 | 1.05 | True | 0.80 | 0.60 | False | False | False |
| F6.1_disc_score@train | fidelity:windows | 9 | 1.53 | True | 0.97 | 2.64 | False | True | True |
| F6.4_mmd | fidelity:windows | 9 | 6.92 | True | 16.25 | 7.93 | True | True | False |
| F6.4_mmd@train | fidelity:windows | 9 | 6.82 | True | 5.23 | 4.78 | True | True | False |
| F7.1_roll_mean_ks | fidelity:long_structure | 9 | 12.07 | True | 8.92 | 18.39 | True | True | False |
| F7.1_roll_mean_ks@train | fidelity:long_structure | 9 | 4.81 | True | 6.31 | 6.68 | True | True | False |
| F7.2_roll_std_ks | fidelity:long_structure | 9 | 6.89 | True | 5.35 | 2.88 | True | True | False |
| F7.2_roll_std_ks@train | fidelity:long_structure | 9 | 2.04 | True | 1.41 | 1.47 | True | True | False |


## Privacy (F10, memorisation)

Composition: F10.1 DCR — distance from a synthetic window to the nearest train window, relative to the same distance for held-out windows (|log ratio|); F10.2 — share of synthetic windows closer to train than the 5th percentile of real-to-real distances. Computed once, against train. Not part of the four rankings.

Columns: `method` — method id; `avg_rank` — mean rank over datasets (seeds averaged within a dataset); 1 = best; `ci_lo` — lower bound of the 95% bootstrap interval of avg_rank; `ci_hi` — upper bound of the 95% bootstrap interval of avg_rank; `p_first` — share of bootstrap samples in which the method has the lowest avg_rank; `p_top3` — share of bootstrap samples in which the method is among the three lowest; `p_worse_than_best_holm` — p-value of the one-sided Wilcoxon test over datasets "worse than the first method", Holm correction; empty for the first method; `tier_wilcoxon` — True — not significantly worse than the first method (p_worse_than_best_holm ≥ 0.05).

Rows: sorted by avg_rank.

| method | avg_rank | ci_lo | ci_hi | p_first | p_top3 | p_worse_than_best_holm | tier_wilcoxon |
|---|---|---|---|---|---|---|---|
| vae_herding | 9.33 | 6.90 | 11.64 | 0.50 | 0.80 |  | True |
| vae_mbb | 10.25 | 6.94 | 13.72 | 0.19 | 0.51 | 1.00 | True |
| vae_rand | 10.37 | 7.37 | 13.58 | 0.03 | 0.45 | 1.00 | True |
| zedge_ts_long | 11.08 | 9.18 | 13.12 | 0.04 | 0.23 | 1.00 | True |
| vae_knn | 11.30 | 8.51 | 13.91 | 0.01 | 0.10 | 1.00 | True |
| vae_greedy | 11.44 | 9.11 | 13.39 | 0.01 | 0.05 | 0.88 | True |
| zedge_ts_ar | 11.53 | 8.84 | 14.66 | 0.04 | 0.20 | 1.00 | True |
| chronos | 11.57 | 7.42 | 15.46 | 0.11 | 0.24 | 1.00 | True |
| zedge_rand | 11.66 | 9.49 | 13.44 | 0.00 | 0.09 | 0.13 | True |
| zedge_mbb | 11.81 | 9.87 | 13.43 | 0.00 | 0.02 | 0.04 | False |
| zedge_herding | 11.91 | 9.66 | 13.74 | 0.00 | 0.06 | 0.13 | True |
| vae_zseries | 11.92 | 10.82 | 13.00 | 0.00 | 0.01 | 1.00 | True |
| vae_atsp | 12.37 | 10.35 | 14.29 | 0.00 | 0.00 | 1.00 | True |
| vae_pctsp | 12.63 | 9.95 | 15.26 | 0.00 | 0.03 | 1.00 | True |
| vae_quilting | 12.90 | 10.21 | 15.38 | 0.00 | 0.00 | 0.39 | True |
| zedge_knn | 13.30 | 10.68 | 15.98 | 0.00 | 0.04 | 1.00 | True |
| diffusion_ts | 13.58 | 10.54 | 16.57 | 0.01 | 0.01 | 1.00 | True |
| zedge_zseries | 13.79 | 10.95 | 16.71 | 0.01 | 0.02 | 1.00 | True |
| timestral | 14.06 | 9.58 | 17.79 | 0.03 | 0.07 | 1.00 | True |
| zedge_atsp | 14.24 | 10.82 | 17.57 | 0.01 | 0.03 | 1.00 | True |
| zedge_greedy | 14.25 | 11.26 | 17.17 | 0.00 | 0.01 | 1.00 | True |
| zedge_quilting | 14.74 | 11.96 | 17.48 | 0.00 | 0.00 | 0.71 | True |
| zedge_pctsp | 14.81 | 11.63 | 17.96 | 0.00 | 0.00 | 1.00 | True |
| timesfm | 16.21 | 10.47 | 21.03 | 0.01 | 0.03 | 1.00 | True |


## Cost next to the rankings

Composition: for each of the four rankings, its quality rank, the same ranking with cost added as a third domain of equal weight (cost: total wall time of a series and peak memory), and the median total time. Times from different hardware are not comparable.

### `holdout_clf` — Fidelity: val + OOT; utility: classification

Columns: `method` — method id; `family` — method family: long-series generator, random selection, optimised selection, seam processing (a joiner on a stitcher that also runs without it; joiner in brackets); `avg_rank` — mean rank over datasets (seeds averaged within a dataset); 1 = best; `rank_with_cost` — avg_rank of the same ranking with cost (total time, peak memory) as a third domain of equal weight; `median_time_s` — median total wall time of one series (training + generation), seconds; `pareto` — True — no other method has both a lower-or-equal avg_rank and a lower-or-equal median_time_s (one of them strictly lower); False otherwise or without timing.

Rows: sorted by median_time_s.

| method | family | avg_rank | rank_with_cost | median_time_s | pareto |
|---|---|---|---|---|---|
| timestral | long-series generator | 18.53 | 14.88 | 1.23 | True |
| timesfm | long-series generator | 15.70 | 13.41 | 2.38 | True |
| chronos | long-series generator | 16.36 | 13.85 | 33.87 | False |
| vae_rand | random selection | 15.55 | 13.24 | 131.24 | True |
| vae_quilting | optimised selection | 14.37 | 12.62 | 131.24 | True |
| vae_greedy | optimised selection | 15.15 | 13.34 | 131.24 | False |
| vae_knn | optimised selection | 15.40 | 13.64 | 131.24 | False |
| vae_mbb | optimised selection | 15.59 | 13.93 | 131.24 | False |
| vae_herding | optimised selection | 13.60 | 12.80 | 131.26 | True |
| vae_zseries | optimised selection | 13.47 | 13.36 | 133.53 | True |
| vae_atsp | optimised selection | 14.81 | 14.25 | 163.58 | False |
| vae_pctsp | optimised selection | 14.85 | 14.17 | 170.95 | False |
| zedge_rand | random selection | 10.35 | 10.65 | 798.37 | True |
| zedge_quilting | optimised selection | 8.56 | 9.63 | 798.37 | True |
| zedge_greedy | optimised selection | 9.16 | 10.21 | 798.37 | False |
| zedge_knn | optimised selection | 9.46 | 10.56 | 798.37 | False |
| zedge_mbb | optimised selection | 10.18 | 11.21 | 798.37 | False |
| zedge_herding | optimised selection | 10.22 | 11.62 | 798.40 | False |
| zedge_zseries | optimised selection | 9.26 | 11.15 | 800.50 | False |
| zedge_atsp | optimised selection | 9.37 | 11.45 | 822.21 | False |
| zedge_pctsp | optimised selection | 9.21 | 11.28 | 838.59 | False |
| diffusion_ts | long-series generator | 13.75 | 16.40 | 2350.05 | False |
| zedge_ts_long | long-series generator | 10.05 | 11.85 | 2932.93 | False |
| zedge_ts_ar | long-series generator | 9.04 | 11.15 | 2948.88 | False |


### `holdout_reg` — Fidelity: val + OOT; utility: regression

Columns: `method` — method id; `family` — method family: long-series generator, random selection, optimised selection, seam processing (a joiner on a stitcher that also runs without it; joiner in brackets); `avg_rank` — mean rank over datasets (seeds averaged within a dataset); 1 = best; `rank_with_cost` — avg_rank of the same ranking with cost (total time, peak memory) as a third domain of equal weight; `median_time_s` — median total wall time of one series (training + generation), seconds; `pareto` — True — no other method has both a lower-or-equal avg_rank and a lower-or-equal median_time_s (one of them strictly lower); False otherwise or without timing.

Rows: sorted by median_time_s.

| method | family | avg_rank | rank_with_cost | median_time_s | pareto |
|---|---|---|---|---|---|
| timestral | long-series generator | 13.76 | 11.70 | 1.23 | True |
| timesfm | long-series generator | 11.39 | 10.54 | 2.38 | True |
| chronos | long-series generator | 13.94 | 12.23 | 33.87 | False |
| vae_rand | random selection | 16.54 | 13.89 | 131.24 | False |
| vae_quilting | optimised selection | 14.94 | 13.00 | 131.24 | False |
| vae_greedy | optimised selection | 15.49 | 13.56 | 131.24 | False |
| vae_knn | optimised selection | 15.96 | 14.01 | 131.24 | False |
| vae_mbb | optimised selection | 16.50 | 14.54 | 131.24 | False |
| vae_herding | optimised selection | 14.23 | 13.22 | 131.26 | False |
| vae_zseries | optimised selection | 13.53 | 13.40 | 133.53 | False |
| vae_atsp | optimised selection | 15.22 | 14.52 | 163.58 | False |
| vae_pctsp | optimised selection | 15.40 | 14.53 | 170.95 | False |
| zedge_rand | random selection | 12.04 | 11.77 | 798.37 | False |
| zedge_quilting | optimised selection | 8.63 | 9.68 | 798.37 | True |
| zedge_greedy | optimised selection | 9.36 | 10.34 | 798.37 | False |
| zedge_knn | optimised selection | 10.05 | 10.95 | 798.37 | False |
| zedge_mbb | optimised selection | 11.92 | 12.37 | 798.37 | False |
| zedge_herding | optimised selection | 11.61 | 12.54 | 798.40 | False |
| zedge_zseries | optimised selection | 9.12 | 11.06 | 800.50 | False |
| zedge_atsp | optimised selection | 9.77 | 11.72 | 822.21 | False |
| zedge_pctsp | optimised selection | 9.65 | 11.57 | 838.59 | False |
| diffusion_ts | long-series generator | 12.22 | 15.38 | 2350.05 | False |
| zedge_ts_long | long-series generator | 9.94 | 11.78 | 2932.93 | False |
| zedge_ts_ar | long-series generator | 8.82 | 11.01 | 2948.88 | False |


### `train_clf` — Fidelity: train; utility: classification

Columns: `method` — method id; `family` — method family: long-series generator, random selection, optimised selection, seam processing (a joiner on a stitcher that also runs without it; joiner in brackets); `avg_rank` — mean rank over datasets (seeds averaged within a dataset); 1 = best; `rank_with_cost` — avg_rank of the same ranking with cost (total time, peak memory) as a third domain of equal weight; `median_time_s` — median total wall time of one series (training + generation), seconds; `pareto` — True — no other method has both a lower-or-equal avg_rank and a lower-or-equal median_time_s (one of them strictly lower); False otherwise or without timing.

Rows: sorted by median_time_s.

| method | family | avg_rank | rank_with_cost | median_time_s | pareto |
|---|---|---|---|---|---|
| timestral | long-series generator | 20.17 | 15.98 | 1.23 | True |
| timesfm | long-series generator | 16.77 | 14.12 | 2.38 | True |
| chronos | long-series generator | 17.56 | 14.65 | 33.87 | False |
| vae_rand | random selection | 16.43 | 13.83 | 131.24 | True |
| vae_quilting | optimised selection | 14.97 | 13.02 | 131.24 | True |
| vae_greedy | optimised selection | 15.87 | 13.81 | 131.24 | False |
| vae_knn | optimised selection | 16.27 | 14.22 | 131.24 | False |
| vae_mbb | optimised selection | 16.46 | 14.51 | 131.24 | False |
| vae_herding | optimised selection | 13.78 | 12.92 | 131.26 | True |
| vae_zseries | optimised selection | 13.93 | 13.67 | 133.53 | False |
| vae_atsp | optimised selection | 15.53 | 14.73 | 163.58 | False |
| vae_pctsp | optimised selection | 15.69 | 14.73 | 170.95 | False |
| zedge_rand | random selection | 9.58 | 10.13 | 798.37 | True |
| zedge_quilting | optimised selection | 7.79 | 9.12 | 798.37 | True |
| zedge_greedy | optimised selection | 8.09 | 9.50 | 798.37 | False |
| zedge_knn | optimised selection | 8.55 | 9.95 | 798.37 | False |
| zedge_mbb | optimised selection | 9.42 | 10.71 | 798.37 | False |
| zedge_herding | optimised selection | 9.38 | 11.06 | 798.40 | False |
| zedge_zseries | optimised selection | 8.20 | 10.45 | 800.50 | False |
| zedge_atsp | optimised selection | 8.40 | 10.80 | 822.21 | False |
| zedge_pctsp | optimised selection | 8.17 | 10.59 | 838.59 | False |
| diffusion_ts | long-series generator | 14.54 | 16.92 | 2350.05 | False |
| zedge_ts_long | long-series generator | 9.24 | 11.31 | 2932.93 | False |
| zedge_ts_ar | long-series generator | 7.93 | 10.41 | 2948.88 | False |


### `train_reg` — Fidelity: train; utility: regression

Columns: `method` — method id; `family` — method family: long-series generator, random selection, optimised selection, seam processing (a joiner on a stitcher that also runs without it; joiner in brackets); `avg_rank` — mean rank over datasets (seeds averaged within a dataset); 1 = best; `rank_with_cost` — avg_rank of the same ranking with cost (total time, peak memory) as a third domain of equal weight; `median_time_s` — median total wall time of one series (training + generation), seconds; `pareto` — True — no other method has both a lower-or-equal avg_rank and a lower-or-equal median_time_s (one of them strictly lower); False otherwise or without timing.

Rows: sorted by median_time_s.

| method | family | avg_rank | rank_with_cost | median_time_s | pareto |
|---|---|---|---|---|---|
| timestral | long-series generator | 15.41 | 12.80 | 1.23 | True |
| timesfm | long-series generator | 12.46 | 11.25 | 2.38 | True |
| chronos | long-series generator | 15.14 | 13.03 | 33.87 | False |
| vae_rand | random selection | 17.42 | 14.48 | 131.24 | False |
| vae_quilting | optimised selection | 15.53 | 13.40 | 131.24 | False |
| vae_greedy | optimised selection | 16.20 | 14.03 | 131.24 | False |
| vae_knn | optimised selection | 16.82 | 14.59 | 131.24 | False |
| vae_mbb | optimised selection | 17.37 | 15.12 | 131.24 | False |
| vae_herding | optimised selection | 14.41 | 13.34 | 131.26 | False |
| vae_zseries | optimised selection | 13.99 | 13.71 | 133.53 | False |
| vae_atsp | optimised selection | 15.94 | 15.00 | 163.58 | False |
| vae_pctsp | optimised selection | 16.24 | 15.09 | 170.95 | False |
| zedge_rand | random selection | 11.27 | 11.26 | 798.37 | True |
| zedge_quilting | optimised selection | 7.86 | 9.17 | 798.37 | True |
| zedge_greedy | optimised selection | 8.29 | 9.62 | 798.37 | False |
| zedge_knn | optimised selection | 9.13 | 10.34 | 798.37 | False |
| zedge_mbb | optimised selection | 11.16 | 11.87 | 798.37 | False |
| zedge_herding | optimised selection | 10.77 | 11.98 | 798.40 | False |
| zedge_zseries | optimised selection | 8.07 | 10.36 | 800.50 | False |
| zedge_atsp | optimised selection | 8.80 | 11.07 | 822.21 | False |
| zedge_pctsp | optimised selection | 8.61 | 10.88 | 838.59 | False |
| diffusion_ts | long-series generator | 13.01 | 15.91 | 2350.05 | False |
| zedge_ts_long | long-series generator | 9.13 | 11.24 | 2932.93 | False |
| zedge_ts_ar | long-series generator | 7.71 | 10.26 | 2948.88 | True |


## Ranks by criterion and slice

Composition: the mean rank of every method in one criterion against one reference or on one test split. The four rankings are built from the fidelity columns against train / val / oot and the utility columns; `@—` (privacy) and cost are not part of them.

### Domains

Composition: one domain alone, the mean of its criteria (fidelity without privacy).

Columns: `method` — method id; `fidelity@<ref>` — mean rank over the fidelity criteria against train / val / oot; @all — against all three; `utility@<split>` — mean rank over the utility criteria tested on val / oot; @all — both.

| method | fidelity@train | fidelity@val | fidelity@oot | fidelity@all | utility@val | utility@oot | utility@all |
|---|---|---|---|---|---|---|---|
| chronos | 17.44 | 13.39 | 16.69 | 15.84 | 13.77 | 16.76 | 15.26 |
| diffusion_ts | 14.29 | 11.60 | 13.81 | 13.23 | 12.57 | 13.97 | 13.27 |
| timesfm | 15.60 | 12.54 | 14.38 | 14.17 | 13.20 | 14.05 | 13.63 |
| timestral | 19.15 | 14.34 | 17.36 | 16.95 | 15.58 | 17.28 | 16.43 |
| zedge_ts_ar | 7.82 | 9.88 | 10.21 | 9.31 | 7.96 | 7.67 | 7.81 |
| zedge_ts_long | 9.20 | 10.50 | 11.13 | 10.28 | 9.01 | 9.34 | 9.17 |
| vae_atsp | 15.79 | 14.53 | 14.17 | 14.83 | 15.41 | 15.96 | 15.68 |
| vae_greedy | 16.13 | 14.85 | 14.54 | 15.18 | 15.76 | 16.13 | 15.94 |
| vae_herding | 13.65 | 13.21 | 13.37 | 13.41 | 14.52 | 14.58 | 14.55 |
| vae_knn | 16.67 | 15.05 | 14.82 | 15.52 | 16.19 | 16.65 | 16.42 |
| vae_mbb | 17.03 | 15.28 | 15.31 | 15.87 | 16.74 | 16.84 | 16.79 |
| vae_pctsp | 15.97 | 14.56 | 14.03 | 14.85 | 15.63 | 16.28 | 15.95 |
| vae_quilting | 15.71 | 14.66 | 14.35 | 14.91 | 14.83 | 14.75 | 14.79 |
| vae_zseries | 13.75 | 13.24 | 12.42 | 13.13 | 13.62 | 14.73 | 14.18 |
| zedge_atsp | 8.15 | 10.35 | 9.83 | 9.44 | 9.48 | 8.62 | 9.05 |
| zedge_greedy | 7.84 | 10.34 | 9.61 | 9.27 | 9.06 | 8.02 | 8.54 |
| zedge_herding | 9.34 | 11.29 | 10.74 | 10.46 | 11.33 | 10.28 | 10.81 |
| zedge_knn | 8.53 | 10.84 | 9.88 | 9.75 | 9.50 | 8.81 | 9.15 |
| zedge_mbb | 9.66 | 11.72 | 10.66 | 10.68 | 11.47 | 10.35 | 10.91 |
| zedge_pctsp | 8.08 | 10.55 | 9.79 | 9.47 | 9.11 | 8.27 | 8.69 |
| zedge_quilting | 8.11 | 10.21 | 9.10 | 9.14 | 8.49 | 6.58 | 7.54 |
| zedge_zseries | 7.84 | 10.47 | 9.45 | 9.25 | 8.59 | 8.26 | 8.43 |
| vae_rand | 17.04 | 15.20 | 15.35 | 15.86 | 16.80 | 16.82 | 16.81 |
| zedge_rand | 9.66 | 11.70 | 10.71 | 10.69 | 11.88 | 10.48 | 11.18 |


### Fidelity

Columns: `method` — method id; `<criterion>@<slice>` — mean rank of the method: fidelity criterion against train / val / oot; `@—` — computed once (privacy).

| method | dependence@oot | dependence@train | dependence@val | distribution@oot | distribution@train | distribution@val | long_structure@oot | long_structure@train | long_structure@val | privacy@— | seams@oot | seams@train | seams@val | target@oot | target@train | target@val | windows@oot | windows@train | windows@val |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| chronos | 16.83 | 17.82 | 14.24 | 17.74 | 19.60 | 14.50 | 17.44 | 19.07 | 14.24 | 11.57 | 14.00 | 11.82 | 11.70 | 15.58 | 17.56 | 14.41 | 18.57 | 18.77 | 11.22 |
| diffusion_ts | 15.79 | 16.75 | 14.25 | 12.86 | 14.57 | 11.08 | 14.23 | 15.24 | 12.11 | 13.58 | 13.87 | 11.74 | 10.24 | 13.65 | 15.07 | 11.08 | 12.46 | 12.34 | 10.85 |
| timesfm | 12.85 | 13.24 | 10.59 | 13.93 | 15.51 | 12.20 | 12.71 | 15.03 | 11.89 | 16.21 | 14.02 | 15.59 | 14.48 | 16.83 | 18.36 | 17.21 | 15.95 | 15.86 | 8.86 |
| timestral | 14.13 | 16.75 | 11.38 | 16.98 | 19.88 | 14.17 | 17.31 | 19.38 | 15.13 | 14.06 | 18.48 | 18.36 | 14.97 | 18.44 | 19.93 | 17.52 | 18.82 | 20.60 | 12.90 |
| zedge_ts_ar | 8.38 | 5.67 | 10.05 | 10.11 | 6.16 | 9.89 | 11.09 | 8.81 | 10.52 | 11.53 | 10.21 | 7.65 | 8.14 | 11.18 | 9.37 | 10.37 | 10.31 | 9.27 | 10.33 |
| zedge_ts_long | 12.87 | 10.71 | 13.46 | 10.09 | 6.57 | 9.87 | 11.00 | 9.71 | 10.28 | 11.08 | 10.83 | 8.70 | 8.52 | 11.65 | 10.36 | 10.35 | 10.37 | 9.12 | 10.52 |
| vae_atsp | 15.53 | 16.76 | 14.50 | 13.62 | 15.90 | 13.64 | 13.51 | 15.05 | 13.33 | 12.37 | 12.78 | 15.12 | 15.55 | 15.40 | 15.97 | 15.53 | 14.18 | 15.94 | 14.62 |
| vae_greedy | 15.35 | 16.40 | 14.50 | 14.22 | 16.33 | 14.05 | 14.00 | 15.64 | 13.33 | 11.44 | 13.23 | 15.42 | 16.02 | 15.53 | 16.67 | 16.05 | 14.94 | 16.32 | 15.15 |
| vae_herding | 14.69 | 14.67 | 14.66 | 12.51 | 13.38 | 12.73 | 12.77 | 13.12 | 12.76 | 9.33 | 13.23 | 12.39 | 11.76 | 13.76 | 13.46 | 13.61 | 13.24 | 14.86 | 13.77 |
| vae_knn | 15.80 | 17.28 | 14.68 | 14.49 | 16.68 | 14.16 | 14.23 | 16.27 | 13.68 | 11.30 | 13.20 | 15.60 | 15.85 | 16.22 | 17.33 | 16.59 | 15.01 | 16.88 | 15.36 |
| vae_mbb | 16.13 | 18.20 | 14.96 | 14.31 | 16.52 | 14.48 | 14.64 | 15.93 | 13.89 | 10.25 | 14.51 | 16.10 | 15.68 | 17.28 | 17.67 | 17.54 | 14.96 | 17.79 | 15.11 |
| vae_pctsp | 15.55 | 16.46 | 14.15 | 13.49 | 16.27 | 13.48 | 13.29 | 15.67 | 13.88 | 12.63 | 12.73 | 15.39 | 15.87 | 14.80 | 15.79 | 15.18 | 14.32 | 16.26 | 14.78 |
| vae_quilting | 15.05 | 16.16 | 14.70 | 14.04 | 16.17 | 14.35 | 14.04 | 15.07 | 13.28 | 12.90 | 13.48 | 15.03 | 15.58 | 14.59 | 15.68 | 15.01 | 14.93 | 16.14 | 15.08 |
| vae_zseries | 13.56 | 13.95 | 13.39 | 12.67 | 14.88 | 12.93 | 12.79 | 14.21 | 13.40 | 11.92 | 10.54 | 12.27 | 12.76 | 12.28 | 13.23 | 13.01 | 12.66 | 13.97 | 13.93 |
| zedge_atsp | 9.04 | 7.76 | 10.15 | 10.89 | 8.87 | 11.40 | 11.09 | 8.88 | 11.46 | 14.24 | 9.64 | 9.22 | 9.56 | 8.07 | 6.66 | 7.98 | 10.25 | 7.52 | 11.56 |
| zedge_greedy | 8.97 | 7.52 | 10.33 | 10.53 | 8.22 | 11.39 | 10.75 | 8.24 | 11.32 | 14.25 | 9.81 | 8.81 | 10.11 | 8.38 | 7.13 | 8.29 | 9.24 | 7.13 | 10.61 |
| zedge_herding | 9.69 | 9.17 | 11.29 | 10.33 | 8.36 | 11.56 | 10.23 | 8.65 | 11.74 | 11.91 | 14.68 | 12.56 | 11.93 | 9.20 | 8.67 | 9.65 | 10.30 | 8.65 | 11.61 |
| zedge_knn | 9.30 | 7.79 | 10.68 | 10.73 | 8.56 | 11.58 | 10.43 | 8.65 | 11.68 | 13.30 | 10.83 | 10.78 | 10.68 | 8.53 | 7.94 | 8.87 | 9.44 | 7.46 | 11.53 |
| zedge_mbb | 9.87 | 9.32 | 11.54 | 10.92 | 8.83 | 12.01 | 10.28 | 9.31 | 11.88 | 11.81 | 12.30 | 11.47 | 12.66 | 9.76 | 9.84 | 10.31 | 10.83 | 9.21 | 11.93 |
| zedge_pctsp | 9.18 | 7.62 | 10.05 | 11.18 | 8.81 | 11.79 | 11.09 | 9.08 | 11.98 | 14.81 | 9.87 | 9.27 | 9.78 | 8.51 | 6.83 | 8.43 | 8.92 | 6.90 | 11.25 |
| zedge_quilting | 8.09 | 7.17 | 9.48 | 10.18 | 9.08 | 11.17 | 10.18 | 9.14 | 11.79 | 14.74 | 9.88 | 8.98 | 9.70 | 7.63 | 6.74 | 8.77 | 8.66 | 7.56 | 10.34 |
| zedge_zseries | 8.55 | 6.88 | 10.19 | 10.43 | 8.02 | 11.26 | 9.94 | 8.18 | 11.83 | 13.79 | 10.68 | 10.61 | 11.01 | 8.21 | 6.29 | 8.17 | 8.91 | 7.06 | 10.33 |
| vae_rand | 16.00 | 18.28 | 15.01 | 14.31 | 16.56 | 14.44 | 14.62 | 15.84 | 13.55 | 10.37 | 14.99 | 16.14 | 15.62 | 17.41 | 17.77 | 17.57 | 14.75 | 17.67 | 15.02 |
| zedge_rand | 9.89 | 9.10 | 11.54 | 11.09 | 8.86 | 12.22 | 9.92 | 8.89 | 11.67 | 11.66 | 13.03 | 11.87 | 12.33 | 9.87 | 10.05 | 10.64 | 10.47 | 9.22 | 11.83 |


### Utility

Columns: `method` — method id; `<criterion>@<slice>` — mean rank of the method: TSTR utility criterion (classification, regression) tested on val / oot.

| method | classification@oot | classification@val | regression@oot | regression@val |
|---|---|---|---|---|
| chronos | 18.19 | 17.18 | 15.32 | 10.35 |
| diffusion_ts | 15.69 | 13.90 | 12.24 | 11.24 |
| timesfm | 18.29 | 17.60 | 9.82 | 8.81 |
| timestral | 21.30 | 21.10 | 13.26 | 10.07 |
| zedge_ts_ar | 7.97 | 8.08 | 7.36 | 7.83 |
| zedge_ts_long | 9.53 | 9.03 | 9.15 | 8.99 |
| vae_atsp | 15.46 | 15.08 | 16.46 | 15.74 |
| vae_greedy | 15.67 | 15.55 | 16.58 | 15.97 |
| vae_herding | 14.11 | 13.72 | 15.05 | 15.31 |
| vae_knn | 15.96 | 15.77 | 17.34 | 16.60 |
| vae_mbb | 15.85 | 15.91 | 17.83 | 17.57 |
| vae_pctsp | 15.61 | 15.21 | 16.95 | 16.05 |
| vae_quilting | 13.95 | 14.49 | 15.55 | 15.17 |
| vae_zseries | 14.71 | 13.52 | 14.75 | 13.72 |
| zedge_atsp | 8.38 | 8.91 | 8.85 | 10.05 |
| zedge_greedy | 7.97 | 8.73 | 8.07 | 9.40 |
| zedge_herding | 9.01 | 9.83 | 11.55 | 12.84 |
| zedge_knn | 8.48 | 8.66 | 9.14 | 10.33 |
| zedge_mbb | 8.72 | 9.63 | 11.99 | 13.32 |
| zedge_pctsp | 8.14 | 8.37 | 8.40 | 9.85 |
| zedge_quilting | 6.81 | 8.11 | 6.36 | 8.86 |
| zedge_zseries | 8.76 | 8.37 | 7.77 | 8.81 |
| vae_rand | 15.78 | 15.87 | 17.86 | 17.74 |
| zedge_rand | 8.87 | 10.11 | 12.09 | 13.65 |


### Cost

Columns: `method` — method id; `<criterion>@<slice>` — mean rank of the method: cost slice: total — total wall time of a series, training — training of the generator (a shared generator is charged to every method and seed using it), generation — sampling + assembly of a new series, memory — peak GPU memory and RSS increase; lower = better rank.

| method | cost@generation | cost@memory | cost@total | cost@training |
|---|---|---|---|---|
| chronos | 20.01 | 14.91 | 2.73 | 2.01 |
| diffusion_ts | 24.00 | 20.75 | 22.64 | 22.64 |
| timesfm | 7.95 | 15.65 | 2.01 | 2.84 |
| timestral | 7.09 | 14.17 | 1.00 | 1.00 |
| zedge_ts_ar | 17.32 | 7.09 | 23.66 | 23.14 |
| zedge_ts_long | 9.26 | 8.26 | 22.63 | 23.14 |
| vae_atsp | 19.92 | 15.43 | 10.81 | 7.59 |
| vae_greedy | 3.18 | 13.75 | 5.64 | 7.59 |
| vae_herding | 6.14 | 13.76 | 8.60 | 7.59 |
| vae_knn | 4.05 | 13.74 | 6.52 | 7.59 |
| vae_mbb | 5.05 | 13.74 | 7.51 | 7.59 |
| vae_pctsp | 21.75 | 14.06 | 11.54 | 7.59 |
| vae_quilting | 2.08 | 13.74 | 4.54 | 7.59 |
| vae_zseries | 9.47 | 16.64 | 9.64 | 7.59 |
| zedge_atsp | 20.56 | 11.32 | 19.92 | 16.82 |
| zedge_greedy | 13.11 | 9.78 | 14.81 | 16.82 |
| zedge_herding | 16.14 | 10.99 | 17.85 | 16.82 |
| zedge_knn | 14.04 | 9.78 | 15.75 | 16.82 |
| zedge_mbb | 15.08 | 9.78 | 16.79 | 16.82 |
| zedge_pctsp | 22.61 | 9.95 | 20.90 | 16.82 |
| zedge_quilting | 12.07 | 9.78 | 13.78 | 16.82 |
| zedge_zseries | 17.22 | 11.01 | 18.87 | 16.82 |
| vae_rand | 1.02 | 13.74 | 3.49 | 7.59 |
| zedge_rand | 11.01 | 9.78 | 12.72 | 16.82 |


### Theme: Class balance

Composition. Fidelity: F8.1 and F11 (class shares of every classification task, rare events separately, multiclass, loss of the minority class). Utility: ECE of the classifiers. Not part of the rankings.

Columns: `method` — method id; `fidelity@<ref>` — mean rank over the theme's fidelity metrics against that reference; `utility@<split>` — mean rank over the theme's utility metrics on that test split.

| method | fidelity@oot | fidelity@train | fidelity@val | utility@oot | utility@val |
|---|---|---|---|---|---|
| chronos | 15.71 | 17.06 | 14.94 | 15.79 | 14.13 |
| diffusion_ts | 14.32 | 15.51 | 11.90 | 14.49 | 12.26 |
| timesfm | 18.32 | 18.77 | 18.89 | 16.48 | 15.78 |
| timestral | 20.03 | 20.85 | 19.37 | 19.50 | 18.72 |
| zedge_ts_ar | 11.72 | 9.47 | 10.58 | 9.98 | 9.16 |
| zedge_ts_long | 11.78 | 9.99 | 10.34 | 10.18 | 9.37 |
| vae_atsp | 14.58 | 15.51 | 14.91 | 15.24 | 14.53 |
| vae_greedy | 14.55 | 16.05 | 15.32 | 15.49 | 14.46 |
| vae_herding | 12.98 | 12.36 | 12.96 | 13.75 | 13.59 |
| vae_knn | 15.46 | 16.86 | 16.01 | 15.94 | 14.65 |
| vae_mbb | 16.77 | 17.10 | 17.07 | 16.17 | 15.35 |
| vae_pctsp | 13.83 | 15.08 | 14.34 | 15.88 | 14.98 |
| vae_quilting | 13.95 | 15.29 | 14.57 | 14.36 | 14.23 |
| vae_zseries | 10.80 | 12.01 | 11.78 | 13.06 | 12.91 |
| zedge_atsp | 8.31 | 6.72 | 8.11 | 8.91 | 10.11 |
| zedge_greedy | 8.67 | 7.35 | 8.29 | 8.20 | 9.27 |
| zedge_herding | 9.39 | 9.25 | 10.08 | 9.61 | 11.28 |
| zedge_knn | 8.64 | 8.30 | 8.96 | 8.72 | 10.05 |
| zedge_mbb | 10.19 | 10.68 | 10.75 | 9.66 | 11.12 |
| zedge_pctsp | 8.86 | 7.20 | 8.53 | 8.71 | 9.95 |
| zedge_quilting | 8.19 | 7.37 | 9.05 | 7.31 | 9.50 |
| zedge_zseries | 8.60 | 6.32 | 8.09 | 8.30 | 8.85 |
| vae_rand | 16.89 | 17.19 | 17.02 | 16.39 | 15.52 |
| zedge_rand | 10.13 | 10.82 | 10.79 | 9.93 | 11.69 |


### Theme: Outliers and extremes

Composition. Fidelity: tail quantiles and the Hill index (F1.5, F1.10), kurtosis (F1.6), large jumps (F2.4), excursion durations (F7.4), F12 (frequency and size of exceedances of the real 0.5/99.5%, local spikes, block maxima and minima). Utility: regression error on the extreme 10% of the target and PR AUC of rare events. Not part of the rankings.

Columns: `method` — method id; `fidelity@<ref>` — mean rank over the theme's fidelity metrics against that reference; `utility@<split>` — mean rank over the theme's utility metrics on that test split.

| method | fidelity@oot | fidelity@train | fidelity@val | utility@oot | utility@val |
|---|---|---|---|---|---|
| chronos | 17.01 | 18.99 | 13.51 | 14.95 | 13.12 |
| diffusion_ts | 12.92 | 14.80 | 11.84 | 12.64 | 11.84 |
| timesfm | 14.35 | 14.92 | 11.73 | 9.97 | 10.61 |
| timestral | 16.35 | 18.98 | 12.94 | 14.61 | 13.62 |
| zedge_ts_ar | 10.88 | 5.55 | 10.84 | 7.16 | 7.99 |
| zedge_ts_long | 10.85 | 6.09 | 10.81 | 8.95 | 9.71 |
| vae_atsp | 13.27 | 16.60 | 13.63 | 14.88 | 14.41 |
| vae_greedy | 13.73 | 16.82 | 13.88 | 14.76 | 14.50 |
| vae_herding | 11.62 | 13.70 | 11.88 | 15.72 | 15.22 |
| vae_knn | 13.70 | 16.70 | 13.72 | 15.81 | 14.99 |
| vae_mbb | 12.76 | 16.01 | 13.75 | 16.97 | 16.56 |
| vae_pctsp | 13.44 | 17.18 | 13.61 | 15.05 | 14.39 |
| vae_quilting | 14.10 | 17.06 | 14.39 | 14.46 | 14.46 |
| vae_zseries | 12.46 | 15.81 | 12.92 | 13.93 | 13.53 |
| zedge_atsp | 12.01 | 9.37 | 12.41 | 9.45 | 9.64 |
| zedge_greedy | 11.22 | 8.60 | 12.23 | 8.69 | 9.25 |
| zedge_herding | 10.36 | 7.81 | 11.14 | 12.75 | 13.11 |
| zedge_knn | 11.40 | 8.66 | 12.03 | 10.56 | 10.42 |
| zedge_mbb | 11.16 | 8.04 | 11.70 | 12.41 | 13.10 |
| zedge_pctsp | 12.23 | 9.37 | 12.62 | 8.80 | 9.11 |
| zedge_quilting | 11.18 | 9.51 | 11.69 | 8.12 | 9.58 |
| zedge_zseries | 11.03 | 8.21 | 11.76 | 9.70 | 9.69 |
| vae_rand | 12.62 | 15.87 | 13.38 | 16.76 | 16.71 |
| zedge_rand | 11.17 | 8.05 | 11.93 | 12.58 | 13.94 |


### Tests by column

Columns: `column` — the ranked column (ranking, domain, criterion@slice); `p_friedman` — p-value of the Friedman test (blocks = datasets); `nemenyi_cd` — Nemenyi critical difference of Friedman ranks; `n_blocks` — number of datasets in the Friedman test (complete blocks; a method missing on a dataset is left out of the test, or the dataset is — whichever keeps more cells); `n_methods_friedman` — number of methods in the Friedman test; `best` — method with the lowest avg_rank in the column.

| column | p_friedman | nemenyi_cd | n_blocks | n_methods_friedman | best |
|---|---|---|---|---|---|
| ranking:holdout_clf | 0.000 | 10.998 | 9 | 22 | zedge_quilting |
| with_cost:holdout_clf | 0.000 | 10.998 | 9 | 22 | zedge_quilting |
| ranking:holdout_reg | 0.000 | 10.998 | 9 | 22 | zedge_quilting |
| with_cost:holdout_reg | 0.000 | 10.998 | 9 | 22 | zedge_quilting |
| ranking:train_clf | 0.000 | 10.998 | 9 | 22 | zedge_quilting |
| with_cost:train_clf | 0.000 | 10.998 | 9 | 22 | zedge_quilting |
| ranking:train_reg | 0.000 | 10.998 | 9 | 22 | zedge_ts_ar |
| with_cost:train_reg | 0.000 | 10.998 | 9 | 22 | zedge_quilting |
| ranking:core_holdout_clf | 0.000 | 10.998 | 9 | 22 | zedge_quilting |
| ranking:core_holdout_reg | 0.000 | 10.998 | 9 | 22 | zedge_quilting |
| ranking:core_train_clf | 0.000 | 10.998 | 9 | 22 | zedge_quilting |
| ranking:core_train_reg | 0.000 | 10.998 | 9 | 22 | zedge_zseries |
| domain:fidelity@train | 0.000 | 10.998 | 9 | 22 | zedge_ts_ar |
| domain:fidelity@val | 0.013 | 10.998 | 9 | 22 | zedge_ts_ar |
| domain:fidelity@oot | 0.000 | 10.998 | 9 | 22 | zedge_quilting |
| domain:fidelity@all | 0.000 | 10.998 | 9 | 22 | zedge_quilting |
| domain:utility@val | 0.000 | 10.998 | 9 | 22 | zedge_ts_ar |
| domain:utility@oot | 0.000 | 10.998 | 9 | 22 | zedge_quilting |
| domain:utility@all | 0.000 | 10.998 | 9 | 22 | zedge_quilting |
| cost@generation | 0.000 | 10.998 | 9 | 22 | vae_rand |
| cost@memory | 0.000 | 10.998 | 9 | 22 | zedge_ts_ar |
| cost@total | 0.000 | 10.998 | 9 | 22 | timestral |
| cost@training | 0.000 | 10.998 | 9 | 22 | timestral |
| fidelity:dependence@oot | 0.000 | 10.998 | 9 | 22 | zedge_quilting |
| fidelity:dependence@train | 0.000 | 10.998 | 9 | 22 | zedge_ts_ar |
| fidelity:dependence@val | 0.179 | 10.998 | 9 | 22 | zedge_quilting |
| fidelity:distribution@oot | 0.000 | 10.998 | 9 | 22 | zedge_ts_long |
| fidelity:distribution@train | 0.000 | 10.998 | 9 | 22 | zedge_ts_ar |
| fidelity:distribution@val | 0.256 | 10.998 | 9 | 22 | zedge_ts_long |
| fidelity:long_structure@oot | 0.000 | 10.998 | 9 | 22 | zedge_rand |
| fidelity:long_structure@train | 0.000 | 10.998 | 9 | 22 | zedge_zseries |
| fidelity:long_structure@val | 0.474 | 10.998 | 9 | 22 | zedge_ts_long |
| fidelity:privacy@— | 0.915 | 10.998 | 9 | 22 | vae_herding |
| fidelity:seams@oot | 0.050 | 10.998 | 9 | 22 | zedge_atsp |
| fidelity:seams@train | 0.001 | 10.998 | 9 | 22 | zedge_ts_ar |
| fidelity:seams@val | 0.010 | 10.998 | 9 | 22 | zedge_ts_ar |
| fidelity:target@oot | 0.000 | 10.998 | 9 | 22 | zedge_quilting |
| fidelity:target@train | 0.000 | 10.998 | 9 | 22 | zedge_zseries |
| fidelity:target@val | 0.000 | 10.998 | 9 | 22 | zedge_atsp |
| fidelity:windows@oot | 0.000 | 10.998 | 9 | 22 | zedge_quilting |
| fidelity:windows@train | 0.000 | 10.998 | 9 | 22 | zedge_pctsp |
| fidelity:windows@val | 0.044 | 10.998 | 9 | 22 | timesfm |
| utility:classification@oot | 0.000 | 10.998 | 9 | 22 | zedge_quilting |
| utility:classification@val | 0.000 | 10.998 | 9 | 22 | zedge_ts_ar |
| utility:regression@oot | 0.000 | 10.998 | 9 | 22 | zedge_quilting |
| utility:regression@val | 0.000 | 10.998 | 9 | 22 | zedge_ts_ar |
| theme:class_balance:fidelity@oot | 0.000 | 10.998 | 9 | 22 | zedge_quilting |
| theme:class_balance:fidelity@train | 0.000 | 10.998 | 9 | 22 | zedge_zseries |
| theme:class_balance:fidelity@val | 0.000 | 10.998 | 9 | 22 | zedge_zseries |
| theme:class_balance:utility@oot | 0.000 | 10.998 | 9 | 22 | zedge_quilting |
| theme:class_balance:utility@val | 0.000 | 10.998 | 9 | 22 | zedge_zseries |
| theme:extremes:fidelity@oot | 0.057 | 10.998 | 9 | 22 | zedge_herding |
| theme:extremes:fidelity@train | 0.000 | 10.998 | 9 | 22 | zedge_ts_ar |
| theme:extremes:fidelity@val | 0.736 | 10.998 | 9 | 22 | zedge_ts_long |
| theme:extremes:utility@oot | 0.000 | 10.998 | 9 | 22 | zedge_ts_ar |
| theme:extremes:utility@val | 0.000 | 10.998 | 9 | 22 | zedge_ts_ar |


## Effect size: median transfer ratio

Columns: `method` — method id; `<criterion>@<split>` — median over datasets, seeds, tasks and models of TSTR / TRTR (quality of a model trained on synthetic data / trained on real data, both tested on real data); 1 = as on real data.

| method | utility:classification@oot | utility:classification@val | utility:regression@oot | utility:regression@val |
|---|---|---|---|---|
| chronos | 0.46 | 0.52 | 0.72 | 0.85 |
| diffusion_ts | 0.78 | 0.77 | 0.83 | 0.80 |
| timesfm | 0.70 | 0.74 | 0.87 | 0.91 |
| timestral | 0.00 | 0.00 | 0.76 | 0.84 |
| zedge_ts_ar | 0.97 | 0.95 | 0.95 | 0.90 |
| zedge_ts_long | 0.92 | 0.90 | 0.91 | 0.84 |
| vae_atsp | 0.67 | 0.71 | 0.60 | 0.55 |
| vae_greedy | 0.67 | 0.70 | 0.61 | 0.55 |
| vae_herding | 0.73 | 0.73 | 0.67 | 0.58 |
| vae_knn | 0.66 | 0.69 | 0.57 | 0.55 |
| vae_mbb | 0.65 | 0.68 | 0.53 | 0.49 |
| vae_pctsp | 0.67 | 0.71 | 0.59 | 0.55 |
| vae_quilting | 0.70 | 0.70 | 0.62 | 0.56 |
| vae_zseries | 0.69 | 0.74 | 0.69 | 0.62 |
| zedge_atsp | 0.95 | 0.92 | 0.93 | 0.85 |
| zedge_greedy | 0.95 | 0.92 | 0.93 | 0.84 |
| zedge_herding | 0.93 | 0.87 | 0.88 | 0.73 |
| zedge_knn | 0.94 | 0.91 | 0.92 | 0.82 |
| zedge_mbb | 0.93 | 0.88 | 0.87 | 0.74 |
| zedge_pctsp | 0.95 | 0.93 | 0.93 | 0.85 |
| zedge_quilting | 0.97 | 0.93 | 0.95 | 0.85 |
| zedge_zseries | 0.93 | 0.90 | 0.93 | 0.85 |
| vae_rand | 0.65 | 0.69 | 0.52 | 0.48 |
| zedge_rand | 0.93 | 0.86 | 0.87 | 0.73 |


## Ranking stability (Kendall τ between the rankings of slices)

Columns: `comparison` — pair of slice types compared (e.g. train ↔ val); `count` — number of compared pairs of rankings; `mean` — mean Kendall τ (1 — the same order, 0 — unrelated, −1 — reversed); `min` — lowest Kendall τ; `max` — highest Kendall τ.

| comparison | count | mean | min | max |
|---|---|---|---|---|
| fidelity ↔ utility | 24.00 | 0.61 | 0.39 | 0.80 |
| linear ↔ gbdt | 4.00 | 0.80 | 0.75 | 0.86 |
| train ↔ oot | 8.00 | 0.82 | 0.62 | 0.93 |
| train ↔ val | 8.00 | 0.72 | 0.47 | 0.93 |
| val ↔ oot | 12.00 | 0.72 | 0.41 | 0.90 |


Columns: `method` — method id; `comparison` — the two kinds of slices compared; `criterion` — the criterion whose two slices are compared; `tau` — Kendall τ between the method orders of the two slices.

| comparison | criterion | tau |
|---|---|---|
| train ↔ val | fidelity:dependence | 0.72 |
| val ↔ oot | fidelity:dependence | 0.72 |
| train ↔ oot | fidelity:dependence | 0.89 |
| train ↔ val | fidelity:distribution | 0.72 |
| val ↔ oot | fidelity:distribution | 0.78 |
| train ↔ oot | fidelity:distribution | 0.84 |
| train ↔ val | fidelity:long_structure | 0.71 |
| val ↔ oot | fidelity:long_structure | 0.61 |
| train ↔ oot | fidelity:long_structure | 0.74 |
| train ↔ val | fidelity:seams | 0.73 |
| val ↔ oot | fidelity:seams | 0.41 |
| train ↔ oot | fidelity:seams | 0.62 |
| train ↔ val | fidelity:target | 0.87 |
| val ↔ oot | fidelity:target | 0.90 |
| train ↔ oot | fidelity:target | 0.93 |
| train ↔ val | fidelity:windows | 0.47 |
| val ↔ oot | fidelity:windows | 0.51 |
| train ↔ oot | fidelity:windows | 0.84 |
| train ↔ val | theme:class_balance:fidelity | 0.93 |
| val ↔ oot | theme:class_balance:fidelity | 0.83 |
| train ↔ oot | theme:class_balance:fidelity | 0.88 |
| val ↔ oot | theme:class_balance:utility | 0.80 |
| train ↔ val | theme:extremes:fidelity | 0.64 |
| val ↔ oot | theme:extremes:fidelity | 0.62 |
| train ↔ oot | theme:extremes:fidelity | 0.81 |
| val ↔ oot | theme:extremes:utility | 0.82 |
| val ↔ oot | utility:classification | 0.83 |
| val ↔ oot | utility:regression | 0.80 |
| linear ↔ gbdt | utility:classification@oot | 0.75 |
| linear ↔ gbdt | utility:classification@val | 0.79 |
| linear ↔ gbdt | utility:regression@oot | 0.86 |
| linear ↔ gbdt | utility:regression@val | 0.81 |


## Sensitivity to the criterion weights: `holdout_clf`

Composition: the ranking `holdout_clf` under 2000 random criterion weights (Dirichlet(1) within each domain). Median Kendall τ with equal weighting: 0.97.

Columns: `method` — method id; `equal_weights_rank` — score of the method with equal criterion weights (lower = better); `p_first` — share of the weight draws in which the method is first; `p_top3` — share of the weight draws in which the method is among the three first.

| method | equal_weights_rank | p_first | p_top3 |
|---|---|---|---|
| zedge_quilting | 8.56 | 1.00 | 1.00 |
| zedge_ts_ar | 9.04 | 0.00 | 0.80 |
| zedge_greedy | 9.16 | 0.00 | 0.84 |
| zedge_pctsp | 9.21 | 0.00 | 0.25 |
| zedge_zseries | 9.26 | 0.00 | 0.11 |
| zedge_atsp | 9.37 | 0.00 | 0.00 |
| zedge_knn | 9.46 | 0.00 | 0.00 |
| zedge_ts_long | 10.05 | 0.00 | 0.00 |
| zedge_mbb | 10.18 | 0.00 | 0.00 |
| zedge_herding | 10.22 | 0.00 | 0.00 |
| zedge_rand | 10.35 | 0.00 | 0.00 |
| vae_zseries | 13.47 | 0.00 | 0.00 |
| vae_herding | 13.60 | 0.00 | 0.00 |
| diffusion_ts | 13.75 | 0.00 | 0.00 |
| vae_quilting | 14.37 | 0.00 | 0.00 |
| vae_atsp | 14.81 | 0.00 | 0.00 |
| vae_pctsp | 14.85 | 0.00 | 0.00 |
| vae_greedy | 15.15 | 0.00 | 0.00 |
| vae_knn | 15.40 | 0.00 | 0.00 |
| vae_rand | 15.55 | 0.00 | 0.00 |
| vae_mbb | 15.59 | 0.00 | 0.00 |
| timesfm | 15.70 | 0.00 | 0.00 |
| chronos | 16.36 | 0.00 | 0.00 |
| timestral | 18.53 | 0.00 | 0.00 |


## Sensitivity to the criterion weights: `holdout_reg`

Composition: the ranking `holdout_reg` under 2000 random criterion weights (Dirichlet(1) within each domain). Median Kendall τ with equal weighting: 0.98.

Columns: `method` — method id; `equal_weights_rank` — score of the method with equal criterion weights (lower = better); `p_first` — share of the weight draws in which the method is first; `p_top3` — share of the weight draws in which the method is among the three first.

| method | equal_weights_rank | p_first | p_top3 |
|---|---|---|---|
| zedge_quilting | 8.63 | 0.81 | 1.00 |
| zedge_ts_ar | 8.82 | 0.19 | 0.98 |
| zedge_zseries | 9.12 | 0.00 | 0.99 |
| zedge_greedy | 9.36 | 0.00 | 0.03 |
| zedge_pctsp | 9.65 | 0.00 | 0.00 |
| zedge_atsp | 9.77 | 0.00 | 0.00 |
| zedge_ts_long | 9.94 | 0.00 | 0.00 |
| zedge_knn | 10.05 | 0.00 | 0.00 |
| timesfm | 11.39 | 0.00 | 0.00 |
| zedge_herding | 11.61 | 0.00 | 0.00 |
| zedge_mbb | 11.92 | 0.00 | 0.00 |
| zedge_rand | 12.04 | 0.00 | 0.00 |
| diffusion_ts | 12.22 | 0.00 | 0.00 |
| vae_zseries | 13.53 | 0.00 | 0.00 |
| timestral | 13.76 | 0.00 | 0.00 |
| chronos | 13.94 | 0.00 | 0.00 |
| vae_herding | 14.23 | 0.00 | 0.00 |
| vae_quilting | 14.94 | 0.00 | 0.00 |
| vae_atsp | 15.22 | 0.00 | 0.00 |
| vae_pctsp | 15.40 | 0.00 | 0.00 |
| vae_greedy | 15.49 | 0.00 | 0.00 |
| vae_knn | 15.96 | 0.00 | 0.00 |
| vae_mbb | 16.50 | 0.00 | 0.00 |
| vae_rand | 16.54 | 0.00 | 0.00 |


## Sensitivity to the criterion weights: `train_clf`

Composition: the ranking `train_clf` under 2000 random criterion weights (Dirichlet(1) within each domain). Median Kendall τ with equal weighting: 0.97.

Columns: `method` — method id; `equal_weights_rank` — score of the method with equal criterion weights (lower = better); `p_first` — share of the weight draws in which the method is first; `p_top3` — share of the weight draws in which the method is among the three first.

| method | equal_weights_rank | p_first | p_top3 |
|---|---|---|---|
| zedge_quilting | 7.79 | 0.61 | 1.00 |
| zedge_ts_ar | 7.93 | 0.39 | 0.72 |
| zedge_greedy | 8.09 | 0.00 | 0.76 |
| zedge_pctsp | 8.17 | 0.00 | 0.22 |
| zedge_zseries | 8.20 | 0.00 | 0.30 |
| zedge_atsp | 8.40 | 0.00 | 0.00 |
| zedge_knn | 8.55 | 0.00 | 0.00 |
| zedge_ts_long | 9.24 | 0.00 | 0.00 |
| zedge_herding | 9.38 | 0.00 | 0.00 |
| zedge_mbb | 9.42 | 0.00 | 0.00 |
| zedge_rand | 9.58 | 0.00 | 0.00 |
| vae_herding | 13.78 | 0.00 | 0.00 |
| vae_zseries | 13.93 | 0.00 | 0.00 |
| diffusion_ts | 14.54 | 0.00 | 0.00 |
| vae_quilting | 14.97 | 0.00 | 0.00 |
| vae_atsp | 15.53 | 0.00 | 0.00 |
| vae_pctsp | 15.69 | 0.00 | 0.00 |
| vae_greedy | 15.87 | 0.00 | 0.00 |
| vae_knn | 16.27 | 0.00 | 0.00 |
| vae_rand | 16.43 | 0.00 | 0.00 |
| vae_mbb | 16.46 | 0.00 | 0.00 |
| timesfm | 16.77 | 0.00 | 0.00 |
| chronos | 17.56 | 0.00 | 0.00 |
| timestral | 20.17 | 0.00 | 0.00 |


## Sensitivity to the criterion weights: `train_reg`

Composition: the ranking `train_reg` under 2000 random criterion weights (Dirichlet(1) within each domain). Median Kendall τ with equal weighting: 0.99.

Columns: `method` — method id; `equal_weights_rank` — score of the method with equal criterion weights (lower = better); `p_first` — share of the weight draws in which the method is first; `p_top3` — share of the weight draws in which the method is among the three first.

| method | equal_weights_rank | p_first | p_top3 |
|---|---|---|---|
| zedge_ts_ar | 7.71 | 0.67 | 0.96 |
| zedge_quilting | 7.86 | 0.32 | 1.00 |
| zedge_zseries | 8.07 | 0.01 | 0.89 |
| zedge_greedy | 8.29 | 0.00 | 0.15 |
| zedge_pctsp | 8.61 | 0.00 | 0.00 |
| zedge_atsp | 8.80 | 0.00 | 0.00 |
| zedge_ts_long | 9.13 | 0.00 | 0.00 |
| zedge_knn | 9.13 | 0.00 | 0.00 |
| zedge_herding | 10.77 | 0.00 | 0.00 |
| zedge_mbb | 11.16 | 0.00 | 0.00 |
| zedge_rand | 11.27 | 0.00 | 0.00 |
| timesfm | 12.46 | 0.00 | 0.00 |
| diffusion_ts | 13.01 | 0.00 | 0.00 |
| vae_zseries | 13.99 | 0.00 | 0.00 |
| vae_herding | 14.41 | 0.00 | 0.00 |
| chronos | 15.14 | 0.00 | 0.00 |
| timestral | 15.41 | 0.00 | 0.00 |
| vae_quilting | 15.53 | 0.00 | 0.00 |
| vae_atsp | 15.94 | 0.00 | 0.00 |
| vae_greedy | 16.20 | 0.00 | 0.00 |
| vae_pctsp | 16.24 | 0.00 | 0.00 |
| vae_knn | 16.82 | 0.00 | 0.00 |
| vae_mbb | 17.37 | 0.00 | 0.00 |
| vae_rand | 17.42 | 0.00 | 0.00 |


## Details

Tables in `leaderboard/`: ranks by metric group and task — `by_group.parquet`, by every leaf — `leaves.parquet`, full summaries by column with CI — `by_column.parquet` (`ranking:<name>` — the four rankings, `with_cost:<name>` — with cost, `domain:<name>`, criteria), the rankings — `rankings.parquet`, their summary — `rankings_summary.parquet`, cost next to them — `rankings_cost.parquet`; core-metric rankings — `rankings_core.parquet`, `rankings_core_summary.parquet`; normalised scores — `normalized.parquet`, `normalized_summary.parquet`; anchor check — `anchor_check.parquet`.
