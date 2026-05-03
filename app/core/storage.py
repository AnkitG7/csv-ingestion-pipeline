# app/core/storage.py

from uuid import uuid4

import aioboto3
from botocore.exceptions import ClientError
from fastapi import UploadFile

from app.core.config import settings
from app.core.profiler import profile_step



session = aioboto3.Session()


async def ensure_bucket_exists() -> None:
    """
    Ensure the configured S3 bucket exists.

    Best practice:
    infrastructure dependencies required by the app
    should be validated (or created) during startup.
    """

    async with session.client(
        "s3",
        endpoint_url=settings.S3_ENDPOINT_URL,
        aws_access_key_id=settings.S3_ACCESS_KEY,
        aws_secret_access_key=settings.S3_SECRET_KEY,
    ) as s3:
        try:
            await s3.head_bucket(Bucket=settings.S3_BUCKET)
        except ClientError:
            await s3.create_bucket(Bucket=settings.S3_BUCKET)


@profile_step("minio_upload")
async def upload_to_s3(file: UploadFile) -> tuple[str, str]:
    """
    Upload incoming file directly to object storage.
    """

    object_key = f"uploads/{uuid4()}-{file.filename}"

    async with session.client(
        "s3",
        endpoint_url=settings.S3_ENDPOINT_URL,
        aws_access_key_id=settings.S3_ACCESS_KEY,
        aws_secret_access_key=settings.S3_SECRET_KEY,
    ) as s3:
        await s3.upload_fileobj(
            file.file,
            settings.S3_BUCKET,
            object_key,
        )

    return object_key, f"s3://{settings.S3_BUCKET}/{object_key}"
