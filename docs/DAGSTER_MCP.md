## Dagster MCP setup for Copilot Chat

This workspace is preconfigured to let GitHub Copilot Chat talk to your Dagster project via the Model Context Protocol (MCP).

### What’s included
- VS Code workspace settings that register a Dagster MCP server under `github.copilot.chat.mcpServers`.
- The server runs via `uvx` using the official Dagster `dg` CLI with the `[mcp]` extra.

### Prerequisites
- Python and [uv](https://github.com/astral-sh/uv). In this repo you can install/refresh uv with:

  - Windows PowerShell:
    - Run the included script `scripts/setup_uv.ps1`.

### Configure (Dagster Open Source)
No token is required for local OSS usage. The MCP server runs with the current workspace as its target.

### Configure (Dagster+ Cloud) — optional
If you use Dagster+ Cloud, set the following:

1) In VS Code settings (already scaffolded):

- `confradar.dagster.cloudUrl`: set to your Dagster+ URL (for example, `https://prod.dagster.cloud/<org>/<deployment>`).

2) Provide your API token as a local environment variable so it isn’t checked in:

- Windows PowerShell (session only):
  - `$env:DAGSTER_CLOUD_API_TOKEN = "<your-token-here>"`

- Windows PowerShell (persist in your profile):
  - `notepad $PROFILE` and add:
    - `$env:DAGSTER_CLOUD_API_TOKEN = "<your-token-here>"`

Restart VS Code after setting the token so Copilot picks it up.

### How it works
- The server command configured in `.vscode/settings.json` is:
  - `uvx --from "dagster-dg[mcp]" dg --path ${workspaceFolder} mcp serve`
- This uses the official `dg` CLI’s MCP server (`dg mcp serve`).
- Copilot Chat connects to this MCP server and can then list/query Dagster definitions, suggest `dg` operations, and more.

### Troubleshooting
- If Copilot doesn’t show Dagster tools:
  - Restart VS Code to ensure settings are reloaded.
  - Ensure `uv` is installed (run `scripts/setup_uv.ps1`).
  - Check that `DAGSTER_CLOUD_API_TOKEN` is set if you’re using Dagster+.
  - Open the Output panel for “GitHub Copilot” to see MCP server start logs.

### Notes
- You can also run the server manually for debugging:
  - `uvx --from "dagster-dg[mcp]" dg --path . mcp serve`
  - This will run a foreground MCP server; stop it with Ctrl+C.

---

Maintained: See `docs/` and the repo wiki for broader architecture and dev workflow.
