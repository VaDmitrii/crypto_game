from logging import DEBUG

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    LOG_LEVEL: str = DEBUG
    CORS_ORIGINS: list[str]

    PRODUCTION_BOT_TOKEN: str
    ADMIN_BOT_TOKEN: str

    MYSQL_USER: str = 'mysql_user'
    MYSQL_PASSWORD: str = 'mysql_password'
    MYSQL_ROOT_PASSWORD: str = 'root_password'
    MYSQL_HOST: str = 'db'
    MYSQL_PORT: int = 3306
    MYSQL_DB: str = 'mysql_db'

    class Config:
        env_file = '.env'
        env_file_encoding = "utf-8"

    @property
    def database_url(self) -> str:
        user = self.MYSQL_USER
        password = self.MYSQL_PASSWORD
        host = self.MYSQL_HOST
        port = self.MYSQL_PORT
        db = self.MYSQL_DB
        return f"mysql+asyncmy://{user}:{password}@{host}:{port}/{db}"


settings = Settings()
