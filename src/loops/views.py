from asyncio import Event
from typing import Any

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.websockets import WebSocket, WebSocketDisconnect

from src.auth.dependencies import get_current_token_payload
from src.crud import get_client_by_id
from src.loops.schemas import LoopsUpdateResponse
from src.loops.service import get_all_loops

router = APIRouter()
security = HTTPBearer()
update_event = Event()

active_connections = []
loops: list[dict[str, Any]] | None = None


@router.websocket(path="/ws")
async def get_loops(
    websocket: WebSocket,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    global loops

    await websocket.accept()
    token = credentials.credentials

    try:
        token_payload = get_current_token_payload(token)
        client_in_db: dict[str, Any] | None = await get_client_by_id(
            token_payload.get("sub"),
        )

        if not client_in_db:
            await websocket.close()

        active_connections.append(websocket)
        loops = await get_all_loops()
        await websocket.send_json(loops)

        while True:
            await update_event.wait()
            update_event.clear()
            await websocket.send_json(loops)

    except WebSocketDisconnect:
        active_connections.remove(websocket)


@router.get("/update")
async def update_endpoint() -> LoopsUpdateResponse:
    global loops

    loops = await get_all_loops()
    update_event.set()

    return LoopsUpdateResponse(message="Loops data has been updated.")
