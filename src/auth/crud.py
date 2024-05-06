from typing import Any

from src.database import get_pool


async def get_client_by_login(login: str) -> dict[str, Any] | None:
    pool = await get_pool()
    return await pool.fetchrow(
        """
        select
            *
        from
            clients
        where
            login = $1
        """,
        login
    )


async def add_client(
    login: str,
    password_hash: bytes,
) -> int:
    pool = await get_pool()
    return await pool.fetchval(
        """
        insert into
            clients (
                login,
                password_hash
            )
        values
            ($1, $2)
        returning
            id
        """,
        login,
        password_hash
    )


async def get_client_by_id(client_id: int) -> dict[str, Any]:
    pool = await get_pool()
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


async def get_client_status(login: str) -> bool:
    pool = await get_pool()
    return await pool.fetchval(
        """
        select (
            is_banned
        )
        from
            clients
        where
            login = $1
        """,
        login
    )
