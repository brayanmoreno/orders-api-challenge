from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.routers import orders
from app.seed import init_db


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(title="Orders API", version="1.4.1", lifespan=lifespan)
app.include_router(orders.router)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
