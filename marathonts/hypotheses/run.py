"""Hypothesis part: benchmark tables → research questions, ranking, case study → REPORT.md.

    python -m marathonts.hypotheses.run [--artifacts-dir artifacts/min] [--only RQ2 CS3] [--plugins my_tests.py]

Reads `artifacts/<profile>/tables/*.parquet`, the predictions and labels (case study: CS7, CS12, CS13) and,
for the moderators (RQ7, CS15) and CS12 subgroups, `data/processed`. Writes the reports to
`artifacts/<profile>/reports/` — REPORT.md (research questions and case study), OVERALL.md (overall leaderboard),
LEADERBOARD.md (ranking by slice), METRIC_VALUES.md (values of the metrics by slice) — and their tables to
`artifacts/<profile>/hypotheses/`, `overall/`, `leaderboard/`, `metric_values/`.

* the overall leaderboard: fidelity on the core metrics and utility, noise-aware ranks, robustness checks
  (`overall.py`);
* the values of the metrics by slice (`metric_values.py`);
* RQ0–RQ9 — method-agnostic research questions (`questions.py`), the confirmatory family C1–C4;
* the ranking of every method in every slice (`leaderboard.py`, RQ1);
* CS1–CS15 — the case study of one method (`--case-method`, default `Config.case_method`), secondary.

Custom hypotheses (`hypotheses.catalog.register_hypothesis`) and statistical tests
(`hypotheses.stats.register_test`) are loaded with `--plugins`; they are reported with the case study.
"""
from __future__ import annotations

import argparse
import dataclasses
import sys
import traceback
from pathlib import Path

import pandas as pd

from marathonts.bench.config import Config  # noqa: E402

from marathonts.bench import registry as R  # noqa: E402
from marathonts.bench.run import load_plugins  # noqa: E402
from marathonts.bench.storage import write_table  # noqa: E402

from .catalog import HYPOTHESES, TITLES, confirmatory, h18_moderators  # noqa: E402
from .questions import QUESTION_TITLES, QUESTIONS, confirmatory_rq, rq7_moderators  # noqa: E402



BUILTIN_TITLES = {
    "CS1": "Distribution and dependence against train",
    "CS2": "Distribution and dependence against val",
    "CS3": "Seam artefacts",
    "CS4": "Structure longer than a window",
    "CS5": "Target structure",
    "CS6": "Realism of single windows and memorisation",
    "CS7": "TSTR of the method vs the random path (case-study task)",
    "CS8": "The same on the other tasks",
    "CS9": "Fidelity vs other stitchers of the same pool and the long-series generators",
    "CS10": "TSTR vs other stitchers of the same pool and the long-series generators",
    "CS11": "The method's effect on TSTR across model classes",
    "CS12": "The method's effect on TSTR over time (val vs OOT) and across subgroups",
    "CS13": "TSTR of the method vs TRTR",
    "CS14": "Computational cost of the method vs the others",
    "CS15": "Moderators of the method's effect (exploratory)",
}


for _h, _t in BUILTIN_TITLES.items():
    TITLES.setdefault(_h, _t)


def _save(df, path):
    """Hypothesis results as Parquet (columns of mixed objects are stringified)."""
    d = df.copy()
    for c in d.columns:
        if d[c].dtype == object:
            d[c] = d[c].map(lambda v: v if v is None or isinstance(v, (str, float, int)) else str(v))
    write_table(d, path)


def excluded_metric(col: str, cfg: Config) -> bool:
    """Is a table column left out by `Config.exclude_metrics`: the column itself, its fidelity metric id (every
    reference), `<id>@<reference>`, or a group prefix ending in "."."""
    from marathonts.bench.fidelity import split_ref

    ex = set(getattr(cfg, "exclude_metrics", None) or ())
    if not ex:
        return False
    base, ref = split_ref(col, cfg.fidelity_ref)
    return bool({col, base, f"{base}@{ref}"} & ex) or any(x.endswith(".") and base.startswith(x) for x in ex)


def load_tables(cfg: Config) -> dict:
    """The benchmark tables, without the (method, dataset) pairs of `Config.leaked` (a dataset in the
    method's training corpus, e.g. Chronos × electricity) — every ranking, question and case-study test —,
    without the datasets of `Config.exclude_datasets` and the metric columns of `Config.exclude_metrics`.
    With `Config.utility_fail_penalty`, the TSTR cells a method's series could not train enter as a
    model that learned nothing (`catalog.impute_failed_utility`, column `imputed`)."""
    from .catalog import PRIMARY_METRIC, configure, impute_failed_utility

    configure(cfg)
    t = Path(cfg.artifacts_dir) / "tables"
    out = {}
    leaked = {(m, d) for m, ds in (getattr(cfg, "leaked", None) or {}).items() for d in ds}
    drop_ds = set(getattr(cfg, "exclude_datasets", None) or ())
    keep_cols = {"dataset", "method", "seed", "task", "task_kind", "model", "regime", "split"}
    for name in ("timing", "fidelity", "utility", "cross_seed", "datasets", "pools"):
        f = t / f"{name}.parquet"
        d = pd.read_parquet(f) if f.exists() else pd.DataFrame()
        if leaked and len(d) and {"method", "dataset"} <= set(d.columns):
            base = d["method"].astype(str).str.removesuffix("@len")
            d = d[[(m, ds) not in leaked for m, ds in zip(base, d["dataset"])]].reset_index(drop=True)
        if drop_ds and len(d) and "dataset" in d:
            d = d[~d["dataset"].isin(drop_ds)].reset_index(drop=True)
        if name in ("fidelity", "utility") and len(d):
            drop = [c for c in d.columns if c not in keep_cols and excluded_metric(c, cfg)]
            if name == "utility" and set(drop) & set(PRIMARY_METRIC.values()):
                raise ValueError(f"exclude_metrics: {sorted(set(drop) & set(PRIMARY_METRIC.values()))} is the "
                                 "primary metric of a task type (Config.primary_metrics)")
            d = d.drop(columns=drop)
        if name == "utility" and getattr(cfg, "utility_fail_penalty", True):   # after the leak filter
            d = impute_failed_utility(d)
        out[name] = d
    return out


def check_tables(T: dict, cfg: Config) -> list[str]:
    """Warnings about analysis roles and choices the tables cannot serve (printed, returned): the noise pair, the
    case-study method, the baselines, core metrics and task types without a primary metric or a criterion of
    the four rankings. Nothing stops: the affected parts are empty or skipped."""
    from marathonts.bench.fidelity import split_ref

    from .catalog import PRIMARY_METRIC
    from .leaderboard import CORE_METRICS, UT_CRITERIA

    fid, ut = T.get("fidelity", pd.DataFrame()), T.get("utility", pd.DataFrame())
    methods = set(fid["method"]) if len(fid) else set()
    out = []
    a, b = tuple(cfg.noise_pair)
    if a not in methods:
        out.append(f"noise_pair[0] {a!r} is not in the tables: no noise margins (verdicts inconclusive), no "
                   "noise-aware ties, no anchors / normalised scores, no RQ3, C3, C4 — set Config.noise_pair")
    if cfg.case_method not in methods:
        out.append(f"case_method {cfg.case_method!r} is not in the tables: the case study is skipped")
    pools = sorted({R.methods.get(m).pool for m in methods if m in R.methods and R.methods.get(m).pool})
    if len(pools) > 1:
        own = R.methods.get(a).pool if a in R.methods else None
        out.append(f"methods of several pool generators ({', '.join(pools)}): all are ranked (RQ1, overall leaderboard; "
                   f"normalised scores against their own pool's random assembly), but the assembly median (RQ2, C2) "
                   f"and the selection / seam-processing contrasts (RQ3, C3, C4) use the pool of noise_pair ({own})")
    miss = [m for m in (cfg.baselines or []) if m not in methods]
    if miss:
        out.append(f"baselines not in the tables: {', '.join(miss)}")
    if len(fid):
        have = {split_ref(c, cfg.fidelity_ref)[0] for c in fid.columns}
        for crit, ms in CORE_METRICS.items():
            lost = [m for m in ms if m not in have]
            if lost:
                out.append(f"core metrics of {crit} not in the tables: {', '.join(lost)}"
                           + (" — the criterion is empty" if len(lost) == len(ms) else ""))
    if len(ut) and "task_kind" in ut:
        kinds = set(ut["task_kind"]) - {"grid", "threshold"}
        for k in sorted(kinds - set(PRIMARY_METRIC)):
            out.append(f"task type {k!r} has no primary metric (Config.primary_metrics): left out of the analysis")
        for k in sorted(kinds - set(UT_CRITERIA)):
            out.append(f"task type {k!r} has no utility criterion (Config.task_criteria): it forms its own, which "
                       "the four rankings (classification / regression) do not include; the overall leaderboard does")
        from .catalog import UT_DIAGNOSTICS, UT_ORIENT

        odd = [c for c in ut.columns if c not in UT_ORIENT and c not in UT_DIAGNOSTICS
               and c not in ("dataset", "method", "seed", "task", "task_kind", "model", "regime", "split")
               and pd.api.types.is_numeric_dtype(ut[c])]
        if odd:
            out.append(f"utility columns without an orientation are not analysed: {', '.join(odd)} "
                       "(Config.metric_orient)")
    for w in out:
        print(f"WARNING: {w}")
    return out


def _verdict_counts(glob: pd.DataFrame) -> str:
    """Summary line of a question: verdict counts, or the count of flagged rows of a table without
    verdicts (discriminative metrics in RQ0, predictive metrics in RQ4, significant moderators)."""
    if glob is None or not len(glob):
        return ""
    if "verdict" in glob:
        v = glob["verdict"].value_counts()
        keys = [k for k in ("better", "worse", "same", "inconclusive") if k in v] + \
               [k for k in v.index if k not in ("better", "worse", "same", "inconclusive")]
        return ", ".join(f"{k}: {int(v[k])}" for k in keys)
    for col, label in (("discriminative", "discriminative metrics"), ("predictive", "predictive pairs")):
        if col in glob:
            return f"{label}: {int(glob[col].sum())} of {len(glob)}"
    if "p_bh" in glob:
        return f"significant after BH: {int((glob['p_bh'] < 0.05).sum())} of {len(glob)}"
    if {"column", "best", "p_friedman"} <= set(glob.columns) and glob["column"].str.startswith("ranking:").any():
        from .leaderboard import RANKINGS

        best = glob.set_index("column")
        return "first by ranking: " + "; ".join(
            f"{k} — {best.loc[c, 'best']} (Friedman p = {best.loc[c, 'p_friedman']:.3g})"
            for k in RANKINGS if (c := f"ranking:{k}") in best.index)
    if "median_time_s" in glob and "method" in glob:
        r = glob.sort_values("median_time_s").iloc[0]
        return f"fastest: {r['method']} ({r['median_time_s']:.0f} s)"
    return ""


def _significant_first(g: pd.DataFrame) -> pd.DataFrame:
    """Rows with a conclusion first (better / worse / same, then by p), so the truncated report table
    shows them; the full table is in the parquet."""
    if "verdict" not in g:
        return g
    key = g["verdict"].map({"better": 0, "worse": 0, "same": 1}).fillna(2)
    p = g[[c for c in ("p_better_adj", "p_worse_adj") if c in g]].min(axis=1) if \
        {"p_better_adj", "p_worse_adj"} & set(g.columns) else pd.Series(0.0, index=g.index)
    return g.assign(_k=key, _p=p).sort_values(["_k", "_p"]).drop(columns=["_k", "_p"])


def _md_table(df: pd.DataFrame, cols: list[str], n: int = 40) -> str:
    cols = [c for c in cols if c in df.columns]
    if not len(df) or not cols:
        return "_no data_\n"
    d = df[cols].head(n).copy()
    d.columns = [str(c) for c in d.columns]
    for c in d.columns:
        if d[c].dtype.kind == "f":
            d[c] = d[c].map(lambda x: "" if pd.isna(x) else f"{x:.3g}")
    esc = lambda x: str(x).replace("|", "\\|")      # unit ids (task|model|…) would split the cells
    head = "| " + " | ".join(map(esc, d.columns)) + " |\n|" + "---|" * len(cols) + "\n"
    return head + "\n".join("| " + " | ".join(esc(x) for x in r) + " |" for r in d.itertuples(index=False)) + "\n"


def _section(lines, hid, title, r, main_cols):
    lines += [f"### {hid}. {title}", ""]
    g = r.get("global")
    if g is not None and len(g):
        cols = main_cols if "median_z" in g.columns else list(g.columns)
        if "comparison" in g.columns and "median_z" in g.columns:
            cols = ["comparison", "kind", *[c for c in main_cols if c not in ("comparator",)]]
        lines.append(_md_table(_significant_first(g), cols))
        if len(g) > 40:
            order = " (rows with a better / worse / same verdict first)" if "verdict" in g else ""
            lines += [f"_Showing 40 rows of {len(g)}{order}; all of them — `hypotheses/{hid}_global.parquet`._", ""]
    for k, v in (r.get("extra") or {}).items():
        if isinstance(v, pd.Series):
            v = v.to_frame()
        if isinstance(v, pd.DataFrame):
            if len(v):
                v = v.reset_index() if (v.index.name or isinstance(v.index, pd.MultiIndex)) else v
                lines += [f"**{k}**", "", _md_table(v, list(v.columns)), ""]
        elif v:
            lines += [f"**{k}**: {v}", ""]


def write_report(results: dict, cfg: Config, out: Path, overall: dict | None = None):
    a_, b_ = tuple(cfg.noise_pair)
    left = [f"`{m}` on {', '.join(ds)}" for m, ds in (cfg.leaked or {}).items() if ds]
    lines = ["# Benchmark report", "",
             f"Datasets: {', '.join(cfg.datasets)}. Seeds: {len(cfg.seeds)}. α = {cfg.alpha}. "
             + (f"Left out of the analysis: datasets {', '.join(cfg.exclude_datasets)} (Config.exclude_datasets). "
                if cfg.exclude_datasets else "")
             + (f"Metrics left out: {', '.join(cfg.exclude_metrics)} (Config.exclude_metrics). "
                if cfg.exclude_metrics else "")
             + (f"Leakage (Config.leaked): {'; '.join(left)}. " if left else "")
             + "Verdict of a "
             "comparison \"A vs B\": better / worse (A better / worse than B) / same (equivalence, TOST) / "
             "inconclusive. Effects are in noise units — divided by the smallest effect size of interest (SESOI: "
             f"the median |{a_} − {b_}| on one pool — or, where {b_} is not run (min), the between-seed "
             f"spread of {a_} — or the method's between-seed spread, see HYPOTHESES.md "
             "§2). Utility: TSTR (training on synthetic data only) vs TRTR (training on real data), tested on the "
             "real val / OOT; transfer ratio = 1 — synthetic data train the model as well as real data. Overall "
             "leaderboard — `OVERALL.md`; ranking of every method in every slice — `LEADERBOARD.md`; values of the "
             "metrics by slice — `METRIC_VALUES.md` (this folder). Tables of the tests — `hypotheses/`.", ""]
    if len(cfg.datasets) < 3:
        lines += [f"> Datasets: {len(cfg.datasets)}. The global tests need at least 3 datasets — "
                  "there are no global verdicts and no confirmatory inference; see the per-dataset tables "
                  "(`hypotheses/*_per_dataset.parquet`).", ""]
    if len(cfg.seeds) < 5:
        lines += [f"> Seeds: {len(cfg.seeds)}. With < 5 seeds the per-dataset verdicts are almost always "
                  "inconclusive (the minimum Wilcoxon p ≥ 1/2^n).", ""]
    ov = (overall or {}).get("main")
    if isinstance(ov, pd.DataFrame) and len(ov):
        cols = ["family", "avg_rank", "ci_lo", "ci_hi", "p_first", "p_top3", "p_worse_than_best_holm", "tier_wilcoxon",
                "fidelity_rank", "utility_rank", "norm_overall", "memorisation_flag"]
        v = overall["variants"].reset_index()
        lines += ["## Overall leaderboard", "",
                  "Fidelity on the core metrics (each criterion against train, val and OOT) and utility (TSTR "
                  "classification and regression, val and OOT), equal weights; noise-aware ranks; privacy and cost "
                  "not included. Composition, columns and the robustness checks — `OVERALL.md`.", "",
                  _md_table(ov.reset_index().rename(columns={"index": "method"}), ["method", *[c for c in cols if c in ov]]),
                  "", "Sensitivity variants:", "",
                  _md_table(v, ["variant", "text", "first", "tau_vs_main", "main_first_place"]), ""]
    conf = results.get("confirmatory_rq")
    lines += ["## Confirmatory inference (C1–C4; TSTR, linear model, OOT; one classification and "
              "regression task; Holm over the whole family)", ""]
    lines.append(_md_table(conf, ["test", "cell", "comparison", "n_datasets", "median_z", "ci_lo", "ci_hi",
                                  "p_two_sided", "p_holm", "p_equiv_holm", "n_better", "n_worse", "verdict"])
                 if isinstance(conf, pd.DataFrame) else "_no data_\n")
    rq1 = results.get("RQ1", {}).get("extra", {})
    lb = rq1.get("rankings")
    if isinstance(lb, pd.DataFrame) and len(lb):
        from .leaderboard import RANKINGS

        lines += ["", "## The four rankings (RQ1)", "",
                  "Composition of each ranking, the meaning of every column and the privacy and cost tables — "
                  "`LEADERBOARD.md`.", "",
                  *[f"- `{k}` — **{d['title']}**. {d['text']}" for k, d in RANKINGS.items()], "",
                  _md_table(lb.reset_index().rename(columns={"index": "method"}), ["method", *lb.columns]), ""]
        for k, d in RANKINGS.items():                # the leaderboard of every ranking
            t = rq1.get(f"ranking_{k}")
            if isinstance(t, pd.DataFrame) and len(t):
                t = t.reset_index().rename(columns={"index": "method"})
                lines += [f"### Ranking `{k}`: {d['title']}", "", _md_table(t, list(t.columns)), ""]
    lbc = rq1.get("rankings_core")
    if isinstance(lbc, pd.DataFrame) and len(lbc):
        from .leaderboard import _CORE_LIST

        lines += ["", "## Core-metric rankings (RQ1)", "",
                  "The four rankings with the fidelity domain restricted to the core metric set, fixed in advance: "
                  f"{_CORE_LIST}. Utility unchanged. Each core ranking, the normalised scores (random assembly = 0, "
                  "real data = 1) and the anchor check — `LEADERBOARD.md`.", "",
                  _md_table(lbc.reset_index().rename(columns={"index": "method"}), ["method", *lbc.columns]), ""]
    ns = rq1.get("normalized_scores")
    if isinstance(ns, pd.DataFrame) and len(ns):
        lines += ["### Normalised scores on the core metrics (random assembly = 0, real data = 1)", "",
                  _md_table(ns.reset_index().rename(columns={"index": "method"}), ["method", *ns.columns]), ""]
    lines += ["", "## Summary", "", "| Question | Verdicts by comparison |", "|---|---|"]
    rq = {h: r for h, r in results.items() if h.startswith("RQ")}
    cs = {h: r for h, r in results.items() if not h.startswith("RQ") and h not in ("confirmatory_rq", "case_cell")}
    for h, r in rq.items():
        lines.append(f"| {h}. {QUESTION_TITLES.get(h, '')} | {_verdict_counts(r.get('global'))} |")
    lines.append("")
    main_cols = ["unit", "comparator", "n_datasets", "median_z", "mean_z", "ci_lo", "ci_hi", "p_better_adj", "p_worse_adj",
                 "p_equiv_adj", "n_better", "n_worse", "n_same", "verdict"]
    lines += ["## Research questions", ""]
    for h, r in rq.items():
        _section(lines, h, QUESTION_TITLES.get(h, ""), r, main_cols)
    if cs:
        lines += ["## Case study: method " + f"`{cfg.case_method}` (secondary, BH within a hypothesis)", "",
                  f"Method `{cfg.case_method}` vs the controls on its own pool, alternative stitchers and long-series "
                  "generators. Sign of the effect: > 0 — the method is better than the comparator. Pre-specified cell "
                  f"(TSTR, task {cfg.stitch_task}, linear model, OOT; Holm over CS7 and CS10):", ""]
        cp = results.get("case_cell")
        lines.append(_md_table(cp, ["hypothesis", "comparator", "n_datasets", "median_z", "ci_lo", "ci_hi",
                                    "p_better_holm", "p_worse_holm", "p_equiv_holm", "n_better", "n_worse",
                                    "n_same", "verdict"]) if isinstance(cp, pd.DataFrame) else "_no data_\n")
        lines += ["", "| Hypothesis | Verdicts |", "|---|---|"]
        for h, r in cs.items():
            lines.append(f"| {h}. {TITLES.get(h, '')} | {_verdict_counts(r.get('global'))} |")
        lines.append("")
        for h, r in cs.items():
            _section(lines, h, TITLES.get(h, ""), r, main_cols)
    out.write_text("\n".join(lines))


def _run_config(a) -> Config:
    """The config the tables were made with (`tables/config.json`, written by `collect`), so roles,
    the task of the case-study cells and the processed data match the run even without `--profile`. Paths of
    another machine (Colab vs Docker) fall back to this checkout's folders of that profile."""
    cfg = Config.profile(a.profile)
    art = Path(a.artifacts_dir) if a.artifacts_dir else cfg.artifacts_dir
    saved = art / "tables" / "config.json"
    if not saved.exists():
        return cfg
    run = Config.from_json(saved.read_text())
    if run.profile_name != a.profile and run.profile_name in ("min", "mid", "max"):
        print(f"tables were made with profile {run.profile_name} (not {a.profile}): using their config")
    base = Config.profile(run.profile_name) if run.profile_name in ("min", "mid", "max") else cfg
    fix = {f.name: getattr(base, f.name) for f in dataclasses.fields(Config)
           if f.name.endswith(("_dir", "_file")) and not Path(getattr(run, f.name)).exists()}
    fix.pop("artifacts_dir", None)                   # set below from this machine
    # analysis settings (`Config.ANALYSIS_KEYS`: leakage list, exclusions, metric choices) are the current ones
    # of the code, not the copy saved with the tables (e.g. a pair of `LEAKED` the saved copy does not list)
    ana = {k: getattr(base, k) for k in Config.ANALYSIS_KEYS}
    for k, v in ana.items():
        if getattr(run, k) != v:
            print(f"{k}: the current setting {v} replaces the one saved with the tables {getattr(run, k)}")
    return dataclasses.replace(run, **fix, **ana, artifacts_dir=art)


def add_analysis_args(ap: argparse.ArgumentParser) -> None:
    """CLI flags of the analysis settings (`Config.ANALYSIS_KEYS`), shared by run, leaderboard and overall."""
    ap.add_argument("--exclude-datasets", nargs="*", metavar="DATASET",
                    help="datasets left out of the analysis (Config.exclude_datasets); their units stay on disk")
    ap.add_argument("--exclude-metrics", nargs="*", metavar="METRIC",
                    help="metrics left out of the analysis (Config.exclude_metrics): fidelity id, id@ref, group "
                         "prefix ending in '.', or a utility metric")
    ap.add_argument("--leaked", help='JSON {method: [datasets]} replacing Config.leaked ("{}" — nothing left out)')
    ap.add_argument("--noise-estimator", help='supplementary: between-seed differences of the noise margin — '
                    '"neighbours" (pre-specified), "pairs" or "perm:<n>"')
    ap.add_argument("--noise-scale", type=float, help="supplementary: factor on every noise margin (default 1)")
    ap.add_argument("--fail-rule", choices=["worst", "chance"],
                    help="supplementary: value of a utility cell the series could not train (default worst)")
    ap.add_argument("--ci-stat", choices=["mean", "median"],
                    help="supplementary: statistic of the global bootstrap interval over datasets (default mean)")


def apply_analysis_args(cfg: Config, a) -> Config:
    import json

    over = {}
    if getattr(a, "exclude_datasets", None) is not None:
        over["exclude_datasets"] = list(a.exclude_datasets)
    if getattr(a, "exclude_metrics", None) is not None:
        over["exclude_metrics"] = list(a.exclude_metrics)
    if getattr(a, "noise_estimator", None):
        over["noise_estimator"] = a.noise_estimator
    if getattr(a, "fail_rule", None):
        over["utility_fail_rule"] = a.fail_rule
    if getattr(a, "ci_stat", None):
        over["ci_stat"] = a.ci_stat
    if getattr(a, "noise_scale", None) is not None:
        over["noise_scale"] = float(a.noise_scale)
    if getattr(a, "leaked", None) is not None:
        over["leaked"] = {k: list(v) for k, v in json.loads(a.leaked).items()}
    return dataclasses.replace(cfg, **over) if over else cfg


def _store(r, res_dir, h):
    for k in ("global", "per_dataset"):
        if isinstance(r.get(k), pd.DataFrame) and len(r[k]):
            _save(r[k], res_dir / f"{h}_{k}.parquet")
    for k, v in (r.get("extra") or {}).items():
        if isinstance(v, pd.Series):
            v = v.to_frame()
        if isinstance(v, pd.DataFrame) and len(v):
            _save(v.reset_index() if (v.index.name or isinstance(v.index, pd.MultiIndex)) else v,
                  res_dir / f"{h}_{k}.parquet")


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--artifacts-dir")
    ap.add_argument("--processed-dir")
    ap.add_argument("--out-dir", help="base folder of the results (default: <artifacts>): reports/ (REPORT.md, OVERALL.md, "
                    "LEADERBOARD.md, METRIC_VALUES.md) and the tables in hypotheses/, overall/, leaderboard/, metric_values/")
    ap.add_argument("--only", nargs="*", help="RQ… / CS… ids (default: all)")
    ap.add_argument("--no-case-study", action="store_true", help="only the research questions and the ranking")
    ap.add_argument("--plugins", nargs="*", help="Python files registering hypotheses, tests, metrics, …")
    ap.add_argument("--config", help="JSON written by Config.to_json()")
    ap.add_argument("--profile", choices=["min", "mid", "max"], default="min")
    ap.add_argument("--case-method", dest="case_method", help="method of the case study (default: Config.case_method)")
    ap.add_argument("--noise-pair", nargs=2, help="two random paths on the same pool")
    ap.add_argument("--baselines", nargs="*")
    ap.add_argument("--case-task", dest="case_task",
                    help="task of the case-study cells (CS7, CS10, CS12, CS13); default: Config.stitch_task")
    ap.add_argument("--rank-exclude", nargs="*", metavar="METHOD",
                    help="methods left out of the rankings (default: Config.rank_exclude — the seam-processing variants, unless every stitcher has them); no names — rank every method")
    ap.add_argument("--no-fail-penalty", dest="fail_penalty", action="store_false", default=None,
                    help="leave out the TSTR cells a method's series could not train instead of entering them as a "
                         "model that learned nothing (Config.utility_fail_penalty)")
    add_analysis_args(ap)
    a = ap.parse_args(argv)
    import marathonts.bench.config as C

    C.RUN_CONTEXT = False                            # the methods without code are read from the published tables
    load_plugins(a.plugins)
    R.load_builtins()
    cfg = Config.from_json(Path(a.config).read_text()) if a.config else _run_config(a)
    run_cfg = cfg                                    # the settings the units were made with (row-level freshness)
    over = {k: v for k, v in dict(case_method=a.case_method, noise_pair=tuple(a.noise_pair) if a.noise_pair else None,
                                  baselines=a.baselines,
                                  stitch_task=a.case_task).items() if v}
    cfg = dataclasses.replace(cfg, **over)
    if a.rank_exclude is not None:                   # [] → rank every method
        cfg = dataclasses.replace(cfg, rank_exclude=list(a.rank_exclude))
    if a.fail_penalty is not None:
        cfg = dataclasses.replace(cfg, utility_fail_penalty=a.fail_penalty)
    if a.artifacts_dir:
        cfg = dataclasses.replace(cfg, artifacts_dir=Path(a.artifacts_dir))
    if a.processed_dir:
        cfg = dataclasses.replace(cfg, processed_dir=Path(a.processed_dir))
    cfg = apply_analysis_args(cfg, a)
    run_cfg = dataclasses.replace(run_cfg, artifacts_dir=cfg.artifacts_dir, processed_dir=cfg.processed_dir)
    T = load_tables(cfg)
    present = sorted(T["fidelity"]["dataset"].unique()) if len(T["fidelity"]) else cfg.datasets
    seeds = sorted(T["fidelity"]["seed"].unique()) if len(T["fidelity"]) else cfg.seeds
    # every method present in the tables (custom ones included)
    methods = sorted(set(T["timing"]["method"])) if len(T["timing"]) else list(cfg.methods)
    # the analysis covers every method of the tables, the frozen ones too: the run switches do not apply
    cfg = dataclasses.replace(cfg, datasets=present, seeds=[int(s) for s in seeds], methods=methods,
                              disabled=[], frozen_methods=[])
    from marathonts.bench.config import PRESPECIFIED_LONG

    # case study: the pre-specified baselines (Diffusion-TS, Chronos) of the run, present or not (missing → p = 1)
    planned = [b for b in cfg.baselines if b in PRESPECIFIED_LONG]
    if not a.baselines:                              # the baselines of the config present in the tables
        cfg = dataclasses.replace(cfg, baselines=[b for b in cfg.baselines if b in methods])
    else:
        planned = [b for b in a.baselines if b in PRESPECIFIED_LONG]
    print(f"profile {cfg.profile_name} | processed {cfg.processed_dir} | case study {cfg.case_method} | "
          f"{len(methods)} methods | {len(present)} datasets × {len(seeds)} seeds")
    from . import engine as E
    from . import leaderboard as LB
    from . import questions as Q

    check_tables(T, cfg)
    E.configure(cfg)
    E.CONFIRMATORY_BASELINES = tuple(dict.fromkeys(planned))
    E.RUN_CFG = run_cfg
    base = Path(a.out_dir) if a.out_dir else Path(cfg.artifacts_dir)
    res_dir, rep_dir = base / "hypotheses", base / "reports"
    res_dir.mkdir(parents=True, exist_ok=True)
    want = lambda h: not a.only or h in a.only     # noqa: E731
    results = {}
    jobs = [(h, fn) for h, fn in QUESTIONS.items()]
    if not a.no_case_study and cfg.case_method not in methods:
        print(f"case study skipped: {cfg.case_method} is not in the tables (--case-method to choose another)")
        a.no_case_study = True
    if not a.no_case_study:
        jobs += [(h, fn) for h, fn in HYPOTHESES.items()]
    for h, fn in jobs:
        if not want(h):
            continue
        print(f"── {h}", flush=True)
        try:
            results[h] = fn(T, cfg)
        except Exception as e:
            print(f"   FAILED {h}: {type(e).__name__}: {e}")
            traceback.print_exc()
            continue
        _store(results[h], res_dir, h)
    for h, fn in (("RQ7", rq7_moderators), ("CS15", h18_moderators)):
        if not want(h) or (h.startswith("CS") and a.no_case_study):
            continue
        try:
            results[h] = fn(results, cfg)
            _store(results[h], res_dir, h)
        except Exception as e:                       # needs the dataset descriptors (data or table)
            print(f"   SKIPPED {h} (needs data/processed or tables/descriptors.parquet): {type(e).__name__}: {e}")
    if not a.only:
        try:
            conf = confirmatory_rq(T, cfg)
            _save(conf, res_dir / "confirmatory.parquet")
            results["confirmatory_rq"] = conf
        except Exception as e:
            print(f"   FAILED confirmatory: {type(e).__name__}: {e}")
            traceback.print_exc()
        if not a.no_case_study:
            cp = confirmatory(results, cfg)
            if len(cp):
                _save(cp, res_dir / "case_cell.parquet")
            results["case_cell"] = cp
        try:
            print(f"leaderboard → {LB.write(Q.leaderboard(T, cfg), cfg, base / 'leaderboard', rep_dir)}")
        except Exception as e:                       # the report is still written
            print(f"   FAILED leaderboard: {type(e).__name__}: {e}")
            traceback.print_exc()
        from . import overall as OV

        ov_dir = base / "overall"
        try:
            overall = OV.build(T, cfg)
            print(f"overall leaderboard → {OV.write(overall, cfg, ov_dir, rep_dir)}")
        except Exception as e:
            print(f"   FAILED overall leaderboard: {type(e).__name__}: {e}")
            traceback.print_exc()
            overall = None
            for f in ov_dir.glob("*"):               # a failed build leaves no overall tables behind
                f.unlink()
    else:
        overall = None
    order = sorted([*QUESTIONS, "RQ7"], key=lambda h: int(h[2:]))
    results = {**{h: results[h] for h in order if h in results},
               **{h: r for h, r in results.items() if h not in order}}
    if not a.only:
        from . import metric_values as MV

        try:
            print(f"metric values → {MV.write(MV.build(T, cfg), cfg, base / 'metric_values', rep_dir)}")
        except Exception as e:
            print(f"   FAILED metric values: {type(e).__name__}: {e}")
            traceback.print_exc()
    rep_dir.mkdir(parents=True, exist_ok=True)
    write_report(results, cfg, rep_dir / "REPORT.md", overall)
    print(f"report → {rep_dir / 'REPORT.md'}")


if __name__ == "__main__":
    main()
