from dependencies import get_db
from fastapi import APIRouter, Depends, HTTPException
from loguru import logger
from sqlalchemy.orm import Session

from .crud import create_user, get_user, get_user_by_email, get_users
from .schema import User

auth = APIRouter(
    # prefix распространяется на этот роут
    prefix="/api/v1",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


@auth.get("/")
def foo():
    logger.info("That's it, beautiful and simple logging!")
    return {"auth": 9999999999}
