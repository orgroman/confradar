"""Tests for GitHub PR MCP server."""
from __future__ import annotations

import json
from typing import Any, Dict
from unittest.mock import AsyncMock, patch

import pytest

from server import (
    GitHubGraphQLClient,
    _add_comment_to_thread,
    _bulk_resolve_threads,
    _list_review_threads,
    _resolve_review_thread,
    _unresolve_review_thread,
)


@pytest.fixture
def mock_gh_client():
    """Create a mock GitHubGraphQLClient."""
    with patch.object(GitHubGraphQLClient, "__init__", return_value=None):
        client = GitHubGraphQLClient()
        client.query = AsyncMock()
        return client


@pytest.mark.asyncio
async def test_list_review_threads_all(mock_gh_client):
    """Test listing all review threads."""
    mock_gh_client.query.return_value = {
        "repository": {
            "pullRequest": {
                "reviewThreads": {
                    "nodes": [
                        {
                            "id": "PRRT_1",
                            "isResolved": False,
                            "comments": {"nodes": [{"id": "C1", "body": "Comment 1"}]},
                        },
                        {
                            "id": "PRRT_2",
                            "isResolved": True,
                            "comments": {"nodes": [{"id": "C2", "body": "Comment 2"}]},
                        },
                    ]
                }
            }
        }
    }

    result = await _list_review_threads(mock_gh_client, "owner", "repo", 123)

    assert len(result) == 2
    assert result[0]["id"] == "PRRT_1"
    assert result[1]["id"] == "PRRT_2"
    mock_gh_client.query.assert_called_once()


@pytest.mark.asyncio
async def test_list_review_threads_filtered(mock_gh_client):
    """Test listing review threads filtered by resolution status."""
    mock_gh_client.query.return_value = {
        "repository": {
            "pullRequest": {
                "reviewThreads": {
                    "nodes": [
                        {
                            "id": "PRRT_1",
                            "isResolved": False,
                            "comments": {"nodes": [{"id": "C1", "body": "Comment 1"}]},
                        },
                        {
                            "id": "PRRT_2",
                            "isResolved": True,
                            "comments": {"nodes": [{"id": "C2", "body": "Comment 2"}]},
                        },
                    ]
                }
            }
        }
    }

    # Test filtering for unresolved only
    result = await _list_review_threads(mock_gh_client, "owner", "repo", 123, resolved=False)

    assert len(result) == 1
    assert result[0]["id"] == "PRRT_1"
    assert result[0]["isResolved"] is False


@pytest.mark.asyncio
async def test_resolve_review_thread(mock_gh_client):
    """Test resolving a single review thread."""
    mock_gh_client.query.return_value = {
        "resolveReviewThread": {"thread": {"id": "PRRT_1", "isResolved": True}}
    }

    result = await _resolve_review_thread(mock_gh_client, "PRRT_1")

    assert result["id"] == "PRRT_1"
    assert result["isResolved"] is True
    mock_gh_client.query.assert_called_once()


@pytest.mark.asyncio
async def test_unresolve_review_thread(mock_gh_client):
    """Test unresolving a single review thread."""
    mock_gh_client.query.return_value = {
        "unresolveReviewThread": {"thread": {"id": "PRRT_1", "isResolved": False}}
    }

    result = await _unresolve_review_thread(mock_gh_client, "PRRT_1")

    assert result["id"] == "PRRT_1"
    assert result["isResolved"] is False
    mock_gh_client.query.assert_called_once()


@pytest.mark.asyncio
async def test_bulk_resolve_threads_with_ids(mock_gh_client):
    """Test bulk resolving specific threads by ID."""
    mock_gh_client.query.side_effect = [
        {"resolveReviewThread": {"thread": {"id": "PRRT_1", "isResolved": True}}},
        {"resolveReviewThread": {"thread": {"id": "PRRT_2", "isResolved": True}}},
    ]

    result = await _bulk_resolve_threads(
        mock_gh_client, "owner", "repo", 123, thread_ids=["PRRT_1", "PRRT_2"]
    )

    assert result["resolved_count"] == 2
    assert len(result["resolved_ids"]) == 2
    assert len(result["failed"]) == 0
    assert mock_gh_client.query.call_count == 2


@pytest.mark.asyncio
async def test_bulk_resolve_threads_auto_fetch(mock_gh_client):
    """Test bulk resolving all unresolved threads (auto-fetch)."""
    # First call: list unresolved threads
    # Subsequent calls: resolve each thread
    mock_gh_client.query.side_effect = [
        {
            "repository": {
                "pullRequest": {
                    "reviewThreads": {
                        "nodes": [
                            {
                                "id": "PRRT_1",
                                "isResolved": False,
                                "comments": {"nodes": []},
                            },
                            {
                                "id": "PRRT_2",
                                "isResolved": False,
                                "comments": {"nodes": []},
                            },
                        ]
                    }
                }
            }
        },
        {"resolveReviewThread": {"thread": {"id": "PRRT_1", "isResolved": True}}},
        {"resolveReviewThread": {"thread": {"id": "PRRT_2", "isResolved": True}}},
    ]

    result = await _bulk_resolve_threads(mock_gh_client, "owner", "repo", 123)

    assert result["resolved_count"] == 2
    assert result["resolved_ids"] == ["PRRT_1", "PRRT_2"]
    assert len(result["failed"]) == 0
    assert mock_gh_client.query.call_count == 3  # 1 list + 2 resolve


@pytest.mark.asyncio
async def test_bulk_resolve_threads_partial_failure(mock_gh_client):
    """Test bulk resolve handling partial failures."""
    mock_gh_client.query.side_effect = [
        {"resolveReviewThread": {"thread": {"id": "PRRT_1", "isResolved": True}}},
        RuntimeError("Network error"),
    ]

    result = await _bulk_resolve_threads(
        mock_gh_client, "owner", "repo", 123, thread_ids=["PRRT_1", "PRRT_2"]
    )

    assert result["resolved_count"] == 1
    assert result["resolved_ids"] == ["PRRT_1"]
    assert len(result["failed"]) == 1
    assert result["failed"][0]["thread_id"] == "PRRT_2"
    assert "Network error" in result["failed"][0]["error"]


@pytest.mark.asyncio
async def test_github_client_missing_token():
    """Test that GitHubGraphQLClient raises error when token is missing."""
    with patch.dict("os.environ", {}, clear=True):
        with pytest.raises(RuntimeError, match="Missing GitHub token"):
            GitHubGraphQLClient()


@pytest.mark.asyncio
async def test_github_client_graphql_error():
    """Test that GitHubGraphQLClient handles GraphQL errors."""
    with patch.dict("os.environ", {"GITHUB_TOKEN": "fake-token"}):
        client = GitHubGraphQLClient()
        
        # Mock the entire async context manager and post call
        mock_response = AsyncMock()
        mock_response.json = lambda: {"errors": [{"message": "Resource not found"}]}
        mock_response.raise_for_status = lambda: None
        
        mock_client = AsyncMock()
        mock_client.post = AsyncMock(return_value=mock_response)
        
        with patch("httpx.AsyncClient") as mock_client_cls:
            mock_client_cls.return_value.__aenter__.return_value = mock_client
            
            with pytest.raises(RuntimeError, match="GraphQL errors"):
                await client.query("query { }", {})


@pytest.mark.asyncio
async def test_add_comment_to_thread():
    """Test adding a comment to a review thread."""
    with patch.dict("os.environ", {"GITHUB_TOKEN": "fake-token"}):
        client = GitHubGraphQLClient()
        
        # Mock the response
        mock_response = AsyncMock()
        mock_response.json = lambda: {
            "data": {
                "addPullRequestReviewThreadReply": {
                    "comment": {
                        "id": "PRRC_test123",
                        "url": "https://github.com/owner/repo/pull/1#discussion_r123456",
                        "body": "This is my justification comment"
                    }
                }
            }
        }
        mock_response.raise_for_status = lambda: None
        
        mock_client = AsyncMock()
        mock_client.post = AsyncMock(return_value=mock_response)
        
        with patch("httpx.AsyncClient") as mock_client_cls:
            mock_client_cls.return_value.__aenter__.return_value = mock_client
            
            result = await _add_comment_to_thread(
                client, "PRRT_thread123", "This is my justification comment"
            )
            
            assert result["id"] == "PRRC_test123"
            assert "justification" in result["body"]
            assert result["url"].startswith("https://github.com")

