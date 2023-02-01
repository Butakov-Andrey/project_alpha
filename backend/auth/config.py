from datetime import timedelta

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    # db
    POSTGRES_USER: str = Field("pg user name", env="POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field("pg user password", env="POSTGRES_PASSWORD")
    POSTGRES_DB: str = Field("database name", env="POSTGRES_DB")
    POSTGRES_SERVER: str = Field("pg container name", env="POSTGRES_SERVER")

    # redis - для хранения черного списка токенов
    REDIS_HOST: str = Field("redis container name", env="REDIS_HOST")
    REDIS_PORT: str = Field("redis port", env="REDIS_PORT")

    # jwt
    authjwt_secret_key: str = Field("auth secret", env="AUTH_SECRET")
    authjwt_denylist_enabled: bool = True
    authjwt_denylist_token_checks: set = {"access", "refresh"}
    authjwt_token_location: set = {"cookies"}
    authjwt_cookie_secure: bool = False
    authjwt_cookie_csrf_protect: bool = True
    # время хранения токена в черном списке
    access_expires: int = timedelta(minutes=15).total_seconds()
    refresh_expires: int = timedelta(days=30).total_seconds()
    # время жизни токена
    authjwt_access_token_expires: int = timedelta(minutes=15).total_seconds()
    authjwt_refresh_token_expires: int = timedelta(days=30).total_seconds()
    # Change to 'lax' in production to make your website more secure from CSRF Attacks, default is None
    # authjwt_cookie_samesite: str = 'lax'

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()

origins = [
    "http://localhost",
    "http://localhost:8000",
]
