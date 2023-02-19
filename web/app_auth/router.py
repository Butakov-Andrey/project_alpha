import main
from dependencies import get_db
from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi_jwt_auth.exceptions import AuthJWTException
from sqlalchemy.orm import Session

from .crud import create_user, get_user_by_email, get_users, is_user_by_email_exist
from .models import User
from .schema import UserIn, UserOut
from .updated_auth import UpdatedAuthJWT
from .utils import check_password, get_role_dict

rout_auth = APIRouter(
    # prefix распространяется на этот роут
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


@rout_auth.get("/", status_code=200, response_class=HTMLResponse)
async def auth(request: Request, Authorize: UpdatedAuthJWT = Depends()):
    try:
        Authorize.jwt_optional()
    except AuthJWTException:
        context = {"request": request}
        response = main.get_templates().TemplateResponse(
            "auth/account.html",
            context,
        )
        return response
    current_user = Authorize.get_jwt_subject() or None
    context = {"request": request, "user": current_user}
    response = main.get_templates().TemplateResponse(
        "auth/account.html",
        context,
    )
    return response


@rout_auth.post("/register", response_model=UserOut)
def register(user: UserIn, db: Session = Depends(get_db)) -> User:
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=400, detail=f"Email {user.email} already registered!"
        )
    return create_user(db=db, user=user)


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
        context = {"request": request, "error": "Incorrect email or password"}
        return main.get_templates().TemplateResponse("auth/account.html", context)

    db_user = get_user_by_email(db, email=email)
    if not check_password(password, db_user.hashed_password):
        context = {"request": request, "error": "Incorrect email or password"}
        return main.get_templates().TemplateResponse("auth/account.html", context)

    role = get_role_dict(db_user.role)
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


@rout_auth.post("/refresh")
def refresh(Authorize: UpdatedAuthJWT = Depends()) -> dict[str, str]:
    """
    Получаем access_token.
    fresh=False - значит, что для этого токена не проверялись логин и пароль
    """
    Authorize.jwt_refresh_token_required()
    current_user = Authorize.get_jwt_subject()
    role = get_role_dict(Authorize.get_raw_jwt()["role"])
    new_access_token = Authorize.create_access_token(
        subject=current_user, user_claims=role, fresh=False
    )
    Authorize.set_access_cookies(new_access_token)
    return {"msg": "The token has been refresh"}


@rout_auth.post("/logout")
async def logout(Authorize: UpdatedAuthJWT = Depends()) -> RedirectResponse:
    Authorize.jwt_required()
    response = RedirectResponse("/", status_code=303)
    Authorize.unset_jwt_cookies(response)
    return response


@rout_auth.get("/partially-protected")
def partially_protected(Authorize: UpdatedAuthJWT = Depends()) -> dict[str, str]:
    Authorize.jwt_optional()
    current_user = Authorize.get_jwt_subject() or "anonymous"
    return {"user": current_user}


@rout_auth.get("/protected")
def protected(Authorize: UpdatedAuthJWT = Depends()) -> dict[str, str]:
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    return {"user": current_user}


@rout_auth.get("/claims")
def user(Authorize: UpdatedAuthJWT = Depends()) -> dict[str, str]:
    Authorize.jwt_required()
    role = Authorize.get_raw_jwt()["role"]
    return {"role": role}


@rout_auth.get("/users", response_model=list[UserOut])
def read_users(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
) -> list[User]:
    users = get_users(db, skip=skip, limit=limit)
    return users
