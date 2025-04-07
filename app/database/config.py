import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_URL: str

    @property
    def DATABASE_URL_aiosqlite(self):
        return f"{self.DB_URL}"

    # Указываем путь к .env в родительской директории
    model_config = SettingsConfigDict(env_file=os.path.join(os.path.dirname(__file__), '..', '..', '.env'), extra="allow")


settings = Settings()
