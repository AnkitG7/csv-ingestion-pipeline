# app/core/middleware.py

import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class RequestTimingMiddleware(BaseHTTPMiddleware):
    """
    Logs total request processing time.
    """

    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        elapsed_ms = (time.perf_counter() - start) * 1000

        print(
            f"[REQUEST] {request.method} {request.url.path} "
            f"status={response.status_code} total={elapsed_ms:.2f}ms"
        )

        return response
