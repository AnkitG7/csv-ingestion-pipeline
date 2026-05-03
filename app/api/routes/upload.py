# app/api/routes/upload.py

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services.upload_service import UploadService

router = APIRouter(prefix="/uploads", tags=["Uploads"])


@router.post("/csv", status_code=202)
async def upload_csv(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    """
    Thin HTTP route:
    - validate request
    - delegate workflow to service
    - return response
    """
    if not file.filename or not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV allowed")

    upload = await UploadService.create_upload(db, file)

    return {
        "upload_id": str(upload.id),
        "status": upload.status,
    }
