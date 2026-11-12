# How to extend the benchmark

Every part of the benchmark is registered by name in a registry (`marathonts/bench/registry.py`) and selected in the
configuration by that name. Your own components are written in a separate Python file — a plugin — and are
switched on without editing the benchmark code or the notebooks: a class or function in the plugin and a line in
the configuration ([CONFIGURATION.md](CONFIGURATION.md)).

Each recipe below follows the same steps: what the component is, the minimal plugin code, how to switch it on,
which stages to run, and where the result appears.

| Component | Registry / function | Interface | Switched on by |
|---|---|---|---|
| [Dataset](#dataset) | `register_parquet_dataset`, `registry.datasets` | `load(cfg) -> pd.Series` (hourly) | `datasets` |
| [Task](#task) | `register_task(Task(...))` | `fit(train) -> params`, `labels(values, params) -> y` | registered = on (`tasks=None`) |
| [Pool generator](#pool-generator) | `registry.pool_generators` | `fit(ctx)`, `sample(n, ctx)`, `state()`, `load_state(arrays, ctx)` | `pool_suites` |
| [Long-series generator](#long-series-generator) | `registry.long_generators` | `fit(ctx)`, `generate(ctx) -> (values, how, seams)` | `long_methods` |
| [Assembler](#assembler) | `registry.assemblers` | `assemble(pool, ctx) -> (path, info)` | `extra_assemblers` |
| [Seam processing](#seam-processing) | `registry.joiners` | `windows_needed(K, T, cfg)`, `join(W, L, cfg) -> (X, seams, src, info)` | `extra_joiners`, `smooth_paths` |
| [Single method](#single-method) | `bench.methods.register_method` | pool + assembler (+ seam processing), or long-series generator | `methods` |
| [ML model](#ml-model) | `registry.models` | `fit`, `predict`, `state`, `load_state`, `kinds` | `models` |
| [Fidelity metric](#fidelity-metric) | `bench.fidelity.register_fidelity_group` | `fn(ctx) -> {metric: value}` + orientation | registered = on (`fidelity_groups=None`) |
| [Utility metric](#utility-metric) | `registry.utility_metrics` | `fn(y, pred, ctx) -> dict` | registered = on; orientation in `metric_orient` |
| [Statistical test](#statistical-test) | `hypotheses.stats.register_test` | `fn(z) -> dict` or `fn(d, margin) -> dict` | registered = on |
| [Hypothesis](#hypothesis) | `hypotheses.catalog.register_hypothesis` | `fn(tables, cfg) -> {"global", "per_dataset", "extra"}` | registered = on |

## Plugin files

A plugin is any Python file that imports the benchmark and registers components; one file can hold several.
Plugins are loaded in every process that needs them:

- **`Config.plugins`** — a list of files. They are imported when the configuration is created
  (`Config.__post_init__`), so they reach every stage, the stage subprocesses of the notebooks (`run_in_env`
  passes the whole configuration) and the analysis (`collect` records the list in `tables/config.json`, and
  `hypotheses.run` reads it from there). A relative path is looked up in the project folder, then in the working
  directory; each file is imported once per process.
- **`--plugins FILE …`** — on `python -m marathonts.bench.run` the files are loaded before the configuration and added to
  `Config.plugins`; on `python -m marathonts.hypotheses.run` they add tests and hypotheses to the analysis.
- **Notebooks** — `plugins=["my_plugins.py"]` in the scope cell of notebooks 01–06 (the file lies in the
  project folder on Drive). Notebook 07 loads the plugins recorded with the tables; a file with only tests or
  hypotheses is added as `main([..., "--plugins", "my_tests.py"])`. Re-running the setup cell re-imports an
  edited plugin.
- **Docker** — the images contain only the package `marathonts/`; the file is mounted into `/app`:

```bash
docker compose run --rm -v "$PWD/my_plugins.py:/app/my_plugins.py" bench all --plugins my_plugins.py
docker compose run --rm -v "$PWD/my_plugins.py:/app/my_plugins.py" hypotheses
```

A name that is already registered raises `KeyError` unless the component is registered with `overwrite=True`.
Parameters of your components are set in `extra={"<component name>": {...}}` and arrive as `ctx.params`
(generators, assemblers, fidelity groups), `cfg.params("<name>")` (seam processing) or `self.params` (models).

The configuration lines of all recipes together, in the notebook form:

```python
cfg = dataclasses.replace(
    cfg,
    methods=None, baselines=None,                       # methods and baselines are rebuilt from the lines below
    plugins=["my_plugins.py"],                          # path from the project folder
    datasets=[*cfg.datasets, "my_sales"],               # dataset
    pool_suites={"vae": "tsgm_vae", "gan": "my_gan"},   # pool generator: the assembly suite on it
    extra_assemblers=["my_greedy"],                     # assembler on every pool: vae_my_greedy, gan_my_greedy
    extra_joiners=["my_blend"],                         # seam processing, run like the built-in ones
    smooth_paths=["greedy", "my_greedy"],               # assemblers that get seam processing
    long_methods=[*cfg.long_methods, "seasonal_boot"],  # long-series generator: method and baseline
    models=[*cfg.models, "my_trees"],                   # ML model
    extra={**cfg.extra, "my_greedy": {"start": 0}},     # parameters of your components
)
```

## Dataset

**What it is.** Any series with a time and a value, brought to an hourly step with an "hour of week" calendar.
The `prepare` stage splits it into train / val / OOT, scales it and derives the window count K and the pool size N
from its length; the window length T is common to all datasets.

**Plugin.** From a Parquet or CSV file with a time column and a value column (`agg`: `mean`, `sum` or `last`
per hour; the path is resolved against the working directory):

```python
from marathonts.bench.datasets import register_parquet_dataset

register_parquet_dataset("my_sales", "data/raw/my_sales/sales.parquet",
                         time_col="ts", value_col="units", agg="sum")
```

Any other source through `DatasetSpec` and a `load(cfg)` that returns an hourly `pd.Series` with a
`DatetimeIndex` (NaN where unknown):

```python
import numpy as np
import pandas as pd
from marathonts.bench import registry as R
from marathonts.bench.datasets import DatasetSpec, hourly

def load(cfg):
    df = pd.read_csv("data/raw/my_prices/prices.csv", parse_dates=["time"])
    return np.log(hourly(df.set_index("time")["price"], "last"))

R.datasets.register("my_prices", DatasetSpec(load, "log price, hourly"))
```

**Switch on.** `datasets=[*cfg.datasets, "my_sales"]` in the configuration, or `--datasets ett my_sales` on the
command line.

**Stages.** `prepare`, then `pools` … `collect` and the analysis. The `raw` stage skips a dataset without
`raw_files`. The first `prepare` proposes the dataset's task thresholds by the tasks' rules on its train split and
writes them to `Config.target_params_file` (the log says so); review and commit the file so that later runs
read the same thresholds. The thresholds of an added dataset enter only its own fingerprints: nothing is redone on
the other datasets.

**Check.** `tables/datasets.parquet` lists n, K, N and the period of the dataset; its rows appear in every table
and report. A series too short for the window length (train under 4·T points, val or OOT under 2·T + `embargo`)
is rejected with a message; gaps longer than `max_gap_interp` stay missing.

## Task

**What it is.** A utility task turns a series in real units into labels: `fit(train) -> params` (thresholds,
computed on train only) and `labels(values, params) -> y` (NaN where the future is unknown). `kind` determines the
models and metrics: `clf` (binary), `mc` (multiclass, labels `0..n_classes−1`), `reg`, `qreg` (quantiles
0.1 / 0.5 / 0.9), `ms` (vector of `h` values), `vol`.

**Plugin.**

```python
import numpy as np
from marathonts.bench.tasks import Task, register_task

def fit(v):                                          # train only
    d = v[12:] - v[:-12]
    return {"thr": float(np.nanquantile(np.abs(d), 0.95))}

def labels(v, p):
    y = np.full(len(v), np.nan)
    d = v[12:] - v[:-12]
    y[:-12] = (np.abs(d) > p["thr"]).astype(float)
    y[:-12][np.isnan(d)] = np.nan
    return y

register_task(Task("spike_h12", "clf", h=12, fit=fit, labels=labels))
```

**Switch on.** With `tasks=None` (default) every registered task runs; `tasks=[...]` selects a subset. A task
becomes the task of the case-study cells (CS7, CS10, CS12, CS13) and of F8 with `stitch_task="spike_h12"`, or for
the analysis only with `--case-task spike_h12`.

**Stages.** The parameters returned by `fit` are exogenous: they are read from `marathonts/bench/target_params.json`
(`{dataset: {task: {parameter: value}}}`), not computed during a run. `prepare` proposes the missing ones by the
`fit` rule on train and writes them; `python -m marathonts.bench.run targets --plugins my_plugins.py` does the same on its
own. Review and commit the file; tasks without parameters (such as regression) need no entry. Then `utility`
computes only the added task's cells in the existing units; `fidelity` recomputes the group F11 (class balance over
the classification tasks of the run); then `collect` and the analysis.

**Check.** Rows with `task == "spike_h12"` in `tables/utility.parquet`, the task in `METRIC_VALUES.md` and in the
utility criteria of the rankings.

A task of a `kind` other than the built-in ones also needs, for the analysis, a primary metric
(`primary_metrics`) and a utility criterion (`task_criteria`, else it forms its own, which the four rankings do not
include) ([CONFIGURATION.md](CONFIGURATION.md#analysis-only-settings)); for the hyperparameter search (`hpo`) a
selection metric `Task(..., select_by=("metric", higher_is_better))` (else the search is skipped and the fixed
parameters are used); for the case study's row-level tests `Task(..., row_loss=fn)` with
`fn(y, pred, scale) -> (n,)` (else its rows are left out of them). Its utility metrics come from a
[utility metric](#utility-metric) for that kind, its models from those that list the kind in `kinds`.

## Pool generator

**What it is.** A generator of short windows. It is trained on the train windows and samples a pool of N windows
`(N, T, 3)`, float32 in the benchmark channels: the value (min-max over train, `ctx.lo` / `ctx.hi`) and
`(sin + 1) / 2`, `(cos + 1) / 2` of the hour of week. Training windows are `ctx.X_core`, early-stopping windows
`ctx.X_hold`, the whole train `ctx.X_train`; `ctx.seed`, `ctx.device`, `ctx.N`, `ctx.K`, `ctx.T` and
`ctx.params` are available. Every assembler of the suite then takes the same pool.

**Plugin.**

```python
import numpy as np
from marathonts.bench import registry as R
from marathonts.bench.generators.base import PoolGenerator
from marathonts.bench.storage import torch_state

@R.pool_generators.register("my_gan")
class MyGAN(PoolGenerator):
    env = "mygan"                                    # envs/mygan.txt; "core" (default) = the main environment
    requires = ("my_gan_lib",)                       # modules checked before training

    def fit(self, ctx):
        from my_gan_lib import train_gan
        self.net = train_gan(ctx.X_core, ctx.X_hold, epochs=ctx.params.get("epochs", 100),
                             device=ctx.device, seed=ctx.seed)
        self.info["epochs_run"] = self.net.epochs_run    # goes into the pool record

    def sample(self, n, ctx):
        return self.net.sample(n)                    # (n, T, 3), values in [0, 1]

    def state(self):                                 # weights → artifacts/<profile>/generators/…parquet
        return torch_state(self.net)

    def load_state(self, arrays, ctx):               # back, without training
        from my_gan_lib import build_gan
        self.net = build_gan(ctx).load_from(arrays)
        return self
```

`state()` returns a dict of numpy arrays; anything picklable can be stored with `bench.storage.blob(obj)` and
restored with `unblob`. Without `load_state` a stored generator cannot be reused and is trained again. Adapters to
use as examples are in `marathonts/bench/generators/builtin.py`: `tsgm_vae` (tsgm), `sdv_par` (SDV PARSynthesizer),
`real_windows`.

**Switch on.** `pool_suites={"vae": "tsgm_vae", "gan": "my_gan"}` with `methods=None`. The whole assembly suite
runs on the new pool: `gan_rand`, `gan_greedy`, `gan_atsp`, `gan_pctsp`, `gan_mbb`, `gan_knn`, `gan_quilting`,
`gan_herding`, plus `gan_rand_b` with `noise_twin=True`, every custom assembler, and seam processing over the
assemblers of `smooth_paths`. The assembler `zseries` has published results only and is not run on any pool, so
`smooth_paths` names the assemblers that get seam processing on the new pool (e.g. `["greedy"]`).

**Stages.** `pools --pool-generators my_gan` in the generator's environment
(`python -m marathonts.bench.run pools --pool-generators my_gan --plugins my_plugins.py`; Colab:
`run_in_env("mygan", "pools", "--pool-generators", "my_gan", config=cfg)` in notebook 02). Without its modules,
the other stages skip it and name `envs/mygan.txt`. A generator of the main environment is also trained by
`generate` when its pool is missing. Then `generate` … `collect` and the analysis.

**Check.** `tables/pools.parquet` (rows with `pool_generator == "my_gan"`: training and sampling time,
`self.info`), the methods `gan_*` in every table and ranking (RQ1 includes the methods of all suites). The case
study of a method on the new pool: `python -m marathonts.hypotheses.run --case-method gan_greedy --noise-pair gan_rand gan_rand_b`.

## Long-series generator

**What it is.** A generator that produces the whole series of length `ctx.L = K·T` itself: values in real units,
hour of week per point, and seam positions (indices where a newly generated piece starts; empty if none). It runs
as a method under its own name and is a baseline of the case study.

**Plugin.** A runnable example: a seasonal block bootstrap of the train series (weeks drawn at random).

```python
import numpy as np
from marathonts.bench import registry as R
from marathonts.bench.generators.base import LongGenerator

@R.long_generators.register("seasonal_boot")
class SeasonalBoot(LongGenerator):
    # env = "myenv"; requires = ("my_lib",)          # own environment, as for a pool generator
    # uses_windows = True                            # if it trains on ctx.X_core / ctx.X_hold

    def fit(self, ctx):                              # optional; timed as fit
        v, how = ctx.train_series()                  # real train: values, hour of week
        self.v = v[~np.isnan(v)]

    def generate(self, ctx):
        rng = np.random.default_rng(ctx.seed)
        n_weeks = len(self.v) // 168
        starts = rng.integers(0, n_weeks, size=ctx.L // 168 + 1) * 168
        values = np.concatenate([self.v[s:s + 168] for s in starts])[:ctx.L]
        how = (ctx.train_series()[1][-1] + 1 + np.arange(ctx.L)) % 168
        seams = np.arange(168, ctx.L, 168)           # a new block starts every week
        return values, how, seams
```

`state()` / `load_state(arrays, ctx)` store and restore trained weights as for a pool generator. Diffusion-TS,
Chronos, TimesFM and Timestral in `marathonts/bench/generators/builtin.py` are examples of trained and pretrained
generators.

**Switch on.** `long_methods=[*cfg.long_methods, "seasonal_boot"]` with `methods=None, baselines=None` in the
notebook cell (with `Config.profile(...)` the lists are rebuilt automatically). It becomes the method
`seasonal_boot` and a baseline.

**Stages.** `generate` (in its environment if it has one: `generate --methods seasonal_boot`), `fidelity`,
`utility`, `collect`, the analysis. Other methods are not redone.

**Check.** Rows with `method == "seasonal_boot"` in `tables/timing.parquet`, `fidelity.parquet`,
`utility.parquet`; the method in every ranking, in RQ2 and in the case-study comparisons CS9 / CS10 (the
pre-specified case-study cell compares against Diffusion-TS and Chronos only).

## Assembler

**What it is.** An assembler: it receives the pool `(N, T, 3)` and returns a path — the indices of `ctx.K`
windows in order — and a dict of diagnostics. With seam processing `ctx.K` is larger than K (as many windows as
the joiner requests). Built-in assemblers are in `marathonts/bench/assemblers.py`; `seam_jump(pool)` gives the N × N matrix
of jumps at the seams (the cost of the built-in greedy and TSP assemblers).

**Plugin.**

```python
import numpy as np
from marathonts.bench import registry as R
from marathonts.bench.assemblers import Assembler, seam_jump

@R.assemblers.register("my_greedy")
class MyGreedy(Assembler):
    # requires = ("my_solver",)                      # modules; without them the unit fails with their names
    # uses_targets = True                            # if it reads the task thresholds (they enter its fingerprint)

    def assemble(self, pool, ctx):
        E = seam_jump(pool)                          # jump at the seam i → j, (N, N); diagonal +inf
        path = [int(ctx.params.get("start", 0))]
        used = set(path)
        for _ in range(ctx.K - 1):
            row = E[path[-1]].copy()
            row[list(used)] = np.inf
            nxt = int(np.argmin(row))
            path.append(nxt)
            used.add(nxt)
        return np.array(path), {"edge_sum": float(sum(E[a, b] for a, b in zip(path, path[1:])))}
```

**Switch on.** `extra_assemblers=["my_greedy"]` (with `methods=None` in the notebook cell): the method
`<prefix>_my_greedy` on every pool of `pool_suites` (`vae_my_greedy`). Parameters: `extra={"my_greedy": {...}}`.
With `smooth_paths` containing `"my_greedy"` it also gets seam processing (`vae_my_greedy_xfade`, …).

**Stages.** `generate` (the pools are reused), `fidelity`, `utility`, `collect`, the analysis.

**Check.** Rows with `method == "vae_my_greedy"` in the tables; the diagnostics of `info` in
`tables/timing.parquet`; the method in the rankings, RQ0–RQ9 and, on the pool of the case-study method, in
CS9 / CS10.

## Seam processing

**What it is.** A joiner: it receives the windows of a path in order `(n, T, F)` and joins them into a series of
length `L = K·T`. Overlaps shorten the series, so `windows_needed(K, T, cfg)` says how many windows to request
from the assembler. It returns the series channels `X (L, F)`, the seam positions, the index of the path window of
each point and diagnostics. Built-ins are `crossfade`, `wsola`, `quilt` (`marathonts/bench/joiners.py`).

**Plugin.** A linear crossfade of the value channel over `overlap` points:

```python
import numpy as np
from marathonts.bench import registry as R
from marathonts.bench.joiners import Joiner

@R.joiners.register("my_blend")
class MyBlend(Joiner):
    def _o(self, cfg):
        return int(cfg.params("my_blend").get("overlap", 6))

    def windows_needed(self, K, T, cfg):
        return 1 + int(np.ceil((K * T - T) / (T - self._o(cfg))))

    def join(self, W, L, cfg):
        o = self._o(cfg)
        n, T, F = W.shape
        X = np.zeros((T + (n - 1) * (T - o), F), np.float32)
        src = np.zeros(len(X), np.int64)
        X[:T], pos, seams = W[0], T, []
        r = np.linspace(0, 1, o, endpoint=False)[:, None]       # weight of the next window
        for k in range(1, n):
            X[pos - o:pos, :1] = (1 - r) * X[pos - o:pos, :1] + r * W[k, :o, :1]
            X[pos:pos + T - o] = W[k, o:]
            src[pos - o // 2:pos + T - o] = k
            seams.append(pos - o // 2)
            pos += T - o
        seams = np.array([s for s in seams if 0 < s < L], int)
        return X[:L], seams, src[:L], {"overlap": o}
```

**Switch on.** `extra_joiners=["my_blend"]` and the assemblers it runs over in `smooth_paths` (e.g.
`["greedy"]`; `"all"` — every assembler except the random path and `vae_quilting`), with `methods=None`. `joiners`
selects among the seam processings (`None` — the built-in ones and `extra_joiners`). Methods:
`<prefix>_<assembler>_my_blend` (`vae_greedy_my_blend`).

**Stages.** `generate`, `fidelity`, `utility`, `collect`, the analysis.

**Check.** Rows of `vae_greedy_my_blend` in the tables. The rankings leave out the seam-processing variants
unless every assembler has them (`rank_exclude=None` and `smooth_paths="all"`); `--rank-exclude` without names
ranks every method. The variants enter RQ3 (b, c) and C4.

## Single method

**What it is.** A method is what is compared: pool + assembler (+ seam processing) or a long-series generator. The
fields above register methods in bulk; `register_method` registers one combination.

**Plugin.**

```python
from marathonts.bench.methods import register_method

register_method("vae_greedy_blend", pool="tsgm_vae", assembler="greedy", joiner="my_blend")
register_method("gan_greedy", pool="my_gan", assembler="greedy")
register_method("my_long", long="seasonal_boot")
```

`register_stitch_suite("gan", "my_gan")` (`bench.methods`) registers the whole suite on one pool, as
`pool_suites` does. The names `real` and anything with `@` are reserved.

**Switch on.** A method registered this way is not part of the method list built from the fields; name it in
`methods` (`methods=[*cfg.methods, "vae_greedy_blend"]`, or `--methods` with the full list).

**Stages and check.** As for an assembler or a long-series generator.

## ML model

**What it is.** A downstream model of the utility stage, trained per task × regime (TRTR on real train, TSTR on
the synthetic series) and tested on the real val / OOT. `kinds` declares the task kinds it supports. The format
of `predict` by kind: `clf` → `(n,)` probability of class 1; `mc` → `(n, C)`; `reg`, `vol` → `(n,)`; `qreg` →
`(n, 3)`; `ms` → `(n, h)`. Hyperparameters come from `marathonts/bench/model_configs.json` (`[<name>]`), updated by
`extra[<name>]`, as `self.params`; `self.task`, `self.seed` and `self.device` are set.

**Plugin.**

```python
from marathonts.bench import registry as R
from marathonts.bench.models import BaseModel

@R.models.register("my_trees")
class MyTrees(BaseModel):
    kinds = {"clf", "reg"}                           # task kinds the model supports

    def fit(self, X, y):
        from sklearn.ensemble import ExtraTreesClassifier, ExtraTreesRegressor
        cls = ExtraTreesClassifier if self.task.kind == "clf" else ExtraTreesRegressor
        self.m = cls(n_estimators=self.params.get("n_estimators", 200), random_state=self.seed, n_jobs=-1)
        self.m.fit(X, y)
        return self

    def predict(self, X):                            # clf → P(y = 1)
        return self.m.predict_proba(X)[:, 1] if self.task.kind == "clf" else self.m.predict(X)

    def state(self):
        from marathonts.bench.storage import blob
        return {"model": blob(self.m)}

    def load_state(self, arrays):
        from marathonts.bench.storage import unblob
        self.m = unblob(arrays["model"])
        return self
```

**Switch on.** `models=[*cfg.models, "my_trees"]` or `--models linear gbdt mlp my_trees`; `model_tasks={"my_trees":
[...]}` restricts it to some tasks. Its fixed hyperparameters and search grid can be added to
`marathonts/bench/model_configs.json` (`"my_trees": {...}`, `"grids": {"my_trees": [...]}`) or set in `extra`.

**Stages.** `utility` computes only the added model's cells (task × model) in the existing units; then `collect` and
the analysis. A model without `kinds` inherits every kind and the stage warns; it also warns about a task that no
model of the run can fit.

**Check.** Rows with `model == "my_trees"` in `tables/utility.parquet`, `METRIC_VALUES.md` (per model), the model
leaves of `LEADERBOARD.md`. The aggregated utility criteria use the models fitted on every task of the criterion;
a model that covers only some of them (here: no `mc`) stays in the per-model leaves.

## Fidelity metric

**What it is.** A metric group: a function that receives a shared context and returns `{metric: value}`; the
orientation of each metric is given at registration (−1: lower is better, +1: higher is better). The context
(`bench.fidelity.FidelityContext`) holds the synthetic series `ctx.x` and its calendar `ctx.how`, the real
reference `ctx.ref` / `ctx.ref_how`, the real train `ctx.train` / `ctx.train_how`, `ctx.T`, the seams `ctx.sv`,
z-scored series `ctx.zx` / `ctx.zr`, random windows `ctx.windows`, window features `ctx.features`, `ctx.rng`,
`ctx.target_params` and `ctx.params`.

**Plugin.**

```python
import numpy as np
from marathonts.bench.fidelity import register_fidelity_group

@register_fidelity_group("M_spikes", {"M1_spike_rate_err": -1})
def spikes(ctx):
    thr = 3 * np.nanstd(np.diff(ctx.ref))
    rate = lambda v: np.nanmean(np.abs(np.diff(v)) > thr)
    return {"M1_spike_rate_err": abs(rate(ctx.x) - rate(ctx.ref))}
```

**Switch on.** With `fidelity_groups=None` (default) every registered group runs. The metric is computed against
every reference (`M1_spike_rate_err`, `M1_spike_rate_err@train`, `M1_spike_rate_err@oot`); `primary_only=True`
in the decorator computes it once, against the primary reference. Parameters: `extra={"M_spikes": {...}}` →
`ctx.params`.

**Stages.** `fidelity` computes only the added group on the existing series (per-group fingerprints), then
`collect` and the analysis. A group that raises does not lose the unit: its metrics are NaN, the error goes to
`errors.log` and the group is retried on the next run; a returned metric that is not in the spec (no orientation)
is logged there too and ignored by the analysis.

**Check.** The columns in `tables/fidelity.parquet` and `metric_values/fidelity.parquet`; the metric in the
rankings (its group is its own criterion unless `metric_criteria={"M_spikes": "distribution"}` assigns one), RQ0,
RQ2–RQ4 and CS9. The overall leaderboard and the tables of `METRIC_VALUES.md` use the core metrics only
(`core_metrics`). `metric_criteria` and `core_metrics` are analysis-only settings; they reach the analysis through
`hypotheses.run --config` ([CONFIGURATION.md](CONFIGURATION.md#analysis-only-settings)). Which case-study
hypotheses a metric enters is set by its name prefix (CS2 — `F1.`–`F3.`, CS4 — `F7.`, …) or by your own
[hypothesis](#hypothesis).

## Utility metric

**What it is.** A function of the labels and predictions of one test split, called for every task;
`ctx = {"kind", "scale", "train_share", "task"}`. It returns a dict of numbers (other values are dropped with a
warning; a key already returned by another metric function keeps the first value).

**Plugin.**

```python
import numpy as np
from marathonts.bench import registry as R

@R.utility_metrics.register("top_decile_precision")
def top_decile_precision(y, pred, ctx):
    if ctx["kind"] != "clf":
        return {}
    top = pred >= np.quantile(pred, 0.9)
    return {"precision_top10": float(y[top].mean())}
```

**Switch on.** Every registered metric function runs. The analysis needs the orientation of each returned
metric: `metric_orient={"precision_top10": 1}`, passed to the analysis with `hypotheses.run --config`
([CONFIGURATION.md](CONFIGURATION.md#analysis-only-settings)); without it the column is not analysed and the
analysis warns.

**Stages.** `utility`: the metric is computed when a cell is computed. The list of metric functions is not part
of the cell fingerprints, so cells already done keep their metrics; to add the metric to an existing run, its
utility units are recomputed (a unit without `cells.json` has no done cells, e.g.
`rm artifacts/<profile>/utility/*/*/seed*/cells.json`). Then `collect` and the analysis.

**Check.** The column `precision_top10` in `tables/utility.parquet` and `metric_values/utility.parquet`.

## Statistical test

**What it is.** A test that adds columns to every comparison table of the analysis. The `global` level receives
the dataset effects in noise units (`z`); the `dataset` level receives the per-seed paired differences of one
dataset and the noise margin (`d, margin`). A test that raises adds a column `<name>_error` and does not stop the
analysis.

**Plugin.**

```python
from marathonts.hypotheses.stats import register_test

@register_test("bayes_sign", level="global")
def bayes_sign(z):
    from scipy import stats
    k, n = int((z > 0).sum()), len(z)
    return {"p_bayes_better": float(stats.beta(1 + k, 1 + n - k).sf(0.5))}
```

**Switch on and run.** Load the file in the analysis: `python -m marathonts.hypotheses.run --plugins my_tests.py`
(notebook 07: `main([..., "--plugins", "my_tests.py"])`). Nothing in stages 0–6 is redone.

**Check.** The column `p_bayes_better` in `artifacts/<profile>/hypotheses/*_global.parquet`.

## Hypothesis

**What it is.** A question about a specific method, reported with the case study: a function of the benchmark
tables (`timing`, `fidelity`, `utility`, `cross_seed`, `datasets`, `pools`) and the configuration that returns
`{"global": DataFrame, "per_dataset": DataFrame, "extra": dict}`. `hypotheses.catalog` provides the helpers
of the built-in ones (`fidelity_long`, `_run`: paired comparisons of the case-study method against comparators,
noise margins, corrections, verdicts).

**Plugin.**

```python
from marathonts.bench.fidelity import ORIENT
from marathonts.hypotheses.catalog import _run, fidelity_long, register_hypothesis

@register_hypothesis("CS16", "Spike rate of the assembled series against the random path")
def cs16(tables, cfg):
    L = fidelity_long(tables["fidelity"])
    return _run(L, ORIENT, ["vae_rand"], units=["M1_spike_rate_err"], adjust="bh",
                alpha=cfg.alpha, q=cfg.equivalence_margin_q, n_boot=cfg.n_boot)
```

**Switch on and run.** `python -m marathonts.hypotheses.run --plugins my_plugins.py my_tests.py` — the plugin of the metric
that the hypothesis tests is loaded too (otherwise its orientation is unknown and its rows are dropped; plugins
recorded in `tables/config.json` are loaded automatically). Hypotheses run with the case study, i.e. when
`--case-method` (default `Config.case_method`) has results in the tables and `--no-case-study` is not given;
`--only CS16` runs it alone.

**Check.** The section `CS16` of `REPORT.md` and `artifacts/<profile>/hypotheses/CS16_global.parquet`,
`CS16_per_dataset.parquet`.

## What is saved and how to load it back

Everything goes to `artifacts/<profile>/` in Parquet ([BENCHMARK.md](BENCHMARK.md), "Artifacts"). The analysis
writes its Markdown reports to `artifacts/<profile>/reports/` — `REPORT.md`, `OVERALL.md`, `LEADERBOARD.md` and
`METRIC_VALUES.md` — and their tables to `hypotheses/`, `overall/`, `leaderboard/` and `metric_values/`, read back
with `pandas.read_parquet`. Trained generators and models are loaded back without training (`marathonts/bench/load.py`):

```python
from marathonts.bench import load
gen = load.load_generator(cfg, "ett", "my_gan", seed=0)
m = load.load_model(cfg, "ett", "gan_greedy", 0, task="spike_h12", model="my_trees", regime="S")
X, y, _ = load.task_xy(cfg, "ett", "spike_h12", split="oot")
pred = m.predict(X)
```

For this the component must have a `load_state` that is the inverse of `state`.
