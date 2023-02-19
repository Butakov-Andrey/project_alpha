import main
from app_auth.updated_auth import UpdatedAuthJWT
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

cash = APIRouter(
    # prefix распространяется на этот роут
    prefix="/cash",
    tags=["cash"],
    responses={404: {"description": "Not found"}},
)


@cash.get("/", response_class=HTMLResponse)
async def test(request: Request, Authorize: UpdatedAuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    context = {"request": request, "user": current_user}
    return main.templates.TemplateResponse("cash/base.html", context)
