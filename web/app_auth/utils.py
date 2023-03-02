from datetime import datetime, timedelta
from typing import Any, Callable

import bcrypt
import jwt
from fastapi import Request
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError


class PasswordHandler:
    def hash_password(self, password: str) -> str:
        encoded_password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        password_hash = encoded_password_hash.decode()
        return password_hash

    def check_password(self, pass_from_user: str, hashed_pass_from_db: str) -> bool:
        return bcrypt.checkpw(pass_from_user.encode(), hashed_pass_from_db.encode())


class JWTHandler:
    def __init__(self):
        # self.ACCESS_TOKEN_EXPIRE_MINUTES = 30
        # self.REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 1
        self.REFRESH_TOKEN_EXPIRE_MINUTES = 2
        self.ALGORITHM = "HS256"
        self.JWT_SECRET_KEY = "secret"
        self.JWT_REFRESH_SECRET_KEY = "refresh_secret"

    def create_access_token(
        self, subject: str | Any, expires_delta: timedelta | None = None
    ) -> str:
        if expires_delta is not None:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES
            )

        to_encode = {"exp": expire, "sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, self.JWT_SECRET_KEY, self.ALGORITHM)
        return encoded_jwt

    def create_refresh_token(
        self, subject: str | Any, expires_delta: timedelta | None = None
    ) -> str:
        if expires_delta is not None:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=self.REFRESH_TOKEN_EXPIRE_MINUTES
            )

        to_encode = {"exp": expire, "sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, self.JWT_REFRESH_SECRET_KEY, self.ALGORITHM)
        return encoded_jwt

    def auth_optional(self, func: Callable) -> Callable:
        async def wrapper(request: Request):
            access_token = request.cookies.get("access_token")
            refresh_token = request.cookies.get("refresh_token")
            if not (access_token and refresh_token):
                print("Tokens not found in cookies")
                return await func(request, user=None)

            try:
                print("Check access token...")
                payload = jwt.decode(
                    access_token,
                    self.JWT_SECRET_KEY,
                    algorithms=[self.ALGORITHM],
                )
                print("Access token is valid")
            except ExpiredSignatureError:
                print("Access token's exp is expired")
                try:
                    print("Check refresh token...")
                    payload = jwt.decode(
                        refresh_token,
                        self.JWT_REFRESH_SECRET_KEY,
                        algorithms=[self.ALGORITHM],
                    )
                    print("Refresh token is valid")
                except InvalidTokenError:
                    print("Refresh token is expired or not valid")
                    return await func(request, user=None)
            except InvalidTokenError:
                print("Access token is invalid")
                return await func(request, user=None)

            print(f"Tokens are valid. User is {payload.get('sub')}")
            return await func(request, user=payload.get("sub"))

        return wrapper

    # TODO
    def auth_required(self, func: Callable) -> Callable:
        async def wrapper(request: Request):
            pass

        return wrapper


jwt_auth = JWTHandler()
pass_handler = PasswordHandler()
