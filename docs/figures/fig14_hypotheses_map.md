# Figure 14 — Research questions, evidence and analyses

**File:** `fig14_hypotheses_map.pdf`

**Suggested caption.** The research questions of the benchmark. RQ0 validates the benchmark itself, RQ1 ranks every method
in every slice, RQ2–RQ9 compare families of methods and properties of the synthetic data. C1–C4
(red) form the pre-specified confirmatory family. The case study of one method is secondary.

## How to read it

- **Evidence colour:** green = utility in TSTR/TRTR (Figs. 10–11), grey = cost records or dataset
  descriptors, white = fidelity (Fig. 12) and utility together.
- **Compared with:** "rand" is the random path of the VAE pool; the "assembly median" is the median,
  per seed, of every assembly method of the pool; "seam-processing contrasts" are the main effects of
  each seam processing; A, B, C are the groups of Fig. 8.
- **Note:** `confirm.` = confirmatory, `explor.` = exploratory, `max only` = needs the decision grid
  (profile `max`).

## Logic of the question set

- RQ0 checks that the benchmark can tell methods apart: two random paths of the same pool must not
  differ, real data (the real-versus-real reference) are compared with the synthetic series on every metric, and only metrics that separate the
  methods beyond noise should carry conclusions.
- RQ1 is the leaderboard: four rankings (fidelity against val + OOT or against train × utility
  classification or regression on val and OOT); privacy, cost (time, memory) and the thematic slices
  for class balance and extremes are ranked separately.
- RQ2 compares generating a long series whole with assembling it from short windows; RQ3
  decomposes assembly into window selection and seam processing.
- RQ4 asks which fidelity metrics, against which reference, predict utility. RQ5 measures the gap to
  real data and the stability of the ranking. RQ6 covers speed and cost. RQ7 looks for dataset
  properties associated with differences between families. RQ8 and RQ9 follow two properties that
  aggregate metrics do not isolate: class shares (rare events above all) and extremes.
- Source: `HYPOTHESES.md`, `marathonts/hypotheses/questions.py`, `marathonts/hypotheses/leaderboard.py`.
