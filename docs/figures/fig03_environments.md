# Figure 3 — Software environments and hand-off through artifacts

**File:** `fig03_environments.pdf`

**Suggested caption.** Isolation of conflicting dependencies. The VAE pool generator runs in a
TensorFlow environment without PyTorch. Assembly, Diffusion-TS, Chronos, TimesFM, Timestral, evaluation and the
statistics run in PyTorch environments that never imports TensorFlow. The only link between the
environments is the Parquet files they write.

## What the figure shows

| Environment | Requirements file | Runs | Main dependencies |
|---|---|---|---|
| base | `envs/base.txt` | `raw`, `prepare` | numpy, scipy, pandas, pyarrow, psutil |
| tsgm | `envs/tsgm.txt` | `pools --pool-generators tsgm_vae` | base + TensorFlow, Keras 3, tsgm 0.1.0 (no torch) |
| sdv (optional) | `envs/sdv.txt` | `pools --pool-generators sdv_par` | base + SDV |
| core | `envs/core.txt` | `generate` (assembly), `fidelity`, `utility`, `collect`, `hypotheses` | base + PyTorch, scikit-learn, XGBoost, statsmodels, ruptures, hmmlearn, elkai, OR-Tools |
| diffusion_ts | `envs/diffusion_ts.txt` | `generate --methods diffusion_ts` | core + einops + Diffusion-TS code |
| chronos | `envs/chronos.txt` | `generate --methods chronos` | core + chronos-forecasting |
| timesfm | `envs/timesfm.txt` | `generate --methods timesfm` | core + timesfm 3.0.2 |
| timestral | `envs/timestral.txt` | `generate --methods timestral` | core + timestral |

## Notes for the text

- The pool is the interface between generator and assembler. The generator writes `(N, T, 3)`
  windows to `artifacts/pools`. `generate` only reads them, so every same-pool method sees exactly
  the same windows.
- Each generator declares its environment and the modules it needs. If the modules are missing and
  the pool does not exist yet, the stage skips that generator and prints which environment to use.
- Docker: target `tsgm` runs stage 2, target `bench` runs the rest. In Colab each notebook has its
  own runtime. `run_in_env(...)` creates a venv from `envs/<env>.txt` and runs the stage as a
  subprocess.
