# GitHub PR Conversations MCP Server

Standalone MCP server that exposes GitHub pull request review conversation tools so agents and MCP clients can manage review threads programmatically.

## Tools
- `list_review_threads(owner, repo, pull_number, resolved?)`
- `resolve_review_thread(thread_id)`
- `unresolve_review_thread(thread_id)`
- `bulk_resolve_threads(owner, repo, pull_number, thread_ids?)`

## Install
Use uv to install as a standalone package:

```powershell
cd mcp-servers/github-pr
uv pip install -e .
```

Set a GitHub token in your environment (requires `repo` scope):
```powershell
$env:GITHUB_TOKEN = "<your-token>"
```

## Run
Launch the server over stdio:
```powershell
uv run github-pr-mcp
```

Or directly via Python:
```powershell
uv run python server.py
```

## VS Code + Copilot Chat
Register this server under `github.copilot.chat.mcpServers` in your VS Code settings:

```json
{
  "github.copilot.chat.mcpServers": {
    "github-pr": {
      "command": "uv",
      "args": ["run", "--directory", "${workspaceFolder}/mcp-servers/github-pr", "github-pr-mcp"],
      "env": {
        "GITHUB_TOKEN": "${env:GITHUB_TOKEN}"
      }
    }
  }
}
```

## Notes
- Uses GitHub GraphQL API v4 (requires token with `repo` scope)
- Thread IDs are GraphQL node IDs (e.g., `PRRT_kw...`)
- `bulk_resolve_threads` resolves all unresolved threads when `thread_ids` is omitted
- Completely standalone—no dependency on the confradar package
