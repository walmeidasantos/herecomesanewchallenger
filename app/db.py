import os
from sqlmodel import create_engine, SQLModel, Session
from dotenv import dotenv_values

class DatabaseConnection():
    _instanace = None

    def __new__(cls):
        if not cls._instanace:
            cls._instanace = super().__new__(cls)
            url = os.getenv("DATABASE_URL")

            cls._instanace = create_engine(url)

        return cls._instanace


def init_db():
    engine = DatabaseConnection()
    SQLModel.metadata.create_all(engine)


def get_session():
    engine = DatabaseConnection()
    with Session(engine,autocommit=False) as session:
        try: 
            yield session
        finally:
            session.close()