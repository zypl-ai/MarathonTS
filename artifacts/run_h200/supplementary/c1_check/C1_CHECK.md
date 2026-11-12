# C1 check — run_h200

Supplementary, not pre-specified (`python -m marathonts.hypotheses.c1_check`). See the module docstring.

## Eligibility

Ranked methods that do not enter C1 (every one of their cells is out; `leaked`: datasets left out for leakage):

| cell                      | method   |   datasets_without_value |   leaked |
|:--------------------------|:---------|-------------------------:|---------:|
| clf_up_h24_q90|linear|oot | chronos  |                        2 |        2 |
| clf_up_h24_q90|linear|oot | timesfm  |                        3 |        3 |
| reg_h24|linear|oot        | chronos  |                        2 |        2 |
| reg_h24|linear|oot        | timesfm  |                        3 |        3 |

Methods of each test:

| cell                      | variant                                    | methods                                                                                                                                                                                                                                                                                           |
|:--------------------------|:-------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| clf_up_h24_q90|linear|oot | pre-specified: complete methods            | diffusion_ts, timestral, vae_atsp, vae_greedy, vae_herding, vae_knn, vae_mbb, vae_pctsp, vae_quilting, vae_rand, vae_zseries, zedge_atsp, zedge_greedy, zedge_herding, zedge_knn, zedge_mbb, zedge_pctsp, zedge_quilting, zedge_rand, zedge_ts_ar, zedge_ts_long, zedge_zseries                   |
| clf_up_h24_q90|linear|oot | (a) every ranked method, incomplete blocks | chronos, diffusion_ts, timesfm, timestral, vae_atsp, vae_greedy, vae_herding, vae_knn, vae_mbb, vae_pctsp, vae_quilting, vae_rand, vae_zseries, zedge_atsp, zedge_greedy, zedge_herding, zedge_knn, zedge_mbb, zedge_pctsp, zedge_quilting, zedge_rand, zedge_ts_ar, zedge_ts_long, zedge_zseries |
| clf_up_h24_q90|linear|oot | (b) every ranked method, complete datasets | chronos, diffusion_ts, timesfm, timestral, vae_atsp, vae_greedy, vae_herding, vae_knn, vae_mbb, vae_pctsp, vae_quilting, vae_rand, vae_zseries, zedge_atsp, zedge_greedy, zedge_herding, zedge_knn, zedge_mbb, zedge_pctsp, zedge_quilting, zedge_rand, zedge_ts_ar, zedge_ts_long, zedge_zseries |
| clf_up_h24_q90|linear|oot | (c) methods of run_l4                      | diffusion_ts, timestral, vae_atsp, vae_greedy, vae_herding, vae_knn, vae_mbb, vae_pctsp, vae_quilting, vae_rand, vae_zseries                                                                                                                                                                      |
| reg_h24|linear|oot        | pre-specified: complete methods            | diffusion_ts, timestral, vae_atsp, vae_greedy, vae_herding, vae_knn, vae_mbb, vae_pctsp, vae_quilting, vae_rand, vae_zseries, zedge_atsp, zedge_greedy, zedge_herding, zedge_knn, zedge_mbb, zedge_pctsp, zedge_quilting, zedge_rand, zedge_ts_ar, zedge_ts_long, zedge_zseries                   |
| reg_h24|linear|oot        | (a) every ranked method, incomplete blocks | chronos, diffusion_ts, timesfm, timestral, vae_atsp, vae_greedy, vae_herding, vae_knn, vae_mbb, vae_pctsp, vae_quilting, vae_rand, vae_zseries, zedge_atsp, zedge_greedy, zedge_herding, zedge_knn, zedge_mbb, zedge_pctsp, zedge_quilting, zedge_rand, zedge_ts_ar, zedge_ts_long, zedge_zseries |
| reg_h24|linear|oot        | (b) every ranked method, complete datasets | chronos, diffusion_ts, timesfm, timestral, vae_atsp, vae_greedy, vae_herding, vae_knn, vae_mbb, vae_pctsp, vae_quilting, vae_rand, vae_zseries, zedge_atsp, zedge_greedy, zedge_herding, zedge_knn, zedge_mbb, zedge_pctsp, zedge_quilting, zedge_rand, zedge_ts_ar, zedge_ts_long, zedge_zseries |
| reg_h24|linear|oot        | (c) methods of run_l4                      | diffusion_ts, timestral, vae_atsp, vae_greedy, vae_herding, vae_knn, vae_mbb, vae_pctsp, vae_quilting, vae_rand, vae_zseries                                                                                                                                                                      |

## Tests

Permutations: 100000 (Skillings-Mack: 5000). Check: on a complete design Skillings-Mack equals Friedman without the tie correction (difference 1.4e-14).

| cell                      | variant                                    | test           |   n_datasets |   n_methods |   missing_cells |   statistic |   p_chi2 |   p_perm |
|:--------------------------|:-------------------------------------------|:---------------|-------------:|------------:|----------------:|------------:|---------:|---------:|
| clf_up_h24_q90|linear|oot | pre-specified: complete methods            | friedman       |            9 |          22 |               0 |       45.8  | 0.00138  |  0.00055 |
| clf_up_h24_q90|linear|oot | (a) every ranked method, incomplete blocks | skillings_mack |            9 |          24 |               5 |       46.6  | 0.00254  |  0.0012  |
| clf_up_h24_q90|linear|oot | (b) every ranked method, complete datasets | friedman       |            5 |          24 |               0 |       48.4  | 0.0015   |  0.00015 |
| clf_up_h24_q90|linear|oot | (c) methods of run_l4                      | friedman       |            9 |          11 |               0 |        6.26 | 0.793    |  0.809   |
| reg_h24|linear|oot        | pre-specified: complete methods            | friedman       |            9 |          22 |               0 |       78.6  | 1.4e-08  |  1e-05   |
| reg_h24|linear|oot        | (a) every ranked method, incomplete blocks | skillings_mack |            9 |          24 |               5 |       85.8  | 3.56e-09 |  0.0002  |
| reg_h24|linear|oot        | (b) every ranked method, complete datasets | friedman       |            5 |          24 |               0 |       47.8  | 0.00179  |  0.00031 |
| reg_h24|linear|oot        | (c) methods of run_l4                      | friedman       |            9 |          11 |               0 |       34.2  | 0.000171 |  3e-05   |

## Holm over the confirmatory family with the permutation p of C1

| test                | cell                      | comparison                           |   p_holm |   p_holm_perm | verdict      |
|:--------------------|:--------------------------|:-------------------------------------|---------:|--------------:|:-------------|
| C1 methods differ   | clf_up_h24_q90|linear|oot | Friedman, all methods                |  0.0124  |       0.00495 | differ       |
| C2 long vs assembly | clf_up_h24_q90|linear|oot | diffusion_ts vs assembly_median      |  0.492   |       0.492   | inconclusive |
| C2 long vs assembly | clf_up_h24_q90|linear|oot | chronos vs assembly_median           |  1       |       1       | inconclusive |
| C3 selection        | clf_up_h24_q90|linear|oot | optimised selection (mean) vs random |  1       |       1       | inconclusive |
| C4 seam processing  | clf_up_h24_q90|linear|oot | any joiner vs none (all paths)       |  0.137   |       0.137   | inconclusive |
| C1 methods differ   | reg_h24|linear|oot        | Friedman, all methods                |  1.4e-07 |       0.0001  | differ       |
| C2 long vs assembly | reg_h24|linear|oot        | diffusion_ts vs assembly_median      |  0.273   |       0.273   | inconclusive |
| C2 long vs assembly | reg_h24|linear|oot        | chronos vs assembly_median           |  0.188   |       0.188   | inconclusive |
| C3 selection        | reg_h24|linear|oot        | optimised selection (mean) vs random |  0.391   |       0.391   | inconclusive |
| C4 seam processing  | reg_h24|linear|oot        | any joiner vs none (all paths)       |  0.0312  |       0.0312  | inconclusive |
