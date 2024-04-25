import os
from sqlmodel import create_engine, SQLModel, Session, text


class DatabaseConnection():
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            url = os.getenv("DATABASE_URL")

            cls._instance = create_engine(url)

        return cls._instance



def init_db():
    engine = DatabaseConnection()
    with Session(engine,autocommit=False) as session:
        try: 
            session.execute(text("CREATE EXTENSION IF NOT EXISTS pgcrypto"))
            session.execute(text("CREATE EXTENSION IF NOT EXISTS pg_trgm"))
        except Exception as e:
            print(e)
        session.commit()

    SQLModel.metadata.create_all(bind=engine)


def get_session():
    engine = DatabaseConnection()
    with Session(engine,autocommit=False) as session:
        try: 
            yield session
        finally:
            session.close()