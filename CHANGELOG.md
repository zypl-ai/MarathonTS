# Changelog

All notable changes of MarathonTS are recorded here. Versions follow [semantic versioning](https://semver.org/);
the tag of the code, of the data on Hugging Face and of the PyPI package is the same.

## [1.0.0] — unreleased

First public release, the version described in the paper.

- Python package `marathonts`. Benchmark pipeline (`marathonts/bench/`): nine open hourly datasets, a window-pool generator, assemblers and seam joiners
  on every pool, long-series generators (Diffusion-TS, Chronos, TimesFM 3.0, Timestral), fidelity (83 metrics in
  12 groups against train, val and OOT), utility (14 tasks, TSTR against TRTR), memorisation and cost.
- Statistical analysis (`marathonts/hypotheses/`): overall leaderboard, rankings by slice, research questions RQ0–RQ9,
  confirmatory family C1–C4.
- Run profiles `min`, `mid`, `max`; Docker images, Colab notebooks and local environments; incremental
  recomputation by unit fingerprints; plugins for every component.
- Results of the two published runs of profile `min`: the main run in `artifacts/run_h200/` (one NVIDIA H200) and
  the replication run in `artifacts/run_l4/` (one NVIDIA L4), tables and reports; full artifacts on Hugging Face.
- Results published without code (`frozen_methods`) enter a run's tables only under the settings they were made
  with (`tables/frozen.json`, stage `freeze`).
- A Git LFS pointer in place of an artifact stops the run with what to do instead of being set aside as truncated.
- Tests (`tests/`, CI): storage, the settings check of the published results, and a smoke test that rebuilds the
  published rankings and questions from the tables of the published runs (`artifacts/run_*/tables/`) (pinned analysis environment `tests/requirements.txt`).
