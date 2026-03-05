from datetime import datetime
from uuid import UUID, uuid4
from src.domain.errors import DomainError, EmployeeAlreadyFiredError

"""
В данном файле объявляются классы доменной области, соответствующие реальным объектам
"""


class Employee:

    def __init__(self, last_name: str,
                 first_name: str,
                 fired: bool = False,
                 fired_dt: datetime | None = None,
                 employee_id: UUID | None = None):
        if last_name is None or first_name is None:
            raise ValueError("Параметры last_name и first_name являются обязательными")

        if last_name and len(last_name.strip()) == 0:
            raise ValueError("Фамилия не может быть пустой")
        if first_name and len(first_name.strip()) == 0:
            raise ValueError("Имя не может быть пустым")

        self.employee_id = employee_id or uuid4()
        self.last_name = last_name.strip() if last_name else last_name
        self.first_name = first_name.strip() if first_name else first_name
        self.fired = fired
        self.fired_dt = fired_dt

    def fire(self, fired_dt: datetime | None = None) -> None:
        """
        Уволить сотрудника
        Если дата не указана, устанавливается текущая
        Если сотрудник уже уволен, выбрасывается исключение (изменено)
        """
        if self.fired:
            raise EmployeeAlreadyFiredError(
                employee_id=self.employee_id,
                fired_dt=self.fired_dt
            )

        self.fired = True
        self.fired_dt = fired_dt or datetime.now()

    def __repr__(self):
        return f"Employee(id={self.employee_id}, name={self.last_name} {self.first_name}, fired={self.fired})"