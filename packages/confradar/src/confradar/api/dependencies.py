"""FastAPI dependencies."""

from __future__ import annotations

from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from confradar.db.base import get_session


def get_db() -> Session:
    """Get database session dependency.
    
    Yields:
        Database session
    """
    session = get_session()
    try:
        yield session
    finally:
        session.close()


# Type alias for dependency injection
DatabaseSession = Annotated[Session, Depends(get_db)]
