import config
from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from redis_db import redis_conn

from .schema import User
from .updated_auth import UpdatedAuthJWT

auth = APIRouter(
    # prefix распространяется на этот роут
    prefix="/api/v1",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


@AuthJWT.load_config
def get_config():
    return config.Settings()


@AuthJWT.token_in_denylist_loader
def check_if_token_in_denylist(decrypted_token):
    """
    Проверяем, есть ли token в черном списке
    """
    jti = decrypted_token["jti"]
    entry = redis_conn.get(jti)
    return entry and entry == "true"


@auth.post("/login")
def login(user: User, Authorize: UpdatedAuthJWT = Depends()):
    """
    Получаем fresh_access_token и refresh_token
    """
    if user.username != "test" or user.password != "test":
        raise HTTPException(status_code=401, detail="Bad username or password")
    access_token = Authorize.create_access_token(subject=user.username, fresh=True)
    refresh_token = Authorize.create_refresh_token(subject=user.username)
    Authorize.set_access_cookies(access_token)
    Authorize.set_refresh_cookies(refresh_token)
    return {"msg": "Successfully login"}


@auth.post("/fresh-login")
def fresh_login(user: User, Authorize: UpdatedAuthJWT = Depends()):
    """
    Получаем fresh_access_token, не меняем refresh_token.
    Используем, где требуется дополнительное подтверждение логина и пароля.
    Пример: удаление репозитория в Github
    """
    if user.username != "test" or user.password != "test":
        raise HTTPException(status_code=401, detail="Bad username or password")
    new_access_token = Authorize.create_access_token(subject=user.username, fresh=True)
    Authorize.set_access_cookies(new_access_token)
    return {"msg": "Successfully login"}


@auth.post("/refresh")
def refresh(Authorize: UpdatedAuthJWT = Depends()):
    """
    Получаем access_token.
    fresh - значит, что для этого токена проверялись логин и пароль
    """
    Authorize.jwt_refresh_token_required()
    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user, fresh=False)
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
def protected(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    return {"user": current_user}


@auth.get("/protected-fresh")
def protected_fresh(Authorize: AuthJWT = Depends()):
    Authorize.fresh_jwt_required()
    current_user = Authorize.get_jwt_subject()
    return {"user": current_user}
