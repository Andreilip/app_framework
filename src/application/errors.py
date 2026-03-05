from dataclasses import dataclass
from uuid import UUID
from datetime import datetime

"""
В данном файле определяются классы ошибок приложения (Application Layer)
Эти ошибки возникают при нарушении бизнес-правил или логики приложения
"""

class ApplicationError(Exception):
    """Базовый класс для всех ошибок приложения"""
    def __init__(self, message: str, code: str = "APPLICATION_ERROR"):
        self.message = message
        self.code = code
        super().__init__(self.message)


class EmployeeNotFoundError(ApplicationError):
    """Ошибка: сотрудник не найден"""
    def __init__(self, employee_id: UUID):
        super().__init__(
            message=f"Сотрудник с ID {employee_id} не найден",
            code="EMPLOYEE_NOT_FOUND"
        )
        self.employee_id = employee_id


class EmployeeAlreadyFiredError(ApplicationError):
    """Ошибка: сотрудник уже уволен"""
    def __init__(self, employee_id: UUID, fired_dt: datetime):
        super().__init__(
            message=f"Сотрудник с ID {employee_id} уже был уволен {fired_dt}",
            code="EMPLOYEE_ALREADY_FIRED"
        )
        self.employee_id = employee_id
        self.fired_dt = fired_dt


class EmployeeAlreadyExistsError(ApplicationError):
    """Ошибка: сотрудник с таким ID уже существует"""
    def __init__(self, employee_id: UUID):
        super().__init__(
            message=f"Сотрудник с ID {employee_id} уже существует",
            code="EMPLOYEE_ALREADY_EXISTS"
        )
        self.employee_id = employee_id


class InvalidEmployeeDataError(ApplicationError):
    """Ошибка: некорректные данные сотрудника"""
    def __init__(self, field: str, reason: str):
        super().__init__(
            message=f"Некорректное значение поля {field}: {reason}",
            code="INVALID_EMPLOYEE_DATA"
        )
        self.field = field
        self.reason = reason


class RepoOperationError(ApplicationError):
    """Ошибка: ошибка при работе с базой данных"""
    def __init__(self, operation: str, details: str = ""):
        message = f"Ошибка при выполнении операции {operation}"
        if details:
            message += f": {details}"
        super().__init__(
            message=message,
            code="REPO_OPERATION_ERROR"
        )
        self.operation = operation
        self.details = details


# DTO для ошибок API
@dataclass
class ErrorResponseDTO:
    """Структура ответа с ошибкой"""
    error_code: str
    error_message: str
    details: dict | None = None
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
    
    def to_dict(self):
        """Преобразует DTO в словарь с сериализацией UUID"""
        result = {
            "error_code": self.error_code,
            "error_message": self.error_message,
            "timestamp": self.timestamp.isoformat()
        }
        
        if self.details:
            # Рекурсивно преобразуем UUID в строки
            result["details"] = self._serialize(self.details)
        else:
            result["details"] = None
            
        return result
    
    def _serialize(self, obj):
        """Рекурсивная сериализация UUID и datetime"""
        if isinstance(obj, UUID):
            return str(obj)
        elif isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, dict):
            return {key: self._serialize(value) for key, value in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [self._serialize(item) for item in obj]
        else:
            return obj