"""
GitHub PR Conversations MCP Server

Implements MCP tools for managing pull request review threads via GitHub GraphQL.

Core tools:
- list_review_threads(owner, repo, pull_number, resolved?)
- resolve_review_thread(thread_id)
- unresolve_review_thread(thread_id)
- bulk_resolve_threads(owner, repo, pull_number, thread_ids?)

Auth:
- Uses a GitHub token from env: GITHUB_TOKEN or GH_TOKEN.
"""
from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Optional

import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("github-pr-mcp")

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

ADD_COMMENT_MUTATION = """
mutation($pullRequestId:ID!, $body:String!, $commitOID:GitObjectID!, $path:String!, $position:Int!) {
  addPullRequestReviewComment(input:{
    pullRequestId:$pullRequestId
    body:$body
    commitOID:$commitOID
    path:$path
    position:$position
  }) {
    comment { id url body }
  }
}
"""

ADD_REPLY_MUTATION = """
mutation($pullRequestReviewThreadId:ID!, $body:String!) {
  addPullRequestReviewThreadReply(input:{
    pullRequestReviewThreadId:$pullRequestReviewThreadId
    body:$body
  }) {
    comment { id url body }
  }
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


async def _add_comment_to_thread(
    gh: GitHubGraphQLClient, thread_id: str, body: str
) -> Dict[str, Any]:
    """Add a reply comment to an existing review thread."""
    data = await gh.query(
        ADD_REPLY_MUTATION, {"pullRequestReviewThreadId": thread_id, "body": body}
    )
    return data.get("addPullRequestReviewThreadReply", {}).get("comment", {})


async def _bulk_resolve_threads(
    gh: GitHubGraphQLClient,
    owner: str,
    repo: str,
    pull_number: int,
    thread_ids: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Resolve multiple review threads for a pull request.

    Args:
        gh: GitHubGraphQLClient instance.
        owner: Repository owner.
        repo: Repository name.
        pull_number: Pull request number.
        thread_ids: List of thread IDs to resolve. If None, all unresolved threads will be resolved.
            If an empty list is provided, zero threads will be resolved (no action).

    Returns:
        Dict with keys:
            - resolved_count: Number of threads successfully resolved.
            - resolved_ids: List of thread IDs that were resolved.
            - failed: List of dicts with thread_id and error for failures.
    """
    if thread_ids is None:
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


@mcp.tool()
async def list_review_threads(
    owner: str,
    repo: str,
    pull_number: int,
    resolved: Optional[bool] = None
) -> str:
    """List review threads for a pull request.
    
    Args:
        owner: Repository owner (username or organization)
        repo: Repository name
        pull_number: Pull request number
        resolved: Optional filter - True for resolved, False for unresolved, None for all
    """
    gh = GitHubGraphQLClient()
    items = await _list_review_threads(gh, owner, repo, pull_number, resolved)
    return json.dumps(items, indent=2)


@mcp.tool()
async def resolve_review_thread(thread_id: str) -> str:
    """Resolve a specific review thread.
    
    Args:
        thread_id: The GraphQL ID of the review thread to resolve
    """
    gh = GitHubGraphQLClient()
    res = await _resolve_review_thread(gh, thread_id)
    return json.dumps(res, indent=2)


@mcp.tool()
async def unresolve_review_thread(thread_id: str) -> str:
    """Unresolve a specific review thread.
    
    Args:
        thread_id: The GraphQL ID of the review thread to unresolve
    """
    gh = GitHubGraphQLClient()
    res = await _unresolve_review_thread(gh, thread_id)
    return json.dumps(res, indent=2)


@mcp.tool()
async def bulk_resolve_threads(
    owner: str,
    repo: str,
    pull_number: int,
    thread_ids: Optional[List[str]] = None
) -> str:
    """Resolve multiple review threads at once.
    
    Args:
        owner: Repository owner (username or organization)
        repo: Repository name
        pull_number: Pull request number
        thread_ids: Optional list of specific thread IDs to resolve. If None, resolves all unresolved threads
    """
    gh = GitHubGraphQLClient()
    summary = await _bulk_resolve_threads(gh, owner, repo, pull_number, thread_ids)
    return json.dumps(summary, indent=2)


@mcp.tool()
async def add_comment_to_thread(thread_id: str, body: str) -> str:
    """Add a reply comment to an existing review thread.
    
    Args:
        thread_id: The GraphQL ID of the review thread to comment on
        body: The comment body (markdown supported)
    """
    gh = GitHubGraphQLClient()
    comment = await _add_comment_to_thread(gh, thread_id, body)
    return json.dumps(comment, indent=2)


def main() -> None:
    """Run the MCP server."""
    mcp.run(transport='stdio')


if __name__ == "__main__":
    main()
