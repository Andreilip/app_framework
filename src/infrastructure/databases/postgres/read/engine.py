from sqlalchemy.ext.asyncio import create_async_engine
from src.infrastructure.databases.postgres.read.settings import database_postgres_settings

READ_DATABASE_URL = (f"postgresql+asyncpg://{database_postgres_settings.DB_READ_USERNAME}:"
               f"{database_postgres_settings.DB_READ_PASSWORD}@"
               f"{database_postgres_settings.DB_READ_HOST}:"
               f"{database_postgres_settings.DB_READ_PORT}/"
               f"{database_postgres_settings.DB_READ_NAME}")

read_engine = create_async_engine(READ_DATABASE_URL)



