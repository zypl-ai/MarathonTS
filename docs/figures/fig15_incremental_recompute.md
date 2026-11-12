# Figure 15 — Incremental recomputation with unit fingerprints

**File:** `fig15_incremental_recompute.pdf`

**Suggested caption.** Dependency graph of unit fingerprints. Each unit of work stores a hash of
its inputs, its own settings, the relevant configuration files, and the fingerprints of the units
it depends on. When a setting changes, only the units downstream of it are recomputed.

## What the figure shows

- **Roots:** processed data (`data_key`: split, number of points, T), the generator training
  windows (`max_windows`, `holdout_frac`), and two committed JSON files (`target_params*.json`,
  `model_configs.json`).
- **Generator training and sampling are separate units.** VAE fitting depends on the training
  windows; pool sampling depends on the fitted weights and the pool size. Diffusion-TS fitting
  depends on the training windows; the loads of the pretrained generators (Chronos, TimesFM, Timestral)
  depend only on the data.
- **Series** of a method depend on their upstream generator units and on the settings of their
  assembler or joiner (e.g. `mbb_bandwidth`, `pctsp_*`, `join_overlap`).
- **Evaluation units:** fidelity depends on the series and the target parameters (of its own dataset:
  the thresholds of a new dataset do not redo the others); labels depend
  on the data and the target parameters; utility (TSTR) depends on the series, the labels and the
  model configurations; TRTR depends on the labels and the model configurations only. Fidelity and
  utility units are fingerprinted per cell (metric group; task × model): the done cells are listed in a
  registry next to the unit (`cells.json`), so an added or changed model, task or metric group computes
  only its own cells.

## Example

Changing `knn_k` (the number of neighbours of `vae_knn`) recomputes the `vae_knn` series (and its
joiner variants, where they are run) together with their fidelity and utility. Pools, VAE weights,
the other methods, labels, TRTR and the fidelity of the real series are kept. Changing the pool size re-samples pools from the stored weights and redoes
every same-pool method, while VAE training, Diffusion-TS, the pretrained generators, labels, TRTR and real-data
fidelity are kept.

## Notes for the text

- This makes long runs resumable across sessions (e.g. Colab disconnections) and keeps all cached
  results consistent with the current configuration.
- A utility unit in which every fit failed (e.g. out of GPU memory) is not marked done and is
  retried on the next run.
- Source: `marathonts/bench/config.py` (`unit_fingerprint`), `BENCHMARK.md` "Stages".
