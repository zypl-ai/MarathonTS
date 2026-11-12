# Figure 9 — Long-series generators (Diffusion-TS, Chronos, TimesFM, Timestral)

**File:** `fig09_long_generators.pdf`

**Suggested caption.** The baselines that generate long series directly. Diffusion-TS grows the
series by autoregressive infilling: each new window takes the last T/2 generated values as known
context and fills in the rest. Chronos samples continuations of the end of the training series in
chunks of 64 points. TimesFM and Timestral give their median forecast of the K·T steps after train,
with the whole train as context (up to the model's limit). Boundaries between chunks or blocks count as seams in the seam metrics.

## Diffusion-TS

- Official implementation (`external/Diffusion-TS`, pinned commit), hyperparameters from
  `Config/etth.yaml` with window length T.
- Trained on the same core windows as the VAE, with an exponential moving average (EMA) of the
  weights; optimiser, learning-rate schedule (warm-up to 8e-4, then plateau decay), batch 128 with
  gradient accumulation 2 and EMA as in the official solver; early stopping on the holdout windows.
- `min`/`mid`: one model per dataset; `max`: one model per seed.
- Generation: the calendar channels are known at every position (hour of week continues from a
  random start, one per seed); only the value channel is generated. Window 1 is generated with no
  known values. Each later window takes the last c = T/2 values as known context and infills the
  remaining T/2 (`fast_sample_infill`, 50 DDIM steps). The result is truncated to K·T.

## Chronos

- `amazon/chronos-t5-small` (`max`: `chronos-t5-base`), no fine-tuning. Loaded once per process; the load time is recorded as
  `fit_wall_s`.
- Context: the last 512 real training values. The model samples one path 64 points at a time; each
  chunk is appended and the context is cut back to the last 512 points.
- The hour of week continues from the end of train.

## TimesFM 3.0 and Timestral 209M

- Pretrained forecasters used zero-shot as documented, package defaults, revisions pinned:
  `google/timesfm-3.0-pytorch` (package `timesfm` 3.0.2) and `mistralai/Timestral-209M` (package `timestral`).
- Context: the whole training split (within 15 360 and 32 768 steps). The series is the median forecast
  of the K·T steps after train: TimesFM in one non-autoregressive pass (no seams), Timestral in blocks of
  1024 steps with each block's median fed back (block boundaries are seams).
- No sampling: the series is the same on every seed, so its between-seed spread is zero.
- Leakage: Chronos is left out on `electricity` and `beijing_pm25`, TimesFM on `household`,
  `beijing_pm25` and `bitcoin` (the same data or object in their training data, DATASETS.md); Timestral is
  pretrained on synthetic data only, and the real data of its post-training are not listed, so its pairs are
  unknown and kept (DATASETS.md).

## Notes for the text

- Calendar handling differs across families. The VAE generates the calendar channels as part of
  the window, Diffusion-TS has them imposed, and Chronos, TimesFM and Timestral continue the real calendar. For this
  reason the calendar-continuity metrics F4.4–F4.5 are left out of the ranking and the cross-family comparisons (RQ1–RQ3, CS9).
- Cost: for the longest dataset (PJM, profile `max`), Diffusion-TS needs about 1 000 sequential
  infills of 50 DDIM steps per seed.
