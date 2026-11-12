# Seam check — run_l4

Supplementary, not pre-specified (`python -m marathonts.hypotheses.seam_check`). See the module docstring.

Series: 1440; F5.6 recomputed equals the published value in 1199 of 1199 series with both defined (largest difference 1.5e-08).

Across methods, Spearman correlation between the median F5.6 and the median exposed share: 0.23. Kendall's tau between the order of the methods by F5.6 and by the chance-adjusted lift: 0.81.

Medians per method (sorted by F5.6; `lift_defined`: series with a seam and a change point):

| method            |   series |   seams |   exposed |   change_points |      f56 |   f56_null |   f56_lift |   lift_defined |
|:------------------|---------:|--------:|----------:|----------------:|---------:|-----------:|-----------:|---------------:|
| timestral         |       90 |       4 |   0.00556 |            10   |   0      |    0.00538 |      0     |             66 |
| vae_zseries       |       90 |      29 |   0.0403  |            88   |   0.0308 |    0.0398  |      0.716 |             81 |
| vae_greedy        |       90 |      29 |   0.0403  |            96.5 |   0.0364 |    0.0402  |      0.875 |             86 |
| diffusion_ts      |       90 |      58 |   0.0806  |            42   |   0.0377 |    0.0785  |      0.494 |             65 |
| vae_pctsp         |       90 |      29 |   0.0403  |           103   |   0.0411 |    0.0402  |      0.998 |             85 |
| vae_atsp          |       90 |      29 |   0.0403  |           105   |   0.0421 |    0.0396  |      1.05  |             86 |
| vae_quilting      |       90 |      32 |   0.0444  |           122   |   0.0458 |    0.0443  |      1.06  |             85 |
| vae_zseries_quilt |       90 |      32 |   0.0444  |           101   |   0.05   |    0.0449  |      1.07  |             87 |
| vae_zseries_xfade |       90 |      32 |   0.0444  |           108   |   0.0524 |    0.044   |      1.16  |             82 |
| vae_knn           |       90 |      29 |   0.0403  |           111   |   0.0533 |    0.04    |      1.3   |             86 |
| vae_zseries_wsola |       90 |      33 |   0.0458  |           108   |   0.0642 |    0.046   |      1.35  |             81 |
| chronos           |       90 |      78 |   0.108   |            56.5 |   0.0894 |    0.108   |      0.822 |             78 |
| vae_mbb           |       90 |      29 |   0.0403  |            94.5 |   0.0917 |    0.0397  |      2.3   |             83 |
| vae_rand          |       90 |      29 |   0.0403  |            89   |   0.0952 |    0.0394  |      2.51  |             83 |
| vae_herding       |       90 |      29 |   0.0403  |            76.5 |   0.114  |    0.0392  |      2.77  |             80 |
| timesfm           |       90 |       0 |   0       |            16   | nan      |  nan       |    nan     |              0 |
