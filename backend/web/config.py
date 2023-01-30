from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    # db
    POSTGRES_USER: str = Field("user name", env="POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field("user password", env="POSTGRES_PASSWORD")
    POSTGRES_DB: str = Field("database name", env="POSTGRES_DB")
    POSTGRES_SERVER: str = Field("database server", env="POSTGRES_SERVER")

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

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()

origins = [
    "http://localhost",
    "http://localhost:8000",
]
