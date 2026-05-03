# app/core/database.py

from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings
from app.core.kafka import init_kafka, stop_kafka
from app.core.storage import ensure_bucket_exists


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy models.
    """
    pass


# engine = create_async_engine(
#     settings.DATABASE_URL,
#     pool_pre_ping=True,
#     pool_size=50,
#     max_overflow=100,
# )
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    pool_size=50,
    max_overflow=100,
    pool_timeout=30,
    pool_pre_ping=True,
)

SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    App lifecycle hook.

    Important:
    Import all models before create_all()
    so SQLAlchemy registers them in Base.metadata.
    """

    # Import models here so SQLAlchemy registers them
    from app.models.uploaded_file import UploadedFile
    from app.models.customer import Customer
    from app.models.customer_staging import CustomerStaging
    from app.models.upload_stage_event import UploadStageEvent

    print("DATABASE_URL =", settings.DATABASE_URL)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # initialize infra dependencies here
    await init_kafka()
    await ensure_bucket_exists()

    yield

    await stop_kafka()
    await engine.dispose()
