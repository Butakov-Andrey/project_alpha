from app_auth.router import rout_auth
from app_cash.router import rout_cash
from config import STATUS_CODE, Settings, settings
from dependencies import get_current_user_and_role_from_jwt
from exceptions import authjwt_exception_handler, custom_http_exception_handler
from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from starlette.exceptions import HTTPException
from starlette.templating import _TemplateResponse

app = FastAPI(
    title="Project Alpha",
    version="0.0.1",
    contact={
        "name": "Andrey Butakov",
        "email": "6669.butakov@gmail.com",
    },
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url=None,
)

# templates
templates = Jinja2Templates(directory="templates/")
templates.env.globals["static"] = settings.STATIC_URL
templates.env.globals["server"] = settings.SERVER_URL

# static
app.mount("/static", StaticFiles(directory="static"))

# middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# templates
def get_templates() -> Jinja2Templates:
    return templates


# authJWT
@AuthJWT.load_config
def get_config() -> Settings:
    return settings


# home
@app.get("/", status_code=STATUS_CODE.HTTP_200_OK, response_class=HTMLResponse)
async def home(
    request: Request,
    user_and_role: tuple[str | None, str | None] = Depends(
        get_current_user_and_role_from_jwt
    ),
) -> _TemplateResponse:
    user, role = user_and_role
    context = {
        settings.REQUEST_FIELD: request,
        settings.USER_FIELD: user,
        settings.ROLE_FIELD: role,
    }
    response = get_templates().TemplateResponse("home.html", context)
    return response


# Exception Handlers
app.add_exception_handler(AuthJWTException, authjwt_exception_handler)
app.add_exception_handler(HTTPException, custom_http_exception_handler)

# Routers
app.include_router(rout_auth)
app.include_router(rout_cash)
