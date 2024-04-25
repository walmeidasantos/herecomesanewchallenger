
import uuid as uuid_pkg
from typing import List,Optional
from datetime import date
from sqlmodel import Field, SQLModel, Column, Computed, String
import sqlalchemy as sa


class Pessoa(SQLModel, table=True):
    """ classe pessoa """
    __tablename__ = "pessoa"

    
    uuid: uuid_pkg.UUID = Field(default_factory=uuid_pkg.uuid4, primary_key=True, index=True, nullable=False)
    name: str = Field(max_length=100)
    nickname: str = Field(max_length=30, unique=True, nullable=False)
    nascimento: str = Field(default=date.today().strftime('%Y-%m-%d'))
    stack: dict = Field(sa_column=Column(sa.JSON), default=dict)
    search_text: str = Column(String, Computed( "name || ' ' || nickname || ' '  || stack", persisted=True))
    __table_args__ = (
        sa.Index('idx_pessoas', "search_text",
                postgresql_ops={"search_text": "gist_trgm_ops"},
                postgresql_using='gist')
    ,)


class Config:
    arbitrary_types_allowed = True