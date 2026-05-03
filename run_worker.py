import asyncio
from app.workers.csv_worker import run_worker

if __name__ == "__main__":
    asyncio.run(run_worker())
