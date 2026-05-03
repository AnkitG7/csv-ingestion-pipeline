# app/core/stage_events.py

from sqlalchemy.ext.asyncio import AsyncConnection


async def record_stage(conn: AsyncConnection, upload_id: str, stage: str) -> None:
    """
    Persist one immutable upload stage transition event.
    """

    await conn.exec_driver_sql(
        """
        INSERT INTO upload_stage_events (upload_id, stage)
        VALUES ($1, $2)
        """,
        (upload_id, stage),
    )
