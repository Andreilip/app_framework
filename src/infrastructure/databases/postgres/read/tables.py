
from sqlalchemy import Table, Column, String, Boolean, DateTime, MetaData, UUID

metadata = MetaData()

employees_table = Table(
    'employees',
    metadata,
    Column('employee_id', UUID, primary_key=True),
    Column('last_name', String, nullable=False),
    Column('first_name', String, nullable=False),
    Column('fired', Boolean, default=False),
    Column('fired_dt', DateTime, nullable=True),
)

