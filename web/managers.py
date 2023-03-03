from app_auth.utils import jwt_auth
from fastapi import WebSocket


class WebsocketConnectionManager:
    @jwt_auth.ws_auth_required
    async def connect(self, websocket: WebSocket, data: str):
        await websocket.accept()

    @jwt_auth.ws_auth_required
    async def receive(self, websocket: WebSocket, data: str):
        await websocket.send_text(data)

    async def disconnect(self, websocket: WebSocket):
        await websocket.close(code=1000)


ws_manager = WebsocketConnectionManager()
