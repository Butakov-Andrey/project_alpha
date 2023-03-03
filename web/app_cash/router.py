import main
from app_auth.utils import jwt_auth
from config import settings
from fastapi import APIRouter, Request, WebSocket
from fastapi.responses import HTMLResponse
from managers import ws_manager

rout_cash = APIRouter()


@rout_cash.get("/cash/", response_class=HTMLResponse)
@jwt_auth.auth_required
async def cash(request: Request, user: str):
    context = {
        settings.REQUEST_FIELD: request,
        settings.USER_FIELD: user,
    }
    response = main.templates.TemplateResponse("cash/base.html", context)
    return response


@rout_cash.websocket("/ws/cash")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    while True:
        data = await websocket.receive_text()
        await ws_manager.receive(websocket, data)
