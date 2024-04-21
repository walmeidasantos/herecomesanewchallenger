from sqlalchemy import URL
from sqlmodel import create_engine, SQLModel, Session
from dotenv import dotenv_values


class DatabaseConnection():
    _instanace = None

    def __new__(cls):
        if not cls._instanace:
            cls._instanace = super().__new__(cls)
            config = dotenv_values(".env")
            url = URL.create(
                    drivername="postgresql",
                    username=config['POSTGRES_USER'],
                    password=config['POSTGRES_PASSWORD'],
                    host=config['POSTGRES_HOST'],
                    port=5438,
                    database=config['POSTGRES_DB']
                    )
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