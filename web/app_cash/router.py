import main
from config import settings
from fastapi import APIRouter, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from managers import WebsocketConnectionManager

rout_cash = APIRouter()

ws_manager = WebsocketConnectionManager()


@rout_cash.get("/cash/", response_class=HTMLResponse)
async def cash(request: Request):
    context = {
        settings.REQUEST_FIELD: request,
    }
    response = main.templates.TemplateResponse("cash/base.html", context)
    return response


@rout_cash.websocket("/ws/cash")
async def websocket_endpoint(websocket: WebSocket):
    try:
        await ws_manager.connect(websocket)

        while True:
            data = await websocket.receive_text()
            await ws_manager.receive(websocket, data)
    except WebSocketDisconnect:
        await ws_manager.disconnect(websocket)
