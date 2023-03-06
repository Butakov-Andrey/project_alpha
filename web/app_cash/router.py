import asyncio

import main
from app_auth.utils import jwt_auth
from config import TEMPLATE_FIELDS, settings
from fastapi import APIRouter, Request, Response, WebSocket
from loguru import logger
from managers import ws_manager

rout_cash = APIRouter()


@rout_cash.get("/cash/")
@jwt_auth.auth_required
async def cash(request: Request, user: str) -> Response:
    context = {
        TEMPLATE_FIELDS.REQUEST: request,
        TEMPLATE_FIELDS.USER: user,
    }
    return main.templates.TemplateResponse("cash/base.html", context)


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
        except asyncio.TimeoutError as exc:
            await ws_manager.disconnect(websocket)
            logger.info(f"WS connection closed due to inactivity! {exc}")
            break
