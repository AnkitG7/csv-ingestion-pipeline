# app/repositories/upload_repository.py

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.profiler import profile_step
from app.models.uploaded_file import UploadedFile


class UploadRepository:
    """
    Handles upload metadata persistence.
    """

    @staticmethod
    @profile_step("db_insert")
    async def create(
        db: AsyncSession,
        upload: UploadedFile,
    ) -> UploadedFile:
        db.add(upload)
        await db.commit()
        await db.refresh(upload)
        return upload

    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        upload_id: UUID,
    ) -> UploadedFile | None:
        result = await db.execute(
            select(UploadedFile).where(UploadedFile.id == upload_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def update_status(
        db: AsyncSession,
        upload: UploadedFile,
        status: str,
    ) -> None:
        upload.status = status
        await db.commit()
