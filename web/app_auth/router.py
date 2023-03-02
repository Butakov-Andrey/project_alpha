import main
from config import RESPONSE_MESSAGE, STATUS_CODE, settings
from dependencies import get_db
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from .crud import get_user_by_email, is_user_by_email_exist
from .utils import jwt_auth, pass_handler

rout_auth = APIRouter(
    prefix="/auth",
)


# external
@rout_auth.get("/", status_code=STATUS_CODE.HTTP_200_OK, response_class=HTMLResponse)
@jwt_auth.auth_optional
async def auth(request: Request, user: str | None):
    context = {
        settings.REQUEST_FIELD: request,
        settings.USER_FIELD: user,
    }
    response = main.templates.TemplateResponse("auth/account.html", context)
    return response


# internal
@rout_auth.post("/login")
async def login(
    request: Request,
    db: Session = Depends(get_db),
    email: str = Form(...),
    password: str = Form(...),
):
    response = RedirectResponse("/", status_code=303)
    bad_response = main.templates.TemplateResponse(
        "auth/account.html",
        {
            settings.REQUEST_FIELD: request,
            settings.ERROR_FIELD: RESPONSE_MESSAGE.INCORRECT_CREDENTIALS,
        },
    )

    if not is_user_by_email_exist(db, email=email):
        return bad_response

    db_user = get_user_by_email(db, email=email)
    if not db_user or not pass_handler.check_password(
        password, str(db_user.hashed_password)
    ):
        return bad_response

    access_token = jwt_auth.create_access_token(subject=email)
    refresh_token = jwt_auth.create_refresh_token(subject=email)
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)
    return response


@rout_auth.post("/logout", response_class=HTMLResponse)
async def logout():
    response = RedirectResponse("/", status_code=303)
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return response
