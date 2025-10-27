"""Tests for Dagster definitions and assets."""

import pytest
from dagster import materialize

from confradar.dagster.definitions import defs


def test_dagster_definitions_load():
    """Test that Dagster definitions load without errors."""
    assert defs is not None
    # Check that we have assets defined
    assert hasattr(defs, "assets")
    assert len(defs.assets) == 6  # 5 scrapers + 1 storage
    # Check that we have jobs defined
    assert hasattr(defs, "jobs")
    assert len(defs.jobs) > 0
    # Check that we have schedules defined
    assert hasattr(defs, "schedules")
    assert len(defs.schedules) > 0


def test_asset_names():
    """Test that all expected assets are defined."""
    asset_names = [a.key.to_user_string() for a in defs.assets]

    # Check scraper assets
    assert "ai_deadlines_conferences" in asset_names
    assert "acl_web_conferences" in asset_names
    assert "chairing_tool_conferences" in asset_names
    assert "elra_conferences" in asset_names
    assert "wikicfp_conferences" in asset_names

    # Check storage asset
    assert "store_conferences" in asset_names


def test_crawl_job_exists():
    """Test that the crawl job is defined."""
    job_names = [job.name for job in defs.jobs]
    assert "crawl_job" in job_names


def test_daily_schedule_exists():
    """Test that the daily crawl schedule is defined."""
    schedule_names = [s.name for s in defs.schedules]
    assert "daily_crawl_schedule" in schedule_names

    # Verify cron schedule
    daily_schedule = [s for s in defs.schedules if s.name == "daily_crawl_schedule"][0]
    assert daily_schedule.cron_schedule == "0 2 * * *"


@pytest.mark.integration
def test_materialize_mock_asset():
    """Test that we can materialize a simple asset (mock test).

    This is a sanity check that Dagster execution works.
    Real scraper tests should be run separately due to network calls.
    """
    from dagster import asset

    @asset
    def test_asset() -> int:
        return 42

    result = materialize([test_asset])
    assert result.success
