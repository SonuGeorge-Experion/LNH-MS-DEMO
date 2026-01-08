from urllib.parse import quote_plus

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    APP_NAME: str = "MS Sample App"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    SECRET_KEY: str = "your_secret_key"  # ideally from .env
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    db_user: str
    db_pass: str
    db_host: str
    db_port: int
    db_name: str
    db_driver: str = "psycopg2"
    async_driver: str = "asyncpg"

    model_config = ConfigDict(env_file=".env")

    @property
    def alembic_db(self) -> str:
        quote_ref = quote_plus(self.db_pass).replace("%", "%%")
        return f"postgresql+{self.db_driver}://{self.db_user}:{quote_ref}@{self.db_host}:{self.db_port}/{self.db_name}"

    @property
    def sync_db_url(self) -> str:
        return f"postgresql+{self.db_driver}://{self.db_user}:{quote_plus(self.db_pass)}@{self.db_host}:{self.db_port}/{self.db_name}"

    @property
    def async_db_url(self) -> str:
        return f"postgresql+{self.async_driver}://{self.db_user}:{quote_plus(self.db_pass)}@{self.db_host}:{self.db_port}/{self.db_name}"


settings = Settings()
