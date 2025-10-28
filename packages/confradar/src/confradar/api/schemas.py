"""Pydantic schemas for API responses."""

from __future__ import annotations

from datetime import date, datetime
from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict


class SourceResponse(BaseModel):
    """Source response schema."""

    id: int
    url: str
    notes: str | None = None

    model_config = ConfigDict(from_attributes=True)


class DeadlineResponse(BaseModel):
    """Deadline response schema."""

    id: int
    kind: str
    due_date: date
    timezone: str | None = None
    source_id: int | None = None

    model_config = ConfigDict(from_attributes=True)


class ConferenceResponse(BaseModel):
    """Conference response schema."""

    id: int
    key: str
    name: str
    homepage: str | None = None
    created_at: datetime
    updated_at: datetime
    deadlines: list[DeadlineResponse] = []
    sources: list[SourceResponse] = []

    model_config = ConfigDict(from_attributes=True)


class ConferenceListItem(BaseModel):
    """Conference list item (minimal fields for listing)."""

    id: int
    key: str
    name: str
    homepage: str | None = None

    model_config = ConfigDict(from_attributes=True)


T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response wrapper."""

    items: list[T]
    total: int
    page: int
    limit: int
    has_more: bool


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    timestamp: datetime
    database: str
