from src.application.repo_interfaces import EmployeeRepoInterface
from src.application.use_case_interfaces import (
    AddEmployeeUseCaseInterface, AddEmployeeInputDTO, AddEmployeeResultDTO,
    UpdateEmployeeUseCaseInterface, UpdateEmployeeInputDTO, UpdateEmployeeResultDTO,
    DeleteEmployeeUseCaseInterface, DeleteEmployeeInputDTO,
    GetEmployeeByIdUseCaseInterface, GetEmployeeByIdInputDTO, GetEmployeeByIdResultDTO,
    GetAllEmployeesUseCaseInterface, GetAllEmployeesResultDTO,
    FireEmployeeUseCaseInterface, FireEmployeeInputDTO, FireEmployeeResultDTO,
    GetAllEmployeeResultItemDTO
)
from src.application.errors import (
    EmployeeNotFoundError,
    EmployeeAlreadyFiredError,
    InvalidEmployeeDataError,
    RepoOperationError
)
from src.domain.models import Employee
from src.domain.services import create_new_employee
from src.domain.errors import DomainError

import logging

"""
В данном файле реализуются пользовательские сценарии с обработкой ошибок
"""

logger = logging.getLogger(__name__)


class AddEmployeeUseCase(AddEmployeeUseCaseInterface):

    def __init__(self, employee_repo: EmployeeRepoInterface):
        self.employee_repo = employee_repo

    async def execute(self, params: AddEmployeeInputDTO) -> AddEmployeeResultDTO:
        try:
            # Валидация входных данных
            if not params.first_name or not params.first_name.strip():
                raise InvalidEmployeeDataError("first_name", "Имя не может быть пустым")
            if not params.last_name or not params.last_name.strip():
                raise InvalidEmployeeDataError("last_name", "Фамилия не может быть пустой") #TODO - здесь можно valueerror
 
            # Создание нового сотрудника
            try:
                new_employee = create_new_employee(
                    last_name=params.last_name.strip(),
                    first_name=params.first_name.strip()
                )
            except DomainError as e:
                raise InvalidEmployeeDataError("employee", str(e))

            # Сохранение в репозиторий
            try:
                await self.employee_repo.add(new_employee)
            except Exception as e:
                logger.error(f"Ошибка БД при добавлении сотрудника: {e}")
                raise RepoOperationError("add", str(e))

            return AddEmployeeResultDTO(new_employee.employee_id)

        except (EmployeeNotFoundError, EmployeeAlreadyFiredError,
                InvalidEmployeeDataError, RepoOperationError):
            # Пробрасываем известные ошибки дальше
            raise
        except Exception as e:
            # Неожиданная ошибка
            logger.error(f"Неожиданная ошибка в AddEmployeeUseCase: {e}")
            raise RepoOperationError("add_employee", "Внутренняя ошибка сервера")


class UpdateEmployeeUseCase(UpdateEmployeeUseCaseInterface):
    def __init__(self, employee_repo: EmployeeRepoInterface):
        self.employee_repo = employee_repo

    async def execute(self, params: UpdateEmployeeInputDTO) -> UpdateEmployeeResultDTO:
        try:
            # Валидация
            if not params.first_name or not params.first_name.strip():
                raise InvalidEmployeeDataError("first_name", "Имя не может быть пустым")
            if not params.last_name or not params.last_name.strip():
                raise InvalidEmployeeDataError("last_name", "Фамилия не может быть пустой")

            # Получаем сотрудника
            try:
                got_employee = await self.employee_repo.get_by_id(params.employee_id)
            except Exception as e:
                logger.error(f"Ошибка БД при получении сотрудника {params.employee_id}: {e}")
                raise RepoOperationError("get_by_id", str(e))

            if got_employee is None:
                raise EmployeeNotFoundError(params.employee_id)

            # Создаем обновленного сотрудника
            updated_employee = Employee(
                employee_id=params.employee_id,
                first_name=params.first_name.strip(),
                last_name=params.last_name.strip(),
                fired=got_employee.fired,
                fired_dt=got_employee.fired_dt
            )

            # Обновляем
            try:
                await self.employee_repo.update(updated_employee)
            except Exception as e:
                logger.error(f"Ошибка БД при обновлении сотрудника {params.employee_id}: {e}")
                raise RepoOperationError("update", str(e))

            return UpdateEmployeeResultDTO(employee_id=params.employee_id)

        except (EmployeeNotFoundError, InvalidEmployeeDataError, RepoOperationError):
            raise
        except Exception as e:
            logger.error(f"Неожиданная ошибка в UpdateEmployeeUseCase: {e}")
            raise RepoOperationError("update_employee", "Внутренняя ошибка сервера")


class DeleteEmployeeUseCase(DeleteEmployeeUseCaseInterface):
    def __init__(self, employee_repo: EmployeeRepoInterface):
        self.employee_repo = employee_repo

    async def execute(self, params: DeleteEmployeeInputDTO) -> None:
        try:
            # Проверяем существование сотрудника
            try:
                employee = await self.employee_repo.get_by_id(params.employee_id)
            except Exception as e:
                logger.error(f"Ошибка БД при получении сотрудника {params.employee_id}: {e}")
                raise RepoOperationError("get_by_id", str(e))

            if employee is None:
                raise EmployeeNotFoundError(params.employee_id)

            # Удаляем
            try:
                await self.employee_repo.delete(params.employee_id)
            except Exception as e:
                logger.error(f"Ошибка БД при удалении сотрудника {params.employee_id}: {e}")
                raise RepoOperationError("delete", str(e))

        except (EmployeeNotFoundError, RepoOperationError):
            raise
        except Exception as e:
            logger.error(f"Неожиданная ошибка в DeleteEmployeeUseCase: {e}")
            raise RepoOperationError("delete_employee", "Внутренняя ошибка сервера")


class GetEmployeeByIdUseCase(GetEmployeeByIdUseCaseInterface):
    def __init__(self, employee_repo: EmployeeRepoInterface):
        self.employee_repo = employee_repo

    async def execute(self, params: GetEmployeeByIdInputDTO) -> GetEmployeeByIdResultDTO:
        try:
            # Получаем сотрудника
            try:
                got_employee = await self.employee_repo.get_by_id(params.employee_id)
            except Exception as e:
                logger.error(f"Ошибка БД при получении сотрудника {params.employee_id}: {e}")
                raise RepoOperationError("get_by_id", str(e))

            if got_employee is None:
                raise EmployeeNotFoundError(params.employee_id)

            return GetEmployeeByIdResultDTO(
                employee_id=got_employee.employee_id,
                first_name=got_employee.first_name,
                last_name=got_employee.last_name,
                fired=got_employee.fired,
                fired_dt=got_employee.fired_dt
            )

        except (EmployeeNotFoundError, RepoOperationError):
            raise
        except Exception as e:
            logger.error(f"Неожиданная ошибка в GetEmployeeByIdUseCase: {e}")
            raise RepoOperationError("get_employee_by_id", "Внутренняя ошибка сервера")


class GetAllEmployeesUseCase(GetAllEmployeesUseCaseInterface):
    def __init__(self, employee_repo: EmployeeRepoInterface):
        self.employee_repo = employee_repo

    async def execute(self) -> GetAllEmployeesResultDTO:
        try:
            # Получаем всех сотрудников
            try:
                employees = await self.employee_repo.get_all()
            except Exception as e:
                logger.error(f"Ошибка БД при получении всех сотрудников: {e}")
                raise RepoOperationError("get_all", str(e))

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

        except RepoOperationError:
            raise
        except Exception as e:
            logger.error(f"Неожиданная ошибка в GetAllEmployeesUseCase: {e}")
            raise RepoOperationError("get_all_employees", "Внутренняя ошибка сервера")


class FireEmployeeUseCase(FireEmployeeUseCaseInterface):
    def __init__(self, employee_repo: EmployeeRepoInterface):
        self.employee_repo = employee_repo

    async def execute(self, params: FireEmployeeInputDTO) -> FireEmployeeResultDTO:
        try:
            # Получаем сотрудника из репозитория
            try:
                employee = await self.employee_repo.get_by_id(params.employee_id)
            except Exception as e:
                logger.error(f"Ошибка БД при получении сотрудника {params.employee_id}: {e}")
                raise RepoOperationError("get_by_id", str(e))

            if employee is None:
                raise EmployeeNotFoundError(params.employee_id)

            # Проверяем, не уволен ли уже сотрудник
            if employee.fired:
                raise EmployeeAlreadyFiredError(employee.employee_id, employee.fired_dt)

            # Используем метод fire из класса Employee
            try:
                employee.fire(params.fired_dt)
            except DomainError as e:
                raise InvalidEmployeeDataError("fired_dt", str(e))

            # Обновляем сотрудника в репозитории
            try:
                await self.employee_repo.update(employee)
            except Exception as e:
                logger.error(f"Ошибка БД при обновлении сотрудника {params.employee_id}: {e}")
                raise RepoOperationError("update", str(e))

            return FireEmployeeResultDTO(
                employee_id=employee.employee_id,
                fired=employee.fired,
                fired_dt=employee.fired_dt
            )

        except (EmployeeNotFoundError, EmployeeAlreadyFiredError,
                InvalidEmployeeDataError, RepoOperationError):
            raise
        except Exception as e:
            logger.error(f"Неожиданная ошибка в FireEmployeeUseCase: {e}")
            raise RepoOperationError("fire_employee", "Внутренняя ошибка сервера")