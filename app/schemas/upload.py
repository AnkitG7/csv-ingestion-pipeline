# app/schemas/upload.py

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class UploadResponse(BaseModel):
    """
    Response returned immediately after upload.
    """

    upload_id: UUID
    status: str


class UploadStatusResponse(BaseModel):
    """
    Upload processing status response.
    """

    upload_id: UUID
    original_name: str
    status: str
    file_size_bytes: int
    created_at: datetime
