import os

import pytest
from alembic import command
from alembic.config import Config
from alembic.runtime.migration import MigrationContext
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text

from app.main import app

TEST_DATABASE_NAME = os.getenv("DATABASE_TEST_NAME")
pytestmark = pytest.mark.integration


@pytest.mark.skipif(
    not TEST_DATABASE_NAME,
    reason="Set DATABASE_TEST_NAME to enable isolated PostgreSQL integration checks.",
)
def test_database_health_uses_isolated_postgres_database(monkeypatch) -> None:
    from app.core.config import get_database_url
    from app.database.session import get_engine

    assert TEST_DATABASE_NAME
    development_database = os.getenv("DATABASE_NAME", "tech_empire_dev")
    assert TEST_DATABASE_NAME != development_database, (
        "PostgreSQL integration checks must never target the development database."
    )

    monkeypatch.setenv("DATABASE_NAME", TEST_DATABASE_NAME)
    get_engine.cache_clear()
    try:
        with TestClient(app) as client:
            response = client.get("/api/v1/health/database")
            assert response.status_code == 200
            assert response.json() == {"status": "ok", "service": "database"}
    finally:
        if get_engine.cache_info().currsize:
            get_engine().dispose()
            get_engine.cache_clear()

    assert get_database_url(TEST_DATABASE_NAME).database == TEST_DATABASE_NAME


@pytest.mark.skipif(
    not TEST_DATABASE_NAME,
    reason="Set DATABASE_TEST_NAME to enable isolated PostgreSQL integration checks.",
)
def test_alembic_can_generate_apply_and_rollback_test_migration(
    monkeypatch, tmp_path
) -> None:
    from app.core.config import get_database_url

    assert TEST_DATABASE_NAME
    development_database = os.getenv("DATABASE_NAME", "tech_empire_dev")
    assert TEST_DATABASE_NAME != development_database
    assert TEST_DATABASE_NAME.endswith("_test"), (
        "Migration smoke tests require a database name ending in _test."
    )

    monkeypatch.setenv("DATABASE_NAME", TEST_DATABASE_NAME)
    baseline_config = Config("alembic.ini")
    generated_versions = tmp_path / "versions"
    generated_versions.mkdir()
    config = Config("alembic.ini")
    config.set_main_option("version_locations", str(generated_versions))
    config.set_main_option("version_table", "phase2_smoke_alembic_version")

    engine = create_engine(
        get_database_url(TEST_DATABASE_NAME),
        connect_args={"connect_timeout": 5},
    )
    try:
        with engine.begin() as connection:
            connection.execute(
                text(
                    "DROP TABLE IF EXISTS "
                    "tech_empire_app.phase2_smoke_alembic_version"
                )
            )

        command.upgrade(baseline_config, "head")
        command.revision(
            config,
            message="phase 2 migration smoke test",
            rev_id="phase2_smoke",
            autogenerate=True,
        )
        generated_revision = next(generated_versions.glob("phase2_smoke_*.py"))
        assert "op." not in generated_revision.read_text(encoding="utf-8"), (
            "The committed schema migration and model metadata must match before "
            "the empty Alembic smoke migration is applied."
        )

        command.upgrade(config, "head")
        with engine.connect() as connection:
            migration_context = MigrationContext.configure(
                connection,
                opts={
                    "version_table": "phase2_smoke_alembic_version",
                    "version_table_schema": "tech_empire_app",
                },
            )
            revision = migration_context.get_current_revision()
        assert revision == "phase2_smoke"
        command.downgrade(config, "base")
    finally:
        with engine.begin() as connection:
            connection.execute(
                text(
                    "DROP TABLE IF EXISTS "
                    "tech_empire_app.phase2_smoke_alembic_version"
                )
            )
        engine.dispose()
