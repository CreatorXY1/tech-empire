from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker

import app.database.session as database_session
from app.api.routes.database_health import get_db_session
from app.main import app


def test_database_health_uses_database_session(monkeypatch) -> None:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    factory = sessionmaker(bind=engine)

    def test_session() -> Session:
        with factory() as session:
            yield session

    app.dependency_overrides[get_db_session] = test_session
    try:
        response = TestClient(app).get("/api/v1/health/database")
    finally:
        app.dependency_overrides.clear()
        engine.dispose()

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "database"}


def test_database_health_reports_missing_configuration(monkeypatch) -> None:
    monkeypatch.delenv("DATABASE_PASSWORD", raising=False)
    database_session.get_engine.cache_clear()

    response = TestClient(app).get("/api/v1/health/database")

    assert response.status_code == 503
    assert response.json() == {
        "detail": {"status": "disconnected", "service": "database"}
    }


def test_database_health_hides_connection_error_details() -> None:
    class UnavailableSession:
        def execute(self, _statement):
            raise SQLAlchemyError("sensitive connection details")

    def unavailable_session():
        yield UnavailableSession()

    app.dependency_overrides[get_db_session] = unavailable_session
    try:
        response = TestClient(app).get("/api/v1/health/database")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 503
    assert response.json() == {
        "detail": {"status": "disconnected", "service": "database"}
    }
    assert "sensitive connection details" not in response.text
