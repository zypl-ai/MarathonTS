"""Experiment configuration: one place for every knob of the pipeline.

Profiles:
* `Config()` / `Config.profile("min")` — the run for Colab: last 10 000 points per dataset, a pool
  of 300 VAE windows, every stitching method (the random path, the alternative stitchers of BASELINES.md A–B; the
  zseries stitcher and its seam-processing variants as published results, `frozen_methods`) except the noise twin `vae_rand_b` (`noise_twin`; margins from the between-seed spread),
  the long-series baselines Diffusion-TS (trained once per dataset), Chronos, TimesFM and Timestral,
  fixed (exogenous) model hyperparameters, MLP only on one task (clf_up_h24_q90), no decision-transfer grid
  (RQ5 c).
* `Config.profile("mid")` — min + the VAE retrained on every seed (90 trainings instead of 9: independent
  seeds) and the noise twin `vae_rand_b`; Diffusion-TS stays one model per dataset as in min
  (`diffusion_train_replicas` raises it). Shares min's processed data.
* `Config.profile("max")` — everything: whole series, hyperparameter search per fit (grid in
  `model_configs.json`, chosen on the tail of the regime's own training data — synthetic in TSTR), the
  larger Chronos (`chronos-t5-base`, about the size of TimesFM and Timestral), MLP on every task with early
  stopping, the decision-transfer grid (RQ5 c), Diffusion-TS retrained on every seed, the noise twin
  `vae_rand_b`, and every seam processing over every stitcher (`smooth_paths="all"`).

The stitching suite (`STITCH_SUITE`) runs on every pool generator of `pool_suites` (default
{"vae": "tsgm_vae"}): another generator is one entry more, e.g. `pool_suites={"vae": "tsgm_vae",
"gan": "my_gan"}` with `methods=None` adds gan_zseries, gan_rand, … to the run. Custom components come
from plugin files (`plugins`, loaded with the config) and one line each: `extra_assemblers` (a
stitcher on every pool), `extra_joiners` (seam processing),
`long_methods` (long-series generators, also the baselines) — EXTENDING.md. Seam processing runs over the
stitchers of `smooth_paths` (min / mid: the zseries stitcher; max: "all" — every stitcher but the random
path) with the joiners of `joiners` (None: all). `disabled` switches off any method or component by name;
`frozen_methods` keeps published results of methods that are not run (their code is not part of the
repository): by default `vae_zseries` — zseries, the proprietary stitching method of zypl.ai (under
development) — and its seam-processing variants (`FROZEN_METHODS`).

Utility trains every model in two regimes only: R (TRTR — train on real, test on real) and S (TSTR
— train on synthetic, test on real); how close TSTR comes to TRTR measures the synthetic data.
* `Config.quick()` — smoke test (tiny models, 2 datasets, 2 seeds).
Every switch is also an ordinary field and can be set on its own. Each profile has its own
processed-data and artifacts folders, so their results never mix.

Components are referred to by their registry names (`bench.registry`). Parameters of custom
components go to `extra[<component name>]` and reach the component as `cfg.params(name)`.
"""
from __future__ import annotations

import dataclasses
import json
import os
from dataclasses import dataclass, field
from pathlib import Path

# the package's own files (task thresholds, model configurations, data hashes) live next to this module; the
# working folders (data/, artifacts/, external/) are taken from the project folder: MARATHONTS_HOME if set, else the
# current directory (the repository root when it is run from a clone)
PKG = Path(__file__).resolve().parent
ROOT = Path(os.environ.get("MARATHONTS_HOME") or Path.cwd()).resolve()

DATASETS = ["ett", "electricity", "household", "pjm", "beijing_pm25", "jena", "metro", "bike", "bitcoin"]

# The stitching suite run on every pool generator: the zseries stitcher, the random path and its noise twin, the
# alternative stitchers (BASELINES.md A). Seam processing (B, `JOINERS`) is added over the stitchers of
# `Config.smooth_paths`. Method name = f"{prefix}_{suffix}"; `Config.pool_suites` maps a prefix to a pool
# generator ({"vae": "tsgm_vae"} → vae_zseries, vae_rand, …). Entries: (suffix, assembler, joiner, description).
STITCH_SUITE = [
    ("zseries", "zseries", None, "zseries: proprietary stitching method of zypl.ai, under development (published results)"),
    ("rand", "random", None, "random path, same pool"),
    ("rand_b", "random_b", None, "noise twin of the random path (mid, max)"),
    ("greedy", "greedy", None, "nearest neighbour by the jump at the seam"),
    ("atsp", "atsp", None, "ATSP tour (LKH) by the jump at the seam, cheapest run of K"),
    ("pctsp", "pctsp", None, "prize-collecting TSP (OR-Tools) by the jump at the seam"),
    ("mbb", "mbb", None, "matched-block bootstrap (Carlstein et al. 1998)"),
    ("knn", "knn", None, "k-nearest-neighbour resampling (Lall & Sharma 1996)"),
    ("quilting", "quilt_sel", "quilt", "image quilting: patch choice + boundary cut (Efros & Freeman 2001)"),
    ("herding", "herding", None, "kernel-herding choice, random order"),
]
# built-in seam processing (`marathonts/bench/joiners.py`) → suffix of its variants: <prefix>_<stitcher>_<tag>
JOINERS = {"crossfade": "xfade", "wsola": "wsola", "quilt": "quilt"}
POOL_SUITES = {"vae": "tsgm_vae"}
LONG_BASELINES = ["diffusion_ts", "chronos", "timesfm", "timestral"]
# the long-series generators of the pre-specified tests (confirmatory C2, case-study cell CS10), fixed in advance:
# generators added later are compared everywhere else but do not change these families
PRESPECIFIED_LONG = ("diffusion_ts", "chronos")


SCOPE_KEYS = ("pool_suites", "extra_assemblers", "extra_joiners", "long_methods", "smooth_paths", "joiners",
              "disabled", "noise_twin", "frozen_methods")
# assemblers that never get a joiner: the random path and its noise twin are the zero point of assembly,
# not ways of assembling
_NO_JOINER = ("random", "random_b")
# method → datasets whose object is in its training corpus (results there are not out-of-sample): left
# out of the analysis (rankings, questions, case study). Rule: the same data (exact) or the same object —
# dataset, city and pollutant, asset — at other stations, years or resolution (related), whether or not
# the periods overlap (DATASETS.md, "Leakage into pretrained models").
#   Chronos (Ansari et al., 2024, Table 3): Electricity (UCI) up to the last 24 points — exact;
#     KDD Cup 2018 (Beijing air quality, 2017–2018) — related to beijing_pm25.
#   TimesFM 3.0 (GiftEvalPretrain): `sceaux` = UCI #235 household, value-identical 2007–2010 — exact;
#     Beijing Air Quality (UCI #501, 12 stations, 2013–2017) — related to beijing_pm25;
#     Monash Bitcoin (daily price, to 2021) — related to bitcoin.
#   Timestral: training data not disclosed, nothing can be checked.
LEAKED = {"chronos": ["electricity", "beijing_pm25"], "timesfm": ["beijing_pm25", "household", "bitcoin"]}
# data settings of one dataset only (`Config.SPLIT_KEYS`): they enter that dataset's keys (`split_key`, `data_key`,
# unit fingerprints); every other dataset hashes them at fixed values (`PINNED_KEYS`), so changing them
# redoes that dataset only and leaves the keys of the others unchanged
DATASET_KEYS = {"bitcoin": ("bitcoin_start", "bitcoin_end")}
PINNED_KEYS = {"bitcoin_start": "2017-01-01", "bitcoin_end": "2026-10-01"}


def _suite_kw(kw: dict) -> dict:
    """Suites / custom components set without `methods`: the methods follow them (else replace() keeps
    the list of the base profile); the same for the baselines and the long methods."""
    kw = dict(kw)
    if any(k in kw for k in SCOPE_KEYS) and "methods" not in kw:
        kw["methods"] = None
    if "long_methods" in kw and "baselines" not in kw:
        kw["baselines"] = None
    return kw


def suite_entries(extra_assemblers=(), extra_joiners=(), smooth_paths="all", joiners=None) -> list[tuple]:
    """The suite on one pool: built-in `STITCH_SUITE` + every custom assembler (suffix = its name) + every
    seam processing (`joiners`: a selection among `JOINERS` and `extra_joiners`; None → all of them) over the
    stitchers `smooth_paths` (suite suffixes or assembler names, "all" → every stitcher except the random path
    and its twin `_NO_JOINER`): <suffix>_<tag> (zseries_xfade, greedy_wsola, …). A custom joiner must be in
    `extra_joiners` (it is registered from there)."""
    out = list(STITCH_SUITE)
    out += [(a, a, None, f"custom assembler {a}") for a in extra_assemblers]
    known = {**JOINERS, **{j: j for j in extra_joiners}}
    if joiners is not None and set(joiners) - set(known):
        raise ValueError(f"joiners {sorted(set(joiners) - set(known))}: not built-in — add them to extra_joiners")
    tags = {j: t for j, t in known.items() if joiners is None or j in joiners}
    plain = [(sfx, a) for sfx, a, j, _ in out if j is None and a not in _NO_JOINER]
    if smooth_paths != "all":
        want = {smooth_paths} if isinstance(smooth_paths, str) else set(smooth_paths or ())
        plain = [(sfx, a) for sfx, a in plain if sfx in want or a in want]
    have = {(a, j) for _, a, j, _ in out}
    for sfx, a in plain:
        out += [(f"{sfx}_{t}", a, j, f"{sfx} + {j}") for j, t in tags.items() if (a, j) not in have]
    return out


def suite_methods(prefix: str, extra_assemblers=(), extra_joiners=(), smooth_paths="all", joiners=None) -> list[str]:
    """Names of the stitching suite on one pool generator: vae → vae_zseries, vae_rand, …"""
    return [f"{prefix}_{sfx}" for sfx, *_ in suite_entries(extra_assemblers, extra_joiners, smooth_paths, joiners)]


def is_disabled(method: str, off, pool_suites=None) -> bool:
    """Is a method switched off by `Config.disabled`: its own name, a suite suffix ("zseries" → <prefix>_zseries and
    its seam-processing variants), or the name of any of its components — assembler ("atsp"), joiner
    ("crossfade"), pool generator ("tsgm_vae") or long-series generator ("chronos")."""
    off = set(off or ())
    if not off:
        return False
    if method in off:
        return True
    from . import registry as R

    if method not in R.methods:
        return False
    s = R.methods.get(method)
    if {s.assembler, s.joiner, s.pool, s.long} & off:
        return True
    sfx_asm = {sfx: a for sfx, a, j, _ in STITCH_SUITE}
    return any(s.assembler == sfx_asm.get(o) for o in off if o in sfx_asm) and s.pool in (pool_suites or {}).values()


_PLUGINS_LOADED: set = set()


def load_plugins(paths) -> None:
    """Import Python files that register custom components (datasets, tasks, pool / long generators,
    assemblers, joiners, models, metrics, tests, hypotheses). A relative path is taken from the
    project folder; each file is imported once per process."""
    import importlib.util
    import sys

    for p in paths or []:
        cands = [Path(p)] if Path(p).is_absolute() else [ROOT / p, Path.cwd() / p]
        cands.append(ROOT / Path(p).name)                     # a config saved on another machine (Colab → Docker)
        f = next((c for c in cands if c.exists()), None)
        if f is None:
            raise FileNotFoundError(f"plugin {p} not found (looked in {', '.join(map(str, cands))})")
        key = str(f.resolve())
        if key in _PLUGINS_LOADED:
            continue
        name = f"marathonts_plugin_{f.stem}"
        spec = importlib.util.spec_from_file_location(name, f)
        mod = importlib.util.module_from_spec(spec)
        sys.modules[name] = mod                               # dataclasses / pickling need the module registered
        try:
            spec.loader.exec_module(mod)
        except BaseException:
            sys.modules.pop(name, None)
            raise
        _PLUGINS_LOADED.add(key)


METHODS = [m for p in POOL_SUITES for m in suite_methods(p, smooth_paths=["zseries"])] + LONG_BASELINES
METHODS_MIN = list(METHODS)
# results published without code (`Config.frozen_methods`): zseries, the proprietary stitching method of zypl.ai
# (under development), and its seam-processing variants;
# methods on a stitcher whose code is not part of the repository are never run (on any pool generator)
UNPUBLISHED_ASSEMBLERS = ("zseries",)
# generators of the main run whose code is not part of the repository: zEDGE (pool generator `zedge_ts`) and
# zEDGE_TS (long-series methods `zedge_ts_long`, `zedge_ts_ar`), proprietary, of zypl.ai; their methods are
# never run, their published results are read from the tables of the run
UNPUBLISHED_GENERATORS = ("zedge_ts", "zedge_ts_long", "zedge_ts_ar")
_UNPUBLISHED_NOTED: set = set()
# False in the analysis (hypotheses.run): it reads the published tables, where the methods without code are kept
# as they are (case-study baselines included), so they are neither filtered nor noted
RUN_CONTEXT = True


def _note_unpublished(methods, frozen, pool_suites) -> None:
    """Say once per set of methods which of them are not run because their code is not in the repository:
    a frozen one keeps its published results, any other one is left out of the run's tables."""
    off = UNPUBLISHED_ASSEMBLERS + UNPUBLISHED_GENERATORS
    hit = [m for m in methods if is_disabled(m, off, pool_suites)]
    key = (tuple(hit), tuple(frozen))
    if not RUN_CONTEXT or not hit or key in _UNPUBLISHED_NOTED:
        return
    _UNPUBLISHED_NOTED.add(key)
    kept, dropped = [m for m in hit if m in frozen], [m for m in hit if m not in frozen]
    if kept:
        print(f"NOTE: {', '.join(kept)}: need code that is not in the repository (zseries, zEDGE, zEDGE_TS: "
              "proprietary, zypl.ai) — not run; their published results are kept (frozen_methods)")
    if dropped:
        print(f"WARNING: {', '.join(dropped)}: need code that is not in the repository (zseries, zEDGE, "
              "zEDGE_TS: proprietary, zypl.ai) — not run and not in frozen_methods, so they are left out of this run")
FROZEN_METHODS = ["vae_zseries", "vae_zseries_xfade", "vae_zseries_wsola", "vae_zseries_quilt"]
CASE_METHOD = "vae_zseries"                                  # the method of the case study (CS1–CS15)
# two independent random stitches of one pool = noise floor; without the twin (min) the margins come from
# the between-seed spread of the random path
NOISE_PAIR = ("vae_rand", "vae_rand_b")
REGIMES = ("R", "S")                             # utility: TRTR (train on real) and TSTR (train on synthetic)


@dataclass
class Config:
    # ── paths (all storage is Parquet) ──
    raw_dir: Path = ROOT / "data" / "raw"
    processed_dir: Path = ROOT / "data" / "processed" / "min"
    artifacts_dir: Path = ROOT / "artifacts" / "min"
    profile_name: str = "min"
    diffusion_ts_dir: Path = ROOT / "external" / "Diffusion-TS"

    # ── scope (registry names) ──
    datasets: list[str] = field(default_factory=lambda: list(DATASETS))
    # pool generators the stitching suite runs on: prefix → pool generator; every entry registers
    # the methods <prefix>_zseries, <prefix>_rand, … (STITCH_SUITE)
    pool_suites: dict = field(default_factory=lambda: dict(POOL_SUITES))
    # custom components (EXTENDING.md): plugin files registering them, loaded with the config — in
    # every notebook, stage subprocess and the hypothesis part
    plugins: list[str] = field(default_factory=list)
    extra_assemblers: list[str] = field(default_factory=list)  # each runs on every pool: <prefix>_<name>
    extra_joiners: list[str] = field(default_factory=list)     # custom seam processing, run like the built-in ones
    # seam processing: which stitchers get it (suite suffixes or assembler names, e.g. ["zseries", "greedy"];
    # "all" → every stitcher except the random path; [] → none) and which joiners (None → every built-in one +
    # extra_joiners). Variants: <prefix>_<stitcher>_<tag> (vae_greedy_xfade). min / mid: ["zseries"]; max: "all"
    smooth_paths: list[str] | str = field(default_factory=lambda: ["zseries"])
    joiners: list[str] | None = None
    # switched off, whatever else selects them: method names, suite suffixes ("zseries", "greedy") or component
    # names (assembler "atsp", joiner "wsola", pool generator, long generator "chronos"); their variants too.
    disabled: list[str] = field(default_factory=list)
    # the noise twin <prefix>_rand_b (a second random path of the same pool, HYPOTHESES.md §2): min — off, the
    # margins come from the between-seed spread of the random path; mid, max — on
    noise_twin: bool = False
    # methods whose results are kept as they are (not run; `collect` carries their rows into the tables where the
    # run has the settings of the results, `tables/frozen.json`): results published without code — the zseries
    # stitcher (`FROZEN_METHODS`)
    frozen_methods: list[str] = field(default_factory=lambda: list(FROZEN_METHODS))
    long_methods: list[str] = field(default_factory=lambda: list(LONG_BASELINES))   # long generators run as methods
    methods: list[str] | None = None                         # None → the suites on every pool + long_methods
    seeds: list[int] = field(default_factory=lambda: list(range(10)))
    pool_generators: list[str] | None = None                # stage `pools`: None → those used by `methods`
    # trained pool generators (VAE) per dataset: 1 → one model shared by all seeds (min: 9 trainings);
    # k → k models, seed s uses model s % k (k · 9 trainings); None → one per seed (mid, max: 90)
    pool_train_replicas: int | None = 1
    case_method: str = CASE_METHOD
    noise_pair: tuple[str, str] = NOISE_PAIR                 # the twin is used only when it is run (not in min)
    # methods left out of the rankings (leaderboard); None → the seam-processing variants unless every
    # stitcher has them (`smooth_paths="all"`); [] → rank every method. The other questions and the case
    # study use every method
    rank_exclude: list[str] | None = None
    leaked: dict = field(default_factory=lambda: {k: list(v) for k, v in LEAKED.items()})   # method → datasets left out of the analysis
    # analysis only: a TSTR cell (task × model × split) a method's series could not train — one class in
    # its labels, no rows, a failed fit — enters as a model that learned nothing (`hypotheses.catalog.
    # impute_failed_utility`: the worse of the chance level and the worst value of the block) instead
    # of being left out, which would rank the method only where it succeeded. False → left out
    utility_fail_penalty: bool = True
    baselines: list[str] | None = None                       # case study: CS9, CS10; None → long_methods
    # ── analysis choices (hypotheses/; never part of a unit fingerprint: changing them reruns only the analysis,
    # notebook 7 / `python -m marathonts.hypotheses.run`; the analysis reads them from the current code, not from the copy
    # saved with the tables — `ANALYSIS_KEYS`). Field names must not start with a prefix of `COMPONENT_KEYS` ──
    # datasets left out of the analysis (rankings, questions, case study); their units stay on disk
    exclude_datasets: list[str] = field(default_factory=list)
    # metrics left out of the analysis: a fidelity metric id (every reference: "F6.1_disc_score"), one reference
    # ("F6.1_disc_score@val", val without suffix: "F6.1_disc_score@val" or the plain id with `fidelity_ref`), a
    # group prefix ending in "." ("F12."), or a utility metric ("ece"; not the primary metric of a task type)
    exclude_metrics: list[str] = field(default_factory=list)
    # core fidelity metrics per criterion (leaderboard core rankings, overall leaderboard, metric values); None → `CORE_METRICS`
    core_metrics: dict | None = None
    # fidelity group → criterion and task type → utility criterion, merged over the built-in maps
    # (`FID_CRITERIA`, `UT_CRITERIA`): a custom group or task type joins a criterion instead of forming its own
    metric_criteria: dict = field(default_factory=dict)
    task_criteria: dict = field(default_factory=dict)
    # task type → primary utility metric, merged over `PRIMARY_METRIC` (a custom task type needs one)
    primary_metrics: dict = field(default_factory=dict)
    # utility metric → orientation (+1 higher is better, −1 lower is better), merged over the built-in metrics:
    # a custom utility metric is analysed only with an orientation
    metric_orient: dict = field(default_factory=dict)
    # memorisation flag of the overall leaderboard: near-copy share of a method ≥ this × that of the real OOT piece
    # (and significantly larger); reported next to the rank, never part of it
    near_copy_ratio: float = 2.0

    # ── data ──
    max_points: int | None = 10_000                         # last N hourly points of every dataset
    split: tuple[float, float, float] = (0.5, 0.25, 0.25)   # train / val / oot (5000 / 2500 / 2500)
    embargo: int = 168                                       # rows dropped between splits
    max_gap_interp: int = 6                                  # hours; longer gaps stay NaN
    bitcoin_start: str = "2017-01-01"
    bitcoin_end: str = "2026-10-01"                          # fixed end: the Kaggle file grows daily

    # ── windows (BENCHMARK.md, Protocol: data) ──
    T: int = 168
    max_windows: int = 5000
    holdout_frac: float = 0.10
    pool_size: int = 300                                     # N = max(pool_size, pool_mult · K) windows in the pool
    pool_mult: int = 2

    # ── VAE (BENCHMARK.md, Protocol: pool generator) ──
    vae_latent: int = 16
    vae_beta: float = 2.0
    vae_epochs: int = 400
    vae_patience: int = 50
    vae_min_epochs: int = 150                                # no stopping / best-weight pick before this epoch
    vae_noise: float = 0.5
    vae_batch: int = 64

    # ── case study and seam metrics ──
    edge_overlap: int = 5                                    # F5.7: width of the seam detector's window (at least 6 points)
    stitch_task: str = "clf_up_h24_q90"                      # task of the case-study cells (CS7, CS10, CS12, CS13)

    # ── alternative stitchers (BASELINES.md A); seam cost of greedy / atsp / pctsp: the jump at the seam ──
    pctsp_solutions: int = 2000                              # vae_pctsp: OR-Tools search stops after this many solutions
    pctsp_time_s: float = 60.0                               # … or this time per unit (a cap: set it so it is rarely hit)
    mbb_bandwidth: float = 1.0                               # vae_mbb: Gaussian kernel, h = this × median jump
    knn_k: int | None = None                                 # vae_knn: neighbours; None → round(√N) (Lall & Sharma)
    quilt_tol: float = 0.1                                   # vae_quilting: candidates within (1 + tol) × best overlap error
    herding_stride: int = 4                                  # vae_herding: every k-th point of a window as features

    # ── seam processing (BASELINES.md B) ──
    join_overlap: int = 12                                   # points two neighbouring windows overlap
    join_wsola_shift: int = 12                               # WSOLA: max shift of the next window

    # ── Diffusion-TS (repo Config/etth.yaml, adapted to T) ──
    dts_d_model: int = 64
    dts_enc_layers: int = 3
    dts_dec_layers: int = 2
    dts_heads: int = 4
    dts_timesteps: int = 500
    dts_sampling_steps: int = 50                             # DDIM steps for infill
    # training as the official Config/etth.yaml + engine/solver.py: 18 000 optimiser steps, batch 128 with
    # gradient accumulation 2, Adam(β = 0.9, 0.96) from base_lr 1e-5, linear warm-up to 8e-4 over 500 steps,
    # then ReduceLROnPlateau on the training loss (×0.5, patience 4000, min 1e-5, threshold 0.1 rel), EMA 0.995
    # every 10 steps as ema-pytorch 0.2.1 (copy for the first 100 steps, decay warm-up). Added for the
    # benchmark: early stopping on the holdout loss of the EMA model, as for the VAE
    dts_steps: int = 18000
    dts_batch: int = 128
    dts_grad_accum: int = 2
    dts_lr: float = 1e-5
    dts_warmup_lr: float = 8e-4
    dts_warmup: int = 500
    dts_lr_factor: float = 0.5
    dts_lr_patience: int = 4000
    dts_min_lr: float = 1e-5
    dts_lr_threshold: float = 0.1
    dts_ema_decay: float = 0.995
    dts_ema_every: int = 10
    dts_ema_after: int = 100
    dts_eval_every: int = 500
    dts_patience_evals: int = 8                              # early stop on holdout loss (as VAE)
    dts_context_frac: float = 0.5                            # AR step keeps this share of the window as context
    dts_infill_coef: float = 1e-2
    dts_infill_lr: float = 5e-2
    dts_train_per_seed: bool = False                         # min / mid: models per dataset (below), seeds vary sampling; max: per seed
    # without dts_train_per_seed: Diffusion-TS models per dataset, seed s uses model s % k (trained with seed r),
    # as `pool_train_replicas` for the VAE; 1 — one model per dataset. Not a `dts_` field: it enters the
    # fingerprints only when > 1 (with one model per dataset the fingerprints do not contain it)
    diffusion_train_replicas: int = 1

    # ── Chronos ──
    chronos_model: str = "amazon/chronos-t5-small"
    chronos_context: int = 512
    chronos_chunk: int = 64

    # ── TimesFM 3.0 / Timestral: zero-shot, package defaults, median point forecast, revisions pinned ──
    timesfm_model: str = "google/timesfm-3.0-pytorch"
    timesfm_revision: str | None = "43046b85ec22d584a13f8098c2ed39c889e129c2"
    timestral_model: str = "mistralai/Timestral-209M"
    timestral_revision: str | None = "9874d252ab0aae16f7f7c999f98f98d6ad7d8365"

    # ── utility (METRICS U1–U3); regimes are fixed: R (TRTR) and S (TSTR), see REGIMES ──
    tasks: list[str] | None = None                           # None → every registered task
    models: list[str] = field(default_factory=lambda: ["linear", "gbdt", "mlp"])
    # models restricted to some tasks (others: every task they support); MLP only on clf_up_h24_q90
    model_tasks: dict = field(default_factory=lambda: {"mlp": ["clf_up_h24_q90"]})
    # exogenous target parameters per dataset and task (thresholds in real units), read — never fitted
    target_params_file: Path = PKG / "target_params.json"
    test_splits: list[str] = field(default_factory=lambda: ["val", "oot"])
    # hyperparameters of every ML model: fixed values and, for the search, grids (MODELS.md)
    model_configs_file: Path = PKG / "model_configs.json"
    hpo: bool = False                                        # hyperparameter search per fit (grid, tail of the regime's own data)
    hpo_val_frac: float = 0.2                                # share of the training data (its tail; real train for TRTR, the series for TSTR) used to choose
    decision_transfer: bool = False                          # U6.1 / U6.4 grid → RQ5 (c)
    grid_methods: list[str] | str | None = None              # RQ5 (c) grid methods; None → the case-study method, noise_pair[0]; "all" → every method
    model_grid_task: str = "clf_up_h24_q90"                  # RQ5 (c) task

    # ── fidelity ──
    fidelity_ref: str = "val"                                # primary real reference for fidelity (no suffix)
    fidelity_extra_refs: list[str] = field(default_factory=lambda: ["train", "oot"])  # also scored as `@<part>`
    fidelity_groups: list[str] | None = None                 # None → every registered metric group
    disc_epochs: int = 30                                    # post-hoc GRU discriminator (F6.1)

    # ── artifacts ──
    save_generator_weights: bool = True
    save_model_weights: bool = True                          # utility predictions are always written (the hypothesis part needs them)
    weights_dtype: str = "float32"                           # "float16" halves weight files

    # ── statistics ──
    alpha: float = 0.05
    n_boot: int = 2000
    boot_block: int = 168                                    # test-row block for bootstrap (1 week)
    equivalence_margin_q: float = 0.5                        # SESOI = median |single-run noise| (HYPOTHESES §2)
    # supplementary sensitivity of the noise margin (HYPOTHESES §8), not pre-specified: how the between-seed
    # differences are formed — "neighbours" (seed k vs k+1, the pre-specified one), "pairs" (every pair of seeds)
    # or "perm:<n>" (neighbours after a random reordering of the seeds with seed n) — and a factor on the margin
    noise_estimator: str = "neighbours"
    noise_scale: float = 1.0
    # supplementary: the statistic of the global bootstrap interval over datasets — "mean" (pre-specified) or
    # "median" (the statistic of the reported effect)
    ci_stat: str = "mean"
    # supplementary: the value of a utility cell the series could not train — "worst" (the pre-specified rule:
    # the worse of the chance level and the worst value of the block) or "chance" (the chance level only)
    utility_fail_rule: str = "worst"

    device: str | None = None                                # None → CUDA if available, else CPU
    extra: dict = field(default_factory=dict)                # params of custom components, by name

    def __post_init__(self):
        load_plugins(self.plugins)                            # custom components first: the suites may use them
        ea, ej = list(self.extra_assemblers), list(self.extra_joiners)
        from .methods import register_long_method, register_stitch_suite

        for prefix, pool in self.pool_suites.items():         # idempotent: every variant is registered once
            register_stitch_suite(prefix, pool, extra_assemblers=ea, extra_joiners=ej)
        for name in self.long_methods:
            register_long_method(name)
        if self.methods is None:
            self.methods = [m for p in self.pool_suites
                            for m in suite_methods(p, ea, ej, self.smooth_paths, self.joiners)] + list(self.long_methods)
        if self.baselines is None:
            self.baselines = list(self.long_methods)
        _note_unpublished([m for m in self.methods if not is_disabled(
                              m, list(self.disabled) + ([] if self.noise_twin else ["rand_b"]), self.pool_suites)]
                          + [m for m in self.frozen_methods if m not in self.methods], self.frozen_methods,
                          self.pool_suites)
        off = (list(self.disabled) + list(self.frozen_methods) + list(UNPUBLISHED_ASSEMBLERS)
               + (list(UNPUBLISHED_GENERATORS) if RUN_CONTEXT else []) + ([] if self.noise_twin else ["rand_b"]))
        self.methods = [m for m in self.methods if not is_disabled(m, off, self.pool_suites)]
        self.baselines = [m for m in self.baselines if not is_disabled(m, off, self.pool_suites)]

    @property
    def smooth_everywhere(self) -> bool:
        """Every stitcher (but the random path) has every seam processing: the variants are ranked."""
        return self.smooth_paths == "all"

    @property
    def runs_dir(self) -> Path:                              # alias of artifacts_dir
        return self.artifacts_dir

    @classmethod
    def quick(cls, **kw) -> "Config":
        c = cls(
            datasets=["ett", "bike"], seeds=[0, 1], vae_epochs=5, vae_patience=3, vae_min_epochs=1,
            dts_steps=60, dts_eval_every=30, dts_sampling_steps=5, dts_timesteps=50, dts_d_model=32,
            dts_enc_layers=1, dts_dec_layers=1, chronos_model="amazon/chronos-t5-tiny",
            timestral_model="mistralai/Timestral-5M", timestral_revision=None,
            n_boot=200, pool_size=80, pctsp_time_s=2.0,
            disc_epochs=3, max_windows=800,
            extra={"mlp": {"epochs": 3}, "gbdt": {"n_estimators": 30}, "sk_hgb": {"n_estimators": 30}},
            processed_dir=ROOT / "data" / "processed" / "quick",
            artifacts_dir=ROOT / "artifacts" / "quick", profile_name="quick",
        )
        return dataclasses.replace(c, **_suite_kw(kw))

    @classmethod
    def profile(cls, name: str = "min", **kw) -> "Config":
        """`min` (Colab run), `mid` (min + the VAE per seed) or `max` (everything on); see the module docstring."""
        if name == "min":
            c = cls()
        elif name == "mid":
            # min + the VAE retrained on every seed (independent seeds); same data as min. Diffusion-TS: one
            # model per dataset as in min (about 1.6 GPU-hours per training on an L4)
            c = cls(profile_name="mid", pool_train_replicas=None, noise_twin=True,    # + the noise twin
                    artifacts_dir=ROOT / "artifacts" / "mid")       # data shared with min (same settings)
        elif name == "max":
            c = cls(
                profile_name="max", processed_dir=ROOT / "data" / "processed" / "max",
                smooth_paths="all",                               # every seam processing over every stitcher
                noise_twin=True,                                  # + the noise twin
                # thresholds from max's own train: min's train lies in max's val / OOT
                target_params_file=PKG / "target_params_max.json",
                artifacts_dir=ROOT / "artifacts" / "max",
                max_points=None, split=(0.6, 0.2, 0.2),
                hpo=True, decision_transfer=True,
                model_tasks={},                                   # every model on every task it supports
                grid_methods="all",                               # RQ5 (c) grid for every method (custom ones too)
                dts_train_per_seed=True,                          # Diffusion-TS retrained on every seed
                chronos_model="amazon/chronos-t5-base",           # ~200M, the size of TimesFM 3.0 and Timestral-209M
                pool_train_replicas=None,                         # VAE retrained on every seed
                extra={"mlp": {"epochs": 200, "early_stopping_patience": 10},
                       # the full boosting configuration (min / mid use the light one in model_configs.json)
                       "gbdt": {"n_estimators": 200, "max_depth": 6, "learning_rate": 0.1, "max_bin": 256,
                                "device": "auto", "multi_strategy_ms": "one_output_per_tree"}},
            )
        else:
            raise KeyError(f"unknown profile {name!r}: min | mid | max")
        return dataclasses.replace(c, **_suite_kw(kw))

    def params(self, name: str) -> dict:
        """Parameters of the component `name` (`extra[name]`), a copy; {} if none are set."""
        return dict(self.extra.get(name, {}))

    def device_str(self) -> str:
        """torch device; "cpu" in an environment without torch (e.g. the tsgm env — TensorFlow
        picks its own device there)."""
        if self.device:
            return self.device
        try:
            import torch
        except ImportError:
            return "cpu"
        return "cuda" if torch.cuda.is_available() else "cpu"

    def to_json(self) -> str:
        """Every field as JSON (paths as strings): the file `--config` reads and `collect` saves with the tables."""
        d = dataclasses.asdict(self)
        return json.dumps({k: str(v) if isinstance(v, Path) else v for k, v in d.items()}, indent=2, default=str)

    @classmethod
    def from_json(cls, text: str) -> "Config":
        """Inverse of `to_json` (used to hand the whole config to another environment)."""
        d = json.loads(text)
        fields = {f.name: f for f in dataclasses.fields(cls)}
        out = {}
        for k, v in d.items():
            if k not in fields:
                continue
            if k.endswith(("_dir", "_file")) and v is not None:
                v = Path(v)
                if k.endswith("_file") and not v.is_absolute() and not v.exists() and (PKG / v.name).exists():
                    v = PKG / v.name               # a package file saved as bench/<name> (before the marathonts package)
            elif isinstance(v, list) and k in ("split", "noise_pair"):
                v = tuple(v)
            out[k] = v
        return cls(**out)

    # knobs that change what a unit produces; resumed units must have been made with the same values
    FINGERPRINT_EXCLUDE = ("datasets", "methods", "pool_suites", "plugins", "extra_assemblers", "extra_joiners",
                           "long_methods", "seeds", "pool_generators", "raw_dir", "processed_dir",
                           "profile_name",
                           "artifacts_dir", "diffusion_ts_dir", "target_params_file", "model_configs_file",
                           "device", "alpha", "n_boot", "boot_block",
                           "equivalence_margin_q", "case_method", "noise_pair", "baselines",
                           "smooth_paths", "joiners", "rank_exclude", "disabled", "noise_twin", "frozen_methods", "leaked",
                           "utility_fail_penalty", "exclude_datasets", "exclude_metrics", "core_metrics",
                           "metric_criteria", "task_criteria", "primary_metrics", "metric_orient", "near_copy_ratio",
                           "noise_estimator", "noise_scale", "ci_stat", "utility_fail_rule")
    # analysis-only settings: the analysis takes them from the current code / profile (`hypotheses.run._run_config`)
    ANALYSIS_KEYS = ("leaked", "rank_exclude", "utility_fail_penalty", "exclude_datasets", "exclude_metrics",
                     "core_metrics", "metric_criteria", "task_criteria", "primary_metrics", "metric_orient",
                     "near_copy_ratio", "noise_estimator", "noise_scale", "ci_stat", "utility_fail_rule")

    # settings that define the processed data: the split (→ exogenous thresholds) and the window
    # length T (→ K, the series length). The training windows (`max_windows`, `holdout_frac`) and the
    # pool size (`pool_size`, `pool_mult`) are not part of it: they are derived at use
    # (`data.window_layout`) and enter only the fingerprints of what depends on them — changing the
    # pool size resamples the pools and redoes the pool-based methods, nothing else.
    SPLIT_KEYS = ("max_points", "split", "embargo", "max_gap_interp", "bitcoin_start", "bitcoin_end")
    DATA_KEYS = SPLIT_KEYS + ("T",)
    # settings of each built-in component (field names or prefixes); any component also gets
    # extra[<its name>]. A resumed unit is reused only if the settings of its own components match.
    COMPONENT_KEYS = {
        "windows": ("max_windows", "holdout_frac"),           # training windows of generators (train_windows)
        "pool_size": ("pool_size", "pool_mult"),              # how many windows a pool holds
        # a generator's training settings (its trained model) and, separately, those only its sampling uses
        "tsgm_vae": ("vae_latent", "vae_beta", "vae_epochs", "vae_patience", "vae_min_epochs", "vae_batch"),
        "tsgm_vae:sample": ("vae_noise",),
        "pool_train": ("pool_train_replicas",),
        "diffusion_ts": ("dts_",),                            # the series: every Diffusion-TS setting
        "diffusion_ts:train": ("dts_d_model", "dts_enc_layers", "dts_dec_layers", "dts_heads", "dts_timesteps",
                               "dts_steps", "dts_batch", "dts_lr", "dts_eval_every", "dts_patience_evals",
                               "dts_grad_accum", "dts_warmup_lr", "dts_warmup", "dts_lr_factor", "dts_lr_patience",
                               "dts_min_lr", "dts_lr_threshold", "dts_ema_decay", "dts_ema_every", "dts_ema_after"),
        "chronos": ("chronos_",), "timesfm": ("timesfm_",), "timestral": ("timestral_",),
        "greedy": (), "atsp": (),
        "pctsp": ("pctsp_",), "mbb": ("mbb_",), "knn": ("knn_",), "quilt_sel": ("quilt_tol", "join_overlap"),
        "herding": ("herding_",),
        "crossfade": ("join_overlap",), "wsola": ("join_",), "quilt": ("join_overlap",),
    }

    @staticmethod
    def _hash(d) -> str:
        import hashlib

        return hashlib.sha1(json.dumps(d, sort_keys=True, default=str).encode()).hexdigest()[:12]

    def _key_values(self, keys, dataset: str | None) -> dict:
        """Values of the data settings `keys` as dataset `dataset` sees them: the settings of another dataset
        (`DATASET_KEYS`) at their pinned values (`PINNED_KEYS`); `dataset` None — every setting as set."""
        own = set(DATASET_KEYS.get(dataset, ()))
        return {k: (PINNED_KEYS[k] if dataset is not None and k in PINNED_KEYS and k not in own else getattr(self, k))
                for k in keys}

    def split_key(self, dataset: str | None = None) -> str:
        return self._hash(self._key_values(self.SPLIT_KEYS, dataset))

    def data_key(self, dataset: str | None = None) -> str:
        return self._hash(self._key_values(self.DATA_KEYS, dataset))

    def unit_fingerprint(self, *components: str, upstream=(), files=(), dataset: str | None = None) -> str:
        """Hash of what one unit of work depends on: the processed data, the settings of the given
        components, fingerprints of the units it reads (`upstream`) and the contents of the exogenous
        files ("targets", "models"). Stored in the unit's record; a mismatch means "redo". With `dataset`, the
        thresholds file counts with the built-in datasets and that dataset only: the thresholds an added dataset
        brings do not redo the units of the others."""
        full = {k: v for k, v in json.loads(self.to_json()).items() if not k.endswith(("_dir", "_file"))}
        d: dict = {"data": self.data_key(dataset), "upstream": list(upstream)}
        for c in components:
            pref = self.COMPONENT_KEYS.get(c, ())
            if pref:
                d.update({k: v for k, v in full.items() if k.startswith(pref)})
            d[f"extra:{c}"] = self.extra.get(c)
        # "every registered …" is hashed as the resolved list: a task / metric group added by a plugin redoes the units
        if "tasks" in d and d["tasks"] is None:
            from . import registry as R

            R.load_builtins()
            d["tasks"] = R.tasks.names()
        if "fidelity_groups" in d and d["fidelity_groups"] is None:
            from . import registry as R

            R.load_builtins()
            d["fidelity_groups"] = R.fidelity_metrics.names()
        paths = {"targets": self.target_params_file, "models": self.model_configs_file}
        for f in files:
            fp = Path(paths[f])
            if not fp.exists():
                d[f"file:{f}"] = None
                continue
            try:                                             # parsed: reformatting the file changes nothing
                d[f"file:{f}"] = json.loads(fp.read_text())
            except ValueError:
                d[f"file:{f}"] = fp.read_text()
                continue
            if f == "targets" and dataset is not None and isinstance(d[f"file:{f}"], dict):
                # a unit depends on the thresholds of its own dataset only. The thresholds of the other built-in
                # datasets enter at their pinned values (`<file>.pinned.json`, a frozen copy — never edit it):
                # changed thresholds of one dataset redo that dataset only, the fingerprints of the others stay
                keep = set(DATASETS) | {dataset}
                pin = fp.with_name(fp.stem + ".pinned.json")
                pin = json.loads(pin.read_text()) if pin.exists() else {}
                cur = d[f"file:{f}"]
                t = {k: (pin[k] if k != dataset and k in pin else v) for k, v in cur.items() if k in keep}
                if isinstance(cur.get("_split_key"), dict):
                    ps = pin.get("_split_key", {})
                    t["_split_key"] = {k: (ps[k] if k != dataset and k in ps else v)
                                       for k, v in cur["_split_key"].items() if k in keep}
                d[f"file:{f}"] = t
        return self._hash(d)

    def fingerprint(self) -> str:
        """Short hash of the settings that determine the artifacts (scope and paths excluded)."""
        import hashlib

        d = {k: v for k, v in json.loads(self.to_json()).items() if k not in self.FINGERPRINT_EXCLUDE}
        # the contents of the exogenous files count too: changing a model or target configuration
        # changes what a unit produces
        for f in (self.model_configs_file, self.target_params_file):
            d[f"file:{Path(f).name}"] = Path(f).read_text() if Path(f).exists() else None
        return hashlib.sha1(json.dumps(d, sort_keys=True).encode()).hexdigest()[:12]
