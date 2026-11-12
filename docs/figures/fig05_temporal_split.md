# Figure 5 — Temporal split and the role of each part

**File:** `fig05_temporal_split.pdf`

**Suggested caption.** Temporal split (profile `min`, drawn to scale). Hatched bars are embargo
gaps of 168 h, wide enough to cover every label horizon h ≤ 168 and the longest feature lag (168).
Inside train, the last 10% is held out to stop generator training early. Every statistic the
methods may use comes from train. Val is the primary fidelity reference; train and OOT are also references. Val and OOT are the utility test
sets.

## How to read it

- **Top row:** train (50%) | embargo | val (25%) | embargo | OOT (25%). In profile `max` the
  shares are 60/20/20 over the full series.
- **Bottom row:** train broken down for the generators: core windows | embargo (168 rows) |
  holdout. Core and holdout windows do not overlap.
- **Labels above** list what each part is used for.

## Design rationale (for the paper)

- **Fidelity is measured against three real references:** val (primary, no suffix), train
  (`@train`) and OOT (`@oot`). Train shows how well a method reproduces the data it was fitted on —
  methods fitted on train, and methods that take reference statistics from train, use this data during fitting; val
  measures generalisation and OOT generalisation under
  drift. Two of the four rankings measure fidelity against val and OOT (`holdout_clf`,
  `holdout_reg`), two against train (`train_clf`, `train_reg`).
- **Real-versus-real reference.** Pseudo-method `real` uses the OOT series as a "synthetic" series (RQ0); it is a reference, not an upper bound, since OOT is shifted in time. OOT
  is shorter than K·T, so each method is also scored on its first len(OOT) points (`@len`) to
  compare at equal length.
- **Utility** uses the same real val and OOT rows for TSTR and TRTR. OOT checks robustness to a
  shift in time (RQ5).
