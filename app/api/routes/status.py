# app/api/routes/status.py

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.upload_repository import UploadRepository
from app.schemas.upload import UploadStatusResponse

router = APIRouter(prefix="/uploads", tags=["Uploads"])


@router.get("/{upload_id}", response_model=UploadStatusResponse)
async def get_upload_status(
    upload_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> UploadStatusResponse:
    upload = await UploadRepository.get_by_id(db, upload_id)

    if not upload:
        raise HTTPException(status_code=404, detail="Upload not found")

    return UploadStatusResponse(
        upload_id=upload.id,
        original_name=upload.original_name,
        status=upload.status,
        file_size_bytes=upload.file_size_bytes,
        created_at=upload.created_at,
    )
