from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, ForeignKeyConstraint, Index, Integer, String, Uuid
from sqlalchemy import CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin


class ProductionOrder(TimestampMixin, Base):
    __tablename__ = "production_orders"
    __table_args__ = (
        ForeignKeyConstraint(
            ["facility_id", "game_save_id"],
            ["facilities.id", "facilities.game_save_id"],
            name="fk_production_orders_facility_save",
            ondelete="RESTRICT",
        ),
        CheckConstraint("batch_count > 0", name="batch_count_positive"),
        Index("ix_production_orders_save_status", "game_save_id", "status"),
        Index("ix_production_orders_facility_save", "facility_id", "game_save_id"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    game_save_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("game_saves.id", ondelete="RESTRICT"), nullable=False
    )
    facility_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    recipe_id: Mapped[str] = mapped_column(String(100), nullable=False)
    batch_count: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False)
    due_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=False), nullable=True)
