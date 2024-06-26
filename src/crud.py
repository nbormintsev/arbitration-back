from typing import Any

from src.database import database_manager


async def get_client_by_id(client_id: int) -> dict[str, Any] | None:
    pool = await database_manager.get_pool()

    return await pool.fetchrow(
        """
        select
            *
        from
            clients
        where
            id = $1
        """,
        client_id
    )
