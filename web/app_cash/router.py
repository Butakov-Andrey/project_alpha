import asyncio

import main
from app_auth.utils import jwt_auth
from config import TEMPLATE_FIELDS, settings
from fastapi import APIRouter, Request, WebSocket
from fastapi.responses import HTMLResponse
from managers import ws_manager

rout_cash = APIRouter()


@rout_cash.get("/cash/", response_class=HTMLResponse)
@jwt_auth.auth_required
async def cash(request: Request, user: str):
    context = {
        TEMPLATE_FIELDS.REQUEST: request,
        TEMPLATE_FIELDS.USER: user,
    }
    response = main.templates.TemplateResponse("cash/base.html", context)
    return response


@rout_cash.websocket("/ws/cash")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    while True:
        try:
            data = await asyncio.wait_for(
                websocket.receive_text(),
                timeout=settings.WS_CONNECTION_TIMEOUT_SECONDS,
            )
            await ws_manager.receive(websocket, data)
        except asyncio.TimeoutError:
            await ws_manager.disconnect(websocket)
            print("Connection closed due to inactivity")
            break
