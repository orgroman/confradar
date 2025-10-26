from __future__ import annotations

from datetime import date
from typing import Optional

from sqlalchemy import String, Text, UniqueConstraint, Index, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin


class Conference(TimestampMixin, Base):
    __tablename__ = "conferences"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    key: Mapped[str] = mapped_column(String(64), nullable=False)  # canonical key, e.g., neurips
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    homepage: Mapped[Optional[str]] = mapped_column(String(512))

    __table_args__ = (
        UniqueConstraint("key", name="uq_conference_key"),
        Index("ix_conference_name", "name"),
    )

    deadlines: Mapped[list["Deadline"]] = relationship(back_populates="conference", cascade="all, delete-orphan")
    sources: Mapped[list["Source"]] = relationship(back_populates="conference", cascade="all, delete-orphan")


class Source(TimestampMixin, Base):
    __tablename__ = "sources"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    conference_id: Mapped[int] = mapped_column(ForeignKey("conferences.id", ondelete="CASCADE"))
    url: Mapped[str] = mapped_column(String(800), nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(Text)

    conference: Mapped[Conference] = relationship(back_populates="sources")
    __table_args__ = (
        UniqueConstraint("conference_id", "url", name="uq_source_conf_url"),
        Index("ix_source_url", "url"),
    )


class Deadline(TimestampMixin, Base):
    __tablename__ = "deadlines"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    conference_id: Mapped[int] = mapped_column(ForeignKey("conferences.id", ondelete="CASCADE"))
    kind: Mapped[str] = mapped_column(String(64), nullable=False)  # submission, notification, camera_ready, etc.
    due_date: Mapped[date] = mapped_column(nullable=False)
    timezone: Mapped[Optional[str]] = mapped_column(String(64))  # e.g., AoE, UTC, etc.
    source_id: Mapped[Optional[int]] = mapped_column(ForeignKey("sources.id"))

    conference: Mapped[Conference] = relationship(back_populates="deadlines")
    source: Mapped[Optional[Source]] = relationship()
    __table_args__ = (
        UniqueConstraint("conference_id", "kind", "due_date", name="uq_deadline_unique"),
        Index("ix_deadline_due_date", "due_date"),
    )
