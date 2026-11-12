# RQ0 inventory — run_l4

Supplementary, not pre-specified (`python -m marathonts.hypotheses.rq0_inventory`). See the module docstring.

Units of RQ0 (c): 297 — fidelity 237 (79 outputs × 3 references), memorisation 2 (against train), utility 58 (14 tasks; models: gbdt, linear, mlp; splits: oot, val). Discriminative: 143.

Fidelity outputs: 83 in 66 metric IDs; IDs with several outputs: F1.5 (3), F1.6 (4), F2.1 (5), F2.2 (2), F3.4 (2), F3.6 (2), F5.3 (2), F6.4 (2), F7.6 (2), F9.1 (2), F9.2 (2).

By reference (memorisation: the actual reference, train; the analysis tables label it val):

| reference   |   units_fidelity |   units_memorisation |   units_utility |   discriminative_fidelity |   discriminative_memorisation |   discriminative_utility |
|:------------|-----------------:|---------------------:|----------------:|--------------------------:|------------------------------:|-------------------------:|
| oot         |               79 |                    0 |              29 |                        36 |                             0 |                       15 |
| train       |               79 |                    2 |               0 |                        50 |                             1 |                        0 |
| val         |               79 |                    0 |              29 |                        26 |                             0 |                       15 |

Outputs left out:

| output                    | metric_id   | group          | reason                                                 |
|:--------------------------|:------------|:---------------|:-------------------------------------------------------|
| F4.4_calendar_continuity  | F4.4        | F4_seasonality | calendar-continuity metric, left out of every question |
| F4.5_calendar_seam_breaks | F4.5        | F4_seasonality | calendar-continuity metric, left out of every question |

Outputs in a redundant pair of RQ0 (d) (|rho| >= 0.9): F1.2_w1, F1.5_quantile_err, F1.6_mean_err, F11.3_multiclass_tvd, F4.1_how_mean, F4.3_hod_mean, F5.1_ks_seam_vs_real, F5.2_ks_seam_vs_inside, F5.3_seam_z_mean, F5.3_seam_z_p95, F6.4_mmd, F6.4_mmd_2T, F8.1_class_tvd, F8.5_cond_event_err, F9.1_precision, F9.2_density_logdev.

Utility units:

| unit                              | discriminative   |
|:----------------------------------|:-----------------|
| clf_down_h24_q10|gbdt|S|oot|auc   | False            |
| clf_down_h24_q10|gbdt|S|val|auc   | False            |
| clf_down_h24_q10|linear|S|oot|auc | False            |
| clf_down_h24_q10|linear|S|val|auc | True             |
| clf_up_h168_q90|gbdt|S|oot|auc    | True             |
| clf_up_h168_q90|gbdt|S|val|auc    | True             |
| clf_up_h168_q90|linear|S|oot|auc  | True             |
| clf_up_h168_q90|linear|S|val|auc  | True             |
| clf_up_h1_q90|gbdt|S|oot|auc      | False            |
| clf_up_h1_q90|gbdt|S|val|auc      | False            |
| clf_up_h1_q90|linear|S|oot|auc    | False            |
| clf_up_h1_q90|linear|S|val|auc    | False            |
| clf_up_h24_q90|gbdt|S|oot|auc     | True             |
| clf_up_h24_q90|gbdt|S|val|auc     | False            |
| clf_up_h24_q90|linear|S|oot|auc   | True             |
| clf_up_h24_q90|linear|S|val|auc   | True             |
| clf_up_h24_q90|mlp|S|oot|auc      | True             |
| clf_up_h24_q90|mlp|S|val|auc      | False            |
| clf_up_h24_q95|gbdt|S|oot|auc     | False            |
| clf_up_h24_q95|gbdt|S|val|auc     | False            |
| clf_up_h24_q95|linear|S|oot|auc   | False            |
| clf_up_h24_q95|linear|S|val|auc   | False            |
| clf_up_h24_q99|gbdt|S|oot|auc     | False            |
| clf_up_h24_q99|gbdt|S|val|auc     | False            |
| clf_up_h24_q99|linear|S|oot|auc   | False            |
| clf_up_h24_q99|linear|S|val|auc   | False            |
| clf_up_h6_q90|gbdt|S|oot|auc      | False            |
| clf_up_h6_q90|gbdt|S|val|auc      | False            |
| clf_up_h6_q90|linear|S|oot|auc    | False            |
| clf_up_h6_q90|linear|S|val|auc    | True             |
| mc3_h24|gbdt|S|oot|logloss        | True             |
| mc3_h24|gbdt|S|val|logloss        | True             |
| mc3_h24|linear|S|oot|logloss      | True             |
| mc3_h24|linear|S|val|logloss      | True             |
| ms_h24|gbdt|S|oot|mase            | True             |
| ms_h24|gbdt|S|val|mase            | True             |
| ms_h24|linear|S|oot|mase          | True             |
| ms_h24|linear|S|val|mase          | True             |
| qreg_h24|gbdt|S|oot|pinball       | True             |
| qreg_h24|gbdt|S|val|pinball       | True             |
| qreg_h24|linear|S|oot|pinball     | False            |
| qreg_h24|linear|S|val|pinball     | True             |
| reg_h168|gbdt|S|oot|mase          | True             |
| reg_h168|gbdt|S|val|mase          | True             |
| reg_h168|linear|S|oot|mase        | True             |
| reg_h168|linear|S|val|mase        | True             |
| reg_h1|gbdt|S|oot|mase            | False            |
| reg_h1|gbdt|S|val|mase            | False            |
| reg_h1|linear|S|oot|mase          | True             |
| reg_h1|linear|S|val|mase          | False            |
| reg_h24|gbdt|S|oot|mase           | True             |
| reg_h24|gbdt|S|val|mase           | True             |
| reg_h24|linear|S|oot|mase         | True             |
| reg_h24|linear|S|val|mase         | True             |
| vol_h24|gbdt|S|oot|mase           | False            |
| vol_h24|gbdt|S|val|mase           | False            |
| vol_h24|linear|S|oot|mase         | False            |
| vol_h24|linear|S|val|mase         | False            |
