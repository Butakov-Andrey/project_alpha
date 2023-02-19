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
    # время жизни токена
    # authjwt_access_token_expires: int = timedelta(minutes=15).total_seconds()
    # authjwt_refresh_token_expires: int = timedelta(days=30).total_seconds()
    authjwt_access_token_expires: int = timedelta(minutes=1).total_seconds()
    authjwt_refresh_token_expires: int = timedelta(minutes=2).total_seconds()
    # Change to 'lax' in production to make your website more secure from CSRF Attacks, default is None
    # authjwt_cookie_samesite: str = 'lax'

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


server = "http://127.0.0.1:1337"
static = f"{server}/static"


origins = [
    "http://localhost:1337",
    "http://127.0.0.1:1337",
]
