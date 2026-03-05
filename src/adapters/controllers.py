from datetime import datetime
from uuid import UUID
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field
from dependency_injector.wiring import inject, Provide

from src.adapters.dependency_injector import Container
from src.application.use_case_interfaces import (
    AddEmployeeInputDTO, UpdateEmployeeInputDTO, DeleteEmployeeInputDTO,
    GetEmployeeByIdInputDTO, FireEmployeeInputDTO
)
from src.application.use_cases import (
    AddEmployeeUseCase, UpdateEmployeeUseCase, GetEmployeeByIdUseCase,
    DeleteEmployeeUseCase, GetAllEmployeesUseCase, FireEmployeeUseCase
)

import logging

router = APIRouter()
logger = logging.getLogger(__name__)



@router.get("/", tags=["Служебные"])
def info():
    """Корневой эндпоинт приложения."""
    return {
        "message": "Добро пожаловать в FastAPI приложение!",
        "docs": "/docs",
        "version": "1.0.0"
    }


@router.get("/health_check", tags=["Служебные"])
def health_check():
    """Проверка работоспособности приложения"""
    return {"status": "healthy", "timestamp": datetime.now()}


# Схемы Pydantic с валидацией
class AddEmployeeInputSchema(BaseModel):
    last_name: str = Field(..., min_length=1, max_length=100, description="Фамилия сотрудника")
    first_name: str = Field(..., min_length=1, max_length=100, description="Имя сотрудника")

    model_config = {
        "json_schema_extra": {
            "example": {
                "last_name": "Иванов",
                "first_name": "Иван"
            }
        }
    }


class AddEmployeeResultSchema(BaseModel):
    employee_id: UUID


@router.post("/add_employee",
             tags=["Сотрудники"],
             response_model=AddEmployeeResultSchema,
             status_code=status.HTTP_201_CREATED)
@inject
async def add_employee(
    employee: AddEmployeeInputSchema,
    use_case: AddEmployeeUseCase = Depends(Provide[Container.add_employee_use_case])
) -> AddEmployeeResultSchema:
    """Добавление нового сотрудника"""
    use_case_params = AddEmployeeInputDTO(
        last_name=employee.last_name,
        first_name=employee.first_name
    )
    result = await use_case.execute(use_case_params)
    return AddEmployeeResultSchema(employee_id=result.employee_id)


class UpdateEmployeeInputSchema(BaseModel):
    employee_id: UUID = Field(..., description="ID сотрудника")
    last_name: str = Field(..., min_length=1, max_length=100, description="Фамилия сотрудника")
    first_name: str = Field(..., min_length=1, max_length=100, description="Имя сотрудника")

    model_config = {
        "json_schema_extra": {
            "example": {
                "employee_id": "123e4567-e89b-12d3-a456-426614174000",
                "last_name": "Петров",
                "first_name": "Петр"
            }
        }
    }


class UpdateEmployeeResultSchema(BaseModel):
    employee_id: UUID


@router.put("/update_employee",
            tags=["Сотрудники"],
            response_model=UpdateEmployeeResultSchema)
@inject
async def update_employee(
    upd_emp: UpdateEmployeeInputSchema,
    use_case: UpdateEmployeeUseCase = Depends(Provide[Container.update_employee_use_case])
) -> UpdateEmployeeResultSchema:
    """Обновление данных сотрудника"""
    use_case_params = UpdateEmployeeInputDTO(
        employee_id=upd_emp.employee_id,
        last_name=upd_emp.last_name,
        first_name=upd_emp.first_name
    )
    result = await use_case.execute(use_case_params)
    return UpdateEmployeeResultSchema(employee_id=result.employee_id)


class DeleteEmployeeInputSchema(BaseModel):
    employee_id: UUID = Field(..., description="ID сотрудника")

    model_config = {
        "json_schema_extra": {
            "example": {
                "employee_id": "123e4567-e89b-12d3-a456-426614174000"
            }
        }
    }


class DeleteEmployeeResultSchema(BaseModel):
    message: str
    employee_id: UUID


@router.delete("/delete_employee",
               tags=["Сотрудники"],
               response_model=DeleteEmployeeResultSchema)
@inject
async def delete_employee(
    del_emp: DeleteEmployeeInputSchema,
    use_case: DeleteEmployeeUseCase = Depends(Provide[Container.delete_employee_use_case])
):
    """Удаление сотрудника"""
    use_case_params = DeleteEmployeeInputDTO(employee_id=del_emp.employee_id)
    await use_case.execute(use_case_params)
    return DeleteEmployeeResultSchema(
        message="Сотрудник успешно удален",
        employee_id=del_emp.employee_id
    )


class GetEmployeeByIdResultSchema(BaseModel):
    employee_id: UUID
    first_name: str
    last_name: str
    fired: bool
    fired_dt: datetime | None


@router.get("/get_employee/{employee_id}",
            tags=["Сотрудники"],
            response_model=GetEmployeeByIdResultSchema)
@inject
async def get_employee(
    employee_id: UUID,
    use_case: GetEmployeeByIdUseCase = Depends(Provide[Container.get_employee_by_id_use_case])
) -> GetEmployeeByIdResultSchema:
    """Получение сотрудника по ID"""
    use_case_params = GetEmployeeByIdInputDTO(employee_id=employee_id)
    result = await use_case.execute(use_case_params)
    return GetEmployeeByIdResultSchema(
        employee_id=result.employee_id,
        first_name=result.first_name,
        last_name=result.last_name,
        fired=result.fired,
        fired_dt=result.fired_dt
    )


class GetAllEmployeesResultItemSchema(BaseModel):
    employee_id: UUID
    first_name: str
    last_name: str
    fired: bool
    fired_dt: datetime | None


class GetAllEmployeesResultSchema(BaseModel):
    employees: list[GetAllEmployeesResultItemSchema]
    count: int


@router.get("/get_all_employees",
            tags=["Сотрудники"],
            response_model=GetAllEmployeesResultSchema)
@inject
async def get_all_employees(
    use_case: GetAllEmployeesUseCase = Depends(Provide[Container.get_all_employees_use_case])
) -> GetAllEmployeesResultSchema:
    """Получение всех сотрудников"""
    result = await use_case.execute()
    employees_schema = [
        GetAllEmployeesResultItemSchema(
            employee_id=emp.employee_id,
            first_name=emp.first_name,
            last_name=emp.last_name,
            fired=emp.fired,
            fired_dt=emp.fired_dt
        )
        for emp in result.employees
    ]
    return GetAllEmployeesResultSchema(
        employees=employees_schema,
        count=len(employees_schema)
    )


class FireEmployeeInputSchema(BaseModel):
    employee_id: UUID = Field(..., description="ID сотрудника")
    fired_dt: datetime | None = Field(None, description="Дата увольнения (если не указана - текущая)")

    model_config = {
        "json_schema_extra": {
            "example": {
                "employee_id": "123e4567-e89b-12d3-a456-426614174000",
                "fired_dt": "2024-01-15T10:30:00"
            }
        }
    }


class FireEmployeeResultSchema(BaseModel):
    employee_id: UUID
    fired: bool
    fired_dt: datetime | None
    message: str


@router.put("/fire_employee",
            tags=["Сотрудники"],
            response_model=FireEmployeeResultSchema)
@inject
async def fire_employee(
    fire_emp: FireEmployeeInputSchema,
    use_case: FireEmployeeUseCase = Depends(Provide[Container.fire_employee_use_case])
) -> FireEmployeeResultSchema:
    """Увольнение сотрудника"""
    use_case_params = FireEmployeeInputDTO(
        employee_id=fire_emp.employee_id,
        fired_dt=fire_emp.fired_dt
    )
    result = await use_case.execute(use_case_params)
    return FireEmployeeResultSchema(
        employee_id=result.employee_id,
        fired=result.fired,
        fired_dt=result.fired_dt,
        message=result.message
    )