import os
from sqlmodel import create_engine, SQLModel, Session, text


class DatabaseConnection():
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            url = os.getenv("DATABASE_URL")

            cls._instance = create_engine(url,echo=True)

        return cls._instance



def init_db():
    engine = DatabaseConnection()
    with Session(engine,autocommit=False) as session:
        try: 
            session.execute(text("CREATE EXTENSION IF NOT EXISTS pgcrypto"))
            session.execute(text("CREATE EXTENSION IF NOT EXISTS pg_trgm"))
        except Exception as e:
            print(e)

    SQLModel.metadata.create_all(bind=engine)
    session.execute(  text("""CREATE OR REPLACE FUNCTION generate_searchable(name VARCHAR, nickname VARCHAR, stack JSON)
        RETURNS TEXT AS $$
        BEGIN
        RETURN name || ' ' || nickname || stack;
        END;
        $$ LANGUAGE plpgsql IMMUTABLE;
"""   ))
    session.execute( text( "CREATE INDEX IF NOT EXISTS idx_pessoas_searchable ON pessoa USING gin(search_text gin_trgm_ops)" ) )
    session.execute( text( "ALTER TABLE pessoa ALTER COLUMN search_text  TEXT GENERATED ALWAYS AS (generate_searchable(name,nickname,stack)) STORED"   ))
    session.commit()

def get_session():
    engine = DatabaseConnection()
    with Session(engine,autocommit=False) as session:
        try: 
            yield session
        finally:
            session.close()