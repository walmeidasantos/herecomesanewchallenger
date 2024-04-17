from typing import Optional
import uuid as uuid_pkg
from sqlalchemy import URL
from sqlmodel import Field, SQLModel, create_engine, Session, select, String, ARRAY,Column, or_, cast
from dotenv import dotenv_values
from pydantic import StringConstraints
from datetime import date
from fastapi import FastAPI, HTTPException, Query, Response, Request, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import json
from time import perf_counter
from psycopg2 import create_engine as pg_create_engine

config = dotenv_values(".env")
URL_OBJ = URL.create(
    drivername="postgresql",
    username=config['POSTGRES_USER'],
    password=config['POSTGRES_PASSWORD'],
    host=config['POSTGRES_HOST'],
    port=5438,
    database=config['POSTGRES_DB']
    )

libdireta = pg_create_engine(URL_OBJ)
vector = create_engine(URL_OBJ)

session = Session(vector,autocommit=False)
SQLModel.metadata.create_all(vector)
app = FastAPI(title='Rinha Backend 2023')


class Pessoa(SQLModel, table=True):
    """ classe pessoa """
    uuid: uuid_pkg.UUID = Field(default_factory=uuid_pkg.uuid4, primary_key=True, index=True, nullable=False)
    name: str = Field(max_length=100)
    nickname: str = Field(max_length=30, unique=True, nullable=False)
    nascimento: str = Field(default=date.today().strftime('%Y-%m-%d'))
    stack = Column(ARRAY(String(32)), nullable=True)



def get_session():

    try:
        yield session
    finally:
        # This will handle closing the session whatever it happens on request
        # when using Depends of FastAPI on a route function.
        session.close()



@app.exception_handler(RequestValidationError)
async def validation_exception_handler(req: Request, exc: RequestValidationError):
    details = exc.errors()
    if any(detail['type'] == 'string_type' and isinstance(detail['input'], int) for detail in details):
        return JSONResponse(
            status_code=400,
            content=jsonable_encoder({'detail': details}),
        )    
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder({'detail': details}),
    )

def serialize(data):
    return json.dumps(data, default=str)


def deserialize(data):
    return json.loads(data)


@app.post('/pessoas', status_code=201)
def create(res: Response, pessoa: Pessoa, session: Session = Depends(get_session)):
    new_pessoa = Pessoa(**pessoa.model_dump())
    session.add(new_pessoa)
    session.commit()
    res.headers.update({'Location': f'/pessoas/{new_pessoa.id}'})


@app.get('/pessoas/{id}')
async def find_by_id(id: str, session: Session = Depends(get_session)):
    pessoa = session.query(Pessoa).get(id)
    if pessoa:
        pessoa_data = pessoa.__dict__
        return pessoa_data
    else:
        raise HTTPException(status_code=404)


@app.get('/pessoas')
def find_by_term(t: str = Query(..., min_length=1), session: Session = Depends(get_session)):
    return session.query(Pessoa).filter(
        or_(Pessoa.apelido.ilike(f'%{t}%'),
            Pessoa.nome.ilike(f'%{t}%'),
            cast(Pessoa.stack, String).ilike(f'%{t}%'))
    ).limit(50).all()


@app.get("/contagem-pessoas")
def count_pessoas(session: Session = Depends(get_session)):
    return session.query(Pessoa).count()



