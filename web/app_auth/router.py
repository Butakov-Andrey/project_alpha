import main
from config import RESPONSE_MESSAGE, TEMPLATE_FIELDS, settings
from dependencies import get_db
from fastapi import APIRouter, Depends, Form, HTTPException, Request, Response
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from .crud import create_user, get_user_by_email, is_user_by_email_exist
from .utils import auth, jwt_auth

rout_auth = APIRouter(prefix="/auth")


@rout_auth.get("/")
@jwt_auth.auth_optional
async def account(request: Request, user: str | None) -> Response:
    context = {
        TEMPLATE_FIELDS.REQUEST: request,
        TEMPLATE_FIELDS.USER: user,
    }
    return main.templates.TemplateResponse("auth/account.html", context)


@rout_auth.post("/")
async def login(
    db: Session = Depends(get_db),
    email: str = Form(...),
    password: str = Form(...),
) -> Response:
    user = get_user_by_email(db, email=email)
    if not (user and auth.check_password(password, str(user.hashed_password))):
        raise HTTPException(
            status_code=403,
            detail=RESPONSE_MESSAGE.INVALID_CREDENTIALS,
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


@rout_auth.post("/logout")
async def logout() -> Response:
    response = RedirectResponse("/", status_code=303)
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return response


@rout_auth.get("/signup")
@jwt_auth.auth_optional
async def signup(request: Request, user: str | None) -> Response:
    context = {
        TEMPLATE_FIELDS.REQUEST: request,
        TEMPLATE_FIELDS.USER: user,
    }
    return main.templates.TemplateResponse("auth/signup.html", context)


@rout_auth.post("/signup")
async def signup_create(
    request: Request,
    db: Session = Depends(get_db),
    email: str = Form(...),
    password: str = Form(...),
) -> Response:
    if not auth.is_valid_email(email):
        message = RESPONSE_MESSAGE.INVALID_EMAIL
    elif is_user_by_email_exist(db, email=email):
        message = RESPONSE_MESSAGE.EMAIL_EXIST
    else:
        create_user(db=db, email=email, password=password)
        return RedirectResponse("/auth/", status_code=307)

    context = {
        TEMPLATE_FIELDS.REQUEST: request,
        TEMPLATE_FIELDS.MESSAGE: message,
    }
    return main.templates.TemplateResponse("auth/signup.html", context)
