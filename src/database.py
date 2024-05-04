from os import getenv

from asyncpg import Pool, create_pool

_pool: Pool | None = None


async def get_pool():
    global _pool

    if not _pool:
        _pool = await create_pool(
            host=getenv("DATABASE_HOST"),
            port=getenv("DATABASE_PORT"),
            database=getenv("DATABASE_NAME"),
            user=getenv("DATABASE_USER"),
            password=getenv("DATABASE_PASSWORD"),
        )

    return _pool
