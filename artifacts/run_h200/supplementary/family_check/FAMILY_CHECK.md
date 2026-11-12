# Family check — run_h200

Supplementary, not pre-specified (`python -m marathonts.hypotheses.family_check`). RQ4 by generator family (see the module docstring); the zEDGE pool and the zEDGE_TS paths form one family.

Methods: 30; families: 6 (chronos: 1, diffusion_ts: 1, timesfm: 1, timestral: 1, tsgm_vae: 12, zedge: 14). Pairs of a metric and a criterion: 956; predictive (pre-specified): 388; median of the median correlations: 0.53.

## Leave one family out

Pre-specified predictive pairs that stay predictive whatever family is left out: 44 of 388.

| left_out     |   n_methods_left_out |   methods_left |   predictive |   of_prespecified_still |   median_rho |
|:-------------|---------------------:|---------------:|-------------:|------------------------:|-------------:|
| chronos      |                    1 |             29 |          379 |                     352 |         0.53 |
| diffusion_ts |                    1 |             29 |          388 |                     370 |         0.54 |
| timesfm      |                    1 |             29 |          384 |                     367 |         0.55 |
| timestral    |                    1 |             29 |          377 |                     356 |         0.55 |
| tsgm_vae     |                   12 |             18 |          235 |                     199 |         0.29 |
| zedge        |                   14 |             16 |           85 |                      70 |         0.21 |

## Selection outside the family

For each criterion and held-out family: the metric with the largest median correlation on the other families, and on the held-out family the share of the pairs (held-out method, other method) ordered as by the transfer ratio (median over datasets; 95 % bootstrap interval over datasets; one-sided Wilcoxon against 0.5).

By held-out family (`interval_above_chance`: criteria whose interval lies above 0.5):

| held_out     |   criteria |   median_concordance |   interval_above_chance |
|:-------------|-----------:|---------------------:|------------------------:|
| chronos      |       4.00 |                 0.88 |                    4.00 |
| diffusion_ts |       4.00 |                 0.81 |                    2.00 |
| timesfm      |       4.00 |                 0.78 |                    4.00 |
| timestral    |       4.00 |                 0.75 |                    3.00 |
| tsgm_vae     |       4.00 |                 0.84 |                    3.00 |
| zedge        |       4.00 |                 0.76 |                    3.00 |

All:

| held_out     |   n_methods | criterion          | metric                    |   rho_on_rest |   n_datasets |   concordance |   ci_lo |   ci_hi |   p_above_chance |
|:-------------|------------:|:-------------------|:--------------------------|--------------:|-------------:|--------------:|--------:|--------:|-----------------:|
| chronos      |           1 | classification@oot | F8.6_cond_future_ks@oot   |         0.842 |            7 |         0.931 |   0.643 |   1     |          0.00781 |
| chronos      |           1 | classification@val | F8.5_cond_event_err@train |         0.818 |            7 |         0.862 |   0.655 |   0.931 |          0.00781 |
| chronos      |           1 | regression@oot     | F8.4_event_by_how@train   |         0.867 |            7 |         0.897 |   0.724 |   0.931 |          0.0391  |
| chronos      |           1 | regression@val     | F8.4_event_by_how         |         0.835 |            7 |         0.793 |   0.69  |   0.966 |          0.0703  |
| diffusion_ts |           1 | classification@oot | F6.6_feature_fid@train    |         0.835 |            9 |         0.821 |   0.621 |   0.893 |          0.00391 |
| diffusion_ts |           1 | classification@val | F8.5_cond_event_err@train |         0.806 |            9 |         0.793 |   0.759 |   0.893 |          0.00195 |
| diffusion_ts |           1 | regression@oot     | F8.4_event_by_how@train   |         0.885 |            9 |         0.821 |   0.483 |   0.963 |          0.0137  |
| diffusion_ts |           1 | regression@val     | F8.4_event_by_how         |         0.846 |            9 |         0.69  |   0.286 |   0.929 |          0.15    |
| timesfm      |           1 | classification@oot | F2.1_w1_d24@train         |         0.829 |            6 |         0.753 |   0.621 |   1     |          0.0156  |
| timesfm      |           1 | classification@val | F8.5_cond_event_err@train |         0.846 |            6 |         0.879 |   0.682 |   0.966 |          0.0156  |
| timesfm      |           1 | regression@oot     | F8.4_event_by_how@train   |         0.876 |            6 |         0.75  |   0.588 |   0.914 |          0.0156  |
| timesfm      |           1 | regression@val     | F8.4_event_by_how         |         0.841 |            6 |         0.81  |   0.57  |   0.905 |          0.0156  |
| timestral    |           1 | classification@oot | F9.2_coverage@train       |         0.823 |            9 |         0.964 |   0.621 |   1     |          0.00586 |
| timestral    |           1 | classification@val | F8.5_cond_event_err@train |         0.83  |            9 |         0.778 |   0.643 |   0.889 |          0.00195 |
| timestral    |           1 | regression@oot     | F8.4_event_by_how         |         0.871 |            9 |         0.586 |   0.259 |   0.776 |          0.318   |
| timestral    |           1 | regression@val     | F8.4_event_by_how         |         0.87  |            9 |         0.724 |   0.569 |   0.897 |          0.00391 |
| tsgm_vae     |          12 | classification@oot | F6.6_feature_fid@train    |         0.761 |            9 |         0.884 |   0.76  |   0.958 |          0.00195 |
| tsgm_vae     |          12 | classification@val | F8.5_cond_event_err@train |         0.759 |            9 |         0.852 |   0.471 |   0.956 |          0.00977 |
| tsgm_vae     |          12 | regression@oot     | F3.1_acf_in_window@train  |         0.777 |            9 |         0.799 |   0.602 |   0.898 |          0.00391 |
| tsgm_vae     |          12 | regression@val     | F6.4_mmd_2T               |         0.784 |            9 |         0.833 |   0.741 |   0.941 |          0.00391 |
| zedge        |          14 | classification@oot | F6.6_feature_fid@oot      |         0.738 |            9 |         0.771 |   0.348 |   0.967 |          0.0488  |
| zedge        |          14 | classification@val | F3.1_acf_in_window        |         0.776 |            9 |         0.665 |   0.504 |   0.969 |          0.0195  |
| zedge        |          14 | regression@oot     | F3.1_acf_in_window@oot    |         0.791 |            9 |         0.771 |   0.634 |   0.943 |          0.00391 |
| zedge        |          14 | regression@val     | F3.1_acf_in_window@train  |         0.841 |            9 |         0.755 |   0.554 |   0.781 |          0.0117  |

## Methods of the other run

RQ4 on the 16 methods (5 families) that `run_l4` also has: 85 predictive pairs; median of the median correlations 0.21; 85 pairs at the smallest p (0.0039).
