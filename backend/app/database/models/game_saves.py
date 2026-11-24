from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, Index, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin


class GameSave(TimestampMixin, Base):
    __tablename__ = "game_saves"
    __table_args__ = (Index("ix_game_saves_company_id", "company_id"),)

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    company_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("companies.id", ondelete="RESTRICT"), nullable=False
    )
    game_time: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False)
    content_version: Mapped[str] = mapped_column(String(32), nullable=False)
