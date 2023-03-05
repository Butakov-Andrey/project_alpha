import uuid

import postgres_db
from sqlalchemy import Column, String

Base = postgres_db.Base


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True, default=str(uuid.uuid4()))
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
