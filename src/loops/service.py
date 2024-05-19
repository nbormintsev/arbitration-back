import json
from typing import Any

from src.loops.crud import get_loops


async def get_all_loops() -> list[dict[str, Any]]:
    loops = await get_loops()
    return json.loads(loops)
