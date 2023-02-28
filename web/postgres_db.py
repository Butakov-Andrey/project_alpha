from config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

PG_USER = settings.POSTGRES_USER
PG_PASSWORD = settings.POSTGRES_PASSWORD
POSTGRES_HOST = settings.POSTGRES_HOST
POSTGRES_DB = settings.POSTGRES_DB

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{PG_USER}:{PG_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
