# C3 check — run_l4

Supplementary, not pre-specified (`python -m marathonts.hypotheses.c3_check`). C3 with every selection strategy and without the zseries assembler (see the module docstring). `median_z`: the median effect over datasets in noise units (> 0: selection better than the random path).

The pre-specified variant reproduces the published C3: True.

| cell                      | variant                                 |   n_assemblers | assemblers                                                                                |   n_datasets |   median_z |   p_two_sided |   p_equiv |
|:--------------------------|:----------------------------------------|---------------:|:------------------------------------------------------------------------------------------|-------------:|-----------:|--------------:|----------:|
| clf_up_h24_q90|linear|oot | pre-specified: every selection strategy |              8 | vae_atsp, vae_greedy, vae_herding, vae_knn, vae_mbb, vae_pctsp, vae_quilting, vae_zseries |            9 |    -0.126  |         0.734 |    0.082  |
| clf_up_h24_q90|linear|oot | without zseries                         |              7 | vae_atsp, vae_greedy, vae_herding, vae_knn, vae_mbb, vae_pctsp, vae_quilting              |            9 |    -0.0967 |         0.734 |    0.0645 |
| reg_h24|linear|oot        | pre-specified: every selection strategy |              8 | vae_atsp, vae_greedy, vae_herding, vae_knn, vae_mbb, vae_pctsp, vae_quilting, vae_zseries |            9 |     0.235  |         0.91  |    0.18   |
| reg_h24|linear|oot        | without zseries                         |              7 | vae_atsp, vae_greedy, vae_herding, vae_knn, vae_mbb, vae_pctsp, vae_quilting              |            9 |     0.039  |         1     |    0.15   |

Holm over the ten confirmatory tests with C3 without zseries (`verdict`: published):

| test                | cell                      | comparison                           |   p_holm |   p_equiv_holm | verdict      | verdict_without_zseries   |
|:--------------------|:--------------------------|:-------------------------------------|---------:|---------------:|:-------------|:--------------------------|
| C1 methods differ   | clf_up_h24_q90|linear|oot | Friedman, all methods                |  1       |          1     | inconclusive | inconclusive              |
| C2 long vs assembly | clf_up_h24_q90|linear|oot | diffusion_ts vs assembly_median      |  0.773   |          1     | inconclusive | inconclusive              |
| C2 long vs assembly | clf_up_h24_q90|linear|oot | chronos vs assembly_median           |  1       |          1     | inconclusive | inconclusive              |
| C3 selection        | clf_up_h24_q90|linear|oot | optimised selection (mean) vs random |  1       |          0.645 | inconclusive | inconclusive              |
| C4 seam processing  | clf_up_h24_q90|linear|oot | any joiner vs none (all paths)       |  0.383   |          1     | inconclusive | inconclusive              |
| C1 methods differ   | reg_h24|linear|oot        | Friedman, all methods                |  0.00115 |          1     | differ       | differ                    |
| C2 long vs assembly | reg_h24|linear|oot        | diffusion_ts vs assembly_median      |  0.312   |          1     | inconclusive | inconclusive              |
| C2 long vs assembly | reg_h24|linear|oot        | chronos vs assembly_median           |  1       |          1     | inconclusive | inconclusive              |
| C3 selection        | reg_h24|linear|oot        | optimised selection (mean) vs random |  1       |          1     | inconclusive | inconclusive              |
| C4 seam processing  | reg_h24|linear|oot        | any joiner vs none (all paths)       |  0.0352  |          1     | inconclusive | inconclusive              |
