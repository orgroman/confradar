# Installs uv and sets up the development environment
# Usage: Run in PowerShell from repo root: scripts/setup_uv.ps1

$ErrorActionPreference = 'Stop'

Write-Host "Installing uv (if not already installed)..."
try {
    if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
        Invoke-Expression (Invoke-WebRequest -UseBasicParsing https://astral.sh/uv/install.ps1)
    } else {
        Write-Host "uv already installed."
    }
}
catch {
    Write-Error "Failed to install uv: $_"
    exit 1
}

Write-Host "Syncing dependencies (including dev group) via uv..."
uv sync --all-groups

Write-Host "Done. Example commands:" -ForegroundColor Green
Write-Host "  uv run pytest"
Write-Host "  uv run confradar parse --text 'Submission: Nov 15, 2025 (AoE)'"
