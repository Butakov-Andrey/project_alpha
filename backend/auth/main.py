import config
import dependencies
import logger
from auth_app import router
from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi_jwt_auth.exceptions import AuthJWTException

logger.add_loggers()

app = FastAPI(
    title="Auth",
    version="0.0.1",
    contact={
        "name": "Andrey Butakov",
        "email": "6669.butakov@gmail.com",
    },
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url=None,
    # prefix распространяется на все роуты и документацию
    root_path="/auth",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=config.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


app.include_router(router.auth, dependencies=[Depends(dependencies.logging)])
