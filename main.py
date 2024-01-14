import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from api.router import api


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:  # noqa U100
    yield


logger = logging.getLogger(__name__)

app = FastAPI(lifespan=lifespan)
app.include_router(api, prefix="/api")


@app.get("/")
async def hello() -> dict:
    return {"msg": "Hello World"}


@app.get("/echo/{msg}")
async def echo(msg: str) -> dict:
    return {"msg": f"{msg}"}


if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host="127.0.0.1",
        port=8000,
        workers=1,
        reload=True,
        access_log=False,
    )
