from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health", summary="Check backend health")
def health_check() -> dict[str, str]:
    """Report that the local API process is responding."""
    return {"status": "ok", "service": "tech-empire-api"}
