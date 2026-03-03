from dependency_injector import containers, providers
from dependency_injector.providers import Factory, Singleton

from src.infrastructure.databases.postgres.read.engine import read_engine
from src.infrastructure.databases.postgres.write.engine import write_engine
from src.adapters.repos import SQLAlchemyPostgresEmployeeRepo
from src.application.use_cases import (
    AddEmployeeUseCase,
    UpdateEmployeeUseCase,
    DeleteEmployeeUseCase,
    GetEmployeeByIdUseCase,
    GetAllEmployeesUseCase,
    FireEmployeeUseCase
)



class Container(containers.DeclarativeContainer):
    """Главный контейнер зависимостей приложения"""
    
    # Конфигурация
    config = providers.Configuration()
    
    # === Infrastrucure Layer ===
    # Движки баз данных (синглтоны)
    write_engine_provider = providers.Singleton(
        lambda: write_engine
    )
    
    read_engine_provider = providers.Singleton(
        lambda: read_engine
    )
    
    # === Adapters Layer ===
    # Репозитории (фабрики)
    employee_write_repo = Factory(
        SQLAlchemyPostgresEmployeeRepo,
        engine=write_engine_provider
    )
    
    employee_read_repo = Factory(
        SQLAlchemyPostgresEmployeeRepo,
        engine=read_engine_provider
    )
    
    # === Application Layer ===
    # Use Cases для записи (используют write репозиторий)
    add_employee_use_case = Factory(
        AddEmployeeUseCase,
        employee_repo=employee_write_repo
    )
    
    update_employee_use_case = Factory(
        UpdateEmployeeUseCase,
        employee_repo=employee_write_repo
    )
    
    delete_employee_use_case = Factory(
        DeleteEmployeeUseCase,
        employee_repo=employee_write_repo
    )
    
    fire_employee_use_case = Factory(
        FireEmployeeUseCase,
        employee_repo=employee_write_repo
    )
    
    # Use Cases для чтения (используют read репозиторий)
    get_employee_by_id_use_case = Factory(
        GetEmployeeByIdUseCase,
        employee_repo=employee_read_repo
    )
    
    get_all_employees_use_case = Factory(
        GetAllEmployeesUseCase,
        employee_repo=employee_read_repo
    )