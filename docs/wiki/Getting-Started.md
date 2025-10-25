# Getting Started

This guide helps you set up the ConfRadar development environment using uv and the LiteLLM proxy.

## Prerequisites

- Docker Desktop (for the LiteLLM proxy)
- Python 3.11+
- uv package manager

## Setup

```powershell
# Install uv (one-time)
iwr -useb https://astral.sh/uv/install.ps1 | iex

# From repo root, install dependencies (with dev extras)
uv sync --extra dev
```

## Run tests

```powershell
cd packages/confradar
uv run pytest -q
cd ../..
```

## LiteLLM proxy (recommended)

The app talks to an OpenAI-compatible endpoint via the LiteLLM proxy by default.

```powershell
# 1) Set your API key (service account preferred)
$env:CONFRADAR_SA_OPENAI = "<your-openai-key>"
# Alternative: $env:OPENAI_API_KEY = "..."

# 2) Start the proxy (listens on http://localhost:4000)
docker compose up -d

# 3) (Optional) Override the base URL used by the app
$env:LITELLM_BASE_URL = "http://localhost:4000"  # default
# Or: $env:LLM_BASE_URL / $env:OPENAI_BASE_URL
```

## Monorepo layout

- Root is a uv workspace aggregator
- Main Python package: `packages/confradar`
- CLI entrypoint: `confradar`

Run the CLI without installing the package globally:

```powershell
uv run confradar parse --text "Submission: Nov 15, 2025 (AoE)"
```

For more details, see the repository README.