from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.database.session import get_db_session

router = APIRouter(tags=["health"])


@router.get("/health/database")
def database_health(session: Session = Depends(get_db_session)) -> dict[str, str]:
    """Check that FastAPI can execute a read-only query against PostgreSQL."""
    try:
        session.execute(text("SELECT 1"))
    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"status": "disconnected", "service": "database"},
        ) from exc
    return {"status": "ok", "service": "database"}
