from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import origins
from .dependencies import logging_dependency
from .logging import add_loggers
from .test_app import router

add_loggers()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router.web, dependencies=[Depends(logging_dependency)])
