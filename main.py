from dataclasses import dataclass
from typing import Optional
from sqlmodel import Field, SQLModel, create_engine, Session, select
import os 
from dotenv import dotenv_values
import psycopg2

config = dotenv_values(".env")

DATABASE_URI = "postgresql://" + config['POSTGRES_USER'] + ":" + config['POSTGRES_PASSWORD'] + "@"+ config['POSTGRES_HOST'] + ":5438/" + config["POSTGRES_DB"]

class Pessoa(SQLModel, table=True):

    id: Optional[int] = Field(default=None,primary_key=True)
    name: str = Field(max_length=100)
    nickname: str = Field(max_length=30)


if __name__ == "__main__":
    #  SQLModel.metadata.create_all(vector)
    vector = create_engine(DATABASE_URI,echo=True)
    eumesmo = Pessoa(name="Teste pessoa 1")
    aMinhaNamoradatambem = Pessoa(name="Teste pessoa 2")
    session = Session(vector)

    # session.add(eumesmo)
    # session.add(aMinhaNamoradatambem)
    # session.commit()
    results = session.exec( select(Pessoa).where(Pessoa.id==1) )
    # print(eumesmo.name)
    # print(aMinhaNamoradatambem.name)
    # for pessoa in results:
    #     print(pessoa)
        
    pessoa = results.first()
    print(pessoa)   
    pessoa.name="Wellingtao"
    session.add(pessoa)
    session.commit()
    session.refresh(pessoa)
    print(pessoa)
    session.close


