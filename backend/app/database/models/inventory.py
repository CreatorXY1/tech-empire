from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    Integer,
    String,
    UniqueConstraint,
    Uuid,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin


class InventoryBalance(TimestampMixin, Base):
    __tablename__ = "inventory_balances"
    __table_args__ = (
        ForeignKeyConstraint(
            ["facility_id", "game_save_id"],
            ["facilities.id", "facilities.game_save_id"],
            name="fk_inventory_balances_facility_save",
            ondelete="RESTRICT",
        ),
        UniqueConstraint(
            "game_save_id", "facility_id", "item_id", name="uq_inventory_balance_location_item"
        ),
        CheckConstraint("quantity >= 0", name="quantity_nonnegative"),
        CheckConstraint("reserved_quantity >= 0", name="reserved_nonnegative"),
        CheckConstraint("reserved_quantity <= quantity", name="reserved_lte_quantity"),
        Index("ix_inventory_balances_game_save_id", "game_save_id"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    game_save_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("game_saves.id", ondelete="RESTRICT"), nullable=False
    )
    facility_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    item_id: Mapped[str] = mapped_column(String(100), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default="0")
    reserved_quantity: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default="0"
    )


class InventoryMovement(Base):
    __tablename__ = "inventory_movements"
    __table_args__ = (
        ForeignKeyConstraint(
            ["facility_id", "game_save_id"],
            ["facilities.id", "facilities.game_save_id"],
            name="fk_inventory_movements_facility_save",
            ondelete="RESTRICT",
        ),
        CheckConstraint("quantity_delta <> 0", name="quantity_delta_nonzero"),
        Index("ix_inventory_movements_save_created", "game_save_id", "created_at"),
        Index("ix_inventory_movements_facility_save", "facility_id", "game_save_id"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    game_save_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("game_saves.id", ondelete="RESTRICT"), nullable=False
    )
    facility_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    item_id: Mapped[str] = mapped_column(String(100), nullable=False)
    quantity_delta: Mapped[int] = mapped_column(Integer, nullable=False)
    movement_type: Mapped[str] = mapped_column(String(40), nullable=False)
    reference_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
