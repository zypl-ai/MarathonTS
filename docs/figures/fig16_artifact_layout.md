# Figure 16 — Artifact layout

**File:** `fig16_artifact_layout.pdf`

**Suggested caption.** Layout of the benchmark outputs. Every unit of work writes its own Parquet
file. The `collect` stage merges them into the published tables in `tables/`.

## Contents

| Path | Row / content |
|---|---|
| `pools/<ds>/<gen>/seed<k>.parquet` | pool windows (N, T, 3); `.record` holds training and sampling time and diagnostics |
| `generators/<ds>/<gen>/…` | generator weights (VAE, Diffusion-TS, SDV, plugins) |
| `series/<ds>/<method>/seed<k>.parquet` | generated series: t, value, hour of week, window, piece, seam flag |
| `records/…` | time, memory, hardware and diagnostics of each generation run |
| `fidelity/…` | one row with all F-metrics |
| `labels/<ds>/<task>.parquet` | real test labels (split, row, y) |
| `utility/<ds>/<method>/seed<k>/` | `metrics`, every `prediction`, weights of every fitted model, `cells.json` (done cells) |
| `tables/` | `timing`, `fidelity`, `utility`, `pools`, `cross_seed`, `datasets`, `inventory`, `hardware`, `config.json` |
| `reports/` | Markdown reports of the analysis: `REPORT.md` (research questions RQ0–RQ9, confirmatory family C1–C4, case study CS1–CS15), `OVERALL.md` (overall leaderboard), `LEADERBOARD.md` (ranking of every method in every slice), `METRIC_VALUES.md` (values of the core fidelity metrics and the primary utility metrics by reference, dataset, task, model and split) |
| `overall/` | tables of the overall leaderboard (fidelity on the core metrics and utility, noise-aware ranks) and its robustness checks |
| `leaderboard/` | tables of the ranking of every method in every slice, incl. `rankings.parquet` (the four rankings) and `rankings_summary.parquet` |
| `metric_values/` | `fidelity.parquet`, `utility.parquet`: median and IQR over seeds of every metric × reference and task × model × split, per dataset and method |
| `hypotheses/` | per-question global and per-dataset tables (RQ*, CS*), confirmatory family |
| `errors.log` | failed units (the run continues) |

## Notes for the text

- Storage: Parquet with zstd; float32 everywhere except series values (float64). Each profile
  writes to its own `artifacts/<profile>/`.
- Every model and generator can be reloaded and used without retraining (`marathonts/bench/load.py`), so
  reviewers can re-evaluate saved models on new test data.
