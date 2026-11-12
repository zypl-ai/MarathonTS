# Calendar check — run_l4

Supplementary, not pre-specified (`python -m marathonts.hypotheses.calendar_check`). Medians over datasets and seeds. `step_one`: share of steps at which the hour of the week advances by exactly one (F4.4). `err_*`: error of the hour of the week inside a piece (between two seams) against the closest valid calendar, in hours (`err_max`: the largest over all series); `share_err_ge3`: share of steps with an error of 3 hours or more.

| method            |   datasets |   series |   step_one |   err_median |   err_p90 |   err_max |   share_err_ge3 |
|:------------------|-----------:|---------:|-----------:|-------------:|----------:|----------:|----------------:|
| vae_rand          |          9 |       90 |      0.676 |            1 |       5   |        84 |          0.195  |
| vae_greedy        |          9 |       90 |      0.676 |            1 |       4   |        84 |          0.164  |
| vae_mbb           |          9 |       90 |      0.687 |            1 |       5   |        84 |          0.19   |
| vae_herding       |          9 |       90 |      0.693 |            1 |       6   |        84 |          0.164  |
| vae_quilting      |          9 |       90 |      0.697 |            1 |       3.5 |        84 |          0.16   |
| vae_knn           |          9 |       90 |      0.702 |            1 |       4   |        84 |          0.174  |
| vae_pctsp         |          9 |       90 |      0.751 |            1 |       2   |        84 |          0.0931 |
| vae_atsp          |          9 |       90 |      0.753 |            1 |       3   |        84 |          0.124  |
| vae_zseries_wsola |          9 |       90 |      0.774 |            1 |       2.5 |        84 |          0.1    |
| vae_zseries       |          9 |       90 |      0.775 |            1 |       2   |        83 |          0.0676 |
| vae_zseries_xfade |          9 |       90 |      0.78  |            1 |       3   |        74 |          0.101  |
| vae_zseries_quilt |          9 |       90 |      0.781 |            1 |       2   |        75 |          0.0641 |
| chronos           |          9 |       90 |      1     |            0 |       0   |         0 |          0      |
| diffusion_ts      |          9 |       90 |      1     |            0 |       0   |         0 |          0      |
| timesfm           |          9 |       90 |      1     |            0 |       0   |         0 |          0      |
| timestral         |          9 |       90 |      1     |            0 |       0   |         0 |          0      |
