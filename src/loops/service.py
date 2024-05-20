import json
from typing import Any

from src.loops.crud import get_loops, get_platforms, get_currencies
from src.loops.schemas import PlatformsResponse, CurrenciesResponse


async def get_all_loops() -> list[dict[str, Any]]:
    loops_in_db = await get_loops()

    return json.loads(loops_in_db)


async def get_all_platforms() -> list[str]:
    platforms = await get_platforms()

    return [platform[0] for platform in platforms]


async def get_all_currencies() -> list[str]:
    currencies = await get_currencies()

    return [currency[0] for currency in currencies]

