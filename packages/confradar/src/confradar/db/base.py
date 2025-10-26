from __future__ import annotations

from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from sqlalchemy import DateTime, func, create_engine
from contextlib import contextmanager


class Base(DeclarativeBase):
    pass


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )


def get_engine():
    """Get SQLAlchemy engine from settings."""
    from confradar.settings import Settings
    settings = Settings()
    return create_engine(settings.database_url)


def get_session() -> Session:
    """Create a new database session.
    
    Returns:
        SQLAlchemy session
        
    Example:
        >>> from confradar.db.base import get_session
        >>> session = get_session()
        >>> try:
        >>>     # Use session
        >>>     session.commit()
        >>> finally:
        >>>     session.close()
    """
    engine = get_engine()
    return Session(engine)


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations.
    
    Example:
        >>> from confradar.db.base import session_scope
        >>> with session_scope() as session:
        >>>     # Use session
        >>>     session.add(conference)
        >>> # Automatically commits or rolls back
    """
    session = get_session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()