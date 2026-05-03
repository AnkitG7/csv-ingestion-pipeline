import json
from aiokafka import AIOKafkaProducer

from app.core.config import settings
from app.core.profiler import profile_step



producer: AIOKafkaProducer | None = None


async def init_kafka() -> None:
    global producer
    producer = AIOKafkaProducer(
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        acks="all",
        enable_idempotence=True,
    )
    await producer.start()


async def stop_kafka() -> None:
    if producer:
        await producer.stop()


@profile_step("kafka_publish")
async def publish_upload_job(payload: dict) -> None:
    await producer.send_and_wait(
        settings.KAFKA_UPLOAD_TOPIC,
        json.dumps(payload).encode(),
    )
