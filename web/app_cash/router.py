import main
from app_auth.updated_auth import UpdatedAuthJWT, auth_required
from config import settings
from fastapi import APIRouter, Depends, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from managers import WebsocketConnectionManager

rout_cash = APIRouter()

ws_manager = WebsocketConnectionManager()


@rout_cash.get("/cash/", response_class=HTMLResponse)
@auth_required
async def cash(
    request: Request, Authorize: UpdatedAuthJWT = Depends(), new_access_token=None
):

    user = Authorize.get_jwt_subject()
    role = Authorize.get_raw_jwt()[settings.ROLE_FIELD]
    context = {
        settings.REQUEST_FIELD: request,
        settings.USER_FIELD: user,
        settings.ROLE_FIELD: role,
    }
    response = main.get_templates().TemplateResponse("cash/base.html", context)
    if new_access_token is not None:
        Authorize.set_access_cookies(new_access_token, response)
    return response


@rout_cash.websocket("/ws/cash")
async def websocket_endpoint(
    websocket: WebSocket, Authorize: UpdatedAuthJWT = Depends()
):
    try:
        await ws_manager.connect(websocket, Authorize)

        while True:
            data = await websocket.receive_text()
            await ws_manager.receive(websocket, Authorize, data)
    except WebSocketDisconnect:
        await ws_manager.disconnect(websocket)
