"""Shared setup of the Colab notebooks: Drive, code, dependencies, paths, separate environments.

Run from every notebook (first cell):

    REPO = "/content/drive/MyDrive/Colab Notebooks/MarathonTS"   # the project folder on Drive
    exec(open(f"{REPO}/colab/colab_setup.py").read())

It mounts Drive, installs the main environment once per runtime (`envs/core.txt` + Chronos, TimesFM,
Timestral + Diffusion-TS — its code is cloned too), and defines `cfg` with data and artifacts on
Drive — every notebook reads what the previous ones wrote, and a disconnected runtime resumes
where it stopped.

Every notebook has its own Colab runtime, so the runtimes are the separate environments:
notebook 2 installs `tsgm` into its runtime (`install_tsgm()`, on top of Colab's TensorFlow with
GPU) and runs the `pools` stage in a subprocess of that runtime (`run_in_env(None, "pools", ...)`);
notebook 3 never imports TensorFlow and only reads the pools from Drive. Other generators with
conflicting dependencies can still get a virtual environment: `run_in_env("sdv", "pools", ...)`
creates `/content/envs/sdv` from `envs/sdv.txt` (once per runtime).
"""
import os
import subprocess
import sys

try:
    from google.colab import drive

    if not os.path.isdir("/content/drive/MyDrive"):
        drive.mount("/content/drive")
except ImportError:                                    # not in Colab: plain local run
    pass

REPO = globals().get("REPO", os.getcwd())
PROFILE = globals().get("PROFILE", "min")                    # min: Colab run; mid: + the VAE per seed; max: everything
ARTIFACTS = globals().get("ARTIFACTS")                        # None → artifacts/<PROFILE>
# the long-series baselines (Diffusion-TS, Chronos, TimesFM, Timestral) run in every profile
MAIN_ENVS = globals().get("MAIN_ENVS", ["core", "chronos", "timesfm", "timestral", "diffusion_ts"])
os.chdir(REPO)
if REPO not in sys.path:
    sys.path.insert(0, REPO)

# packages only some methods / metrics need: a failed build must not stop the notebook (the method or
# metric then fails or is NaN with a message naming the package: vae_atsp, vae_pctsp, F5.5–F5.6, F7.7)
OPTIONAL_PACKAGES = {"elkai", "ortools", "ruptures", "hmmlearn"}


def _env_lines(env: str) -> list[str]:
    """Requirement lines of envs/<env>.txt with `-r other.txt` expanded."""
    out = []
    for line in open(f"{REPO}/envs/{env}.txt").read().splitlines():
        line = line.split("#")[0].strip()
        if line.startswith("-r "):
            out += _env_lines(line[3:].strip().removesuffix(".txt"))
        elif line:
            out.append(line)
    return out


def _pkg(line: str) -> str:
    import re

    return re.split(r"[<>=!~;\[ ]", line, maxsplit=1)[0].lower()


_marker = f"/tmp/.stitch_bench_env_{'_'.join(MAIN_ENVS)}"            # per set of environments
if not os.path.exists(_marker):
    _lines = list(dict.fromkeys(l for e in MAIN_ENVS for l in _env_lines(e)))
    _main = [l for l in _lines if _pkg(l) not in OPTIONAL_PACKAGES]
    _opt = [l for l in _lines if _pkg(l) in OPTIONAL_PACKAGES]
    with open("/tmp/stitch_req_main.txt", "w") as _f:
        _f.write("\n".join(_main) + "\n")
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-r", "/tmp/stitch_req_main.txt"], check=True)
    for _l in _opt:
        if subprocess.run([sys.executable, "-m", "pip", "install", "-q", _l]).returncode:
            print(f"WARNING: optional package {_l!r} failed to install — the methods / metrics that need it "
                  f"will fail or be NaN (see artifacts/errors.log)")
    open(_marker, "w").close()

_dts = f"{REPO}/external/Diffusion-TS"
if "diffusion_ts" in MAIN_ENVS and not os.path.isdir(_dts):
    subprocess.run(["git", "clone", "-q", "https://github.com/Y-debug-sys/Diffusion-TS.git", _dts], check=True)
    subprocess.run(["git", "-C", _dts, "checkout", "-q", "566307e6cf2d8095e58de4c6e3a6ae965b69b5b5"], check=True)

from pathlib import Path  # noqa: E402
import warnings  # noqa: E402

# non-critical library warnings flood the outputs (thousands per stage): NaN in empty slices and
# 0 / 0 (the metric is then NaN — by design), p-values floored by scipy, logistic regression not
# converging in the discriminator, near-singular matrices, deprecations. The project itself never
# warns; errors still raise and go to artifacts/errors.log. Stage subprocesses inherit the
# built-in categories through PYTHONWARNINGS.
for _c in (RuntimeWarning, FutureWarning, DeprecationWarning, PendingDeprecationWarning):
    warnings.filterwarnings("ignore", category=_c)                  # scipy's LinAlgWarning is a RuntimeWarning
warnings.filterwarnings("ignore", message=r"p-value (floored|capped)")
warnings.filterwarnings("ignore", message=r".*(failed to converge|did not converge)")
warnings.filterwarnings("ignore", message=r".*will be removed")                # deprecations sent as UserWarning
os.environ["PYTHONWARNINGS"] = "ignore::RuntimeWarning,ignore::FutureWarning,ignore::DeprecationWarning"

# re-running this cell picks up edited project code: Python keeps imported modules, so a runtime that already
# imported bench / hypotheses (any cell run before) would otherwise keep running the code imported then
for _m in [m for m in sys.modules if m.split(".")[0] in ("bench", "hypotheses") or m.startswith("marathonts_plugin_")]:
    del sys.modules[_m]

from marathonts.bench.config import Config  # noqa: E402
from marathonts.bench.timing import hardware  # noqa: E402

cfg = Config.profile(PROFILE)
if ARTIFACTS:
    cfg = __import__("dataclasses").replace(cfg, artifacts_dir=Path(ARTIFACTS))


TSGM_VERSION = "0.1.0"


def install_tsgm(py: str = sys.executable) -> None:
    """Install tsgm into the interpreter `py` (default: this runtime, on top of Colab's TensorFlow
    and Keras 3 — nothing else is reinstalled). tsgm 0.1.0's setup.py reads its version from
    `locals()` after `exec`, which Python 3.13 does not fill (PEP 667): pip then fails with
    KeyError('__version__') before installing anything. The sdist is downloaded directly from PyPI
    and that one line is patched."""
    probe = subprocess.run([py, "-c", "import tsgm"], capture_output=True)
    if probe.returncode == 0:
        return
    import json as _json
    import tarfile
    import tempfile
    import urllib.request

    meta = _json.loads(urllib.request.urlopen(f"https://pypi.org/pypi/tsgm/{TSGM_VERSION}/json").read())
    url = next(u["url"] for u in meta["urls"] if u["packagetype"] == "sdist")
    tmp = tempfile.mkdtemp()
    tgz = os.path.join(tmp, "tsgm.tar.gz")
    urllib.request.urlretrieve(url, tgz)
    with tarfile.open(tgz) as tf:
        tf.extractall(tmp, filter="data")
    src_dir = os.path.join(tmp, f"tsgm-{TSGM_VERSION}")
    setup_py = os.path.join(src_dir, "setup.py")
    src = open(setup_py).read()
    old = "        exec(f.read())\n    return locals()['__version__']"
    if old in src:
        src = src.replace(old, "        ns = {}\n        exec(f.read(), ns)\n    return ns['__version__']")
        open(setup_py, "w").write(src)
    print(f"installing tsgm {TSGM_VERSION} …")
    subprocess.run([py, "-m", "pip", "install", "-q", src_dir], check=True)


def _requirements(env: str) -> list[str]:
    """Lines of envs/<env>.txt with `-r other.txt` expanded (the Drive path has spaces)."""
    out = []
    for line in open(f"{REPO}/envs/{env}.txt").read().splitlines():
        line = line.split("#")[0].strip()
        if line.startswith("-r "):
            out += _requirements(line[3:].strip().removesuffix(".txt"))
        elif line:
            out.append(line)
    return out


def env_python(env: str | None) -> str:
    """Python of a separate virtual environment built from envs/<env>.txt (created once per runtime);
    None → this runtime's own Python. Uses `virtualenv` (Colab's `python -m venv` often lacks
    ensurepip)."""
    if env is None:
        return sys.executable
    root = f"/content/envs/{env}" if os.path.isdir("/content") else f"{REPO}/.envs/{env}"
    py = f"{root}/bin/python"
    if not os.path.exists(py):
        print(f"creating environment {env} …")
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "virtualenv"], check=True)
        subprocess.run([sys.executable, "-m", "virtualenv", "-q", root], check=True)
        subprocess.run([py, "-m", "pip", "install", "-q", "--upgrade", "pip"], check=True)
        req = _requirements(env)
        tsgm = [r for r in req if r.split("=")[0].split(";")[0].strip() == "tsgm"]
        req_file = f"/tmp/stitch_req_{env}.txt"
        with open(req_file, "w") as f:
            f.write("\n".join(r for r in req if r not in tsgm) + "\n")
        subprocess.run([py, "-m", "pip", "install", "-q", "-r", req_file], check=True)
        if tsgm:                                     # patched sdist (see install_tsgm)
            install_tsgm(py)
    return py


def run_in_env(env: str | None, *args: str, config=None) -> None:
    """Run `python -m marathonts.bench.run <args>` as a subprocess in the environment `env` (None → this
    runtime's Python, in a fresh process). The whole config (`config` or the notebook's `cfg`:
    scope, artifacts dir, every setting and `extra`) is handed over as JSON, so the subprocess sees
    exactly the notebook's settings. Output is streamed; failing units go to artifacts/errors.log."""
    c = config or cfg
    cfg_file = f"/tmp/stitch_cfg_{os.getpid()}.json"
    with open(cfg_file, "w") as f:
        f.write(c.to_json())
    cmd = [env_python(env), "-m", "marathonts.bench.run", *args, "--config", cfg_file]
    print("$", " ".join(cmd))
    # read raw chunks, not lines: progress bars redraw with "\r" and never end a line
    with subprocess.Popen(cmd, cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as p:
        while True:
            chunk = p.stdout.read1(4096)
            if not chunk:
                break
            print(chunk.decode(errors="replace"), end="", flush=True)
    if p.returncode:
        raise RuntimeError(f"stage failed in env {env or 'runtime'} (exit {p.returncode})")


print("repo:", REPO)
print("profile:", PROFILE, "| processed:", cfg.processed_dir)
print("artifacts:", cfg.artifacts_dir)
# the tsgm runtime (MAIN_ENVS = ["base"]) must not create a torch CUDA context: TF trains there
print("hardware:", hardware(use_torch="core" in MAIN_ENVS))
