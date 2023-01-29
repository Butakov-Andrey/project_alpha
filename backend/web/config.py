from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    # db
    POSTGRES_USER: str = Field("user name", env="POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field("user password", env="POSTGRES_PASSWORD")
    POSTGRES_DB: str = Field("database name", env="POSTGRES_DB")
    POSTGRES_SERVER: str = Field("database server", env="POSTGRES_SERVER")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()

origins = [
    "http://localhost",
    "http://localhost:8000",
]
