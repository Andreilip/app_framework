from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

# Импортируем ошибки (добавлено)
from src.application.errors import (
    EmployeeNotFoundError,
    EmployeeAlreadyFiredError,
    EmployeeAlreadyExistsError,
    InvalidEmployeeDataError
)

"""
В данном файле выставляются все интерфейсы пользовательских сценариев
С данного файла начинает проектироваться все логика приложения
Интерфейсы сценариев -> сценарии -> сервисы и методы доменной модели -> 
интерфейсы репозиториев -> репозитории -> эндпоинты

Добавляется класс входных данных
Добавляется класс выходных данных
Надо бить на файлы, чтобы минимизировать конфликты слияния
"""


#------------------- AddEmployee
@dataclass
class AddEmployeeInputDTO:
    last_name: str
    first_name: str

@dataclass
class AddEmployeeResultDTO:
    employee_id: UUID

class AddEmployeeUseCaseInterface(ABC):
    @abstractmethod
    async def execute(self, employee: AddEmployeeInputDTO) -> AddEmployeeResultDTO:
        """
        Добавляет нового сотрудника
        Возможные ошибки:
        - InvalidEmployeeDataError: некорректные данные
        - EmployeeAlreadyExistsError: сотрудник с таким ID уже существует
        - DatabaseOperationError: ошибка БД
        """
        ...

#------------------ UpdateEmployee

@dataclass
class UpdateEmployeeInputDTO:
    employee_id: UUID
    first_name: str
    last_name: str

@dataclass
class UpdateEmployeeResultDTO:
    employee_id: UUID

class UpdateEmployeeUseCaseInterface(ABC):
    @abstractmethod
    async def execute(self, params: UpdateEmployeeInputDTO) -> UpdateEmployeeResultDTO:
        """
        Обновляет данные сотрудника
        Возможные ошибки:
        - EmployeeNotFoundError: сотрудник не найден
        - InvalidEmployeeDataError: некорректные данные
        - DatabaseOperationError: ошибка БД
        """
        ...

#------------------ DeleteEmployee
@dataclass
class DeleteEmployeeInputDTO:
    employee_id: UUID

class DeleteEmployeeUseCaseInterface(ABC):
    @abstractmethod
    async def execute(self, params: DeleteEmployeeInputDTO) -> None:
        """
        Удаляет сотрудника
        Возможные ошибки:
        - EmployeeNotFoundError: сотрудник не найден
        - DatabaseOperationError: ошибка БД
        """
        ...

#----------------- GetEmployeeById

@dataclass
class GetEmployeeByIdInputDTO:
    employee_id: UUID

@dataclass
class GetEmployeeByIdResultDTO:
    employee_id: UUID
    first_name: str
    last_name: str
    fired: bool
    fired_dt: datetime | None

class GetEmployeeByIdUseCaseInterface(ABC):
    @abstractmethod
    async def execute(self, params: GetEmployeeByIdInputDTO) -> GetEmployeeByIdResultDTO:
        """
        Получает сотрудника по ID
        Возможные ошибки:
        - EmployeeNotFoundError: сотрудник не найден
        - DatabaseOperationError: ошибка БД
        """
        ...

#----------------- GetAllEmployees
@dataclass
class GetAllEmployeeResultItemDTO:
    employee_id: UUID
    first_name: str
    last_name: str
    fired: bool
    fired_dt: datetime | None

@dataclass
class GetAllEmployeesResultDTO:
    employees: list[GetAllEmployeeResultItemDTO]

class GetAllEmployeesUseCaseInterface(ABC):
    @abstractmethod
    async def execute(self) -> GetAllEmployeesResultDTO:
        """
        Получает всех сотрудников
        Возможные ошибки:
        - DatabaseOperationError: ошибка БД
        """
        ...

# ------------------- FireEmployee
@dataclass
class FireEmployeeInputDTO:
    employee_id: UUID
    fired_dt: datetime | None = None  # Если не указана, ставится текущая дата

@dataclass
class FireEmployeeResultDTO:
    employee_id: UUID
    fired: bool
    fired_dt: datetime | None
    message: str = "Employee successfully fired"

class FireEmployeeUseCaseInterface(ABC):
    @abstractmethod
    async def execute(self, params: FireEmployeeInputDTO) -> FireEmployeeResultDTO:
        """
        Увольняет сотрудника (устанавливает fired=True и fired_dt)
        Возможные ошибки:
        - EmployeeNotFoundError: сотрудник не найден
        - EmployeeAlreadyFiredError: сотрудник уже уволен
        - DatabaseOperationError: ошибка БД
        """
        ...