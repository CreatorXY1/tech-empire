from collections.abc import Generator
from functools import lru_cache

from fastapi import HTTPException, status
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import get_database_url


@lru_cache(maxsize=1)
def get_engine() -> Engine:
    """Create the backend's lazy PostgreSQL engine."""
    return create_engine(
        get_database_url(),
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=5,
        connect_args={"connect_timeout": 5},
    )


def get_session_factory() -> sessionmaker[Session]:
    return sessionmaker(
        bind=get_engine(),
        autoflush=False,
        expire_on_commit=False,
    )


def get_db_session() -> Generator[Session, None, None]:
    """Yield one request-scoped session and always close it afterward."""
    try:
        session_context = get_session_factory()()
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"status": "disconnected", "service": "database"},
        ) from exc
    with session_context as session:
        yield session


def dispose_database_engine() -> None:
    """Close pooled connections during application shutdown, if initialized."""
    if get_engine.cache_info().currsize:
        engine = get_engine()
        engine.dispose()
        get_engine.cache_clear()
