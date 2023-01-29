import postgres_db
from fastapi import Request
from loguru import logger


# database dependency
def get_db():
    db = postgres_db.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# logging dependency
def logging(request: Request):
    logger.debug("----------")
    logger.debug(f"{request.method} {request.url}")
    logger.debug("Params:")
    for name, value in request.path_params.items():
        logger.debug(f"\t{name}: {value}")
    logger.debug("Headers:")
    for name, value in request.headers.items():
        logger.debug(f"\t{name}: {value}")
