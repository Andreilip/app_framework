from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

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
        ...

#------------------ DeleteEmployee
@dataclass
class DeleteEmployeeInputDTO:
    employee_id: UUID



class DeleteEmployeeUseCaseInterface(ABC):
    @abstractmethod
    async def execute(self, params: DeleteEmployeeInputDTO) -> None:
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
        """
        ...