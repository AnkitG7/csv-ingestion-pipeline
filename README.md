# CSV Ingestion Pipeline

An asynchronous, production-style CSV ingestion system built with FastAPI, PostgreSQL, Kafka, and MinIO.

This project accepts CSV uploads through an API, stores the raw file in object storage, persists upload metadata in PostgreSQL, publishes an ingestion job to Kafka, and processes the file asynchronously through a worker pipeline.

The system is designed to reflect real-world backend ingestion architecture with:

* asynchronous request handling
* durable object storage
* metadata persistence
* queue-based background processing
* staging-to-final promotion
* status tracking and debug inspection
* load testing and profiling support

---

# Architecture Overview

The ingestion flow is:

1. Client uploads CSV via FastAPI
2. FastAPI stores raw file in MinIO
3. FastAPI stores upload metadata in PostgreSQL
4. FastAPI publishes ingestion job to Kafka
5. Worker consumes Kafka job
6. Worker downloads file from MinIO
7. Worker inserts rows into staging table
8. Worker promotes rows into final table
9. Worker updates upload status and stage events

This separates the synchronous API path from the asynchronous ingestion pipeline.

```text
Client
  -> FastAPI
      -> MinIO (store raw CSV)
      -> PostgreSQL (store metadata)
      -> Kafka (publish job)
  -> Worker
      -> MinIO (download CSV)
      -> PostgreSQL staging
      -> PostgreSQL final
```

---

# Tech Stack

* FastAPI
* PostgreSQL
* SQLAlchemy (Async)
* Kafka
* MinIO (S3-compatible object storage)
* Docker Compose
* Locust (load testing)

---

# Project Structure

```text
csv-ingestion/
├── app/
│   ├── api/
│   │   └── routes/
│   │       ├── upload.py
│   │       └── debug.py
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── kafka.py
│   │   ├── profiler.py
│   │   └── storage.py
│   ├── models/
│   ├── repositories/
│   ├── services/
│   ├── workers/
│   │   ├── worker.py
│   │   └── csv_worker.py
│   └── main.py
│
├── tests/
│   ├── test_pipeline_debug.py
│   ├── test_all_stages.py
│   └── verify_pipeline_reality.py
│
├── locustfile.py
├── docker-compose.yml
├── .env.example
└── README.md
```

---

# Features

* Upload CSV files via REST API
* Store raw uploaded files in MinIO
* Persist upload metadata in PostgreSQL
* Publish ingestion jobs to Kafka
* Process CSV asynchronously in worker
* Insert rows into staging table
* Promote staged rows into final table
* Track upload lifecycle and stage events
* Debug full ingestion pipeline per upload
* Profile request and worker execution
* Load test upload throughput with Locust

---

# Setup Instructions

## 1. Clone Repository

```bash
git clone https://github.com/<your-username>/csv-ingestion-pipeline.git
cd csv-ingestion-pipeline
```

---

## 2. Create Virtual Environment

```bash
python -m venv .venvp
```

Activate:

### Windows

```bash
.venvp\Scripts\activate
```

### Linux / macOS

```bash
source .venvp/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment

Create `.env` in project root:

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/appdb

KAFKA_BOOTSTRAP_SERVERS=localhost:9092
KAFKA_UPLOAD_TOPIC=csv-upload-topic

S3_ENDPOINT_URL=http://localhost:9000
S3_ACCESS_KEY=minioadmin
S3_SECRET_KEY=minioadmin
S3_BUCKET=csv-uploads
```

---

## 5. Start Infrastructure

```bash
docker-compose up -d
```

This starts:

* PostgreSQL
* Kafka
* Zookeeper
* MinIO

---

## 6. Run Database Migrations

```bash
alembic upgrade head
```

---

# Running the Application

## Start FastAPI API

```bash
uvicorn app.main:app --reload
```

API available at:

```text
http://127.0.0.1:8000
```

Swagger docs:

```text
http://127.0.0.1:8000/docs
```

---

## Start Worker

Run in separate terminal:

```bash
python -m app.workers.worker
```

This starts the Kafka consumer and background ingestion worker.

---

# API Endpoints

## Upload CSV

```http
POST /uploads/csv
```

Uploads CSV file and queues async ingestion.

### Example

Use Swagger UI or curl:

```bash
curl -X POST "http://127.0.0.1:8000/uploads/csv" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@sample.csv"
```

### Response

```json
{
  "upload_id": "uuid",
  "status": "queued"
}
```

---

## Debug Upload Pipeline

```http
GET /debug/uploads/{upload_id}
```

Returns full pipeline state for one upload:

* upload metadata
* stage events
* staging rows
* final rows

This is useful for debugging and verification.

---

# Running Tests

## Verify Pipeline Reality

End-to-end verification that proves:

* FastAPI request is real
* MinIO upload/download is real
* PostgreSQL writes are real
* Kafka worker execution is real
* staging is real
* promotion is real

```bash
python tests/verify_pipeline_reality.py
```

---

## Debug Pipeline Flow

```bash
python tests/test_pipeline_debug.py
```

---

## Inspect Stage History

```bash
python tests/test_all_stages.py
```

---

# Load Testing

Run Locust load test:

```bash
locust -f locustfile.py --host=http://localhost:8000 --users 20 --spawn-rate 20 --run-time 30s --headless
```

This tests concurrent upload throughput on:

```text
POST /uploads/csv
```

---

# Profiling

The system includes lightweight request and function profiling.

Example logs:

```text
[PROFILE] minio_upload=53.87ms
[PROFILE] db_insert=18.97ms
[PROFILE] kafka_publish=6.02ms
[PROFILE] upload_service.create_upload=81.42ms
[REQUEST] POST /uploads/csv status=202 total=94.00ms
```

This helps identify latency across:

* object storage
* database
* Kafka
* service orchestration
* HTTP request lifecycle

---

# Pipeline Stages

Each upload progresses through these stages:

* queued
* downloading
* staged
* promoting
* completed

These stages are persisted in `upload_stage_events` and can be inspected via debug endpoint.

---

# Notes

* `customer_staging` is intentionally emptied after promotion
* `customers` stores final promoted rows
* identical timestamps across fast stages are expected when committed in same DB transaction
* worker logs appear in worker terminal, not Uvicorn terminal

---

# Production Considerations

This project is intentionally designed in a production-oriented style:

* thin route layer
* service orchestration
* repository abstraction
* async job handoff
* staging-to-final promotion
* isolated profiling boundaries
* infrastructure-backed verification

Potential next improvements:

* retries and dead-letter queues
* idempotency keys
* schema validation
* metrics and tracing
* auth and rate limiting
* partitioned Kafka consumers
* horizontal worker scaling

---

# License

MIT
