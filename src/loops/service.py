import json
from typing import Any

from src.loops.crud import get_all_loops, get_all_platforms, get_all_currencies


async def get_loops() -> list[dict[str, Any]]:
    loops_in_db: str | None = await get_all_loops()

    if not loops_in_db:
        print('No loops found currently.')

        return []

    return json.loads(loops_in_db)


async def get_platforms() -> list[str]:
    platforms = await get_all_platforms()

    return [platform[0] for platform in platforms]


async def get_currencies() -> list[str]:
    currencies = await get_all_currencies()

    return [currency[0] for currency in currencies]
