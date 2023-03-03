from app_auth.utils import jwt_auth
from fastapi import WebSocket


class WebsocketConnectionManager:
    @jwt_auth.ws_auth_required
    async def connect(self, websocket: WebSocket):
        await websocket.accept()

    async def receive(self, websocket: WebSocket, data: str = "Default data"):
        await websocket.send_text(data)

    async def disconnect(self, websocket: WebSocket):
        await websocket.close(code=1000)


ws_manager = WebsocketConnectionManager()
