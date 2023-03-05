import main
from config import TEMPLATE_FIELDS
from fastapi import Request, WebSocket, WebSocketDisconnect
from fastapi.responses import Response
from managers import ws_manager
from starlette.exceptions import HTTPException
from starlette.websockets import WebSocketState


async def custom_ws_exception_handler(
    websocket: WebSocket,
    exc: WebSocketDisconnect,
):
    # TODO logger instead of prints
    print("WS disconnected!", exc.code, exc.reason)
    if exc.code == 1001:
        print("Client is leaving")
    else:
        if websocket.application_state != WebSocketState.DISCONNECTED:
            await ws_manager.disconnect(websocket)


async def custom_http_exception_handler(
    request: Request,
    exc: HTTPException,
) -> Response:
    if exc.status_code == 401:
        return main.templates.TemplateResponse(
            "_exceptions/401.html",
            {
                TEMPLATE_FIELDS.REQUEST: request,
                TEMPLATE_FIELDS.ERROR: exc.detail,
                TEMPLATE_FIELDS.STATUS_CODE: exc.status_code,
            },
            status_code=401,
        )
    if exc.status_code == 403:

        return main.templates.TemplateResponse(
            "auth/account.html",
            context={
                TEMPLATE_FIELDS.REQUEST: request,
                TEMPLATE_FIELDS.MESSAGE: exc.detail,
                TEMPLATE_FIELDS.STATUS_CODE: exc.status_code,
            },
            status_code=403,
        )
    if exc.status_code == 404:
        # TODO Table of content
        return main.templates.TemplateResponse(
            "_exceptions/404.html",
            {
                TEMPLATE_FIELDS.REQUEST: request,
                TEMPLATE_FIELDS.ERROR: exc.detail,
                TEMPLATE_FIELDS.STATUS_CODE: exc.status_code,
            },
            status_code=404,
        )
    raise exc
