from fastapi import FastAPI
from src.adapters.dependency_injector import Container
from src.adapters.controllers import router
from src.ui.api.fastapi.settings import fastapi_settings

"""
В данном файле инициализируется и настраивается приложение FastAPI
"""
def setup_di(app: FastAPI) -> None:
    """
    Настройка dependency injection для FastAPI приложения
    """
    # Создаем контейнер
    container = Container()
    
    # Сохраняем контейнер в состоянии приложения
    app.state.container = container
    
    # Wiring для всех модулей, где используются зависимости
    container.wire(modules=[
        "src.adapters.controllers",  # ваш файл с контроллерами
    ])
def create_app() -> FastAPI:
    """
    Фабрика создания FastAPI приложения
    """
    app = FastAPI(
        title=fastapi_settings.APP_TITLE,          # Название API (отображается в документации)
        description=fastapi_settings.APP_DESCRIPTION,  # Описание
        docs_url=fastapi_settings.APP_DOCS_URL,  # URL для Swagger документации
        version=fastapi_settings.API_VERSION   # Версия API
        )
    
    # Настройка Dependency Injection
    setup_di(app)
    
    # Подключение роутеров
    app.include_router(router)
    
    return app

app = create_app()




