import main
from config import RESPONSE_MESSAGE, TEMPLATE_FIELDS, settings
from dependencies import get_db
from fastapi import APIRouter, Depends, Form, Header, HTTPException, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from .crud import get_user_by_email
from .utils import auth, jwt_auth

rout_auth = APIRouter(
    prefix="/auth",
)


# external
@rout_auth.get("/", status_code=200, response_class=HTMLResponse)
@jwt_auth.auth_optional
async def account(request: Request, user: str | None) -> Response:
    # TODO
    csrf_token = request.cookies.get("csrftoken")

    context = {
        TEMPLATE_FIELDS.REQUEST: request,
        TEMPLATE_FIELDS.USER: user,
        "test": csrf_token,
    }
    response = main.templates.TemplateResponse("auth/account.html", context)
    return response


# internal
@rout_auth.post("/login")
async def login(
    db: Session = Depends(get_db), email: str = Form(...), password: str = Form(...)
) -> Response:
    # check email and password
    user = get_user_by_email(db, email=email)
    if not (user and auth.check_password(password, str(user.hashed_password))):
        raise HTTPException(
            status_code=401,
            detail=RESPONSE_MESSAGE.INCORRECT_CREDENTIALS,
        )

    access_token = jwt_auth.create_access_token(subject=email)
    refresh_token = jwt_auth.create_refresh_token(subject=email)
    response = RedirectResponse("/", status_code=303)

    response.set_cookie(
        key="access_token",
        value=access_token,
        max_age=settings.COOKIE_EXPIRE_SECONDS,
        expires=settings.COOKIE_EXPIRE_SECONDS,
        httponly=True,
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        max_age=settings.COOKIE_EXPIRE_SECONDS,
        expires=settings.COOKIE_EXPIRE_SECONDS,
        httponly=True,
    )
    return response


@rout_auth.post("/logout", response_class=HTMLResponse)
async def logout() -> Response:
    response = RedirectResponse("/", status_code=303)
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return response
