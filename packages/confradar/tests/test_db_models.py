from __future__ import annotations

from datetime import date

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from confradar.db import Base, Conference, Deadline, Source


def test_create_schema_and_insert_basic_entities(tmp_path):
    # Use a temporary SQLite database file
    db_path = tmp_path / "test.db"
    engine = create_engine(f"sqlite:///{db_path}", future=True)

    # Create schema
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        conf = Conference(key="neurips", name="NeurIPS", homepage="https://neurips.cc")
        session.add(conf)
        session.flush()  # get conf.id

        src = Source(conference_id=conf.id, url="https://neurips.cc/Conferences/2025/CallForPapers")
        session.add(src)
        session.flush()

        dl = Deadline(
            conference_id=conf.id,
            kind="submission",
            due_date=date(2025, 5, 20),
            timezone="AoE",
            source_id=src.id,
        )
        session.add(dl)

        session.commit()

    # Verify round-trip
    with Session(engine) as session:
        fetched = session.query(Conference).filter_by(key="neurips").one()
        assert fetched.name == "NeurIPS"
        assert len(fetched.deadlines) == 1
        d = fetched.deadlines[0]
        assert d.kind == "submission"
        assert d.due_date.isoformat() == "2025-05-20"


def test_unique_constraints(tmp_path):
    engine = create_engine(f"sqlite:///{tmp_path/'u.db'}", future=True)
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        c = Conference(key="acl", name="ACL")
        session.add(c)
        session.flush()

        session.add_all([
            Deadline(conference_id=c.id, kind="submission", due_date=date(2025, 1, 1)),
        ])
        session.commit()

        # Insert duplicate deadline should violate unique constraint
        session.add(Deadline(conference_id=c.id, kind="submission", due_date=date(2025, 1, 1)))
        try:
            session.commit()
            committed = True
        except Exception:
            session.rollback()
            committed = False

    assert committed is False
