from fastapi import APIRouter, Depends, HTTPException
from loguru import logger
from sqlalchemy.orm import Session

from ..dependencies import get_db
from . import crud
from .schema import User

web = APIRouter(
    prefix="/web",
    tags=["web"],
    responses={404: {"description": "Not found"}},
)


@web.get("/")
def foo():
    logger.info("That's it, beautiful and simple logging!")
    return {"users": 666}


@web.get("/sec")
@logger.catch
def foo_sec():
    a = 1 / 0
    return {"users": a}


@web.get("/thr")
def foo_thr():
    try:
        a = 1 / 0
    except ZeroDivisionError:
        logger.exception("What?!")
    return {"users": a}


@web.get("/users/", response_model=list[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@web.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@web.post("/users/", response_model=User)
def create_user(user: User, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)
