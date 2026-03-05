import logging
import traceback
from datetime import datetime
from fastapi import Request, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from src.application.errors import (
    ApplicationError,
    EmployeeNotFoundError,
    EmployeeAlreadyFiredError,
    EmployeeAlreadyExistsError,
    InvalidEmployeeDataError,
    RepoOperationError,
    ErrorResponseDTO
)

logger = logging.getLogger(__name__)


async def application_error_handler(request: Request, exc: ApplicationError):
    """Обработчик для всех ошибок приложения"""
    logger.error(f"Application error: {exc.code} - {exc.message}")

    status_code = status.HTTP_400_BAD_REQUEST

    if isinstance(exc, EmployeeNotFoundError):
        status_code = status.HTTP_404_NOT_FOUND
    elif isinstance(exc, (EmployeeAlreadyFiredError, EmployeeAlreadyExistsError)):
        status_code = status.HTTP_409_CONFLICT
    elif isinstance(exc, InvalidEmployeeDataError):
        status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    elif isinstance(exc, RepoOperationError):
        status_code = status.HTTP_503_SERVICE_UNAVAILABLE
 
    error_response = ErrorResponseDTO(
        error_code=exc.code,
        error_message=exc.message,
        details=getattr(exc, "__dict__", None)
    )

    return JSONResponse(
    status_code=status_code,
    content=error_response.to_dict()  
    )


async def validation_error_handler(request: Request, exc: ValidationError):
    """Обработчик для ошибок валидации Pydantic"""
    logger.error(f"Validation error: {exc}")

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "VALIDATION_ERROR",
            "message": "Ошибка валидации входных данных",
            "details": exc.errors(),
            "timestamp": datetime.now().isoformat()
        }
    )


async def general_error_handler(request: Request, exc: Exception):
    """Обработчик для всех остальных необработанных ошибок"""
    logger.error(f"Unhandled exception: {exc}")
    logger.error(traceback.format_exc())

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "INTERNAL_SERVER_ERROR",
            "message": "Внутренняя ошибка сервера",
            "timestamp": datetime.now().isoformat()
        }
    )