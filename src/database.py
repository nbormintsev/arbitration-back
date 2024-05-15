import os
from asyncpg import Pool, create_pool


class DatabaseManager:
    def __init__(self):
        self._pool: Pool | None = None

    async def get_pool(self) -> Pool:
        if self._pool is None:
            self._pool = await create_pool(
                host=os.getenv("DATABASE_HOST"),
                port=int(os.getenv("DATABASE_PORT")),
                database=os.getenv("DATABASE_NAME"),
                user=os.getenv("DATABASE_USER"),
                password=os.getenv("DATABASE_PASSWORD"),
            )

        return self._pool

    async def close_pool(self) -> None:
        if self._pool:
            await self._pool.close()
            self._pool = None


database_manager = DatabaseManager()
