from typing import Any

from src.database import get_pool


async def get_client_by_email(email: str) -> dict[str, Any] | None:
    pool = await get_pool()

    return await pool.fetchrow(
        """
        select
            *
        from
            clients
        where
            email = $1
        """,
        email
    )


async def add_client(
    email: str,
    name: str,
    password_hash: bytes,
) -> int:
    pool = await get_pool()

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


async def get_client_status(email: str) -> bool:
    pool = await get_pool()

    return await pool.fetchval(
        """
        select (
            is_banned
        )
        from
            clients
        where
            email = $1
        """,
        email
    )
