from fastapi import FastAPI
from src.adapters.controllers import router
from src.ui.api.fastapi.settings import fastapi_settings

"""
В данном файле инициализируется и настраивается приложение FastAPI
"""

app = FastAPI(
    title=fastapi_settings.APP_TITLE,          # Название API (отображается в документации)
    description=fastapi_settings.APP_DESCRIPTION,  # Описание
    docs_url=fastapi_settings.APP_DOCS_URL,  # URL для Swagger документации
    version=fastapi_settings.API_VERSION   # Версия API
)

app.include_router(router)
