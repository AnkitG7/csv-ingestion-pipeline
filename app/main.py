# app/main.py

from fastapi import FastAPI

from app.api.routes.debug import router as debug_router
from app.api.routes.status import router as status_router
from app.api.routes.upload import router as upload_router
from app.core.database import lifespan
from app.core.middleware import RequestTimingMiddleware


app = FastAPI(lifespan=lifespan)
app.add_middleware(RequestTimingMiddleware)
app.include_router(upload_router)
app.include_router(status_router)
app.include_router(debug_router)
