# Research questions and hypotheses

> The protocol was frozen on 21 October 2026, before the main run; every change made after the freeze is listed in [PROTOCOL_AMENDMENTS.md](PROTOCOL_AMENDMENTS.md).

The benchmark compares ways of obtaining a **long synthetic time series**: assembly from a pool of
short windows (different ways of selecting and ordering windows and of processing seams) and long-series
generators. The questions below are posed about families of methods and about the benchmark itself.
The quality of synthetic data is measured in two ways: fidelity (how closely the series resembles
the real one in its statistics, F1–F12, against three real references — train, val and OOT) and
utility — **TSTR versus TRTR**: a model trained only on synthetic data (TSTR — train on synthetic,
test on real) is compared with the same model trained on real data (TRTR — train on real, test on
real), on the same real test rows of val and OOT, in classification and regression tasks. Metrics
are described in [METRICS.md](METRICS.md).

The benchmark result consists of four parts:

0. **Overall leaderboard** (`marathonts/hypotheses/overall.py` → `artifacts/<profile>/reports/OVERALL.md`, §3, RQ1,
   **Overall leaderboard**) — one ranking of every method by fidelity on the core metrics (against train,
   val and OOT) and utility (classification and regression), with noise-aware ranks and robustness checks;
   privacy and cost are not part of it.
1. **Ranking** (RQ1, `marathonts/hypotheses/leaderboard.py` → `artifacts/<profile>/reports/LEADERBOARD.md`) —
   the rank of each method in each slice: fidelity × reference (train / val / OOT), utility × task
   family × split (val / OOT), cost; with confidence intervals and tests; four rankings — fidelity
   against val + OOT or against train × utility classification or regression; privacy (F10) and cost
   are ranked separately and are not part of them.
2. **Research questions RQ0–RQ9** (`marathonts/hypotheses/questions.py`) — conclusions with statistical tests;
   the confirmatory family C1–C4 (§3.9) gives the main conclusion of the paper.
3. **Case study** CS1–CS15 (`marathonts/hypotheses/catalog.py`, §4) — one method under study (flag `--case-method`,
   by default `vae_zseries`) against its controls and alternatives. Secondary; any method can be analysed this way.

The overall leaderboard heads `artifacts/<profile>/reports/REPORT.md`; everything else goes into it too (`<profile>` — `min`, `mid` or `max`;
default `min`). The values of the metrics behind the rankings — `artifacts/<profile>/reports/METRIC_VALUES.md`
(`marathonts/hypotheses/metric_values.py`): values of the core fidelity metrics and the primary utility metrics by
reference, dataset, task, model and split.

## 1. Methods and roles

| Method | Family | Role in the analysis |
|---|---|---|
| `vae_rand` | assembly: random selection | the simplest assembly from the VAE pool: K windows in random order; reference point for RQ2–RQ3 |
| `vae_rand_b` | assembly: random selection | a second random order of the same pool — **noise** (the difference between two equally random assemblies); `mid` and `max` only; not ranked, serves as a check (RQ0, RQ1) |
| `vae_zseries`, `vae_greedy`, `vae_atsp`, `vae_pctsp`, `vae_mbb`, `vae_knn`, `vae_quilting`, `vae_herding` | assembly: optimised selection | different ways of selecting and ordering windows from the same pool ([BASELINES.md](BASELINES.md), section A); `vae_zseries` — zseries, the proprietary assembler of zypl.ai (under development): its results are published (`Config.frozen_methods`), its code is not part of the repository |
| `vae_zseries_{xfade,wsola,quilt}` | assembly: seam processing | crossfade, WSOLA, quilting on top of the `vae_zseries` path (section B; published results; `max`: in addition on top of every assembler except the random path and `vae_quilting`) |
| `diffusion_ts` | long-series generator | Diffusion-TS, autoregressive extension (trained once per dataset in `min` / `mid`, on each seed in `max`) |
| `chronos` | long-series generator | Chronos, trajectory sampling without training |
| `timesfm`, `timestral` | long-series generator | TimesFM 3.0 and Timestral: the median forecast after train, without training; the same series on every seed: no between-seed spread of their own, so in RQ2 the margin is the spread of the compared method (§2) |
| `real` | reference | real OOT data (real-versus-real reference for fidelity, RQ0) or a model trained on the real train (TRTR, utility reference) |

A method's family is determined from its description (`bench.methods`: pool + assembler + seam
processing, or a long-series generator), so custom methods ([EXTENDING.md](EXTENDING.md)) enter
the ranking and the questions automatically.

## 2. General testing rules

**Direction of the effect.** For a pair "A versus B" the difference
`d = orientation × (A − B)` is computed, where the orientation is +1 for "higher is better" metrics
and −1 for "lower is better" metrics. **d > 0 always means "A is better than B".** Which method
plays the role of A is stated in each question (for example, in RQ2 A is the long-series generator,
in RQ3 A is a way of selecting windows or of processing seams).

**Units of replication.**
- *Within a dataset* — seeds (10). A seed determines generator training, the pool, the random paths
  and the models. Methods with the same seed form a pair (and a block in the ranking).
- *Across datasets* — datasets (9). The global conclusion is drawn from dataset means, not from
  pooled seeds; otherwise large datasets would not be independent.

**What a seed changes in different profiles.** In `max`, VAE and Diffusion-TS are retrained on each
seed: the per-dataset conclusion generalises over the training procedure. In `min`, the VAE is
trained once per dataset, and seeds change only pool sampling and random paths: the per-dataset
conclusion is conditional on this trained model, and the between-seed spread (the noise for
comparisons with independently trained methods) does not include training variability and is
therefore smaller; Diffusion-TS in `min` is also trained once per dataset. In `mid` the VAE is retrained
on every seed (seeds are independent and include training variability) and Diffusion-TS is one model per
dataset as in `min`: its between-seed spread covers sampling only; `diffusion_train_replicas` (or
`dts_train_per_seed`) adds training variability to it. Comparisons on
a single pool (RQ3, CS1–CS8) are not affected by this: all assembly methods use the same pool. The
global conclusion over the 9 datasets generalises over datasets in any profile.

**Tasks a synthetic series could not train.** A TSTR cell (task × model × split) can be missing for a
method whose series exists: its labels have one class (a smooth median forecast has no move above the
threshold), it gives no rows, or the fit failed. Left out, such a cell would rank the method only where
it succeeded — on the easier datasets. With `Config.utility_fail_penalty = True` (default; `--no-fail-penalty`
turns it off) the cell enters as a model that learned nothing (`hypotheses.catalog.impute_failed_utility`,
column `imputed`). Each metric takes the worse of two values: the chance level — ROC AUC 0.5, PR AUC =
positive share p of the test rows, log-loss H(p) for a binary task and ln K for a K-class task, Brier
p(1 − p) — and the worst value any method has in that block (dataset, seed, task, model, split); a
metric without a chance level — regression ones and the metrics of plugin tasks — takes the worst value
of the block. An imputed cell therefore never ranks above a method whose series trained the task. The
chance level is the score of a constant prediction, so AUC is not set below 0.5: an AUC below 0.5 is an
inverted ranking, not an absence of skill. The expected cells are those of TRTR
on the same (dataset, seed), so the rule covers every method, task and model, built-in or plugin. A
method left out on a dataset for leakage (`Config.leaked`) is not imputed there, and neither is a method
with no unit at all. The raw tables in `artifacts/<profile>/tables/` are not changed.

**Noise and the smallest effect size of interest.** For each (dataset, metric) pair, the noise is
the median of |`vae_rand` − `vae_rand_b`| over seeds: how much two equally random assemblies of one
pool typically differ within one run. In `min`, where `vae_rand_b` is not run, it is the median of
|`vae_rand`(seed k) − `vae_rand`(seed k+1)|: the pool is resampled on every seed, so this noise also
contains the pool's sampling variance and is wider — the verdicts are more conservative. This is the pre-specified smallest effect size of interest
(SESOI): it serves both as the threshold of practical significance ("better" only if the effect is
larger) and as the equivalence margin ("the same" if the effect is shown to be smaller). The median
rather than the 95th percentile: with 10 seeds the 95th percentile is close to the maximum, and
"the same" would be obtained almost always. Noise is a property of the pool, not of any method.

For comparisons with independently trained methods (long-series generators in RQ2, C2), the noise is
the median of |A(seed k) − A(seed k+1)| — the between-seed spread, including generator retraining — of
whichever of the two compared methods has the larger one. A pair of random assemblies of one pool does
not have this component, and a generator used without sampling (TimesFM, Timestral: the same series on
every seed) has none of its own, so the comparator's spread sets the margin.

Global effects are expressed **in noise units** (`z = d / noise`), so datasets and metrics of
different scales are comparable.

**Verdict for each unit of analysis** (a metric, or task × model × regime × split):

| Verdict | Condition |
|---|---|
| **better** | the one-sided Wilcoxon "A is better" is significant after correction at level α/2, and the effect exceeds the noise (per dataset — the Hodges–Lehmann estimate, globally — median z > 1) |
| **worse** | the same in the opposite direction |
| **same** | equivalence is demonstrated: TOST (two one-sided Wilcoxon tests) with margin ±noise is significant |
| **inconclusive** | none of the conditions: the data are insufficient to say "better", "worse" or "the same" |

"Same" is **demonstrated** absence of a difference, not absence of significance. Absence of
significance is inconclusive.

The verdict can go either way, so each one-sided p is compared with α/2: together this is a
two-sided test at level α, and the probability of a false directional conclusion does not exceed
α. TOST is tested at level α. If the noise of a metric on a dataset is zero (a discrete metric,
all values coincide), the smallest effect size of interest is undefined: the per-dataset verdict is
inconclusive, the dataset is excluded from the global test, and the number of such datasets is
shown in the column `n_datasets_zero_margin`.

**Tests.**

| Level | Test | Purpose |
|---|---|---|
| dataset, over seeds | Wilcoxon signed-rank (one-sided in both directions), TOST, Hodges–Lehmann, rank-biserial | non-parametric paired test: metric distributions over seeds are not normal |
| global, over datasets | Wilcoxon on dataset means, sign test (share of datasets where better), t-test on dataset means, two-level bootstrap (datasets → seeds) for the confidence interval, TOST with margin ±1 noise unit | several tests with different assumptions; the conclusion is robust if they agree. The unit is the dataset: seeds of one dataset are not independent |
| many methods (ranking, RQ0, C1) | Friedman (blocks — datasets); each method against the best — one-sided Wilcoxon over datasets with Holm (Benavoli et al., 2016); Nemenyi CD — for reference | whether there are any differences at all, and who is statistically indistinguishable from the best. The Nemenyi CD grows with the number of methods, and its conclusion depends on the set of methods |
| ranks | two-level bootstrap of ranks (datasets → seeds), probability of being first / in the top 3 | uncertainty of the position in the ranking |
| ranking agreement (RQ1, RQ5) | Kendall τ | whether the order of methods coincides across slices |
| relations between metrics (RQ0, RQ4) | Spearman within a dataset across methods, Wilcoxon over datasets, BH | which metrics duplicate each other, which predict utility |
| over test rows (CS7, CS12, CS13) | predictions are averaged over seeds, ΔAUC on the same test rows — block bootstrap by weeks | the difference is visible on the test itself. Not DeLong per seed: rows are autocorrelated (labels at horizon h overlap), and DeLong gives false positives several times more often than nominal; the seeds share one test |
| cost | median time with bootstrap over datasets, slope of log(time) on log(K) | how much a method costs and how time grows with series length |

**Multiple comparisons.** Three levels.
- *Confirmatory* — the family C1–C4 (§3.9): two pre-specified cells (classification and
  regression), Holm correction over all tests of the family together; a missing test enters with
  p = 1 and receives the verdict `missing`, so the correction is not weakened. The result is the
  first section of `REPORT.md` and `confirmatory.parquet`. Only these give the main conclusion of
  the paper. The cells and the composition of the family are fixed (§3.9).
- *Secondary* (RQ0, RQ2–RQ6, case study): Benjamini–Hochberg within a question. The conclusion is
  "where better, where worse", with false discovery rate control.
- *Exploratory* (RQ7, CS11, CS12 subgroups, CS15): p-values are shown, but conclusions are
  formulated as hypotheses for future work.

The correction is applied at two levels: global p-values — within a question, over all units of
analysis and comparisons; p-values of per-dataset verdicts — within each "question × dataset" pair,
by the same method. The number of datasets with each verdict in the global table is counted from
the corrected verdicts.

**Power.** With 10 seeds the minimal one-sided Wilcoxon p ≈ 0.001, so a verdict on a single dataset
is possible. With 9 datasets the minimal one-sided p ≈ 0.002. A global conclusion over dozens of
metrics after correction will be obtained only for large and consistent effects. An effect visible
on 2–3 datasets remains inconclusive globally and is visible in the per-dataset verdicts. The main lever of power is
the number of datasets, not of seeds.

## 3. Research questions

### RQ0. Validity of the benchmark

**Question.** Does the benchmark measure what it should? (a) Two random assemblies of one pool
(`vae_rand_b` versus `vae_rand`; `mid` and `max` only) are equivalent on all metrics. (b) How real OOT data compare with
the methods in fidelity: a reference, not an upper bound, since OOT is shifted in time. (c) Which metrics discriminate between methods beyond the noise at all.
(d) Which metrics duplicate each other, and how much the conclusion depends on the reference.

**How it is tested.**
- (a) The noise is estimated on even seeds and TOST on odd seeds, so as not to measure noise and
  equivalence on the same data (`noise_floor`).
- (b) The share of datasets where `real` is better than the method, for each metric
  (`ceiling_share_real_better`). The real OOT is shorter than the synthetic series (20% of the series
  versus K·T), so each method is evaluated on the first len(OOT) points of its series
  (`<name>@len`). A metric is flagged for further inspection (`uninformative_metrics`) if the median of
  this share over methods is below 0.5. This may reflect distribution shift between OOT and the reference,
  sampling variability or limited metric sensitivity; the flag alone does not make the metric invalid and
  does not remove it from any ranking.
- (c) For each metric (fidelity against train / val / OOT; TSTR utility for each cell) — Friedman
  across methods, blocks — datasets, BH; plus the ratio of the spread of methods (IQR of the
  methods' means over seeds) to the noise, median over datasets. A metric is *discriminative* if
  p_BH < α and the spread > 1 noise unit. Summary — the share of discriminative metrics by group and
  reference.
- (d) Spearman between metrics over (dataset, method) pairs after ranking the methods within a
  dataset: pairs with |ρ| ≥ 0.9 (`redundant_pairs`) and the agreement of one metric against
  different references (`reference_agreement`: ρ val ↔ train, val ↔ OOT).

**Supports:** that the verdicts of the other questions are calibrated, and shows which metrics to
rely on. **Does not support:** anything about the quality of the methods.

---

### RQ1. Ranking of all methods in all slices

**Question.** How do the methods rank in each slice and in each of the four rankings, and with what
uncertainty?

**Ranked methods.** Every method of the tables, the published results of `frozen_methods` included, except
the second path of the noise pair and — unless every assembler has them — the
seam-processing variants (`*_xfade`, `*_wsola`, `*_quilt`). Seam processing runs over `vae_zseries` only, so
ranking its variants would let `vae_zseries` enter four times and every other assembler once. With
`smooth_paths="all"` (`max`) every assembler but the random path has every seam processing and the
variants are ranked. `vae_quilting` (choice of windows and boundary cut together) is one method, not a
variant, and is always ranked.
`Config.rank_exclude` / `--rank-exclude` sets the list explicitly (no names — rank every method). The
methods left out of the rankings take part in every other question and in the case study.

**Slices (leaves).** Fidelity — one metric against one real reference: train, val or OOT
(suffix `@train` / `@oot`, no suffix — val; group F10 — distance to train — is computed once,
slice "—"). Utility — TSTR of one task × model × split (val / OOT) × metric. Cost — time (total,
training, generation) and memory.

**Ranks.** Within a leaf, methods are ranked for each (dataset, seed) pair — methods of one seed
share the pool and the test rows and form a block; rank 1 is the best, ties receive the average
rank; if a method is missing from a block, the ranks of the others are rescaled to 1…k (a TSTR cell
the method's series could not train is not missing: it enters as a model that learned nothing, see
§2). Ranks are
averaged along a fixed hierarchy with equal weights at each level, so that a group with dozens of
metrics does not outweigh a group with two:

```
leaf (metric | task × model × metric) → group (F-group | task type) → criterion × slice (reference / split)
     → criterion (mean over its slices) → domain (fidelity | utility) → ranking
```

| Criterion | Groups | Slices |
|---|---|---|
| fidelity: distribution | F1, F2, F12 (outliers and extremes) | train, val, OOT |
| fidelity: dependence | F3, F4 (without calendar F4.4–F4.5: for Diffusion-TS, Chronos, TimesFM and Timestral the calendar is given) | train, val, OOT |
| fidelity: windows | F6, F9 | train, val, OOT |
| fidelity: long_structure | F7 | train, val, OOT |
| fidelity: target | F8, F11 (class balance) | train, val, OOT |
| fidelity: seams | F5 | train, val, OOT |
| fidelity: privacy | F10 | — |
| utility: classification | U2.1–U2.5 (clf., multiclass) | val, OOT |
| utility: regression | U2.6–U2.9 (regression, quantiles, multi-step, volatility) | val, OOT |
| cost | time and memory of the series | total (total time), training (generator training), generation (sampling + assembly of a new series by the trained model), memory (peak GPU memory and RSS increase) |

**Thematic slices** — separate rankings by cross-cutting properties; leaves are taken from
different groups, each metric has equal weight, and they do not enter the rankings (their
leaves are already in the criteria):

| Theme | Fidelity (train / val / OOT) | Utility (val / OOT) |
|---|---|---|
| class balance | F8.1, F11.1–F11.4 | ECE of binary classifiers: a shift of the class share in the synthetic data gives poor calibration on real data |
| outliers and extremes | F1.5 (q01, q99), F1.6 (kurtosis), F1.10 (Hill), F2.4, F7.4, F12.1–F12.5 | regression error on the extreme 10% of the target (`mae_extreme`), PR AUC of rare events |

A utility criterion includes the primary metric of the task type (AUC, log-loss, MASE, pinball) and
the models trained on all tasks of the criterion (in `min` / `mid` — linear and boosting; the MLP, trained
on one task only, is kept as a separate leaf).

**Rankings** (`leaderboard.RANKINGS`). Four rankings, each the mean of two domains with equal weight:
fidelity — the mean of the six fidelity criteria (distribution, dependence, windows, long_structure,
target, seams), each averaged over its references; utility — one criterion, TSTR on val and OOT.

| Ranking | Fidelity | Utility |
|---|---|---|
| `holdout_clf` | val, OOT | classification (val, OOT) |
| `holdout_reg` | val, OOT | regression (val, OOT) |
| `train_clf` | train | classification (val, OOT) |
| `train_reg` | train | regression (val, OOT) |

Within a fidelity criterion the references are averaged equally. Not part of the four rankings:
privacy (F10, computed once against train; its own table — the criterion `fidelity:privacy@—`), cost
(time and memory), the thematic slices. Cost is reported next to each ranking: the same ranking with
cost as a third domain of equal weight (total time and peak memory; `with_cost:<ranking>`) and the
Pareto front "rank × median time" (on the front: no other method has both a lower-or-equal rank and a
lower-or-equal time, one of them strictly lower). Training of a shared generator (the pool VAE,
Diffusion-TS in `min` / `mid`) is charged to each method and seed that uses it; times from different
hardware are not comparable. Every table in `LEADERBOARD.md` is preceded by its composition and the
meaning of each of its columns.

**Core-metric rankings** (`leaderboard.CORE_RANKINGS`, `core_<ranking>`). The same four rankings with
the fidelity domain restricted to a core set of one or two canonical metrics per criterion
(`leaderboard.CORE_METRICS`); utility is unchanged. The core rankings give the order on a small set of
metrics with a defined interpretation; the full rankings, over every fidelity leaf, are reported next to them.

| Criterion | Core metrics |
|---|---|
| distribution | F1.2 Wasserstein of values, F2.1 KS of 24 h changes |
| dependence | F3.5 log power spectrum (every lag), F4.1 weekly profile |
| windows | F6.1 discriminative score, F6.4 MMD of windows |
| long structure | F7.1 and F7.2 KS of the rolling mean and rolling spread |
| target | F11.1 class shares of every classification task |
| seams | F5.7 detectability of the seams |

The set is fixed in advance by what the metrics measure, not by how well they separated the methods
in a run: choosing the metrics that discriminate (RQ0 (c)) on the same data as the ranking would select
noise that happens to favour some method and inflate the differences.

**Normalised scores** (`normalized_summary.parquet`, `normalized.parquet`). Each core metric on the scale
random assembly (`noise_pair[0]`) = 0, real data = 1: (x − x_random) / (x_real − x_random); above 1 — closer
to the reference than the real data, below 0 — worse than a random assembly. Fidelity: against val and
train, on the series cut to the length of the real reference (`<method>@len`, seed 0), the same length
as `real`; utility: TSTR against TRTR, seeds averaged within a dataset, models fitted on every task. A
dataset is left out of a metric when its anchors differ by no more than the noise. Summary: median over
the metrics of a criterion within a dataset, then over datasets. The scores give the size of the effect
next to the ranks and do not enter the rankings.

**Anchor check** (`anchor_check.parquet`). For every fidelity metric (against val and train) and every
utility cell: per dataset, gap = |real − random assembly| and noise = median over seeds of |random −
twin|; ratio = gap / noise, median over datasets; separated — ratio > 1, i.e. the metric tells real data
from a random assembly beyond the noise. The competing methods are not used, so the check does not
depend on who wins. Computed on all seeds and separately on even and odd seeds: a flip — the verdict
differs between the two halves. Fidelity: `real` is a piece of OOT, shorter than the synthetic series,
so for distance metrics the gap is underestimated and the check is conservative. The check is a
diagnostic of the metrics; it does not change the core set.

**Domains** (`leaderboard.DOMAINS`) — fidelity or utility ranks as a whole, alongside the criteria:
fidelity against train, val, OOT and over all three (without F10), utility on val, OOT and on both.

**Uncertainty and tests.** Two-level bootstrap (datasets, then seeds within a dataset) of mean
ranks → rank interval, probability of being first and of entering the top 3. Friedman with blocks —
datasets. The top tier is the best method and all methods that are not significantly worse than it
(one-sided Wilcoxon over datasets, Holm). **Place and tier.** The place of a method is its position by mean
rank; the tier is a test against the best. The tests do not separate the places within the tier, and these
places do not reproduce between runs on different hardware (BENCHMARK.md, "Published runs"), so the
leaderboard is read by tier. Tier membership is not monotone in the place: a method that loses to the best on
almost every dataset leaves the tier even with a close mean rank, while a method with variable ranks, or one
ranked on fewer datasets because of leakage, can stay in it. Sensitivity to weights: each ranking under 2000 random
criterion weights (Dirichlet(1) within each domain) — share of first places, top 3, and Kendall τ
with equal weights. Noise check (`mid`, `max`): `vae_rand` and `vae_rand_b`, ranked together with all others, must
be indistinguishable in each criterion — two-sided Wilcoxon over datasets for the difference of
their ranks, Holm over criteria (`twin.parquet`). The Nemenyi CD is reported for reference only: with
a dozen or more methods it exceeds the rank differences this check tests.

**Result:** `artifacts/<profile>/reports/LEADERBOARD.md` and the tables in `artifacts/<profile>/leaderboard/` — `rankings.parquet` (the four rankings),
`rankings_summary.parquet` (rank, P(first) and tier in each ranking), `rankings_cost.parquet` (rank with
cost, median time and the Pareto front for each ranking),
`by_column.parquet` (each ranking, ranking with cost, domain, criterion × slice with intervals), `by_group.parquet`, `leaves.parquet`
(each leaf), `tests.parquet`, `stability.parquet`, `kendall.parquet`, `weights.parquet`,
`transfer_ratio.parquet`, `twin.parquet` (`mid`, `max`); core-metric rankings — `rankings_core.parquet`,
`rankings_core_summary.parquet`; `normalized.parquet`, `normalized_summary.parquet`, `anchor_check.parquet`.

**Overall leaderboard** (`marathonts/hypotheses/overall.py`). One ranking, its composition fixed in advance. Fidelity —
the core criteria (`CORE_METRICS`), each the mean of its ranks against train, val and OOT with equal weights:
the aim is synthetic data close to the real series, and the three parts are three pieces of it (train — the
longest and most precise reference; val and OOT — not seen by the generator); the split exists for utility,
so that TSTR has no leakage. Utility — TSTR classification and regression with equal weights, each tested on
val and OOT. Overall = the mean of the two domains. Privacy (F10) and cost are not part of it.

*Noise-aware ranks.* Within a leaf (dataset, seed, metric × reference or task × model × metric × split) two
methods whose scores differ by no more than the noise of the leaf tie: rank = 1 + #{methods better beyond
the noise} + ½ #{other methods within the noise}; with zero noise this is the ordinary average rank. Noise of
a (dataset, leaf) — the estimate of the anchor check: median over seeds of |`vae_rand` − `vae_rand_b`|, or,
without the twin (`min`), of the between-seed difference of `vae_rand`. Between seeds the pool changes too,
so the estimate bounds the within-seed noise from above and the ties are conservative. Near-identical
methods then share a place instead of splitting the ranks of the others. Ranks are averaged as in the four
rankings; uncertainty and the tier — two-level bootstrap, one-sided Wilcoxon against the first, Holm.

*Next to the rank.* Fidelity and utility ranks alone and their Pareto front; normalised scores (random
assembly = 0, real data = 1; criteria and domains averaged with the same equal weights; fidelity against
val and train — `real` is a piece of OOT); a memorisation flag — the share of synthetic windows closer to
train than the 5th percentile of real-to-real distances (F10.2) against the same share of the real OOT
piece: flagged when the median ratio over datasets is ≥ 2 and the excess is significant (one-sided
Wilcoxon over datasets, Holm over the methods). The flag does not change the rank; F10 does not tell
copying from a collapse onto typical windows. The near-copy share of the real OOT piece is itself 1 on three datasets and 0 on three
others, so the flag is raised for none of the controls of the supplementary memorisation check (section 8), an
exact copy of train included; the signed DCR ratio and the count of exact copies separate these controls and
are reported with the flag.

*Robustness.* Sensitivity variants fixed in advance: ordinary average ranks; fidelity against train
only; against val + OOT only; without the metrics with no anchor check (F5.7 — real data have no seams;
F6.1 against val — not separated from the noise); every fidelity metric instead of the core set; only the
datasets where every method is ranked — each with Kendall τ against the leaderboard. One method per
generator: each method ranked in a field of one method per generator (the random assembly represents the
VAE pool), so that many variants of one generator cannot move the others. Leave-one-dataset-out: best and
worst place. Random criterion weights: Dirichlet(1) within each domain, 2000 draws.

**Result:** `artifacts/<profile>/reports/OVERALL.md` and the tables in `artifacts/<profile>/overall/` — `overall.parquet` (the leaderboard with the
columns next to the rank), `criteria.parquet`, `variants.parquet`, `sensitivity.parquet`, `field.parquet`,
`lodo.parquet`, `weights.parquet`.

---

### RQ2. Assembly from a window pool versus long-series generators

**Question.** How does assembly from a pool of short windows compare with generating a long series as
a whole?

**Comparisons.** Each long-series generator (A: `diffusion_ts`, `chronos`, `timesfm`, `timestral`, custom ones) against
(1) the simplest assembly — the random path `vae_rand`, and (2) the **assembly median** — the median
of all pool assembly methods for each (dataset, seed, metric), the pseudo-method `assembly_median`.
The median rather than the best assembly method: the best method would be selected on the same
data on which the comparison is made.

**Metrics:** utility — TSTR on the primary metric of each task × model × split; fidelity — all
metrics against val and OOT. Noise — the larger of the between-seed spreads of generator A and of the
assembly it is compared with (§2). BH over the whole question.

**Supports:** where assembly from windows is better than, worse than or equivalent to holistic generation — by task
type, metric group and over time (val / OOT).

---

### RQ3. Within assembly: window selection × seam processing

**Question.** Do the selection and order of the windows and the processing of the seams move the series towards the real data, each against its own control, when a series is assembled from one pool?

**Comparisons** (all on one pool — noise `vae_rand` vs `vae_rand_b`, in `min` the between-seed spread of `vae_rand`).
With several pool generators (e.g. `pool_suites={"vae": …, "gan": …}`) RQ3, C3, C4 and the assembly median
of RQ2 / C2 use the pool of `noise_pair` only; the other pool's methods are ranked (RQ1, overall leaderboard,
normalised against their own pool's random assembly) and the analysis warns at start. Run the analysis with
`--noise-pair gan_rand gan_rand_b` for the contrasts within the other pool:
- (a) each selection method (`zseries`, `greedy`, `atsp`, `pctsp`, `mbb`, `knn`, `quilting`,
  `herding`) against the random path `vae_rand`;
- (b) each seam processing against the same path without processing (`*_xfade`, `*_wsola`,
  `*_quilt` against `vae_zseries`; in `max` against every assembler);
- (c) the **main effect of each processing** (processing − no processing, averaged over the assemblers
  that have every processing: `vae_zseries`; in `max` every assembler except the random path).

The random path has no seam processing, so there is no factorial contrast "selection × processing"
with a random level.
In `min` and `mid` (b) and (c) rest on the published results of `vae_zseries`, whose code is not part of the
repository (§3.9).

**Metrics:** as in RQ2. BH over the whole question. The smallest effect size of interest is the
same for all comparisons and contrasts — the noise of §2: it is a threshold of practical significance,
not an estimate of the contrast's variance (for main effects, which are means over several methods, the
variance is smaller).

**Supports:** the contribution of each assembly factor. Comparing a specific
method with its controls is the case study (§4).

---

### RQ4. Does fidelity predict utility

**Question.** Which fidelity metrics — and against which reference — tell us which synthetic data
will train models better?

**How it is tested.** For each fidelity metric (oriented: higher is better; against train, val and
OOT) and each utility criterion (transfer ratio of a task family on val or OOT; median over seeds,
tasks and models of the criterion), Spearman ρ across methods is computed within a dataset. Over
datasets: median ρ, share of datasets with ρ > 0, Wilcoxon of ρ against 0, BH over all
"metric × criterion" pairs. A metric is *predictive* if p_BH < α and median ρ > 0.

**Result:** a table of metrics with ρ; a summary by reference (`by_reference`: whether fidelity
against OOT predicts better than against val or train) and by metric group (`by_group`), the top 5
predictors of each criterion. In the ranking the same is visible as Kendall τ between the fidelity
and utility criteria.

**Supports:** which metrics are associated with utility among the compared methods, as candidates for
selecting generators without training models.
**Does not support:** causality, or selection of a generator outside the compared families (methods that
share a pool or a generator are not independent observations).

---

### RQ5. Gap to real data and robustness

**Question.** (a) How does each method's TSTR compare with TRTR? (b) Is the ranking stable over
time (val → OOT) and across model classes (linear ↔ boosting)? (c) Do decisions made on synthetic
data transfer to real data?

**How it is tested.**
- (a) Transfer ratio by method × criterion × split: median over datasets, bootstrap interval over
  datasets, one-sided Wilcoxon (ratio − 1 < 0) over datasets, BH. Verdict `worse than real` or
  inconclusive.
- (b) Kendall τ between the val ↔ OOT and model ↔ model (linear ↔ gbdt; every pair of models fitted on every
  task of a criterion) rankings (from the ranking) and the
  rank shift OOT − val of each method.
- (c) Only the `max` profile (`decision_transfer=True`): Spearman between the ranking of a grid of
  11 model configurations on real data and on the method's synthetic data (U6.1), threshold
  transfer (U6.4).

---

### RQ6. Speed and cost

**Question.** How fast is each method — in training and in generating a new series — how much
memory does it need, and which methods lie on the Pareto front "quality × time"?

**How it is tested.** Median total time over datasets with a bootstrap interval, time relative to
the fastest, slope of log(time) on log(K) with bootstrap over datasets (how time grows with series
length); cost components — generator training, generation of a new series by the trained model
(sampling + assembly), peak GPU memory, RSS increase (`cost_parts`); cost ranks over these slices
with the tests from the ranking (`cost_ranks`); for each of the four rankings of RQ1 the Pareto front
"rank × time" and the rank with cost as a third domain (`pareto`). Generation is separated from training because in practice a
generator is trained once, while series are generated many times. Times from different hardware are
not comparable — the report warns about this.

---

### RQ7. Moderators (exploratory)

**Question.** How do the effects of method families vary with dataset properties?

**Test:** Spearman between dataset descriptors (ACF at 24 and 168, kurtosis of increments,
volatility clustering, trend, share of missing values) and the dataset effects from RQ2 and the
main effects of RQ3 (median over metrics, in noise units), BH. With 9 datasets — exploratory only.
Needs the prepared data (`data/processed`, for the descriptors) and at least 4 datasets with an effect;
without the data RQ7 and CS15 are skipped with a message, the rest of the report is unaffected.

---

### RQ8. Class balance

**Question.** Do the methods preserve class shares in all classification tasks — above all for rare
events — and how much does an error in the share cost for models trained on synthetic data?

**How it is tested.**
- (a) Ranking on the "class balance" theme (RQ1) with Friedman tests and Wilcoxon against the best.
- (b) Family comparisons on the theme's metrics (F8.1, F11 against val and OOT; TSTR ECE of binary
  and multiclass tasks where computed): each assembly method against the random path (pool noise) and each long-series generator
  against the assembly median (between-seed spread of the generator); BH over the question.
- (c) Relation: within a dataset, Spearman across methods between each balance metric and the
  theme's utility (mean ECE rank), Wilcoxon over datasets, BH — whether a wrong class share explains
  poor TSTR calibration.

**Why separately.** A random assembly of windows preserves the class share only on average; any
method may shift class shares or under-represent rare events (F11.4). In fidelity aggregates such
shifts are averaged with dozens of other metrics.

---

### RQ9. Outliers and extremes

**Question.** Do the methods preserve the tails, outliers and extremes of the real series, and does
this matter for models that must predict extremes?

**How it is tested.** As RQ8, on the metrics of the "outliers and extremes" theme: fidelity — tail
quantiles, kurtosis, Hill index, large jumps, outlier durations, F12 (frequency and magnitude of
exceedances of the real 0.5% / 99.5%, local spikes, weekly maxima and minima); utility — regression
error on the extreme 10% of the target and PR AUC of rare events. (a) Theme ranking, (b) family
comparisons, (c) relation of fidelity tail metrics to quality on extremes.

**Why separately.** Generation and seam processing can change the tails of the series and the
spikes at window boundaries; metrics over the whole distribution are little affected by such changes.

---

### 3.9. Confirmatory family C1–C4

Two pre-specified cells: **classification** — U2.1 (upper tail, h = 24, q = 0.90), AUC, and
**regression** — U2.6 (h = 24), MASE; both — TSTR, linear model, OOT
(`questions.CONFIRMATORY_CELLS`). In each cell:

| Test | What it tests | How |
|---|---|---|
| C1 | whether the methods differ at all | Friedman over the methods of the default ranking (not changed by `--rank-exclude`), blocks — datasets; a method left out on a dataset (`Config.leaked`) drops out of the test, the dataset stays |
| C2 | `diffusion_ts` and `chronos` against the assembly median | as RQ2, noise — the larger of the two between-seed spreads; the composition is fixed (`CONFIRMATORY_GENERATORS`): custom long-series generators are compared in RQ2 but do not enter the family |
| C3 | main effect of window selection | the mean of every selection strategy of the default ranking (no seam processing) against the random path |
| C4 | main effect of seam processing | all processings against no processing, averaged over the assemblers that have every processing (`vae_zseries`; `max`: every assembler but the random path) |

In total 10 tests (2 + 4 + 2 + 2) with a single Holm correction on the two-sided p. Verdict: C1 —
`differ` / inconclusive; C2–C4 — better / worse if p_Holm < α and |median z| > 1, same if TOST
(Holm) is significant.

In `min` and `mid` the seam processing runs over `vae_zseries` only (`smooth_paths=["zseries"]`), whose code is not
part of the repository (`frozen_methods`). C4 and RQ3 (b, c) therefore rest on its published results: they can be
checked from the tables, not recomputed. The seam processings themselves are open; `smooth_paths=["greedy"]` (or
any open assembler) computes them over an open path — an addition outside the pre-specified protocol, not a
replacement of C4.

## 4. Case study: one method against its controls

The questions of §3 compare families. The case study answers a question about one method — by
default `vae_zseries` (`Config.case_method`, flag `--case-method`): how it compares with its controls on the
same pool (`vae_rand`), other assemblers of the same pool and long-series
generators, and what drives it. Below, "the method under study" is this method; the sign of the
effect d > 0 means it is better than the method it is compared with. The case study is secondary
(BH within a hypothesis; the pre-specified cell CS7 + CS10 — Holm within it) and does not enter the
confirmatory conclusion of the benchmark. `vae_zseries` is zseries, the proprietary assembler of zypl.ai (under development): the case study reports its
results against its controls; its code is not part of the repository (`Config.frozen_methods`). The benchmark evaluates the quality of synthetic data (TSTR
versus TRTR), not the benefit of augmentation.

### CS1. Distribution and dependence against train

**Hypothesis.** `vae_zseries` is better than `vae_rand` on the metrics of the marginal distribution,
increments and temporal dependence measured against train — the data the pool generator was trained on.

**Metrics:** the metrics of F1–F3 against train (`@train`), except F3.2 (it belongs to CS4).

**Comparison and test:** against `vae_rand`; BH.

**Supports:** that the method changes the distribution and dependence of the series relative to a random
assembly of the same pool.
**Does not support:** realism on unseen data (this is CS2) or usefulness for models (CS7, CS8, CS13).

---

### CS2. Distribution and dependence against val

**Hypothesis.** `vae_zseries` is better than `vae_rand` on the same metrics measured against val.

**Metrics:** the metrics of F1–F3 against val, except F3.2.

**Comparison and test:** against `vae_rand`; BH.

**Supports:** that what the method changes against train holds on unseen data. Read together with CS1.
**Does not support:** usefulness for models (this is CS7, CS8, CS13); realism of long structure (CS4) and of seams (CS3).

---

### CS3. Seam artefacts

**Hypothesis.** The seams of `vae_zseries` are less noticeable than those of a random assembly.

**Metrics:** F5.1–F5.7. Checks: F5.4 (local ACF), F5.5–F5.6 (a change-point detector finds the seams), F5.7 (a
classifier distinguishes a segment containing a seam from a random one).

**Comparison and test:** against `vae_rand`; BH. In addition, in CS9 and CS10 the seams are
compared with the chunks of the generation of Diffusion-TS, Chronos and Timestral (there a
"seam" is a chunk boundary).

**Supports:** that the method changes the seam metrics relative to a random assembly.
**Does not support:** that the seams are indistinguishable from real transitions: for that, F5.7
should be about 0.5, while the comparison with `vae_rand` only says "better than random".

---

### CS4. Structure longer than a window

**Hypothesis.** `vae_zseries` is better than `vae_rand` on properties at scales larger than the window
length T.

**Metrics:** F3.2 (ACF at lags T…3T), F6.4 on 2T
windows (MMD of windows spanning a seam), F7.1–F7.7 (rolling statistics, level crossings, outlier
durations, drawdowns, trend, regimes).

**Comparison and test:** against `vae_rand`; BH.

**Supports:** a difference between assembly and random assembly of short windows in the long
structure of the series.
**Does not support:** that the long structure is better than that of a long-series generator (this
is CS9).

---

### CS5. Target structure

**Hypothesis.** `vae_zseries` is better than `vae_rand` on the metrics of the target: class shares and
event dynamics.

**Metrics:** F8.1 (class shares), F8.2 (event duration), F8.3 (time between events), F8.4 (events by
hour of the week), F8.5 (conditional probability of an event given features), F8.6 (conditional
distribution of the future change).

**Comparison and test:** against `vae_rand`; BH.

**Supports:** that the method changes the target structure of the series relative to a random
assembly of the same pool.
**Does not support:** usefulness for a classifier (this is CS7).

---

### CS6. Assembly does not change the realism of individual windows and does not increase memorisation

**Hypothesis (equivalence).** `vae_zseries` and `vae_rand` **do not differ** on metrics of individual
windows of length T and on memorisation.

**Metrics:** F6.1, F6.2, F6.4 (T windows), F6.6, F6.8, F9.1–F9.2, F10.1–F10.2.

**Comparison and test:** against `vae_rand`; expected verdict "same" (TOST); BH.

**Why.** Assembly does not change the content of windows; it only selects and orders them. Hence,
on metrics of individual windows it should coincide with a random assembly. If assembly is
"better" on them, it systematically selects more typical windows; F9.1 (recall, coverage) then shows
whether diversity decreases.

**Supports:** that the effects of CS2–CS4, if any, are obtained by ordering and selection, without loss of
diversity and without copying train.
**Does not support:** that VAE windows are realistic in an absolute sense — this is a property of
the generator, visible in CS9.

---

### CS7. TSTR against a random assembly — pre-specified cell of the case study

**Hypothesis.** On task U2.1 (`stitch_task`), a model trained only on `vae_zseries` synthetic data performs better
on real data than one trained only on `vae_rand` synthetic data. TRTR is common
to all methods (the same real data, the same model seed), so "higher TSTR" and "closer to TRTR" are
the same thing.

**Metrics:** task U2.1 (upper tail, h = 24, q = 0.90), ROC AUC — the task of the case-study cells
(`stitch_task`); it carries no extra weight in the benchmark. The pre-specified cell of the case study is the linear model, OOT (Holm together with CS10, `case_cell.parquet`); the other models and val
are secondary. It does not enter the benchmark's confirmatory family (§3.9).

**Comparison and test:** against `vae_rand`; noise — a pair of random assemblies of one pool (`min`: the
between-seed spread of `vae_rand`); Holm; block bootstrap over test rows.

**Supports:** that it is the assembly, and not the VAE pool itself (`vae_rand`), that brings the
synthetic data closer to real data.

**Does not support:** transfer to other tasks (CS8) and models (CS11).

---

### CS8. TSTR on the other tasks

**Hypothesis.** TSTR of `vae_zseries` is higher than TSTR of `vae_rand` on tasks
U2.2–U2.9: other horizons, rare events, lower tail, multiclass, regression, quantiles, multi-step
forecasting, volatility.

**Metrics:** the primary metric of the task — AUC (binary), log-loss (multiclass), MASE
(regression, multi-step forecasting, volatility), pinball (quantiles). All models and both splits.

**Comparison and test:** against `vae_rand`; BH.

**Supports:** that assembly brings the whole series closer to the real one across tasks.
`clf_down_h24_q10` is the opposite tail.

**Does not support:** that the effect is the same across tasks. The per-task verdicts are the
answer to "where better, where worse".

---

### CS9. Fidelity against other assemblers and long-series generators

**Hypothesis (two-sided).** On which metrics the method under study is better than, worse than or equivalent to
(a) other ways of assembling a series from the same VAE pool — sections A and B of
[BASELINES.md](BASELINES.md): `vae_greedy`, `vae_atsp`, `vae_pctsp`, `vae_mbb`,
`vae_knn`, `vae_quilting`, `vae_herding`, `vae_zseries_{xfade,wsola,quilt}`; (b) the long-series
generators (`baselines`, by default all four: Diffusion-TS, Chronos, TimesFM, Timestral).

**Metrics:** all F-metrics against val except F4.4–F4.5: calendar coherence is given by
construction for the long-series generators (Diffusion-TS: the calendar is imposed from a random start; Chronos, TimesFM
and Timestral: the real calendar continues train), whereas the pool generators (VAE) generate it as part of a window,
so these two metrics measure different things for the two groups and are left out.

**Comparison and test:** against each method of (a) — the noise of a pair of random assemblies
(the same pool); against (b) — the between-seed spread of the method under study; BH over all comparisons of the
hypothesis together. The result is read by metric group (F1…F12) and by dataset.

**Supports:** a "where better / where worse" map relative to all alternatives. The comparison with
`vae_herding`
separates the effect of window selection from that of their order; with `vae_zseries_{xfade,wsola,quilt}`
— what seam processing adds on top of the method's own path.

**Does not support:** that a difference from (b) is due to assembly rather than the VAE. This is
separated by the pair CS9 + CS2/CS4: if `vae_rand` also differs from the baseline in the same
direction, the difference is attributed to the generator, not to the assembler.

---

### CS10. TSTR against other assemblers and long-series generators

**Hypothesis (two-sided).** On which tasks and models the TSTR of the method under study is higher than, lower than
or equivalent to the TSTR of (a) other assemblers of the same pool (as in CS9) and (b) the long-series
generators (as in CS9).

**Metrics:** primary metrics of all tasks, regime S. **Test:** against (a) — the noise of a pair of
random assemblies, against (b) — the between-seed spread of the method under study; BH over all comparisons
together. The cell "U2.1, linear model, OOT, AUC" against Diffusion-TS and Chronos (fixed in advance,
`PRESPECIFIED_LONG`) enters the pre-specified cell of the case study (Holm together with CS7).

**Supports:** a practical comparison: whose synthetic data are more useful to models.

**Does not support:** the reason for the differences. This is shown by the comparison with CS7: if
`vae_rand` also scores below the baseline, the difference is attributed to the VAE generator, not to
the assembler.

---

### CS11. The effect of assembly on TSTR does not depend on the model class (exploratory)

**Hypothesis.** The effect of assembly (S `vae_zseries` − S `vae_rand`) has the same sign and a comparable
size for the linear model, boosting and MLP.

**Test:** Friedman across models with datasets as blocks: tasks, splits and seeds within a dataset
are averaged (they share a series and are not independent as separate blocks); before averaging,
the effect of each task is divided by a single number — the median |effect| of that task over all
models — so that tasks of different scales are comparable and the order of models does not change.
Share of blocks where the sign of the effect coincides for all models. Only tasks on which all
models are trained enter: in `min` and `mid` the MLP is trained only on U2.1, so there
CS11 is about U2.1; in `max` — all 14 tasks (without XGBoost the fallback boosting has no multi-step
task, which then drops out).

**Supports:** that the effect is not an artefact of one model.

**Does not support:** transfer to models outside the set (sequential networks, MiniRocket).

---

### CS12. The effect is stable over time and across subgroups

**Hypothesis.** (a) The effect on the TSTR of the case-study task (U2.1) is the same on val and on OOT (the shift
in time does not destroy it). (b) The effect is not concentrated in one subgroup of test rows:
weekends / weekdays, calm / medium / turbulent periods (volatility terciles).

**Test:** (a) for each dataset, the shift of the effect `d_OOT − d_val` (mean over seeds) is
divided by the median of the same shift for the noise pair (`vae_rand − vae_rand_b`) — this is also
a difference of differences, with the same variance (`min`, without the twin: the between-seed spread of
the shift of `vae_rand`); TOST ±1 over datasets, against `vae_rand` and every long-series generator
(`baselines`); BH. (b) ΔAUC within subgroups over rows (regime S), Wilcoxon over
datasets, BH — exploratory; requires `data/processed` (calendar and volatility of the test rows),
skipped without it.

**Supports:** that the conclusion of CS7 is not an accident of one period or market regime.

**Does not support:** stability at horizons beyond OOT.

---

### CS13. TSTR of the method under study against TRTR

**Hypothesis (two-sided).** A model trained only on `vae_zseries` synthetic data (TSTR, regime S) is worse
than, better than or as good as a model trained on the real train (TRTR, regime R) on real val / OOT.

**Metrics:** the primary metric of each task (AUC, log-loss, MASE, pinball), all models and both
splits. In addition — the **transfer ratio** of each method (TSTR relative to TRTR; 1 means the
synthetic data train the model as well as real data): for AUC — (TSTR − 0.5) / (TRTR − 0.5), the
share of quality above chance; for other "higher is better" metrics — TSTR / TRTR; for losses —
TRTR / TSTR. Tables `CS13_transfer_ratio_case_cell` (pre-specified cell by dataset) and
`CS13_transfer_ratio_by_task`.

**Comparison and test:** `vae_zseries` in regime S against `real` in regime R; general procedure (noise —
the between-seed spread of the method under study); BH. Over test rows — block bootstrap of ΔAUC by weeks for
seed-averaged predictions (U2.1).

**Supports:** how close the synthetic data are to real data in terms of information useful to the
model: a verdict of same means TSTR is equivalent to TRTR within the margin for this task and model.

**Does not support:** that the closeness is due to assembly — this is CS7 / CS8; who is closest to
TRTR — RQ1.

---

### CS14. Computational cost

**Hypothesis (two-sided).** (a) The total time of the method under study (VAE training + pool sampling + assembly)
is lower than, higher than or the same as (±10%) that of every other method (the random path, the alternative
assemblers, the long-series generators), and how much the
assembly itself adds compared with a random assembly. (b) Assembly time grows polynomially with
K; the exponent is estimated.

**Metrics:** `fit_wall_s`, `sample_wall_s`, `assemble_wall_s`, `total_wall_s`, peak GPU memory and
RAM — recorded by the benchmark for each run together with the hardware.

**Test:** Wilcoxon on the log ratio of times (over datasets), TOST ±10%, bootstrap interval of the
ratio; slope of log(time) on log(K) with bootstrap over datasets.

**Supports:** the cost of quality and scalability to long series (PJM, K = 519).
**Does not support:** anything if times were measured on different hardware — the analysis issues a
warning when the table contains more than one GPU type.

---

### CS15. Moderators: where assembly is better or worse (exploratory)

**Hypothesis.** The size of the assembly effect (CS2, CS4, CS7, CS10) is related to dataset properties:
daily (ACF 24) and weekly (ACF 168) seasonality, heaviness of the increment tails, volatility
clustering, trend, length K, share of missing values.

**Test:** Spearman correlation between the dataset effect (in noise units) and a descriptor, BH.
With 9 datasets — exploratory only.

**Supports:** hypotheses about which series show a larger or smaller assembly effect.
**Does not support:** a causal relationship — 9 points and many correlated descriptors.

## 5. Metrics, questions and case study

| Metrics | Questions | Case study |
|---|---|---|
| all F-metrics against train, val and OOT | RQ0 (c, d), RQ1, RQ4 | — |
| F-metrics against val and OOT | RQ2, RQ3 | — |
| F1–F3 against train | RQ0–RQ4 | CS1 |
| F1–F3 against val | RQ0–RQ4 | CS2, CS9 |
| F3.2, F6.4 (2T), F7.1–F7.7 | RQ0–RQ4 | CS4, CS9 |
| F4.1–F4.3 | RQ0–RQ4 | CS9 |
| F4.4–F4.5 (calendar: given for Diffusion-TS, Chronos, TimesFM, Timestral; generated by the pool generators) | RQ0 (a, b) only | — |
| F5.1–F5.7 | RQ0–RQ4 (seams criterion) | CS3, CS9 |
| F6.1–F6.8, F9.1–F9.2 | RQ0–RQ4 | CS6, CS9 |
| F8.1–F8.6 | RQ0–RQ4 | CS5, CS9 |
| F10.1–F10.2 | RQ0, RQ1 (privacy, ranked separately), RQ4 | CS6, CS9 |
| F8.1, F11.1–F11.4; ECE of binary tasks (TSTR) | RQ1 ("class balance" theme), RQ8 | CS5 (F8.1), CS9 (F11) |
| F1.5, F1.6, F1.10, F2.4, F7.4, F12.1–F12.5; `mae_extreme`, PR AUC of rare events (TSTR) | RQ1 ("outliers and extremes" theme), RQ9 | CS2 (F1, F2), CS4 (F7.4), CS9 (all F-metrics) |
| F9.4 (diversity across seeds) | descriptive, in the `cross_seed` table | — |
| all tasks, regime S (TSTR), primary metric | RQ0 (c), RQ1, RQ2, RQ3 | CS7, CS8, CS10 |
| all tasks, all metrics, regime S | RQ1 (leaves) | — |
| all tasks, regime S against R (TRTR): transfer ratio | RQ1 (effect size), RQ4, RQ5 | CS13 |
| U2.1 (AUC) and U2.6 h = 24 (MASE), linear model, OOT | confirmatory family C1–C4 | — |
| U6.1, U6.4 | RQ5 (c) | — |
| `*_wall_s`, `*_gpu_peak_mb`, `*_rss_delta_mb` | RQ1 (cost slices, rankings with cost), RQ6 | CS14 |
| dataset descriptors | RQ7 | CS15 |

A metric, task or model added to the benchmark (EXTENDING.md) does not change the procedure — only the
set of leaves and units of analysis.

## 6. How to read the result

1. **Confirmatory conclusion** (`REPORT.md`, after the overall leaderboard) — the main conclusion of the paper:
   whether the methods differ (C1), how assembly from windows compares with long-series
   generators (C2), what window selection (C3) and seam processing (C4) contribute — in
   classification and regression.
2. **Overall leaderboard** (`OVERALL.md`, first section of `REPORT.md`) — one
   order of the methods by fidelity and utility, the top tier and how stable it is under the sensitivity
   variants, a field of one method per generator, dataset removal and random weights.
3. **Ranking** (`LEADERBOARD.md`) — the order of methods in each slice, the top tier, rank intervals; how
   stable the ranking is with respect to the reference, split, model and weights.
   **Metric values** (`METRIC_VALUES.md`) — the measured values behind the ranks: the core fidelity metrics
   and the primary utility metrics by reference, dataset, task, model and split, TRTR (`real`) for scale.
4. **Questions RQ0–RQ9** — a map of "where better, where worse, where the same" by method family
   with false discovery rate control; RQ0 — which metrics can be relied on, RQ4 — which of them
   predict utility.
5. **Case study** — secondary: where one method differs from its controls and alternatives.

All four reports are in `artifacts/<profile>/reports/`.

Inconclusive is not "no effect" but "the effect is smaller than the noise or inconsistent across
datasets". "Same" is demonstrated equivalence.

## 7. Pipeline

The analysis (`marathonts/hypotheses/`) runs on the benchmark tables ([BENCHMARK.md](BENCHMARK.md)). It does
not generate data or train generators: it needs `artifacts/<profile>/tables/*.parquet`, and the case study
also needs the utility predictions and labels (`artifacts/<profile>/utility`, `artifacts/<profile>/labels`); dataset
descriptors (RQ7, CS15) and the CS12 subgroups read `data/processed` (without it these parts are
skipped). It runs on CPU. The per-dataset tests of all comparisons run as matrices (the exact
sign-flip permutation test that scipy's Wilcoxon uses for tied or zero differences with ≤ 13 seeds
is computed in one matrix product, with the same p-values), and every bootstrap draws all its
resamples at once.

### Data flow

```
artifacts/<profile>/tables/fidelity.parquet  (metrics against val, @train, @oot)
artifacts/<profile>/tables/utility.parquet   (TSTR / TRTR × task × model × val / OOT)
artifacts/<profile>/tables/timing.parquet
        │
        ├─► leaderboard.py: rank per (dataset, seed) in each leaf → group → criterion × slice → criterion → domain → four rankings
        │      rank bootstrap, Friedman, Wilcoxon against the best (Holm), Kendall τ, weights → leaderboard/, reports/LEADERBOARD.md
        │
        ├─► questions.py: RQ0–RQ9 — long tables (dataset, seed, unit, method, value)
        │      noise: median |vae_rand − vae_rand_b| (or between-seed spread of method A)
        │      pairs / contrasts: d = orientation · (A − B) → per dataset and globally → BH → verdict
        │      confirmatory family C1–C4 → Holm → confirmatory.parquet
        │
        ├─► overall.py: noise-aware ranks, robustness checks → overall/, reports/OVERALL.md
        │
        ├─► metric_values.py: median / IQR over seeds of every metric → metric_values/, reports/METRIC_VALUES.md
        │
        └─► catalog.py: case study CS1–CS15 (method --case-method) + row-level bootstrap by weeks
                                           ▼
             hypotheses/RQ*_*.parquet, CS*_*.parquet, confirmatory.parquet; reports/REPORT.md
             (folders under artifacts/<profile>/)
```

### Modules

| File | What it does |
|---|---|
| `marathonts/hypotheses/stats.py` | tests: Wilcoxon, sign, t-test, TOST, Hodges–Lehmann, rank-biserial, Holm, BH, two-level and block bootstrap, Friedman + Nemenyi, Page. DeLong, Diebold–Mariano and Stouffer are implemented but not used in the conclusions: test rows are autocorrelated, and the seeds share one test |
| `marathonts/hypotheses/engine.py` | noise, paired differences, per-dataset and global summary, verdicts |
| `marathonts/hypotheses/overall.py` | overall leaderboard: noise-aware ranks, next-to-the-rank columns, robustness checks (RQ1) |
| `marathonts/hypotheses/leaderboard.py` | ranking of all methods in all slices (RQ1) |
| `marathonts/hypotheses/metric_values.py` | values of the core fidelity metrics and the primary utility metrics by reference, dataset, task, model and split (median and IQR over seeds) |
| `marathonts/hypotheses/questions.py` | RQ0–RQ9 and the confirmatory family C1–C4 |
| `marathonts/hypotheses/catalog.py` | loading of long tables, transfer ratio, case study CS1–CS15 |
| `marathonts/hypotheses/run.py` | runs everything, writes the tables and the reports `REPORT.md`, `OVERALL.md`, `LEADERBOARD.md`, `METRIC_VALUES.md` to `reports/` |

### Running

```bash
python -m marathonts.hypotheses.run                        # questions, ranking, metric values, case study
python -m marathonts.hypotheses.run --no-case-study        # questions, ranking and metric values only
python -m marathonts.hypotheses.run --only RQ2 RQ3         # selected questions only: no confirmatory family, overall leaderboard,
                                                #   ranking files, metric values or case-study pre-specified cell
python -m marathonts.hypotheses.overall                    # overall leaderboard only → artifacts/<profile>/overall/, reports/OVERALL.md
python -m marathonts.hypotheses.leaderboard                # ranking only → artifacts/<profile>/leaderboard/, reports/LEADERBOARD.md
python -m marathonts.hypotheses.metric_values              # metric values only → artifacts/<profile>/metric_values/, reports/METRIC_VALUES.md
python -m marathonts.hypotheses.run --artifacts-dir /content/drive/MyDrive/marathonts_artifacts --out-dir /tmp/hyp   # base folder: /tmp/hyp/reports, hypotheses, overall, leaderboard, metric_values
python -m marathonts.hypotheses.run --plugins my_tests.py  # custom tests and hypotheses (EXTENDING.md)
python -m marathonts.hypotheses.run --case-method gan_greedy --noise-pair gan_rand gan_rand_b   # case study of another method
python -m marathonts.hypotheses.run --config cfg.json      # run settings (Config.to_json)
python -m marathonts.hypotheses.run --rank-exclude         # rank every method (names: the list of methods left out of the rankings)
python -m marathonts.hypotheses.run --no-fail-penalty      # leave out the TSTR cells a series could not train (§2)
python -m marathonts.hypotheses.run --exclude-datasets bitcoin --exclude-metrics F6.1_disc_score@val --leaked '{}'   # analysis choices (CONFIGURATION.md)
```

### Results

`--out-dir X` sets the base folder in place of `artifacts/<profile>/`: the reports go to `X/reports/`, the tables
to `X/hypotheses/`, `X/overall/`, `X/leaderboard/` and `X/metric_values/`. `python -m marathonts.hypotheses.overall --out D`,
`python -m marathonts.hypotheses.leaderboard --out D` and `python -m marathonts.hypotheses.metric_values --out D` write the tables to `D`
and the report to `D/../reports/`.

| File | Contents |
|---|---|
| `artifacts/<profile>/reports/REPORT.md` | human-readable report: overall leaderboard, confirmatory family, RQ0–RQ9, case study CS1–CS15 |
| `artifacts/<profile>/reports/OVERALL.md`, `artifacts/<profile>/overall/*.parquet` | overall leaderboard (list of files — §3, RQ1, **Overall leaderboard**) |
| `artifacts/<profile>/reports/LEADERBOARD.md`, `artifacts/<profile>/leaderboard/*.parquet` | ranking (list of files — §3, RQ1, **Result**) |
| `artifacts/<profile>/reports/METRIC_VALUES.md` | values of the core fidelity metrics and the primary utility metrics by reference, dataset, task, model and split: fidelity per real reference (method × metric, median over datasets of the median over seeds; `real` — the real OOT part scored as a series) and per core metric (method × dataset); utility primary metric per model and test split (method × task, TRTR first); the pre-specified cells per dataset; the cells a method's series could not train |
| `artifacts/<profile>/metric_values/fidelity.parquet`, `utility.parquet` | median and IQR over seeds of every metric × reference and task × model × split, per dataset and method |
| `artifacts/<profile>/hypotheses/confirmatory.parquet` | confirmatory family C1–C4 with Holm correction and verdict |
| `artifacts/<profile>/hypotheses/RQ*_global.parquet` | per unit of analysis and comparison: effect in noise units, interval, p before and after correction, number of datasets with each verdict, global verdict |
| `artifacts/<profile>/hypotheses/RQ*_per_dataset.parquet` | the same for each dataset: n seeds, effect, noise, p, verdict |
| `artifacts/<profile>/hypotheses/RQ*_<extra>.parquet` | additional tables (real-versus-real reference, discriminative power, redundancy, predictors, stability, Pareto) |
| `artifacts/<profile>/hypotheses/CS*_*.parquet`, `case_cell.parquet` | case study and its pre-specified cell |

### What is required from the benchmark

- All methods of the profile on the same seeds (in the tables: 16 in `min` — 12 run by the pipeline and the
  4 published results of `frozen_methods` —, 17 in `mid`, 35 in `max`). Without `vae_rand_b`
  (`min`) the noise is the between-seed spread of `vae_rand` and RQ0 (a) and the noise check of RQ1 are
  skipped; without `vae_rand` — no RQ2 (1), RQ3 and C3; without seam-processing variants — no RQ3 (b, c)
  and C4. Without TRTR (`real`, regime R) there
  is no transfer ratio (RQ4, RQ5).
- Fidelity against three references: `Config.fidelity_extra_refs = ["train", "oot"]` (default).
  Tables without `@oot` metrics give the ranking and RQ4 without the OOT slice.
- Run configuration: `hypotheses.run` takes it from `artifacts/<profile>/tables/config.json`
  (written by the `collect` stage).
- At least 3 seeds for per-dataset tests; 10 are planned (minimal p ≈ 0.001).
- At least 3 datasets for global tests; 9 are planned.
- A timing table from a single hardware type for RQ6.

### Custom methods, tests and hypotheses

- A method (`bench.methods.register_method`, EXTENDING.md) enters the ranking and RQ0–RQ9
  automatically; its family is determined from its description.
- A statistical test: `hypotheses.stats.register_test(name, level="dataset" | "global")` — the
  test's columns are added to all comparison tables.
- A hypothesis about a specific method: `hypotheses.catalog.register_hypothesis("CS16", "title")` —
  appears in the report together with the case study.
- Case-study roles: the method (`--case-method`), the noise pair (`--noise-pair`), baselines (`--baselines`), the task of the case-study cells (`--case-task`, by
  default `Config.stitch_task`).

Examples — [EXTENDING.md](EXTENDING.md).

## 8. Supplementary analyses (not pre-specified)

Checks added after the main run, in answer to review. They do not change the pre-specified analysis, and their
verdicts are exploratory. All run on CPU in seconds to minutes, locally or in Colab, after the analysis stage
(`python -m marathonts.hypotheses.run`); no GPU and no new generation are needed.

| Check | Command | Input | Output |
|---|---|---|---|
| The analysis with the zEDGE pool in place of the VAE pool (assembly median of RQ2 / C2, contrasts of RQ3 / C3 / C4) | `python -m marathonts.hypotheses.run --artifacts-dir <run> --noise-pair zedge_rand zedge_rand_b --no-case-study --out-dir <run>/supplementary/zedge_pool` | `<run>/tables/` | `artifacts/run_h200/supplementary/zedge_pool/` |
| Pools: values replaced for NaN, range of the value, flat windows | `python -m marathonts.hypotheses.pool_check --artifacts-dir <run>` | `<run>/pools/` (Hugging Face; not for ETT and PJM) | `artifacts/run_*/supplementary/pool_check/` |
| Calendar of the series: share of steps at which the hour of the week advances by one, error of the hour of the week inside a piece against the closest valid calendar | `python -m marathonts.hypotheses.calendar_check --artifacts-dir <run>` | `<run>/series/` (Hugging Face; not for ETT and PJM) | `artifacts/run_*/supplementary/calendar_check/` |
| The analysis without the fidelity metrics that use the calendar of the series (value-only fidelity; utility unchanged, since every task uses the hour of the week as a feature) | `python -m marathonts.hypotheses.run --artifacts-dir <run> --no-case-study --exclude-metrics F3.8_calendar_corr_err F4.1_how_mean F4.2_how_std F4.3_hod_mean F4.4_calendar_continuity F4.5_calendar_seam_breaks F8.4_event_by_how --out-dir <run>/supplementary/value_only` | `<run>/tables/` | `artifacts/run_h200/supplementary/value_only/` |
| Noise margin under other estimators (supplementary): every pair of seeds, random orderings of the seeds, a margin ×0.5 and ×2 | `python -m marathonts.hypotheses.run --artifacts-dir <run> --no-case-study --noise-estimator pairs` (or `perm:<n>`, or `--noise-scale 0.5`) `--out-dir <variant>` | `<run>/tables/` | `artifacts/run_h200/supplementary/noise_sensitivity/<variant>/` (global verdicts of RQ2, RQ3, C1–C4) |
| Noise check: the margins, their zero and near-zero values, and the verdicts that change under the variants | `python -m marathonts.hypotheses.noise_check --analysis-dir <run> --variant pairs=<dir> perm1=<dir> …` | the outputs above | `artifacts/run_h200/supplementary/noise_check/` |
| Bootstrap interval of the median over datasets (the statistic of the reported effect) next to the pre-specified interval of the mean; verdicts unchanged | `python -m marathonts.hypotheses.run --artifacts-dir <run> --no-case-study --ci-stat median --out-dir <dir>` | `<run>/tables/` | `artifacts/run_*/supplementary/ci_median/` (global tables of RQ2, RQ3 and C1–C4) |
| Utility cells a series could not train: counts by method, task and model, and the reason (one-class labels, no rows, or a failed fit) | `python -m marathonts.hypotheses.failure_check --artifacts-dir <run> --series-dir <run>/series` | `<run>/tables/`, `<run>/series/` (Hugging Face; not for ETT and PJM) | `artifacts/run_*/supplementary/failure_check/` |
| The analysis with a fixed chance-level penalty for such cells, and with the cells left out | `python -m marathonts.hypotheses.run --artifacts-dir <run> --no-case-study --fail-rule chance` (or `--no-fail-penalty`) `--out-dir <dir>` | `<run>/tables/` | `artifacts/run_*/supplementary/fail_rule/{chance,none}/` (overall leaderboard, RQ2, RQ3, C1–C4) |
| Noise-aware ranks: a worked example, order invariance, the share of non-transitive ties, and the places and top tier against ordinary average ranks | `python -m marathonts.hypotheses.tie_check --artifacts-dir <run>` | `<run>/tables/` | `artifacts/run_*/supplementary/tie_check/` |
| Top tier: the paired datasets with the observed leader, and the set of methods that no other method is shown to beat when every pair is tested (Holm over all pairs; accounts for the selection of the leader) | `python -m marathonts.hypotheses.tier_check --artifacts-dir <run>` | `<run>/tables/` | `artifacts/run_*/supplementary/tier_check/` |
| RQ4 by generator family: leave one family out, a metric chosen on the other families applied to the held-out family (share of correctly ordered pairs, bootstrap interval over datasets), and RQ4 on the methods of the other run | `python -m marathonts.hypotheses.family_check --artifacts-dir <run> [--restrict-to <other run>]` | `<run>/tables/` | `artifacts/run_*/supplementary/family_check/` |
| C1: the method-by-dataset eligibility mask, a permutation calibration of the Friedman test, Skillings-Mack with the incomplete datasets kept, every method on the complete datasets, the methods of the other run, and Holm over C1–C4 with the permutation p | `python -m marathonts.hypotheses.c1_check --artifacts-dir <run> [--restrict-to <other run>]` | `<run>/tables/`, `<run>/hypotheses/confirmatory.parquet` | `artifacts/run_*/supplementary/c1_check/` |
| C3 without the task-aware assembler zseries (the open assemblers against the random path), with Holm over C1–C4 recomputed | `python -m marathonts.hypotheses.c3_check --artifacts-dir <run>` | `<run>/tables/`, `<run>/hypotheses/confirmatory.parquet` | `artifacts/run_*/supplementary/c3_check/` |
| RQ0: the inventory of the 297 units of the validity check (fidelity outputs × references, memorisation, utility units), mapped to the metric IDs, with the outputs left out and those in redundant pairs | `python -m marathonts.hypotheses.rq0_inventory --artifacts-dir <run>` | `<run>/hypotheses/RQ0_*.parquet` | `artifacts/run_*/supplementary/rq0_inventory/` |
| RQ5 (a): absolute TSTR and TRTR scores by task, model and split, the ROC AUC cells with an undefined ratio, and the tests by criterion | `python -m marathonts.hypotheses.rq5_check --artifacts-dir <run>` | `<run>/tables/`, `<run>/hypotheses/RQ5_global.parquet` | `artifacts/run_*/supplementary/rq5_check/` |
| F5.6 against the density of the seams: the share of positions near a seam and F5.6 against its chance level (circular shifts of the seams) | `python -m marathonts.hypotheses.seam_check --artifacts-dir <run> --series-dir <series>` | `<run>/tables/`, the series of the run | `artifacts/run_*/supplementary/seam_check/` |
| The analysis on the seam metrics defined for every method (F5.5 only; the seam criterion leaves the core rankings for every method) | `python -m marathonts.hypotheses.run --artifacts-dir <run> --no-case-study --exclude-metrics F5.1_ks_seam_vs_real F5.2_ks_seam_vs_inside F5.3_seam_z_mean F5.3_seam_z_p95 F5.4_seam_local_acf F5.6_cp_at_seams F5.7_seam_detect_auc_dev --out-dir <run>/supplementary/common_metrics` | `<run>/tables/` | `artifacts/run_*/supplementary/common_metrics/` |
| Memorisation diagnostics F10: the signed DCR ratio, near copies with bootstrap intervals, exact copies; controls with exact copies of train, copies with noise and partial copies, flagged by the rule of the analysis | `python -m marathonts.hypotheses.memorisation_check --artifacts-dir <run> --series-dir <series> --data-dir data/processed/min` | `<run>/tables/`, the series of the run, the prepared data | `artifacts/run_*/supplementary/memorisation_check/` |

A family C1–C4 in the zEDGE-pool output is computed in the same way as the confirmatory family, but it is not
confirmatory: only the family on the VAE pool was fixed in advance.
