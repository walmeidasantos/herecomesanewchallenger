import os
from sqlmodel import create_engine, SQLModel, Session, text


class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            url = os.getenv("DB_URL")
            cls._instance = create_engine(url, echo=False, isolation_level="AUTOCOMMIT")

        return cls._instance


def init_db():
    engine = DatabaseConnection()
    with Session(bind=engine) as session:
        try:
            session.execute(text("CREATE EXTENSION IF NOT EXISTS pgcrypto"))
            session.execute(text("CREATE EXTENSION IF NOT EXISTS pg_trgm"))
        except Exception as e:
            print(e)

    SQLModel.metadata.create_all(bind=engine)
    session.execute(
        text(
            """CREATE OR REPLACE FUNCTION generate_searchable(nome VARCHAR, apelido VARCHAR, stack JSON)
        RETURNS TEXT AS $$
        BEGIN
        RETURN nome || ' ' || apelido || stack;
        END;
        $$ LANGUAGE plpgsql IMMUTABLE;
"""
        )
    )
    session.execute(
        text(
            """
                ALTER TABLE pessoa
                ADD COLUMN IF NOT EXISTS search_text text GENERATED ALWAYS AS (generate_searchable(nome, apelido, stack)) STORED;
            """
        )
    )
    session.execute(
        text(
            "CREATE INDEX IF NOT EXISTS idx_pessoas_searchable ON pessoa USING gin(search_text gin_trgm_ops)"
        )
    )


def get_session():
    engine = DatabaseConnection()
    with Session(bind=engine) as session:
        try:
            yield session
        finally:
            session.close()
