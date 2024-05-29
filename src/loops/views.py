from asyncio import Event
from typing import Any

from fastapi import APIRouter, Query
from fastapi.security import HTTPBearer
from fastapi.websockets import WebSocket, WebSocketDisconnect, WebSocketState

from src.auth.dependencies import get_current_token_payload
from src.crud import get_client_by_id
from src.loops.schemas import (
    LoopsUpdateResponse,
)
from src.loops.service import (
    get_loops,
    get_platforms,
    get_currencies,
)

router = APIRouter()
security = HTTPBearer()
update_event = Event()

active_connections = []
loops: list[dict[str, Any]] | None = None


@router.websocket(path="/ws")
async def get_all_loops(
    websocket: WebSocket,
    token: str = Query(...),
):
    global loops

    await websocket.accept()

    try:
        token_payload = get_current_token_payload(token)
        client_in_db: dict[str, Any] | None = await get_client_by_id(
            token_payload.get("sub"),
        )

        if not client_in_db:
            await websocket.close()

            return

        active_connections.append(websocket)
        loops = await get_loops()
        update_event.set()

        while True:
            await update_event.wait()
            update_event.clear()
            await websocket.send_json(loops)

    except WebSocketDisconnect:
        active_connections.remove(websocket)


@router.get(path="/update", response_model=LoopsUpdateResponse)
async def update_endpoint() -> LoopsUpdateResponse:
    global loops

    loops = await get_loops()
    update_event.set()

    return LoopsUpdateResponse(message="Loops data has been updated.")


@router.get(path="/platforms")
async def get_all_platforms() -> list[str]:
    return await get_platforms()


@router.get(path="/currencies")
async def get_all_currencies() -> list[str]:
    return await get_currencies()
