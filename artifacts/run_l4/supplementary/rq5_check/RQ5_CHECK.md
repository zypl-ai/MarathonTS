# RQ5 check — run_l4

Supplementary, not pre-specified (`python -m marathonts.hypotheses.rq5_check`). See the module docstring.

## Tests of RQ5 (a) by criterion

| unit               |   tests |   rejected |   median_ratio_min |   median_ratio_max |   ci_hi_max |   p_bh_max |   datasets_min |   datasets_max |
|:-------------------|--------:|-----------:|-------------------:|-------------------:|------------:|-----------:|---------------:|---------------:|
| classification@oot |      16 |         16 |              0     |              0.712 |       0.964 |     0.0159 |              6 |              9 |
| classification@val |      16 |         16 |              0     |              0.754 |       0.981 |     0.0159 |              6 |              9 |
| regression@oot     |      16 |         16 |              0.492 |              0.871 |       0.937 |     0.0159 |              6 |              9 |
| regression@val     |      16 |         16 |              0.471 |              0.89  |       0.991 |     0.0312 |              6 |              9 |

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

| task             | model   | split   | metric   |   trtr |   tstr_median |   tstr_best | best_method   |   n_methods | higher_is_better   |
|:-----------------|:--------|:--------|:---------|-------:|--------------:|------------:|:--------------|------------:|:-------------------|
| clf_down_h24_q10 | gbdt    | oot     | auc      | 0.78   |         0.736 |       0.763 | vae_herding   |          16 | True               |
| clf_down_h24_q10 | gbdt    | val     | auc      | 0.854  |         0.742 |       0.834 | diffusion_ts  |          16 | True               |
| clf_down_h24_q10 | linear  | oot     | auc      | 0.818  |         0.767 |       0.805 | vae_knn       |          16 | True               |
| clf_down_h24_q10 | linear  | val     | auc      | 0.851  |         0.769 |       0.847 | diffusion_ts  |          16 | True               |
| clf_up_h168_q90  | gbdt    | oot     | auc      | 0.732  |         0.571 |       0.64  | timesfm       |          16 | True               |
| clf_up_h168_q90  | gbdt    | val     | auc      | 0.722  |         0.555 |       0.636 | diffusion_ts  |          16 | True               |
| clf_up_h168_q90  | linear  | oot     | auc      | 0.78   |         0.584 |       0.734 | timesfm       |          16 | True               |
| clf_up_h168_q90  | linear  | val     | auc      | 0.786  |         0.635 |       0.735 | timesfm       |          16 | True               |
| clf_up_h1_q90    | gbdt    | oot     | auc      | 0.936  |         0.906 |       0.931 | timesfm       |          16 | True               |
| clf_up_h1_q90    | gbdt    | val     | auc      | 0.926  |         0.88  |       0.936 | timesfm       |          16 | True               |
| clf_up_h1_q90    | linear  | oot     | auc      | 0.892  |         0.862 |       0.911 | timesfm       |          16 | True               |
| clf_up_h1_q90    | linear  | val     | auc      | 0.881  |         0.853 |       0.88  | timesfm       |          16 | True               |
| clf_up_h24_q90   | gbdt    | oot     | auc      | 0.764  |         0.619 |       0.679 | diffusion_ts  |          16 | True               |
| clf_up_h24_q90   | gbdt    | val     | auc      | 0.739  |         0.611 |       0.655 | vae_greedy    |          16 | True               |
| clf_up_h24_q90   | linear  | oot     | auc      | 0.742  |         0.629 |       0.721 | timesfm       |          16 | True               |
| clf_up_h24_q90   | linear  | val     | auc      | 0.747  |         0.652 |       0.721 | timesfm       |          16 | True               |
| clf_up_h24_q90   | mlp     | oot     | auc      | 0.789  |         0.647 |       0.703 | timesfm       |          16 | True               |
| clf_up_h24_q90   | mlp     | val     | auc      | 0.757  |         0.644 |       0.717 | diffusion_ts  |          16 | True               |
| clf_up_h24_q95   | gbdt    | oot     | auc      | 0.732  |         0.636 |       0.677 | timesfm       |          16 | True               |
| clf_up_h24_q95   | gbdt    | val     | auc      | 0.751  |         0.625 |       0.671 | vae_greedy    |          16 | True               |
| clf_up_h24_q95   | linear  | oot     | auc      | 0.791  |         0.679 |       0.744 | timesfm       |          16 | True               |
| clf_up_h24_q95   | linear  | val     | auc      | 0.794  |         0.66  |       0.726 | vae_rand      |          16 | True               |
| clf_up_h24_q99   | gbdt    | oot     | auc      | 0.724  |         0.612 |       0.676 | vae_zseries   |          16 | True               |
| clf_up_h24_q99   | gbdt    | val     | auc      | 0.723  |         0.636 |       0.671 | vae_greedy    |          16 | True               |
| clf_up_h24_q99   | linear  | oot     | auc      | 0.869  |         0.643 |       0.724 | vae_rand      |          16 | True               |
| clf_up_h24_q99   | linear  | val     | auc      | 0.928  |         0.723 |       0.786 | vae_rand      |          16 | True               |
| clf_up_h6_q90    | gbdt    | oot     | auc      | 0.911  |         0.801 |       0.916 | timesfm       |          16 | True               |
| clf_up_h6_q90    | gbdt    | val     | auc      | 0.902  |         0.726 |       0.906 | timesfm       |          16 | True               |
| clf_up_h6_q90    | linear  | oot     | auc      | 0.863  |         0.693 |       0.89  | timesfm       |          16 | True               |
| clf_up_h6_q90    | linear  | val     | auc      | 0.775  |         0.713 |       0.882 | timesfm       |          16 | True               |
| mc3_h24          | gbdt    | oot     | logloss  | 0.672  |         0.968 |       0.896 | vae_herding   |          16 | False              |
| mc3_h24          | gbdt    | val     | logloss  | 0.507  |         0.932 |       0.791 | vae_herding   |          16 | False              |
| mc3_h24          | linear  | oot     | logloss  | 0.534  |         0.912 |       0.777 | vae_herding   |          16 | False              |
| mc3_h24          | linear  | val     | logloss  | 0.45   |         0.896 |       0.709 | vae_zseries   |          16 | False              |
| ms_h24           | gbdt    | oot     | mase     | 0.778  |         1.21  |       1.03  | vae_herding   |          16 | False              |
| ms_h24           | gbdt    | val     | mase     | 0.744  |         1.31  |       1.06  | chronos       |          16 | False              |
| ms_h24           | linear  | oot     | mase     | 0.638  |         0.931 |       0.76  | vae_herding   |          16 | False              |
| ms_h24           | linear  | val     | mase     | 0.562  |         0.974 |       0.798 | timestral     |          16 | False              |
| qreg_h24         | gbdt    | oot     | pinball  | 0.245  |         0.408 |       0.31  | timesfm       |          16 | False              |
| qreg_h24         | gbdt    | val     | pinball  | 0.262  |         0.498 |       0.339 | timesfm       |          16 | False              |
| qreg_h24         | linear  | oot     | pinball  | 0.249  |         0.347 |       0.279 | vae_herding   |          16 | False              |
| qreg_h24         | linear  | val     | pinball  | 0.186  |         0.298 |       0.239 | chronos       |          16 | False              |
| reg_h1           | gbdt    | oot     | mase     | 0.437  |         0.632 |       0.461 | timesfm       |          16 | False              |
| reg_h1           | gbdt    | val     | mase     | 0.385  |         0.644 |       0.527 | vae_greedy    |          16 | False              |
| reg_h1           | linear  | oot     | mase     | 0.151  |         0.168 |       0.153 | vae_rand      |          16 | False              |
| reg_h1           | linear  | val     | mase     | 0.155  |         0.184 |       0.175 | vae_zseries   |          16 | False              |
| reg_h168         | gbdt    | oot     | mase     | 1.02   |         1.77  |       0.952 | timestral     |          16 | False              |
| reg_h168         | gbdt    | val     | mase     | 1.01   |         1.84  |       0.957 | timestral     |          16 | False              |
| reg_h168         | linear  | oot     | mase     | 0.903  |         1.52  |       0.961 | timesfm       |          16 | False              |
| reg_h168         | linear  | val     | mase     | 0.859  |         1.52  |       0.881 | timesfm       |          16 | False              |
| reg_h24          | gbdt    | oot     | mase     | 0.796  |         1.17  |       0.795 | timesfm       |          16 | False              |
| reg_h24          | gbdt    | val     | mase     | 0.793  |         1.23  |       0.816 | timesfm       |          16 | False              |
| reg_h24          | linear  | oot     | mase     | 0.832  |         1.05  |       0.874 | timesfm       |          16 | False              |
| reg_h24          | linear  | val     | mase     | 0.581  |         0.969 |       0.573 | timestral     |          16 | False              |
| vol_h24          | gbdt    | oot     | mase     | 0.099  |         0.209 |       0.11  | vae_pctsp     |          16 | False              |
| vol_h24          | gbdt    | val     | mase     | 0.0809 |         0.201 |       0.116 | vae_pctsp     |          16 | False              |
| vol_h24          | linear  | oot     | mase     | 0.0879 |         0.184 |       0.114 | vae_pctsp     |          16 | False              |
| vol_h24          | linear  | val     | mase     | 0.0676 |         0.189 |       0.134 | timestral     |          16 | False              |
