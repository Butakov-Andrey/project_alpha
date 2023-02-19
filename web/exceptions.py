import main
from fastapi import Request
from fastapi.exception_handlers import http_exception_handler
from fastapi_jwt_auth.exceptions import AuthJWTException
from starlette.exceptions import HTTPException


async def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return main.get_templates().TemplateResponse(
        "401.html",
        {"request": request, "error": exc.message, "status_code": exc.status_code},
    )


async def custom_http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 404:
        return main.get_templates().TemplateResponse(
            "404.html",
            {"request": request, "error": exc.detail, "status_code": exc.status_code},
        )
    else:
        return await http_exception_handler(request, exc)
