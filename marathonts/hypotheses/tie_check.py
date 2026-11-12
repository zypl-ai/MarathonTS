"""Supplementary check of the noise-aware ranks of the overall leaderboard (not pre-specified): order
invariance, non-transitive ties and the change against ordinary average ranks.

    python -m marathonts.hypotheses.tie_check --artifacts-dir artifacts/run_h200 [--out-dir <dir>]

The algorithm (`overall.rank_noise`): within a block (dataset, seed, leaf), with the noise e of the leaf on that
dataset (one value for every pair of methods), the rank of method i is
1 + #{j: s_j beats s_i by more than e} + ½ #{j ≠ i: |s_j − s_i| ≤ e}. No groups are formed, so ties need not
be transitive and every method is ranked from its own comparisons; the ranks of a block always sum to
k(k + 1)/2. With methods missing in a block (leakage), the ranks are rescaled to 1…k. Written to `<out>/`
(default `<artifacts>/supplementary/tie_check`): `places.parquet` (mean rank, place and tier with
noise-aware and with ordinary ranks) and `TIE_CHECK.md`.
"""
from __future__ import annotations

import argparse
import dataclasses
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pandas as pd

from marathonts.bench import registry as R
from marathonts.bench.storage import write_table


def example() -> str:
    """The three-method example of the docstring, computed with `rank_noise`."""
    from marathonts.hypotheses.overall import rank_noise

    L = pd.DataFrame({"dataset": "d", "seed": 0, "leaf": "l", "slice": "s", "method": ["A", "B", "C"],
                      "score": [1.2, 0.6, 0.0]})
    r = rank_noise(L, 3, pd.Series([1.0], index=pd.MultiIndex.from_tuples([("d", "l", "s")])))
    p = rank_noise(L, 3, None)
    t = pd.DataFrame({"score (higher is better)": L["score"].to_numpy(), "noise-aware rank": r["rank"].to_numpy(),
                      "ordinary rank": p["rank"].to_numpy()}, index=L["method"])
    return ("Scores 1.2 (A), 0.6 (B), 0.0 (C), noise 1: A ties B, B ties C, but A beats C. A: 1 + 0 + ½·1 = 1.5; "
            "B: 1 + 0 + ½·2 = 2; C: 1 + 1 + ½·1 = 2.5.\n\n" + t.to_markdown())


def load(art: Path):
    import marathonts.bench.config as C
    from marathonts.bench.config import Config
    from marathonts.hypotheses import engine as E
    from marathonts.hypotheses.run import _run_config, load_tables

    C.RUN_CONTEXT = False
    cfg = _run_config(SimpleNamespace(profile="min", artifacts_dir=str(art)))
    cfg = dataclasses.replace(cfg, artifacts_dir=art)
    T = load_tables(cfg)
    methods = sorted(set(T["timing"]["method"]))
    cfg = dataclasses.replace(cfg, methods=methods, disabled=[], frozen_methods=[])
    E.configure(cfg)
    assert isinstance(cfg, Config)
    return T, cfg


def run(art: Path) -> tuple[pd.DataFrame, dict]:
    from marathonts.hypotheses import overall as O
    from marathonts.hypotheses.leaderboard import leaderboard_methods, summarize

    R.load_builtins()
    T, cfg = load(art)
    methods = leaderboard_methods(T, cfg)
    k = len(methods)
    noise = O.leaf_noise(T, cfg)
    L = O.select(O.rows(T, cfg, methods), cfg)
    ranks = O.rank_noise(L, k, noise)
    # order invariance: other names, so the method columns come in another order
    rng = np.random.default_rng(0)
    alias = dict(zip(methods, [f"m{i:03d}" for i in rng.permutation(len(methods))]))
    back = {v: m for m, v in alias.items()}
    r2 = O.rank_noise(L.assign(method=L["method"].map(alias)), k, noise)
    r2 = r2.assign(method=r2["method"].map(back))
    key = ["dataset", "seed", "leaf", "slice", "method"]
    j = ranks.set_index(key)["rank"].align(r2.set_index(key)["rank"], join="inner")
    order_diff = float(np.nanmax(np.abs(j[0].to_numpy() - j[1].to_numpy())))
    # non-transitive ties: pairs (i, j) not tied but linked by a method tied with both
    idx = ["dataset", "seed", "leaf", "slice"]
    W = L.pivot_table(index=idx, columns="method", values="score")
    keyn = pd.MultiIndex.from_arrays([W.index.get_level_values(n) for n in ("dataset", "leaf", "slice")])
    eps = noise.reindex(keyn).fillna(0.0).to_numpy()
    S = W.to_numpy(float)
    pairs = tied = intrans = 0
    for i in range(0, len(S), 2000):
        s, e = S[i:i + 2000], eps[i:i + 2000, None, None]
        ok = ~np.isnan(s)
        both = ok[:, :, None] & ok[:, None, :]
        off = both & ~np.eye(s.shape[1], dtype=bool)[None]
        Tm = (np.abs(s[:, :, None] - s[:, None, :]) <= e) & off
        link = np.einsum("nij,njk->nik", Tm.astype(np.int32), Tm.astype(np.int32)) > 0
        pairs += int(off.sum()) // 2
        tied += int(Tm.sum()) // 2
        intrans += int((link & ~Tm & off).sum()) // 2
    # noise-aware against ordinary ranks: mean rank, place and tier
    main = summarize(O.overall_rank(O.aggregate(ranks)[1]), 1000)
    plain = summarize(O.overall_rank(O.aggregate(O.rank_noise(L, k, None))[1]), 1000)
    P = pd.DataFrame({"mean_rank": main["avg_rank"], "place": main["avg_rank"].rank(method="min"),
                      "top_tier": main["tier_wilcoxon"]})
    Q = pd.DataFrame({"mean_rank_plain": plain["avg_rank"], "place_plain": plain["avg_rank"].rank(method="min"),
                      "top_tier_plain": plain["tier_wilcoxon"]})
    P = P.join(Q).sort_values("mean_rank")
    info = dict(order_max_abs_diff=order_diff, pairs=pairs, tied=tied, intransitive=intrans,
                tau=float(P["mean_rank"].corr(P["mean_rank_plain"], method="kendall")))
    return P, info


def report(P: pd.DataFrame, info: dict, art: Path) -> str:
    ch = P[(P["place"] != P["place_plain"]) | (P["top_tier"] != P["top_tier_plain"])]
    return "\n".join([
        f"# Tie check — {art.name}", "",
        "Supplementary, not pre-specified (`python -m marathonts.hypotheses.tie_check`). Noise-aware ranks of the "
        "overall leaderboard (`overall.rank_noise`, see the module docstring).", "",
        "## Worked example", "", example(), "",
        "## Order invariance", "",
        f"Ranks recomputed with the methods renamed so that they come in another order: largest difference "
        f"{info['order_max_abs_diff']:.3g}.", "",
        "## Non-transitive ties", "",
        f"Pairs of methods compared within a block: {info['pairs']}; tied (within the noise): {info['tied']} "
        f"({info['tied'] / info['pairs']:.1%}); not tied but linked by a method tied with both: "
        f"{info['intransitive']} ({info['intransitive'] / info['pairs']:.1%}).", "",
        "## Against ordinary ranks", "",
        f"Kendall's tau between the mean ranks: {info['tau']:.3f}. Methods whose place or tier membership differs:",
        "", ch.to_markdown(floatfmt=".2f") if len(ch) else "none", "", "All methods:", "",
        P.to_markdown(floatfmt=".2f"), ""])


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--artifacts-dir", required=True)
    ap.add_argument("--out-dir")
    a = ap.parse_args(argv)
    art = Path(a.artifacts_dir)
    out = Path(a.out_dir) if a.out_dir else art / "supplementary" / "tie_check"
    P, info = run(art)
    out.mkdir(parents=True, exist_ok=True)
    write_table(P.reset_index(names="method"), out / "places.parquet", keep64=["mean_rank", "mean_rank_plain"])
    text = report(P, info, art)
    (out / "TIE_CHECK.md").write_text(text)
    print(text)


if __name__ == "__main__":
    main()
