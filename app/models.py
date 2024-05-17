import uuid as uuid_pkg
from typing import Optional, List
from datetime import date
from sqlmodel import Field, SQLModel, Column
import sqlalchemy as sa


class PessoaJson(SQLModel, table=False):
    """classe pessoa json"""

    apelido: str = Field(max_length=30, unique=True, nullable=False)
    nome: str = Field(max_length=100)
    nascimento: str = Field(default=date.today().strftime("%Y-%m-%d"))
    stack: Optional[List[str]] = Field(sa_column=Column(sa.JSON))


class Pessoa(PessoaJson, table=True):
    """classe pessoa"""

    __table_args__ = {"keep_existing": True}

    id: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4, primary_key=True, index=True, nullable=False
    )
