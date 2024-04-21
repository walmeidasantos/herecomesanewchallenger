
import uuid as uuid_pkg
from typing import List
from datetime import date
from sqlmodel import Field, SQLModel, String, ARRAY,Column,Float


class Pessoa(SQLModel, table=True):
    """ classe pessoa """
    uuid: uuid_pkg.UUID = Field(default_factory=uuid_pkg.uuid4, primary_key=True, index=True, nullable=False)
    name: str = Field(max_length=100)
    nickname: str = Field(max_length=30, unique=True, nullable=False)
    nascimento: str = Field(default=date.today().strftime('%Y-%m-%d'))
    stack: List =  Field(sa_column=Column(ARRAY(String), nullable=True))

class Config:
    arbitrary_types_allowed = True