# Methods compared

Ways to assemble a long series from a pool of N generated windows (which K windows, in what order, how the
seams are processed) and long-series generators. `vae_zseries` is zseries, the proprietary assembler of zypl.ai (under development), on the same
pool: its results are published (`Config.frozen_methods`), its code is not part of the repository. Its results
and those of its seam-processing variants `vae_zseries_{xfade,wsola,quilt}` enter the tables and the analysis
as published; the pipeline does not run them.

Only methods whose series enter the benchmark tables are listed here: each outputs a series of length
`K·T` in the same channels and enters the utility test of BENCHMARK.md (Protocol: utility) like any other series. Methods that
were considered but not included are in [LITERATURE.md](LITERATURE.md).

**In the benchmark** ([BENCHMARK.md](BENCHMARK.md)) all profiles use all methods of sections A
and B except CSDI, plus Diffusion-TS, Chronos, TimesFM and Timestral from section C; the noise twin `vae_rand_b` runs in `mid`
and `max` only. All methods of A and B take the same VAE pool (`min`: 300 windows); the methods of B are
applied on top of the `vae_zseries` path (published results; `max`: in addition on top of every assembler except the
random path and `vae_quilting`, run by the pipeline).

Each alternative assembler uses the seam criterion of its own literature, nothing taken from `vae_zseries`.
The three solvers (greedy, ATSP, PCTSP) are general-purpose optimisers without a seam criterion of their
own; they get the jump at the seam — the Euclidean distance between the last point of a window and the
first point of the next, over every channel (value and hour of week, all on [0, 1]) — the frame distance of
video textures (Schödl et al. 2000).

| Method | In the benchmark | Implementation |
|---|---|---|
| Random path | `vae_rand` (control); `vae_rand_b` — a second random order, noise estimate (`mid`, `max`) | `marathonts/bench/assemblers.py` `random`, `random_b` |
| Greedy nearest neighbour | `vae_greedy` (start from a random window) | `greedy` |
| ATSP, LKH | `vae_atsp` | `atsp` (`elkai`) |
| Prize-collecting TSP | `vae_pctsp` (up to 2000 solutions, no more than 60 s per unit) | `pctsp` (OR-Tools) |
| Matched-block bootstrap | `vae_mbb` (Gaussian kernel, h = median jump) | `mbb` |
| k-nearest-neighbour resampling | `vae_knn` (k = round(√N), weights ∝ 1/rank) | `knn` |
| Image quilting | `vae_quilting` (overlap of 12 points, tolerance 0.1) | `quilt_sel` + joiner `quilt` |
| Kernel herding + random order | `vae_herding` | `herding` |
| zseries | `vae_zseries` (published results) | — (code not part of the repository) |
| Overlap-add / crossfade | `vae_zseries_xfade` (overlap of 12 points; published results); `max`: `vae_<assembler>_xfade` | `marathonts/bench/joiners.py` `crossfade` |
| WSOLA | `vae_zseries_wsola` (shift of up to 12 points; published results); `max`: `vae_<assembler>_wsola` | `wsola` |
| Image quilting (boundary cut only) | `vae_zseries_quilt` (published results); `max`: `vae_<assembler>_quilt` | `quilt` |
| Seam inpainting: CSDI | no (requires a separately trained diffusion model) | — |
| Diffusion-TS | `diffusion_ts` (`min`, `mid`: trained once per dataset; `max`: on every seed) | `marathonts/bench/generators/builtin.py` |
| Chronos | `chronos` | `marathonts/bench/generators/builtin.py` |
| TimesFM 3.0 | `timesfm` (median forecast, the whole train as context, up to 15 360 points) | `marathonts/bench/generators/builtin.py` |
| Timestral 209M | `timestral` (median forecast, the whole train as context, up to 32 768 points) | `marathonts/bench/generators/builtin.py` |
| TimeGAN | no (candidate: pool generator, `EXTENDING.md`) | — |

"In-house" in the "Code" column means that there is no ready-made library, but the method takes 10–40 lines
on top of the pool (`marathonts/bench/assemblers.py`).

## A. Same window pool, different selection and order

A comparison of assembly proper: the generator and the pool are the same for all. Every method draws
K windows without repeats.

| Method | Idea | Year | Paper | Code |
|---|---|---|---|---|
| Random path | K random windows from the pool in random order | — | — | BENCHMARK.md, What is compared |
| Greedy nearest neighbour | At each step the window with the smallest jump at the seam is taken | — | — | in-house |
| ATSP, Lin–Kernighan–Helsgaun | Shortest Hamiltonian path over the matrix of jumps at the seams | 2000 | Helsgaun K. *An effective implementation of the Lin–Kernighan traveling salesman heuristic*. EJOR 126(1), 2000 | `elkai` — [github.com/fikisipi/elkai](https://github.com/fikisipi/elkai). The tour is built over all N windows, and the best segment of length K is taken from it. LKH licence: non-commercial only |
| Prize-collecting TSP (selection of K out of N + order) | A route that may skip vertices at a penalty — subset selection and order at the same time | 1989 | Balas E. *The prize collecting traveling salesman problem*. Networks 19(6), 1989 | Google OR-Tools, routing + `AddDisjunction` — [github.com/google/or-tools](https://github.com/google/or-tools) (Apache 2.0). Costs converted to integers, exactly K windows via a visit counter |
| Matched-block bootstrap | The next block is drawn with a kernel of how well its beginning matches the end of the current block | 1998 | Carlstein E., Do K.-A., Hall P., Hesterberg T., Künsch H. *Matched-block bootstrap for dependent data*. Bernoulli 4(3), 1998 | in-house: `P(i→j) ∝ exp(−½ (jump_ij / h)²)`, h = median jump |
| k-nearest-neighbour resampling | The next piece is the successor of one of the k nearest neighbours of the current state, drawn with weight ∝ 1/rank; k = √n | 1996 | Lall U., Sharma A. *A nearest neighbor bootstrap for resampling hydrologic time series*. Water Resources Research 32(3), 1996 | in-house: the k windows whose first point is nearest to the last point of the current window |
| Image quilting | The next patch overlaps the current one; it is drawn at random among the patches whose overlap error is within (1 + ε) of the best, and the overlap is cut along the minimum-error boundary | 2001 | Efros A., Freeman W. *Image quilting for texture synthesis and transfer*. SIGGRAPH 2001 | in-house: overlap of 12 points, ε = 0.1, sum of squared differences of the value channel; the cut — joiner `quilt` |
| Kernel herding / MMD selection + random order | Windows that minimise MMD to train are selected greedily; the order is random — separates the effect of selection from the effect of order | 2010 | Chen Y., Welling M., Smola A. *Super-samples from kernel herding*. UAI 2010; MMD: Gretton A. et al. *A kernel two-sample test*. JMLR 13, 2012 | in-house; a similar submodular selection — `apricot-select`, [github.com/jmschrei/apricot](https://github.com/jmschrei/apricot) |
| zseries (`vae_zseries`) | The proprietary assembler of zypl.ai (under development); its results are published, its code is not part of the repository | — | — | — |

The seam cost of the solvers: Schödl A., Szeliski R., Salesin D., Essa I. *Video textures*. SIGGRAPH 2000.

## B. Seam processing

Applied on top of the `vae_zseries` path (`min`, `mid`: the published results `vae_zseries_{xfade,wsola,quilt}`;
`max`: in addition on top of every assembler except the random path and `vae_quilting`, which has its own
boundary cut). Because of the overlap the series is shorter than `K·T`,
so additional windows are taken to reach the required length.

| Method | Idea | Year | Paper | Code |
|---|---|---|---|---|
| Overlap-add / crossfade | Windows overlap by `o` points and are blended with window weights (Hann) | 1977 | Allen J., Rabiner L. *A unified approach to short-time Fourier analysis and synthesis*. Proc. IEEE 65(11), 1977 | in-house + `scipy.signal.windows.hann` |
| WSOLA | Before blending, the next window is shifted within a tolerance to maximise the correlation in the overlap | 1993 | Verhelst W., Roelands M. *An overlap-add technique based on waveform similarity (WSOLA)*. ICASSP 1993 | in-house |
| Image quilting (min-error boundary cut) | In the overlap zone a cut with minimum error is sought (DP); in 1D — the join point with min \|a−b\| | 2001 | Efros A., Freeman W. *Image quilting for texture synthesis and transfer*. SIGGRAPH 2001 | in-house |
| Seam inpainting: CSDI | A diffusion model fills in the zone around the seam, conditioned on both neighbouring windows | 2021 | Tashiro Y., Song J., Song Y., Ermon S. *CSDI: Conditional score-based diffusion models for probabilistic time series imputation*. NeurIPS 2021 | [github.com/ermongroup/CSDI](https://github.com/ermongroup/CSDI). Must be trained on the train windows |

## C. Another generator or long-series generation without assembly

A comparison of the whole "VAE + assembly" approach, not only of the assembly: the generator changes.

| Method | Idea | Year | Paper | Code |
|---|---|---|---|---|
| Diffusion-TS (autoregressive continuation) | A diffusion transformer; the next window is generated in imputation mode, conditioned on the tail of the previous one | 2024 | Yuan X., Qiao Y. *Diffusion-TS: Interpretable diffusion for general time series generation*. ICLR 2024 | [github.com/Y-debug-sys/Diffusion-TS](https://github.com/Y-debug-sys/Diffusion-TS). Must be trained on the same windows |
| Chronos (trajectory sampling) | A pretrained foundation model; a trajectory of length K·T is sampled from the tail of train without training | 2024 | Ansari A. F. et al. *Chronos: Learning the language of time series*. TMLR 2024 | [github.com/amazon-science/chronos-forecasting](https://github.com/amazon-science/chronos-forecasting) (Apache 2.0). Univariate: K·T steps (5040 in `min`) are generated in chunks, the calendar is computed from time |
| TimesFM (median forecast) | A pretrained decoder-only foundation model (Google), zero-shot; the K·T steps after train are its median forecast in one pass. No sampling: the same series on every seed | 2024 (3.0: 2026) | Das A., Kong W., Sen R., Zhou Y. *A decoder-only foundation model for time-series forecasting*. ICML 2024 | [github.com/google-research/timesfm](https://github.com/google-research/timesfm) (code Apache 2.0, weights of 3.0: TimesFM Non-Commercial License v1.0) |
| Timestral (median forecast) | A pretrained foundation model (Mistral), zero-shot; the K·T steps after train are its median forecast, block by block (1024 steps) with the median fed back. No sampling | 2026 | Mistral AI. *Timestral* (announcement, 15 October 2026; no paper yet) | [github.com/mistralai/timestral](https://github.com/mistralai/timestral) (code Apache 2.0, weights Modified MIT) |
| TimeGAN (pool generator replacement) | A GAN with a supervised one-step-ahead loss in latent space; the TimeGAN pool is assembled by every assembler of the suite | 2019 | Yoon J., Jarrett D., van der Schaar M. *Time-series generative adversarial networks*. NeurIPS 2019 | `tsgm`; [github.com/jsyoon0823/TimeGAN](https://github.com/jsyoon0823/TimeGAN) |
