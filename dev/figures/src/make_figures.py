"""Benchmark design figures (structure and pipelines, no results).

    python docs/figures/src/make_figures.py

Graphviz (`dot`) renders the diagrams, matplotlib the timeline. Every figure is written as a vector
PDF to `docs/figures/` and its Graphviz source to `docs/figures/src/dot/`.
"""
from __future__ import annotations

import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE.parent
DOT = HERE / "dot"

FONT = "Helvetica"
# one palette for all figures; fills stay distinct in grayscale (different lightness)
C = dict(
    data="#D6E6F4",      # real data, preprocessing
    gen="#F9DCC2",       # generative models
    stitch="#FCEFB4",    # assembly
    ml="#D5ECD0",        # downstream ML (utility)
    stats="#E3DAF0",     # statistics, hypotheses
    store="#EDEDED",     # artifacts on disk
    eval="#F6D5DA",      # fidelity evaluation
    white="#FFFFFF",
    edge="#3A3A3A",
    accent="#B03A2E",    # leakage guards, "real only" paths
    muted="#7A7A7A",
)

HEAD = f"""
  graph [fontname="{FONT}", fontsize=11, pad=0.15, nodesep=0.28, ranksep=0.38, newrank=true];
  node  [fontname="{FONT}", fontsize=10, shape=box, style="rounded,filled", fillcolor="{C['white']}",
         color="{C['edge']}", penwidth=0.8, margin="0.10,0.05"];
  edge  [fontname="{FONT}", fontsize=8.5, color="{C['edge']}", penwidth=0.8, arrowsize=0.6];
"""


def render(name: str, body: str, rankdir: str = "TB") -> None:
    src = f"digraph {name} {{\n  rankdir={rankdir};\n{HEAD}\n{body}\n}}\n"
    DOT.mkdir(parents=True, exist_ok=True)
    (DOT / f"{name}.dot").write_text(src)
    subprocess.run(["dot", "-Tpdf", "-o", str(OUT / f"{name}.pdf")], input=src.encode(), check=True)
    subprocess.run(["dot", "-Tsvg", "-o", str(OUT / f"{name}.svg")], input=src.encode(), check=True)   # the site


def store(n: str, label: str) -> str:
    return f'{n} [shape=cylinder, style=filled, fillcolor="{C["store"]}", label="{label}"];'


# ---------------------------------------------------------------------------------------------
# 1. Software architecture
# ---------------------------------------------------------------------------------------------
def fig01():
    W = 8                                    # grid columns

    def cell(t, d, col, span=1, bold=True):
        name = f"<B>{t}</B>" if bold else t
        sub = f'<BR/><FONT POINT-SIZE="8">{d}</FONT>' if d else ""
        return f'<TD COLSPAN="{span}" BGCOLOR="{C[col]}" STYLE="ROUNDED">{name}{sub}</TD>'

    def layer(title, cells, note=""):
        lab = f'<FONT POINT-SIZE="8.5" COLOR="{C["muted"]}">{note}</FONT>' if note else ""
        return (f'<TR><TD ALIGN="LEFT" VALIGN="MIDDLE" BORDER="0"><B>{title}</B><BR ALIGN="LEFT"/>{lab}</TD>'
                + "".join(cells) + "</TR>")

    rows = [
        layer("Execution", [cell("Docker", "bench (PyTorch) · tsgm (TF)", "white", 3),
                            cell("Colab notebooks", "01_data … 07_hypotheses", "white", 3),
                            cell("envs/", "base · core · tsgm · sdv ·<br/>diffusion_ts · chronos · timesfm · timestral", "white", 2)],
              "3 ways to run"),
        layer("bench: infra", [cell("run.py", "stage driver", "store", 1),
                               cell("config.py", "Config, profiles,<br/>unit fingerprints", "store", 2),
                               cell("registry.py", "10 name registries", "store", 2),
                               cell("storage.py · load.py", "Parquet I/O, reload", "store", 2),
                               cell("timing.py", "time, memory", "store", 1)]),
        layer("bench: stages", [cell("datasets.py<br/>data.py", "raw → hourly →<br/>split → windows", "data", 1),
                                cell("tasks.py", "14 tasks,<br/>features, labels", "data", 1),
                                cell("generators/", "pool: tsgm_vae, sdv_par,<br/>real_windows · long:<br/>diffusion_ts, chronos,<br/>timesfm, timestral", "gen", 2),
                                cell("assemblers.py<br/>joiners.py", "10 assemblers,<br/>3 seam joiners", "stitch", 1),
                                cell("methods.py", "16 methods (min),<br/>4 of them published", "stitch", 1),
                                cell("fidelity.py", "F1–F12, 83 metrics<br/>× 3 references", "eval", 1),
                                cell("utility.py<br/>models.py", "TSTR / TRTR,<br/>linear, MLP, GBDT", "ml", 1)],
              "raw → prepare → pools →<br/>generate → fidelity →<br/>utility → collect"),
        layer("Libraries", [cell("external/Diffusion-TS", "official code, pinned commit", "gen", 2),
                            cell("zseries assembler", "vae_zseries: proprietary method of zypl.ai (under development),<br/>results published, code not in the repository", "stitch", 3),
                            cell("PyTorch · XGBoost · scikit-learn · statsmodels · OR-Tools · elkai · tsgm · Chronos · TimesFM · Timestral",
                                 "", "white", 3, bold=False)]),
        layer("Storage", [cell("data/", "raw/ · processed/&lt;profile&gt;/", "store", 3),
                          cell("artifacts/&lt;profile&gt;/", "pools · generators · series · records · fidelity · labels ·<br/>utility · tables · reports · overall · leaderboard ·<br/>metric_values · hypotheses",
                               "store", 5)],
              "Parquet (zstd)"),
        layer("hypotheses", [cell("overall.py", "overall leaderboard", "stats", 1),
                          cell("leaderboard.py", "ranking in every slice", "stats", 1),
                          cell("metric_values.py", "metric values<br/>by slice", "stats", 1),
                          cell("questions.py", "RQ0–RQ9, C1–C4", "stats", 1),
                          cell("catalog.py", "loaders,<br/>case study CS", "stats", 1),
                          cell("engine.py · stats.py", "noise, paired effects,<br/>verdicts; Wilcoxon, TOST,<br/>bootstrap, Holm/BH", "stats", 1),
                          cell("reports/", "OVERALL.md · LEADERBOARD.md<br/>METRIC_VALUES.md · REPORT.md", "stats", 2)],
              "reads tables only (CPU)"),
    ]
    table = (f'<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="5" CELLPADDING="5" COLOR="{C["edge"]}">'
             + "".join(rows) + "</TABLE>>")
    render("fig01_architecture", f'  t [shape=plaintext, style="", fontsize=9.5, label={table}];')


# ---------------------------------------------------------------------------------------------
# 2. Stage pipeline
# ---------------------------------------------------------------------------------------------
def fig02():
    stage = lambda n, t, d, col: f'{n} [label=<<b>{t}</b><br/><font point-size="8.5">{d}</font>>, fillcolor="{C[col]}"];'
    body = f"""
  node [width=2.6];
  {stage("raw", "0 · raw", "download, CSV/TXT → lossless Parquet", "data")}
  {stage("prep", "1 · prepare", "hourly series, gap fill, last max_points,<br/>temporal split, scaler, T, K, N", "data")}
  {stage("tgt", "1a · targets (manual, once)", "propose task thresholds on train<br/>→ committed target_params.json", "data")}
  {stage("pools", "2 · pools", "fit pool generator (own env),<br/>sample N windows per seed", "gen")}
  {stage("gen", "3 · generate", "12 methods (min; published results skipped): assemble K·T series from pools;<br/>run long-series generators (Diffusion-TS, Chronos, TimesFM, Timestral)", "stitch")}
  {stage("fid", "4 · fidelity", "F1–F12 vs real val, train, OOT<br/>(+ real ceiling, @len)", "eval")}
  {stage("utl", "5 · utility", "labels; TSTR &amp; TRTR × 14 tasks × 3 models<br/>× {val, OOT}", "ml")}
  {stage("col", "6 · collect", "merge unit files into tables", "store")}
  {stage("sci", "7 · hypotheses", "leaderboard, ranking, metric values, RQ0–RQ9, C1–C4,<br/>case study → reports/: OVERALL.md, LEADERBOARD.md,<br/>METRIC_VALUES.md, REPORT.md", "stats")}

  raw -> prep -> pools -> gen -> fid -> utl -> col -> sci;
  prep -> tgt [style=dashed, arrowhead=none];
  tgt -> utl [style=dashed, label=" thresholds", constraint=false];

  node [width=0, shape=cylinder, style=filled, fillcolor="{C['store']}", fontsize=8.5];
  a0 [label="data/raw/<ds>/*.parquet"];
  a1 [label="data/processed/<profile>/<ds>.parquet\\n+ .meta.parquet (data_key)"];
  a2 [label="pools/<ds>/<gen>/seed<k>\\ngenerators/ (weights)"];
  a3 [label="series/, records/\\n(time, memory, hardware)"];
  a4 [label="fidelity/<ds>/<method>/seed<k>"];
  a5 [label="labels/, utility/…/metrics,\\npredictions, models"];
  a6 [label="tables/*.parquet\\nconfig.json, hardware"];
  a7 [label="reports/*.md\\noverall/, leaderboard/,\\nmetric_values/,\\nhypotheses/RQ*, CS*, confirmatory"];
  {{rank=same; raw; a0}} {{rank=same; prep; a1}} {{rank=same; pools; a2}} {{rank=same; gen; a3}}
  {{rank=same; fid; a4}} {{rank=same; utl; a5}} {{rank=same; col; a6}} {{rank=same; sci; a7}}
  edge [style=dashed, color="{C['muted']}", arrowsize=0.5];
  raw -> a0; prep -> a1; pools -> a2; gen -> a3; fid -> a4; utl -> a5; col -> a6; sci -> a7;

  node [shape=plaintext, style="", fontsize=8.5, fontcolor="{C['muted']}"];
  e1 [label="env: base"]; e2 [label="env: base"]; e3 [label="env: tsgm / sdv\\n(TensorFlow, no torch)"];
  e4 [label="env: core\\n(+ diffusion_ts, chronos,\\ntimesfm, timestral)"]; e5 [label="env: core"]; e6 [label="env: core"];
  e7 [label="env: core"]; e8 [label="env: core (CPU)"];
  {{rank=same; raw; e1}} {{rank=same; prep; e2}} {{rank=same; pools; e3}} {{rank=same; gen; e4}}
  {{rank=same; fid; e5}} {{rank=same; utl; e6}} {{rank=same; col; e7}} {{rank=same; sci; e8}}
  edge [style=invis];
  e1 -> raw; e2 -> prep; e3 -> pools; e4 -> gen; e5 -> fid; e6 -> utl; e7 -> col; e8 -> sci;
"""
    render("fig02_stage_pipeline", body)


# ---------------------------------------------------------------------------------------------
# 3. Environments and hand-off through Parquet
# ---------------------------------------------------------------------------------------------
def fig03():
    body = f"""
  compound=true;
  subgraph cluster_tf {{ label=<<b>env tsgm</b> (Docker target <i>tsgm</i>, Colab 02_pools)<br/><font point-size="8.5">TensorFlow + Keras 3 + tsgm 0.1.0, no torch</font>>;
    style="rounded,filled"; fillcolor="{C['gen']}"; color="{C['edge']}";
    vae [label="pools --pool-generators tsgm_vae\\nfit β-VAE, sample N windows"];
  }}
  subgraph cluster_sdv {{ label=<<b>env sdv</b> (optional)>; style="rounded,filled"; fillcolor="{C['gen']}"; color="{C['edge']}";
    sdv [label="pools --pool-generators sdv_par"];
  }}
  subgraph cluster_core {{ label=<<b>env core</b> (Docker target <i>bench</i>, Colab 03–07)<br/><font point-size="8.5">PyTorch (CUDA or CPU), scikit-learn, XGBoost, statsmodels, OR-Tools, elkai</font>>;
    style="rounded,filled"; fillcolor="{C['stitch']}"; color="{C['edge']}";
    g [label="generate\\nall stitchings of the pool"];
    subgraph cluster_dts {{ label="+ diffusion_ts (einops, repo code)"; style="rounded,dashed"; color="{C['muted']}"; fillcolor="{C['white']}";
      dts [label="generate --methods diffusion_ts"]; }}
    subgraph cluster_chr {{ label="+ chronos (chronos-forecasting)"; style="rounded,dashed"; color="{C['muted']}"; fillcolor="{C['white']}";
      chr [label="generate --methods chronos"]; }}
    subgraph cluster_tfm {{ label="+ timesfm (timesfm 3.0.2)"; style="rounded,dashed"; color="{C['muted']}"; fillcolor="{C['white']}";
      tfm [label="generate --methods timesfm"]; }}
    subgraph cluster_tst {{ label="+ timestral (timestral)"; style="rounded,dashed"; color="{C['muted']}"; fillcolor="{C['white']}";
      tst [label="generate --methods timestral"]; }}
    f [label="fidelity · utility · collect"];
    s [label="hypotheses"];
    g -> f; dts -> f; chr -> f; tfm -> f; tst -> f; f -> s;
  }}
  subgraph cluster_base {{ label=<<b>env base</b>  numpy, scipy, pandas, pyarrow>; style="rounded,filled"; fillcolor="{C['data']}"; color="{C['edge']}";
    rp [label="raw · prepare"];
  }}
  dp [shape=cylinder, style=filled, fillcolor="{C['store']}", label="data/processed\\n(Parquet)"];
  pp [shape=cylinder, style=filled, fillcolor="{C['store']}", label="artifacts/pools\\n(N, T, 3) per seed"];
  sp [shape=cylinder, style=filled, fillcolor="{C['store']}", label="artifacts/series, records"];
  rp -> dp;
  dp -> vae; dp -> sdv; dp -> g; dp -> dts; dp -> chr; dp -> tfm; dp -> tst;
  vae -> pp; sdv -> pp;
  pp -> g [label=" read only"];
  g -> sp; dts -> sp; chr -> sp; tfm -> sp; tst -> sp;
  note [shape=note, style=filled, fillcolor="{C['white']}", fontsize=8.5,
        label="Environments communicate only through Parquet artifacts.\\nTensorFlow is never imported in env core;\\na generator whose modules are missing is skipped\\nwith a hint, not an error (run_in_env in Colab)."];
"""
    render("fig03_environments", body)


# ---------------------------------------------------------------------------------------------
# 4. Data preprocessing
# ---------------------------------------------------------------------------------------------
def fig04():
    body = f"""
  node [fillcolor="{C['data']}"];
  src [shape=folder, style=filled, label="9 public datasets\\nETTh1 · Electricity · Household · PJM · Beijing PM2.5\\nJena · Metro · Bike · Bitcoin\\n(CSV / TXT; 1 min – 1 h)"];
  raw [label=<<b>raw</b><br/>lossless CSV → Parquet (float64, all columns);<br/>original removed only after row-count check>];
  hr  [label=<<b>Univariate hourly series</b><br/>hourly mean (Electricity, Household, Jena) ·<br/>last log-price (Bitcoin) · as is (others)>];
  gap [label=<<b>Gaps</b><br/>interpolate ≤ 6 h; longer stay NaN<br/>(windows with NaN are dropped)>];
  cut [label=<<b>Length</b><br/>last max_points points<br/>(min: 10 000; max: full series)>];
  spl [label=<<b>Temporal split with embargo 168 h</b><br/>train | val | OOT = 50/25/25 (min) · 60/20/20 (max)>];
  sc  [label=<<b>Fit on train only</b><br/>min–max scaler lo, hi · T = 168 · K = round(n_train / T)<br/>N = max(300, 2K) · stride s ≈ (n_train − T)/5000<br/>task thresholds (target_params.json)>, fillcolor="{C['white']}", color="{C['accent']}", penwidth=1.3];
  ch  [label=<<b>Channels</b> (L, 3) in [0, 1]<br/>0: (x − lo)/(hi − lo)<br/>1, 2: (sin + 1)/2, (cos + 1)/2 of hour-of-week (168)>];
  win [label=<<b>Windows</b> (n, T, 3), stride s<br/>train core | embargo (168 rows) | holdout (last 10%)>];

  src -> raw -> hr -> gap -> cut -> spl -> sc -> ch -> win;

  node [fillcolor="{C['white']}", fontsize=8.5];
  u1 [label="generator training\\n(core windows)", fillcolor="{C['gen']}"];
  u2 [label="early stopping\\n(holdout windows)", fillcolor="{C['gen']}"];
  u3 [label="reference statistics\\n(full train)", fillcolor="{C['stitch']}"];
  u4 [label="fidelity references\\n(val primary · train, OOT;\\nreal units)", fillcolor="{C['eval']}"];
  u5 [label="utility test rows\\n(val, OOT)", fillcolor="{C['ml']}"];
  win -> u1; win -> u2; ch -> u3; spl -> u4 [label=" val, train, OOT"]; spl -> u5 [label=" val, OOT", minlen=2];
  meta [shape=note, style=filled, fillcolor="{C['store']}", label="<ds>.meta.parquet\\nlo, hi, T, K, N, s, boundaries,\\ndata_key = hash(split, max_points, T)"];
  sc -> meta [style=dashed, color="{C['muted']}"];
"""
    render("fig04_data_preprocessing", body)


# ---------------------------------------------------------------------------------------------
# 5. Temporal split timeline (matplotlib)
# ---------------------------------------------------------------------------------------------
def fig05():
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle

    plt.rcParams.update({"pdf.fonttype": 42, "ps.fonttype": 42, "font.family": "sans-serif",
                         "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"], "font.size": 8})
    # profile min: n = 9 664, train = 5 000, val = OOT = 2 332, embargo 168 between parts
    n_tr, emb, n_val, n_oot = 5000, 168, 2332, 2332
    hold, emb_in = 500, 168          # holdout = last 10% of train; embargo of 168 rows (Config.embargo) before it
    core = n_tr - hold - emb_in
    end = n_tr + 2 * emb + n_val + n_oot
    fig, ax = plt.subplots(figsize=(7.0, 2.7))
    y1, y2, hgt = 1.15, 0.35, 0.42

    def seg(a, w, y, color, text="", hatch=None):
        ax.add_patch(Rectangle((a, y), w, hgt, fc=color, ec=C["edge"], lw=0.6, hatch=hatch))
        if text:
            ax.text(a + w / 2, y + hgt / 2, text, ha="center", va="center")

    seg(0, n_tr, y1, C["data"], "train  (50%)")
    seg(n_tr, emb, y1, "white", hatch="/////")
    seg(n_tr + emb, n_val, y1, C["ml"], "val  (25%)")
    seg(n_tr + emb + n_val, emb, y1, "white", hatch="/////")
    seg(n_tr + 2 * emb + n_val, n_oot, y1, C["ml"], "OOT  (25%)")

    seg(0, core, y2, C["gen"], "core — generator training windows")
    seg(core, emb_in, y2, "white", hatch="/////")
    seg(core + emb_in, hold, y2, C["gen"])
    # train row zoom guides
    for xa, xb in ((0, 0), (n_tr, core + emb_in + hold)):
        ax.plot([xa, xb], [y1, y2 + hgt], lw=0.5, ls=":", color=C["muted"])

    kw = dict(fontsize=7.2, color="#333333")
    ax.annotate("holdout (last 10%):\nearly stopping", xy=(core + emb_in + hold / 2, y2), xytext=(n_tr + 420, y2 - 0.12),
                ha="left", va="top", arrowprops=dict(arrowstyle="-", lw=0.5, color=C["muted"]), **kw)
    ax.annotate("embargo (168)", xy=(core + emb_in / 2, y2), xytext=(core - 900, y2 - 0.12), ha="center", va="top",
                arrowprops=dict(arrowstyle="-", lw=0.5, color=C["muted"]), **kw)
    for xc in (n_tr + emb / 2, n_tr + emb + n_val + emb / 2):
        ax.text(xc, y1 - 0.05, "embargo\n168 h", ha="center", va="top", **kw)

    uses = [
        (n_tr / 2, "scaler lo/hi · T, K, N · task thresholds\nreference statistics · TRTR training · fidelity '@train'"),
        (n_tr + emb + n_val / 2, "fidelity reference (primary)\nutility test (val)"),
        (n_tr + 2 * emb + n_val + n_oot / 2, "utility test (OOT) · fidelity '@oot'\n'real' ceiling (RQ0)"),
    ]
    for xc, t in uses:
        ax.text(xc, y1 + hgt + 0.08, t, ha="center", va="bottom", **kw)
    ax.text(-60, y1 + hgt / 2, "split", ha="right", va="center", fontweight="bold")
    ax.text(-60, y2 + hgt / 2, "inside\ntrain", ha="right", va="center", fontweight="bold")
    ax.annotate("", xy=(end, 0.0), xytext=(0, 0.0), arrowprops=dict(arrowstyle="->", lw=0.7, color=C["edge"]))
    ax.text(end, -0.06, "time (hours)", ha="right", va="top", **kw)
    ax.text(0, -0.06, "profile min: n = 9 664 hourly points, train 5 000, val = OOT = 2 332 (to scale)",
            ha="left", va="top", fontsize=7.2, color=C["muted"])
    ax.set_xlim(-700, end + 30)
    ax.set_ylim(-0.3, 2.15)
    ax.axis("off")
    fig.tight_layout(pad=0.1)
    fig.savefig(OUT / "fig05_temporal_split.pdf")
    fig.savefig(OUT / "fig05_temporal_split.svg")
    plt.close(fig)


# ---------------------------------------------------------------------------------------------
# 6. Pool generator: beta-VAE
# ---------------------------------------------------------------------------------------------
def fig06():
    body = f"""
  node [fillcolor="{C['gen']}"];
  xc [label="train core windows\\n(n ≤ 5000, T, 3)", fillcolor="{C['data']}"];
  xh [label="holdout windows\\n(last 10% of train)", fillcolor="{C['data']}"];
  subgraph cluster_vae {{ label=<<b>β-VAE</b>  (tsgm vae_conv5 + BetaVAE)>; style="rounded,filled"; fillcolor="#FDF0E4"; color="{C['edge']}";
    enc [label="Conv encoder\\n→ μ, log σ²  (latent 16)"];
    z   [label="z = μ + σ·ε", shape=ellipse];
    dec [label="Conv decoder\\n→ (T, 3)"];
    loss [label="loss = reconstruction + β·KL\\nβ = 2 · Adam 1e-3 · batch 64", shape=box, style="rounded,dashed", fillcolor="{C['white']}"];
    enc -> z -> dec; dec -> loss [style=dashed]; enc -> loss [style=dashed];
  }}
  es [label=<<b>Early stopping</b> after every epoch<br/>holdout loss with z = μ<br/>epochs 1–150 ignored (min_epochs)<br/>patience 50 · ≤ 400 epochs · keep best weights>, fillcolor="{C['white']}"];
  w  [shape=cylinder, style=filled, fillcolor="{C['store']}", label="generators/<ds>/tsgm_vae/\\nreplica<r> (min) · seed<k> (mid, max)"];
  smp [label=<<b>Sampling</b> (per seed)<br/>z ~ 0.5 · N(0, I) → decoder<br/>NaN → 0.5, clip to [0, 1]>];
  pool [shape=cylinder, style=filled, fillcolor="{C['store']}", label="pool (N, T, 3)\\nN = max(300, 2K)\\npools/<ds>/tsgm_vae/seed<k>"];
  use [label="all same-pool methods\\n(14 in min)", fillcolor="{C['stitch']}"];

  xc -> enc [label=" fit"];
  xh -> es; loss -> es [style=dashed];
  es -> w [label=" best weights"];
  w -> smp -> pool -> use;

  rep [shape=note, style=filled, fillcolor="{C['white']}", fontsize=8.5,
       label="Model sharing across seeds (pool_train_replicas)\\nmin: 1 model / dataset   mid, max: 1 model per seed. Seeds always change sampling.\\nFit and sampling have separate fingerprints:\\nnew N re-samples without re-training."];
  w -> rep [style=dotted, arrowhead=none, color="{C['muted']}"];
"""
    render("fig06_pool_generator_vae", body)


# ---------------------------------------------------------------------------------------------
# 8. Method family (17 methods in mid)
# ---------------------------------------------------------------------------------------------
def fig08():
    def tbl(title, rows, fill, note=""):
        tr = "".join(f'<TR><TD ALIGN="LEFT" BGCOLOR="{bg or fill}">{a}</TD><TD ALIGN="LEFT" BGCOLOR="{bg or fill}">'
                     f'<FONT POINT-SIZE="8.5">{b}</FONT></TD></TR>' for a, b, bg in rows)
        nt = f'<TR><TD COLSPAN="2" ALIGN="LEFT" BALIGN="LEFT"><FONT POINT-SIZE="8" COLOR="{C["muted"]}">{note}</FONT></TD></TR>' if note else ""
        return (f'<<TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0" CELLPADDING="3" COLOR="{C["edge"]}" BGCOLOR="{C["white"]}">'
                f'<TR><TD COLSPAN="2" ALIGN="LEFT"><B>{title}</B></TD></TR>{tr}{nt}</TABLE>>')

    hl = "#F3D27A"
    a_rows = [
        ("<B>vae_zseries</B>", "<B>zseries: proprietary method of zypl.ai (under development),<BR ALIGN=\"LEFT\"/>case study (published results)</B><BR ALIGN=\"LEFT\"/>", hl),
        ("vae_rand", "K random windows, random order (control)", None),
        ("vae_rand_b", "second random order, noise estimate (mid, max)", None),
        ("vae_greedy", "nearest neighbour by the jump at the seam", None),
        ("vae_atsp", "asymmetric TSP over pool (LKH), cheapest K-run", None),
        ("vae_pctsp", "prize-collecting TSP (OR-Tools)", None),
        ("vae_mbb", "matched-block bootstrap, Gaussian kernel of the jump", None),
        ("vae_knn", "k-NN resampling, weights ∝ 1/rank, k = √N", None),
        ("vae_quilting", "image quilting: choice by overlap error + min-error cut", None),
        ("vae_herding", "kernel herding to train windows (MMD)", None),
    ]
    b_rows = [
        ("crossfade", "Hann-window blend of the overlap", None),
        ("wsola", "shift ≤ 12 to best correlation, then blend", None),
        ("quilt", "cut at minimum-difference point", None),
    ]
    c_rows = [
        ("diffusion_ts", "Diffusion-TS, autoregressive infill (context T/2)", None),
        ("chronos", "Chronos-T5-small, zero-shot, context 512", None),
        ("timesfm", "TimesFM 3.0, zero-shot median forecast, all train", None),
        ("timestral", "Timestral 209M, zero-shot median forecast, all train", None),
    ]
    body = f"""
  nodesep=0.35; ranksep=0.45;
  node [shape=plaintext, style="", margin=0];
  pool [shape=cylinder, style=filled, fillcolor="{C['store']}", margin="0.1,0.05",
        label="pool of N VAE windows\\n(shared per dataset × seed)"];
  trn  [shape=box, style="rounded,filled", fillcolor="{C['data']}", margin="0.1,0.05", label="real train"];
  A [label={tbl("A · Selection and order (same pool) — 10 methods", a_rows, C['stitch'])}];
  B [label={tbl("B · Seam joiners on the vae_zseries path — 3 methods", b_rows, C['stitch'],
                "overlap 12 points; vae_zseries_{xfade,wsola,quilt}: published results;<br/>max: over every assembler but random and vae_quilting")}];
  Cc [label={tbl("C · Long-series generators (no pool) — 4 methods", c_rows, C['gen'])}];
  R [label={tbl("Reference (not a method)", [("real", "OOT series (fidelity ceiling); real-train model (TRTR)", None)], C['ml'])}];
  out [shape=box, style="rounded,filled", fillcolor="{C['white']}", penwidth=1.2, margin="0.12,0.06",
       label="17 methods (min: 16, without vae_rand_b; 4 of them published results) × 10 seeds × 9 datasets\\n→ one series per unit, length K·T; real units + hour-of-week, window / piece id, seam flag"];
  pool -> A; A -> B [label=" path of vae_zseries"];
  trn -> Cc [label=" fit / context"];
  {{rank=same; pool; trn}}
  {{rank=same; A; Cc}}
  A -> out; B -> out; Cc -> out;
  R -> out [style=invis];
  Cc -> R [style=invis];
"""
    render("fig08_method_family", body)


# ---------------------------------------------------------------------------------------------
# 9. Long-series generators
# ---------------------------------------------------------------------------------------------
def fig09():
    body = f"""
  node [fillcolor="{C['gen']}"];
  subgraph cluster_d {{ label=<<b>Diffusion-TS</b> (official code, Config/etth.yaml with window T)>; style="rounded,filled"; fillcolor="#FDF0E4"; color="{C['edge']}";
    dtr [label=<<b>Fit</b> on train core windows (T, 3)<br/>official recipe: warm-up + plateau lr, batch 128 × 2, EMA<br/>early stopping on holdout<br/>min/mid: one model per dataset; max: per seed>];
    d0  [label=<<b>Window 1</b>: calendar channels imposed<br/>(hour-of-week from a random start per seed),<br/>value channel sampled by infill (DDIM, 50 steps)>];
    d1  [label=<<b>Window m + 1</b>: first c = T/2 values = last c of the series<br/>(known), calendar continues; infill the remaining T/2>];
    dl  [label="length ≥ K·T ?", shape=diamond, style=filled, fillcolor="{C['white']}"];
    dtr -> d0 -> d1 -> dl; dl -> d1 [label=" no: append T/2"];
  }}
  subgraph cluster_c {{ label=<<b>Chronos</b> (amazon/chronos-t5-small; max: t5-base, zero-shot)>; style="rounded,filled"; fillcolor="#FDF0E4"; color="{C['edge']}";
    cld [label=<<b>Load</b> once per process<br/>(load time recorded as fit_wall_s)>];
    c0  [label=<<b>Context</b>: last 512 train values (real units)>];
    c1  [label=<<b>Sample</b> next 64 points (1 sample path)<br/>append; context = last 512 points>];
    cl  [label="length ≥ K·T ?", shape=diamond, style=filled, fillcolor="{C['white']}"];
    cld -> c0 -> c1 -> cl; cl -> c1 [label=" no"];
  }}
  subgraph cluster_f {{ label=<<b>TimesFM 3.0 · Timestral 209M</b> (zero-shot, package defaults)>; style="rounded,filled"; fillcolor="#FDF0E4"; color="{C['edge']}";
    f0  [label=<<b>Context</b>: the whole train split<br/>(limits 15 360 / 32 768 steps)>];
    f1  [label=<<b>Median forecast</b> of K·T steps<br/>TimesFM: one pass · Timestral: blocks of 1024, median fed back<br/>no sampling: the same series on every seed>];
    f0 -> f1;
  }}
  out [label="series K·T (truncated)\\nchunk boundaries = seams for F5 metrics", fillcolor="{C['white']}"];
  dl -> out [label=" yes"]; cl -> out [label=" yes"]; f1 -> out;
  note [shape=note, style=filled, fillcolor="{C['white']}", fontsize=8.5,
        label="Chronos, TimesFM, Timestral: calendar continues from the end of train.\\nDiffusion-TS and VAE: calendar is part of the window\\n(generated by VAE, imposed for Diffusion-TS)."];
  cl -> note [style=invis];
"""
    render("fig09_long_generators", body)


# ---------------------------------------------------------------------------------------------
# 10. Utility (downstream ML) pipeline
# ---------------------------------------------------------------------------------------------
def fig10():
    body = f"""
  node [fillcolor="{C['ml']}"];
  rtr [label="real train\\n(values, hour-of-week)", fillcolor="{C['data']}"];
  syn [label="synthetic series of method m\\n(K·T, real units)", fillcolor="{C['stitch']}"];
  rte [label="real val and OOT", fillcolor="{C['data']}"];
  thr [label=<<b>Task parameters</b> (frozen, from train)<br/>target_params.json: quantile thresholds>, fillcolor="{C['white']}", color="{C['accent']}", penwidth=1.3];

  subgraph cluster_fe {{ label=<<b>make_xy</b> — computed on each series separately (no lags across series)>; style="rounded,filled"; fillcolor="{C['white']}"; color="{C['edge']}";
    fr [label="features: x_t, x_t − x_{{t−l}}, l ∈ {{1,2,3,6,12,24,48,168}},\\nsin/cos hour-of-week  (11 features)"];
    lb [label="labels: 14 tasks (U2.1–U2.9)\\nclf · mc · reg · qreg · ms · vol"];
  }}
  rtr -> fr; syn -> fr; rte -> fr; thr -> lb;

  subgraph cluster_r {{ label=<<b>Regime R — TRTR</b> (pseudo-method real, once per seed)>; style="rounded,filled"; fillcolor="{C['white']}"; color="{C['edge']}";
    mr [label="fit on real train"]; }}
  subgraph cluster_s {{ label=<<b>Regime S — TSTR</b> (every method, every seed)>; style="rounded,filled"; fillcolor="{C['white']}"; color="{C['edge']}";
    ms [label="fit on synthetic only"]; }}
  lb -> mr; lb -> ms; fr -> mr; fr -> ms;

  mdl [label=<<b>Models</b> (fixed configs, model_configs.json)<br/>linear (PyTorch, L-BFGS / ridge) · MLP 64→32 (PyTorch)<br/>GBDT (XGBoost); standardisation fitted on own training set>, fillcolor="{C['white']}"];
  mdl -> mr [style=dashed]; mdl -> ms [style=dashed];

  pc [label=<<b>Prior correction</b> (clf, mc): class probabilities<br/>P(c|x) ∝ P<sub>balanced</sub>(c|x) · share<sub>train</sub>(c)>];
  ev [label=<<b>Predict on the same real test rows</b><br/>val and OOT>];
  mr -> ev; ms -> ev; rte -> ev [style=dashed, label=" X, y"]; ev -> pc;
  met [label=<<b>Metrics</b><br/>binary: AUC, PR AUC, Brier, log-loss, ECE, F1, lift<br/>multiclass: macro AUC, log-loss, macro F1<br/>regression: MAE, RMSE, MASE, sMAPE, extremes<br/>quantile: pinball, coverage, crossings · multistep: MASE>];
  pc -> met;
  o1 [shape=cylinder, style=filled, fillcolor="{C['store']}", label="utility/<ds>/<m>/seed<k>/\\nmetrics · predictions · models"];
  met -> o1;
  tr [label=<<b>Comparison</b> (hypothesis tests): TSTR(m) vs TRTR, TSTR(m) vs TSTR(m′)<br/>transfer ratio, row-level block bootstrap on predictions>, fillcolor="{C['stats']}"];
  o1 -> tr;
"""
    render("fig10_utility_pipeline", body)


# ---------------------------------------------------------------------------------------------
# 11. Tasks × models grid
# ---------------------------------------------------------------------------------------------
def fig11():
    rows = [
        ("U2.1", "clf_up_h24_q90", "clf", "24", "Δ<sub>24</sub> &gt; q<sub>0.90</sub> (case-study task)", "P(y=1)"),
        ("U2.2", "clf_up_h{1,6,168}_q90", "clf", "1, 6, 168", "other horizons", "P(y=1)"),
        ("U2.3", "clf_up_h24_q{95,99}", "clf", "24", "rare events", "P(y=1)"),
        ("U2.4", "clf_down_h24_q10", "clf", "24", "Δ<sub>24</sub> &lt; q<sub>0.10</sub>", "P(y=1)"),
        ("U2.5", "mc3_h24", "mc", "24", "down / neutral / up", "3 probs"),
        ("U2.6", "reg_h{1,24,168}", "reg", "1, 24, 168", "value x<sub>t+h</sub>", "scalar"),
        ("U2.7", "qreg_h24", "qreg", "24", "quantiles 0.1, 0.5, 0.9", "3 values"),
        ("U2.8", "ms_h24", "ms", "1…24", "path x<sub>t+1:t+24</sub>", "24 values"),
        ("U2.9", "vol_h24", "vol", "24", "std of next 24 changes", "scalar"),
    ]
    cell = lambda t, b=False, bg=None, al="LEFT": (f'<TD ALIGN="{al}"' + (f' BGCOLOR="{bg}"' if bg else "") + ">"
                                                     + (f"<B>{t}</B>" if b else t) + "</TD>")
    hdr = "".join(cell(h, True, C["store"]) for h in
                  ["ID", "task name(s)", "kind", "h (hours)", "target", "model output", "linear", "MLP", "GBDT"])
    body_rows = []
    for i, (id_, nm, kind, h, tgt, out) in enumerate(rows):
        bg = C["ml"] if i == 0 else None
        mlp = "✓" if i == 0 else "✓ (max)"
        gb = "✓"
        body_rows.append("<TR>" + "".join([cell(id_, i == 0, bg), cell(nm, False, bg), cell(kind, False, bg),
                                            cell(h, False, bg), cell(tgt, False, bg), cell(out, False, bg),
                                            cell("✓", False, bg, "CENTER"), cell(mlp, False, bg, "CENTER"),
                                            cell(gb, False, bg, "CENTER")]) + "</TR>")
    table = (f'<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4" COLOR="{C["edge"]}">'
             f"<TR>{hdr}</TR>{''.join(body_rows)}"
             f'<TR><TD COLSPAN="9" ALIGN="LEFT"><FONT POINT-SIZE="8">14 tasks in total; all share one feature set '
             f"(11 features). Labels are computed on each series with thresholds frozen on real train. "
             f"MLP runs on U2.1 only in profiles min/mid and on all tasks in max.<BR ALIGN=\"LEFT\"/>"
             f"Every (task, model) is fitted in regime S (TSTR) and R (TRTR) and evaluated on real val and OOT."
             f"</FONT></TD></TR></TABLE>>")
    render("fig11_tasks_models", f'  t [shape=plaintext, style="", label={table}];')


# ---------------------------------------------------------------------------------------------
# 12. Fidelity evaluation
# ---------------------------------------------------------------------------------------------
def fig12():
    groups = [
        ("F1", "Marginal", "KS, W1, Anderson–Darling, QQ corr., quantiles, moments, out-of-range, coverage, JS, Hill tail"),
        ("F2", "Increments", "Δ_k distributions (k = 1, 6, 24, h, 168), volatility ratio, up-share, large jumps"),
        ("F3", "Temporal dependence", "ACF lags &lt; T, ACF lags T…3T, PACF, ACF of |Δ| and Δ², spectrum, peaks, Hurst/DFA"),
        ("F4", "Seasonality, calendar", "hour-of-week and hour-of-day mean/std profiles, calendar continuity"),
        ("F5", "Seams", "jump z-scores, seams vs interior, local ACF, change points (PELT), seam detectability AUC"),
        ("F6", "Window distribution", "GRU discriminator, C2ST on window features, predictive score, MMD, feature-FID, NN distance"),
        ("F7", "Long structure", "rolling mean/std, level crossings, excursions, drawdowns, trend, HMM regimes"),
        ("F8", "Target", "class-share TVD, event durations, inter-event times, hour profile, conditionals"),
        ("F9", "Diversity, coverage", "precision / recall, density / coverage on window embeddings"),
        ("F10", "Memorisation", "distance to closest train record vs holdout, near-copy share (once, vs train)"),
        ("F11", "Class balance", "class shares of every classification task (relative error), rare events, multiclass TVD, lost minority"),
        ("F12", "Extremes, outliers", "exceedances of real 0.5 / 99.5% (rate, size), local spikes, weekly block maxima / minima"),
    ]
    tr = "".join(f'<TR><TD ALIGN="LEFT"><B>{a}</B></TD><TD ALIGN="LEFT"><B>{b}</B></TD>'
                 f'<TD ALIGN="LEFT"><FONT POINT-SIZE="8.5">{c}</FONT></TD></TR>' for a, b, c in groups)
    table = (f'<<TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="3" COLOR="{C["edge"]}" BGCOLOR="{C["eval"]}">'
             f'<TR><TD COLSPAN="3" ALIGN="LEFT" BGCOLOR="{C["store"]}"><B>12 registered metric groups, 83 metrics × 3 references</B>'
             f'</TD></TR>{tr}</TABLE>>')
    body = f"""
  rankdir=LR; nodesep=0.18; ranksep=0.4;
  subgraph cluster_in {{ label=<<b>Series under test</b>>; style="rounded"; color="{C['edge']}";
    s  [label="method m, seed k\\n(length K·T)", fillcolor="{C['stitch']}"];
    sl [label="m@len: first len(OOT) points\\n(seed 0; equal-length ceiling)", fillcolor="{C['stitch']}"];
    re [label="real: OOT series\\n(seed 0; ceiling, RQ0;\\nnot scored against OOT)", fillcolor="{C['ml']}"];
  }}
  subgraph cluster_ref {{ label=<<b>Real references</b>>; style="rounded"; color="{C['edge']}";
    rv [label="val — primary reference\\n(no suffix)", fillcolor="{C['data']}", penwidth=1.3];
    rt [label="train — '@train'\\n(fit to training data)", fillcolor="{C['data']}"];
    ro [label="OOT — '@oot'\\n(generalisation under drift)", fillcolor="{C['data']}"];
  }}
  f [label=<<b>fidelity(series, reference)</b><br/><font point-size="8.5">same code for every method;<br/>pairwise distances, GRU in torch (GPU)</font>>, fillcolor="{C['white']}"];
  g [shape=plaintext, style="", margin=0, label={table}];
  o [shape=cylinder, style=filled, fillcolor="{C['store']}", label="fidelity/<ds>/<m>/seed<k>\\none row per unit\\n+ ORIENT (orientation)"];
  s -> f; sl -> f; re -> f; rv -> f; rt -> f; ro -> f;
  f -> g -> o;
"""
    render("fig12_fidelity_evaluation", body)


# ---------------------------------------------------------------------------------------------
# 13. Statistical analysis pipeline
# ---------------------------------------------------------------------------------------------
def fig13():
    body = f"""
  node [fillcolor="{C['stats']}"];
  t1 [shape=cylinder, style=filled, fillcolor="{C['store']}", label="tables/\\ntiming · fidelity · utility"];
  t2 [shape=cylinder, style=filled, fillcolor="{C['store']}", label="utility predictions\\n+ real labels"];
  lg [label=<<b>Long format</b>: (dataset, seed, unit, method, value)<br/>unit = metric @ reference (train · val · OOT)<br/>or task × model × regime × split × metric>];
  t1 -> lg;

  subgraph cluster_rank {{ label=<<b>Ranking</b> (RQ1)>; style="rounded,filled"; fillcolor="{C['white']}"; color="{C['edge']}";
    rk [label=<rank methods per (dataset, seed) in every leaf<br/>leaf → group → criterion × slice → domain → ranking<br/>(equal weights per level; thematic slices; domain ranks)<br/>4 rankings: fidelity val+OOT | train × utility clf | reg<br/>privacy, cost separately; + cost as third domain, Pareto>];
    ru [label=<two-level bootstrap of ranks: CI, P(first), P(top 3)<br/>Friedman · each method vs the best: Wilcoxon, Holm (tier)<br/>Kendall τ between slices · Dirichlet weights · noise-pair check>];
    rk -> ru;
  }}
  subgraph cluster_pair {{ label=<<b>Paired comparisons</b> A vs B (RQ0a, RQ2, RQ3, RQ5a, RQ8b, RQ9b)>; style="rounded,filled"; fillcolor="{C['white']}"; color="{C['edge']}";
    nz [label=<<b>Noise</b> = smallest effect of interest (per dataset, unit)<br/>same pool: median |vae_rand − vae_rand_b| (min: |vae_rand(k) − vae_rand(k+1)|)<br/>independently trained A: median |A(k) − A(k+1)|>];
    pd [label=<d = orientation · (A − B) on matching seeds; d &gt; 0 ⇔ A better<br/>B: a method, the assembly median, or a contrast<br/>(selection, seam processing)>];
    ds [label=<per dataset (10 seeds): two one-sided Wilcoxon (α/2),<br/>TOST (± noise), Hodges–Lehmann>];
    gl [label=<global (9 datasets): d / noise → Wilcoxon · sign · t-test<br/>TOST ±1 · two-level bootstrap CI; BH within question>];
    vd [label=<<b>Verdict</b>: better · worse · same · inconclusive>, fillcolor="{C['white']}", penwidth=1.3];
    nz -> pd; pd -> ds -> vd; pd -> gl -> vd;
  }}
  co [label=<<b>Associations</b> (RQ0c–d, RQ4, RQ7, RQ8c, RQ9c)<br/>Friedman per metric (discriminative?) · Spearman ρ within a dataset<br/>across methods (metric ↔ metric, fidelity ↔ utility, descriptor ↔ effect)<br/>→ median ρ, Wilcoxon over datasets, BH>];
  lg -> rk; lg -> nz; lg -> co;
  cf [label=<<b>Confirmatory family C1–C4</b> (pre-specified, joint Holm)<br/>cells: U2.1 AUC and U2.6 (h = 24) MASE · TSTR · linear · OOT<br/>C1 methods differ · C2 Diffusion-TS, Chronos vs assembly median<br/>C3 selection main effect · C4 seam-processing main effect>, fillcolor="{C['white']}", color="{C['accent']}", penwidth=1.3];
  vd -> cf [style=dashed]; lg -> cf [style=dashed];
  cs [label=<<b>Case study</b> CS1–CS15: one method (--case-method) vs its controls,<br/>alternatives and long-series generators; row-level tests: predictions<br/>averaged over seeds, ΔAUC on identical rows, block bootstrap by week>];
  t2 -> cs; vd -> cs [style=dotted, arrowhead=none];
  out [shape=note, style=filled, fillcolor="{C['store']}", label="reports/: OVERALL.md, LEADERBOARD.md,\\nMETRIC_VALUES.md, REPORT.md\\ntables: overall/, leaderboard/, metric_values/,\\nhypotheses/RQ*, CS*, confirmatory.parquet"];
  ru -> out; cf -> out; co -> out; cs -> out;
"""
    render("fig13_statistical_pipeline", body)


# ---------------------------------------------------------------------------------------------
# 14. Map of the research questions
# ---------------------------------------------------------------------------------------------
def fig14():
    U, O, M = C["ml"], C["store"], C["white"]
    rows = [
        ("RQ0", "benchmark validity: noise, real-data ceiling, which metrics discriminate, redundancy",
         "all F (3 references), TSTR", "rand vs rand_b (mid, max); real; Friedman", M, ""),
        ("RQ1", "<B>ranking of every method in every slice</B>", "all leaves: F × reference, U × split, cost",
         "all methods", M, "leaderboard"),
        ("RQ2", "assembly from a window pool vs generators of long series", "F (val, OOT), TSTR all tasks",
         "long gen. vs rand, assembly median", M, ""),
        ("RQ3", "inside assembly: window selection × seam processing", "F (val, OOT), TSTR all tasks",
         "vs random path; seam-processing contrasts", M, ""),
        ("RQ4", "does fidelity predict utility (which metrics, which reference)", "F (3 references) ↔ transfer ratio",
         "Spearman across methods", M, ""),
        ("RQ5", "gap to real data; stability over time and model class; decision transfer", "TSTR / TRTR, U6",
         "real (TRTR); Kendall τ", U, "(c) max only"),
        ("RQ6", "speed and cost: training, generation, memory; quality–time Pareto", "time, memory",
         "all methods", O, ""),
        ("RQ7", "moderators: dataset properties and family differences", "dataset descriptors", "effects of RQ2, RQ3", O, "explor."),
        ("RQ8", "class balance: shares of every classification task, rare events", "F8.1, F11; TSTR ECE",
         "vs random path; long gen. vs assembly median", M, ""),
        ("RQ9", "extremes: tails, outliers, block maxima / minima", "F1 tails, F2.4, F7.4, F12; extreme error, rare PR AUC",
         "vs random path; long gen. vs assembly median", M, ""),
        ("C1–C4", "<B>confirmatory: methods differ; long vs assembly; selection; seam processing</B>",
         "U2.1 AUC, U2.6 MASE (TSTR, linear, OOT)", "Friedman; assembly median; contrasts", U, "confirm."),
        ("CS1–CS15", "case study of one method (default vae_zseries) vs its controls and alternatives",
         "F (val), TSTR", "vae_rand, A, B, C", M, "secondary"),
    ]
    hdr = "".join(f'<TD BGCOLOR="{C["store"]}" ALIGN="LEFT"><B>{h}</B></TD>'
                  for h in ["id", "question", "evidence", "analysis / compared with", "note"])
    tr = ""
    for h, claim, ev, cmp_, col, note in rows:
        red = note.startswith("confirm")
        hcell = f'<FONT COLOR="{C["accent"]}"><B>{h}</B></FONT>' if red else f"<B>{h}</B>"
        ecol = col
        tr += (f'<TR><TD ALIGN="LEFT" BGCOLOR="{C["stats"]}">{hcell}</TD><TD ALIGN="LEFT">{claim}</TD>'
               f'<TD ALIGN="LEFT" BGCOLOR="{ecol}">{ev}</TD><TD ALIGN="LEFT">{cmp_}</TD>'
               + (f'<TD ALIGN="LEFT"><FONT POINT-SIZE="8">{note}</FONT></TD></TR>' if note else "<TD> </TD></TR>"))
    foot = ("Evidence colour: utility TSTR/TRTR (green), cost and descriptors (grey), "
            "fidelity and utility together (white). F = fidelity metric groups (Fig. 12); A, B, C = method groups of "
            "Fig. 8.<BR ALIGN=\"LEFT\"/>Confirmatory family: joint Holm over C1–C4 in both cells. Other questions: "
            "BH within a question; RQ7 exploratory. The case study is secondary.<BR ALIGN=\"LEFT\"/>")
    table = (f'<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="3" COLOR="{C["edge"]}">'
             f"<TR>{hdr}</TR>{tr}"
             f'<TR><TD COLSPAN="5" ALIGN="LEFT"><FONT POINT-SIZE="8">{foot}</FONT></TD></TR></TABLE>>')
    render("fig14_hypotheses_map", f'  t [shape=plaintext, style="", fontsize=9, label={table}];')


# ---------------------------------------------------------------------------------------------
# 15. Incremental recomputation (unit fingerprints)
# ---------------------------------------------------------------------------------------------
def fig15():
    k = lambda n, t: f'{n} [shape=plaintext, style="", fontsize=8, fontcolor="{C["muted"]}", label="{t}"];'
    body = f"""
  rankdir=LR; nodesep=0.18; ranksep=0.42;
  node [fontsize=9];
  dk  [label="processed data\\ndata_key: split, max_points, T", fillcolor="{C['data']}"];
  wl  [label="training windows\\nmax_windows, holdout_frac", fillcolor="{C['data']}"];
  tp  [label="target_params*.json", shape=note, style=filled, fillcolor="{C['store']}"];
  mc  [label="model_configs.json", shape=note, style=filled, fillcolor="{C['store']}"];
  gf  [label="pool generator fit\\n(VAE weights)", fillcolor="{C['gen']}"];
  gs  [label="pool sample\\npool_size, pool_mult", fillcolor="{C['gen']}"];
  df  [label="Diffusion-TS fit", fillcolor="{C['gen']}"];
  ch  [label="pretrained load\\n(Chronos, TimesFM, Timestral)", fillcolor="{C['gen']}"];
  sr  [label="series of method m\\n+ assembler/joiner settings\\n(e.g. knn_k, mbb_*, join_overlap)", fillcolor="{C['stitch']}"];
  fi  [label="fidelity unit\\n+ fidelity_*, disc_epochs", fillcolor="{C['eval']}"];
  lb  [label="labels", fillcolor="{C['ml']}"];
  ut  [label="utility unit (TSTR)\\n+ tasks, models, hpo", fillcolor="{C['ml']}"];
  tr  [label="TRTR (real)", fillcolor="{C['ml']}"];
  dk -> wl -> gf -> gs -> sr; wl -> df -> sr; dk -> ch -> sr;
  sr -> fi; tp -> fi; tp -> lb; dk -> lb;
  sr -> ut; lb -> ut; mc -> ut; lb -> tr; mc -> tr;
  note [shape=note, style=filled, fillcolor="{C['white']}", fontsize=8.5,
        label="unit_fp = hash(processed data, own settings,\\nrelevant JSON files, upstream unit_fp).\\nA unit is skipped if its files exist with the same unit_fp;\\nfidelity and utility: per cell (cells.json).\\nExample: changing knn_k recomputes vae_knn series\\nand their fidelity/utility; pools, VAE, other methods,\\nlabels, TRTR and real fidelity are kept."];
"""
    render("fig15_incremental_recompute", body)


# ---------------------------------------------------------------------------------------------
# 16. Artifact layout
# ---------------------------------------------------------------------------------------------
def fig16():
    rows = [
        ("artifacts/&lt;profile&gt;/", "", True),
        ("├── pools/&lt;ds&gt;/&lt;gen&gt;/seed&lt;k&gt;.parquet", "pool windows (N, T, 3) + record", False),
        ("├── generators/&lt;ds&gt;/&lt;gen&gt;/…parquet", "generator weights (VAE, Diffusion-TS, SDV)", False),
        ("├── series/&lt;ds&gt;/&lt;method&gt;/seed&lt;k&gt;.parquet", "t, value, how, window, piece, seam", False),
        ("├── records/&lt;ds&gt;/&lt;method&gt;/seed&lt;k&gt;.parquet", "time, memory, hardware, diagnostics", False),
        ("├── fidelity/&lt;ds&gt;/&lt;method&gt;/seed&lt;k&gt;.parquet", "all F-metrics (+ .cells.json)", False),
        ("├── labels/&lt;ds&gt;/&lt;task&gt;.parquet", "real test labels: split, row, y", False),
        ("├── utility/&lt;ds&gt;/&lt;method&gt;/seed&lt;k&gt;/", "", False),
        ("│   ├── cells.json", "done cells with their fingerprints", False),
        ("│   ├── metrics.parquet", "U-metrics per task × model × regime × split", False),
        ("│   ├── predictions.parquet", "every prediction (scalar or vector)", False),
        ("│   └── models.parquet", "weights of every fitted model", False),
        ("├── tables/", "timing, fidelity, utility, pools, cross_seed,", False),
        ("│", "datasets, inventory, hardware, config.json", False),
        ("├── reports/", "Markdown reports of the analysis:", False),
        ("│   ├── REPORT.md", "RQ0–RQ9, C1–C4, case study CS1–CS15", False),
        ("│   ├── OVERALL.md", "overall leaderboard, robustness checks", False),
        ("│   ├── LEADERBOARD.md", "ranks of every method per slice", False),
        ("│   └── METRIC_VALUES.md", "metric values by reference, dataset, task, model, split", False),
        ("├── overall/", "overall leaderboard tables, robustness checks", False),
        ("├── leaderboard/", "rankings.parquet, ranks per slice, tests, stability", False),
        ("├── metric_values/", "fidelity, utility: median and IQR over seeds", False),
        ("├── hypotheses/", "RQ*, CS* global / per dataset, confirmatory", False),
        ("└── errors.log", "failed units (run continues)", False),
    ]
    tr = "".join(
        f'<TR><TD ALIGN="LEFT"><FONT FACE="Courier">{"<B>" + a + "</B>" if b else a}</FONT></TD>'
        + (f'<TD ALIGN="LEFT"><FONT COLOR="{C["muted"]}">{d}</FONT></TD></TR>' if d else '<TD></TD></TR>') for a, d, b in rows)
    table = (f'<<TABLE BORDER="1" COLOR="{C["edge"]}" CELLBORDER="0" CELLSPACING="0" CELLPADDING="2" '
             f'BGCOLOR="{C["white"]}">{tr}'
             f'<TR><TD COLSPAN="2" ALIGN="LEFT"><FONT POINT-SIZE="8">Parquet, zstd; float32 except series values '
             f"(float64). Every unit file carries its unit_fp.</FONT></TD></TR></TABLE>>")
    render("fig16_artifact_layout", f'  t [shape=plaintext, style="", fontsize=9, label={table}];')


# ---------------------------------------------------------------------------------------------
# 17. Profiles
# ---------------------------------------------------------------------------------------------
def fig17():
    rows = [
        ("methods", "16 (no vae_rand_b)", "17", "35: + seam processing of every assembler<br/>but random and vae_quilting"),
        ("pool size N", "max(300, 2K) = 300", "as min", "max(300, 2K)"),
        ("series length, split", "last 10 000 pts; 50/25/25", "as min", "full series; 60/20/20"),
        ("VAE trainings", "1 per dataset (9)", "1 per seed (90)", "1 per seed (90)"),
        ("Diffusion-TS trainings", "1 per dataset (9)", "1 per dataset (9)", "1 per seed (90)"),
        ("hyper-parameter search", "no", "no", "grid on tail of own train (TSTR: synthetic)"),
        ("Chronos", "t5-small", "t5-small", "t5-base"),
        ("MLP tasks", "U2.1 only", "U2.1 only", "all tasks"),
        ("MLP epochs", "30, no early stop", "as min", "≤ 200, early stop"),
        ("GBDT", "100 trees, depth 4, 64 bins", "as min", "200 trees, depth 6, 256 bins"),
        ("decision grid (RQ5 c)", "off", "off", "on"),
        ("seeds × datasets", "10 × 9", "10 × 9", "10 × 9"),
    ]
    hdr = "".join(f'<TD BGCOLOR="{C["store"]}"><B>{h}</B></TD>' for h in ["setting", "min (default)", "mid", "max"])
    tr = "".join("<TR>" + f'<TD ALIGN="LEFT"><B>{a}</B></TD>' + "".join(f'<TD ALIGN="LEFT" BALIGN="LEFT">{x}</TD>' for x in r)
                 + "</TR>" for a, *r in rows)
    table = (f'<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4" COLOR="{C["edge"]}">'
             f"<TR>{hdr}</TR>{tr}"
             f'<TR><TD COLSPAN="4" ALIGN="LEFT" BALIGN="LEFT"><FONT POINT-SIZE="8">Each profile writes to data/processed/&lt;profile&gt;/ '
             f"and artifacts/&lt;profile&gt;/; mid reuses min data. Method counts include 4 published results (vae_zseries and its<br/>"
             f"seam-processing variants), which are not generated: 1 080 generated series in min "
             f"(9 datasets × 10 seeds × 12 methods), 1 170 in mid (13), 2 790 in max (31 methods).</FONT></TD></TR></TABLE>>")
    render("fig17_profiles", f'  t [shape=plaintext, style="", fontsize=9, label={table}];')


# ---------------------------------------------------------------------------------------------
# 18. Extensibility
# ---------------------------------------------------------------------------------------------
def fig18():
    regs = [
        ("datasets", "load(cfg) → hourly pd.Series", "selectable by name", "data"),
        ("tasks", "fit(train) → params; labels(values, params)", "new utility task (all methods)", "data"),
        ("pool_generators", "fit, sample(n), state, load_state", "whole assembly suite on the new pool", "gen"),
        ("long_generators", "fit, generate, state, load_state", "new method, compared in RQ2 and ranked", "gen"),
        ("assemblers", "assemble(pool, ctx) → path, info", "&lt;prefix&gt;_&lt;name&gt; on every pool", "stitch"),
        ("joiners", "windows_needed; join(W, L) → X, seams, src", "&lt;prefix&gt;_&lt;assembler&gt;_&lt;name&gt;", "stitch"),
        ("methods", "pool + assembler (+ joiner) | long-series generator", "explicit method definition", "stitch"),
        ("models", "fit, predict, state, load_state, kinds", "fitted in TSTR and TRTR", "ml"),
        ("fidelity_metrics", "fn(ctx) → {metric: value} + orientation", "new F-columns × 3 references, ranked", "eval"),
        ("utility_metrics", "fn(y, pred, ctx) → dict", "new U-columns", "ml"),
        ("hypotheses: tests", "fn(d, margin) or fn(z) → dict", "columns in every comparison table", "stats"),
        ("hypotheses: catalog", "fn(tables, cfg) → global, per_dataset, extra", "case-study section in REPORT.md", "stats"),
    ]
    hdr = "".join(f'<TD BGCOLOR="{C["store"]}" ALIGN="LEFT"><B>{h}</B></TD>' for h in ["registry", "interface", "effect when registered"])
    tr = "".join(f'<TR><TD ALIGN="LEFT" BGCOLOR="{C[col]}"><B>{n}</B></TD><TD ALIGN="LEFT">{i}</TD>'
                 f'<TD ALIGN="LEFT">{e}</TD></TR>' for n, i, e, col in regs)
    table = (f'<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4" COLOR="{C["edge"]}">'
             f"<TR>{hdr}</TR>{tr}</TABLE>>")
    body = f"""
  rankdir=LR; ranksep=0.5;
  pl [label="plugin file\\nmy_plugins.py\\n@register(name)", shape=note, style=filled, fillcolor="{C['white']}"];
  cf [label=<<b>Config</b><br/><font point-size="8.5">plugins · pool_suites · extra_assemblers<br/>extra_joiners · long_methods · extra={{…}}</font>>, fillcolor="{C['store']}"];
  t [shape=plaintext, style="", margin=0, fontsize=9, label={table}];
  pl -> t [label=" registers"]; cf -> t [label=" selects by name"];
  {{rank=same; pl; cf}}
"""
    render("fig18_extensibility", body)


if __name__ == "__main__":
    for f in (fig01, fig02, fig03, fig04, fig05, fig06, fig08, fig09, fig10, fig11, fig12, fig13, fig14,
              fig15, fig16, fig17, fig18):
        f()
        print("ok", f.__name__)
