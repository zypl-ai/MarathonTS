# Family check — run_l4

Supplementary, not pre-specified (`python -m marathonts.hypotheses.family_check`). RQ4 by generator family (see the module docstring); the zEDGE pool and the zEDGE_TS paths form one family.

Methods: 16; families: 5 (chronos: 1, diffusion_ts: 1, timesfm: 1, timestral: 1, tsgm_vae: 12). Pairs of a metric and a criterion: 956; predictive (pre-specified): 0; median of the median correlations: 0.20.

## Leave one family out

Pre-specified predictive pairs that stay predictive whatever family is left out: 0 of 0.

| left_out     |   n_methods_left_out |   methods_left |   predictive |   of_prespecified_still |   median_rho |
|:-------------|---------------------:|---------------:|-------------:|------------------------:|-------------:|
| chronos      |                    1 |             15 |            0 |                       0 |         0.18 |
| diffusion_ts |                    1 |             15 |            0 |                       0 |         0.18 |
| timesfm      |                    1 |             15 |            0 |                       0 |         0.18 |
| timestral    |                    1 |             15 |            0 |                       0 |         0.18 |
| tsgm_vae     |                   12 |              4 |            0 |                       0 |       nan    |

## Selection outside the family

For each criterion and held-out family: the metric with the largest median correlation on the other families, and on the held-out family the share of the pairs (held-out method, other method) ordered as by the transfer ratio (median over datasets; 95 % bootstrap interval over datasets; one-sided Wilcoxon against 0.5).

By held-out family (`interval_above_chance`: criteria whose interval lies above 0.5):

| held_out     |   criteria |   median_concordance |   interval_above_chance |
|:-------------|-----------:|---------------------:|------------------------:|
| chronos      |       4.00 |                 0.90 |                    4.00 |
| diffusion_ts |       4.00 |                 0.56 |                    0.00 |
| timesfm      |       4.00 |                 0.90 |                    2.00 |
| timestral    |       4.00 |                 0.93 |                    2.00 |

All:

| held_out     |   n_methods | criterion          | metric                     |   rho_on_rest |   n_datasets |   concordance |   ci_lo |   ci_hi |   p_above_chance |
|:-------------|------------:|:-------------------|:---------------------------|--------------:|-------------:|--------------:|--------:|--------:|-----------------:|
| chronos      |           1 | classification@oot | F3.2_acf_beyond_window@oot |         0.684 |            7 |         1     |  0.933  |   1     |          0.00781 |
| chronos      |           1 | classification@val | F8.6_cond_future_ks@oot    |         0.679 |            7 |         0.933 |  0.714  |   1     |          0.00781 |
| chronos      |           1 | regression@oot     | F3.1_acf_in_window@oot     |         0.725 |            7 |         0.867 |  0.8    |   1     |          0.00781 |
| chronos      |           1 | regression@val     | F3.1_acf_in_window@train   |         0.771 |            7 |         0.667 |  0.533  |   0.933 |          0.0547  |
| diffusion_ts |           1 | classification@oot | F3.1_acf_in_window         |         0.774 |            9 |         0.462 |  0.267  |   0.867 |          0.27    |
| diffusion_ts |           1 | classification@val | F3.1_acf_in_window         |         0.803 |            9 |         0.462 |  0.267  |   0.933 |          0.445   |
| diffusion_ts |           1 | regression@oot     | F3.1_acf_in_window@oot     |         0.732 |            9 |         0.667 |  0.267  |   0.933 |          0.125   |
| diffusion_ts |           1 | regression@val     | F3.1_acf_in_window@train   |         0.775 |            9 |         0.857 |  0.154  |   0.933 |          0.0625  |
| timesfm      |           1 | classification@oot | F2.2_vol_ratio_err_d24@oot |         0.714 |            6 |         0.9   |  0.471  |   1     |          0.0469  |
| timesfm      |           1 | classification@val | F1.9_js                    |         0.618 |            6 |         0.567 |  0.0714 |   0.933 |          0.344   |
| timesfm      |           1 | regression@oot     | F3.1_acf_in_window@oot     |         0.732 |            6 |         0.9   |  0.6    |   1     |          0.0312  |
| timesfm      |           1 | regression@val     | F3.1_acf_in_window@train   |         0.775 |            6 |         0.9   |  0.7    |   0.967 |          0.0156  |
| timestral    |           1 | classification@oot | F3.1_acf_in_window         |         0.621 |            9 |         0.933 |  0.0714 |   1     |          0.0508  |
| timestral    |           1 | classification@val | F1.4_qq_corr               |         0.582 |            9 |         0.929 |  0.333  |   1     |          0.0879  |
| timestral    |           1 | regression@oot     | F3.1_acf_in_window@oot     |         0.729 |            9 |         0.933 |  0.6    |   1     |          0.0117  |
| timestral    |           1 | regression@val     | F3.1_acf_in_window@train   |         0.779 |            9 |         0.867 |  0.8    |   0.935 |          0.0469  |
