# Failure check — run_l4

Supplementary, not pre-specified (`python -m marathonts.hypotheses.failure_check`). Missing TSTR cells (task × model × split that a method's series could not train) and their reason: `one_class` — the labels of the synthetic series have one class (intrinsic); `no_rows` — no usable rows; `other` — two or more classes, the fit failed or was not run (recoverable).

Missing: 3636 of 83288 TSTR cells (4.37%).

By task kind:

| task_kind   |   cells |   missing |
|:------------|--------:|----------:|
| clf         |   42968 |      3248 |
| mc          |    5760 |       388 |
| ms          |    5760 |         0 |
| qreg        |    5760 |         0 |
| reg         |   17280 |         0 |
| vol         |    5760 |         0 |

By method and reason (`cells`: all TSTR cells of the method):

| method            |   one_class |   cells |
|:------------------|------------:|--------:|
| chronos           |         648 |    5188 |
| diffusion_ts      |         168 |    5200 |
| timesfm           |        1140 |    5160 |
| timestral         |        1620 |    5160 |
| vae_atsp          |          10 |    5210 |
| vae_greedy        |          14 |    5206 |
| vae_knn           |           8 |    5212 |
| vae_pctsp         |          12 |    5208 |
| vae_quilting      |           8 |    5212 |
| vae_zseries       |           2 |    5218 |
| vae_zseries_quilt |           4 |    5216 |
| vae_zseries_xfade |           2 |    5218 |

By task and reason:

| task             |   one_class |
|:-----------------|------------:|
| clf_down_h24_q10 |         476 |
| clf_up_h168_q90  |         620 |
| clf_up_h1_q90    |         200 |
| clf_up_h24_q90   |         600 |
| clf_up_h24_q95   |         460 |
| clf_up_h24_q99   |         652 |
| clf_up_h6_q90    |         240 |
| mc3_h24          |         388 |
