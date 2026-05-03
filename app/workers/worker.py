# app/workers/worker.py

import asyncio

from app.workers.csv_worker import run_worker


def main() -> None:
    asyncio.run(run_worker())


if __name__ == "__main__":
    main()
