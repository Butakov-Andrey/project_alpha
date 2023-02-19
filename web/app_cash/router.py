from typing import Callable

import main
from app_auth.updated_auth import UpdatedAuthJWT
from app_auth.utils import get_role_dict
from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi_jwt_auth.exceptions import AuthJWTException

rout_cash = APIRouter(
    # prefix распространяется на этот роут
    prefix="/cash",
    tags=["cash"],
    responses={404: {"description": "Not found"}},
)


def auth_required(func: Callable) -> Callable:
    async def wrapper(
        request: Request, Authorize: UpdatedAuthJWT = Depends()
    ) -> Response:
        try:
            Authorize.jwt_required()
            print("Checking access token...")
        except AuthJWTException:
            try:
                Authorize.jwt_refresh_token_required()
                print("Checking refresh token...")
                current_user = Authorize.get_jwt_subject()
                role = get_role_dict(Authorize.get_raw_jwt()["role"])
                new_access_token = Authorize.create_access_token(
                    subject=current_user, user_claims=role, fresh=False
                )
                response = await func(request, Authorize, new_access_token)
                Authorize.set_access_cookies(new_access_token, response)
                return response
            except AuthJWTException:
                response = RedirectResponse("/auth/", status_code=303)
                return response
        response = await func(request, Authorize)
        return response

    return wrapper


@rout_cash.get("/", response_class=HTMLResponse)
@auth_required
async def cash(request: Request, Authorize: UpdatedAuthJWT, new_access_token=None):
    context = {"request": request}

    # код из @auth_required

    current_user = Authorize.get_jwt_subject()
    context["user"] = current_user
    response = main.get_templates().TemplateResponse("cash/base.html", context)
    if new_access_token is not None:
        Authorize.set_access_cookies(new_access_token, response)
    return response


# @rout_cash.get("/", response_class=HTMLResponse)
# async def cash(
#     request: Request, Authorize: UpdatedAuthJWT = Depends(), new_access_token=None
# ):
#     context = {"request": request}

#     try:
#         Authorize.jwt_required()
#         print("Checking access token...")
#     except AuthJWTException:
#         try:
#             Authorize.jwt_refresh_token_required()
#             print("Checking refresh token...")
#             current_user = Authorize.get_jwt_subject()
#             role = get_role_dict(Authorize.get_raw_jwt()["role"])
#             new_access_token = Authorize.create_access_token(
#                 subject=current_user, user_claims=role, fresh=False
#             )
#         except AuthJWTException:
#             response = RedirectResponse("/auth/", status_code=303)
#             return response

#     current_user = Authorize.get_jwt_subject()
#     context["user"] = current_user
#     response = main.get_templates().TemplateResponse("cash/base.html", context)
#     if new_access_token is not None:
#         Authorize.set_access_cookies(new_access_token, response)
#     return response
