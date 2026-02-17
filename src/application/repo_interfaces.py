from abc import ABC

from src.domain.models import Employee
from uuid import UUID

"""
В данном файле  выставляются все интерфейсы репозиториев данных
"""

class EmployeeRepoInterface(ABC):
    async def get_by_id(self,employee_id: UUID)->Employee:
        ...

    async def add(self, employee:Employee)->None:
        ...

    async def update(self, employee:Employee)->None:
        ...

    async def delete(self, employee_id: UUID)->None:
        ...

    async def get_all(self)->list[Employee]:
        ...
