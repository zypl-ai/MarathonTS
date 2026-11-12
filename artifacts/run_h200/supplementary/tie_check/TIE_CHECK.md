# Tie check — run_h200

Supplementary, not pre-specified (`python -m marathonts.hypotheses.tie_check`). Noise-aware ranks of the overall leaderboard (`overall.rank_noise`, see the module docstring).

## Worked example

Scores 1.2 (A), 0.6 (B), 0.0 (C), noise 1: A ties B, B ties C, but A beats C. A: 1 + 0 + ½·1 = 1.5; B: 1 + 0 + ½·2 = 2; C: 1 + 1 + ½·1 = 2.5.

| method   |   score (higher is better) |   noise-aware rank |   ordinary rank |
|:---------|---------------------------:|-------------------:|----------------:|
| A        |                        1.2 |                1.5 |               1 |
| B        |                        0.6 |                2   |               2 |
| C        |                        0   |                2.5 |               3 |

## Order invariance

Ranks recomputed with the methods renamed so that they come in another order: largest difference 0.

## Non-transitive ties

Pairs of methods compared within a block: 2013010; tied (within the noise): 572781 (28.5%); not tied but linked by a method tied with both: 234747 (11.7%).

## Against ordinary ranks

Kendall's tau between the mean ranks: 0.971. Methods whose place or tier membership differs:

| method        |   mean_rank |   place | top_tier   |   mean_rank_plain |   place_plain | top_tier_plain   |
|:--------------|------------:|--------:|:-----------|------------------:|--------------:|:-----------------|
| zedge_knn     |        9.33 |    5.00 | True       |              9.22 |          8.00 | True             |
| zedge_ts_ar   |        9.40 |    7.00 | True       |              8.89 |          5.00 | True             |
| zedge_ts_long |        9.50 |    8.00 | True       |              9.21 |          7.00 | True             |
| zedge_rand    |       10.75 |   11.00 | True       |             10.85 |         11.00 | False            |

All methods:

| method         |   mean_rank |   place | top_tier   |   mean_rank_plain |   place_plain | top_tier_plain   |
|:---------------|------------:|--------:|:-----------|------------------:|--------------:|:-----------------|
| zedge_quilting |        8.27 |    1.00 | True       |              7.83 |          1.00 | True             |
| zedge_zseries  |        8.79 |    2.00 | True       |              8.55 |          2.00 | True             |
| zedge_greedy   |        8.95 |    3.00 | True       |              8.75 |          3.00 | True             |
| zedge_pctsp    |        9.18 |    4.00 | True       |              8.89 |          4.00 | True             |
| zedge_knn      |        9.33 |    5.00 | True       |              9.22 |          8.00 | True             |
| zedge_atsp     |        9.39 |    6.00 | True       |              9.10 |          6.00 | True             |
| zedge_ts_ar    |        9.40 |    7.00 | True       |              8.89 |          5.00 | True             |
| zedge_ts_long  |        9.50 |    8.00 | True       |              9.21 |          7.00 | True             |
| zedge_herding  |       10.48 |    9.00 | True       |             10.50 |          9.00 | True             |
| zedge_mbb      |       10.58 |   10.00 | True       |             10.69 |         10.00 | True             |
| zedge_rand     |       10.75 |   11.00 | True       |             10.85 |         11.00 | False            |
| vae_herding    |       13.53 |   12.00 | False      |             13.82 |         12.00 | False            |
| vae_zseries    |       13.68 |   13.00 | True       |             13.82 |         13.00 | True             |
| diffusion_ts   |       13.78 |   14.00 | False      |             13.86 |         14.00 | False            |
| timesfm        |       14.43 |   15.00 | True       |             14.39 |         15.00 | True             |
| vae_quilting   |       14.44 |   16.00 | True       |             14.46 |         16.00 | True             |
| vae_pctsp      |       15.27 |   17.00 | False      |             15.43 |         17.00 | False            |
| vae_atsp       |       15.28 |   18.00 | False      |             15.51 |         18.00 | False            |
| vae_greedy     |       15.57 |   19.00 | False      |             15.78 |         19.00 | False            |
| chronos        |       15.78 |   20.00 | True       |             15.85 |         20.00 | True             |
| vae_knn        |       16.01 |   21.00 | False      |             16.31 |         21.00 | False            |
| vae_mbb        |       16.30 |   22.00 | False      |             16.61 |         22.00 | False            |
| vae_rand       |       16.47 |   23.00 | False      |             16.72 |         23.00 | False            |
| timestral      |       16.77 |   24.00 | False      |             16.86 |         24.00 | False            |
