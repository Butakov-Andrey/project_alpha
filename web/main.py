import config
import dependencies
import logger
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from test_app import router

logger.add_loggers()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router.web, dependencies=[Depends(dependencies.logging)])
