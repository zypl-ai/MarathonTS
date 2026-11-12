# Figure 12 — Fidelity evaluation

**File:** `fig12_fidelity_evaluation.pdf`

**Suggested caption.** Fidelity evaluation. Every generated series, the real OOT series (real-versus-real reference),
and length-matched truncations of the generated series are scored by the same code against three
real references: val (primary), train and OOT. The metrics are organised in 12 groups (83 metrics);
memorisation (F10) is computed once, against train.

## Inputs

- **Series under test:** each (method, seed) series of length K·T; `m@len`, the first len(OOT)
  points of each method (seed 0), for an equal-length comparison with the real series; `real`, the OOT
  series (seed 0).
- **References:** val (primary, no suffix); train (`@train`): how well a method reproduces the
  data it was fitted on — methods fitted on train, and methods that take reference statistics from train, use this data
  during fitting; OOT (`@oot`): generalisation under temporal drift. `real` is a piece of OOT
  and is not scored against OOT.

## Metric groups

F1 marginal distribution · F2 increments · F3 temporal dependence (incl. ACF beyond the window
length, T…3T) · F4 seasonality and calendar · F5 seams · F6 window-level distribution
(post-hoc GRU discriminator, C2ST, predictive score, MMD, feature-FID, nearest-neighbour distance)
· F7 long-range structure (rolling statistics, level crossings, drawdowns, trend, HMM regimes) ·
F8 target structure · F9 diversity and coverage · F10 memorisation · F11 class balance over every
classification task (relative error of class shares, rare events, multiclass TVD, lost minority
class) · F12 extremes and outliers (exceedances of the real 0.5 / 99.5% quantiles, local spikes,
weekly block maxima and minima).

## Notes for the text

- Each metric has an orientation (`ORIENT`, higher or lower is better).
- AUC-type scores are reported as |AUC − 0.5|, ratios as |log ratio|; window features are 16
  in-house statistics; nearest-neighbour distances are Euclidean.
- Pairwise distances (MMD, nearest neighbours, precision/recall) and the GRU discriminator run in
  torch on the GPU. Cross-seed diversity (F9.4) is computed separately at the `collect` stage.
- Source: `marathonts/bench/fidelity.py`, `METRICS.md`.
