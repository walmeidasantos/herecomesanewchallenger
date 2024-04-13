from dataclasses import dataclass
from sqlmodel import Field, SQLModel, create_engine
from typing import Optional
import os 
from dotenv import dotenv_values
import psycopg2

config = dotenv_values(".env")

DATABASE_URI = "postgresql://" + config['POSTGRES_USER'] + ":" + config['POSTGRES_PASSWORD'] + "@"+ config['POSTGRES_HOST'] + ":5438/" + config["POSTGRES_DB"]
vector = create_engine(DATABASE_URI,echo=True)
SQLModel.metadata.create_all(vector)


class Pessoa(SQLModel, table=True):

    id: Optional[int] = Field(default=None,primary_key=True)
    name: str


if __name__ == "__main__":
     print(DATABASE_URI)
       


