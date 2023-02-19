from config import Settings
from dependencies import get_db
from fastapi import APIRouter, Depends, HTTPException
from redis_db import redis_conn
from sqlalchemy.orm import Session

from .crud import create_user, get_user_by_email, get_users
from .models import User
from .schema import UserIn, UserOut
from .updated_auth import UpdatedAuthJWT
from .utils import check_password, get_role_dict

auth = APIRouter(
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


@auth.post("/register", response_model=UserOut)
def register(user: UserIn, db: Session = Depends(get_db)) -> User:
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=400, detail=f"Email {user.email} already registered!"
        )
    return create_user(db=db, user=user)


@auth.post("/login")
def login(
    user: UserIn, Authorize: UpdatedAuthJWT = Depends(), db: Session = Depends(get_db)
) -> dict[str, str]:
    """
    Получаем fresh_access_token и refresh_token
    """
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        role = get_role_dict(db_user.role)
        if check_password(user.password, db_user.hashed_password):
            access_token = Authorize.create_access_token(
                subject=user.email, user_claims=role, fresh=True
            )
            refresh_token = Authorize.create_refresh_token(
                subject=user.email, user_claims=role
            )
            Authorize.set_access_cookies(access_token)
            Authorize.set_refresh_cookies(refresh_token)
            return {"msg": "Successfully login"}
    else:
        return {"message": "Incorrect email or password"}


@auth.post("/fresh-login")
def fresh_login(
    user: UserIn, Authorize: UpdatedAuthJWT = Depends(), db: Session = Depends(get_db)
) -> dict[str, str]:
    """
    Получаем fresh_access_token, не меняем refresh_token.
    Используем, где требуется дополнительное подтверждение логина и пароля.
    Пример: удаление репозитория в Github
    """
    db_user = get_user_by_email(db, email=user.email)
    role = get_role_dict(db_user.role)
    if check_password(user.password, db_user.hashed_password):
        new_access_token = Authorize.create_access_token(
            subject=user.email, user_claims=role, fresh=True
        )
        Authorize.set_access_cookies(new_access_token)
        return {"msg": "Successfully login"}
    else:
        return {"message": "Incorrect email or password"}


@auth.post("/refresh")
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


@auth.delete("/logout")
def logout(Authorize: UpdatedAuthJWT = Depends()) -> dict[str, str]:
    Authorize.jwt_required()
    Authorize.unset_jwt_cookies()
    return {"msg": "Successfully logout"}


@auth.delete("/access-revoke")
def access_revoke(Authorize: UpdatedAuthJWT = Depends()) -> dict[str, str]:
    """
    Добавляем в черный список access_token текущего пользователя
    """
    Authorize.jwt_required()
    jti = Authorize.get_raw_jwt()["jti"]
    redis_conn.setex(jti, Settings().access_expires, "true")
    return {"detail": "Access token has been revoke"}


@auth.delete("/refresh-revoke")
def refresh_revoke(Authorize: UpdatedAuthJWT = Depends()) -> dict[str, str]:
    """
    Добавляем в черный список refresh_token текущего пользователя
    """
    Authorize.jwt_refresh_token_required()
    jti = Authorize.get_raw_jwt()["jti"]
    redis_conn.setex(jti, Settings().refresh_expires, "true")
    return {"detail": "Refresh token has been revoke"}


@auth.get("/partially-protected")
def partially_protected(Authorize: UpdatedAuthJWT = Depends()) -> dict[str, str]:
    Authorize.jwt_optional()
    current_user = Authorize.get_jwt_subject() or "anonymous"
    return {"user": current_user}


@auth.get("/protected")
def protected(Authorize: UpdatedAuthJWT = Depends()) -> dict[str, str]:
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    return {"user": current_user}


@auth.get("/protected-fresh")
def protected_fresh(Authorize: UpdatedAuthJWT = Depends()) -> dict[str, str]:
    Authorize.fresh_jwt_required()
    current_user = Authorize.get_jwt_subject()
    return {"user": current_user}


@auth.get("/claims")
def user(Authorize: UpdatedAuthJWT = Depends()) -> dict[str, str]:
    Authorize.jwt_required()
    role = Authorize.get_raw_jwt()["role"]
    return {"role": role}


@auth.get("/users", response_model=list[UserOut])
def read_users(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
) -> list[User]:
    users = get_users(db, skip=skip, limit=limit)
    return users
