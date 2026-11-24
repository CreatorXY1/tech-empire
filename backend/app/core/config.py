import os

DEFAULT_FRONTEND_ORIGIN = "http://127.0.0.1:5173"


def get_frontend_origin() -> str:
    """Read the single permitted local browser origin from the environment."""
    return os.getenv("FRONTEND_ORIGIN", DEFAULT_FRONTEND_ORIGIN).strip().rstrip("/")
