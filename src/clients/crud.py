from datetime import timedelta, datetime
from typing import Any

from src.database import database_manager


async def get_client_settings_by_id(client_id: int) -> dict[str, Any] | None:
    pool = await database_manager.get_pool()

    return await pool.fetchrow(
        """
        select
            *
        from
            client_settings
        where
            client = $1
        """,
        client_id
    )


async def create_client_settings(
    client_id: int,
    notification_min_spread: float,
    language: str,
    timezone_offset: timedelta,
) -> int:
    pool = await database_manager.get_pool()

    return await pool.fetchval(
        """
        insert into
            client_settings (
                client,
                notification_min_spread,
                language,
                timezone_offset
            )
        values
            ($1, $2, $3, $4)
        returning
            id
        """,
        client_id,
        notification_min_spread,
        language,
        timezone_offset
    )


async def update_client_settings(
    client_id: int,
    notification_min_spread: float,
    language: str,
    timezone_offset: timedelta,
) -> int:
    pool = await database_manager.get_pool()

    return await pool.fetchval(
        """
        update
            client_settings
        set
            notification_min_spread = $1,
            language = $2,
            timezone_offset = $3
        where
            client = $4
        returning
            id
        """,
        notification_min_spread,
        language,
        timezone_offset,
        client_id
    )


async def create_client_device(
    client_id: int,
    device_hash: bytes,
    device_name: str,
    last_online: datetime,
) -> int:
    pool = await database_manager.get_pool()

    return await pool.fetchval(
        """
        insert into
            client_devices (
                client,
                device_hash,
                device_name,
                last_online
            )
        values
            ($1, $2, $3, $4)
        returning
            id
        """,
        client_id,
        device_hash,
        device_name,
        last_online
    )


async def get_client_devices_by_id(client_id: int) -> list:
    pool = await database_manager.get_pool()

    return await pool.fetch(
        """
        select
            *
        from
            client_devices
        where
            client = $1
        """,
        client_id
    )


async def remove_client_device(device_id: int) -> dict[str, Any] | None:
    pool = await database_manager.get_pool()

    return await pool.fetchrow(
        """
        delete from
            client_devices
        where
            id = $1
        returning
            *
        """,
        device_id
    )


async def update_client_password(
    client_id: int,
    password_hash: bytes,
) -> int:
    pool = await database_manager.get_pool()

    return await pool.fetchval(
        """
        update
            clients
        set
            password_hash = $1
        where
            id = $2
        returning
            id
        """,
        password_hash,
        client_id
    )
