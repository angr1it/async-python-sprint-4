from pydantic import Extra, PostgresDsn
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    app_title: str
    database_dsn: PostgresDsn
    jwt_secret: str
    user_secret: str
    echo_db_engine: bool

    class Config:
        env_file: str = ".env"
        extra = Extra.allow


app_settings = AppSettings()
