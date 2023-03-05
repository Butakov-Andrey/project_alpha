from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import User
from .utils import auth


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def is_user_by_email_exist(db: Session, email: str) -> bool:
    subquery = select(User).filter(User.email == email).exists()
    return db.query(subquery).scalar()


def create_user(db: Session, email: str, password: str) -> None:
    hashed_password = auth.hash_password(password)
    db_user = User(email=email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
