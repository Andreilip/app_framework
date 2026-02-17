from pydantic_settings import BaseSettings, SettingsConfigDict

"""
Настройки приложения через Pydantic.
Автоматически загружает переменные из .env файла.
Либо заполняет значениями по умолчанию
"""

class FastapiSettings(BaseSettings):
    APP_ROOT_PATH: str = ""
    APP_RELOAD: bool = False
    APP_HOST: str = "localhost"
    APP_PORT: int = 8000
    APP_INIT_LOGGING: bool = False
    VIEW_API_VERSION: bool = True
    API_VERSION: str = "1.0.0"
    APP_DOCS_URL: str = "/docs"
    APP_DESCRIPTION: str = "Тестовое приложение на Питон"
    APP_TITLE: str = "Hello World API"

    model_config = SettingsConfigDict(env_file=".env", extra="allow")


fastapi_settings = FastapiSettings()
