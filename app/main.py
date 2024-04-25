
from fastapi import FastAPI, HTTPException, Query, Response, Request, Depends
from time import perf_counter
import uvicorn
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import json
from fastapi.encoders import jsonable_encoder
from sqlmodel import Session, or_, cast, String
from db import init_db, get_session
from models import Pessoa


app = FastAPI(title='Rinha Backend 2023')
app.debug = True

@app.on_event("startup")
def on_startup():
    init_db()

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
    try: 
        new_pessoa = Pessoa(**pessoa.model_dump())
        session.add(new_pessoa)
        session.commit()
        res.headers.update({'Location': f'/pessoas/{new_pessoa.id}'})
    except ValueError:
        raise HTTPException(status_code=422)
    return serialize(new_pessoa)

@app.get('/pessoas/{id}')
async def find_by_id(id: str, session: Session = Depends(get_session)):
    
    try:
        pessoa = session.query(Pessoa).get(id)
        pessoa_data = pessoa.__dict__
        return pessoa_data
    except:
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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8003)