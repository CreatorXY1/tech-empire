import importlib.util
from pathlib import Path

from alembic.migration import MigrationContext
from alembic.operations import Operations
from sqlalchemy import create_engine, inspect

from app.database.base import Base
import app.database.models  # noqa: F401


EXPECTED_MILESTONE_TABLES = {
    "companies",
    "game_saves",
    "facilities",
    "equipment_instances",
    "inventory_balances",
    "production_orders",
    "inventory_movements",
    "financial_transactions",
}


def test_metadata_contains_only_documented_milestone_entities() -> None:
    assert set(Base.metadata.tables) == EXPECTED_MILESTONE_TABLES


def test_initial_schema_creates_with_foreign_keys_and_constraints() -> None:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    try:
        Base.metadata.create_all(engine)
        inspector = inspect(engine)
        assert set(inspector.get_table_names()) == EXPECTED_MILESTONE_TABLES
        assert inspector.get_foreign_keys("game_saves")
        assert inspector.get_unique_constraints("inventory_balances")
        assert inspector.get_check_constraints("inventory_balances")
        assert inspector.get_check_constraints("production_orders")
    finally:
        engine.dispose()


def test_money_uses_fixed_precision() -> None:
    company_balance = Base.metadata.tables["companies"].c.cash_balance.type
    transaction_amount = Base.metadata.tables["financial_transactions"].c.amount.type

    assert (company_balance.precision, company_balance.scale) == (14, 2)
    assert (transaction_amount.precision, transaction_amount.scale) == (14, 2)


def test_initial_migration_applies_and_rolls_back_on_isolated_sqlite() -> None:
    migration_path = (
        Path(__file__).resolve().parents[1]
        / "migrations"
        / "versions"
        / "0002_initial_milestone_persistence.py"
    )
    spec = importlib.util.spec_from_file_location("phase2_initial_migration", migration_path)
    assert spec and spec.loader
    migration = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(migration)

    engine = create_engine("sqlite+pysqlite:///:memory:")
    try:
        with engine.begin() as connection:
            context = MigrationContext.configure(connection)
            with Operations.context(context):
                migration.upgrade()

        assert set(inspect(engine).get_table_names()) == EXPECTED_MILESTONE_TABLES

        with engine.begin() as connection:
            context = MigrationContext.configure(connection)
            with Operations.context(context):
                migration.downgrade()

        assert inspect(engine).get_table_names() == []
    finally:
        engine.dispose()
