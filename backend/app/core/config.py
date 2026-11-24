import os
from pathlib import Path
from urllib.parse import quote

from dotenv import load_dotenv
from sqlalchemy.engine import URL

DEFAULT_FRONTEND_ORIGIN = "http://127.0.0.1:5173"
BACKEND_ROOT = Path(__file__).resolve().parents[2]

# Load local backend settings for both Uvicorn and Alembic. Existing process
# environment variables take precedence over values in the local .env file.
load_dotenv(BACKEND_ROOT / ".env", override=False)


def get_frontend_origin() -> str:
    """Read the single permitted local browser origin from the environment."""
    return os.getenv("FRONTEND_ORIGIN", DEFAULT_FRONTEND_ORIGIN).strip().rstrip("/")


def get_database_url(database_name: str | None = None) -> URL:
    """Build a PostgreSQL URL without exposing credentials to the frontend."""
    password = os.getenv("DATABASE_PASSWORD", "")
    if not password:
        raise RuntimeError(
            "DATABASE_PASSWORD is not configured. Set it in backend/.env "
            "or the backend process environment."
        )

    try:
        port = int(os.getenv("DATABASE_PORT", "5433"))
    except ValueError as exc:
        raise RuntimeError("DATABASE_PORT must be an integer.") from exc
    if not 1 <= port <= 65535:
        raise RuntimeError("DATABASE_PORT must be between 1 and 65535.")

    return URL.create(
        drivername="postgresql+psycopg",
        username=os.getenv("DATABASE_USER", "tech_empire_app"),
        password=password,
        host=os.getenv("DATABASE_HOST", "127.0.0.1"),
        port=port,
        database=database_name or os.getenv("DATABASE_NAME", "tech_empire_dev"),
    )
