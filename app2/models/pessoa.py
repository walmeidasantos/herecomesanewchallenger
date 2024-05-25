from typing import Optional, List
import uuid as uuid_pkg
from datetime import date
from sqlmodel import Field, SQLModel, Column
import sqlalchemy as sa


class PessoaBase(SQLModel, table=False):
    """classe pessoa json"""

    apelido: str = Field(max_length=30, unique=True, nullable=False)
    nome: str = Field(max_length=100)
    nascimento: str = Field(default=date.today().strftime("%Y-%m-%d"))
    stack: Optional[List[str]] = Field(sa_column=Column(sa.JSON))


class PessoaCreate(PessoaBase): ...


class Pessoa(PessoaBase, table=True):
    """classe pessoa"""

    id: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4, primary_key=True, index=True, nullable=False
    )
