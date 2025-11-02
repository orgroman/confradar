from __future__ import annotations

from datetime import date

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin


class ConferenceSeries(TimestampMixin, Base):
    __tablename__ = "conference_series"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)  # Full series name
    short_name: Mapped[str] = mapped_column(String(64), nullable=False)  # Acronym
    homepage: Mapped[str | None] = mapped_column(String(512))
    notes: Mapped[str | None] = mapped_column(Text)

    __table_args__ = (
        UniqueConstraint("short_name", name="uq_series_short_name"),
        Index("ix_series_name", "name"),
    )

    conferences: Mapped[list[Conference]] = relationship(
        back_populates="series", cascade="all, delete-orphan"
    )


class Conference(TimestampMixin, Base):
    __tablename__ = "conferences"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    series_id: Mapped[int | None] = mapped_column(
        ForeignKey("conference_series.id", ondelete="SET NULL")
    )
    key: Mapped[str] = mapped_column(String(64), nullable=False)  # canonical key, e.g., neurips_2025
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    year: Mapped[int | None] = mapped_column()
    location: Mapped[str | None] = mapped_column(String(255))  # City, Country
    event_start_date: Mapped[date | None] = mapped_column()
    event_end_date: Mapped[date | None] = mapped_column()
    homepage: Mapped[str | None] = mapped_column(String(512))
    submission_url: Mapped[str | None] = mapped_column(String(512))
    notes: Mapped[str | None] = mapped_column(Text)

    __table_args__ = (
        UniqueConstraint("key", name="uq_conference_key"),
        Index("ix_conference_name", "name"),
        Index("ix_conference_year", "year"),
        Index("ix_conference_series", "series_id"),
        Index("ix_conference_dates", "event_start_date", "event_end_date"),
        CheckConstraint(
            "year IS NULL OR (year >= 2020 AND year <= 2035)",
            name="ck_conference_year",
        ),
    )

    series: Mapped[ConferenceSeries | None] = relationship(back_populates="conferences")
    deadlines: Mapped[list[Deadline]] = relationship(
        back_populates="conference", cascade="all, delete-orphan"
    )
    sources: Mapped[list[Source]] = relationship(
        back_populates="conference", cascade="all, delete-orphan"
    )


class Source(TimestampMixin, Base):
    __tablename__ = "sources"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    conference_id: Mapped[int] = mapped_column(ForeignKey("conferences.id", ondelete="CASCADE"))
    url: Mapped[str] = mapped_column(String(800), nullable=False)
    notes: Mapped[str | None] = mapped_column(Text)

    conference: Mapped[Conference] = relationship(back_populates="sources")
    __table_args__ = (
        UniqueConstraint("conference_id", "url", name="uq_source_conf_url"),
        Index("ix_source_url", "url"),
    )


class Deadline(TimestampMixin, Base):
    __tablename__ = "deadlines"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    conference_id: Mapped[int] = mapped_column(ForeignKey("conferences.id", ondelete="CASCADE"))
    kind: Mapped[str] = mapped_column(
        String(64), nullable=False
    )  # submission, notification, camera_ready, etc.
    due_date: Mapped[date] = mapped_column(nullable=False)
    timezone: Mapped[str | None] = mapped_column(String(64))  # e.g., AoE, UTC, etc.
    source_id: Mapped[int | None] = mapped_column(ForeignKey("sources.id"))

    conference: Mapped[Conference] = relationship(back_populates="deadlines")
    source: Mapped[Source | None] = relationship()
    __table_args__ = (
        UniqueConstraint("conference_id", "kind", "due_date", name="uq_deadline_unique"),
        Index("ix_deadline_due_date", "due_date"),
    )
