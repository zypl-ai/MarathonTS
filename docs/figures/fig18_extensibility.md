# Figure 18 — Extension points

**File:** `fig18_extensibility.pdf`

**Suggested caption.** Extension points. Every part of the benchmark is registered by name. A
plugin file registers new components, and the configuration selects them. A new pool generator,
assembler, seam joiner or long-series generator becomes part of the comparison and of the relevant
hypotheses without changes to the benchmark code.

## How it works

- A plugin (`my_plugins.py`) uses `@registry.<kind>.register("name")`, or the helpers
  `register_task`, `register_method`, `register_fidelity_group`, `register_test`,
  `register_hypothesis`.
- `Config` loads the plugin everywhere: in every notebook, in subprocesses of other environments,
  and in the hypothesis part (the run configuration is stored in `tables/config.json`).
- Automatic expansion: `pool_suites` adds the whole assembly suite on a new pool generator
  (`<prefix>_zseries`, `<prefix>_rand`, …); `extra_assemblers` adds an assembler on every pool,
  `extra_joiners` a seam processing over the assemblers of `smooth_paths`; `long_methods` adds a long-series
  generator as a method and a baseline; `disabled` switches off any method or component by name. New methods enter
  the ranking and the research questions automatically (their family is read from the method spec);
  the confirmatory family covers Diffusion-TS and Chronos.
- Any method can be the subject of the case study (`hypotheses.run --case-method … --noise-pair …`).
- Source: `marathonts/bench/registry.py`, `EXTENDING.md`.
