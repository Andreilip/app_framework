from datetime import datetime
from uuid import UUID
from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from dependency_injector.wiring import inject, Provide
from src.ui.api.fastapi.settings import fastapi_settings
from src.adapters.dependency_injector import Container
from src.application.use_case_interfaces import (
    AddEmployeeInputDTO, UpdateEmployeeInputDTO, DeleteEmployeeInputDTO,
    GetEmployeeByIdInputDTO, FireEmployeeInputDTO, GetAllEmployeeResultItemDTO,
    GetEmployeeByIdResultDTO, GetAllEmployeesResultDTO, FireEmployeeResultDTO
)
from src.application.use_cases import (
    AddEmployeeUseCase, UpdateEmployeeUseCase, GetEmployeeByIdUseCase,
    DeleteEmployeeUseCase, GetAllEmployeesUseCase, FireEmployeeUseCase
)

router = APIRouter()


@router.get("/", tags=["Служебные"])
def info():
    """
    Корневой эндпоинт приложения.
    Возвращает информацию о приложении.
    """
    return {
        "message": "Добро пожаловать в FastAPI приложение!",
        "docs": fastapi_settings.APP_DOCS_URL,
        "version": fastapi_settings.API_VERSION
    }


@router.get("/health_check", tags=["Служебные"])
def health_check():
    """Проверка работоспособности приложения"""
    return {"status": "healthy", "timestamp": datetime.now()}


# Схемы Pydantic
class AddEmployeeInputSchema(BaseModel, AddEmployeeInputDTO):
    pass


class AddEmployeeResultSchema(BaseModel):
    employee_id: UUID


@router.post("/add_employee", tags=["Сотрудники"])
@inject
async def add_employee(
    employee: AddEmployeeInputSchema,
    use_case: AddEmployeeUseCase = Depends(Provide[Container.add_employee_use_case])
) -> AddEmployeeResultSchema:
    """Добавление нового сотрудника"""
    use_case_params = AddEmployeeInputDTO(**employee.model_dump())
    result = await use_case.execute(use_case_params)
    return AddEmployeeResultSchema.model_validate(result.__dict__)


class UpdateEmployeeInputSchema(BaseModel, UpdateEmployeeInputDTO):
    pass


class UpdateEmployeeResultSchema(BaseModel):
    employee_id: UUID


@router.put("/update_employee", tags=["Сотрудники"])
@inject
async def update_employee(
    upd_emp: UpdateEmployeeInputSchema,
    use_case: UpdateEmployeeUseCase = Depends(Provide[Container.update_employee_use_case])
) -> UpdateEmployeeResultSchema:
    """Обновление данных сотрудника"""
    use_case_params = UpdateEmployeeInputDTO(**upd_emp.model_dump())
    result = await use_case.execute(use_case_params)
    return UpdateEmployeeResultSchema.model_validate(result.__dict__)


class DeleteEmployeeInputSchema(BaseModel, DeleteEmployeeInputDTO):
    pass


@router.put("/delete_employee", tags=["Сотрудники"])
@inject
async def delete_employee(
    del_emp: DeleteEmployeeInputSchema,
    use_case: DeleteEmployeeUseCase = Depends(Provide[Container.delete_employee_use_case])
):
    """Удаление сотрудника"""
    use_case_params = DeleteEmployeeInputDTO(**del_emp.model_dump())
    await use_case.execute(use_case_params)
    return {"message": "Сотрудник успешно удален"}


class GetEmployeeByIdResultSchema(BaseModel, GetEmployeeByIdResultDTO):
    pass


@router.get("/get_employee/{employee_id}", tags=["Сотрудники"])
@inject
async def get_employee(
    employee_id: UUID,
    use_case: GetEmployeeByIdUseCase = Depends(Provide[Container.get_employee_by_id_use_case])
) -> GetEmployeeByIdResultSchema:
    """Получение сотрудника по ID"""
    use_case_params = GetEmployeeByIdInputDTO(employee_id=employee_id)
    result = await use_case.execute(use_case_params)
    return GetEmployeeByIdResultSchema.model_validate(result.__dict__)


class GetAllEmployeesResultItemSchema(BaseModel, GetAllEmployeeResultItemDTO):
    pass


class GetAllEmployeesResultSchema(BaseModel, GetAllEmployeesResultDTO):
    pass


@router.get("/get_all_employees", tags=["Сотрудники"])
@inject
async def get_all_employees(
    use_case: GetAllEmployeesUseCase = Depends(Provide[Container.get_all_employees_use_case])
) -> GetAllEmployeesResultSchema:
    """Получение всех сотрудников"""
    result = await use_case.execute()
    employees_schema = [
        GetAllEmployeesResultItemSchema.model_validate(emp.__dict__)
        for emp in result.employees
    ]
    return GetAllEmployeesResultSchema(employees=employees_schema)


class FireEmployeeInputSchema(BaseModel, FireEmployeeInputDTO):
    pass


class FireEmployeeResultSchema(BaseModel, FireEmployeeResultDTO):
    pass

@router.put("/fire_employee", tags=["Сотрудники"])
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
    return FireEmployeeResultSchema.model_validate(result.__dict__)