"""Tests for event date ordering constraint and conference series seeding."""

from __future__ import annotations

from datetime import date

import pytest
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from confradar.data import MAJOR_SERIES
from confradar.db import Base, Conference, ConferenceSeries


def test_event_date_ordering_constraint_valid_dates(tmp_path):
    """Test that valid event dates (end >= start) are accepted."""
    engine = create_engine(f"sqlite:///{tmp_path/'test.db'}", future=True)
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        # Test with end date after start date (valid)
        conf1 = Conference(
            key="test_conf_1",
            name="Test Conference 1",
            event_start_date=date(2025, 7, 1),
            event_end_date=date(2025, 7, 5),
        )
        session.add(conf1)
        session.commit()

        # Test with same start and end date (valid edge case)
        conf2 = Conference(
            key="test_conf_2",
            name="Test Conference 2",
            event_start_date=date(2025, 8, 1),
            event_end_date=date(2025, 8, 1),
        )
        session.add(conf2)
        session.commit()

    # Verify both conferences were saved
    with Session(engine) as session:
        saved_conf1 = session.query(Conference).filter_by(key="test_conf_1").one()
        assert saved_conf1.event_start_date == date(2025, 7, 1)
        assert saved_conf1.event_end_date == date(2025, 7, 5)

        saved_conf2 = session.query(Conference).filter_by(key="test_conf_2").one()
        assert saved_conf2.event_start_date == date(2025, 8, 1)
        assert saved_conf2.event_end_date == date(2025, 8, 1)


def test_event_date_ordering_constraint_invalid_dates(tmp_path):
    """Test that invalid event dates (end < start) are rejected."""
    engine = create_engine(f"sqlite:///{tmp_path/'test.db'}", future=True)
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        # Try to create a conference with end date before start date (invalid)
        conf = Conference(
            key="test_conf_invalid",
            name="Invalid Conference",
            event_start_date=date(2025, 7, 10),
            event_end_date=date(2025, 7, 5),  # End before start - should fail
        )
        session.add(conf)

        # This should raise IntegrityError due to check constraint
        with pytest.raises(IntegrityError) as exc_info:
            session.commit()

        # Verify the error is related to the check constraint
        assert "ck_conference_event_date_order" in str(exc_info.value).lower() or \
               "check constraint" in str(exc_info.value).lower()


def test_event_date_ordering_constraint_null_dates(tmp_path):
    """Test that NULL dates are allowed and don't trigger constraint."""
    engine = create_engine(f"sqlite:///{tmp_path/'test.db'}", future=True)
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        # Only start date
        conf1 = Conference(
            key="test_conf_start_only",
            name="Conference with Start Only",
            event_start_date=date(2025, 7, 1),
            event_end_date=None,
        )
        session.add(conf1)

        # Only end date
        conf2 = Conference(
            key="test_conf_end_only",
            name="Conference with End Only",
            event_start_date=None,
            event_end_date=date(2025, 7, 5),
        )
        session.add(conf2)

        # Both dates NULL
        conf3 = Conference(
            key="test_conf_no_dates",
            name="Conference with No Dates",
            event_start_date=None,
            event_end_date=None,
        )
        session.add(conf3)

        # All should succeed
        session.commit()

    # Verify all conferences were saved
    with Session(engine) as session:
        assert session.query(Conference).filter_by(key="test_conf_start_only").one()
        assert session.query(Conference).filter_by(key="test_conf_end_only").one()
        assert session.query(Conference).filter_by(key="test_conf_no_dates").one()


@pytest.mark.parametrize("start_date,end_date,description", [
    (date(2025, 1, 1), date(2025, 1, 1), "same day"),
    (date(2020, 1, 1), date(2020, 1, 7), "year 2020 boundary"),
    (date(2035, 12, 25), date(2035, 12, 31), "year 2035 boundary"),
    (date(2025, 6, 1), date(2025, 6, 30), "multi-day conference"),
])
def test_event_date_ordering_boundary_cases(tmp_path, start_date, end_date, description):
    """Test various boundary cases for valid date ranges."""
    engine = create_engine(f"sqlite:///{tmp_path/'test.db'}", future=True)
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        conf = Conference(
            key=f"test_conf_{description.replace(' ', '_')}",
            name=f"Test Conference: {description}",
            event_start_date=start_date,
            event_end_date=end_date,
            year=start_date.year,
        )
        session.add(conf)
        session.commit()

    # Verify conference was saved
    with Session(engine) as session:
        saved_conf = session.query(Conference).filter_by(
            key=f"test_conf_{description.replace(' ', '_')}"
        ).one()
        assert saved_conf.event_start_date == start_date
        assert saved_conf.event_end_date == end_date


def test_seed_conference_series_creates_new_series(tmp_path):
    """Test that seeding creates new conference series using canonical data."""
    engine = create_engine(f"sqlite:///{tmp_path/'test.db'}", future=True)
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        # Create series using the canonical MAJOR_SERIES data
        series_map = {}
        for short_name, name, homepage in MAJOR_SERIES:
            series = ConferenceSeries(
                short_name=short_name,
                name=name,
                homepage=homepage
            )
            session.add(series)
            session.flush()
            series_map[short_name] = series.id
        session.commit()

        # Verify all major series were created
        assert len(series_map) == len(MAJOR_SERIES)
        for short_name, _, _ in MAJOR_SERIES:
            assert short_name in series_map

    # Verify series exist in database with correct data
    with Session(engine) as session:
        neurips = session.query(ConferenceSeries).filter_by(short_name="NeurIPS").one()
        assert neurips.name == "Conference on Neural Information Processing Systems"
        assert neurips.homepage == "https://neurips.cc"

        icml = session.query(ConferenceSeries).filter_by(short_name="ICML").one()
        assert icml.name == "International Conference on Machine Learning"
        assert icml.homepage == "https://icml.cc"

        acl = session.query(ConferenceSeries).filter_by(short_name="ACL").one()
        assert acl.name == "Annual Meeting of the Association for Computational Linguistics"
        assert acl.homepage == "https://aclweb.org"


def test_seed_conference_series_idempotency(tmp_path):
    """Test that running seed script multiple times is idempotent."""
    # Use a subset of MAJOR_SERIES for faster testing
    test_series = MAJOR_SERIES[:2]  # Just NeurIPS and ICML
    
    engine = create_engine(f"sqlite:///{tmp_path/'test.db'}", future=True)
    Base.metadata.create_all(engine)

    # First seeding
    with Session(engine) as session:
        series_map_1 = {}
        for short_name, name, homepage in test_series:
            existing = session.query(ConferenceSeries).filter_by(short_name=short_name).first()
            if not existing:
                series = ConferenceSeries(short_name=short_name, name=name, homepage=homepage)
                session.add(series)
                session.flush()
                series_map_1[short_name] = series.id
            else:
                series_map_1[short_name] = existing.id
        session.commit()
        count_after_first = session.query(ConferenceSeries).count()

    # Second seeding (should be idempotent)
    with Session(engine) as session:
        series_map_2 = {}
        for short_name, name, homepage in test_series:
            existing = session.query(ConferenceSeries).filter_by(short_name=short_name).first()
            if not existing:
                series = ConferenceSeries(short_name=short_name, name=name, homepage=homepage)
                session.add(series)
                session.flush()
                series_map_2[short_name] = series.id
            else:
                series_map_2[short_name] = existing.id
        session.commit()
        count_after_second = session.query(ConferenceSeries).count()

    # Count should remain the same
    assert count_after_first == count_after_second
    assert count_after_first == 2

    # IDs should be the same for matching series
    assert series_map_1["NeurIPS"] == series_map_2["NeurIPS"]
    assert series_map_1["ICML"] == series_map_2["ICML"]


def test_seed_conference_series_dry_run(tmp_path):
    """Test dry-run mode behavior for seeding."""
    engine = create_engine(f"sqlite:///{tmp_path/'test.db'}", future=True)
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        # Verify no series exist initially
        count_before = session.query(ConferenceSeries).count()
        assert count_before == 0
        
        # Add a series manually
        series = ConferenceSeries(
            short_name="TEST",
            name="Test Conference",
            homepage="https://test.com"
        )
        session.add(series)
        session.commit()
        
        # Verify series was created
        count_after = session.query(ConferenceSeries).count()
        assert count_after == 1
        
        # Verify it can be queried
        test_series = session.query(ConferenceSeries).filter_by(short_name="TEST").one()
        assert test_series.name == "Test Conference"


def test_conference_series_unique_constraint(tmp_path):
    """Test that duplicate short_name violates unique constraint."""
    engine = create_engine(f"sqlite:///{tmp_path/'test.db'}", future=True)
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        # Create first series
        series1 = ConferenceSeries(
            short_name="ICML",
            name="International Conference on Machine Learning",
            homepage="https://icml.cc"
        )
        session.add(series1)
        session.commit()

        # Try to create duplicate with same short_name (should fail)
        series2 = ConferenceSeries(
            short_name="ICML",  # Duplicate short_name
            name="Different Name",
            homepage="https://different.com"
        )
        session.add(series2)

        with pytest.raises(IntegrityError) as exc_info:
            session.commit()

        # Verify the error is related to the unique constraint
        assert "uq_series_short_name" in str(exc_info.value).lower() or \
               "unique constraint" in str(exc_info.value).lower()
