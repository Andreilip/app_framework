from src.application.repo_interfaces import EmployeeRepoInterface
from src.application.use_case_interfaces import AddEmployeeUseCaseInterface, \
    AddEmployeeInputDTO, AddEmployeeResultDTO, UpdateEmployeeUseCaseInterface, UpdateEmployeeInputDTO, \
    UpdateEmployeeResultDTO, DeleteEmployeeUseCaseInterface, DeleteEmployeeInputDTO, \
    GetEmployeeByIdUseCaseInterface, GetEmployeeByIdInputDTO, GetEmployeeByIdResultDTO, GetAllEmployeesUseCaseInterface, \
    GetAllEmployeesResultDTO, FireEmployeeUseCaseInterface, FireEmployeeInputDTO, FireEmployeeResultDTO, \
    GetAllEmployeeResultItemDTO
from src.domain.models import Employee
from src.domain.services import create_new_employee

"""
В данном файле реализуются пользовательские сценарии

"""

class AddEmployeeUseCase(AddEmployeeUseCaseInterface):

    def __init__(self, employee_repo: EmployeeRepoInterface):
        self.employee_repo = employee_repo

    async def execute(self, params: AddEmployeeInputDTO)->AddEmployeeResultDTO:
        new_employee = create_new_employee(params.first_name,params.last_name)
        await self.employee_repo.add(new_employee)
        return AddEmployeeResultDTO(new_employee.employee_id)

class UpdateEmployeeUseCase(UpdateEmployeeUseCaseInterface):
    def __init__(self, employee_repo: EmployeeRepoInterface):
        self.employee_repo = employee_repo

    async def execute(self, params: UpdateEmployeeInputDTO) -> UpdateEmployeeResultDTO:
        got_employee = await self.employee_repo.get_by_id(params.employee_id)
        updated_employee = Employee(
            employee_id=params.employee_id,
            first_name=params.first_name,
            last_name=params.last_name,
            fired=got_employee.fired,
            fired_dt=got_employee.fired_dt
        )
        await self.employee_repo.update(updated_employee)
        return UpdateEmployeeResultDTO(employee_id=params.employee_id)

class DeleteEmployeeUseCase(DeleteEmployeeUseCaseInterface):
    def __init__(self, employee_repo: EmployeeRepoInterface):
        self.employee_repo = employee_repo

    async def execute(self, params: DeleteEmployeeInputDTO) -> None:
        await self.employee_repo.delete(params.employee_id)
        return

class GetEmployeeByIdUseCase(GetEmployeeByIdUseCaseInterface):
    def __init__(self, employee_repo: EmployeeRepoInterface):
        self.employee_repo = employee_repo

    async def execute(self, params: GetEmployeeByIdInputDTO) -> GetEmployeeByIdResultDTO:
        got_employee= await self.employee_repo.get_by_id(params.employee_id)
        return GetEmployeeByIdResultDTO(
            employee_id=got_employee.employee_id,
            first_name=got_employee.first_name,
            last_name=got_employee.last_name,
            fired=got_employee.fired,
            fired_dt=got_employee.fired_dt
        )

class GetAllEmployeesUseCase(GetAllEmployeesUseCaseInterface):
    def __init__(self, employee_repo: EmployeeRepoInterface):
        self.employee_repo = employee_repo

    async def execute(self) -> GetAllEmployeesResultDTO:
        employees = await self.employee_repo.get_all()
        employees_schema: list[GetAllEmployeeResultItemDTO] = [
            GetAllEmployeeResultItemDTO(
                employee_id=emp.employee_id,
                first_name=emp.first_name,
                last_name=emp.last_name,
                fired=emp.fired,
                fired_dt=emp.fired_dt
            ) for emp in employees
        ]
        return GetAllEmployeesResultDTO(employees=employees_schema)


class FireEmployeeUseCase(FireEmployeeUseCaseInterface):
    def __init__(self, employee_repo: EmployeeRepoInterface):
        self.employee_repo = employee_repo

    async def execute(self, params: FireEmployeeInputDTO) -> FireEmployeeResultDTO:
        # Получаем сотрудника из репозитория
        employee = await self.employee_repo.get_by_id(params.employee_id)

        # Используем метод fire из класса Employee
        employee.fire(params.fired_dt)

        # Обновляем сотрудника в репозитории
        await self.employee_repo.update(employee)

        return FireEmployeeResultDTO(
            employee_id=employee.employee_id,
            fired=employee.fired,
            fired_dt=employee.fired_dt
        )