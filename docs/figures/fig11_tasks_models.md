# Figure 11 — Downstream tasks and models

**File:** `fig11_tasks_models.pdf`

**Suggested caption.** The 14 downstream tasks (U2.1–U2.9) and the models trained on each. All
tasks use the same 11 features. Labels are functions of the series, with thresholds frozen on real
train. Task U2.1 (green) is the task of the pre-specified case-study cell.

## Tasks

| ID | Task(s) | Kind | Target |
|---|---|---|---|
| U2.1 | `clf_up_h24_q90` | binary | change over 24 h above the 0.90 train quantile |
| U2.2 | `clf_up_h{1,6,168}_q90` | binary | same, other horizons |
| U2.3 | `clf_up_h24_q{95,99}` | binary | rare events |
| U2.4 | `clf_down_h24_q10` | binary | change below the 0.10 quantile (opposite tail) |
| U2.5 | `mc3_h24` | 3 classes | down / neutral / up |
| U2.6 | `reg_h{1,24,168}` | regression | value x_{t+h} |
| U2.7 | `qreg_h24` | quantile regression | quantiles 0.1 / 0.5 / 0.9 |
| U2.8 | `ms_h24` | multistep | vector x_{t+1..t+24} |
| U2.9 | `vol_h24` | volatility | std of the next 24 hourly changes |

## Models

- `linear`: logistic/softmax regression (L-BFGS, balanced weights, C = 1), ridge (α = 1, exact
  solve), linear quantile regression (smoothed pinball). PyTorch.
- `mlp`: 64 → 32 ReLU network, Adam lr 1e-3, weight decay 1e-4, batch 512. In `min`/`mid` it runs
  30 epochs on U2.1 only; in `max`, up to 200 epochs with early stopping on all tasks.
- `gbdt`: XGBoost. `min`/`mid`: 100 trees, depth 4, 64 bins, CPU, vector leaves for the multistep
  task. `max`: 200 trees, depth 6, 256 bins, one ensemble per step.

## Notes for the text

- Every (task, model) pair is fitted in both regimes (S and R) and evaluated on both val and OOT.
- Every task enters the ranking and the research questions with equal weight, grouped into
  classification and regression; U2.1 only marks the case-study cell (CS7), U2.2–U2.9 are case study CS8.
- Source: `marathonts/bench/tasks.py`, `marathonts/bench/models.py`, `MODELS.md`, `METRICS.md` (U2–U4).
