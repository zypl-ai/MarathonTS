# Protocol amendments

The analysis protocol of the benchmark is `docs/HYPOTHESES.md` together with the code of the analysis
(`marathonts/hypotheses/`). This file records when it was frozen and every change made after the freeze. Changes after the
freeze are exploratory: they are not part of the pre-specified analysis.

## Freeze

- **Frozen:** 21 October 2026, commit `7fea7530b061948199f08777c10045892b1976f8` of the authors' internal
  repository (the public repository starts from a later, squashed commit). At that commit, `HYPOTHESES.md`
  has sha256 `4302d5af157afff8776f1ff3c6770714304e7b138ffa3f4473224b264159958b` and the analysis code
  (`hypotheses/`) has the git tree id `48fb97d374d41467336fd3bdfe26d3db967ef0e2`. The commit is available
  from the authors on request.
- **Main run:** carried out on 24 to 26 October 2026, after the freeze. The analysis is pre-specified with
  respect to the main run.
- **Before the freeze:** the replication run (profile `min`, NVIDIA L4) was completed on 21 October 2026,
  before the freeze.

## Changes after the freeze

| Date | Change | Kind | Effect on the results |
|---|---|---|---|
| 2026-10-28 | The leaderboard is read by tier, not by place: the places within the top tier are not separated by the tests and did not reproduce between the main and the replication run | interpretation, adopted after the two runs were compared | none on the numbers; the paper reports tiers |
| 2026-10-29 | Tied methods share a place in the rank bootstrap, so P(first) and P(top 3) do not depend on how a sort breaks ties on a given CPU; ties of RQ4 top predictors broken by the unit name | computation | P(top 3) of tied methods only |
| 2026-10-29 | The ablations `vae_edge_beam` and `vae_sa` of the zseries assembler, listed in the frozen protocol for RQ3 and the case study, are not part of the release; the published analysis is run without them | scope of the release | the comparisons of the two ablations are not reported; they are not ranked |
| 2026-11-03 | Wording: Diffusion-TS receives the calendar, only the window generators generate it | wording | none |
| 2026-11-05 | RQ3: the question is reworded from "what matters more when assembling from one pool" to "do the selection and order of the windows and the processing of the seams move the series towards the real data, each against its own control"; the comparisons, tests and corrections are unchanged | wording | none |
| 2026-11-09 | Real-data ceiling renamed the real-versus-real reference; the RQ0 (b) flag reads "flagged for inspection" and does not by itself make a metric invalid (it never removed a metric from a ranking) | interpretation | none |
| 2026-11-09 | Supplementary analyses: the analysis with the zEDGE pool in place of the VAE pool, the pool check, the calendar check and the analysis without the fidelity metrics that use the calendar (`HYPOTHESES.md`, section 8) | exploratory additions | none on the pre-specified results |
| 2026-11-09 | Analysis options `noise_estimator` ("neighbours", the pre-specified default; "pairs"; "perm:<n>") and `noise_scale` (default 1) for supplementary sensitivity checks of the noise margin, and the noise check (`marathonts/hypotheses/noise_check.py`) | exploratory additions | none: the defaults reproduce the pre-specified analysis (published outputs identical) |
| 2026-11-09 | Analysis option `ci_stat` ("mean", the pre-specified default; "median") for a supplementary bootstrap interval of the median over datasets; the paper's table of C1–C4 shows both intervals | exploratory addition | none on the verdicts; the defaults reproduce the pre-specified analysis |
| 2026-11-09 | Analysis option `utility_fail_rule` ("worst", the pre-specified default; "chance", a fixed chance-level penalty) and the failure check (`marathonts/hypotheses/failure_check.py`) for supplementary checks of the imputation of untrainable utility cells | exploratory additions | none: the defaults reproduce the pre-specified analysis |
| 2026-11-09 | Tie check (`marathonts/hypotheses/tie_check.py`) and a test of the noise-aware ranks (`tests/test_ties.py`: the worked example, order invariance, the sum of the ranks) | exploratory addition | none |
| 2026-11-09 | Tier check (`marathonts/hypotheses/tier_check.py`): paired datasets with the leader and an all-pairs non-rejection set; the top tier is described as a non-rejection set that does not establish equivalence | exploratory addition, interpretation | none on the numbers |
| 2026-11-10 | RQ4 described as associations among the compared methods, not as selection of an unseen generator; family check (`marathonts/hypotheses/family_check.py`): leave one generator family out, selection outside the family, RQ4 on the methods of the other run | exploratory addition, interpretation | none on the numbers |
| 2026-11-10 | C1 described as a complete design (a method left out for leakage on any dataset drops out of the test, as the protocol states) with its methods listed; C1 check (`marathonts/hypotheses/c1_check.py`): eligibility mask, permutation calibration, Skillings-Mack and complete-dataset sensitivity, the methods of the other run | exploratory addition, wording | none on the verdicts |
| 2026-11-10 | C4 and the seam contrasts of RQ3 described as conditional on the VAE pool and the zseries path; C3 check (`marathonts/hypotheses/c3_check.py`): C3 without the task-aware assembler zseries | exploratory addition, wording | none on the verdicts |
| 2026-11-10 | The dataset descriptors of RQ7 and CS15 are read from `tables/descriptors.parquet` (written by `collect`) when the prepared datasets are not available, so that the analysis of the published tables needs no data; the computation of the descriptors is unchanged | software | none: RQ7 recomputed from the table equals the published one |
| 2026-11-10 | RQ0 units described (237 fidelity metric × reference, 2 memorisation, 58 utility; the discriminative shares by reference given for the fidelity metrics alone); RQ0 inventory (`marathonts/hypotheses/rq0_inventory.py`); the memorisation metrics, labelled val in the analysis tables, are computed against train | exploratory addition, wording | none on the numbers |
| 2026-11-10 | RQ5 (a) reported with the tests, intervals and the absence of a practical margin; RQ5 check (`marathonts/hypotheses/rq5_check.py`): absolute scores, undefined ROC AUC cells, tests by criterion | exploratory addition, wording | none on the numbers |
| 2026-11-10 | Undefined metrics in the hierarchy described (not imputed; a criterion without a defined leaf is left out of the method's domain); seam check (`marathonts/hypotheses/seam_check.py`): F5.6 against the density of the seams; the analysis on the seam metrics defined for every method; `tabulate` declared as a dependency (the Markdown reports need it) | exploratory addition, wording, software | none on the pre-specified results |
| 2026-11-10 | Memorisation diagnostics described with their sign (F10.1 is the absolute log ratio); memorisation check (`hypotheses/memorisation_check.py`): signed DCR ratio, near copies with intervals, controls with exact and near copies of train; the privacy statement qualified (no protection against membership or attribute inference is claimed) | exploratory addition, wording | none on the pre-specified results |
