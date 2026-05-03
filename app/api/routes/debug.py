# app/api/routes/debug.py

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db

router = APIRouter(prefix="/debug", tags=["Debug"])


@router.get("/uploads/{upload_id}")
async def inspect_upload_pipeline(
    upload_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """
    Debug endpoint to inspect full pipeline state for one upload.
    """

    # upload_result = await db.execute(
    #     text("""
    #         SELECT id, original_name, status, file_size_bytes, created_at
    #         FROM uploaded_files
    #         WHERE id = :upload_id
    #     """),
    #     {"upload_id": str(upload_id)},
    # )
    upload_result = await db.execute(
        text("""
        SELECT id, original_name, storage_key, status, file_size_bytes, created_at
        FROM uploaded_files
        WHERE id = :upload_id
    """),
        {"upload_id": str(upload_id)},
    )
    upload = upload_result.mappings().first()

    if not upload:
        raise HTTPException(status_code=404, detail="Upload not found")

    events_result = await db.execute(
        text("""
            SELECT stage, created_at
            FROM upload_stage_events
            WHERE upload_id = :upload_id
            ORDER BY id
        """),
        {"upload_id": str(upload_id)},
    )
    stage_events = [dict(row) for row in events_result.mappings().all()]

    staging_result = await db.execute(
        text("""
            SELECT id, upload_id, name, email, age
            FROM customer_staging
            WHERE upload_id = :upload_id
            ORDER BY id
        """),
        {"upload_id": str(upload_id)},
    )
    staging_rows = [dict(row) for row in staging_result.mappings().all()]

    final_result = await db.execute(
        text("""
            SELECT id, upload_id, name, email, age
            FROM customers
            WHERE upload_id = :upload_id
            ORDER BY id
        """),
        {"upload_id": str(upload_id)},
    )
    final_rows = [dict(row) for row in final_result.mappings().all()]

    return {
        "upload": dict(upload),
        "stage_events": stage_events,
        "staging_rows": staging_rows,
        "final_rows": final_rows,
    }
