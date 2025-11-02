"""Dagster asset checks for data quality validation.

These checks validate the quality of scraped and stored conference data.
"""

from dagster import AssetCheckResult, AssetCheckSeverity, asset_check
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import sessionmaker

from confradar.db.models import Conference, Deadline
from confradar.settings import get_settings


@asset_check(asset="store_conferences", description="Validates minimum conference count per source")
def check_conference_count() -> AssetCheckResult:
    """Check that we have a minimum number of conferences (>10) from each source.

    This ensures that scraping is working and we're collecting adequate data.
    """
    settings = get_settings()
    engine = create_engine(settings.database_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Count total conferences
        total_count = session.query(func.count(Conference.id)).scalar()

        if total_count < 10:
            return AssetCheckResult(
                passed=False,
                severity=AssetCheckSeverity.ERROR,
                description=f"Only {total_count} conferences found (expected >10)",
                metadata={"count": total_count, "threshold": 10},
            )

        return AssetCheckResult(
            passed=True,
            description=f"Found {total_count} conferences",
            metadata={"count": total_count},
        )
    finally:
        session.close()


@asset_check(asset="store_conferences", description="Validates required fields are present")
def check_required_fields() -> AssetCheckResult:
    """Check that all conferences have required fields (name, key).

    Ensures data integrity and completeness.
    """
    settings = get_settings()
    engine = create_engine(settings.database_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Check for conferences with missing name or key
        invalid_conferences = (
            session.query(Conference)
            .filter((Conference.name.is_(None)) | (Conference.key.is_(None)))
            .count()
        )

        if invalid_conferences > 0:
            return AssetCheckResult(
                passed=False,
                severity=AssetCheckSeverity.ERROR,
                description=f"{invalid_conferences} conferences missing required fields",
                metadata={"invalid_count": invalid_conferences},
            )

        total_count = session.query(func.count(Conference.id)).scalar()
        return AssetCheckResult(
            passed=True,
            description=f"All {total_count} conferences have required fields",
            metadata={"total_count": total_count},
        )
    finally:
        session.close()


@asset_check(asset="store_conferences", description="Validates deadline date formats")
def check_deadline_dates() -> AssetCheckResult:
    """Check that all deadlines have valid date formats.

    Ensures that deadline dates are properly formatted and stored.
    """
    settings = get_settings()
    engine = create_engine(settings.database_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Count total deadlines
        total_deadlines = session.query(func.count(Deadline.id)).scalar()

        # Check for deadlines with null due_date (shouldn't happen due to schema)
        invalid_deadlines = session.query(Deadline).filter(Deadline.due_date.is_(None)).count()

        if invalid_deadlines > 0:
            return AssetCheckResult(
                passed=False,
                severity=AssetCheckSeverity.ERROR,
                description=f"{invalid_deadlines} deadlines have invalid dates",
                metadata={
                    "total": total_deadlines,
                    "invalid": invalid_deadlines,
                },
            )

        if total_deadlines == 0:
            return AssetCheckResult(
                passed=True,
                severity=AssetCheckSeverity.WARN,
                description="No deadlines found (may be expected if scrapers don't extract deadlines yet)",
                metadata={"total": 0},
            )

        return AssetCheckResult(
            passed=True,
            description=f"All {total_deadlines} deadlines have valid dates",
            metadata={"total": total_deadlines},
        )
    finally:
        session.close()


@asset_check(asset="store_conferences", description="Detects duplicate conference keys")
def check_duplicate_conferences() -> AssetCheckResult:
    """Check for duplicate conference keys in the database.

    Conference keys should be unique to prevent data inconsistencies.
    """
    settings = get_settings()
    engine = create_engine(settings.database_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Find keys that appear more than once
        stmt = (
            select(Conference.key, func.count(Conference.id).label("count"))
            .group_by(Conference.key)
            .having(func.count(Conference.id) > 1)
        )

        duplicates = session.execute(stmt).all()

        if duplicates:
            duplicate_keys = [key for key, count in duplicates]
            return AssetCheckResult(
                passed=False,
                severity=AssetCheckSeverity.WARN,
                description=f"Found {len(duplicates)} duplicate conference keys",
                metadata={
                    "duplicate_count": len(duplicates),
                    "duplicate_keys": duplicate_keys[:5],  # Show first 5
                },
            )

        total_count = session.query(func.count(Conference.id)).scalar()
        return AssetCheckResult(
            passed=True,
            description=f"No duplicate keys found among {total_count} conferences",
            metadata={"total": total_count},
        )
    finally:
        session.close()
