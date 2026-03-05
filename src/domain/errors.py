from uuid import UUID
from datetime import datetime

"""
В данном файле объявляются ошибки доменной области
Эти ошибки возникают при нарушении бизнес-правил в доменных объектах
"""


class DomainError(Exception):
    """Базовый класс для всех доменных ошибок"""
    def __init__(self, message: str, code: str = "DOMAIN_ERROR"):
        self.message = message
        self.code = code
        super().__init__(self.message)


class EmployeeAlreadyFiredError(DomainError):
    """Ошибка: попытка уволить уже уволенного сотрудника"""
    def __init__(self, employee_id: UUID, fired_dt: datetime | None = None):
        message = f"Сотрудник с ID {employee_id} уже уволен"
        if fired_dt:
            message += f" (дата увольнения: {fired_dt})"
        super().__init__(
            message=message,
            code="EMPLOYEE_ALREADY_FIRED"
        )
        self.employee_id = employee_id
        self.fired_dt = fired_dt
