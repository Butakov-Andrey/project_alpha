import hmac
from typing import Any, Callable, Optional, Union

import main
from fastapi import Depends, Request, Response, WebSocket
from fastapi.responses import RedirectResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import (
    AuthJWTException,
    CSRFError,
    JWTDecodeError,
    MissingTokenError,
)


class UpdatedAuthJWT(AuthJWT):
    """
    Класс из библиотеки fastapi-jwt-auth (https://github.com/IndominusByte/fastapi-jwt-auth)
    Переопределен один метод
    """

    def _verify_and_get_jwt_in_cookies(
        self,
        type_token: str,
        request: Union[Request, WebSocket],
        csrf_token: Optional[str] = None,
        fresh: Optional[bool] = False,
    ) -> "AuthJWT":
        """
        Check if cookies have a valid access or refresh token. if an token present in
        cookies, self._token will set. raises exception error when an access or refresh token
        is invalid or doesn't match with CSRF token double submit
        :param type_token: indicate token is access or refresh token
        :param request: for identity get cookies from HTTP or WebSocket
        :param csrf_token: the CSRF double submit token
        :param fresh: check freshness token if True
        """
        if type_token not in ["access", "refresh"]:
            raise ValueError("type_token must be between 'access' or 'refresh'")
        if not isinstance(request, (Request, WebSocket)):
            raise TypeError("request must be an instance of 'Request' or 'WebSocket'")

        if type_token == "access":
            # метод пытается вытащить csrf_token из заголовка "X-CSRF-Token"
            # но токен находится в cookie
            csrf_cookie_key = self._access_csrf_cookie_key
            csrf_cookie = request.cookies.get(csrf_cookie_key)

            cookie_key = self._access_cookie_key
            cookie = request.cookies.get(cookie_key)
            if not isinstance(request, WebSocket):
                # csrf_token = request.headers.get(self._access_csrf_header_name)
                csrf_token = csrf_cookie

        if type_token == "refresh":
            csrf_cookie_key = self._refresh_csrf_cookie_key
            csrf_cookie = request.cookies.get(csrf_cookie_key)

            cookie_key = self._refresh_cookie_key
            cookie = request.cookies.get(cookie_key)
            if not isinstance(request, WebSocket):
                # csrf_token = request.headers.get(self._refresh_csrf_header_name)
                csrf_token = csrf_cookie
        if not cookie:
            raise MissingTokenError(
                status_code=401, message="Missing cookie {}".format(cookie_key)
            )

        if self._cookie_csrf_protect and not csrf_token:
            if isinstance(request, WebSocket) or request.method in self._csrf_methods:
                raise CSRFError(status_code=401, message="Missing CSRF Token")

        # set token from cookie and verify jwt
        self._token = cookie
        self._verify_jwt_in_request(self._token, type_token, "cookies", fresh)

        decoded_token = self.get_raw_jwt()

        if self._cookie_csrf_protect and csrf_token:
            if isinstance(request, WebSocket) or request.method in self._csrf_methods:
                if "csrf" not in decoded_token:
                    raise JWTDecodeError(status_code=422, message="Missing claim: csrf")
                if not hmac.compare_digest(csrf_token, decoded_token["csrf"]):
                    raise CSRFError(
                        status_code=401,
                        message="CSRF double submit tokens do not match",
                    )


def auth_required(func: Callable) -> Callable:
    async def wrapper(
        request: Request, Authorize: UpdatedAuthJWT = Depends()
    ) -> Response:
        """
        Декоратор проверяет access_token, если он не валидный,
        пытается получить новый из refresh_token, если он тоже не валидный,
        то отправляет на страницу авторизации
        """
        try:
            Authorize.jwt_required()
        except AuthJWTException:
            try:
                Authorize.jwt_refresh_token_required()
                current_user = Authorize.get_jwt_subject()

                new_access_token = Authorize.create_access_token(
                    subject=current_user,
                    user_claims={"role": Authorize.get_raw_jwt()["role"]},
                    fresh=False,
                )
                response = await func(request, Authorize, new_access_token)
                Authorize.set_access_cookies(new_access_token, response)
                return response
            except AuthJWTException:
                response = RedirectResponse("/auth/", status_code=303)
                return response
        return await func(request, Authorize)

    return wrapper


async def auth_jwt_required(Authorize: UpdatedAuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        user = Authorize.get_jwt_subject()
        role = Authorize.get_raw_jwt()["role"]
    except AuthJWTException:
        try:
            context: dict[str, Any] = dict()
            Authorize.jwt_refresh_token_required()
            user = Authorize.get_jwt_subject()
            role = Authorize.get_raw_jwt()["role"]
            new_access_token = Authorize.create_access_token(
                subject=user,
                user_claims={"role": role},
                fresh=False,
            )
            response = main.get_templates().TemplateResponse("cash/base.html", context)
            Authorize.set_access_cookies(new_access_token, response)
            return response
        except AuthJWTException:
            response = RedirectResponse("/auth/", status_code=303)
            return response
    return user, role
