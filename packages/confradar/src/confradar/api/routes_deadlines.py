"""Deadlines API routes."""

from __future__ import annotations

from datetime import date, datetime, timedelta

from fastapi import APIRouter, Query
from sqlalchemy import select

from confradar.db.models import Conference, Deadline

from .dependencies import DatabaseSession
from .schemas import ConferenceListItem, DeadlineResponse, PaginatedResponse

router = APIRouter(prefix="/api/deadlines", tags=["deadlines"])


class DeadlineWithConference(DeadlineResponse):
    """Deadline with associated conference information."""

    conference: ConferenceListItem


@router.get("/upcoming", response_model=PaginatedResponse[DeadlineWithConference])
async def get_upcoming_deadlines(
    db: DatabaseSession,
    days: int = Query(30, ge=1, le=365, description="Number of days to look ahead"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
) -> PaginatedResponse[DeadlineWithConference]:
    """Get upcoming deadlines within specified days.
    
    Args:
        db: Database session
        days: Number of days to look ahead (default: 30)
        page: Page number
        limit: Items per page
        
    Returns:
        Paginated list of upcoming deadlines with conference info
    """
    today = date.today()
    end_date = today + timedelta(days=days)
    
    # Build query with join to get conference info
    query = (
        select(Deadline, Conference)
        .join(Conference)
        .where(Deadline.due_date >= today, Deadline.due_date <= end_date)
        .order_by(Deadline.due_date)
    )
    
    # Count total
    from sqlalchemy import func
    
    count_query = (
        select(func.count())
        .select_from(Deadline)
        .where(Deadline.due_date >= today, Deadline.due_date <= end_date)
    )
    total = db.scalar(count_query) or 0
    
    # Apply pagination
    offset = (page - 1) * limit
    query = query.offset(offset).limit(limit)
    
    # Execute query
    results = db.execute(query).all()
    
    # Build response items
    items = []
    for deadline, conference in results:
        item_data = DeadlineResponse.model_validate(deadline).model_dump()
        item_data["conference"] = ConferenceListItem.model_validate(conference)
        items.append(DeadlineWithConference(**item_data))
    
    # Calculate has_more
    has_more = (page * limit) < total
    
    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        limit=limit,
        has_more=has_more,
    )
