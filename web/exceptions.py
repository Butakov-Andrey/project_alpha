import main
from config import STATUS_CODE, settings
from fastapi import Request
from fastapi.responses import RedirectResponse, Response
from starlette.exceptions import HTTPException


async def authjwt_exception_handler() -> RedirectResponse:
    response = RedirectResponse("/auth/", status_code=STATUS_CODE.HTTP_303_SEE_OTHER)
    return response


async def custom_http_exception_handler(
    request: Request, exc: HTTPException
) -> Response:
    if exc.status_code == STATUS_CODE.HTTP_404_NOT_FOUND:
        return main.get_templates().TemplateResponse(
            "_exceptions/404.html",
            {
                settings.REQUEST_FIELD: request,
                settings.ERROR_FIELD: exc.detail,
                settings.STATUS_CODE_FIELD: exc.status_code,
            },
        )
    else:
        raise exc
