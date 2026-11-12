"""Supplementary inventory of the units of RQ0 (not pre-specified): every metric and reference that the validity
check tests, mapped to the metric IDs of the paper's metric table, with the exclusions and the expanded outputs.

    python -m marathonts.hypotheses.rq0_inventory --artifacts-dir artifacts/run_h200 [--out-dir <dir>]

RQ0 (c) (`questions.rq0_validity`) tests every fidelity unit against train, val and OOT and every utility unit
(task × model × test split, primary metric). The 83 fidelity outputs (`fidelity.ORIENT`) belong to 66 metric IDs
(F1.1 ... F12.x): some IDs have several outputs (lags, quantiles, window lengths). Two outputs, the
calendar-continuity metrics F4.4 and F4.5, are left out of every question (`catalog.CALENDAR_VALIDITY`). The two
memorisation metrics F10 are computed once, against train; the tables of the analysis label a unit without a
reference suffix with the primary reference (val), so `reference_label` shows val and `reference` train.

Written to `<out>/` (default `<artifacts>/supplementary/rq0_inventory`): `inventory.parquet` (one row per unit:
unit, kind, group, metric ID, output, reference label, reference, discriminative, and whether it is in a
redundant pair of RQ0 (d)), `excluded.parquet` (the outputs left out) and `RQ0_INVENTORY.md`. CPU only.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from marathonts.bench.storage import write_table


def run(art: Path):
    from marathonts.bench.fidelity import GROUP_OF, ORIENT, split_ref
    from marathonts.hypotheses.catalog import CALENDAR_VALIDITY

    G = pd.read_parquet(art / "hypotheses" / "RQ0_global.parquet")
    red = pd.read_parquet(art / "hypotheses" / "RQ0_redundant_pairs.parquet")
    in_pair = set(red["metric_a"]) | set(red["metric_b"])
    rows = []
    for r in G.itertuples():
        fid = str(r.group).startswith("F")
        if fid:
            out = str(r.unit).split("@")[0]
            mid = out.split("_")[0]
            kind = "memorisation" if str(r.group).startswith("F10") else "fidelity"
            ref = "train" if kind == "memorisation" else r.reference
        else:
            task, model, _, split, metric = str(r.unit).split("|")
            out, mid, kind, ref = f"{task}|{model}|{metric}", task, "utility", split
        rows.append(dict(unit=r.unit, kind=kind, group=r.group, metric_id=mid, output=out,
                         reference_label=r.reference, reference=ref, discriminative=bool(r.discriminative),
                         in_redundant_pair=out in in_pair))
    inv = pd.DataFrame(rows)
    outputs = sorted({split_ref(u, "val")[0] for u in ORIENT})
    used = set(inv.loc[inv["kind"] != "utility", "output"])
    excl = pd.DataFrame([dict(output=o, metric_id=o.split("_")[0], group=GROUP_OF.get(o),
                              reason="calendar-continuity metric, left out of every question"
                              if o in CALENDAR_VALIDITY else "not tested in RQ0")
                         for o in outputs if o not in used])
    ids = pd.Series(outputs).str.split("_").str[0]
    info = dict(outputs=len(outputs), ids=ids.nunique(),
                multi={k: int(v) for k, v in ids.value_counts().items() if v > 1})
    return inv, excl, info


def report(inv, excl, info, art: Path) -> str:
    by = inv.pivot_table(index="reference", columns="kind", values="discriminative", aggfunc=["size", "sum"],
                         fill_value=0)
    by.columns = [f"{a}_{b}".replace("size", "units").replace("sum", "discriminative") for a, b in by.columns]
    ut = inv[inv["kind"] == "utility"]
    return "\n".join([
        f"# RQ0 inventory — {art.name}", "",
        "Supplementary, not pre-specified (`python -m marathonts.hypotheses.rq0_inventory`). See the module "
        "docstring.", "",
        f"Units of RQ0 (c): {len(inv)} — fidelity {int((inv['kind'] == 'fidelity').sum())} "
        f"({inv.loc[inv['kind'] == 'fidelity', 'output'].nunique()} outputs × 3 references), memorisation "
        f"{int((inv['kind'] == 'memorisation').sum())} (against train), utility {len(ut)} "
        f"({ut['metric_id'].nunique()} tasks; models: {', '.join(sorted(ut['output'].str.split('|').str[1].unique()))}; "
        f"splits: {', '.join(sorted(ut['reference'].unique()))}). Discriminative: {int(inv['discriminative'].sum())}.",
        "",
        f"Fidelity outputs: {info['outputs']} in {info['ids']} metric IDs; IDs with several outputs: "
        + ", ".join(f"{k} ({v})" for k, v in sorted(info["multi"].items())) + ".", "",
        "By reference (memorisation: the actual reference, train; the analysis tables label it val):", "",
        by.to_markdown(), "",
        "Outputs left out:", "", excl.to_markdown(index=False) if len(excl) else "none", "",
        f"Outputs in a redundant pair of RQ0 (d) (|rho| >= 0.9): "
        f"{', '.join(sorted(inv.loc[inv['in_redundant_pair'], 'output'].unique()))}.", "",
        "Utility units:", "", ut[["unit", "discriminative"]].to_markdown(index=False), ""])


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--artifacts-dir", required=True)
    ap.add_argument("--out-dir")
    a = ap.parse_args(argv)
    art = Path(a.artifacts_dir)
    out = Path(a.out_dir) if a.out_dir else art / "supplementary" / "rq0_inventory"
    inv, excl, info = run(art)
    out.mkdir(parents=True, exist_ok=True)
    write_table(inv, out / "inventory.parquet")
    write_table(excl, out / "excluded.parquet")
    text = report(inv, excl, info, art)
    (out / "RQ0_INVENTORY.md").write_text(text)
    print(text)


if __name__ == "__main__":
    main()
