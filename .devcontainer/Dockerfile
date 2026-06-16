FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
        git \
        curl \
        ca-certificates \
        build-essential \
        bubblewrap \
        socat \
    && rm -rf /var/lib/apt/lists/*

ENV UV_LINK_MODE=copy

WORKDIR /workspace
COPY pyproject.toml .
RUN uv sync --group dev

RUN curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && rm -rf /var/lib/apt/lists/* \
    && npm install -g @anthropic-ai/claude-code
