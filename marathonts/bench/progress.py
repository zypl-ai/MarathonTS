"""Progress bars (tqdm.auto: widgets in Colab / Jupyter, text in a terminal or Docker).

* `bar(...)` — a stage's bar over its units, or a nested one (`leave=False`) inside a unit:
  VAE / Diffusion-TS training, stitching, autoregressive generation, utility tasks.
* `log(msg)` — a message printed without breaking the bars.
* `silence(module)` — turn off the bars of third-party code that opens one per call
  (Diffusion-TS opens one per sampling call: thousands per series).

`BENCH_PROGRESS=0` turns every bar off (e.g. for log files).
"""
from __future__ import annotations

import os

ENABLED = os.environ.get("BENCH_PROGRESS", "1") != "0"


def bar(iterable=None, total=None, desc: str = "", leave: bool = True, unit: str = "it", **kw):
    from tqdm.auto import tqdm

    return tqdm(iterable, total=total, desc=desc, leave=leave, unit=unit, disable=not ENABLED,
                dynamic_ncols=True, mininterval=1.0, **kw)


def log(msg: str) -> None:
    try:
        from tqdm.auto import tqdm

        tqdm.write(msg)
    except Exception:
        print(msg, flush=True)


def _passthrough(iterable=None, *args, **kwargs):
    return iterable if iterable is not None else range(kwargs.get("total", 0) or 0)


def silence(module) -> None:
    """Replace `module.tqdm` by a pass-through iterator."""
    if hasattr(module, "tqdm"):
        module.tqdm = _passthrough
