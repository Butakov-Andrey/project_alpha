from app_auth.updated_auth import UpdatedAuthJWT, ws_auth_required
from fastapi import WebSocket


class WebsocketConnectionManager:
    @ws_auth_required
    async def connect(self, websocket: WebSocket, Authorize: UpdatedAuthJWT, data: str):
        await websocket.accept()

    @ws_auth_required
    async def receive(self, websocket: WebSocket, Authorize: UpdatedAuthJWT, data: str):
        pass

    async def disconnect(self, websocket: WebSocket):
        await websocket.close()
