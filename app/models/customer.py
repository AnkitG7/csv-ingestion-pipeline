# app/models/customer.py

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Customer(Base):
    """
    Final business table populated after validation.
    """

    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    upload_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("uploaded_files.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
