from fastapi import Request
from loguru import logger
from postgres_db import SessionLocal


# database dependency
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# logger dependency
def logging(request: Request):
    logger.debug("----------")
    logger.debug(f"{request.method} {request.url}")
    logger.debug("Params:")
    for name, value in request.path_params.items():
        logger.debug(f"\t{name}: {value}")
    logger.debug("Headers:")
    for name, value in request.headers.items():
        logger.debug(f"\t{name}: {value}")
