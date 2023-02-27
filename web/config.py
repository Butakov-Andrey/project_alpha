from datetime import timedelta

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    # db
    POSTGRES_USER: str = Field("pg user name", env="POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field("pg user password", env="POSTGRES_PASSWORD")
    POSTGRES_DB: str = Field("database name", env="POSTGRES_DB")
    POSTGRES_HOST: str = Field("pg container name", env="POSTGRES_HOST")

    # redis - для хранения черного списка токенов
    REDIS_HOST: str = Field("redis container name", env="REDIS_HOST")
    REDIS_PORT: str = Field("redis port", env="REDIS_PORT")

    # jwt
    authjwt_secret_key: str = Field("auth secret", env="AUTH_SECRET")
    authjwt_denylist_enabled: bool = False
    authjwt_denylist_token_checks: set = {"access", "refresh"}
    authjwt_token_location: set = {"cookies"}
    authjwt_cookie_secure: bool = False
    authjwt_cookie_csrf_protect: bool = True
    # cookies
    CSRF_REFRESH_TOKEN: str = "csrf_refresh_token"
    # время жизни токена
    # authjwt_access_token_expires: float = timedelta(minutes=15).total_seconds()
    # authjwt_refresh_token_expires: float = timedelta(days=30).total_seconds()
    authjwt_access_token_expires: float = timedelta(minutes=1).total_seconds()
    authjwt_refresh_token_expires: float = timedelta(minutes=2).total_seconds()

    # fields
    ROLE_FIELD: str = "role"
    USER_FIELD: str = "user"
    REQUEST_FIELD: str = "request"
    ERROR_FIELD: str = "error"
    STATUS_CODE_FIELD: str = "status_code"

    # deploy
    SERVER_URL: str = "http://127.0.0.1:1337"
    STATIC_URL: str = f"{SERVER_URL}/static"
    ORIGINS: list[str] = [SERVER_URL]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()


class STATUS_CODE:
    HTTP_200_OK = 200
    HTTP_303_SEE_OTHER = 303
    HTTP_404_NOT_FOUND = 404


class RESPONSE_MESSAGE:
    VALID_TOKEN = "Token is valid. Successfully login."
    INVALID_TOKEN = "Token is invalid."
    INCORRECT_CREDENTIALS = "Incorrect email or password."
