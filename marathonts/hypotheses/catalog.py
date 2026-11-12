"""Case study of one method (`Config.case_method`, `--case-method`; CS1–CS15, HYPOTHESES.md §4) and the shared
loaders of the hypothesis part. The research questions RQ0–RQ9 are in
`questions.py`; the case study compares one method with its controls on the same pool, the
alternative stitchers and the long-series baselines. It is secondary (BH within a hypothesis);
the confirmatory family of the benchmark is `questions.confirmatory_rq`.

Utility is TSTR against TRTR: every model is trained either on the real train (regime R, TRTR, the
pseudo-method `real`) or only on a method's synthetic series (regime S, TSTR) and tested on the
same real rows. Methods are compared by their TSTR; how close it comes to TRTR is the transfer
ratio (`transfer_ratio`, 1 = as good as real data).

Each `h_*` function takes the loaded benchmark tables and returns
`{"global": DataFrame, "per_dataset": DataFrame, "extra": dict}`; `run.py` writes them out
and builds the report.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

from . import engine as E
from . import stats as S

from marathonts.bench import registry as R  # noqa: E402
from marathonts.bench.fidelity import ORIENT  # noqa: E402

PRIMARY_METRIC = {"clf": "auc", "mc": "logloss", "reg": "mase", "qreg": "pinball", "ms": "mase", "vol": "mase"}
# utility metrics analysed, with their orientation (+1 higher is better); the other columns of the utility table
# are diagnostics (`UT_DIAGNOSTICS`). A custom metric joins with `Config.metric_orient`
UT_ORIENT = {"auc": 1, "pr_auc": 1, "brier": -1, "logloss": -1, "ece": -1, "f1": 1, "lift10": 1, "macro_f1": 1,
             "mae": -1, "rmse": -1, "mase": -1, "smape": -1, "mae_extreme": -1, "pinball": -1, "coverage80_err": -1}
HIGHER_BETTER = {m for m, o in UT_ORIENT.items() if o > 0}
UT_DIAGNOSTICS = {"fit_s", "predict_s", "n_train", "n_synth_train", "params", "hpo_candidates", "n", "pos_share",
                  "coverage80", "crossing_share", "mase_last", "config_fingerprint", "unit_fp", "imputed"}
_DEFAULTS: dict = {}


def configure(cfg) -> None:
    """Apply the analysis choices of `cfg` (`Config.primary_metrics`, `metric_orient`, `core_metrics`,
    `metric_criteria`, `task_criteria`) to the module tables, in place, starting from the built-in values each
    time (idempotent). Called when the tables are loaded (`run.load_tables`) and by the leaderboards."""
    from . import leaderboard as LB

    tabs = {"PRIMARY_METRIC": PRIMARY_METRIC, "UT_ORIENT": UT_ORIENT, "HIGHER_BETTER": HIGHER_BETTER,
            "FID_CRITERIA": LB.FID_CRITERIA, "UT_CRITERIA": LB.UT_CRITERIA, "CORE_METRICS": LB.CORE_METRICS}
    for k, v in tabs.items():
        _DEFAULTS.setdefault(k, type(v)(v))
        v.clear()
        v.update(_DEFAULTS[k])
    PRIMARY_METRIC.update(getattr(cfg, "primary_metrics", None) or {})
    UT_ORIENT.update({m: (1 if o > 0 else -1) for m, o in (getattr(cfg, "metric_orient", None) or {}).items()})
    HIGHER_BETTER.clear()
    HIGHER_BETTER.update(m for m, o in UT_ORIENT.items() if o > 0)
    LB.FID_CRITERIA.update(getattr(cfg, "metric_criteria", None) or {})
    LB.UT_CRITERIA.update(getattr(cfg, "task_criteria", None) or {})
    if getattr(cfg, "core_metrics", None) is not None:
        LB.CORE_METRICS.clear()
        LB.CORE_METRICS.update({c: tuple(ms) for c, ms in cfg.core_metrics.items()})
    LB.core_changed()
    global FAIL_RULE
    FAIL_RULE = getattr(cfg, "utility_fail_rule", "worst") or "worst"
CONFIRMATORY_CELL = ("linear", "oot")          # model, split of the case-study pre-specified cell (CS7, CS10)
# value of a model that learned nothing, where the metric has one (p = positive share of the test rows):
# a constant score has ROC AUC 0.5 and PR AUC p; the constant probability p has log-loss H(p) and Brier
# p(1 − p); in a K-class task the uniform prediction has log-loss ln K. The imputed value is the worse of
# this level and the worst value of its block; every other metric (and these where the level is undefined)
# takes the worst value of its block
def _entropy(p):
    return float(-(p * np.log(p) + (1 - p) * np.log(1 - p))) if 0 < p < 1 else np.nan


def _n_classes(row):
    try:
        return R.tasks.get(row["task"]).n_classes
    except Exception:
        return None


CHANCE = {
    "auc": lambda row: 0.5,
    "pr_auc": lambda row: row["pos_share"] if row["task_kind"] == "clf" else np.nan,
    "logloss": lambda row: (_entropy(row["pos_share"]) if row["task_kind"] == "clf"
                            else np.log(_n_classes(row)) if _n_classes(row) else np.nan),
    "brier": lambda row: row["pos_share"] * (1 - row["pos_share"]) if row["task_kind"] == "clf" else np.nan,
}
UT_KEY = ["dataset", "seed", "task", "model", "split"]


FAIL_RULE = "worst"     # Config.utility_fail_rule: "worst" (pre-specified) or "chance" (supplementary: fixed no-skill)


def impute_failed_utility(ut: pd.DataFrame) -> pd.DataFrame:
    """TSTR cells a method's series could not train, filled as a model that learned nothing.

    Expected cells of a (dataset, seed) are those of TRTR (`real`, regime R): every task × model × split
    fitted on real train — any registered task, model or plugin. A method with a unit there (its series
    exists and is not left out for leakage) but no TSTR row for an expected cell failed on it: one class
    in the labels of its series, no rows, a failed fit. The new row gets, for every metric of the cell,
    the worse of the chance level (`CHANCE`) and the worst value any method has in that block (the worst
    value alone where the metric has no chance level), and `imputed` =
    True; a block without any other method stays missing. Rows of the other task kinds (decision-transfer
    grid, thresholds) are left as they are."""
    if ut is None or not len(ut) or "regime" not in ut:
        return ut
    ut = ut.assign(imputed=False)
    plain = ~ut["task_kind"].isin(["grid", "threshold"])
    R_ = ut[plain & (ut["regime"] == "R")]
    S_ = ut[plain & (ut["regime"] == "S") & ~ut["method"].astype(str).str.contains("@")]
    if not len(R_) or not len(S_):
        return ut
    expected = R_[UT_KEY + ["task_kind", "pos_share"]].drop_duplicates(UT_KEY)
    units = S_[["dataset", "seed", "method"]].drop_duplicates()
    want = units.merge(expected, on=["dataset", "seed"])
    have = S_[UT_KEY + ["method"]].drop_duplicates()
    miss = want.merge(have, on=UT_KEY + ["method"], how="left", indicator=True)
    miss = miss[miss["_merge"] == "left_only"].drop(columns="_merge")
    if not len(miss):
        return ut
    metrics = [c for c in UT_ORIENT if c in ut]
    worst = S_.groupby(UT_KEY)[metrics].agg({m: "min" if m in HIGHER_BETTER else "max" for m in metrics})
    rows = []
    for r in miss.to_dict("records"):
        key = tuple(r[k] for k in UT_KEY)
        w = worst.loc[key] if key in worst.index else None
        vals = {}
        for m in metrics:
            v = w[m] if w is not None else np.nan
            if pd.isna(v):                             # the metric does not exist for this task kind
                continue
            c = CHANCE[m](r) if m in CHANCE else np.nan
            if FAIL_RULE == "chance":                  # a fixed no-skill value, whatever the other methods score
                if not pd.isna(c):
                    vals[m] = c
                continue
            vals[m] = v if pd.isna(c) else (min(c, v) if m in HIGHER_BETTER else max(c, v))
        if vals:
            rows.append({**r, **vals, "regime": "S", "imputed": True})
    return pd.concat([ut, pd.DataFrame(rows)], ignore_index=True) if rows else ut


_WARNED: set = set()


def _warn_once(msg: str) -> None:
    if msg not in _WARNED:
        _WARNED.add(msg)
        print(f"WARNING: {msg}")


# ─────────────────────── long tables ───────────────────────────────────────
def fidelity_long(fid: pd.DataFrame) -> pd.DataFrame:
    """Long table; `<method>@len` rows (length-matched, only for the ceiling of RQ0) stay in it but
    nothing except RQ0 selects them."""
    cols = [c for c in fid.columns if c in ORIENT]
    return fid.melt(id_vars=["dataset", "method", "seed"], value_vars=cols, var_name="unit", value_name="value")


def utility_long(ut: pd.DataFrame, metrics_by_kind=PRIMARY_METRIC, all_metrics=False) -> pd.DataFrame:
    empty = pd.DataFrame(columns=["dataset", "method", "seed", "task", "model", "regime", "split", "value",
                                  "metric", "unit"])
    if ut is None or not len(ut) or "task_kind" not in ut:
        return empty
    u = ut[~ut["task_kind"].isin(["grid", "threshold"])].copy()
    rows = []
    for kind, g in u.groupby("task_kind"):
        if not all_metrics and kind not in metrics_by_kind:
            _warn_once(f"task type {kind!r} has no primary utility metric (Config.primary_metrics): left out")
            continue
        mets = [metrics_by_kind[kind]] if not all_metrics else \
            [c for c in g.columns if c in UT_ORIENT and g[c].notna().any()]
        mets = [m for m in mets if m in g]
        for m in mets:
            t = g[["dataset", "method", "seed", "task", "model", "regime", "split", m]].rename(columns={m: "value"})
            t["metric"] = m
            rows.append(t)
    if not rows:
        return empty
    L = pd.concat(rows, ignore_index=True)
    L["unit"] = L["task"] + "|" + L["model"] + "|" + L["regime"] + "|" + L["split"] + "|" + L["metric"]
    return L


def _orient_units(units, metric_of):
    return {u: (1.0 if metric_of(u) in HIGHER_BETTER else -1.0) for u in units}


def _ut_orient(L):
    return _orient_units(L["unit"].unique(), lambda u: u.split("|")[-1])


def _run(long, orient, comparators, units=None, adjust="bh", alpha=0.05, q=0.5, n_boot=2000,
         method_override=None, margin="pool"):
    """margin: "pool" — rand vs rand_b on the shared pool, or the between-seed spread of rand where the twin
    is not run (min) (comparisons on the same pool);
    "seed" — between-seed spread of the case-study method (comparisons with independently trained methods)."""
    if units is not None:
        long = long[long["unit"].isin(units)]
    if margin == "seed":
        src = method_override if method_override is not None else long
        margins = E.seed_margins(src.assign(method=E.CASE_METHOD) if method_override is not None else src, q)
    else:
        margins = E.noise_margins(long, q)
    per_all, glob_all = [], []
    for comp in comparators:
        pairs = E.paired(long, orient, comp, method_override=method_override)
        if not len(pairs):
            continue
        per, glob = E.summarize(pairs, margins, alpha, n_boot)
        per["comparator"], glob["comparator"] = comp, comp
        per_all.append(per)
        glob_all.append(glob)
    per = pd.concat(per_all, ignore_index=True) if per_all else pd.DataFrame()
    glob = pd.concat(glob_all, ignore_index=True) if glob_all else pd.DataFrame()
    glob = E.finalize(glob, adjust, alpha) if len(glob) else glob
    per, glob = E.finalize_per_dataset(per, glob, adjust, alpha)
    return {"global": glob, "per_dataset": per, "extra": {}}


# ─────────────────────── fidelity hypotheses ───────────────────────────────
def _primary_ref(u: str) -> bool:
    """A metric against the primary reference (no `@<part>` suffix): the case study uses the val
    reference; `@train` enters only CS1, the other references only the RQs."""
    return "@" not in u


def _fid_units(prefixes=(), names=(), exclude=()):
    out = []
    for u in filter(_primary_ref, ORIENT):
        if u in exclude:
            continue
        if any(u.startswith(p) for p in prefixes) or u in names:
            out.append(u)
    return out


def h0_noise(T, cfg):
    """Benchmark validity: (a) the two random stitches are equivalent on every metric;
    (b) ceiling: real OOT data against every method on fidelity."""
    L = fidelity_long(T["fidelity"])
    # (a) vae_rand_b vs vae_rand as if vae_rand_b were the method under study: the margin would come from the pair being tested,
    #     so use the half-split of seeds: margin on even seeds, test on odd seeds. Only where the twin is run (mid, max).
    if E.has_twin(L):
        even, odd = L[L["seed"] % 2 == 0], L[L["seed"] % 2 == 1]
        margins = E.noise_margins(even, cfg.equivalence_margin_q)
        pairs = E.paired(odd, ORIENT, E.NOISE[0], method=E.NOISE[1])
        per, glob = E.summarize(pairs, margins, cfg.alpha, cfg.n_boot)
        glob = E.finalize(glob, "bh", cfg.alpha)
        per["comparator"], glob["comparator"] = E.NOISE[0], E.NOISE[0]
        per, glob = E.finalize_per_dataset(per, glob, "bh", cfg.alpha)
        glob = glob.assign(comparator=f"{E.NOISE[1]} vs {E.NOISE[0]}")
    else:
        per, glob = pd.DataFrame(), pd.DataFrame()
    # (b) ceiling: real OOT vs every method scored on the same length (`<method>@len`, first seed)
    real = L[L["method"] == "real"].groupby(["dataset", "unit"])["value"].mean()
    ceil = []
    for m in cfg.methods:
        mm = L[L["method"] == f"{m}@len"].groupby(["dataset", "unit"])["value"].mean()
        j = pd.concat([real.rename("real"), mm.rename("m")], axis=1).dropna().reset_index()
        j["real_better"] = j["unit"].map(ORIENT) * (j["real"] - j["m"]) > 0
        ceil.append(j.groupby("unit")["real_better"].mean().rename(m))
    ceiling = pd.concat(ceil, axis=1) if ceil else pd.DataFrame()
    # a metric is flagged uninformative when real data is not better than the case-study method on most datasets
    flagged = sorted(ceiling.index[ceiling[E.CASE_METHOD] < 0.5]) if E.CASE_METHOD in ceiling else []
    return {"global": glob, "per_dataset": per,
            "extra": {"ceiling_share_real_better": ceiling, "uninformative_metrics": ", ".join(flagged)}}


_DIST_DEP = ("F1.", "F2.", "F3.")


def h1_train_fit(T, cfg):
    """Distribution and dependence (F1–F3) against train: what the method was fitted on."""
    L = fidelity_long(T["fidelity"])
    units = [u for u in ORIENT if u.endswith("@train") and u.startswith(_DIST_DEP)
             and not u.startswith("F3.2_acf_beyond_window")]
    return _run(L, ORIENT, [E.NOISE[0]], units, "bh", cfg.alpha, cfg.equivalence_margin_q, cfg.n_boot)


def h2_marginal_dependence(T, cfg):
    """The same metrics against val: does the fit transfer to unseen data."""
    L = fidelity_long(T["fidelity"])
    units = _fid_units(_DIST_DEP, exclude=("F3.2_acf_beyond_window",))
    return _run(L, ORIENT, [E.NOISE[0]], units, "bh", cfg.alpha, cfg.equivalence_margin_q, cfg.n_boot)


def h3_seams(T, cfg):
    L = fidelity_long(T["fidelity"])
    return _run(L, ORIENT, [E.NOISE[0]], _fid_units(("F5.",)), "bh", cfg.alpha, cfg.equivalence_margin_q, cfg.n_boot)


def h4_long_structure(T, cfg):
    L = fidelity_long(T["fidelity"])
    units = _fid_units(("F7.",), names=("F3.2_acf_beyond_window", "F6.4_mmd_2T"))
    return _run(L, ORIENT, [E.NOISE[0]], units, "bh", cfg.alpha, cfg.equivalence_margin_q, cfg.n_boot)


def h5_target_structure(T, cfg):
    L = fidelity_long(T["fidelity"])
    units = _fid_units(("F8.",))
    return _run(L, ORIENT, [E.NOISE[0]], units, "bh", cfg.alpha, cfg.equivalence_margin_q, cfg.n_boot)


def h6_window_equivalence(T, cfg):
    L = fidelity_long(T["fidelity"])
    units = _fid_units(("F9.", "F10."), names=("F6.1_disc_score", "F6.2_c2st_auc_dev", "F6.4_mmd",
                                                 "F6.6_feature_fid", "F6.8_nn_dist_logratio"))
    return _run(L, ORIENT, [E.NOISE[0]], units, "bh", cfg.alpha, cfg.equivalence_margin_q, cfg.n_boot)


# calendar continuity: the pool generators generate the calendar as part of a window, while the long-series
# generators receive it (Diffusion-TS: imposed from a random start; the pretrained forecasters: the real
# calendar continuing train) — continuous by construction, so these checks are left out of the rankings
CALENDAR_VALIDITY = ("F4.4_calendar_continuity", "F4.5_calendar_seam_breaks")


def _run_mixed(long, orient, units, adjust, cfg, method_override=None):
    """The method under study vs the alternative stitchers (same pool → margin from the noise pair) and vs the
    long-series baselines (independently trained → margin from the between-seed spread of the method); one
    multiple-testing family over both."""
    parts = []
    if E.ALTERNATIVES:
        parts.append(_run(long, orient, list(E.ALTERNATIVES), units, adjust, cfg.alpha, cfg.equivalence_margin_q,
                          cfg.n_boot, method_override=method_override))
    if E.BASELINES:
        parts.append(_run(long, orient, list(E.BASELINES), units, adjust, cfg.alpha, cfg.equivalence_margin_q,
                          cfg.n_boot, method_override=method_override, margin="seed"))
    gl = [p["global"] for p in parts if len(p["global"])]
    pr = [p["per_dataset"] for p in parts if len(p["per_dataset"])]
    glob = pd.concat(gl, ignore_index=True) if gl else pd.DataFrame()
    per = pd.concat(pr, ignore_index=True) if pr else pd.DataFrame()
    if len(glob):
        glob = E.finalize(glob, adjust, cfg.alpha)
    per, glob = E.finalize_per_dataset(per, glob, adjust, cfg.alpha)
    return {"global": glob, "per_dataset": per, "extra": {}}


def h7_fidelity_vs_alternatives(T, cfg):
    """Fidelity of the method under study against every alternative stitcher on the same pool and the long-series
    baselines (`baselines`: Diffusion-TS, Chronos, TimesFM, Timestral by default)."""
    L = fidelity_long(T["fidelity"])
    units = [u for u in ORIENT if _primary_ref(u) and u not in CALENDAR_VALIDITY]
    return _run_mixed(L, ORIENT, units, "bh", cfg)


# ─────────────────────── utility hypotheses: TSTR against TRTR ─────────────
def _tstr(L):
    """TSTR rows (regime S) of the synthetic methods."""
    return L[(L["regime"] == "S") & (L["method"] != "real")]


def transfer_ratio(L) -> pd.DataFrame:
    """TSTR relative to TRTR per (dataset, method, seed, task, model, split): 1 = the synthetic data
    trains a model as good as the real data. AUC: skill above chance, (TSTR − 0.5) / (TRTR − 0.5)
    (NaN when TRTR is within 0.02 of chance); other higher-is-better metrics: TSTR / TRTR; losses:
    TRTR / TSTR."""
    key = ["dataset", "seed", "task", "model", "split", "metric"]
    trtr = L[(L["method"] == "real") & (L["regime"] == "R")].set_index(key)["value"].rename("trtr")
    s = _tstr(L).join(trtr, on=key)
    m, a, b = s["metric"], s["value"], s["trtr"]
    auc = m == "auc"
    hb = m.isin(HIGHER_BETTER) & ~auc
    ratio = np.where(auc, (a - 0.5) / (b - 0.5).where((b - 0.5) > 0.02),
                     np.where(hb, a / b.where(b != 0), b / a.where(a != 0)))
    return s.assign(ratio=ratio)


def _ratio_table(R_, keys):
    """Median transfer ratio per method (rows) × `keys` (columns), seeds and datasets pooled."""
    t = R_.groupby(["method", *keys])["ratio"].median().unstack(keys) if keys else \
        R_.groupby("method")["ratio"].median().to_frame("ratio")
    return t.round(3)


def _method_as(L, regime_method, regime_comp_method="real", regime_comp=None):
    """Re-key rows so 'the method in regime A' is compared with 'comparator in regime B' on one unit id."""
    regime_comp = regime_comp or regime_method
    o = L[(L["method"] == E.CASE_METHOD) & (L["regime"] == regime_method)].copy()
    c = L[(L["method"] == regime_comp_method) & (L["regime"] == regime_comp)].copy()
    for t in (o, c):
        t["unit"] = t["task"] + "|" + t["model"] + "|" + t["split"] + "|" + t["metric"]
    return o, c


def h8_tstr_vs_trtr(T, cfg):
    """TSTR of the method under study against TRTR: the method trained on synthetic (S) vs `real` trained on real (R),
    every task / model / split; the margin is the between-seed spread of the method. "same" = the
    synthetic series trains models as good as the real one. Extra: transfer ratios of every method."""
    L = utility_long(T["utility"])
    o, c = _method_as(L, "S", "real", "R")
    long = c.assign(method="TRTR")
    orient = _orient_units(o["unit"].unique(), lambda u: u.split("|")[-1])
    res = _run(long, orient, ["TRTR"], None, "bh", cfg.alpha, cfg.equivalence_margin_q, cfg.n_boot,
               method_override=o, margin="seed")
    Rt = transfer_ratio(L)
    m, s = CONFIRMATORY_CELL
    prim = Rt[(Rt["task"] == E.CASE_TASK) & (Rt["model"] == m) & (Rt["split"] == s)]
    res["extra"].update(
        transfer_ratio_case_cell=_ratio_table(prim, ["dataset"]),
        transfer_ratio_by_task=_ratio_table(Rt, ["task"]),
        rowlevel=rowlevel_tests(cfg, E.CASE_TASK, "S", "real", "R"))
    return res


def h9_tstr_primary(T, cfg):
    """Pre-specified case-study cell: TSTR of the method under study against the random stitch on the same
    pool (task `stitch_task`)."""
    L = _tstr(utility_long(T["utility"]))
    L = L[L["task"] == E.CASE_TASK]
    res = _run(L, _ut_orient(L), [E.NOISE[0]], None, "holm", cfg.alpha,
               cfg.equivalence_margin_q, cfg.n_boot)
    res["extra"]["rowlevel"] = rowlevel_tests(cfg, E.CASE_TASK, "S", E.NOISE[0], "S")
    return res


def h10_tstr_other_tasks(T, cfg):
    L = _tstr(utility_long(T["utility"]))
    L = L[L["task"] != E.CASE_TASK]
    return _run(L, _ut_orient(L), [E.NOISE[0]], None, "bh", cfg.alpha,
                cfg.equivalence_margin_q, cfg.n_boot)


def h11_model_robustness(T, cfg):
    """Does the stitching effect on TSTR (S method − S rand) depend on the model class? Friedman over
    models with blocks = datasets (tasks, splits and seeds averaged: within a dataset they share the
    series and are not independent blocks). Only tasks every model is fitted on enter (min / mid:
    MLP only on one task → CS11 is about that task)."""
    L = _tstr(utility_long(T["utility"]))
    o = L[L["method"] == E.CASE_METHOD].set_index(["dataset", "seed", "task", "split", "model"])["value"]
    r = L[L["method"] == E.NOISE[0]].set_index(["dataset", "seed", "task", "split", "model"])["value"]
    sign = L.drop_duplicates("task").set_index("task")["metric"].map(lambda m: 1 if m in HIGHER_BETTER else -1)
    d = (o - r).dropna().reset_index(name="d")
    d["d"] *= d["task"].map(sign)
    cells = d.pivot_table(index=["dataset", "task", "split"], columns="model", values="d", aggfunc="mean").dropna()
    tasks = sorted(cells.index.get_level_values("task").unique())
    # tasks differ in scale: divide each task by one number (its median |d| over all models), so the
    # order of the models within a cell is kept
    scale = cells.abs().stack().groupby(level="task").median().replace(0, np.nan)
    wide = cells.div(scale, level="task", axis=0).groupby(level="dataset").mean().dropna()   # blocks = datasets
    p, ranks, cd = S.friedman_nemenyi(wide)
    sign_agree = (np.sign(wide).nunique(axis=1) == 1).mean() if len(wide) else np.nan
    g = pd.DataFrame([dict(unit="effect_by_model", p_friedman=p, nemenyi_cd=cd, n_blocks=len(wide),
                           share_blocks_same_sign=sign_agree, tasks=", ".join(tasks))])
    return {"global": g, "per_dataset": wide.reset_index(), "extra": {"avg_rank_of_effect": ranks}}


def h13_ranking(T, cfg):
    """Which method's synthetic data comes closest to TRTR: Friedman over all synthetic methods with
    blocks = datasets on the transfer ratio (seeds averaged), Nemenyi critical difference; on the
    confirmatory cell (task `stitch_task`, linear, OOT) and on all cells (tasks, models, splits averaged)."""
    Rt = transfer_ratio(utility_long(T["utility"]))
    m, s = CONFIRMATORY_CELL
    scopes = {E.CASE_TASK + "|" + m + "|" + s:Rt[(Rt["task"] == E.CASE_TASK) & (Rt["model"] == m) & (Rt["split"] == s)],
              "all_cells": Rt}
    rows, extra = [], {}
    for name, R_ in scopes.items():
        wide = R_.groupby(["dataset", "method"])["ratio"].mean().unstack("method")
        wide = wide.dropna(axis=1, how="all").dropna()
        p, ranks, cd = S.friedman_nemenyi(wide)
        rows.append(dict(unit=name, p_friedman=p, nemenyi_cd=cd, n_blocks=len(wide), n_methods=wide.shape[1],
                         best=ranks.index[0] if ranks is not None and len(ranks) else None,
                         method_rank=float(ranks.get(E.CASE_METHOD, np.nan)) if ranks is not None else np.nan))
        if ranks is not None:
            extra[f"ranks_{name}"] = pd.DataFrame({"avg_rank": ranks.round(2),
                                                   "median_ratio": wide.median().reindex(ranks.index).round(3)})
    return {"global": pd.DataFrame(rows), "per_dataset": pd.DataFrame(), "extra": extra}


def h14_decision_transfer(T, cfg):
    """U6.1 rank agreement of the grid (AUC on R vs on S) and U6.4 threshold transfer; needs the
    benchmark run with `decision_transfer=True` (profile max). Empty otherwise."""
    u = T["utility"]
    if "task_kind" not in u:
        return {"global": pd.DataFrame(), "per_dataset": pd.DataFrame(), "extra": {}}
    grid = u[u["task_kind"] == "grid"]
    rows = []
    for (ds, m, seed), g in grid.groupby(["dataset", "method", "seed"]):
        w = g.pivot_table(index="grid_id", columns="regime", values="auc")
        if {"R", "S"} <= set(w.columns) and len(w) > 2:
            rows.append(dict(dataset=ds, method=m, seed=seed, unit="U6.1_rank_agreement",
                             value=float(w["R"].corr(w["S"], method="spearman"))))
    for r in u[u["task_kind"] == "threshold"].itertuples():
        rows.append(dict(dataset=r.dataset, method=r.method, seed=r.seed, unit="U6.4_threshold_transfer",
                         value=float(r.f1_transfer / r.f1_oracle) if r.f1_oracle else np.nan))
    L = pd.DataFrame(rows)
    if not len(L):
        return {"global": pd.DataFrame(), "per_dataset": pd.DataFrame(),
                "extra": {"note": "no grid in the tables: run the benchmark with decision_transfer=True (profile max)"}}
    orient = {"U6.1_rank_agreement": 1.0, "U6.4_threshold_transfer": 1.0}
    return _run(L, orient, [E.NOISE[0]], None, "bh", cfg.alpha, cfg.equivalence_margin_q, cfg.n_boot)


def h15_tstr_vs_alternatives(T, cfg):
    """TSTR of the method under study against every alternative stitcher on the same pool and the long-series
    baselines, all tasks / models / splits; the pre-specified cell against each baseline is confirmatory."""
    L = _tstr(utility_long(T["utility"]))
    return _run_mixed(L, _ut_orient(L), None, "bh", cfg)


def h16_temporal_stability(T, cfg):
    """Is the TSTR effect on the task `stitch_task` the same on val and on OOT? Per dataset the shift
    (d_OOT − d_val) is scaled by the same shift of the noise pair (rand − rand_b), a difference of
    differences like the effect itself; without the twin (min) — by the between-seed spread of the shift
    (OOT − val) of rand. TOST at ±1 across datasets."""
    L = _tstr(utility_long(T["utility"]))
    L = L[L["task"] == E.CASE_TASK]
    key = ["dataset", "seed", "model"]

    def shift(a, b):
        def d(split):
            o = L[(L["method"] == a) & (L["split"] == split)].set_index(key)["value"]
            c = L[(L["method"] == b) & (L["split"] == split)].set_index(key)["value"]
            return o - c
        return (d("oot") - d("val")).dropna()

    if E.has_twin(L):
        noise = shift(*E.NOISE).abs().groupby(level=["dataset", "model"]).quantile(cfg.equivalence_margin_q)
    else:
        def own(split):
            return L[(L["method"] == E.NOISE[0]) & (L["split"] == split)].set_index(key)["value"]
        sh0 = (own("oot") - own("val")).dropna().sort_index()
        noise = (sh0.groupby(level=["dataset", "model"]).diff().abs()
                 .groupby(level=["dataset", "model"]).quantile(cfg.equivalence_margin_q))
    out = []
    for comp in (E.NOISE[0], *E.BASELINES):
        sh = shift(E.CASE_METHOD, comp).groupby(level=["dataset", "model"]).mean()
        j = pd.concat([sh.rename("shift"), noise.rename("margin")], axis=1).dropna().reset_index()
        j = j[j["margin"] > 0]
        for m, g in j.groupby("model"):
            z = (g["shift"] / g["margin"]).to_numpy()                  # unit = dataset
            out.append(dict(unit=f"oot_minus_val|{m}", comparator=comp, n_datasets=len(z),
                            mean_shift=float(g["shift"].mean()), median_z=float(np.median(z)) if len(z) else np.nan,
                            p_equiv=S.tost(z, 1.0), p_two_sided=S.wilcoxon(z)))
    g = pd.DataFrame(out)
    if len(g):
        g["p_equiv_adj"] = S.bh(g["p_equiv"].to_numpy())
        g["p_two_sided_adj"] = S.bh(g["p_two_sided"].to_numpy())
    try:                                            # needs data/processed (test-split calendar, volatility)
        sub = subgroup_tests(cfg)
    except Exception as e:
        sub = f"skipped: {type(e).__name__}: {e}"
    return {"global": g, "per_dataset": pd.DataFrame(), "extra": {"subgroups": sub}}


# ─────────────────────── timing ────────────────────────────────────────────
def h17_cost(T, cfg):
    t = T["timing"].copy()
    if not len(t) or "total_wall_s" not in t:
        return {"global": pd.DataFrame(), "per_dataset": pd.DataFrame(), "extra": {}}
    if "gpu" not in t:
        t["gpu"] = "none"
    hw = t["gpu"].fillna("none").unique()
    rows, per = [], []
    t["log_total"] = np.log(t["total_wall_s"].clip(lower=1e-3))
    for comp in [m for m in cfg.methods if m != E.CASE_METHOD]:
        a = t[t["method"] == E.CASE_METHOD].set_index(["dataset", "seed"])["log_total"]
        b = t[t["method"] == comp].set_index(["dataset", "seed"])["log_total"]
        d = (b - a).dropna().reset_index(name="d")            # > 0: the method under study is faster
        if not len(d):
            continue
        dm = d.groupby("dataset")["d"].mean()
        lo, hi = S.hier_bootstrap_ci(d, cfg.n_boot)
        pe = S.tost(dm, np.log(1.10))                         # "same" = within ±10% time
        rows.append(dict(unit="total_wall_time", comparator=comp, median_ratio_comp_over_method=float(np.exp(dm.median())),
                         ci_ratio_lo=float(np.exp(lo)), ci_ratio_hi=float(np.exp(hi)),
                         p_method_faster=S.wilcoxon(dm, "greater"), p_method_slower=S.wilcoxon(dm, "less"),
                         p_equiv_10pct=pe, n_datasets=len(dm)))
        per.append(d.assign(comparator=comp))
    g = pd.DataFrame(rows)
    if len(g):
        g["p_method_faster_adj"] = S.holm(g["p_method_faster"].to_numpy())
        g["p_method_slower_adj"] = S.holm(g["p_method_slower"].to_numpy())
    # scaling with K: slope of log time on log K, bootstrap over datasets
    sc = []
    med = t.groupby(["method", "dataset"]).agg(total=("total_wall_s", "median"), assemble=("assemble_wall_s", "median"),
                                               K=("K", "first")).reset_index()
    rng = np.random.default_rng(0)
    for m, g2 in med.groupby("method"):
        for col in ("total", "assemble"):
            x, y = np.log(g2["K"].to_numpy(float)), np.log(g2[col].clip(lower=1e-3).to_numpy(float))
            if len(x) < 3 or np.ptp(x) == 0:
                continue
            slope = np.polyfit(x, y, 1)[0]
            bs = [np.polyfit(x[i], y[i], 1)[0] for i in (rng.integers(0, len(x), len(x)) for _ in range(500))
                  if np.ptp(x[i]) > 0]
            sc.append(dict(method=m, time=col, slope_logT_logK=float(slope),
                           ci_lo=float(np.quantile(bs, 0.025)), ci_hi=float(np.quantile(bs, 0.975))))
    pool_hw = set(t["pool_gpu"].dropna()) if "pool_gpu" in t else set()
    if pool_hw - set(hw):
        hw = list(hw) + [f"pools: {x}" for x in pool_hw - set(hw)]
    return {"global": g, "per_dataset": pd.concat(per) if per else pd.DataFrame(),
            "extra": {"scaling": pd.DataFrame(sc), "hardware": list(hw),
                      "warning": "times from different hardware are not comparable" if len(hw) > 1 else ""}}


# ─────────────────────── moderators ────────────────────────────────────────
def dataset_descriptors(cfg) -> pd.DataFrame:
    """Dataset descriptors (RQ7, CS15): from the prepared datasets when every one of them is there, otherwise from
    `tables/descriptors.parquet` of the run (written by `collect`), so that the analysis of the published tables
    needs no data."""
    from marathonts.bench.data import DESCRIPTOR_TABLE, descriptors, prepared_exists

    if all(prepared_exists(ds, cfg) for ds in cfg.datasets):
        return descriptors(cfg)
    f = cfg.artifacts_dir / "tables" / DESCRIPTOR_TABLE
    if not f.exists():
        raise FileNotFoundError(f"dataset descriptors: neither the prepared datasets nor {f}")
    d = pd.read_parquet(f)
    return d[d["dataset"].isin(cfg.datasets)].reset_index(drop=True)


def h18_moderators(results: dict, cfg) -> dict:
    desc = dataset_descriptors(cfg)
    eff = {}
    for h in ("CS2", "CS4", "CS7", "CS10"):
        per = results.get(h, {}).get("per_dataset")
        if per is None or not len(per) or "effect_noise_units" not in per:
            continue
        for comp, g in per.groupby("comparator"):
            eff[f"{h}:{comp}"] = g.groupby("dataset")["effect_noise_units"].median()
    rows = []
    for name, e in eff.items():
        j = desc.set_index("dataset").join(e.rename("effect")).dropna()
        for c in desc.columns.drop("dataset"):
            if len(j) >= 4 and j[c].nunique() > 1:
                from scipy.stats import spearmanr

                r, p = spearmanr(j[c], j["effect"])
                rows.append(dict(effect=name, descriptor=c, spearman=float(r), p=float(p), n=len(j)))
    g = pd.DataFrame(rows)
    if len(g):
        g["p_bh"] = S.bh(g["p"].to_numpy())
    return {"global": g, "per_dataset": desc, "extra": {}}


# ─────────────────────── row-level tests ───────────────────────────────────
_LABELS: dict = {}


def _rows(cfg, ds, method, seed, task=None):
    """Row-level predictions of a unit (of one task, if given) joined with the labels:
    task, model, regime, split, row, y, score."""
    from marathonts.bench.methods import Artifacts
    from marathonts.bench.storage import is_valid
    from marathonts.bench.utility import load_labels, row_scores

    from marathonts.bench import cells as CL

    if ds in (getattr(cfg, "leaked", None) or {}).get(method, ()):
        return None                                  # dataset in the method's training corpus (`Config.leaked`)
    A = Artifacts(cfg)
    f = A.utility_dir(ds, method, seed) / "predictions.parquet"
    run = E.RUN_CFG or cfg                            # role overrides (--case-method, --case-task) do not change the units
    frozen = method in getattr(run, "frozen_methods", ())   # published results without code: no settings check
    if not is_valid(f):
        return None
    filters = [("regime", "in", ["R", "S"])] + ([("task", "==", task)] if task else [])
    pred = pd.read_parquet(f, filters=filters)
    if not frozen:                                   # only the cells made with the run's settings (marathonts/bench/cells.py)
        want = CL.utility_cells(run, method, ds)
        done = CL.utility_done(run, A.utility_dir(ds, method, seed), method, ds)
        fresh = {k for k, fp in want.items() if done.get(k) == fp}
        pred = pred[[f"{t}|{m}" in fresh for t, m in zip(pred["task"].astype(str), pred["model"].astype(str))]]
        if not len(pred):
            return None                              # missing, or made with other settings
    tasks = [task] if task else sorted(pred["task"].astype(str).unique())
    key = (str(A.root), ds, tuple(tasks))
    if key not in _LABELS:
        _LABELS[key] = load_labels(A, ds, tasks)
    if not len(_LABELS[key]):
        return None
    return row_scores(pred, _LABELS[key])


def rowlevel_tests(cfg, task, regime_method, comp_method, regime_comp):
    """Test-row evidence for one cell, per dataset: the seed-averaged predictions of the method under study and of the
    comparator are compared on the same test rows by a moving-block bootstrap (block = 1 week).

    Not DeLong per seed + Stouffer: test rows are autocorrelated (h-step labels overlap), which makes
    DeLong anti-conservative, and all seeds share one test set, so per-seed tests are not independent.
    Averaging over seeds and resampling week blocks handles both."""
    from sklearn.metrics import roc_auc_score

    out = []
    for ds in cfg.datasets:
        acc = {}                                    # (model, split) → {"a": [...], "b": [...], "y", "rows"}
        for seed in cfg.seeds:
            a, b = _rows(cfg, ds, E.CASE_METHOD, seed, task), _rows(cfg, ds, comp_method, seed, task)
            if a is None or b is None:
                continue
            a = a[(a["task"] == task) & (a["regime"] == regime_method)]
            b = b[(b["task"] == task) & (b["regime"] == regime_comp)]
            for (m, s), ga in a.groupby(["model", "split"], observed=True):
                gb = b[(b["model"] == m) & (b["split"] == s)]
                j = ga.merge(gb, on="row", suffixes=("_a", "_b")).sort_values("row")
                if len(j) < 50:
                    continue
                d = acc.setdefault((m, s), {"a": [], "b": [], "y": j["y_a"].to_numpy(), "rows": j["row"].to_numpy()})
                if len(j) != len(d["rows"]) or not np.array_equal(j["row"].to_numpy(), d["rows"]):
                    continue
                d["a"].append(j["score_a"].to_numpy())
                d["b"].append(j["score_b"].to_numpy())
        for (m, s), d in acc.items():
            if not d["a"]:
                continue
            sa, sb, y = np.mean(d["a"], axis=0), np.mean(d["b"], axis=0), d["y"]
            if R.tasks.get(task).kind == "clf":
                fn, sign = roc_auc_score, 1.0
                fn_rows = S.auc_rows if np.isin(y, (0, 1)).all() else None     # other labels: sklearn's loop
            else:                                   # per-row losses: compare mean loss, lower is better
                fn, sign = (lambda yy, sc: -float(np.mean(sc))), 1.0
                fn_rows = lambda yy, sc: -sc.mean(1)
            try:
                diff = sign * (fn(y, sa) - fn(y, sb))
            except ValueError:
                continue
            lo, hi, p2 = S.paired_block_bootstrap(fn, sa, sb, y, block=cfg.boot_block,
                                                  n_boot=max(200, cfg.n_boot // 4), seed=0, fn_rows=fn_rows)
            out.append(dict(dataset=ds, model=m, split=s, comparator=comp_method, n_seeds=len(d["a"]),
                            n_rows=len(y), diff=diff, boot_ci_lo=lo, boot_ci_hi=hi, p_boot=p2))
    r = pd.DataFrame(out)
    if len(r):
        r["p_boot_bh"] = S.bh(r["p_boot"].to_numpy())
    return r


def subgroup_tests(cfg):
    """Exploratory: AUC of the method under study vs rand (TSTR, task `stitch_task`) inside subgroups of test rows —
    weekend / weekday and volatility terciles of the real series."""
    from marathonts.bench.data import load_prepared

    from sklearn.metrics import roc_auc_score

    out = []
    for ds in cfg.datasets:
        p = load_prepared(ds, cfg)
        for split in cfg.test_splits:
            v, how = p.part(split)
            vol = pd.Series(v).diff().abs().rolling(24).mean().to_numpy()
            terc = pd.qcut(vol, 3, labels=["calm", "mid", "turbulent"]) if np.isfinite(vol).sum() > 30 else None
            groups = {"weekend": how >= 120, "weekday": how < 120}
            if terc is not None:
                for t in ("calm", "mid", "turbulent"):
                    groups[t] = np.asarray(terc == t)
            for seed in cfg.seeds:
                a, b = _rows(cfg, ds, E.CASE_METHOD, seed, E.CASE_TASK), _rows(cfg, ds, E.NOISE[0], seed, E.CASE_TASK)
                if a is None or b is None:
                    continue
                sel = lambda t: t[(t["task"] == E.CASE_TASK) & (t["regime"] == "S") & (t["split"] == split)]
                j = sel(a).merge(sel(b), on=["row", "model"], suffixes=("_a", "_b"))
                for gname, mask in groups.items():
                    jj = j[mask[j["row"].to_numpy()]]
                    for m, g in jj.groupby("model", observed=True):
                        y = g["y_a"].to_numpy()
                        if len(np.unique(y)) < 2:
                            continue
                        out.append(dict(dataset=ds, split=split, seed=seed, model=m, subgroup=gname,
                                        d_auc=roc_auc_score(y, g["score_a"]) - roc_auc_score(y, g["score_b"])))
    r = pd.DataFrame(out)
    if not len(r):
        return r
    s = r.groupby(["subgroup", "model", "split"]).apply(
        lambda g: pd.Series(dict(mean_d_auc=g["d_auc"].mean(),
                                 p_two_sided=S.wilcoxon(g.groupby("dataset")["d_auc"].mean())))).reset_index()
    s["p_bh"] = S.bh(s["p_two_sided"].to_numpy())
    return s


HYPOTHESES = {}
TITLES: dict = {}


def register_hypothesis(hid: str, title: str = "", overwrite: bool = False):
    """Decorator: `fn(tables, cfg) -> {"global": DataFrame, "per_dataset": DataFrame, "extra": dict}`.
    `tables` holds the benchmark tables (timing, fidelity, utility, cross_seed, datasets, pools)."""
    def deco(fn):
        if hid in HYPOTHESES and not overwrite:
            raise KeyError(f"hypothesis {hid} already registered")
        HYPOTHESES[hid], TITLES[hid] = fn, title
        return fn

    return deco


# the case study CS1–CS14 (CS15 = `h18_moderators`, run separately in run.py); `h0_noise` is used by RQ0
_BUILTIN = {
    "CS1": h1_train_fit, "CS2": h2_marginal_dependence, "CS3": h3_seams, "CS4": h4_long_structure,
    "CS5": h5_target_structure, "CS6": h6_window_equivalence, "CS7": h9_tstr_primary,
    "CS8": h10_tstr_other_tasks, "CS9": h7_fidelity_vs_alternatives, "CS10": h15_tstr_vs_alternatives,
    "CS11": h11_model_robustness, "CS12": h16_temporal_stability, "CS13": h8_tstr_vs_trtr, "CS14": h17_cost,
}
HYPOTHESES.update(_BUILTIN)



# ─────────────────────── case-study pre-specified cell ─────────────────────
def confirmatory(results: dict, cfg) -> pd.DataFrame:
    """The pre-specified cell of the case study (task `stitch_task`, linear model, OOT, TSTR) — CS7 (the method vs
    vae_rand) and CS10 (the method vs each long-series baseline present) — Holm-adjusted
    together. Not the benchmark's confirmatory family (`questions.confirmatory_rq`)."""
    m, s = CONFIRMATORY_CELL
    met = PRIMARY_METRIC[R.tasks.get(E.CASE_TASK).kind]
    unit = f"{E.CASE_TASK}|{m}|S|{s}|{met}"
    want = [("CS7", unit, E.NOISE[0])] + [("CS10", unit, b) for b in E.CONFIRMATORY_BASELINES]
    rows = []
    for h, u, comp in want:                          # the family is always these tests
        g = results.get(h, {}).get("global")
        r = g[(g["unit"] == u) & (g["comparator"] == comp)] if g is not None and len(g) else []
        if not len(r):
            rows.append(dict(hypothesis=h, comparator=comp, n_datasets=0, missing=True))
        else:
            r = r.iloc[0]
            rows.append(dict(hypothesis=h, comparator=comp, n_datasets=r.n_datasets, median_z=r.median_z,
                             ci_lo=r.ci_lo, ci_hi=r.ci_hi, p_better=r.p_better, p_worse=r.p_worse,
                             p_equiv=r.p_equiv, p_sign=r.p_sign, p_ttest=r.p_ttest,
                             n_better=r.n_better, n_worse=r.n_worse, n_same=r.n_same, missing=False))
    c = pd.DataFrame(rows)
    if c["missing"].all():
        return pd.DataFrame()
    for col in ("p_better", "p_worse", "p_equiv"):
        if col not in c:
            c[col] = np.nan
        # a missing test counts as p = 1: the Holm family stays the pre-specified one
        c[col + "_holm"] = S.holm(c[col].fillna(1.0).to_numpy())
    c["verdict"] = ["missing" if r.missing else
                    S.verdict(r.p_better_holm, r.p_worse_holm, r.p_equiv_holm, r.median_z, 1.0, cfg.alpha)
                    for r in c.itertuples()]
    return c
