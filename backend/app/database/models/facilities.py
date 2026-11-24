from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, Index, String, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin


class Facility(TimestampMixin, Base):
    __tablename__ = "facilities"
    __table_args__ = (
        UniqueConstraint("id", "game_save_id", name="uq_facilities_id_game_save"),
        Index("ix_facilities_game_save_id", "game_save_id"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    game_save_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("game_saves.id", ondelete="RESTRICT"), nullable=False
    )
    facility_definition_id: Mapped[str] = mapped_column(String(100), nullable=False)
