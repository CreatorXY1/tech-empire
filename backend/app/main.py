from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.health import router as health_router
from app.api.routes.database_health import router as database_health_router
from app.core.config import get_frontend_origin
from app.database.session import dispose_database_engine


@asynccontextmanager
async def lifespan(_: FastAPI):
    yield
    dispose_database_engine()

app = FastAPI(
    title="Tech Empire API",
    description="Local-first API foundation for Tech Empire.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[get_frontend_origin()],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["Accept", "Content-Type"],
)

app.include_router(health_router, prefix="/api/v1")
app.include_router(database_health_router, prefix="/api/v1")
