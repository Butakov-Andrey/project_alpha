import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    # postgres
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str

    # redis
    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_DB: int

    # jwt
    ALGORITHM: str = "HS256"
    JWT_SECRET_KEY: str
    JWT_REFRESH_SECRET_KEY: str
    # время жизни jwt токенов
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    # время жизни cookie с jwt токенами
    COOKIE_EXPIRE_SECONDS: int = REFRESH_TOKEN_EXPIRE_MINUTES * 60
    # timeout websockets подключения при бездействии
    WS_CONNECTION_TIMEOUT_SECONDS: int = ACCESS_TOKEN_EXPIRE_MINUTES * 60

    # deploy
    SERVER_URL: str = "http://127.0.0.1:1337"
    STATIC_URL: str = f"{SERVER_URL}/static"
    ORIGINS: list[str] = [SERVER_URL]

    class Config:
        env_file = os.getenv("ENV_FILE")
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()


class RESPONSE_MESSAGE:
    INVALID_CREDENTIALS: str = "Invalid email or password!"
    INVALID_EMAIL: str = "Invalid email!"
    EMAIL_EXIST: str = "Email exists!"

    NO_TOKENS: str = "No tokens detected!"
    INVALID_TOKENS: str = "Invalid tokens!"


class TEMPLATE_FIELDS:
    USER: str = "user"
    REQUEST: str = "request"
    ERROR: str = "error"
    MESSAGE: str = "message"
    STATUS_CODE: str = "status_code"


class COOKIE:
    ACCESS: str = "access_token"
    REFRESH: str = "refresh_token"
