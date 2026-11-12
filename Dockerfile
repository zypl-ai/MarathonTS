# Two images, one per environment; they share data/ and artifacts/ through volumes:
#
#   tsgm  — TensorFlow + tsgm: the `pools` stage of the tsgm_vae generator (no torch)
#   bench — PyTorch (CUDA 12 / CPU) + everything else: stitching, Diffusion-TS, Chronos, TimesFM,
#           Timestral, SDV, fidelity, utility, collect, hypotheses
#
#   docker build --target tsgm  -t marathonts:tsgm  .
#   docker build --target bench -t marathonts:bench .
#   (or `docker compose build`, see docker-compose.yml)
#
# Anything after the image name is passed to `python -m marathonts.bench.run`.

# ─────────────────────── tsgm environment ───────────────────────
FROM python:3.11-slim AS tsgm
ENV PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1 KERAS_BACKEND=tensorflow TF_CPP_MIN_LOG_LEVEL=2
# "[and-cuda]" pulls the CUDA libraries for TensorFlow on Linux; set to "" for a CPU-only image
ARG TF_EXTRA="[and-cuda]"
WORKDIR /app
COPY envs ./envs
# tensorflow comes from TF_EXTRA alone (tsgm.txt would pull the CUDA build even for TF_EXTRA="")
RUN grep -v '^tensorflow' envs/tsgm.txt > /tmp/tsgm.txt && pip install "tensorflow${TF_EXTRA}" -r /tmp/tsgm.txt
COPY marathonts ./marathonts
VOLUME ["/app/data", "/app/artifacts"]
ENTRYPOINT ["python", "-m", "marathonts.bench.run"]
CMD ["pools", "--pool-generators", "tsgm_vae"]

# ─────────────────────── main environment ───────────────────────
FROM pytorch/pytorch:2.5.1-cuda12.4-cudnn9-runtime AS bench
ENV PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY envs ./envs
RUN pip install -r envs/core.txt -r envs/diffusion_ts.txt -r envs/chronos.txt -r envs/timesfm.txt \
    -r envs/timestral.txt -r envs/sdv.txt
# Diffusion-TS is not a pip package: the official repository at a pinned commit (MIT licence)
ARG DIFFUSION_TS_COMMIT=566307e6cf2d8095e58de4c6e3a6ae965b69b5b5
RUN git clone https://github.com/Y-debug-sys/Diffusion-TS.git external/Diffusion-TS \
    && git -C external/Diffusion-TS checkout ${DIFFUSION_TS_COMMIT}
COPY marathonts ./marathonts
COPY README.md LICENSE NOTICE ./
VOLUME ["/app/data", "/app/artifacts"]
ENTRYPOINT ["python", "-m", "marathonts.bench.run"]
CMD ["all"]
