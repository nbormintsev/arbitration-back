from contextlib import asynccontextmanager
from os import getenv

import uvicorn
from fastapi import FastAPI

from src.auth.router import router as auth_router
from src.database import get_pool


@asynccontextmanager
async def lifespan(_app: FastAPI):
    _app.state.pool = await get_pool()
    yield
    await _app.state.pool.close()


app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)


def start():
    """Точка входа для poetry."""
    uvicorn.run(
        app='src.main:app',
        host=getenv('BACK_HOST'),
        port=int(getenv('BACK_PORT')),
        reload=True
    )
