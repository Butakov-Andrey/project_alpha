import main
from config import settings
from fastapi import Request, WebSocket, WebSocketDisconnect
from fastapi.responses import Response
from managers import ws_manager
from starlette.exceptions import HTTPException
from starlette.websockets import WebSocketState


async def custom_ws_exception_handler(websocket: WebSocket, exc: WebSocketDisconnect):
    print("WS disconnected!", exc.code, exc.reason)
    if exc.code == 1001:
        print("Client is leaving")
    else:
        if websocket.application_state != WebSocketState.DISCONNECTED:
            await ws_manager.disconnect(websocket)


async def custom_http_exception_handler(
    request: Request, exc: HTTPException
) -> Response:
    if exc.status_code == 404:
        return main.templates.TemplateResponse(
            "_exceptions/404.html",
            {
                settings.REQUEST_FIELD: request,
                settings.ERROR_FIELD: exc.detail,
                settings.STATUS_CODE_FIELD: exc.status_code,
            },
        )
    elif exc.status_code == 401:
        return main.templates.TemplateResponse(
            "auth/account.html",
            {
                settings.REQUEST_FIELD: request,
                settings.ERROR_FIELD: exc.detail,
            },
        )
    else:
        raise exc
