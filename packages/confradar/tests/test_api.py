"""Tests for FastAPI endpoints."""

from __future__ import annotations

from datetime import date, timedelta

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from confradar.api.app import create_app
from confradar.db import Base, Conference, Deadline, Source


@pytest.fixture
def test_db(tmp_path):
    """Create a test database with sample data."""
    db_path = tmp_path / "test.db"
    engine = create_engine(f"sqlite:///{db_path}", future=True)
    Base.metadata.create_all(engine)
    
    with Session(engine) as session:
        # Create test conferences
        conf1 = Conference(key="neurips", name="NeurIPS 2025", homepage="https://neurips.cc")
        conf2 = Conference(key="icml", name="ICML 2025", homepage="https://icml.cc")
        conf3 = Conference(key="acl", name="ACL 2025", homepage="https://aclanthology.org")
        session.add_all([conf1, conf2, conf3])
        session.flush()
        
        # Add sources
        src1 = Source(conference_id=conf1.id, url="https://neurips.cc/cfp")
        src2 = Source(conference_id=conf2.id, url="https://icml.cc/cfp")
        session.add_all([src1, src2])
        session.flush()
        
        # Add deadlines
        today = date.today()
        deadlines = [
            Deadline(
                conference_id=conf1.id,
                kind="submission",
                due_date=today + timedelta(days=10),
                timezone="AoE",
                source_id=src1.id,
            ),
            Deadline(
                conference_id=conf2.id,
                kind="submission",
                due_date=today + timedelta(days=20),
                timezone="UTC",
                source_id=src2.id,
            ),
            Deadline(
                conference_id=conf3.id,
                kind="submission",
                due_date=today + timedelta(days=50),
                timezone="AoE",
            ),
            Deadline(
                conference_id=conf1.id,
                kind="notification",
                due_date=today + timedelta(days=60),
                timezone="AoE",
            ),
        ]
        session.add_all(deadlines)
        session.commit()
    
    return f"sqlite:///{db_path}"


@pytest.fixture
def app(test_db, monkeypatch):
    """Create FastAPI app with test database."""
    monkeypatch.setenv("DATABASE_URL", test_db)
    
    # Reload settings to pick up new DATABASE_URL
    from confradar import settings as settings_module
    settings_module.settings = settings_module.Settings()
    
    return create_app()


@pytest.mark.asyncio
async def test_health_check(app):
    """Test health check endpoint."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["database"] == "healthy"
        assert "timestamp" in data


@pytest.mark.asyncio
async def test_list_conferences(app):
    """Test list conferences endpoint."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/conferences")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "page" in data
        assert "limit" in data
        assert "has_more" in data
        assert data["total"] == 3
        assert len(data["items"]) == 3
        assert data["page"] == 1
        assert data["limit"] == 20
        assert data["has_more"] is False


@pytest.mark.asyncio
async def test_list_conferences_pagination(app):
    """Test pagination in list conferences."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Get page 1 with limit 2
        response = await client.get("/api/conferences?page=1&limit=2")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 3
        assert len(data["items"]) == 2
        assert data["has_more"] is True
        
        # Get page 2 with limit 2
        response = await client.get("/api/conferences?page=2&limit=2")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 3
        assert len(data["items"]) == 1
        assert data["has_more"] is False


@pytest.mark.asyncio
async def test_get_conference_details(app):
    """Test get conference details endpoint."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/conferences/1")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["key"] == "neurips"
        assert data["name"] == "NeurIPS 2025"
        assert "deadlines" in data
        assert "sources" in data
        assert len(data["deadlines"]) == 2  # submission and notification
        assert len(data["sources"]) == 1


@pytest.mark.asyncio
async def test_get_conference_not_found(app):
    """Test get conference with invalid ID."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/conferences/999")
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data


@pytest.mark.asyncio
async def test_search_conferences(app):
    """Test search conferences endpoint."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Search for "NeurIPS"
        response = await client.get("/api/conferences/search?q=NeurIPS")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 1
        assert any(item["name"] == "NeurIPS 2025" for item in data["items"])
        
        # Search for "ICML"
        response = await client.get("/api/conferences/search?q=ICML")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 1
        assert any(item["name"] == "ICML 2025" for item in data["items"])


@pytest.mark.asyncio
async def test_search_conferences_no_query(app):
    """Test search without query parameter."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/conferences/search")
        assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_upcoming_deadlines(app):
    """Test upcoming deadlines endpoint."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Get deadlines for next 30 days
        response = await client.get("/api/deadlines/upcoming?days=30")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert data["total"] >= 2  # Should have at least 2 deadlines within 30 days
        
        # Verify deadline has conference info
        if data["items"]:
            deadline = data["items"][0]
            assert "conference" in deadline
            assert "id" in deadline["conference"]
            assert "name" in deadline["conference"]


@pytest.mark.asyncio
async def test_upcoming_deadlines_days_filter(app):
    """Test upcoming deadlines with different day ranges."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Get deadlines for next 15 days (should have 1)
        response = await client.get("/api/deadlines/upcoming?days=15")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        
        # Get deadlines for next 90 days (should have all)
        response = await client.get("/api/deadlines/upcoming?days=90")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 4
