from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, ForeignKeyConstraint, Index, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin


class EquipmentInstance(TimestampMixin, Base):
    __tablename__ = "equipment_instances"
    __table_args__ = (
        ForeignKeyConstraint(
            ["facility_id", "game_save_id"],
            ["facilities.id", "facilities.game_save_id"],
            name="fk_equipment_instances_facility_save",
            ondelete="RESTRICT",
        ),
        Index("ix_equipment_instances_game_save_id", "game_save_id"),
        Index("ix_equipment_instances_facility_save", "facility_id", "game_save_id"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    game_save_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("game_saves.id", ondelete="RESTRICT"), nullable=False
    )
    facility_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    equipment_definition_id: Mapped[str] = mapped_column(String(100), nullable=False)
