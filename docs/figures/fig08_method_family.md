# Figure 8 — The compared methods

**File:** `fig08_method_family.pdf`

**Suggested caption.** The compared methods. Groups A and B take windows from the same VAE pool, so
they differ only in which windows they pick, in what order, and how seams are handled. Group C
generates long series directly. Every method returns one series of length K·T per (dataset, seed).

## Groups

**A — Selection and order (10 methods in mid / max, 9 in min without `vae_rand_b`; same pool).**
`vae_zseries` (zseries, the proprietary assembler of zypl.ai (under development), the case-study method: its results are published
(`Config.frozen_methods`), its code is not part of the repository); the
control `vae_rand` (K random windows in random order) and, in `mid` and `max`, `vae_rand_b` (a second
independent random order, used to estimate noise); alternative assemblers, each with the seam criterion
of its own literature: `vae_greedy` (nearest neighbour by the jump at the seam), `vae_atsp` (asymmetric
TSP over the whole pool with LKH via `elkai`; the cheapest run of K consecutive windows in the tour),
`vae_pctsp` (prize-collecting TSP in OR-Tools: chooses K of N windows and their order at once; up to
2 000 solutions or 60 s) — the three solvers by the jump at the seam, the Euclidean distance between the
last point of a window and the first point of the next (the frame distance of video textures);
`vae_mbb` (matched-block bootstrap: a Gaussian kernel of the jump, bandwidth = median jump), `vae_knn`
(k-nearest-neighbour resampling, k = √N, weights ∝ 1/rank), `vae_quilting` (image quilting: a random
window among those whose overlap error is within 1.1 × the best, then the minimum-error cut),
`vae_herding` (kernel herding towards train windows under MMD; random order).

**B — Seam joiners (3 methods; 21 in max).** Applied to the path of `vae_zseries` (published results; in `max`
also to every assembler except the random path and `vae_quilting`). Neighbouring windows overlap by 12 points: `xfade` blends the overlap with a
Hann window, `wsola` first shifts the next window by up to 12 points to the best correlation, and
`quilt` cuts at the point of minimum difference (1-D image quilting). Overlap shortens the series, so
the joiner takes more windows than K and truncates the result to K·T.

**C — Long-series generators (4 methods).** `diffusion_ts` (Diffusion-TS trained on the same
training windows; series grown by autoregressive infilling), `chronos` (pretrained Chronos-T5-small,
zero-shot, sampled), `timesfm` (TimesFM 3.0) and `timestral` (Timestral 209M): pretrained forecasters
used zero-shot as documented — the median forecast of the K·T steps after train, the whole train as
context (up to the model's limit), the same series on every seed. See Fig. 9.

**Reference.** `real` is not a method: in fidelity it is the OOT series (real-versus-real reference); in utility it
is the model trained on real train (TRTR).

## Notes for the text

- Scale: 16 methods in `min` (without `vae_rand_b`), 17 in `mid`, 35 in `max`, of them 4 published
  results (`vae_zseries` and its three joiner variants); the pipeline runs 12 / 13 / 31 methods × 10 seeds
  × 9 datasets = 1 080 / 1 170 / 2 790 generated series.
- Every series is stored with its hour of week, the source window and piece of each point, and a
  seam flag. The seam metrics (F5) use the flag; for group C, chunk boundaries count as seams.
- Source: `marathonts/bench/methods.py`, `marathonts/bench/assemblers.py`, `marathonts/bench/joiners.py`, `BASELINES.md`.
