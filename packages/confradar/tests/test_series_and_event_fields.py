from __future__ import annotations

from datetime import date

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from confradar.db import Base, Conference, ConferenceSeries


def test_conference_series_and_event_fields(tmp_path):
    # Use SQLite for a fast, isolated test
    engine = create_engine(f"sqlite:///{tmp_path/'series.db'}", future=True)
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        series = ConferenceSeries(
            name="International Conference on Machine Learning", short_name="ICML"
        )
        session.add(series)
        session.flush()

        conf = Conference(
            key="icml_2025",
            name="ICML 2025",
            year=2025,
            location="Vienna, Austria",
            event_start_date=date(2025, 7, 12),
            event_end_date=date(2025, 7, 18),
            homepage="https://icml.cc",
            submission_url="https://cmt3.research.microsoft.com/ICML2025",
            series_id=series.id,
        )
        session.add(conf)
        session.commit()

    with Session(engine) as session:
        fetched = session.query(Conference).filter_by(key="icml_2025").one()
        assert fetched.series_id is not None
        assert fetched.year == 2025
        assert fetched.location == "Vienna, Austria"
        assert fetched.event_start_date.isoformat() == "2025-07-12"
        assert fetched.event_end_date.isoformat() == "2025-07-18"

        s = session.query(ConferenceSeries).filter_by(id=fetched.series_id).one()
        assert s.short_name == "ICML"
        # relationship population (optional; may be empty in SQLite without backrefs until refreshed)
        # ensure that at least one conference is linked
        assert len(session.query(Conference).filter_by(series_id=s.id).all()) == 1
