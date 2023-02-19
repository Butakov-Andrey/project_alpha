from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import User
from .schema import UserIn
from .utils import hash_password


def get_user_by_email(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()


def is_user_by_email_exist(db: Session, email: str) -> bool:
    subquery = select(User).filter(User.email == email).exists()
    return db.query(subquery).scalar() is True


def get_users(db: Session, skip: int = 0, limit: int = 10) -> list[User]:
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserIn) -> User:
    hashed_password = hash_password(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
