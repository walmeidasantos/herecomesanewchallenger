import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from ..models import Pessoa
from sqlmodel import text, delete, SQLModel
import asyncio

# from sqlalchemy_utils import create_database, database_exists

url = os.getenv("DB_URL", "")
async_url = os.getenv("ASYNC_DB_URL", "")
AsyncEngine = create_async_engine(
    url,
    echo=False,
    pool_size=250,
    max_overflow=10,
)
# Session = sessionmaker(
#     bind=AsyncEngine,
#     autocommit=False,
#     autoflush=False,
#     expire_on_commit=False,
#     class_=AsyncSession,
# )
Session = AsyncSession(bind=AsyncEngine, autoflush=True)


async def get_database():
    """Provides a generator for database sessions with proper context management.

    Yields:
        SessionLocal: An open database session.
    """
    async with Session() as session:
        try:
            yield session
        except Exception as err:
            await session.rollback()
            raise err
        finally:
            await session.close()


async def delete_pessoas() -> None:
    statement = delete(Pessoa)
    await Session.execute(statement)


async def init_db() -> None:
    """Initializes the database schema and extensions.

    Args:
        session: An open database session.
    """
    async with AsyncEngine.connect() as session:
        # if not database_exists(url):
        #    await session.run_sync(create_database(url))
        try:
            await session.run_sync(SQLModel.metadata.create_all, checkfirst=True)
            await session.execute(text("CREATE EXTENSION IF NOT EXISTS pgcrypto"))
            await session.execute(text("CREATE EXTENSION IF NOT EXISTS pg_trgm"))
            await session.execute(
                text(
                    """
                    CREATE OR REPLACE FUNCTION generate_searchable(nome VARCHAR, apelido VARCHAR, stack JSON)
                    RETURNS TEXT AS $$
                    BEGIN
                      RETURN nome || ' ' || apelido || stack;
                    END;
                    $$ LANGUAGE plpgsql IMMUTABLE;
                    """
                )
            )
            await session.execute(
                text(
                    """
                   ALTER TABLE pessoa
                   ADD COLUMN IF NOT EXISTS search_text text GENERATED ALWAYS AS (generate_searchable(nome, apelido, stack)) STORED;
                   """
                )
            )
            await session.execute(
                text(
                    "CREATE INDEX IF NOT EXISTS idx_pessoas_searchable ON pessoa USING gin(search_text gin_trgm_ops)"
                )
            )
        except Exception as e:
            print(e)


if __name__ == "__main__":
    asyncio.run(init_db())
