# Calendar check — run_h200

Supplementary, not pre-specified (`python -m marathonts.hypotheses.calendar_check`). Medians over datasets and seeds. `step_one`: share of steps at which the hour of the week advances by exactly one (F4.4). `err_*`: error of the hour of the week inside a piece (between two seams) against the closest valid calendar, in hours (`err_max`: the largest over all series); `share_err_ge3`: share of steps with an error of 3 hours or more.

| method              |   datasets |   series |   step_one |   err_median |   err_p90 |   err_max |   share_err_ge3 |
|:--------------------|-----------:|---------:|-----------:|-------------:|----------:|----------:|----------------:|
| vae_mbb             |          9 |       90 |      0.68  |            1 |       5   |        84 |          0.204  |
| vae_rand            |          9 |       90 |      0.683 |            1 |       4   |        84 |          0.181  |
| vae_knn             |          9 |       90 |      0.7   |            1 |       4   |        84 |          0.167  |
| vae_greedy          |          9 |       90 |      0.717 |            1 |       3   |        84 |          0.147  |
| vae_pctsp           |          9 |       90 |      0.738 |            1 |       2.5 |        84 |          0.101  |
| vae_quilting        |          9 |       90 |      0.739 |            1 |       3   |        84 |          0.132  |
| vae_atsp            |          9 |       90 |      0.746 |            1 |       2   |        79 |          0.0985 |
| vae_herding         |          9 |       90 |      0.764 |            1 |       2   |        84 |          0.073  |
| vae_zseries         |          9 |       90 |      0.779 |            1 |       2   |        25 |          0.0327 |
| vae_zseries_wsola   |          9 |       90 |      0.783 |            1 |       2   |        44 |          0.0715 |
| vae_zseries_xfade   |          9 |       90 |      0.783 |            1 |       2   |        40 |          0.0674 |
| vae_zseries_quilt   |          9 |       90 |      0.788 |            1 |       2   |        23 |          0.0309 |
| zedge_zseries_wsola |          9 |       90 |      0.993 |            0 |       0   |        47 |          0.0393 |
| zedge_zseries_quilt |          9 |       90 |      0.994 |            0 |       0   |         0 |          0      |
| zedge_zseries_xfade |          9 |       90 |      0.994 |            0 |       0   |        35 |          0.0381 |
| zedge_quilting      |          9 |       90 |      0.994 |            0 |       0   |         0 |          0      |
| zedge_herding       |          9 |       90 |      0.994 |            0 |       0   |         0 |          0      |
| zedge_mbb           |          9 |       90 |      0.994 |            0 |       0   |         0 |          0      |
| zedge_rand          |          9 |       90 |      0.994 |            0 |       0   |         0 |          0      |
| zedge_knn           |          9 |       90 |      0.995 |            0 |       0   |         0 |          0      |
| zedge_zseries       |          9 |       90 |      0.995 |            0 |       0   |         0 |          0      |
| zedge_greedy        |          9 |       90 |      0.995 |            0 |       0   |         0 |          0      |
| zedge_atsp          |          9 |       90 |      0.995 |            0 |       0   |         0 |          0      |
| zedge_pctsp         |          9 |       90 |      0.995 |            0 |       0   |         0 |          0      |
| timesfm             |          9 |       90 |      1     |            0 |       0   |         0 |          0      |
| zedge_ts_ar         |          9 |       90 |      1     |            0 |       0   |         0 |          0      |
| zedge_ts_long       |          9 |       90 |      1     |            0 |       0   |         0 |          0      |
| diffusion_ts        |          9 |       90 |      1     |            0 |       0   |         0 |          0      |
| timestral           |          9 |       90 |      1     |            0 |       0   |         0 |          0      |
| chronos             |          9 |       90 |      1     |            0 |       0   |         0 |          0      |
