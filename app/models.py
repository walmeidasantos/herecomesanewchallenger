
import uuid as uuid_pkg
from typing import List,Optional
from datetime import date
from sqlmodel import Field, SQLModel, Column, Computed, String, default
import sqlalchemy as sa
from sqlalchemy.sql import func

class PessoaJson(SQLModel, table=False):
    """ classe pessoa for json """
    name: str = Field(max_length=100)
    nickname: str = Field(max_length=30, unique=True, nullable=False)
    nascimento: str = Field(default=date.today().strftime('%Y-%m-%d'))
    stack: dict = Field(sa_column=Column(sa.JSON), default=dict)

class Pessoa(PessoaJson, table=True):
    """ classe pessoa """
    __tablename__ = "pessoa"

    uuid: uuid_pkg.UUID = Field(default_factory=uuid_pkg.uuid4, primary_key=True, index=True, nullable=False)



class Config:
    arbitrary_types_allowed = True