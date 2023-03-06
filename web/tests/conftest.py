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


# shared data
@pytest.fixture(scope="class")
def data():
    return {
        "content_type": "text/html",
        "home_title": "Home",
        "signup": "Sign Up",
        "login": "Log In",
        "logout": "Log Out",
        "email": "E-mail",
        "pass": "Password",
        "logout_mes": "Are you sure you want to log out?",
        "invalid_email_pass_mes": "Invalid email or password!",
        "invalid_tokens_mes": "Invalid tokens!",
        "no_tokens_mes": "No tokens detected!",
        "exist_email_mes": "Email exists!",
        "invalid_email_mes": "Invalid email!",
        "auth_user_email": "test@email.com",
        "auth_user_pass": "test12345",
        "auth_user_email_bad": "non_exist@email.com",
        "auth_user_pass_bad": "wrong_pass",
        "invalid_access_cookie": "invalid_access_token",
        "invalid_refresh_cookie": "invalid_refresh_token",
    }


# db
@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    yield engine


@pytest.fixture(scope="class")
def db(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    db = Session(bind=connection)

    yield db

    db.close()
    transaction.rollback()
    connection.close()


# clients
@pytest_asyncio.fixture(scope="class")
async def async_client(db):
    main.app.dependency_overrides[get_db] = lambda: db

    async with AsyncClient(app=main.app, base_url="http://test") as async_client:
        yield async_client


@pytest.fixture(scope="class")
def client(db):
    main.app.dependency_overrides[get_db] = lambda: db

    with TestClient(main.app) as client:
        yield client


@pytest.fixture(scope="class")
def auth_client(db, data):
    main.app.dependency_overrides[get_db] = lambda: db

    with TestClient(
        app=main.app,
        base_url="http://127.0.0.1:1337",
    ) as client:
        client.post(
            "/auth/signup/",
            data={
                "email": data.get("auth_user_email"),
                "password": data.get("auth_user_pass"),
            },
        )
        yield client
