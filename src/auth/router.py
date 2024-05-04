from asyncpg import Pool
from fastapi import APIRouter, Depends

from src.database import get_pool

router = APIRouter(prefix="/clients")


@router.get("/count/")
async def get_client_count(pool: Pool = Depends(get_pool)):
    async with pool.acquire() as connection:
        async with connection.transaction():
            result = await connection.fetchval("SELECT COUNT(*) FROM clients")
            return {"result": result}
