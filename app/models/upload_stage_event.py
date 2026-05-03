# app/models/upload_stage_event.py

from datetime import datetime

from sqlalchemy import DateTime, Integer, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class UploadStageEvent(Base):
    """
    Immutable audit trail of upload stage transitions.
    """

    __tablename__ = "upload_stage_events"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    upload_id: Mapped[str] = mapped_column(Text, index=True, nullable=False)
    stage: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
