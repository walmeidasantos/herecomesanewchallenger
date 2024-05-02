import uuid as uuid_pkg
from typing import Optional
from pydantic import schema, computed_field, model_validator, validator, root_validator
from datetime import date
from sqlmodel import Field, SQLModel, Column, Computed, String, default, text
import sqlalchemy as sa
from pydantic.json_schema import SkipJsonSchema
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import column_property


class PessoaJson(SQLModel, table=False):
    nome: str = Field(max_length=100)
    apelido: str = Field(max_length=30, unique=True, nullable=False)
    nascimento: str = Field(default=date.today().strftime("%Y-%m-%d"))
    stack: dict = Field(sa_column=Column(sa.JSON), default=dict)


class Pessoa(PessoaJson, table=True):
    """classe pessoa"""

    id: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4, primary_key=True, index=True, nullable=False
    )
