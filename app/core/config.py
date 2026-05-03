from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/appdb"

    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"
    KAFKA_UPLOAD_TOPIC: str = "csv-upload-topic"

    S3_ENDPOINT_URL: str = "http://localhost:9000"
    S3_ACCESS_KEY: str = "minioadmin"
    S3_SECRET_KEY: str = "minioadmin"
    S3_BUCKET: str = "csv-uploads"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
