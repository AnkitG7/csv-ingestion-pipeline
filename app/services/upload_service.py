# app/services/upload_service.py

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.kafka import publish_upload_job
from app.core.profiler import profile_step
from app.core.storage import upload_to_s3
from app.models.uploaded_file import UploadedFile
from app.repositories.upload_repository import UploadRepository


class UploadService:
    """
    Handles upload orchestration:
    - upload file to object storage
    - create metadata record
    - publish async processing job
    """

    @staticmethod
    @profile_step("upload_service.create_upload")
    async def create_upload(
        db: AsyncSession,
        file: UploadFile,
    ) -> UploadedFile:
        object_key, storage_uri = await upload_to_s3(file)

        upload = UploadedFile(
            original_name=file.filename,
            storage_key=storage_uri,
            file_size_bytes=file.size or 0,
            status="queued",
        )

        upload = await UploadRepository.create(db, upload)

        await publish_upload_job(
            {
                "upload_id": str(upload.id),
                "storage_key": object_key,
            }
        )

        return upload
