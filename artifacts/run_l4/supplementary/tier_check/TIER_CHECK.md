# Tier check — run_l4

Supplementary, not pre-specified (`python -m marathonts.hypotheses.tier_check`). `tier`: the pre-specified top tier (comparisons with the observed leader, Holm over them). `all_pairs_set`: methods that no other method is shown to beat (one-sided Wilcoxon over datasets for every ordered pair, Holm over all pairs); it does not depend on the choice of the leader. Both are non-rejection sets: membership does not establish equivalence and may reflect limited power.

Leader: vae_herding; 13 methods, 9 datasets, 156 ordered pairs; smallest one-sided p before correction: 0.0020. Top tier: 11 methods; all-pairs set: 13 methods.

|              |   mean_rank |   paired_datasets_with_leader |   p_worse_than_leader_holm | tier   |   min_p_all_pairs_holm | all_pairs_set   |
|:-------------|------------:|------------------------------:|---------------------------:|:-------|-----------------------:|:----------------|
| vae_herding  |        5.54 |                             9 |                   nan      | True   |                  1     | True            |
| diffusion_ts |        6.27 |                             9 |                     0.5    | True   |                  1     | True            |
| vae_quilting |        6.36 |                             9 |                     0.5    | True   |                  1     | True            |
| vae_zseries  |        6.41 |                             9 |                     0.5    | True   |                  1     | True            |
| timesfm      |        6.72 |                             6 |                     0.5    | True   |                  1     | True            |
| vae_atsp     |        7.11 |                             9 |                     0.0879 | True   |                  1     | True            |
| vae_rand     |        7.2  |                             9 |                     0.0879 | True   |                  1     | True            |
| vae_mbb      |        7.22 |                             9 |                     0.0879 | True   |                  1     | True            |
| vae_pctsp    |        7.23 |                             9 |                     0.0879 | True   |                  0.605 | True            |
| chronos      |        7.43 |                             7 |                     0.391  | True   |                  1     | True            |
| vae_knn      |        7.56 |                             9 |                     0.0586 | True   |                  0.605 | True            |
| vae_greedy   |        7.6  |                             9 |                     0.0469 | False  |                  0.305 | True            |
| timestral    |        8.56 |                             9 |                     0.0469 | False  |                  0.605 | True            |
