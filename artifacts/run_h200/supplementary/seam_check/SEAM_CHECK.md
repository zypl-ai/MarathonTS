# Seam check — run_h200

Supplementary, not pre-specified (`python -m marathonts.hypotheses.seam_check`). See the module docstring.

Series: 2700; F5.6 recomputed equals the published value in 2355 of 2355 series with both defined (largest difference 2.6e-08).

Across methods, Spearman correlation between the median F5.6 and the median exposed share: 0.08. Kendall's tau between the order of the methods by F5.6 and by the chance-adjusted lift: 0.81.

Medians per method (sorted by F5.6; `lift_defined`: series with a seam and a change point):

| method              |   series |   seams |   exposed |   change_points |      f56 |   f56_null |   f56_lift |   lift_defined |
|:--------------------|---------:|--------:|----------:|----------------:|---------:|-----------:|-----------:|---------------:|
| timestral           |       90 |       4 |   0.00556 |            10   |   0      |    0.00538 |      0     |             66 |
| vae_zseries         |       90 |      29 |   0.0403  |            86.5 |   0.0222 |    0.0399  |      0.568 |             87 |
| zedge_zseries       |       90 |      29 |   0.0403  |            74.5 |   0.024  |    0.0396  |      0.605 |             75 |
| vae_pctsp           |       90 |      29 |   0.0403  |           120   |   0.0267 |    0.0401  |      0.668 |             88 |
| vae_atsp            |       90 |      29 |   0.0403  |           113   |   0.0277 |    0.0404  |      0.669 |             90 |
| zedge_ts_ar         |       90 |      58 |   0.0806  |            76.5 |   0.0291 |    0.0805  |      0.38  |             81 |
| vae_greedy          |       90 |      29 |   0.0403  |           115   |   0.0292 |    0.0399  |      0.725 |             90 |
| diffusion_ts        |       90 |      58 |   0.0806  |            41   |   0.0358 |    0.08    |      0.447 |             70 |
| vae_quilting        |       90 |      32 |   0.0444  |           122   |   0.041  |    0.0448  |      0.926 |             90 |
| zedge_atsp          |       90 |      29 |   0.0403  |            78   |   0.0446 |    0.04    |      1.15  |             80 |
| zedge_pctsp         |       90 |      29 |   0.0403  |            77   |   0.0451 |    0.0401  |      1.15  |             78 |
| zedge_quilting      |       90 |      32 |   0.0444  |            74.5 |   0.0455 |    0.0444  |      1.02  |             81 |
| vae_knn             |       90 |      29 |   0.0403  |           118   |   0.0489 |    0.0395  |      1.18  |             90 |
| vae_zseries_quilt   |       90 |      32 |   0.0444  |            97.5 |   0.0508 |    0.0445  |      1.16  |             90 |
| vae_zseries_xfade   |       90 |      32 |   0.0444  |            96   |   0.0529 |    0.0441  |      1.13  |             88 |
| zedge_zseries_quilt |       90 |      32 |   0.0444  |            80   |   0.0551 |    0.0443  |      1.27  |             74 |
| zedge_ts_long       |       90 |      58 |   0.0806  |            68.5 |   0.0551 |    0.0792  |      0.695 |             80 |
| zedge_zseries_xfade |       90 |      32 |   0.0444  |            80.5 |   0.0585 |    0.0439  |      1.34  |             74 |
| zedge_greedy        |       90 |      29 |   0.0403  |            75.5 |   0.0619 |    0.0393  |      1.56  |             80 |
| vae_zseries_wsola   |       90 |      33 |   0.0458  |           102   |   0.0812 |    0.0457  |      1.75  |             88 |
| zedge_knn           |       90 |      29 |   0.0403  |            74.5 |   0.0814 |    0.0394  |      2     |             81 |
| zedge_zseries_wsola |       90 |      33 |   0.0458  |            84   |   0.0857 |    0.0461  |      1.87  |             71 |
| chronos             |       90 |      78 |   0.108   |            36   |   0.0914 |    0.109   |      0.826 |             82 |
| vae_mbb             |       90 |      29 |   0.0403  |           109   |   0.0947 |    0.0399  |      2.49  |             89 |
| vae_rand            |       90 |      29 |   0.0403  |           110   |   0.1    |    0.0395  |      2.51  |             90 |
| vae_herding         |       90 |      29 |   0.0403  |            77   |   0.105  |    0.0394  |      2.65  |             84 |
| zedge_mbb           |       90 |      29 |   0.0403  |            53.5 |   0.14   |    0.0391  |      3.15  |             79 |
| zedge_herding       |       90 |      29 |   0.0403  |            48   |   0.142  |    0.0389  |      3.67  |             78 |
| zedge_rand          |       90 |      29 |   0.0403  |            52.5 |   0.151  |    0.0387  |      3.89  |             77 |
| timesfm             |       90 |       0 |   0       |            16   | nan      |  nan       |    nan     |              0 |
