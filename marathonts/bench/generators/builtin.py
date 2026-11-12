"""Built-in generators.

Pool generators: `tsgm_vae` (BENCHMARK.md, Protocol: pool generator), `sdv_par` (SDV PARSynthesizer), `real_windows`
(random real train windows — a control / smoke-test stand-in, no learning).
Long generators: `diffusion_ts` (Diffusion-TS, autoregressive infill), `chronos` (Chronos sampling), `timesfm`
(TimesFM 3.0) and `timestral` (Timestral) — the median forecast after train.
"""
from __future__ import annotations

import copy
import os
import sys
import time

import numpy as np

from .. import registry as R
from ..progress import bar, silence
from ..storage import blob, torch_state
from .base import GenContext, LongGenerator, PoolGenerator, calendar_channels



def init_tensorflow():
    """Import TF before torch touches CUDA and let it grow GPU memory: by default TF reserves the
    whole GPU, while torch runs in the same process. Returns tf or None."""
    os.environ["KERAS_BACKEND"] = "tensorflow"      # tsgm is written for Keras 3 on TensorFlow (jax → constant samples)
    os.environ.pop("TF_USE_LEGACY_KERAS", None)     # Colab may set it: tf.keras would then be Keras 2
    try:
        import tensorflow as tf
    except Exception:
        return None
    for gpu in tf.config.list_physical_devices("GPU"):
        try:
            tf.config.experimental.set_memory_growth(gpu, True)
        except RuntimeError:                       # already initialised in this process
            pass
    return tf


# ─────────────────────── tsgm VAE (BENCHMARK.md, Protocol: pool generator) ──────────────────────────────
@R.pool_generators.register("tsgm_vae")
class TsgmVAE(PoolGenerator):
    """`tsgm` vae_conv5 + BetaVAE; early stopping on holdout loss after `vae_min_epochs`; z ~ N(0, 1) · noise."""

    env = "tsgm"
    requires = ("tensorflow", "tsgm")

    def fit(self, ctx: GenContext):
        tf = init_tensorflow()
        import keras

        cfg = ctx.cfg
        keras.utils.set_random_seed(ctx.seed)
        try:
            tf.config.experimental.reset_memory_stats("GPU:0")
        except Exception:
            pass
        vae = self._build(ctx)

        def holdout_loss(X):
            zm, zlv, _ = vae.encoder(X, training=False)
            rec_x = vae.decoder(zm, training=False)
            r = tf.reduce_mean(vae._get_reconstruction_loss(X, rec_x))
            kl = tf.reduce_mean(tf.reduce_sum(-0.5 * (1 + zlv - zm ** 2 - tf.exp(zlv)), axis=1))
            return float(r + kl)

        best, best_ep, best_w, ep = np.inf, -1, None, -1
        with bar(range(cfg.vae_epochs), desc="VAE epochs", leave=False, unit="ep") as it:
            for ep in it:
                vae.fit(ctx.X_core, epochs=1, batch_size=cfg.vae_batch, verbose=0)
                hl = holdout_loss(ctx.X_hold)
                if ep + 1 < cfg.vae_min_epochs:          # early epochs: undertrained, holdout loss misleads
                    it.set_postfix(holdout=f"{hl:.4g}", warmup=True)
                    continue
                if hl < best:
                    best, best_ep = hl, ep
                    best_w = vae.encoder.get_weights() + vae.decoder.get_weights()
                it.set_postfix(holdout=f"{hl:.4g}", best_epoch=best_ep)
                if ep - best_ep >= cfg.vae_patience:
                    break
        if best_w is not None:                       # holdout loss never finite → keep the last weights
            ne = len(vae.encoder.get_weights())
            vae.encoder.set_weights(best_w[:ne])
            vae.decoder.set_weights(best_w[ne:])
        self.vae, self.tf = vae, tf
        self.info.update(vae_epochs_run=ep + 1, vae_best_epoch=best_ep, vae_holdout_loss=best,
                         tf_gpus=len(tf.config.list_physical_devices("GPU")))   # 0 = trained on CPU
        try:
            self.info["fit_tf_gpu_peak_mb"] = tf.config.experimental.get_memory_info("GPU:0")["peak"] / 2**20
        except Exception:
            pass

    @staticmethod
    def _build(ctx):
        init_tensorflow()
        import keras
        import tsgm

        arch = tsgm.models.zoo["vae_conv5"](seq_len=ctx.T, feat_dim=ctx.X_core.shape[2], latent_dim=ctx.cfg.vae_latent)
        vae = tsgm.models.cvae.BetaVAE(arch.encoder, arch.decoder, beta=ctx.cfg.vae_beta)
        vae.compile(optimizer=keras.optimizers.Adam(1e-3))
        return vae

    def load_state(self, a, ctx):
        vae = self._build(ctx)
        ne, nd = len(vae.encoder.get_weights()), len(vae.decoder.get_weights())
        vae.encoder.set_weights([a[f"encoder.{i}"] for i in range(ne)])
        vae.decoder.set_weights([a[f"decoder.{i}"] for i in range(nd)])
        self.vae = vae
        return self

    def sample(self, n, ctx):
        rng = np.random.default_rng(ctx.seed)
        z = (rng.standard_normal((n, ctx.cfg.vae_latent)) * ctx.cfg.vae_noise).astype(np.float32)
        out = np.asarray(self.vae.decoder(z, training=False))
        return np.clip(np.nan_to_num(out, nan=0.5), 0, 1).astype(np.float32)

    def state(self):
        w = {f"encoder.{i}": a for i, a in enumerate(self.vae.encoder.get_weights())}
        w.update({f"decoder.{i}": a for i, a in enumerate(self.vae.decoder.get_weights())})
        return w


# ─────────────────────── real windows (control / smoke tests) ──────────────
@R.pool_generators.register("real_windows")
class RealWindows(PoolGenerator):
    """N random real core windows — no generator at all. A control for 'is the generator needed'
    and the stand-in for the VAE in smoke tests without TensorFlow."""

    def fit(self, ctx):
        self.X = ctx.X_core

    def load_state(self, a, ctx):                    # nothing learned: the windows come from the data
        self.fit(ctx)
        return self

    def sample(self, n, ctx):
        rng = np.random.default_rng(ctx.seed)
        return self.X[rng.choice(len(self.X), n, replace=len(self.X) < n)]


# ─────────────────────── SDV PARSynthesizer ────────────────────────────────
@R.pool_generators.register("sdv_par")
class SdvPAR(PoolGenerator):
    """SDV's sequential PARSynthesizer on train windows (each window = one sequence).
    Params (`Config.extra["sdv_par"]`): epochs (default 128), max_windows (default 2000)."""

    env = "sdv"
    requires = ("sdv",)

    def fit(self, ctx):
        import pandas as pd
        from sdv.sequential import PARSynthesizer

        try:
            from sdv.metadata import Metadata
            make_md = "multi"
        except ImportError:
            from sdv.metadata import SingleTableMetadata as Metadata
            make_md = "single"
        prm = ctx.params
        X = ctx.X_core
        rng = np.random.default_rng(ctx.seed)
        if len(X) > prm.get("max_windows", 2000):
            X = X[rng.choice(len(X), prm.get("max_windows", 2000), replace=False)]
        n, T, F = X.shape
        df = pd.DataFrame(X.reshape(n * T, F), columns=[f"c{i}" for i in range(F)])
        df.insert(0, "t", np.tile(np.arange(T), n))
        df.insert(0, "win", np.repeat(np.arange(n), T).astype(str))
        md = Metadata.detect_from_dataframe(df) if make_md == "multi" else Metadata()
        if make_md == "single":
            md.detect_from_dataframe(df)
        md.update_column(column_name="win", sdtype="id")
        md.update_column(column_name="t", sdtype="numerical")
        md.set_sequence_key("win")
        md.set_sequence_index("t")
        self.syn = PARSynthesizer(md, epochs=prm.get("epochs", 128), enforce_min_max_values=True,
                                  cuda=ctx.device.startswith("cuda"), verbose=False)
        self.syn.fit(df)
        self.F, self.T = F, T

    def sample(self, n, ctx):
        import random

        import torch

        random.seed(ctx.seed)                          # SDV samples from the global random state:
        np.random.seed(ctx.seed)                       # seed it so a pool depends only on the seed
        torch.manual_seed(ctx.seed)
        out = self.syn.sample(num_sequences=n, sequence_length=self.T)
        cols = [f"c{i}" for i in range(self.F)]
        W = np.stack([g.sort_values("t")[cols].to_numpy(np.float32)[: self.T] for _, g in out.groupby("win")])
        return np.clip(W[:n], 0, 1)

    def state(self):
        return {"synthesizer": blob(self.syn), "shape": np.array([self.F, self.T])}

    def load_state(self, a, ctx):
        from ..storage import unblob

        self.syn = unblob(a["synthesizer"])
        self.F, self.T = (int(v) for v in a["shape"])
        return self


# ─────────────────────── Diffusion-TS ──────────────────────────────────────
@R.long_generators.register("diffusion_ts")
class DiffusionTS(LongGenerator):
    """Official Diffusion-TS model (cfg.diffusion_ts_dir) trained on the core windows by the official recipe
    (optimiser, warm-up + plateau schedule, batch and accumulation, EMA of Config/etth.yaml) plus early
    stopping on holdout; the long series is grown by infilling: each new window keeps the
    last `dts_context_frac · T` values of the previous one. The calendar channels are imposed
    (hour of week continues from a random start); the model fills only the value channel."""

    env = "diffusion_ts"
    uses_windows = True
    requires = ("torch", "einops")

    def fit(self, ctx):
        if not ctx.cfg.dts_train_per_seed:           # shared models per dataset; seeds vary only the sampling
            from ..storage import read_arrays, write_arrays

            import time

            from ..storage import read_record, write_record

            from ..methods import dts_replica, dts_shared, is_fresh

            rep = dts_replica(ctx.cfg, ctx.seed)       # replica r is trained with seed r (as the VAE replicas)
            shared, fp = dts_shared(ctx.cfg, ctx.p.name, rep)    # fingerprint: training settings only
            shared_rec = shared.with_name(shared.name.replace(".parquet", ".record.parquet"))
            if shared.exists() and is_fresh(shared_rec, fp):         # same dts_* settings and data
                self.load_state(read_arrays(shared), ctx)
                r = read_record(shared_rec)
                self.info.update(dts_shared=True, dts_trained_here=False, dts_steps_run=r.get("dts_steps_run"),
                                 dts_holdout_loss=r.get("dts_holdout_loss"))
                self.load_s = float(r["train_wall_s"])   # every seed reports the cost of the shared model (RQ6)
                return
            t0 = time.perf_counter()
            self._train(ctx, seed=rep)
            self.load_s = time.perf_counter() - t0
            write_arrays(self.state(), shared, dtype=None)
            write_record({**self.info, "train_wall_s": self.load_s, "unit_fp": fp}, shared_rec)
            self.info.update(dts_shared=True, dts_trained_here=True)
            return
        self._train(ctx, seed=ctx.seed)

    def _train(self, ctx, seed):
        import torch

        cfg, dev = ctx.cfg, ctx.device
        torch.manual_seed(seed)
        np.random.seed(seed)
        model = self._build(ctx)
        ema = copy.deepcopy(model).eval()
        ema.requires_grad_(False)              # as ema_pytorch: infill's Langevin steps need frozen weights
        # optimiser and scheduler of the official solver (engine/solver.py, Config/etth.yaml)
        from engine.lr_sch import ReduceLROnPlateauWithWarmup

        opt = torch.optim.Adam(model.parameters(), lr=cfg.dts_lr, betas=(0.9, 0.96))
        sch = ReduceLROnPlateauWithWarmup(opt, factor=cfg.dts_lr_factor, patience=cfg.dts_lr_patience,
                                          min_lr=cfg.dts_min_lr, threshold=cfg.dts_lr_threshold, threshold_mode="rel",
                                          warmup_lr=cfg.dts_warmup_lr, warmup=cfg.dts_warmup, verbose=False)
        Xc = torch.as_tensor(ctx.X_core * 2 - 1, dtype=torch.float32)
        Xh = torch.as_tensor(ctx.X_hold * 2 - 1, dtype=torch.float32, device=dev)
        g = torch.Generator().manual_seed(seed)

        def batches():                                      # DataLoader(shuffle=True, drop_last=True), cycled
            n, B = len(Xc), cfg.dts_batch
            while True:
                perm = torch.randperm(n, generator=g)
                for i in range(0, max(n - B, 0) + 1, B):
                    yield perm[i:i + B]

        def ema_update(step):                               # ema-pytorch 0.2.1: EMA(beta, update_every=10)
            if step % cfg.dts_ema_every:
                return
            with torch.no_grad():
                if step <= cfg.dts_ema_after:               # the first steps: a copy of the model
                    ema.load_state_dict(model.state_dict())
                    return
                e = step - cfg.dts_ema_after - 1
                decay = 0.0 if e <= 0 else min(cfg.dts_ema_decay, 1 - (1 + e) ** (-2 / 3))
                for pe, pm in zip(ema.parameters(), model.parameters()):
                    pe.lerp_(pm, 1 - decay)
                for be, bm in zip(ema.buffers(), model.buffers()):
                    be.copy_(bm)

        stream = batches()

        def hold_loss():
            torch.manual_seed(12345)                        # same noise / t for every evaluation
            with torch.no_grad():
                return float(np.mean([ema(Xh[i:i + 256]).item() for i in range(0, len(Xh), 256)]))

        best, best_state, bad, step = np.inf, None, 0, 0
        it = bar(range(1, cfg.dts_steps + 1), desc="Diffusion-TS train", leave=False, unit="step")
        for step in it:
            total = 0.0
            for _ in range(cfg.dts_grad_accum):              # as the official trainer
                loss = model(Xc[next(stream)].to(dev)) / cfg.dts_grad_accum
                loss.backward()
                total += loss.item()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            opt.step()
            sch.step(total)
            opt.zero_grad()
            ema_update(step)
            if step % cfg.dts_eval_every == 0 and len(Xh):
                hl = hold_loss()
                it.set_postfix(holdout=f"{hl:.4g}")
                torch.manual_seed(seed * 7919 + step)
                if hl < best:
                    best, best_state, bad = hl, copy.deepcopy(ema.state_dict()), 0
                else:
                    bad += 1
                    if bad >= cfg.dts_patience_evals:
                        break
        it.close()
        if best_state is not None:
            ema.load_state_dict(best_state)
        self.ema = ema
        self.info.update(dts_steps_run=step, dts_holdout_loss=best)

    @staticmethod
    def _build(ctx):
        d = str(ctx.cfg.diffusion_ts_dir)
        if d not in sys.path:
            sys.path.insert(0, d)
        import Models.interpretable_diffusion.gaussian_diffusion as gd

        silence(gd)                                 # one bar per sampling call → thousands per series
        Diffusion_TS = gd.Diffusion_TS
        cfg = ctx.cfg
        return Diffusion_TS(
            seq_length=ctx.T, feature_size=ctx.X_core.shape[2], n_layer_enc=cfg.dts_enc_layers,
            n_layer_dec=cfg.dts_dec_layers, d_model=cfg.dts_d_model, timesteps=cfg.dts_timesteps,
            sampling_timesteps=cfg.dts_sampling_steps, loss_type="l1", beta_schedule="cosine",
            n_heads=cfg.dts_heads, mlp_hidden_times=4, attn_pd=0.0, resid_pd=0.0, kernel_size=1,
            padding_size=0).to(ctx.device)

    def load_state(self, a, ctx):
        import torch

        ema = self._build(ctx).eval()
        ema.load_state_dict({k: torch.as_tensor(v) for k, v in a.items()})
        ema.requires_grad_(False)
        self.ema = ema
        return self

    def generate(self, ctx):
        import torch

        cfg, dev, T, L = ctx.cfg, ctx.device, ctx.T, ctx.L
        c = int(round(cfg.dts_context_frac * T))
        how0 = int(np.random.default_rng(ctx.seed).integers(0, 168))
        ang = 2 * np.pi * ((how0 + np.arange(L + T)) % 168) / 168
        cal = torch.as_tensor(np.column_stack([np.sin(ang), np.cos(ang)]), dtype=torch.float32, device=dev)
        kw = {"coef": cfg.dts_infill_coef, "learning_rate": cfg.dts_infill_lr}
        ema = self.ema

        def infill(start, known_values):
            tgt = torch.zeros((1, T, 3), device=dev)
            mask = torch.zeros((1, T, 3), dtype=torch.bool, device=dev)
            tgt[0, :, 1:] = cal[start:start + T]
            mask[0, :, 1:] = True
            k = len(known_values)
            if k:
                tgt[0, :k, 0] = known_values
                mask[0, :k, 0] = True
            return ema.fast_sample_infill((1, T, 3), tgt, cfg.dts_sampling_steps, partial_mask=mask,
                                          model_kwargs=kw)[0, :, 0].detach()

        torch.manual_seed(ctx.seed)
        n_steps = 1 + max(0, -(-(L - T) // (T - c)))
        with bar(total=n_steps, desc="Diffusion-TS generate", leave=False, unit="window") as it:
            vals = infill(0, torch.zeros(0, device=dev))
            it.update()
            total, seams = T, []
            while total < L:
                new = infill(total - c, vals[-c:])
                seams.append(total)
                vals = torch.cat([vals, new[c:]])
                total += T - c
                it.update()
        v01 = ((vals[:L].cpu().numpy() + 1) / 2).clip(0, 1)
        return v01 * (ctx.hi - ctx.lo) + ctx.lo, (how0 + np.arange(L)) % 168, np.asarray(seams, int)

    def state(self):
        return torch_state(self.ema)


# ─────────────────────── Chronos ───────────────────────────────────────────
_CHRONOS: dict = {}          # (model, device) → (pipeline, load seconds)


@R.long_generators.register("chronos")
class Chronos(LongGenerator):
    """Pretrained Chronos samples a K·T trajectory continuing the last `chronos_context` train
    points, in chunks of `chronos_chunk`. Loaded once per process; `fit` reports that load time
    for every seed. Weights are not saved (the model id is in the config)."""

    env = "chronos"
    requires = ("torch", "chronos")

    def fit(self, ctx):
        import torch
        from chronos import ChronosPipeline

        key = (ctx.cfg.chronos_model, ctx.device)
        if key not in _CHRONOS:
            t0 = time.perf_counter()
            pipe = ChronosPipeline.from_pretrained(
                ctx.cfg.chronos_model, device_map=ctx.device,
                torch_dtype=torch.bfloat16 if ctx.device.startswith("cuda") else torch.float32)
            _CHRONOS[key] = (pipe, time.perf_counter() - t0)
        self.pipe, self.load_s = _CHRONOS[key]
        self.info["chronos_model"] = ctx.cfg.chronos_model

    def load_state(self, a, ctx):                    # pretrained: weights come from the model id
        self.fit(ctx)
        return self

    def generate(self, ctx):
        import torch

        cfg, L = ctx.cfg, ctx.L
        v_tr, how_tr = ctx.train_series()
        torch.manual_seed(ctx.seed)
        ctxt = torch.tensor(v_tr[-cfg.chronos_context:], dtype=torch.float32)
        out, seams, total = [], [], 0
        with bar(total=-(-L // cfg.chronos_chunk), desc="Chronos generate", leave=False, unit="chunk") as it:
            while total < L:
                n = min(cfg.chronos_chunk, L - total)
                y = self.pipe.predict(ctxt[None], prediction_length=n, num_samples=1)[0, 0].float().cpu()
                if total:
                    seams.append(total)
                out.append(y)
                ctxt = torch.cat([ctxt, y])[-cfg.chronos_context:]
                total += n
                it.update()
        v = torch.cat(out).numpy().astype(float)
        return v, (how_tr[-1] + 1 + np.arange(L)) % 168, np.asarray(seams, int)


_PRETRAINED: dict = {}        # (generator, model, revision, device) → (forecaster, load seconds)


class _Pretrained(LongGenerator):
    """A pretrained forecaster used zero-shot, as officially documented: the whole train split (up to the
    model's own context limit) is the context, and the K·T series is the forecaster's point forecast —
    the median — of the steps after train. No sampling: the series is the same on every seed. The
    context is not part of the output. Loaded once per process; `fit` reports the load time for every
    seed; weights are not saved (the model id and revision are in the config)."""

    name = ""

    def _load(self, ctx, model, revision):
        raise NotImplementedError

    @staticmethod
    def _finite(v, L):
        v = np.asarray(v, float).reshape(-1)
        if len(v) < L or not np.isfinite(v[:L]).all():
            raise RuntimeError(f"forecast of {len(v)} points with {int((~np.isfinite(v)).sum())} non-finite "
                               f"(expected {L} finite)")
        return v[:L]

    def fit(self, ctx):
        cfg = ctx.cfg
        model, rev = getattr(cfg, f"{self.name}_model"), getattr(cfg, f"{self.name}_revision")
        key = (self.name, model, rev, ctx.device)
        if key not in _PRETRAINED:
            t0 = time.perf_counter()
            _PRETRAINED[key] = (self._load(ctx, model, rev), time.perf_counter() - t0)
        self.model, self.load_s = _PRETRAINED[key]
        self.info.update({f"{self.name}_model": model, f"{self.name}_revision": rev})

    def load_state(self, a, ctx):                    # pretrained: weights come from the model id
        self.fit(ctx)
        return self


@R.long_generators.register("timesfm")
class TimesFM(_Pretrained):
    """TimesFM 3.0 (Google, `timesfm` package): `TimesFM3Forecaster.predict(context, horizon)` with the
    package defaults — one non-autoregressive pass over the whole horizon, the point forecast is the
    median quantile. Context: the last ≤ 15 360 train points (the model's limit). No chunks, no seams."""

    name, env, requires = "timesfm", "timesfm", ("torch", "timesfm3")

    def _load(self, ctx, model, rev):
        from timesfm3 import TimesFM3Forecaster

        return TimesFM3Forecaster.from_pretrained(model, device=ctx.device, revision=rev)

    def generate(self, ctx):
        v_tr, how_tr = ctx.train_series()
        v_tr = np.asarray(v_tr, np.float32)
        out = self.model.predict(v_tr, horizon=ctx.L)
        v = self._finite(out.forecast, ctx.L)
        self.info["context_used"] = int(min(len(v_tr), self.model.global_context))
        return v, (how_tr[-1] + 1 + np.arange(ctx.L)) % 168, np.zeros(0, int)


@R.long_generators.register("timestral")
class Timestral(_Pretrained):
    """Timestral (Mistral, `timestral` package): `TimestralForecaster.forecast(context, prediction_length)`
    with the forecaster defaults — the whole train as context (≤ 32 768 steps), horizons longer than one
    decode block forecast block by block with each block's median fed back; the series is the median.
    Seams: the block boundaries."""

    name, env, requires = "timestral", "timestral", ("torch", "timestral")

    def _load(self, ctx, model, rev):
        from timestral import TimestralForecaster

        return TimestralForecaster.from_pretrained(model, device=ctx.device, revision=rev)

    def generate(self, ctx):
        v_tr, how_tr = ctx.train_series()
        fc = self.model.forecast(np.asarray(v_tr, np.float32), prediction_length=ctx.L)
        v = self._finite(fc.median.detach().float().cpu().numpy(), ctx.L)
        block = int(self.model.config.patch_size * self.model.per_shot_horizon_patches)
        self.info["context_used"] = int(min(len(v_tr), self.model.max_context))
        return v, (how_tr[-1] + 1 + np.arange(ctx.L)) % 168, np.arange(block, ctx.L, block, dtype=int)


__all__ = ["TsgmVAE", "RealWindows", "SdvPAR", "DiffusionTS", "Chronos", "TimesFM", "Timestral",
           "init_tensorflow", "calendar_channels"]
