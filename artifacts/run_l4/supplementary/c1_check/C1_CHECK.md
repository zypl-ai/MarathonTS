# C1 check — run_l4

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

| cell                      | variant                                    | methods                                                                                                                                        |
|:--------------------------|:-------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------|
| clf_up_h24_q90|linear|oot | pre-specified: complete methods            | diffusion_ts, timestral, vae_atsp, vae_greedy, vae_herding, vae_knn, vae_mbb, vae_pctsp, vae_quilting, vae_rand, vae_zseries                   |
| clf_up_h24_q90|linear|oot | (a) every ranked method, incomplete blocks | chronos, diffusion_ts, timesfm, timestral, vae_atsp, vae_greedy, vae_herding, vae_knn, vae_mbb, vae_pctsp, vae_quilting, vae_rand, vae_zseries |
| clf_up_h24_q90|linear|oot | (b) every ranked method, complete datasets | chronos, diffusion_ts, timesfm, timestral, vae_atsp, vae_greedy, vae_herding, vae_knn, vae_mbb, vae_pctsp, vae_quilting, vae_rand, vae_zseries |
| reg_h24|linear|oot        | pre-specified: complete methods            | diffusion_ts, timestral, vae_atsp, vae_greedy, vae_herding, vae_knn, vae_mbb, vae_pctsp, vae_quilting, vae_rand, vae_zseries                   |
| reg_h24|linear|oot        | (a) every ranked method, incomplete blocks | chronos, diffusion_ts, timesfm, timestral, vae_atsp, vae_greedy, vae_herding, vae_knn, vae_mbb, vae_pctsp, vae_quilting, vae_rand, vae_zseries |
| reg_h24|linear|oot        | (b) every ranked method, complete datasets | chronos, diffusion_ts, timesfm, timestral, vae_atsp, vae_greedy, vae_herding, vae_knn, vae_mbb, vae_pctsp, vae_quilting, vae_rand, vae_zseries |

## Tests

Permutations: 100000 (Skillings-Mack: 5000). Check: on a complete design Skillings-Mack equals Friedman without the tie correction (difference 8e-15).

| cell                      | variant                                    | test           |   n_datasets |   n_methods |   missing_cells |   statistic |   p_chi2 |   p_perm |
|:--------------------------|:-------------------------------------------|:---------------|-------------:|------------:|----------------:|------------:|---------:|---------:|
| clf_up_h24_q90|linear|oot | pre-specified: complete methods            | friedman       |            9 |          11 |               0 |       12    | 0.286    |  0.287   |
| clf_up_h24_q90|linear|oot | (a) every ranked method, incomplete blocks | skillings_mack |            9 |          13 |               5 |       11.9  | 0.454    |  0.469   |
| clf_up_h24_q90|linear|oot | (b) every ranked method, complete datasets | friedman       |            5 |          13 |               0 |        6.65 | 0.88     |  0.901   |
| reg_h24|linear|oot        | pre-specified: complete methods            | friedman       |            9 |          11 |               0 |       35.2  | 0.000115 |  4e-05   |
| reg_h24|linear|oot        | (a) every ranked method, incomplete blocks | skillings_mack |            9 |          13 |               5 |       42.2  | 3.04e-05 |  0.0002  |
| reg_h24|linear|oot        | (b) every ranked method, complete datasets | friedman       |            5 |          13 |               0 |       27.5  | 0.00653  |  0.00147 |

## Holm over the confirmatory family with the permutation p of C1

| test                | cell                      | comparison                           |   p_holm |   p_holm_perm | verdict      |
|:--------------------|:--------------------------|:-------------------------------------|---------:|--------------:|:-------------|
| C1 methods differ   | clf_up_h24_q90|linear|oot | Friedman, all methods                |  1       |        1      | inconclusive |
| C2 long vs assembly | clf_up_h24_q90|linear|oot | diffusion_ts vs assembly_median      |  0.773   |        0.773  | inconclusive |
| C2 long vs assembly | clf_up_h24_q90|linear|oot | chronos vs assembly_median           |  1       |        1      | inconclusive |
| C3 selection        | clf_up_h24_q90|linear|oot | optimised selection (mean) vs random |  1       |        1      | inconclusive |
| C4 seam processing  | clf_up_h24_q90|linear|oot | any joiner vs none (all paths)       |  0.383   |        0.383  | inconclusive |
| C1 methods differ   | reg_h24|linear|oot        | Friedman, all methods                |  0.00115 |        0.0004 | differ       |
| C2 long vs assembly | reg_h24|linear|oot        | diffusion_ts vs assembly_median      |  0.312   |        0.312  | inconclusive |
| C2 long vs assembly | reg_h24|linear|oot        | chronos vs assembly_median           |  1       |        1      | inconclusive |
| C3 selection        | reg_h24|linear|oot        | optimised selection (mean) vs random |  1       |        1      | inconclusive |
| C4 seam processing  | reg_h24|linear|oot        | any joiner vs none (all paths)       |  0.0352  |        0.0352 | inconclusive |
