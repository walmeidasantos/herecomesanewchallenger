from fastapi import FastAPI, HTTPException, Query, Response, Request, Depends
import uvicorn
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlmodel import Session, text, select
from db import init_db, get_session
from models import Pessoa, PessoaJson

app = FastAPI(title="Rinha Backend 2023")
# app.debug = True


@app.on_event("startup")
def on_startup():
    init_db()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, handler):
    return Response(status_code=400)


@app.post("/pessoas", status_code=201)
async def create_person(
    person: PessoaJson, res: Response, session: Session = Depends(get_session)
):
    try:
        new_pessoa = Pessoa.model_validate(person)
        pessoa_existe = session.exec(
            select(Pessoa).where(Pessoa.apelido == new_pessoa.apelido)
        ).first()
        if pessoa_existe:
            raise ValueError

        session.add(new_pessoa)
        session.commit()
        session.refresh(new_pessoa)
        res.headers["Location"] = f"/pessoas/{new_pessoa.id}"
        return new_pessoa
    except ValueError:
        raise HTTPException(status_code=400)


@app.get("/pessoas/{id}")
async def find_by_id(id: str, session: Session = Depends(get_session)):

    try:
        pessoa_existe = session.exec(select(Pessoa).where(Pessoa.id == id)).first()
        if pessoa_existe:
            return pessoa_existe
        else:
            raise HTTPException(status_code=404)
    except:
        raise HTTPException(status_code=400)


@app.get("/pessoas", response_model=list[Pessoa])
async def find_by_term(
    term: str = Query(..., alias="t"), session: Session = Depends(get_session)
):
    pessoas = []
    try:
        raw_query = "SELECT id, nome,apelido,stack,nascimento FROM pessoa WHERE search_text ilike :term"
        result = session.execute(text(raw_query), {"term": "%" + term + "%"}).fetchmany(
            30
        )

        for row in result:
            pessoa = Pessoa(
                id=row.id,
                nome=row.nome,
                apelido=row.apelido,
                stack=row.stack,
                nascimento=row.nascimento,
            )
            pessoas.append(pessoa.model_dump())

        return pessoas
    except:
        raise HTTPException(status_code=400)


@app.get("/contagem-pessoas")
def count_pessoas(session: Session = Depends(get_session)):
    return session.query(Pessoa).count()


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=9999)
