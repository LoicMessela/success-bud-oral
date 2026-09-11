# syntax=docker/dockerfile:1
# LiveKit Cloud Build image. `lk agent create` / `lk agent deploy` use this.
# Do not bake LIVEKIT_URL / LIVEKIT_API_KEY / LIVEKIT_API_SECRET into the image;
# LiveKit Cloud injects those. Put GOOGLE_API_KEY in Cloud secrets.

ARG PYTHON_VERSION=3.13
FROM ghcr.io/astral-sh/uv:python${PYTHON_VERSION}-bookworm-slim AS base

ENV PYTHONUNBUFFERED=1
ENV UV_COMPILE_BYTECODE=1

FROM base AS build

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    python3-dev \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN mkdir -p tests
RUN uv sync --locked --no-dev

COPY . .

FROM base

ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/app" \
    --shell "/sbin/nologin" \
    --uid "${UID}" \
    appuser

COPY --from=build --chown=appuser:appuser /app /app
WORKDIR /app
USER appuser

CMD ["uv", "run", "agent.py", "start"]
