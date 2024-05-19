from asyncio import Event
from typing import Any

from fastapi import APIRouter, WebSocket, Query, WebSocketDisconnect, status

from src.auth.dependencies import get_current_token_payload
from src.crud import get_client_by_id
from src.loops.service import get_all_loops

router = APIRouter()
active_connections = []
update_event = Event()


@router.websocket(path="/ws")
async def get_loops(
    websocket: WebSocket,
    # token: str = Query(...),
):
    await websocket.accept()

    try:
        # token_payload = get_current_token_payload(token)
        # client_in_db: dict[str, Any] | None = await get_client_by_id(
        #     token_payload.get("sub"),
        # )
        #
        # if not client_in_db:
        #     await websocket.close()

        active_connections.append(websocket)
        await websocket.send_json(await get_all_loops())

        while True:
            await update_event.wait()
            update_event.clear()
            await websocket.send_json(await get_all_loops())

    except WebSocketDisconnect:
        active_connections.remove(websocket)


@router.get("/update")
async def update_endpoint() -> dict[str, str]:
    update_event.set()

    return {"message": "Loops data has been updated."}
