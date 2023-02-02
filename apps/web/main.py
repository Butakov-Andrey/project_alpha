import config
import dependencies
import logger
from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from redis_db import redis_conn
from test_app import router

logger.add_loggers()

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# добавляем в любое приложение, где необходима авторизация
@AuthJWT.load_config
def get_config():
    return config.Settings()


# добавляем в любое приложение, где необходима авторизация
@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


# добавляем в любое приложение, где необходима авторизация
@AuthJWT.token_in_denylist_loader
def check_if_token_in_denylist(decrypted_token):
    """
    Проверяем, есть ли token в черном списке
    """
    jti = decrypted_token["jti"]
    entry = redis_conn.get(jti)
    return entry and entry == "true"


app.include_router(router.web, dependencies=[Depends(dependencies.logging)])
