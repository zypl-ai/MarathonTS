# Pool check — run_h200

Supplementary, not pre-specified (`python -m marathonts.hypotheses.pool_check`). Value channel, scaled with the bounds of train ([0, 1]). `exact_half`: values exactly 0.5 (upper bound of NaN replaced by 0.5); `nan_windows`: windows that are 0.5 everywhere; `at_0`, `at_1`: shares at the bounds; `flat_share`: share of windows with a standard deviation below 0.01.

Pools: all 9 datasets of the main run. The pools of ETT and PJM are not redistributed (licences, `hf_card/LICENSES.md`), so on the published data the check covers the other 7 datasets; the rows of ETT and PJM come from the run's delivery (kept by the authors).

|                              |   seeds |   windows |   exact_half |   nan_windows |      at_0 |      at_1 |       min |    max |   window_std_median |   flat_share |
|:-----------------------------|--------:|----------:|-------------:|--------------:|----------:|----------:|----------:|-------:|--------------------:|-------------:|
| ('tsgm_vae', 'beijing_pm25') |      10 |      3000 |            0 |             0 | 0         | 0         | 0.002949  | 0.9088 |             0.145   |      0       |
| ('tsgm_vae', 'bike')         |      10 |      3000 |            0 |             0 | 0         | 0         | 0.0002708 | 0.8155 |             0.175   |      0.03133 |
| ('tsgm_vae', 'bitcoin')      |      10 |      3000 |            0 |             0 | 0         | 0         | 0.03116   | 0.9162 |             0.0438  |      0.03067 |
| ('tsgm_vae', 'electricity')  |      10 |      3000 |            0 |             0 | 0         | 0         | 0.257     | 0.8734 |             0.1702  |      0       |
| ('tsgm_vae', 'ett')          |      10 |      3000 |            0 |             0 | 0         | 0         | 0.08845   | 0.8016 |             0.05725 |      0       |
| ('tsgm_vae', 'household')    |      10 |      3000 |            0 |             0 | 0         | 0         | 0.006374  | 0.8713 |             0.2101  |      0       |
| ('tsgm_vae', 'jena')         |      10 |      3000 |            0 |             0 | 0         | 0         | 0.1169    | 0.9004 |             0.09388 |      0       |
| ('tsgm_vae', 'metro')        |      10 |      3000 |            0 |             0 | 0         | 0         | 0.007646  | 0.9594 |             0.2522  |      0       |
| ('tsgm_vae', 'pjm')          |      10 |      3000 |            0 |             0 | 0         | 0         | 0.04336   | 0.9824 |             0.187   |      0       |
| ('zedge_ts', 'beijing_pm25') |      10 |      3000 |            0 |             0 | 0.000252  | 0.000254  | 0         | 1      |             0.1172  |      0       |
| ('zedge_ts', 'bike')         |      10 |      3000 |            0 |             0 | 0.005599  | 0.0001448 | 0         | 1      |             0.139   |      0       |
| ('zedge_ts', 'bitcoin')      |      10 |      3000 |            0 |             0 | 1.786e-05 | 0.0001925 | 0         | 1      |             0.02592 |      0.032   |
| ('zedge_ts', 'electricity')  |      10 |      3000 |            0 |             0 | 0.0001627 | 0.0001885 | 0         | 1      |             0.1641  |      0       |
| ('zedge_ts', 'ett')          |      10 |      3000 |            1 |             0 | 0         | 0.0002361 | 0.09571   | 1      |             0.08684 |      0       |
| ('zedge_ts', 'household')    |      10 |      3000 |            0 |             0 | 0.002575  | 0.0001349 | 0         | 1      |             0.173   |      0       |
| ('zedge_ts', 'jena')         |      10 |      3000 |            1 |             0 | 9.921e-05 | 0         | 0         | 0.8435 |             0.07172 |      0       |
| ('zedge_ts', 'metro')        |      10 |      3000 |            0 |             0 | 0.0002937 | 0.0002956 | 0         | 1      |             0.2838  |      0       |
| ('zedge_ts', 'pjm')          |      10 |      3000 |            0 |             0 | 0.0001885 | 6.746e-05 | 0         | 1      |             0.1463  |      0       |
