"""Supplementary check of the top tier of the overall leaderboard (not pre-specified): the paired datasets
behind each comparison with the leader, and a non-rejection set that accounts for the selection of the leader.

    python -m marathonts.hypotheses.tier_check --artifacts-dir artifacts/run_h200 [--out-dir <dir>]

The pre-specified top tier (`leaderboard.summarize`): the method with the best mean rank and every method that a
one-sided Wilcoxon test over datasets, Holm-corrected over the comparisons with that method, does not show to be
worse. The leader is chosen on the same data, which the test does not account for. The all-pairs set tests
every ordered pair of methods (one-sided Wilcoxon over the datasets ranked for both, Holm over all pairs) and
keeps every method that no other method is shown to beat; it does not depend on which method is the observed
leader. Both are non-rejection sets: membership does not establish equivalence and may reflect limited power.
Written to `<out>/` (default `<artifacts>/supplementary/tier_check`): `tier.parquet` and `TIER_CHECK.md`.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from marathonts.bench import registry as R
from marathonts.bench.storage import write_table


def run(art: Path) -> tuple[pd.DataFrame, dict]:
    from marathonts.hypotheses import overall as O
    from marathonts.hypotheses import stats as S
    from marathonts.hypotheses.leaderboard import leaderboard_methods, summarize
    from marathonts.hypotheses.tie_check import load

    R.load_builtins()
    T, cfg = load(art)
    methods = leaderboard_methods(T, cfg)
    k = len(methods)
    x = O.overall_rank(O.aggregate(O.rank_noise(O.select(O.rows(T, cfg, methods), cfg), k, O.leaf_noise(T, cfg)))[1])
    main = summarize(x, 1000)
    D = x.unstack("method").groupby(level="dataset").mean()[main.index]
    best = main.index[0]
    alpha = cfg.alpha
    # all ordered pairs: is i worse (higher rank) than j?
    names = list(main.index)
    p = {}
    for i in names:
        for j in names:
            if i != j:
                d = (D[i] - D[j]).dropna().to_numpy()
                p[(i, j)] = S.wilcoxon(d, "greater") if len(d) else np.nan
    keys = list(p)
    adj = dict(zip(keys, S.holm(np.array([p[q] for q in keys], float))))
    beaten = {i: [j for j in names if j != i and adj[(i, j)] < alpha] for i in names}
    out = pd.DataFrame({
        "mean_rank": main["avg_rank"],
        "paired_datasets_with_leader": [int((D[m] - D[best]).notna().sum()) if m != best else int(D[m].notna().sum())
                                        for m in names],
        "p_worse_than_leader_holm": main["p_worse_than_best_holm"],
        "tier": main["tier_wilcoxon"],
        "min_p_all_pairs_holm": [min([adj[(i, j)] for j in names if j != i]) for i in names],
        "all_pairs_set": [not beaten[i] for i in names],
    }, index=names)
    info = dict(leader=best, k=k, n_datasets=len(D), n_pairs=len(keys),
                min_p_raw=float(np.nanmin(list(p.values()))), tier=int(out["tier"].sum()),
                all_pairs=int(out["all_pairs_set"].sum()))
    return out, info


def report(out: pd.DataFrame, info: dict, art: Path) -> str:
    return "\n".join([
        f"# Tier check — {art.name}", "",
        "Supplementary, not pre-specified (`python -m marathonts.hypotheses.tier_check`). `tier`: the "
        "pre-specified top tier (comparisons with the observed leader, Holm over them). `all_pairs_set`: methods "
        "that no other method is shown to beat (one-sided Wilcoxon over datasets for every ordered pair, Holm over "
        "all pairs); it does not depend on the choice of the leader. Both are non-rejection sets: membership does "
        "not establish equivalence and may reflect limited power.", "",
        f"Leader: {info['leader']}; {info['k']} methods, {info['n_datasets']} datasets, {info['n_pairs']} ordered "
        f"pairs; smallest one-sided p before correction: {info['min_p_raw']:.4f}. Top tier: {info['tier']} methods; "
        f"all-pairs set: {info['all_pairs']} methods.", "",
        out.to_markdown(floatfmt=".3g"), ""])


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--artifacts-dir", required=True)
    ap.add_argument("--out-dir")
    a = ap.parse_args(argv)
    art = Path(a.artifacts_dir)
    out_dir = Path(a.out_dir) if a.out_dir else art / "supplementary" / "tier_check"
    out, info = run(art)
    out_dir.mkdir(parents=True, exist_ok=True)
    write_table(out.reset_index(names="method"), out_dir / "tier.parquet", keep64=["mean_rank"])
    text = report(out, info, art)
    (out_dir / "TIER_CHECK.md").write_text(text)
    print(text)


if __name__ == "__main__":
    main()
