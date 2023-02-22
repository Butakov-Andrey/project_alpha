import main
from app_auth.updated_auth import UpdatedAuthJWT, auth_required
from fastapi import APIRouter, Depends, Request, WebSocket
from fastapi.responses import HTMLResponse

rout_cash = APIRouter()


@rout_cash.get("/cash/", response_class=HTMLResponse)
@auth_required
async def cash(
    request: Request, Authorize: UpdatedAuthJWT = Depends(), new_access_token=None
):
    user = Authorize.get_jwt_subject()
    role = Authorize.get_raw_jwt()["role"]
    context = {"request": request, "user": user, "role": role}
    response = main.get_templates().TemplateResponse("cash/base.html", context)
    if new_access_token is not None:
        Authorize.set_access_cookies(new_access_token, response)
    return response


@rout_cash.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print("Accepting client connection...")
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")
