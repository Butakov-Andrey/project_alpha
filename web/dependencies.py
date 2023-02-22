from app_auth.updated_auth import UpdatedAuthJWT
from fastapi import Depends
from fastapi_jwt_auth.exceptions import AuthJWTException
from postgres_db import SessionLocal


# database dependency
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# JWT auth dependency
async def get_current_user_and_role_from_jwt(
    Authorize: UpdatedAuthJWT = Depends(),
) -> tuple[str | None, str | None]:
    user = None
    role = None
    try:
        Authorize.jwt_required()
    except AuthJWTException:
        try:
            Authorize.jwt_refresh_token_required()
        except AuthJWTException:
            return user, role
    user = Authorize.get_jwt_subject()
    role = Authorize.get_raw_jwt()["role"]
    return user, role
