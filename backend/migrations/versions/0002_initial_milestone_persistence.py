"""Add the minimum Milestone 01 persistence entities.

Revision ID: 0002_milestone01_persistence
Revises: 0001_persistence_foundation
"""
from alembic import op
import sqlalchemy as sa


revision = "0002_milestone01_persistence"
down_revision = "0001_persistence_foundation"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "companies",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=40), nullable=False),
        sa.Column(
            "cash_balance",
            sa.Numeric(precision=14, scale=2),
            server_default=sa.text("0.00"),
            nullable=False,
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint("cash_balance >= 0", name="ck_companies_cash_balance_nonnegative"),
        sa.PrimaryKeyConstraint("id", name="pk_companies"),
    )
    op.create_table(
        "game_saves",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("company_id", sa.Uuid(), nullable=False),
        sa.Column("game_time", sa.DateTime(timezone=False), nullable=False),
        sa.Column("content_version", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(
            ["company_id"], ["companies.id"], name="fk_game_saves_company_id_companies", ondelete="RESTRICT"
        ),
        sa.PrimaryKeyConstraint("id", name="pk_game_saves"),
    )
    op.create_index("ix_game_saves_company_id", "game_saves", ["company_id"], unique=False)
    op.create_table(
        "facilities",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("game_save_id", sa.Uuid(), nullable=False),
        sa.Column("facility_definition_id", sa.String(length=100), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(
            ["game_save_id"], ["game_saves.id"], name="fk_facilities_game_save_id_game_saves", ondelete="RESTRICT"
        ),
        sa.PrimaryKeyConstraint("id", name="pk_facilities"),
        sa.UniqueConstraint("id", "game_save_id", name="uq_facilities_id_game_save"),
    )
    op.create_index("ix_facilities_game_save_id", "facilities", ["game_save_id"], unique=False)
    op.create_table(
        "equipment_instances",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("game_save_id", sa.Uuid(), nullable=False),
        sa.Column("facility_id", sa.Uuid(), nullable=True),
        sa.Column("equipment_definition_id", sa.String(length=100), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(
            ["facility_id", "game_save_id"],
            ["facilities.id", "facilities.game_save_id"],
            name="fk_equipment_instances_facility_save",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["game_save_id"], ["game_saves.id"], name="fk_equipment_instances_game_save_id_game_saves", ondelete="RESTRICT"
        ),
        sa.PrimaryKeyConstraint("id", name="pk_equipment_instances"),
    )
    op.create_index(
        "ix_equipment_instances_game_save_id", "equipment_instances", ["game_save_id"], unique=False
    )
    op.create_index(
        "ix_equipment_instances_facility_save",
        "equipment_instances",
        ["facility_id", "game_save_id"],
        unique=False,
    )
    op.create_table(
        "inventory_balances",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("game_save_id", sa.Uuid(), nullable=False),
        sa.Column("facility_id", sa.Uuid(), nullable=False),
        sa.Column("item_id", sa.String(length=100), nullable=False),
        sa.Column("quantity", sa.Integer(), server_default=sa.text("0"), nullable=False),
        sa.Column("reserved_quantity", sa.Integer(), server_default=sa.text("0"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint("quantity >= 0", name="ck_inventory_balances_quantity_nonnegative"),
        sa.CheckConstraint("reserved_quantity >= 0", name="ck_inventory_balances_reserved_nonnegative"),
        sa.CheckConstraint("reserved_quantity <= quantity", name="ck_inventory_balances_reserved_lte_quantity"),
        sa.ForeignKeyConstraint(
            ["facility_id", "game_save_id"],
            ["facilities.id", "facilities.game_save_id"],
            name="fk_inventory_balances_facility_save",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["game_save_id"], ["game_saves.id"], name="fk_inventory_balances_game_save_id_game_saves", ondelete="RESTRICT"
        ),
        sa.PrimaryKeyConstraint("id", name="pk_inventory_balances"),
        sa.UniqueConstraint(
            "game_save_id", "facility_id", "item_id", name="uq_inventory_balance_location_item"
        ),
    )
    op.create_index("ix_inventory_balances_game_save_id", "inventory_balances", ["game_save_id"], unique=False)
    op.create_table(
        "production_orders",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("game_save_id", sa.Uuid(), nullable=False),
        sa.Column("facility_id", sa.Uuid(), nullable=False),
        sa.Column("recipe_id", sa.String(length=100), nullable=False),
        sa.Column("batch_count", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=False), nullable=False),
        sa.Column("due_at", sa.DateTime(timezone=False), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=False), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint("batch_count > 0", name="ck_production_orders_batch_count_positive"),
        sa.ForeignKeyConstraint(
            ["facility_id", "game_save_id"],
            ["facilities.id", "facilities.game_save_id"],
            name="fk_production_orders_facility_save",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["game_save_id"], ["game_saves.id"], name="fk_production_orders_game_save_id_game_saves", ondelete="RESTRICT"
        ),
        sa.PrimaryKeyConstraint("id", name="pk_production_orders"),
    )
    op.create_index(
        "ix_production_orders_save_status", "production_orders", ["game_save_id", "status"], unique=False
    )
    op.create_index(
        "ix_production_orders_facility_save",
        "production_orders",
        ["facility_id", "game_save_id"],
        unique=False,
    )
    op.create_table(
        "inventory_movements",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("game_save_id", sa.Uuid(), nullable=False),
        sa.Column("facility_id", sa.Uuid(), nullable=False),
        sa.Column("item_id", sa.String(length=100), nullable=False),
        sa.Column("quantity_delta", sa.Integer(), nullable=False),
        sa.Column("movement_type", sa.String(length=40), nullable=False),
        sa.Column("reference_id", sa.Uuid(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint("quantity_delta <> 0", name="ck_inventory_movements_quantity_delta_nonzero"),
        sa.ForeignKeyConstraint(
            ["facility_id", "game_save_id"],
            ["facilities.id", "facilities.game_save_id"],
            name="fk_inventory_movements_facility_save",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["game_save_id"], ["game_saves.id"], name="fk_inventory_movements_game_save_id_game_saves", ondelete="RESTRICT"
        ),
        sa.PrimaryKeyConstraint("id", name="pk_inventory_movements"),
    )
    op.create_index(
        "ix_inventory_movements_save_created", "inventory_movements", ["game_save_id", "created_at"], unique=False
    )
    op.create_index(
        "ix_inventory_movements_facility_save",
        "inventory_movements",
        ["facility_id", "game_save_id"],
        unique=False,
    )
    op.create_table(
        "financial_transactions",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("game_save_id", sa.Uuid(), nullable=False),
        sa.Column("transaction_type", sa.String(length=40), nullable=False),
        sa.Column("amount", sa.Numeric(precision=14, scale=2), nullable=False),
        sa.Column("currency", sa.String(length=3), server_default=sa.text("'USD'"), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("reference_id", sa.Uuid(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint("amount <> 0", name="ck_financial_transactions_amount_nonzero"),
        sa.ForeignKeyConstraint(
            ["game_save_id"], ["game_saves.id"], name="fk_financial_transactions_game_save_id_game_saves", ondelete="RESTRICT"
        ),
        sa.PrimaryKeyConstraint("id", name="pk_financial_transactions"),
    )
    op.create_index(
        "ix_financial_transactions_save_created",
        "financial_transactions",
        ["game_save_id", "created_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_table("financial_transactions")
    op.drop_index("ix_inventory_movements_facility_save", table_name="inventory_movements")
    op.drop_index("ix_inventory_movements_save_created", table_name="inventory_movements")
    op.drop_table("inventory_movements")
    op.drop_index("ix_production_orders_facility_save", table_name="production_orders")
    op.drop_index("ix_production_orders_save_status", table_name="production_orders")
    op.drop_table("production_orders")
    op.drop_index("ix_inventory_balances_game_save_id", table_name="inventory_balances")
    op.drop_table("inventory_balances")
    op.drop_index("ix_equipment_instances_facility_save", table_name="equipment_instances")
    op.drop_index("ix_equipment_instances_game_save_id", table_name="equipment_instances")
    op.drop_table("equipment_instances")
    op.drop_index("ix_facilities_game_save_id", table_name="facilities")
    op.drop_table("facilities")
    op.drop_index("ix_game_saves_company_id", table_name="game_saves")
    op.drop_table("game_saves")
    op.drop_table("companies")
