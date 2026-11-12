# Pool check — run_l4

Supplementary, not pre-specified (`python -m marathonts.hypotheses.pool_check`). Value channel, scaled with the bounds of train ([0, 1]). `exact_half`: values exactly 0.5 (upper bound of NaN replaced by 0.5); `nan_windows`: windows that are 0.5 everywhere; `at_0`, `at_1`: shares at the bounds; `flat_share`: share of windows with a standard deviation below 0.01.

|                              |   seeds |   windows |   exact_half |   nan_windows |   at_0 |   at_1 |       min |    max |   window_std_median |   flat_share |
|:-----------------------------|--------:|----------:|-------------:|--------------:|-------:|-------:|----------:|-------:|--------------------:|-------------:|
| ('tsgm_vae', 'beijing_pm25') |      10 |      3000 |            0 |             0 |      0 |      0 | 0.001408  | 0.9415 |             0.1238  |        0     |
| ('tsgm_vae', 'bike')         |      10 |      3000 |            0 |             0 |      0 |      0 | 0.001186  | 0.9462 |             0.2006  |        0     |
| ('tsgm_vae', 'bitcoin')      |      10 |      3000 |            0 |             0 |      0 |      0 | 0.02434   | 0.8435 |             0.04689 |        0.102 |
| ('tsgm_vae', 'electricity')  |      10 |      3000 |            0 |             0 |      0 |      0 | 0.2375    | 0.8931 |             0.1723  |        0     |
| ('tsgm_vae', 'ett')          |      10 |      3000 |            0 |             0 |      0 |      0 | 0.08779   | 0.8443 |             0.0557  |        0     |
| ('tsgm_vae', 'household')    |      10 |      3000 |            0 |             0 |      0 |      0 | 0.0008324 | 0.8576 |             0.1329  |        0     |
| ('tsgm_vae', 'jena')         |      10 |      3000 |            0 |             0 |      0 |      0 | 0.1026    | 0.9227 |             0.0878  |        0     |
| ('tsgm_vae', 'metro')        |      10 |      3000 |            0 |             0 |      0 |      0 | 0.005093  | 0.9589 |             0.268   |        0     |
| ('tsgm_vae', 'pjm')          |      10 |      3000 |            0 |             0 |      0 |      0 | 0.06315   | 0.9883 |             0.181   |        0     |
