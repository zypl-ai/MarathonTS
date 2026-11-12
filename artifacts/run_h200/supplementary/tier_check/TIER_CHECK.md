# Tier check — run_h200

Supplementary, not pre-specified (`python -m marathonts.hypotheses.tier_check`). `tier`: the pre-specified top tier (comparisons with the observed leader, Holm over them). `all_pairs_set`: methods that no other method is shown to beat (one-sided Wilcoxon over datasets for every ordered pair, Holm over all pairs); it does not depend on the choice of the leader. Both are non-rejection sets: membership does not establish equivalence and may reflect limited power.

Leader: zedge_quilting; 24 methods, 9 datasets, 552 ordered pairs; smallest one-sided p before correction: 0.0020. Top tier: 15 methods; all-pairs set: 24 methods.

|                |   mean_rank |   paired_datasets_with_leader |   p_worse_than_leader_holm | tier   |   min_p_all_pairs_holm | all_pairs_set   |
|:---------------|------------:|------------------------------:|---------------------------:|:-------|-----------------------:|:----------------|
| zedge_quilting |        8.27 |                             9 |                   nan      | True   |                      1 | True            |
| zedge_zseries  |        8.79 |                             9 |                     0.41   | True   |                      1 | True            |
| zedge_greedy   |        8.95 |                             9 |                     0.41   | True   |                      1 | True            |
| zedge_pctsp    |        9.18 |                             9 |                     0.293  | True   |                      1 | True            |
| zedge_knn      |        9.33 |                             9 |                     0.41   | True   |                      1 | True            |
| zedge_atsp     |        9.39 |                             9 |                     0.41   | True   |                      1 | True            |
| zedge_ts_ar    |        9.4  |                             9 |                     0.41   | True   |                      1 | True            |
| zedge_ts_long  |        9.5  |                             9 |                     0.191  | True   |                      1 | True            |
| zedge_herding  |       10.5  |                             9 |                     0.107  | True   |                      1 | True            |
| zedge_mbb      |       10.6  |                             9 |                     0.123  | True   |                      1 | True            |
| zedge_rand     |       10.7  |                             9 |                     0.107  | True   |                      1 | True            |
| vae_herding    |       13.5  |                             9 |                     0.0449 | False  |                      1 | True            |
| vae_zseries    |       13.7  |                             9 |                     0.0547 | True   |                      1 | True            |
| diffusion_ts   |       13.8  |                             9 |                     0.0449 | False  |                      1 | True            |
| timesfm        |       14.4  |                             6 |                     0.125  | True   |                      1 | True            |
| vae_quilting   |       14.4  |                             9 |                     0.0547 | True   |                      1 | True            |
| vae_pctsp      |       15.3  |                             9 |                     0.0449 | False  |                      1 | True            |
| vae_atsp       |       15.3  |                             9 |                     0.0449 | False  |                      1 | True            |
| vae_greedy     |       15.6  |                             9 |                     0.0449 | False  |                      1 | True            |
| chronos        |       15.8  |                             7 |                     0.0938 | True   |                      1 | True            |
| vae_knn        |       16    |                             9 |                     0.0449 | False  |                      1 | True            |
| vae_mbb        |       16.3  |                             9 |                     0.0449 | False  |                      1 | True            |
| vae_rand       |       16.5  |                             9 |                     0.0449 | False  |                      1 | True            |
| timestral      |       16.8  |                             9 |                     0.0449 | False  |                      1 | True            |
