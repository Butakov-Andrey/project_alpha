from fastapi import WebSocket


class WebsocketConnectionManager:
    async def connect(self, websocket: WebSocket):
        await websocket.accept()

    async def receive(self, websocket: WebSocket, data: str):
        pass

    async def disconnect(self, websocket: WebSocket):
        await websocket.close()
