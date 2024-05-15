from typing import Any

from src.database import database_manager


async def add_client(
    email: str,
    name: str,
    password_hash: bytes,
) -> int:
    pool = await database_manager.get_pool()

    return await pool.fetchval(
        """
        insert into
            clients (
                email,
                name,
                password_hash
            )
        values
            ($1, $2, $3)
        returning
            id
        """,
        email,
        name,
        password_hash
    )


async def get_client_by_email(client_email: str) -> dict[str, Any] | None:
    pool = await database_manager.get_pool()

    return await pool.fetchrow(
        """
        select
            *
        from
            clients
        where
            email = $1
        """,
        client_email
    )
