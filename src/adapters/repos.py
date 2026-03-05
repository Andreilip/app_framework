from uuid import UUID
from sqlalchemy import insert, update, delete, select
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncEngine
from src.application.repo_interfaces import EmployeeRepoInterface
from src.application.errors import (
    EmployeeNotFoundError,
    EmployeeAlreadyExistsError,
    RepoOperationError
)
from src.domain.models import Employee
from src.infrastructure.databases.postgres.write.tables import employees_table

import logging

"""
В данном файле находятся все реализации репозиториев данных
для SQLAlchemy и СУБД Postgres с обработкой ошибок
"""

logger = logging.getLogger(__name__)


class SQLAlchemyPostgresEmployeeRepo(EmployeeRepoInterface):
    def __init__(self, engine: AsyncEngine):
        self.engine = engine

    async def get_by_id(self, employee_id: UUID) -> Employee | None:
        """Получение сотрудника по ID с обработкой ошибок"""
        try:
            select_query = select(employees_table).where(
                employees_table.c.employee_id == employee_id
            )

            async with self.engine.connect() as conn:
                query_result = await conn.execute(select_query)
                result = query_result.first()

            if result is None:
                return None

            return Employee(**result._asdict())

        except SQLAlchemyError as e:
            logger.error(f"SQLAlchemy error in get_by_id for {employee_id}: {e}")
            raise RepoOperationError("get_by_id", str(e)) # TODO -поменять на RepositoryOperationError
        except Exception as e:
            logger.error(f"Unexpected error in get_by_id for {employee_id}: {e}")
            raise RepoOperationError("get_by_id", "Неожиданная ошибка при получении сотрудника")

    async def add(self, employee: Employee) -> None:
        """Добавление сотрудника с обработкой ошибок"""
        try:
            insert_query = insert(employees_table).values(
                employee_id=employee.employee_id,
                last_name=employee.last_name,
                first_name=employee.first_name,
                fired=employee.fired,
                fired_dt=employee.fired_dt
            )

            async with self.engine.connect() as conn:
                await conn.execute(insert_query)
                await conn.commit()

        except IntegrityError as e:
            logger.error(f"Integrity error in add for {employee.employee_id}: {e}")
            # Проверяем, это ошибка дубликата?
            if "duplicate key" in str(e).lower():
                raise EmployeeAlreadyExistsError(employee.employee_id)
            raise RepoOperationError("add", "Нарушение целостности данных")
        except SQLAlchemyError as e:
            logger.error(f"SQLAlchemy error in add for {employee.employee_id}: {e}")
            raise RepoOperationError("add", str(e))
        except Exception as e:
            logger.error(f"Unexpected error in add for {employee.employee_id}: {e}")
            raise RepoOperationError("add", "Неожиданная ошибка при добавлении сотрудника")

    async def update(self, employee: Employee) -> None:
        """Обновление сотрудника с обработкой ошибок"""
        try:
            # Сначала проверяем, существует ли сотрудник
            existing = await self.get_by_id(employee.employee_id)
            if existing is None:
                raise EmployeeNotFoundError(employee.employee_id)

            update_query = (update(employees_table)
                .where(employees_table.c.employee_id == employee.employee_id)
                .values(
                    last_name=employee.last_name,
                    first_name=employee.first_name,
                    fired=employee.fired,
                    fired_dt=employee.fired_dt
                ))

            async with self.engine.connect() as conn:
                await conn.execute(update_query)
                await conn.commit()

        except EmployeeNotFoundError:
            raise
        except SQLAlchemyError as e:
            logger.error(f"SQLAlchemy error in update for {employee.employee_id}: {e}")
            raise RepoOperationError("update", str(e))
        except Exception as e:
            logger.error(f"Unexpected error in update for {employee.employee_id}: {e}")
            raise RepoOperationError("update", "Неожиданная ошибка при обновлении сотрудника")

    async def delete(self, employee_id: UUID) -> None:
        """Удаление сотрудника с обработкой ошибок"""
        try:
            # Сначала проверяем, существует ли сотрудник
            existing = await self.get_by_id(employee_id)
            if existing is None:
                raise EmployeeNotFoundError(employee_id)

            delete_query = (delete(employees_table)
                .where(employees_table.c.employee_id == employee_id))

            async with self.engine.connect() as conn:
                await conn.execute(delete_query)
                await conn.commit()

        except EmployeeNotFoundError:
            raise
        except SQLAlchemyError as e:
            logger.error(f"SQLAlchemy error in delete for {employee_id}: {e}")
            raise RepoOperationError("delete", str(e))
        except Exception as e:
            logger.error(f"Unexpected error in delete for {employee_id}: {e}")
            raise RepoOperationError("delete", "Неожиданная ошибка при удалении сотрудника")

    async def get_all(self) -> list[Employee]:
        """Получение всех сотрудников с обработкой ошибок"""
        try:
            select_query = select(employees_table)

            async with self.engine.connect() as conn:
                query_result = await conn.execute(select_query)
                rows = query_result.fetchall()

            return [Employee(**row._asdict()) for row in rows]

        except SQLAlchemyError as e:
            logger.error(f"SQLAlchemy error in get_all: {e}")
            raise RepoOperationError("get_all", str(e))
        except Exception as e:
            logger.error(f"Unexpected error in get_all: {e}")
            raise RepoOperationError("get_all", "Неожиданная ошибка при получении списка сотрудников")