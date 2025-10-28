"""Conference API routes."""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import func, or_, select

from confradar.db.models import Conference, Deadline

from .dependencies import DatabaseSession
from .schemas import (
    ConferenceListItem,
    ConferenceResponse,
    PaginatedResponse,
)

router = APIRouter(prefix="/api/conferences", tags=["conferences"])


@router.get("", response_model=PaginatedResponse[ConferenceListItem])
async def list_conferences(
    db: DatabaseSession,
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    field: str | None = Query(None, description="Filter by research field"),
    location: str | None = Query(None, description="Filter by location"),
    year: int | None = Query(None, description="Filter by conference year"),
    deadline_start: str | None = Query(None, description="Filter by deadline start date"),
    deadline_end: str | None = Query(None, description="Filter by deadline end date"),
    sort: Literal["name", "deadline", "date"] = Query("name", description="Sort by field"),
) -> PaginatedResponse[ConferenceListItem]:
    """List conferences with filtering, pagination, and sorting.
    
    Args:
        db: Database session
        page: Page number (1-indexed)
        limit: Items per page
        field: Filter by research field
        location: Filter by location
        year: Filter by conference year
        deadline_start: Filter by deadline start date (ISO format)
        deadline_end: Filter by deadline end date (ISO format)
        sort: Sort by field
        
    Returns:
        Paginated list of conferences
    """
    # Build base query
    query = select(Conference)
    
    # Apply filters (basic implementation - can be enhanced with metadata)
    # For now, filtering by name/key as field/location would need additional columns
    filters = []
    if field:
        # Search in name or key for field
        filters.append(or_(
            Conference.name.ilike(f"%{field}%"),
            Conference.key.ilike(f"%{field}%")
        ))
    
    if location:
        # Search in name for location
        filters.append(Conference.name.ilike(f"%{location}%"))
    
    # Deadline filters require join
    if deadline_start or deadline_end or year:
        query = query.join(Deadline)
        
        if deadline_start:
            filters.append(Deadline.due_date >= deadline_start)
        
        if deadline_end:
            filters.append(Deadline.due_date <= deadline_end)
            
        if year:
            filters.append(func.extract('year', Deadline.due_date) == year)
        
        # Distinct to avoid duplicates from join
        query = query.distinct()
    
    if filters:
        query = query.where(*filters)
    
    # Apply sorting
    if sort == "name":
        query = query.order_by(Conference.name)
    elif sort == "deadline" and (deadline_start or deadline_end or year):
        query = query.order_by(Deadline.due_date)
    else:
        query = query.order_by(Conference.name)
    
    # Count total
    count_query = select(func.count()).select_from(Conference)
    if filters:
        if deadline_start or deadline_end or year:
            count_query = count_query.join(Deadline).distinct()
        count_query = count_query.where(*filters)
    
    total = db.scalar(count_query) or 0
    
    # Apply pagination
    offset = (page - 1) * limit
    query = query.offset(offset).limit(limit)
    
    # Execute query
    conferences = db.scalars(query).all()
    
    # Calculate has_more
    has_more = (page * limit) < total
    
    return PaginatedResponse(
        items=[ConferenceListItem.model_validate(c) for c in conferences],
        total=total,
        page=page,
        limit=limit,
        has_more=has_more,
    )


@router.get("/search", response_model=PaginatedResponse[ConferenceListItem])
async def search_conferences(
    db: DatabaseSession,
    q: str = Query(..., min_length=1, description="Search query"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
) -> PaginatedResponse[ConferenceListItem]:
    """Full-text search for conferences.
    
    Args:
        db: Database session
        q: Search query
        page: Page number
        limit: Items per page
        
    Returns:
        Paginated search results
    """
    # Build search query
    search_filter = or_(
        Conference.name.ilike(f"%{q}%"),
        Conference.key.ilike(f"%{q}%"),
        Conference.homepage.ilike(f"%{q}%")
    )
    
    query = select(Conference).where(search_filter).order_by(Conference.name)
    
    # Count total
    count_query = select(func.count()).select_from(Conference).where(search_filter)
    total = db.scalar(count_query) or 0
    
    # Apply pagination
    offset = (page - 1) * limit
    query = query.offset(offset).limit(limit)
    
    # Execute query
    conferences = db.scalars(query).all()
    
    # Calculate has_more
    has_more = (page * limit) < total
    
    return PaginatedResponse(
        items=[ConferenceListItem.model_validate(c) for c in conferences],
        total=total,
        page=page,
        limit=limit,
        has_more=has_more,
    )


@router.get("/{conference_id}", response_model=ConferenceResponse)
async def get_conference(
    conference_id: int,
    db: DatabaseSession,
) -> ConferenceResponse:
    """Get conference details by ID.
    
    Args:
        conference_id: Conference ID
        db: Database session
        
    Returns:
        Conference details with deadlines and sources
        
    Raises:
        HTTPException: If conference not found
    """
    conference = db.get(Conference, conference_id)
    
    if not conference:
        raise HTTPException(status_code=404, detail="Conference not found")
    
    return ConferenceResponse.model_validate(conference)
