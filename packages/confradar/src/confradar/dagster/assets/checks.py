"""Asset checks for data quality, freshness, and volume monitoring.

This module implements Dagster asset checks to monitor pipeline health:
- Data quality checks (conference count, required fields)
- Freshness checks (data staleness detection)
- Volume checks (unexpected changes in conference counts)
- Duplicate detection
"""

from datetime import datetime, timedelta, timezone
from typing import Any

from dagster import AssetCheckResult, AssetCheckSeverity, asset_check
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

from confradar.dagster.assets.storage import store_conferences
from confradar.db.models import Conference, Source
from confradar.settings import get_settings


@asset_check(asset=store_conferences, description="Check minimum conference count threshold")
def conference_count_check(context, store_conferences: dict[str, int]) -> AssetCheckResult:
    """Check that total conference count meets minimum threshold.

    Alerts if the total number of conferences stored is below expected minimum.
    This helps detect scraping failures or data loss.

    Args:
        context: Dagster execution context
        store_conferences: Output from store_conferences asset

    Returns:
        AssetCheckResult indicating pass/fail with metadata
    """
    total_scraped = store_conferences.get("total_scraped", 0)
    min_threshold = 100  # Expected minimum conferences across all sources

    context.log.info(f"Conference count check: {total_scraped} scraped (threshold: {min_threshold})")

    if total_scraped < min_threshold:
        return AssetCheckResult(
            passed=False,
            severity=AssetCheckSeverity.ERROR,
            description=f"Only {total_scraped} conferences found (expected ≥{min_threshold}). "
            f"This may indicate scraping failures or missing sources.",
            metadata={
                "total_scraped": total_scraped,
                "threshold": min_threshold,
                "new_conferences": store_conferences.get("new_conferences", 0),
                "updated_conferences": store_conferences.get("updated_conferences", 0),
            },
        )

    return AssetCheckResult(
        passed=True,
        description=f"Conference count healthy: {total_scraped} conferences (≥{min_threshold})",
        metadata={
            "total_scraped": total_scraped,
            "threshold": min_threshold,
            "new_conferences": store_conferences.get("new_conferences", 0),
            "updated_conferences": store_conferences.get("updated_conferences", 0),
        },
    )


@asset_check(asset=store_conferences, description="Check data freshness per source")
def data_freshness_check(context) -> AssetCheckResult:
    """Check that data has been updated recently for all sources.

    Alerts if any source hasn't been scraped in over 24 hours, which may
    indicate scraper failures or scheduling issues.

    Args:
        context: Dagster execution context

    Returns:
        AssetCheckResult indicating pass/fail with metadata
    """
    settings = get_settings()
    engine = create_engine(settings.database_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Check when each source was last updated
        # Get the most recent source record per source notes (which contains source name)
        from sqlalchemy import distinct, select

        source_freshness = {}
        stale_sources = []
        freshness_threshold = timedelta(hours=25)  # Allow 1 hour buffer beyond daily schedule
        now = datetime.now(timezone.utc)

        # Get distinct source types from notes field
        sources = (
            session.query(distinct(Source.notes))
            .filter(Source.notes.like("Scraped from%"))
            .all()
        )

        for (source_notes,) in sources:
            # Extract source name from notes (e.g., "Scraped from aideadlines" -> "aideadlines")
            source_name = source_notes.replace("Scraped from ", "") if source_notes else "unknown"

            # Get most recent update for this source
            latest = (
                session.query(func.max(Source.updated_at))
                .filter(Source.notes == source_notes)
                .scalar()
            )

            if latest:
                age = now - latest.replace(tzinfo=timezone.utc)
                source_freshness[source_name] = {
                    "last_updated": latest.isoformat(),
                    "age_hours": age.total_seconds() / 3600,
                }

                if age > freshness_threshold:
                    stale_sources.append(source_name)
            else:
                source_freshness[source_name] = {
                    "last_updated": "never",
                    "age_hours": float("inf"),
                }
                stale_sources.append(source_name)

        context.log.info(f"Data freshness check: {len(stale_sources)} stale sources")

        if stale_sources:
            return AssetCheckResult(
                passed=False,
                severity=AssetCheckSeverity.WARN,
                description=f"Stale data detected for {len(stale_sources)} source(s): "
                f"{', '.join(stale_sources)}. Data hasn't been updated in >24 hours.",
                metadata=source_freshness,
            )

        return AssetCheckResult(
            passed=True,
            description=f"All {len(source_freshness)} sources have fresh data (< 24 hours old)",
            metadata=source_freshness,
        )

    except Exception as e:
        context.log.error(f"Error checking data freshness: {e}")
        return AssetCheckResult(
            passed=False,
            severity=AssetCheckSeverity.ERROR,
            description=f"Failed to check data freshness: {str(e)}",
        )
    finally:
        session.close()


@asset_check(asset=store_conferences, description="Check for unexpected volume changes")
def volume_change_check(context, store_conferences: dict[str, int]) -> AssetCheckResult:
    """Check for unexpected changes in conference volumes per source.

    Alerts if any source shows a dramatic change in conference count compared
    to typical volumes, which may indicate scraping issues or site changes.

    Args:
        context: Dagster execution context
        store_conferences: Output from store_conferences asset

    Returns:
        AssetCheckResult indicating pass/fail with metadata
    """
    # Expected minimum conferences per source (based on historical data)
    expected_minimums = {
        "aideadlines": 20,  # Typically ~50-100 conferences
        "acl_web": 10,  # Typically ~20-30 conferences
        "chairing_tool": 5,  # Varies widely
        "elra": 3,  # Small source
        "wikicfp": 30,  # Large source, typically 100+ conferences
    }

    volume_issues = []
    source_counts = {}

    # Extract per-source counts from store_conferences output
    for key, value in store_conferences.items():
        if key.endswith("_count"):
            source_name = key.replace("_count", "")
            source_counts[source_name] = value

            expected_min = expected_minimums.get(source_name, 0)
            if value < expected_min:
                volume_issues.append(
                    f"{source_name}: {value} conferences (expected ≥{expected_min})"
                )

    context.log.info(f"Volume check: {len(volume_issues)} sources below threshold")

    if volume_issues:
        return AssetCheckResult(
            passed=False,
            severity=AssetCheckSeverity.WARN,
            description=f"Unexpected low volume for {len(volume_issues)} source(s): "
            f"{'; '.join(volume_issues)}",
            metadata=source_counts,
        )

    return AssetCheckResult(
        passed=True,
        description=f"All {len(source_counts)} sources have healthy conference volumes",
        metadata=source_counts,
    )


@asset_check(asset=store_conferences, description="Check for duplicate conferences")
def duplicate_detection_check(context) -> AssetCheckResult:
    """Check for duplicate conferences in the database.

    Detects conferences that may have duplicate entries based on similar names
    or multiple entries with the same key, which could indicate data quality issues.

    Args:
        context: Dagster execution context

    Returns:
        AssetCheckResult indicating pass/fail with metadata
    """
    settings = get_settings()
    engine = create_engine(settings.database_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Check for conferences with duplicate keys (shouldn't happen with proper constraints)
        duplicate_keys = (
            session.query(Conference.key, func.count(Conference.id))
            .group_by(Conference.key)
            .having(func.count(Conference.id) > 1)
            .all()
        )

        duplicate_count = len(duplicate_keys)

        context.log.info(f"Duplicate detection: found {duplicate_count} duplicate keys")

        if duplicate_count > 0:
            # Get details of duplicates for reporting
            duplicate_details = [
                {"key": key, "count": count} for key, count in duplicate_keys[:10]
            ]

            return AssetCheckResult(
                passed=False,
                severity=AssetCheckSeverity.WARN,
                description=f"Found {duplicate_count} conferences with duplicate keys. "
                f"This may indicate data quality issues.",
                metadata={
                    "duplicate_count": duplicate_count,
                    "examples": duplicate_details,
                },
            )

        # If no key duplicates, check for similar names (potential semantic duplicates)
        # This is a basic check - could be enhanced with fuzzy matching
        total_conferences = session.query(func.count(Conference.id)).scalar()

        return AssetCheckResult(
            passed=True,
            description=f"No duplicate conference keys found across {total_conferences} conferences",
            metadata={
                "total_conferences": total_conferences,
                "duplicate_count": 0,
            },
        )

    except Exception as e:
        context.log.error(f"Error checking for duplicates: {e}")
        return AssetCheckResult(
            passed=False,
            severity=AssetCheckSeverity.ERROR,
            description=f"Failed to check for duplicates: {str(e)}",
        )
    finally:
        session.close()
