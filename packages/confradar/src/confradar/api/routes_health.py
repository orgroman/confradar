"""Health check and utility routes."""

from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter
from sqlalchemy import text

from .dependencies import DatabaseSession
from .schemas import HealthResponse

router = APIRouter(prefix="/api", tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check(db: DatabaseSession) -> HealthResponse:
    """Health check endpoint.
    
    Args:
        db: Database session
        
    Returns:
        Health status
    """
    # Check database connectivity
    try:
        db.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
    
    return HealthResponse(
        status="ok" if db_status == "healthy" else "degraded",
        timestamp=datetime.now(),
        database=db_status,
    )
