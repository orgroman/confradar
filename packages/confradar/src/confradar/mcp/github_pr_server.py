"""
GitHub PR Conversations MCP Server

Implements MCP tools for managing pull request review threads via GitHub GraphQL.

Core tools:
- list_review_threads(owner, repo, pull_number, resolved?)
- resolve_review_thread(owner, repo, thread_id)
- unresolve_review_thread(owner, repo, thread_id)
- bulk_resolve_threads(owner, repo, pull_number, thread_ids?)

Auth:
- Uses a GitHub token from env: GITHUB_TOKEN or GH_TOKEN.

Note: This server uses the Python MCP SDK. Ensure the 'mcp' package is installed
(e.g., install the optional extra 'confradar[mcp]').
"""
from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Optional

import httpx

# Import MCP only inside main()/bootstrap paths so test/lint/imports don't break without the optional dep

GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"


class GitHubGraphQLClient:
    def __init__(self, token: Optional[str] = None):
        token = token or os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
        if not token:
            raise RuntimeError(
                "Missing GitHub token. Please set GITHUB_TOKEN or GH_TOKEN in the environment."
            )
        self._headers = {
            "Authorization": f"bearer {token}",
            "Accept": "application/vnd.github+json",
        }

    async def query(self, query: str, variables: Dict[str, Any]) -> Dict[str, Any]:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(
                GITHUB_GRAPHQL_URL,
                headers=self._headers,
                json={"query": query, "variables": variables},
            )
            resp.raise_for_status()
            data = resp.json()
            if "errors" in data and data["errors"]:
                raise RuntimeError(f"GraphQL errors: {data['errors']}")
            return data["data"]


LIST_THREADS_QUERY = """
query($owner:String!, $repo:String!, $number:Int!){
  repository(owner:$owner, name:$repo){
    pullRequest(number:$number){
      reviewThreads(first:100){
        nodes{
          id
          isResolved
          comments(first:5){ nodes{ id url body path } }
        }
      }
    }
  }
}
"""

RESOLVE_THREAD_MUTATION = """
mutation($threadId:ID!){
  resolveReviewThread(input:{threadId:$threadId}){ thread{ id isResolved } }
}
"""

UNRESOLVE_THREAD_MUTATION = """
mutation($threadId:ID!){
  unresolveReviewThread(input:{threadId:$threadId}){ thread{ id isResolved } }
}
"""


async def _list_review_threads(
    gh: GitHubGraphQLClient,
    owner: str,
    repo: str,
    pull_number: int,
    resolved: Optional[bool] = None,
) -> List[Dict[str, Any]]:
    data = await gh.query(
        LIST_THREADS_QUERY, {"owner": owner, "repo": repo, "number": pull_number}
    )
    nodes = (
        data.get("repository", {})
        .get("pullRequest", {})
        .get("reviewThreads", {})
        .get("nodes", [])
    )
    if resolved is None:
        return nodes
    return [n for n in nodes if bool(n.get("isResolved")) == resolved]


async def _resolve_review_thread(gh: GitHubGraphQLClient, thread_id: str) -> Dict[str, Any]:
    data = await gh.query(RESOLVE_THREAD_MUTATION, {"threadId": thread_id})
    return data.get("resolveReviewThread", {}).get("thread", {})


async def _unresolve_review_thread(gh: GitHubGraphQLClient, thread_id: str) -> Dict[str, Any]:
    data = await gh.query(UNRESOLVE_THREAD_MUTATION, {"threadId": thread_id})
    return data.get("unresolveReviewThread", {}).get("thread", {})


async def _bulk_resolve_threads(
    gh: GitHubGraphQLClient,
    owner: str,
    repo: str,
    pull_number: int,
    thread_ids: Optional[List[str]] = None,
) -> Dict[str, Any]:
    if not thread_ids:
        threads = await _list_review_threads(gh, owner, repo, pull_number, resolved=False)
        thread_ids = [t["id"] for t in threads]

    resolved_ids: List[str] = []
    failed: List[Dict[str, Any]] = []
    for tid in thread_ids:
        try:
            res = await _resolve_review_thread(gh, tid)
            if res.get("isResolved"):
                resolved_ids.append(tid)
            else:
                failed.append({"thread_id": tid, "error": "not resolved"})
        except Exception as e:
            failed.append({"thread_id": tid, "error": str(e)})

    return {"resolved_count": len(resolved_ids), "resolved_ids": resolved_ids, "failed": failed}


def main() -> None:
    # Defer MCP imports so the module can be imported without the optional dependency present
    from mcp import Server
    from mcp.server.stdio import stdio_server
    from pydantic import BaseModel

    server = Server("github-pr-mcp")

    class ListThreadsArgs(BaseModel):
        owner: str
        repo: str
        pull_number: int
        resolved: Optional[bool] = None

    @server.tool("list_review_threads", args_schema=ListThreadsArgs)
    async def list_review_threads(params: ListThreadsArgs):
        gh = GitHubGraphQLClient()
        items = await _list_review_threads(gh, params.owner, params.repo, params.pull_number, params.resolved)
        # Return as a compact JSON string for easier display
        return json.dumps(items, indent=2)

    class ThreadIdArgs(BaseModel):
        thread_id: str

    @server.tool("resolve_review_thread", args_schema=ThreadIdArgs)
    async def resolve_review_thread(params: ThreadIdArgs):
        gh = GitHubGraphQLClient()
        res = await _resolve_review_thread(gh, params.thread_id)
        return json.dumps(res, indent=2)

    @server.tool("unresolve_review_thread", args_schema=ThreadIdArgs)
    async def unresolve_review_thread(params: ThreadIdArgs):
        gh = GitHubGraphQLClient()
        res = await _unresolve_review_thread(gh, params.thread_id)
        return json.dumps(res, indent=2)

    class BulkResolveArgs(BaseModel):
        owner: str
        repo: str
        pull_number: int
        thread_ids: Optional[List[str]] = None

    @server.tool("bulk_resolve_threads", args_schema=BulkResolveArgs)
    async def bulk_resolve_threads(params: BulkResolveArgs):
        gh = GitHubGraphQLClient()
        summary = await _bulk_resolve_threads(
            gh, params.owner, params.repo, params.pull_number, params.thread_ids
        )
        return json.dumps(summary, indent=2)

    stdio_server.run(server)


if __name__ == "__main__":
    main()
