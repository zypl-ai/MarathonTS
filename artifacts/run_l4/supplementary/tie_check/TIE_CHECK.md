# Tie check — run_l4

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

Pairs of methods compared within a block: 543960; tied (within the noise): 146111 (26.9%); not tied but linked by a method tied with both: 55976 (10.3%).

## Against ordinary ranks

Kendall's tau between the mean ranks: 0.949. Methods whose place or tier membership differs:

| method     |   mean_rank |   place | top_tier   |   mean_rank_plain |   place_plain | top_tier_plain   |
|:-----------|------------:|--------:|:-----------|------------------:|--------------:|:-----------------|
| vae_mbb    |        7.22 |    8.00 | True       |              7.28 |          9.00 | True             |
| vae_pctsp  |        7.23 |    9.00 | True       |              7.26 |          8.00 | True             |
| vae_knn    |        7.56 |   11.00 | True       |              7.67 |         12.00 | True             |
| vae_greedy |        7.60 |   12.00 | False      |              7.66 |         11.00 | False            |

All methods:

| method       |   mean_rank |   place | top_tier   |   mean_rank_plain |   place_plain | top_tier_plain   |
|:-------------|------------:|--------:|:-----------|------------------:|--------------:|:-----------------|
| vae_herding  |        5.54 |    1.00 | True       |              5.42 |          1.00 | True             |
| diffusion_ts |        6.27 |    2.00 | True       |              6.19 |          2.00 | True             |
| vae_quilting |        6.36 |    3.00 | True       |              6.26 |          3.00 | True             |
| vae_zseries  |        6.41 |    4.00 | True       |              6.36 |          4.00 | True             |
| timesfm      |        6.72 |    5.00 | True       |              6.61 |          5.00 | True             |
| vae_atsp     |        7.11 |    6.00 | True       |              7.17 |          6.00 | True             |
| vae_rand     |        7.20 |    7.00 | True       |              7.26 |          7.00 | True             |
| vae_mbb      |        7.22 |    8.00 | True       |              7.28 |          9.00 | True             |
| vae_pctsp    |        7.23 |    9.00 | True       |              7.26 |          8.00 | True             |
| chronos      |        7.43 |   10.00 | True       |              7.42 |         10.00 | True             |
| vae_knn      |        7.56 |   11.00 | True       |              7.67 |         12.00 | True             |
| vae_greedy   |        7.60 |   12.00 | False      |              7.66 |         11.00 | False            |
| timestral    |        8.56 |   13.00 | False      |              8.58 |         13.00 | False            |
