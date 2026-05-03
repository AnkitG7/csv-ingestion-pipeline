# app/workers/csv_worker.py

import csv
import io
import json

import aioboto3
from aiokafka import AIOKafkaConsumer

from app.core.config import settings
from app.core.database import engine
from app.core.stage_events import record_stage


async def run_worker() -> None:
    """
    Kafka worker loop.
    Consumes upload jobs and processes CSV files.
    """

    consumer = AIOKafkaConsumer(
        settings.KAFKA_UPLOAD_TOPIC,
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        group_id="csv-workers",
    )
    await consumer.start()

    session = aioboto3.Session()

    try:
        async for msg in consumer:
            payload = json.loads(msg.value.decode("utf-8"))
            await process_job(session, payload)
    finally:
        await consumer.stop()


async def process_job(session: aioboto3.Session, payload: dict) -> None:
    """
    Process one CSV upload job.
    """

    upload_id = payload["upload_id"]
    object_key = payload["storage_key"]

    # -------------------------------------------------------------------------
    # Stage: downloading
    # -------------------------------------------------------------------------
    async with engine.begin() as conn:
        await conn.exec_driver_sql(
            """
            UPDATE uploaded_files
            SET status = 'downloading'
            WHERE id = $1
            """,
            (upload_id,),
        )
        await record_stage(conn, upload_id, "downloading")

    # Download file from MinIO
    async with session.client(
        "s3",
        endpoint_url=settings.S3_ENDPOINT_URL,
        aws_access_key_id=settings.S3_ACCESS_KEY,
        aws_secret_access_key=settings.S3_SECRET_KEY,
    ) as s3:
        obj = await s3.get_object(Bucket=settings.S3_BUCKET, Key=object_key)
        body = await obj["Body"].read()

    # Parse CSV
    input_stream = io.StringIO(body.decode("utf-8"))
    reader = csv.DictReader(input_stream)

    # Build COPY-safe CSV buffer
    output_stream = io.StringIO()
    writer = csv.writer(output_stream)

    for row in reader:
        writer.writerow([
            upload_id,
            row["name"],
            row["email"],
            row["age"],
        ])

    output_stream.seek(0)

    async with engine.begin() as conn:
        raw = await conn.get_raw_connection()

        # ---------------------------------------------------------------------
        # Stage: staged
        # ---------------------------------------------------------------------
        await raw._connection.copy_to_table(
            "customer_staging",
            source=io.BytesIO(output_stream.getvalue().encode("utf-8")),
            columns=["upload_id", "name", "email", "age"],
            format="csv",
        )

        await conn.exec_driver_sql(
            """
            UPDATE uploaded_files
            SET status = 'staged'
            WHERE id = $1
            """,
            (upload_id,),
        )
        await record_stage(conn, upload_id, "staged")

        # ---------------------------------------------------------------------
        # Stage: promoting
        # ---------------------------------------------------------------------
        await conn.exec_driver_sql(
            """
            UPDATE uploaded_files
            SET status = 'promoting'
            WHERE id = $1
            """,
            (upload_id,),
        )
        await record_stage(conn, upload_id, "promoting")

        # Atomic move: staging -> final
        await conn.exec_driver_sql(
            """
            WITH moved_rows AS (
                DELETE FROM customer_staging
                WHERE upload_id = CAST($1 AS text)
                RETURNING upload_id, name, email, age
            )
            INSERT INTO customers (upload_id, name, email, age)
            SELECT upload_id::uuid, name, email, age::int
            FROM moved_rows
            """,
            (upload_id,),
        )

        # ---------------------------------------------------------------------
        # Stage: completed
        # ---------------------------------------------------------------------
        await conn.exec_driver_sql(
            """
            UPDATE uploaded_files
            SET status = 'completed'
            WHERE id = $1
            """,
            (upload_id,),
        )
        await record_stage(conn, upload_id, "completed")
