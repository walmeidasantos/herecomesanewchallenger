
import uuid as uuid_pkg
from pydantic import schema
from datetime import date
from sqlmodel import Field, SQLModel, Column, Computed, String, default
import sqlalchemy as sa
from sqlalchemy.sql import func

class PessoaJson(SQLModel, table=False):
    name: str = Field(max_length=100)
    nickname: str = Field(max_length=30, unique=True, nullable=False)
    nascimento: str = Field(default=date.today().strftime('%Y-%m-%d'))
    stack: dict = Field(sa_column=Column(sa.JSON), default=dict)

class Pessoa(PessoaJson, table=True):
    """ classe pessoa """
    __tablename__ = "pessoa"

    uuid: uuid_pkg.UUID = Field(default_factory=uuid_pkg.uuid4, primary_key=True, index=True, nullable=False)
    _search_text: str 



class Config:
    arbitrary_types_allowed = True
    underscore_attrs_are_private = True