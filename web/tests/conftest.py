import main
import pytest
import pytest_asyncio
from dependencies import get_db
from fastapi.testclient import TestClient
from httpx import AsyncClient
from postgres_db import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

SQLALCHEMY_DATABASE_URL = "sqlite:///./tests/test.db"


@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    yield engine


@pytest.fixture(scope="function")
def db(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    db = Session(bind=connection)

    yield db

    db.close()
    transaction.rollback()
    connection.close()


@pytest_asyncio.fixture(scope="function")
async def async_client(db):
    main.app.dependency_overrides[get_db] = lambda: db

    async with AsyncClient(app=main.app, base_url="http://test") as async_client:
        yield async_client


@pytest.fixture(scope="function")
def client(db):
    main.app.dependency_overrides[get_db] = lambda: db

    with TestClient(main.app) as client:
        yield client
