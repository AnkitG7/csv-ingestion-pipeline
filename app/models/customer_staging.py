# app/models/customer_staging.py

from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class CustomerStaging(Base):
    """
    Raw staging table for CSV ingestion before promotion.

    Important:
    One upload can contain many staged rows,
    so upload_id must NOT be the primary key.
    """

    __tablename__ = "customer_staging"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    upload_id: Mapped[str] = mapped_column(Text, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255))
    age: Mapped[str] = mapped_column(String(50))
