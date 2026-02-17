from sqlalchemy.ext.asyncio import create_async_engine
from src.infrastructure.databases.postgres.write.settings import database_postgres_settings

WRITE_DATABASE_URL = (f"postgresql+asyncpg://{database_postgres_settings.DB_WRITE_USERNAME}:"
               f"{database_postgres_settings.DB_WRITE_PASSWORD}@"
               f"{database_postgres_settings.DB_WRITE_HOST}:"
               f"{database_postgres_settings.DB_WRITE_PORT}/"
               f"{database_postgres_settings.DB_WRITE_NAME}")

write_engine = create_async_engine(WRITE_DATABASE_URL)


