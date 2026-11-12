# Contributing to MarathonTS

Contributions are welcome: new datasets, generators, assemblers, seam joiners, downstream models, metrics,
statistical tests and fixes.

## Reporting a problem

Open a [GitHub issue](https://github.com/zypl-ai/MarathonTS/issues) with the command you ran, the profile, the
environment (Docker, Colab or local; Python and library versions) and the error message or the unexpected
output. For a question about a result, name the table or report and the method, dataset and seed.

## Adding a component

Every component is registered by name in a plugin file and switched on by one line of configuration; no
benchmark code has to change. [EXTENDING.md](docs/EXTENDING.md) describes each kind of component with its
interface, an example, how to switch it on and which stages it recomputes.

A new component should:

- use the training split only (no information from val or OOT);
- follow the interface of its kind in EXTENDING.md and leave storage to the pipeline, so that the
  fingerprints and incremental recomputation work;
- come with a short description in the relevant file of `docs/` and, for a method, its reference in
  `docs/BASELINES.md` and `docs/LITERATURE.md`.

## Before a pull request

1. Run the tests: `pip install -r tests/requirements.txt && python -m pytest tests` (a few minutes: the smoke
   test rebuilds the published rankings and questions from `artifacts/run_*/tables/`; CI runs the same). For a change
   to the pipeline, also `python -m marathonts.bench.run all --quick` and
   `python -m marathonts.hypotheses.run --artifacts-dir artifacts/quick`.
2. If the change affects the results of the `min` run, say so in the pull request: published tables in
   `artifacts/run_h200/` and `artifacts/run_l4/` are updated only together with a new version (see [CHANGELOG.md](CHANGELOG.md)).
3. Code, comments and documentation are in English.

By contributing, you agree that your contribution is licensed under the [Apache License 2.0](LICENSE).
