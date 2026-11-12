# C3 check — run_h200

Supplementary, not pre-specified (`python -m marathonts.hypotheses.c3_check`). C3 with every selection strategy and without the zseries assembler (see the module docstring). `median_z`: the median effect over datasets in noise units (> 0: selection better than the random path).

The pre-specified variant reproduces the published C3: True.

| cell                      | variant                                 |   n_assemblers | assemblers                                                                                |   n_datasets |   median_z |   p_two_sided |   p_equiv |
|:--------------------------|:----------------------------------------|---------------:|:------------------------------------------------------------------------------------------|-------------:|-----------:|--------------:|----------:|
| clf_up_h24_q90|linear|oot | pre-specified: every selection strategy |              8 | vae_atsp, vae_greedy, vae_herding, vae_knn, vae_mbb, vae_pctsp, vae_quilting, vae_zseries |            9 |     0.0569 |        0.57   |    0.0488 |
| clf_up_h24_q90|linear|oot | without zseries                         |              7 | vae_atsp, vae_greedy, vae_herding, vae_knn, vae_mbb, vae_pctsp, vae_quilting              |            9 |    -0.0222 |        0.734  |    0.0273 |
| reg_h24|linear|oot        | pre-specified: every selection strategy |              8 | vae_atsp, vae_greedy, vae_herding, vae_knn, vae_mbb, vae_pctsp, vae_quilting, vae_zseries |            9 |     0.609  |        0.0977 |    0.248  |
| reg_h24|linear|oot        | without zseries                         |              7 | vae_atsp, vae_greedy, vae_herding, vae_knn, vae_mbb, vae_pctsp, vae_quilting              |            9 |     0.484  |        0.0977 |    0.15   |

Holm over the ten confirmatory tests with C3 without zseries (`verdict`: published):

| test                | cell                      | comparison                           |   p_holm |   p_equiv_holm | verdict      | verdict_without_zseries   |
|:--------------------|:--------------------------|:-------------------------------------|---------:|---------------:|:-------------|:--------------------------|
| C1 methods differ   | clf_up_h24_q90|linear|oot | Friedman, all methods                |  0.0124  |          1     | differ       | differ                    |
| C2 long vs assembly | clf_up_h24_q90|linear|oot | diffusion_ts vs assembly_median      |  0.492   |          1     | inconclusive | inconclusive              |
| C2 long vs assembly | clf_up_h24_q90|linear|oot | chronos vs assembly_median           |  1       |          1     | inconclusive | inconclusive              |
| C3 selection        | clf_up_h24_q90|linear|oot | optimised selection (mean) vs random |  1       |          0.273 | inconclusive | inconclusive              |
| C4 seam processing  | clf_up_h24_q90|linear|oot | any joiner vs none (all paths)       |  0.137   |          1     | inconclusive | inconclusive              |
| C1 methods differ   | reg_h24|linear|oot        | Friedman, all methods                |  1.4e-07 |          1     | differ       | differ                    |
| C2 long vs assembly | reg_h24|linear|oot        | diffusion_ts vs assembly_median      |  0.273   |          1     | inconclusive | inconclusive              |
| C2 long vs assembly | reg_h24|linear|oot        | chronos vs assembly_median           |  0.188   |          1     | inconclusive | inconclusive              |
| C3 selection        | reg_h24|linear|oot        | optimised selection (mean) vs random |  0.391   |          1     | inconclusive | inconclusive              |
| C4 seam processing  | reg_h24|linear|oot        | any joiner vs none (all paths)       |  0.0312  |          1     | inconclusive | inconclusive              |
