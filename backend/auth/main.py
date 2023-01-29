import config
import dependencies
import logger
from auth_app import router
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

logger.add_loggers()

app = FastAPI(
    title="Auth",
    version="0.0.1",
    contact={
        "name": "Andrey Butakov",
        "email": "6669.butakov@gmail.com",
    },
    openapi_url="/openapi.json",
    docs_url="/swagger",
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

app.include_router(router.auth, dependencies=[Depends(dependencies.logging)])
