from uuid import UUID
from sqlalchemy import insert, update, delete, select
from sqlalchemy.ext.asyncio import AsyncEngine
from src.application.repo_interfaces import EmployeeRepoInterface
from src.domain.models import Employee
from src.infrastructure.databases.postgres.write.tables import employees_table


"""
В данном файле находятся все реализации репозиториев данных
для SQLAlchemy и СУБД Postgres
"""




class SQLAlchemyPostgresEmployeeRepo(EmployeeRepoInterface):
    def __init__(self,engine: AsyncEngine):
        self.engine = engine

    async def get_by_id(self,  employee_id: UUID)-> Employee:
        select_query = select(employees_table).where(
            employees_table.c.employee_id == employee_id
        )
        # Выполнение
        async with self.engine.connect() as conn:
            query_result= await conn.execute(select_query)
            result=query_result.first()
        return Employee(**result._asdict())


    async def add(self, employee: Employee) -> None:
        # Запрос на добавление
        insert_query = insert(employees_table).values(
            employee_id=employee.employee_id,
            last_name=employee.last_name,
            first_name= employee.first_name,
            fired=employee.fired,
            fired_dt=employee.fired_dt
        )

        # Выполнение
        async with self.engine.connect() as conn:
            await conn.execute(insert_query)
            await conn.commit()


    async def update(self, employee:Employee)->None:
        update_query = (update(employees_table).
        where(employees_table.c.employee_id == employee.employee_id
        ).values(
            last_name=employee.last_name,
            first_name=employee.first_name,
            fired=employee.fired,
            fired_dt=employee.fired_dt
        ))

        # Выполнение
        async with self.engine.connect() as conn:
            await conn.execute(update_query)
            await conn.commit()

    async def delete(self, employee_id: UUID)->None:
        delete_query = (delete(employees_table).
        where(employees_table.c.employee_id == employee_id)
        )
        # Выполнение
        async with self.engine.connect() as conn:
            await conn.execute(delete_query)
            await conn.commit()

    async def get_all(self)->list[Employee]:
        # Запрос на выборку всех записей
        select_query = select(employees_table)

        # Выполнение
        async with self.engine.connect() as conn:
            query_result = await conn.execute(select_query)
            rows = query_result.fetchall()

        # Преобразование каждой строки в Employee
        return [Employee(**row._asdict()) for row in rows]

