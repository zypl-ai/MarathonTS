# Figure 6 — Pool generator (β-VAE)

**File:** `fig06_pool_generator_vae.pdf`

**Suggested caption.** The window-pool generator. A convolutional β-VAE is trained on core training
windows and stopped early on the holdout loss. After training, N windows are sampled from a shrunk
prior and written to disk as the pool that every same-pool method shares.

## Details

| Item | Value |
|---|---|
| Architecture | `tsgm` `vae_conv5` encoder/decoder + `BetaVAE`, latent dimension 16 |
| Loss | reconstruction + β·KL, β = 2 |
| Optimisation | Adam, lr 1e-3, batch 64, up to 400 epochs |
| Early stopping | holdout loss after each epoch with z = μ; patience 50; best weights restored; epochs 1–150 are not eligible (`vae_min_epochs`; taken from earlier work of the authors on other data) |
| Sampling | z ~ 0.5 · N(0, I) → decoder → NaN replaced by 0.5 → clipped to [0, 1] |
| Pool | N = max(300, 2K) windows of shape (T, 3), per (dataset, seed) |

## Model sharing across seeds (`pool_train_replicas`)

- `min`: one VAE per dataset (9 trainings in total); seeds change only the sampling.
- `mid`, `max`: one VAE per seed (90).
- Any other value k of `pool_train_replicas` gives k VAEs per dataset; seed s uses model s mod k.

The training time of a shared model is recorded for every seed and enters the cost comparison
(RQ6) for each of them.

## Notes for the text

- The assembler does not depend on where the pool comes from. Any generator that outputs windows in
  the same three channels can replace the VAE (registry `pool_generators`; e.g. `sdv_par`,
  `real_windows`).
- Fitting and sampling have separate fingerprints. Changing N re-samples the pools from the saved
  weights without retraining the VAE.
