from fastapi import FastAPI, HTTPException, Query, Response, Request, Depends
import uvicorn
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlmodel import Session, text, select
from db import init_db, get_session
from models import Pessoa, PessoaJson


app = FastAPI(title="Rinha Backend 2023")


# app.debug = True
def serialize(data) -> str:
    return json.dumps(data, default=str)


@app.on_event("startup")
def on_startup():
    init_db()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(req: Request, exc: RequestValidationError):
    details = exc.errors()
    if any(
        detail["type"] == "string_type" and isinstance(detail["input"], int)
        for detail in details
    ):
        return JSONResponse(
            status_code=422,
            content=jsonable_encoder({"detail": details}),
        )
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder({"detail": details}),
    )


@app.post("/pessoas", status_code=201, response_model_exclude_unset=True)
def create(res: Response, pessoa: PessoaJson, session: Session = Depends(get_session)):

    try:
        new_pessoa = Pessoa.model_validate(pessoa)
        pessoa_existe = session.exec(
            select(Pessoa).where(Pessoa.apelido == new_pessoa.apelido)
        ).first()
        if pessoa_existe:
            raise ValueError

        session.add(new_pessoa)
        session.commit()
        session.refresh(new_pessoa)
        # res.headers.update({"Location": f"/pessoas/{new_pessoa.id}"})
        return new_pessoa
    except ValueError:
        raise HTTPException(status_code=400)
    return serialize(new_pessoa)


@app.get("/pessoas/{id}")
def find_by_id(uuid: str, session: Session = Depends(get_session)):

    try:
        pessoa_existe = session.exec(select(Pessoa).where(Pessoa.id == uuid)).first()
        if pessoa_existe:
            return pessoa_existe
        raise HTTPException(status_code=404)
    except:
        raise HTTPException(status_code=400)


@app.get("/pessoas", response_model=list[Pessoa])
def find_by_term(
    termo: str = Query(..., min_length=1), session: Session = Depends(get_session)
):
    pessoas = []
    try:
        raw_query = "SELECT id, nome,apelido,stack,nascimento FROM pessoa WHERE search_text ilike :termo "
        result = session.execute(
            text(raw_query), {"termo": "%" + termo + "%"}
        ).fetchmany(30)

        for row in result:
            pessoa = Pessoa(
                id=row.id,
                nome=row.nome,
                apelido=row.apelido,
                stack=row.stack,
                nascimento=row.nascimento,
            )
            pessoas.append(pessoa.dict())

        return pessoas
    except:
        raise HTTPException(status_code=400)


@app.get("/contagem-pessoas")
def count_pessoas(session: Session = Depends(get_session)):
    return session.query(Pessoa).count()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8003)
