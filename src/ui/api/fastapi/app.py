from fastapi import FastAPI
from pydantic import ValidationError

from src.adapters.dependency_injector import Container
from src.adapters.controllers import router
from src.adapters.error_handlers import (
    application_error_handler,
    validation_error_handler,
    general_error_handler
)
from src.application.errors import ApplicationError
from src.ui.api.fastapi.settings import fastapi_settings

import logging

logger = logging.getLogger(__name__)


def setup_di(app: FastAPI) -> None:
    """Настройка dependency injection для FastAPI приложения"""
    container = Container()
    app.state.container = container
    container.wire(modules=[
        "src.adapters.controllers",
    ])
    logger.debug("Dependency injection configured")


def setup_exception_handlers(app: FastAPI) -> None:
    """Настройка обработчиков исключений"""
    app.add_exception_handler(ApplicationError, application_error_handler)
    app.add_exception_handler(ValidationError, validation_error_handler)
    app.add_exception_handler(Exception, general_error_handler)
    logger.debug("Exception handlers configured")


def create_app() -> FastAPI:
    """Фабрика создания FastAPI приложения"""
    app = FastAPI(
        title=fastapi_settings.APP_TITLE,
        description=fastapi_settings.APP_DESCRIPTION,
        docs_url=fastapi_settings.APP_DOCS_URL,
        version=fastapi_settings.API_VERSION
    )
    
    # Настройка Dependency Injection
    setup_di(app)
    
    # Настройка обработчиков ошибок
    setup_exception_handlers(app)
    
    # Подключение роутеров
    app.include_router(router)
    
    logger.info("FastAPI application created successfully")
    return app


app = create_app()