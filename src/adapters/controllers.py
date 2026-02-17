from datetime import datetime
from uuid import UUID
from fastapi import APIRouter
from pydantic import BaseModel

from src.adapters.repos import SQLAlchemyPostgresEmployeeRepo
from src.application.use_case_interfaces import AddEmployeeInputDTO, UpdateEmployeeInputDTO, DeleteEmployeeInputDTO, \
    GetEmployeeByIdInputDTO, FireEmployeeInputDTO, GetAllEmployeeResultItemDTO, GetEmployeeByIdResultDTO, \
    GetAllEmployeesResultDTO, FireEmployeeResultDTO
from src.application.use_cases import AddEmployeeUseCase, UpdateEmployeeUseCase, GetEmployeeByIdUseCase, \
    DeleteEmployeeUseCase, GetAllEmployeesUseCase, FireEmployeeUseCase
from src.infrastructure.databases.postgres.read.engine import read_engine
from src.infrastructure.databases.postgres.write.engine import write_engine
from src.ui.api.fastapi.settings import fastapi_settings

"""
 В данном файле находится реализация всех эндпоинтов
"""

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


@router.get("/health_check", tags=["Служебные"],summary="Проверка работоспособности приложения")
def health_check():
    """
    Проверка работоспособности приложения
    """
    return {"status": "healthy", "timestamp": datetime.now()}


class AddEmployeeInputSchema(BaseModel,AddEmployeeInputDTO):
    pass
class AddEmployeeResultSchema(BaseModel):
    employee_id:UUID
@router.post("/add_employee",tags=["Сотрудники"])
async def add_employee (employee:AddEmployeeInputSchema)->AddEmployeeResultSchema:
    employee_repo = SQLAlchemyPostgresEmployeeRepo(write_engine)
    use_case=AddEmployeeUseCase(employee_repo)
    use_case_params=AddEmployeeInputDTO(**employee.model_dump())
    result=await use_case.execute(use_case_params)
    return AddEmployeeResultSchema.model_validate(result.__dict__)


class UpdateEmployeeInputSchema(BaseModel,UpdateEmployeeInputDTO):
    pass
class UpdateEmployeeResultSchema(BaseModel):
    employee_id:UUID
@router.put("/update_employee",tags=["Сотрудники"])
async def update_employee(upd_emp: UpdateEmployeeInputSchema):
    repo = SQLAlchemyPostgresEmployeeRepo(write_engine)
    use_case_params = UpdateEmployeeInputDTO(**upd_emp.model_dump())
    result = await UpdateEmployeeUseCase(repo).execute(use_case_params)
    return UpdateEmployeeResultSchema.model_validate(result.__dict__)


class DeleteEmployeeInputSchema(BaseModel,DeleteEmployeeInputDTO):
    pass
@router.put("/delete_employee",tags=["Сотрудники"])
async def delete_employee(del_emp: DeleteEmployeeInputSchema):
    repo = SQLAlchemyPostgresEmployeeRepo(write_engine)
    use_case_params = DeleteEmployeeInputDTO(**del_emp.model_dump())
    await DeleteEmployeeUseCase(repo).execute(use_case_params)
    return


class GetEmployeeByIdResultSchema(BaseModel,GetEmployeeByIdResultDTO):
    pass
@router.get("/get_employee/{employee_id}", tags=["Сотрудники"])
async def get_employee(employee_id: UUID):
    repo = SQLAlchemyPostgresEmployeeRepo(read_engine)
    use_case_params = GetEmployeeByIdInputDTO(employee_id=employee_id)
    result = await GetEmployeeByIdUseCase(repo).execute(use_case_params)
    return GetEmployeeByIdResultSchema.model_validate(result.__dict__)


class GetAllEmployeesResultItemSchema(BaseModel,GetAllEmployeeResultItemDTO):
    pass

class GetAllEmployeesResultSchema(BaseModel,GetAllEmployeesResultDTO):
    pass

@router.get("/get_all_employees", tags=["Сотрудники"])
async def get_all_employees():
    repo = SQLAlchemyPostgresEmployeeRepo(read_engine)
    result = await GetAllEmployeesUseCase(repo).execute()
    employees_schema = [
        GetAllEmployeesResultItemSchema.model_validate(emp.__dict__)
        for emp in result.employees
    ]
    get_all_employees_result={"employees": employees_schema}
    return  GetAllEmployeesResultSchema.model_validate(get_all_employees_result)


class FireEmployeeInputSchema(BaseModel,FireEmployeeInputDTO):
    pass

class FireEmployeeResultSchema(BaseModel,FireEmployeeResultDTO):
    pass

@router.put("/fire_employee", tags=["Сотрудники"])
async def fire_employee(fire_emp: FireEmployeeInputSchema):
    repo = SQLAlchemyPostgresEmployeeRepo(write_engine)
    use_case_params = FireEmployeeInputDTO(
        employee_id=fire_emp.employee_id,
        fired_dt=fire_emp.fired_dt
    )
    result = await FireEmployeeUseCase(repo).execute(use_case_params)
    return FireEmployeeResultSchema.model_validate(result.__dict__)