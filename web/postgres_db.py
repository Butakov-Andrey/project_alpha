from config import Settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

PG_USER = Settings().POSTGRES_USER
PG_PASSWORD = Settings().POSTGRES_PASSWORD
POSTGRES_HOST = Settings().POSTGRES_HOST
POSTGRES_DB = Settings().POSTGRES_DB

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{PG_USER}:{PG_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
