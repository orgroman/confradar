# GitHub PR Conversations MCP Server

This repo includes a lightweight MCP server that exposes GitHub pull request conversation tools so Copilot (or any MCP client) can manage review threads programmatically.

## Tools
- `list_review_threads(owner, repo, pull_number, resolved?)`
- `resolve_review_thread(thread_id)`
- `unresolve_review_thread(thread_id)`
- `bulk_resolve_threads(owner, repo, pull_number, thread_ids?)`

## Install
Use uv to install the optional extra with the MCP SDK:

- Windows PowerShell
```powershell
uv pip install -e packages/confradar[mcp]
```

Set a GitHub token in your environment (repo scope):
```powershell
$env:GITHUB_TOKEN = "<your-token>"
```

## Run
Launch the server over stdio using the packaged entrypoint:
```powershell
uv run confradar-github-mcp
```

Alternatively, point an MCP client directly to the module:
```powershell
uv run python -m confradar.mcp.github_pr_server
```

## VS Code + Copilot Chat
You can register this server under `github.copilot.chat.mcpServers` in your VS Code settings. Example snippet:

```json
{
  "github.copilot.chat.mcpServers": {
    "confradar-github-pr": {
      "command": "uv",
      "args": ["run", "confradar-github-mcp"],
      "env": {
        "GITHUB_TOKEN": "${env:GITHUB_TOKEN}"
      }
    }
  }
}
```

## Notes
- The server uses the GitHub GraphQL API v4 and requires a token with `repo` scope.
- Thread IDs are GraphQL node IDs (e.g., `PRRT_kw...`).
- `bulk_resolve_threads` resolves all unresolved threads when `thread_ids` is omitted.
