from app_auth.router import auth
from app_cash.router import cash
from config import Settings, origins, server, static
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from redis_db import redis_conn

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
    # prefix распространяется на все роуты и документацию
    root_path="/web",
)

# static
app.mount("/static", StaticFiles(directory="static"), name="static")


# templates
templates = Jinja2Templates(directory="templates/")
templates.env.globals["static"] = static
templates.env.globals["server"] = server


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@AuthJWT.load_config
def get_config() -> Settings:
    return Settings()


@AuthJWT.token_in_denylist_loader
def check_if_token_in_denylist(decrypted_token: dict) -> None | str:
    """
    Проверяем, есть ли token в черном списке
    """
    jti = decrypted_token["jti"]
    entry = redis_conn.get(jti)
    return entry and entry == "true"


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


@app.get("/", status_code=200, response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


app.include_router(auth)
app.include_router(cash)
