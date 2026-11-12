# Literature review: related methods for assembling synthetic series

Methods related to assembling a long series from pieces that were not included in the method list
([BASELINES.md](BASELINES.md)): they have no implementation, come from another field or use the real
train directly instead of a generator pool.

## Analogues from other fields

| Method | Idea | Literature | Implementation |
|---|---|---|---|
| Unit selection (concatenative speech synthesis) | Selection and ordering of speech fragments by the sum of target cost + concatenation cost, Viterbi search. A conceptual analogue of assembly from a window pool | Hunt A., Black A. *Unit selection in a concatenative speech synthesis system using a large speech database*. ICASSP 1996. [doi:10.1109/ICASSP.1996.541110](https://doi.org/10.1109/ICASSP.1996.541110) | Festival (C++, speech only) — [cstr.ed.ac.uk/projects/festival](https://www.cstr.ed.ac.uk/projects/festival/) |
| Video Textures | A transition matrix between frames by similarity; a random walk on the Markov chain gives an endless video | Schödl A., Szeliski R., Salesin D., Essa I. *Video Textures*. SIGGRAPH 2000. [doi:10.1145/344779.345012](https://doi.org/10.1145/344779.345012) | no official one; on a pool it coincides with matched-block from BASELINES.md; its frame distance is the seam cost of the solvers there (greedy, ATSP, PCTSP) |
| Motion Graphs | A graph of motion clips with transitions at similar poses, path search under constraints | Kovar L., Gleicher M., Pighin F. *Motion Graphs*. SIGGRAPH 2002. [doi:10.1145/566654.566605](https://doi.org/10.1145/566654.566605) | no official one |
| Graphcut textures | Optimal seam between overlapping patches via min-cut; in 1D it coincides with image quilting | Kwatra V., Schödl A., Essa I., Turk G., Bobick A. *Graphcut textures: image and video synthesis using graph cuts*. SIGGRAPH 2003. [doi:10.1145/882262.882264](https://doi.org/10.1145/882262.882264) | no official one |

## Diffusion generation of long content

| Method | Idea | Literature | Implementation |
|---|---|---|---|
| RePaint | Inpainting with an unconditional diffusion model: the known part is resampled at every step | Lugmayr A. et al. *RePaint: Inpainting using denoising diffusion probabilistic models*. CVPR 2022. [arXiv:2201.09865](https://arxiv.org/abs/2201.09865) | [github.com/andreas128/RePaint](https://github.com/andreas128/RePaint) — images only, a separate diffusion model for series is needed |
| MultiDiffusion | Overlapping windows are reconciled at every denoising step (averaging of overlaps) | Bar-Tal O., Yariv L., Lipman Y., Dekel T. *MultiDiffusion: Fusing diffusion paths for controlled image generation*. ICML 2023. [arXiv:2302.08113](https://arxiv.org/abs/2302.08113) | [github.com/omerbt/MultiDiffusion](https://github.com/omerbt/MultiDiffusion) — for Stable Diffusion; for series this is a custom implementation on top of Diffusion-TS |
| DiffCollage | A factor graph of overlapping pieces, parallel generation of content of arbitrary length | Zhang Q., Song J., Huang X., Chen Y., Liu M.-Y. *DiffCollage: Parallel generation of large content with diffusion models*. CVPR 2023. [arXiv:2303.17076](https://arxiv.org/abs/2303.17076) | no official code; [project page](https://research.nvidia.com/labs/dir/diffcollage/) |

## Resampling the real series (bootstrap and surrogates)

| Method | Idea | Literature | Implementation |
|---|---|---|---|
| Moving block bootstrap | Concatenation of random overlapping blocks of fixed length | Künsch H. *The jackknife and the bootstrap for general stationary observations*. Ann. Statist. 17(3), 1989. [doi:10.1214/aos/1176347265](https://doi.org/10.1214/aos/1176347265) | [arch](https://github.com/bashtage/arch) (`MovingBlockBootstrap`), [tsbootstrap](https://github.com/astrogilda/tsbootstrap) |
| Circular block bootstrap | The same, with the series wrapped into a circle — all points are equally likely | Politis D., Romano J. *A circular block-resampling procedure for stationary data*. In: LePage R., Billard L. (eds.) Exploring the Limits of Bootstrap, Wiley, 1992 (book chapter, no open link) | [arch](https://github.com/bashtage/arch) (`CircularBlockBootstrap`), [tsbootstrap](https://github.com/astrogilda/tsbootstrap) |
| Stationary bootstrap | The block length is random (geometric) — the result is stationary | Politis D., Romano J. *The stationary bootstrap*. JASA 89(428), 1994. [doi:10.1080/01621459.1994.10476870](https://doi.org/10.1080/01621459.1994.10476870) | [arch](https://github.com/bashtage/arch) (`StationaryBootstrap`), [tsbootstrap](https://github.com/astrogilda/tsbootstrap), [recombinator](https://pypi.org/project/recombinator/) |
| Optimal block length | Automatic selection of the block length for the stationary / circular bootstrap | Politis D., White H. *Automatic block-length selection for the dependent bootstrap*. Econometric Reviews 23(1), 2004. [doi:10.1081/ETC-120028836](https://doi.org/10.1081/ETC-120028836) | [arch](https://github.com/bashtage/arch) (`optimal_block_length`) |
| Seasonal block bootstrap | Blocks start at the same seasonal phase, so seasonality is not broken | Dudek A., Leśkow J., Paparoditis E., Politis D. *A generalized block bootstrap for seasonal time series*. J. Time Series Analysis 35(2), 2014. [ideas.repec.org](https://ideas.repec.org/a/bla/jtsera/v35y2014i2p89-114.html) | no ready-made Python one |
| Sieve bootstrap | Fitting AR(p) with growing p, resampling the residuals, generation by recursion | Bühlmann P. *Sieve bootstrap for time series*. Bernoulli 3(2), 1997. [projecteuclid.org](https://projecteuclid.org/euclid.bj/1177526726) | [tsbootstrap](https://github.com/astrogilda/tsbootstrap) (`SieveBootstrap`) |
| Markov bootstrap | Resampling via a kernel estimate of the transition density of a Markov chain | Rajarshi M. *Bootstrap in Markov-sequences based on estimates of transition density*. Ann. Inst. Statist. Math. 42, 1990. [doi:10.1007/BF00050835](https://doi.org/10.1007/BF00050835) | [tsbootstrap](https://github.com/astrogilda/tsbootstrap) (its own variation: HMM over blocks) |
| AAFT surrogates | Random Fourier phases with matching of the value distribution | Theiler J. et al. *Testing for nonlinearity in time series: the method of surrogate data*. Physica D 58, 1992. [doi:10.1016/0167-2789(92)90102-S](https://doi.org/10.1016/0167-2789(92)90102-S) | [nolitsa](https://github.com/manu-mannattil/nolitsa) |
| IAAFT surrogates | Iterative matching of both the spectrum and the value distribution | Schreiber T., Schmitz A. *Improved surrogate data for nonlinearity tests*. Phys. Rev. Lett. 77, 1996. [doi:10.1103/PhysRevLett.77.635](https://doi.org/10.1103/PhysRevLett.77.635) | [nolitsa](https://github.com/manu-mannattil/nolitsa) |

## Augmentations of real series

| Method | Idea | Literature | Implementation |
|---|---|---|---|
| Window warping / window slicing | Speeding up or slowing down a segment of the series and returning to the original length; cutting out sub-windows | Le Guennec A., Malinowski S., Tavenard R. *Data augmentation for time series classification using convolutional neural networks*. AALTD @ ECML/PKDD 2016. [HAL](https://halshs.archives-ouvertes.fr/halshs-01357973) | [tsgm](https://github.com/AlexanderVNikitin/tsgm) (`tsgm.models.augmentations`), [tsaug](https://github.com/arundo/tsaug) |
| DBA augmentation | Synthetic series as weighted DTW barycentres of real ones | Forestier G., Petitjean F., Dau H. A., Webb G. I., Keogh E. *Generating synthetic time series to augment sparse datasets*. ICDM 2017. [IEEE Xplore](https://ieeexplore.ieee.org/document/8215569); DBA: Petitjean F. et al. Pattern Recognition 44(3), 2011. [doi:10.1016/j.patcog.2010.09.013](https://doi.org/10.1016/j.patcog.2010.09.013) | [tsgm](https://github.com/AlexanderVNikitin/tsgm) (`DTWBarycentricAveraging`), [MSD-IRIMAS/Augmenting-TSC-Elastic-Averaging](https://github.com/MSD-IRIMAS/Augmenting-TSC-Elastic-Averaging) |
