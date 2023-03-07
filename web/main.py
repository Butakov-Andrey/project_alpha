from app_auth.router import rout_auth
from app_auth.utils import jwt_auth
from app_cash.router import rout_cash
from config import TEMPLATE_FIELDS, settings
from dependencies import logging
from exceptions import custom_http_exception_handler, custom_ws_exception_handler
from fastapi import Depends, FastAPI, Request, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from logger import add_loggers
from starlette.exceptions import HTTPException

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

# logger
add_loggers()

# templates
templates = Jinja2Templates(directory="templates/")
templates.env.globals["static"] = settings.STATIC_URL
templates.env.globals["server"] = settings.SERVER_URL

# static
app.mount("/static", StaticFiles(directory="static"))

# cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# home
@app.get("/", status_code=200, dependencies=[Depends(logging)])
@jwt_auth.auth_optional
async def home(request: Request, user: str | None) -> Response:
    context = {
        TEMPLATE_FIELDS.REQUEST: request,
        TEMPLATE_FIELDS.USER: user,
    }
    response = templates.TemplateResponse("home.html", context)
    return response


# exception Handlers
app.add_exception_handler(HTTPException, custom_http_exception_handler)
app.add_exception_handler(WebSocketDisconnect, custom_ws_exception_handler)

# routers
app.include_router(rout_auth, dependencies=[Depends(logging)])
app.include_router(rout_cash, dependencies=[Depends(logging)])
