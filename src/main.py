from contextlib import asynccontextmanager
from os import getenv

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.auth.views import router as auth_router
from src.database import get_pool, close_pool


@asynccontextmanager
async def lifespan(_app: FastAPI):
    await get_pool()
    yield
    await close_pool()


app = FastAPI(lifespan=lifespan)
app.include_router(router=auth_router, prefix="/auth", tags=["Auth"])


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def start():
    """Точка входа для poetry."""
    uvicorn.run(
        app='src.main:app',
        host=getenv('BACK_HOST'),
        port=int(getenv('BACK_PORT')),
        reload=True
    )
