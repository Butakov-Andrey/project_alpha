import config
import requests
from dependencies import get_db
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from loguru import logger
from redis_db import redis_conn
from sqlalchemy.orm import Session

from .crud import create_user, get_user_by_email, get_users
from .schema import UserIn, UserOut
from .updated_auth import UpdatedAuthJWT
from .utils import check_password

auth = APIRouter(
    # prefix распространяется на этот роут
    prefix="",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

templates = Jinja2Templates(directory="templates")


@auth.post("/register", response_model=UserOut)
def register(user: UserIn, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        logger.info(f"Email {user.email} already registered!")
        raise HTTPException(
            status_code=400, detail=f"Email {user.email} already registered!"
        )
    return create_user(db=db, user=user)


@auth.post("/login")
def login(
    user: UserIn, Authorize: UpdatedAuthJWT = Depends(), db: Session = Depends(get_db)
):
    """
    Получаем fresh_access_token и refresh_token
    """
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        another_claims = {"info": "Дополнительная информация в jwt"}
        if check_password(user.password, db_user.hashed_password):
            access_token = Authorize.create_access_token(
                subject=user.email, user_claims=another_claims, fresh=True
            )
            refresh_token = Authorize.create_refresh_token(subject=user.email)
            Authorize.set_access_cookies(access_token)
            Authorize.set_refresh_cookies(refresh_token)
            return {"msg": "Successfully login"}
    else:
        return {"message": "Incorrect email or password"}


@auth.post("/fresh-login")
def fresh_login(
    user: UserIn, Authorize: UpdatedAuthJWT = Depends(), db: Session = Depends(get_db)
):
    """
    Получаем fresh_access_token, не меняем refresh_token.
    Используем, где требуется дополнительное подтверждение логина и пароля.
    Пример: удаление репозитория в Github
    """
    db_user = get_user_by_email(db, email=user.email)
    if check_password(user.password, db_user.hashed_password):
        another_claims = {"info": "Дополнительная информация в jwt"}
        new_access_token = Authorize.create_access_token(
            subject=user.email, user_claims=another_claims, fresh=True
        )
        Authorize.set_access_cookies(new_access_token)
        return {"msg": "Successfully login"}
    else:
        return {"message": "Incorrect email or password"}


@auth.post("/refresh")
def refresh(Authorize: UpdatedAuthJWT = Depends()):
    """
    Получаем access_token.
    fresh=False - значит, что для этого токена не проверялись логин и пароль
    """
    Authorize.jwt_refresh_token_required()
    current_user = Authorize.get_jwt_subject()
    another_claims = {"info": "Дополнительная информация в jwt"}
    new_access_token = Authorize.create_access_token(
        subject=current_user, user_claims=another_claims, fresh=False
    )
    Authorize.set_access_cookies(new_access_token)
    return {"msg": "The token has been refresh"}


@auth.delete("/logout")
def logout(Authorize: UpdatedAuthJWT = Depends()):
    Authorize.jwt_required()
    Authorize.unset_jwt_cookies()
    return {"msg": "Successfully logout"}


@auth.delete("/access-revoke")
def access_revoke(Authorize: UpdatedAuthJWT = Depends()):
    """
    Добавляем в черный список access_token текущего пользователя
    """
    Authorize.jwt_required()
    jti = Authorize.get_raw_jwt()["jti"]
    redis_conn.setex(jti, config.settings.access_expires, "true")
    return {"detail": "Access token has been revoke"}


@auth.delete("/refresh-revoke")
def refresh_revoke(Authorize: UpdatedAuthJWT = Depends()):
    """
    Добавляем в черный список refresh_token текущего пользователя
    """
    Authorize.jwt_refresh_token_required()
    jti = Authorize.get_raw_jwt()["jti"]
    redis_conn.setex(jti, config.settings.refresh_expires, "true")
    return {"detail": "Refresh token has been revoke"}


@auth.get("/partially-protected")
def partially_protected(Authorize: UpdatedAuthJWT = Depends()):
    Authorize.jwt_optional()
    current_user = Authorize.get_jwt_subject() or "anonymous"
    return {"user": current_user}


@auth.get("/protected")
def protected(Authorize: UpdatedAuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    return {"user": current_user}


@auth.get("/protected-fresh")
def protected_fresh(Authorize: UpdatedAuthJWT = Depends()):
    Authorize.fresh_jwt_required()
    current_user = Authorize.get_jwt_subject()
    return {"user": current_user}


@auth.get("/claims")
def user(request: Request, Authorize: UpdatedAuthJWT = Depends()):
    Authorize.jwt_required()
    foo_claims = Authorize.get_raw_jwt()["info"]

    url = "http://web:8000/api/v1/"
    session = requests.Session()
    session.trust_env = False
    res = session.get(url)
    print(res.text)

    return {"info": foo_claims, "microserv": res.text}


@auth.get("/users", response_model=list[UserOut])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users
