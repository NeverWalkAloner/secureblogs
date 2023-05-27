from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    Query,
    status,
    WebSocket,
    WebSocketDisconnect,
    WebSocketException,
)

from app.api.deps import DBSession
from app.api.websockets.managers import ws_manager
from app.crud.crud_user import get_user_by_token


router = APIRouter()


async def get_token(
    websocket: WebSocket,
    token: Annotated[str | None, Query()] = None,
):
    if token is None:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    return token


@router.websocket("/ws/post_request")
async def websocket_endpoint(
    websocket: WebSocket,
    db: DBSession,
    token: Annotated[str, Depends(get_token)],
):
    user = await get_user_by_token(db, token)
    if not user:
        raise WebSocketException(code=status.HTTP_401_UNAUTHORIZED)
    try:
        await ws_manager.connect(user.id, websocket)
        await ws_manager.send_personal_message(
            {"message": "connection accepted"},
            user.id,
        )
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(user.id)
