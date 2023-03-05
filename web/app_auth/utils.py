from datetime import datetime, timedelta
from typing import Any, Callable

import bcrypt
import jwt
from config import COOKIE, RESPONSE_MESSAGE, settings
from fastapi import HTTPException, Request, WebSocket, WebSocketDisconnect
from jwt.exceptions import InvalidTokenError
from pydantic import EmailStr


class AuthHandler:
    def hash_password(self, password: str) -> str:
        encoded_password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        password_hash = encoded_password_hash.decode()
        return password_hash

    def check_password(self, pass_from_user: str, hashed_pass_from_db: str) -> bool:
        return bcrypt.checkpw(pass_from_user.encode(), hashed_pass_from_db.encode())

    def is_valid_email(self, email: str) -> bool:
        try:
            EmailStr.validate(email)
            return True
        except ValueError:
            return False


class JWTHandler:
    def create_access_token(
        self, subject: str | Any, expires_delta: timedelta | None = None
    ) -> str:
        if expires_delta is not None:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )

        to_encode = {"exp": expire, "sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, settings.ALGORITHM)
        return encoded_jwt

    def create_refresh_token(
        self, subject: str | Any, expires_delta: timedelta | None = None
    ) -> str:
        if expires_delta is not None:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
            )

        to_encode = {"exp": expire, "sub": str(subject)}
        encoded_jwt = jwt.encode(
            to_encode, settings.JWT_REFRESH_SECRET_KEY, settings.ALGORITHM
        )
        return encoded_jwt

    def auth_optional(self, func: Callable) -> Callable:
        async def wrapper(request: Request):
            access_token = request.cookies.get(COOKIE.ACCESS)
            refresh_token = request.cookies.get(COOKIE.REFRESH)
            if not (access_token and refresh_token):
                return await func(request, user=None)
            try:
                payload = jwt.decode(
                    access_token,
                    settings.JWT_SECRET_KEY,
                    algorithms=[settings.ALGORITHM],
                )
            except InvalidTokenError:
                try:
                    payload = jwt.decode(
                        refresh_token,
                        settings.JWT_REFRESH_SECRET_KEY,
                        algorithms=[settings.ALGORITHM],
                    )
                except InvalidTokenError:
                    return await func(request, user=None)
            return await func(request, user=payload.get("sub"))

        return wrapper

    def auth_required(self, func: Callable) -> Callable:
        async def wrapper(request: Request):
            access_token = request.cookies.get(COOKIE.ACCESS)
            refresh_token = request.cookies.get(COOKIE.REFRESH)
            if not (access_token and refresh_token):
                raise HTTPException(status_code=401, detail=RESPONSE_MESSAGE.NO_TOKENS)
            try:
                payload = jwt.decode(
                    access_token,
                    settings.JWT_SECRET_KEY,
                    algorithms=[settings.ALGORITHM],
                )
                response = await func(request, user=payload.get("sub"))
            except InvalidTokenError:
                try:
                    payload = jwt.decode(
                        refresh_token,
                        settings.JWT_REFRESH_SECRET_KEY,
                        algorithms=[settings.ALGORITHM],
                    )
                    response = await func(request, user=payload.get("sub"))
                    new_access_token = self.create_access_token(
                        subject=payload.get("sub")
                    )
                    response.set_cookie(
                        key="access_token",
                        value=new_access_token,
                        max_age=settings.COOKIE_EXPIRE_SECONDS,
                        expires=settings.COOKIE_EXPIRE_SECONDS,
                        httponly=True,
                    )
                except InvalidTokenError:
                    raise HTTPException(
                        status_code=401, detail=RESPONSE_MESSAGE.INVALID_TOKENS
                    )
            return response

        return wrapper

    def ws_auth_required(self, func: Callable) -> Callable:
        async def wrapper(self, websocket: WebSocket, data: str = "mes"):
            response = await func(self, websocket, data)
            access_token = websocket.cookies.get("access_token")
            refresh_token = websocket.cookies.get("refresh_token")
            if not (access_token and refresh_token):
                raise WebSocketDisconnect(code=1008, reason=RESPONSE_MESSAGE.NO_TOKENS)
            try:
                jwt.decode(
                    access_token,
                    settings.JWT_SECRET_KEY,
                    algorithms=[settings.ALGORITHM],
                )
            except InvalidTokenError:
                try:
                    jwt.decode(
                        refresh_token,
                        settings.JWT_REFRESH_SECRET_KEY,
                        algorithms=[settings.ALGORITHM],
                    )
                except InvalidTokenError:
                    raise WebSocketDisconnect(
                        code=1008, reason=RESPONSE_MESSAGE.INVALID_TOKENS
                    )
            return response

        return wrapper


jwt_auth = JWTHandler()
auth = AuthHandler()
