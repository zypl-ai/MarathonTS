# Failure check — run_h200

Supplementary, not pre-specified (`python -m marathonts.hypotheses.failure_check`). Missing TSTR cells (task × model × split that a method's series could not train) and their reason: `one_class` — the labels of the synthetic series have one class (intrinsic); `no_rows` — no usable rows; `other` — two or more classes, the fit failed or was not run (recoverable).

Missing: 3462 of 156398 TSTR cells (2.21%).

By task kind:

| task_kind   |   cells |   missing |
|:------------|--------:|----------:|
| clf         |   80798 |      3090 |
| mc          |   10800 |       372 |
| ms          |   10800 |         0 |
| qreg        |   10800 |         0 |
| reg         |   32400 |         0 |
| vol         |   10800 |         0 |

By method and reason (`cells`: all TSTR cells of the method):

| method            |   one_class |   cells |
|:------------------|------------:|--------:|
| chronos           |         558 |    5190 |
| diffusion_ts      |         112 |    5200 |
| timesfm           |        1140 |    5160 |
| timestral         |        1620 |    5160 |
| vae_atsp          |           6 |    5214 |
| vae_greedy        |           4 |    5216 |
| vae_knn           |           2 |    5218 |
| vae_pctsp         |           6 |    5214 |
| vae_quilting      |           6 |    5214 |
| vae_zseries_quilt |           2 |    5218 |
| vae_zseries_wsola |           2 |    5218 |
| vae_zseries_xfade |           4 |    5216 |

By task and reason:

| task             |   one_class |
|:-----------------|------------:|
| clf_down_h24_q10 |         468 |
| clf_up_h168_q90  |         592 |
| clf_up_h1_q90    |         188 |
| clf_up_h24_q90   |         576 |
| clf_up_h24_q95   |         464 |
| clf_up_h24_q99   |         602 |
| clf_up_h6_q90    |         200 |
| mc3_h24          |         372 |
