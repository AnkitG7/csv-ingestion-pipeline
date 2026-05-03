# app/services/ingest_service.py

import csv
import io

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.customer_repository import CustomerRepository
from app.repositories.upload_repository import UploadRepository


class IngestService:
    """
    Handles CSV parsing, staging, and promotion.
    """

    @staticmethod
    async def parse_csv_bytes(data: bytes) -> list[str]:
        text_stream = io.StringIO(data.decode("utf-8"))
        reader = csv.DictReader(text_stream)

        rows = []
        for row in reader:
            rows.append(
                f"{row['upload_id']},{row['name']},{row['email']},{row['age']}\n"
            )
        return rows

    @staticmethod
    async def finalize(db: AsyncSession, upload_id: str) -> None:
        await CustomerRepository.promote_from_staging(db, upload_id)

        upload = await UploadRepository.get_by_id(db, upload_id)
        if upload:
            upload.status = "completed"
            await db.commit()
