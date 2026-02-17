from pydantic_settings import BaseSettings, SettingsConfigDict

"""
Настройки подключения к БД через Pydantic.
Автоматически загружает переменные из .env файла.
Либо заполняет значениями по умолчанию
"""
class DatabasePostgresSettings(BaseSettings):
    DB_WRITE_NAME: str = "postgres"
    DB_WRITE_USERNAME: str = "postgres"
    DB_WRITE_PASSWORD: str = "1"
    DB_WRITE_HOST: str = "127.0.0.1"
    DB_WRITE_PORT: int = 5432

    model_config = SettingsConfigDict(env_file=".env",extra="allow")


database_postgres_settings = DatabasePostgresSettings()