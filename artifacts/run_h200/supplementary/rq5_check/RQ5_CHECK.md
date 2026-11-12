# RQ5 check — run_h200

Supplementary, not pre-specified (`python -m marathonts.hypotheses.rq5_check`). See the module docstring.

## Tests of RQ5 (a) by criterion

| unit               |   tests |   rejected |   median_ratio_min |   median_ratio_max |   ci_hi_max |   p_bh_max |   datasets_min |   datasets_max |
|:-------------------|--------:|-----------:|-------------------:|-------------------:|------------:|-----------:|---------------:|---------------:|
| classification@oot |      30 |         30 |              0     |              0.982 |       0.996 |     0.0158 |              6 |              9 |
| classification@val |      30 |         30 |              0     |              0.949 |       0.978 |     0.0158 |              6 |              9 |
| regression@oot     |      30 |         30 |              0.519 |              0.955 |       0.986 |     0.0158 |              6 |              9 |
| regression@val     |      30 |         30 |              0.474 |              0.929 |       0.991 |     0.0312 |              6 |              9 |

## ROC AUC cells with an undefined ratio

160 of 2700 cells (dataset × seed × task × model × split; 5.9%): the real series is within 0.02 of chance.

| dataset      | task             |   cells |
|:-------------|:-----------------|--------:|
| bitcoin      | clf_up_h24_q90   |      30 |
| beijing_pm25 | clf_up_h24_q99   |      20 |
| bitcoin      | clf_up_h24_q95   |      20 |
| bitcoin      | clf_up_h24_q99   |      20 |
| bitcoin      | clf_up_h6_q90    |      20 |
| beijing_pm25 | clf_up_h24_q95   |      10 |
| bitcoin      | clf_down_h24_q10 |      10 |
| bitcoin      | clf_up_h1_q90    |      10 |
| household    | clf_up_h24_q99   |      10 |
| pjm          | clf_up_h168_q90  |      10 |

## Absolute scores

Primary metric; TRTR: the real series; TSTR: median over the methods, and the best method.

| task             | model   | split   | metric   |   trtr |   tstr_median |   tstr_best | best_method         |   n_methods | higher_is_better   |
|:-----------------|:--------|:--------|:---------|-------:|--------------:|------------:|:--------------------|------------:|:-------------------|
| clf_down_h24_q10 | gbdt    | oot     | auc      | 0.78   |         0.726 |      0.799  | zedge_ts_long       |          30 | True               |
| clf_down_h24_q10 | gbdt    | val     | auc      | 0.854  |         0.796 |      0.866  | zedge_ts_ar         |          30 | True               |
| clf_down_h24_q10 | linear  | oot     | auc      | 0.818  |         0.756 |      0.836  | zedge_ts_ar         |          30 | True               |
| clf_down_h24_q10 | linear  | val     | auc      | 0.851  |         0.796 |      0.839  | zedge_ts_ar         |          30 | True               |
| clf_up_h168_q90  | gbdt    | oot     | auc      | 0.732  |         0.571 |      0.695  | zedge_ts_long       |          30 | True               |
| clf_up_h168_q90  | gbdt    | val     | auc      | 0.722  |         0.55  |      0.647  | zedge_ts_ar         |          30 | True               |
| clf_up_h168_q90  | linear  | oot     | auc      | 0.78   |         0.584 |      0.743  | zedge_ts_ar         |          30 | True               |
| clf_up_h168_q90  | linear  | val     | auc      | 0.786  |         0.653 |      0.781  | zedge_ts_ar         |          30 | True               |
| clf_up_h1_q90    | gbdt    | oot     | auc      | 0.936  |         0.925 |      0.932  | zedge_quilting      |          30 | True               |
| clf_up_h1_q90    | gbdt    | val     | auc      | 0.926  |         0.904 |      0.936  | timesfm             |          30 | True               |
| clf_up_h1_q90    | linear  | oot     | auc      | 0.892  |         0.879 |      0.911  | timesfm             |          30 | True               |
| clf_up_h1_q90    | linear  | val     | auc      | 0.881  |         0.872 |      0.882  | zedge_mbb           |          30 | True               |
| clf_up_h24_q90   | gbdt    | oot     | auc      | 0.764  |         0.651 |      0.758  | zedge_ts_ar         |          30 | True               |
| clf_up_h24_q90   | gbdt    | val     | auc      | 0.739  |         0.644 |      0.703  | diffusion_ts        |          30 | True               |
| clf_up_h24_q90   | linear  | oot     | auc      | 0.743  |         0.657 |      0.742  | zedge_ts_ar         |          30 | True               |
| clf_up_h24_q90   | linear  | val     | auc      | 0.747  |         0.664 |      0.749  | zedge_pctsp         |          30 | True               |
| clf_up_h24_q90   | mlp     | oot     | auc      | 0.789  |         0.672 |      0.757  | zedge_quilting      |          30 | True               |
| clf_up_h24_q90   | mlp     | val     | auc      | 0.757  |         0.652 |      0.727  | zedge_quilting      |          30 | True               |
| clf_up_h24_q95   | gbdt    | oot     | auc      | 0.732  |         0.649 |      0.747  | zedge_atsp          |          30 | True               |
| clf_up_h24_q95   | gbdt    | val     | auc      | 0.751  |         0.662 |      0.726  | zedge_zseries       |          30 | True               |
| clf_up_h24_q95   | linear  | oot     | auc      | 0.791  |         0.659 |      0.786  | zedge_ts_long       |          30 | True               |
| clf_up_h24_q95   | linear  | val     | auc      | 0.794  |         0.712 |      0.769  | zedge_ts_ar         |          30 | True               |
| clf_up_h24_q99   | gbdt    | oot     | auc      | 0.724  |         0.626 |      0.761  | zedge_greedy        |          30 | True               |
| clf_up_h24_q99   | gbdt    | val     | auc      | 0.723  |         0.687 |      0.802  | zedge_ts_ar         |          30 | True               |
| clf_up_h24_q99   | linear  | oot     | auc      | 0.869  |         0.657 |      0.866  | zedge_ts_ar         |          30 | True               |
| clf_up_h24_q99   | linear  | val     | auc      | 0.928  |         0.761 |      0.859  | zedge_ts_long       |          30 | True               |
| clf_up_h6_q90    | gbdt    | oot     | auc      | 0.911  |         0.88  |      0.915  | timesfm             |          30 | True               |
| clf_up_h6_q90    | gbdt    | val     | auc      | 0.902  |         0.817 |      0.908  | timesfm             |          30 | True               |
| clf_up_h6_q90    | linear  | oot     | auc      | 0.863  |         0.83  |      0.89   | timesfm             |          30 | True               |
| clf_up_h6_q90    | linear  | val     | auc      | 0.775  |         0.739 |      0.882  | timesfm             |          30 | True               |
| mc3_h24          | gbdt    | oot     | logloss  | 0.672  |         0.871 |      0.67   | zedge_zseries       |          30 | False              |
| mc3_h24          | gbdt    | val     | logloss  | 0.507  |         0.782 |      0.508  | zedge_ts_ar         |          30 | False              |
| mc3_h24          | linear  | oot     | logloss  | 0.534  |         0.761 |      0.657  | zedge_pctsp         |          30 | False              |
| mc3_h24          | linear  | val     | logloss  | 0.45   |         0.799 |      0.599  | zedge_zseries       |          30 | False              |
| ms_h24           | gbdt    | oot     | mase     | 0.778  |         1.04  |      0.827  | zedge_quilting      |          30 | False              |
| ms_h24           | gbdt    | val     | mase     | 0.744  |         1.5   |      1.16   | zedge_zseries       |          30 | False              |
| ms_h24           | linear  | oot     | mase     | 0.638  |         0.873 |      0.639  | zedge_ts_ar         |          30 | False              |
| ms_h24           | linear  | val     | mase     | 0.562  |         0.919 |      0.595  | zedge_zseries_wsola |          30 | False              |
| qreg_h24         | gbdt    | oot     | pinball  | 0.245  |         0.355 |      0.252  | zedge_quilting      |          30 | False              |
| qreg_h24         | gbdt    | val     | pinball  | 0.262  |         0.494 |      0.339  | timesfm             |          30 | False              |
| qreg_h24         | linear  | oot     | pinball  | 0.249  |         0.309 |      0.248  | zedge_zseries_wsola |          30 | False              |
| qreg_h24         | linear  | val     | pinball  | 0.186  |         0.295 |      0.204  | zedge_zseries       |          30 | False              |
| reg_h1           | gbdt    | oot     | mase     | 0.437  |         0.544 |      0.461  | timesfm             |          30 | False              |
| reg_h1           | gbdt    | val     | mase     | 0.385  |         0.684 |      0.48   | zedge_ts_long       |          30 | False              |
| reg_h1           | linear  | oot     | mase     | 0.151  |         0.16  |      0.153  | zedge_zseries       |          30 | False              |
| reg_h1           | linear  | val     | mase     | 0.155  |         0.179 |      0.158  | zedge_zseries       |          30 | False              |
| reg_h168         | gbdt    | oot     | mase     | 1.02   |         1.75  |      0.952  | timestral           |          30 | False              |
| reg_h168         | gbdt    | val     | mase     | 1.01   |         2.23  |      0.957  | timestral           |          30 | False              |
| reg_h168         | linear  | oot     | mase     | 0.903  |         1.58  |      0.956  | zedge_ts_long       |          30 | False              |
| reg_h168         | linear  | val     | mase     | 0.859  |         1.94  |      0.881  | timesfm             |          30 | False              |
| reg_h24          | gbdt    | oot     | mase     | 0.796  |         1.1   |      0.796  | timesfm             |          30 | False              |
| reg_h24          | gbdt    | val     | mase     | 0.793  |         1.39  |      0.81   | timesfm             |          30 | False              |
| reg_h24          | linear  | oot     | mase     | 0.832  |         0.888 |      0.841  | zedge_quilting      |          30 | False              |
| reg_h24          | linear  | val     | mase     | 0.581  |         0.957 |      0.573  | timestral           |          30 | False              |
| vol_h24          | gbdt    | oot     | mase     | 0.099  |         0.164 |      0.0903 | zedge_zseries_wsola |          30 | False              |
| vol_h24          | gbdt    | val     | mase     | 0.0809 |         0.154 |      0.0769 | zedge_zseries_xfade |          30 | False              |
| vol_h24          | linear  | oot     | mase     | 0.0879 |         0.127 |      0.0847 | zedge_zseries_xfade |          30 | False              |
| vol_h24          | linear  | val     | mase     | 0.0676 |         0.136 |      0.0581 | zedge_zseries_xfade |          30 | False              |
