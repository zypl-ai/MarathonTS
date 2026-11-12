# Benchmark design figures

Vector PDF figures of the benchmark *design* (structure, pipelines, data flow, generative and ML
pipelines, statistics). They show no results. Each figure has a Markdown file with the same name
that contains a suggested caption and a description for the paper.

| # | Figure | Topic |
|---|---|---|
| 1 | [fig01_architecture](fig01_architecture.md) | layered software architecture |
| 2 | [fig02_stage_pipeline](fig02_stage_pipeline.md) | pipeline stages, outputs, environments |
| 3 | [fig03_environments](fig03_environments.md) | dependency isolation, hand-off via Parquet |
| 4 | [fig04_data_preprocessing](fig04_data_preprocessing.md) | raw data → windows, leakage boundary |
| 5 | [fig05_temporal_split](fig05_temporal_split.md) | split, embargoes, role of each part |
| 6 | [fig06_pool_generator_vae](fig06_pool_generator_vae.md) | β-VAE pool generator |
| 8 | [fig08_method_family](fig08_method_family.md) | the compared methods (16 in min, 17 in mid, 35 in max) |
| 9 | [fig09_long_generators](fig09_long_generators.md) | Diffusion-TS, Chronos, TimesFM and Timestral baselines |
| 10 | [fig10_utility_pipeline](fig10_utility_pipeline.md) | TSTR vs TRTR protocol |
| 11 | [fig11_tasks_models](fig11_tasks_models.md) | downstream tasks × models |
| 12 | [fig12_fidelity_evaluation](fig12_fidelity_evaluation.md) | fidelity inputs, three references, metric groups |
| 13 | [fig13_statistical_pipeline](fig13_statistical_pipeline.md) | statistical analysis: ranking, comparisons, associations, confirmatory family |
| 14 | [fig14_hypotheses_map](fig14_hypotheses_map.md) | research questions RQ0–RQ9, C1–C4, evidence, analyses |
| 15 | [fig15_incremental_recompute](fig15_incremental_recompute.md) | unit fingerprints, caching |
| 16 | [fig16_artifact_layout](fig16_artifact_layout.md) | output layout |
| 17 | [fig17_profiles](fig17_profiles.md) | run profiles min / mid / max |
| 18 | [fig18_extensibility](fig18_extensibility.md) | registries and plugins |

## Regenerating

```bash
python docs/figures/src/make_figures.py      # needs Graphviz (`dot`) and matplotlib
```

The Graphviz sources are written to `src/dot/`. All figures share one colour code:
blue = real data, orange = generative models, yellow = assembly, pink = fidelity,
green = downstream ML, purple = statistics, grey = infrastructure and storage. Fills differ in
lightness, so they stay distinguishable in grayscale. Fonts are embedded (Helvetica, TrueType).

Numbers in the figures follow the code defaults (`marathonts/bench/config.py`) and the profile `min` unless a
figure says otherwise. Update the figures when these defaults change.
