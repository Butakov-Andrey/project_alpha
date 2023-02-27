import main
from config import STATUS_CODE, settings
from dependencies import get_current_user_and_role_from_jwt, get_db
from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi_jwt_auth.exceptions import AuthJWTException
from sqlalchemy.orm import Session

from .crud import create_user, get_user_by_email, is_user_by_email_exist
from .models import User
from .schema import UserIn, UserOut
from .updated_auth import UpdatedAuthJWT
from .utils import check_password

rout_auth = APIRouter(
    # prefix распространяется на этот роут
    prefix="/auth",
)


# external
@rout_auth.get("/", status_code=STATUS_CODE.HTTP_200_OK, response_class=HTMLResponse)
async def auth(
    request: Request,
    user_and_role=Depends(get_current_user_and_role_from_jwt),
):
    user, role = user_and_role
    context = {
        settings.REQUEST_FIELD: request,
        settings.USER_FIELD: user,
        settings.ROLE_FIELD: role,
    }
    response = main.get_templates().TemplateResponse("auth/account.html", context)
    return response


# internal
@rout_auth.post("/login")
async def login(
    request: Request,
    Authorize: UpdatedAuthJWT = Depends(),
    db: Session = Depends(get_db),
    email: str = Form(...),
    password: str = Form(...),
) -> RedirectResponse:
    """
    Получаем fresh_access_token и refresh_token
    """
    if not is_user_by_email_exist(db, email=email):
        return main.get_templates().TemplateResponse(
            "auth/account.html",
            {
                settings.REQUEST_FIELD: request,
                settings.ERROR_FIELD: settings.INCORRECT_CREDENTIALS,
            },
        )

    db_user = get_user_by_email(db, email=email)
    if not db_user or not check_password(password, str(db_user.hashed_password)):
        return main.get_templates().TemplateResponse(
            "auth/account.html",
            {
                settings.REQUEST_FIELD: request,
                settings.ERROR_FIELD: settings.INCORRECT_CREDENTIALS,
            },
        )

    role = {settings.ROLE_FIELD: db_user.role}
    response = RedirectResponse("/", status_code=303)
    access_token = Authorize.create_access_token(
        subject=email,
        user_claims=role,
        fresh=True,
    )
    refresh_token = Authorize.create_refresh_token(
        subject=email,
        user_claims=role,
    )
    Authorize.set_access_cookies(access_token, response)
    Authorize.set_refresh_cookies(refresh_token, response)
    return response


@rout_auth.post("/logout")
async def logout(Authorize: UpdatedAuthJWT = Depends()) -> RedirectResponse:
    response = RedirectResponse("/", status_code=303)
    try:
        Authorize.jwt_required()
        Authorize.unset_jwt_cookies(response)
        return response
    except AuthJWTException:
        Authorize.unset_jwt_cookies(response)
        return response


# waiting...
@rout_auth.post("/register", response_model=UserOut)
def register(user: UserIn, db: Session = Depends(get_db)) -> User:
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=400, detail=f"Email {user.email} already registered!"
        )
    return create_user(db=db, user=user)
