from models import Pessoa, PessoaJson
from fastapi import FastAPI, HTTPException, Query, Response, Depends
import uvicorn
from fastapi.exceptions import RequestValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlmodel import text
from database import init_db, get_database, delete_pessoas

app = FastAPI(title="Rinha Backend 2023")
# app.debug = True


@app.on_event("startup")
async def on_startup():
    await init_db()
    # await delete_pessoas()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler():
    return Response(status_code=400)


@app.post("/pessoas", status_code=201)
async def create_person(
    person: PessoaJson, res: Response, session: AsyncSession = Depends(get_database)
):
    try:
        new_pessoa = Pessoa.model_validate(person)
        pessoa_existe = (
            await session.execute(
                select(Pessoa).where(Pessoa.apelido == new_pessoa.apelido)
            )
        ).first()
        if pessoa_existe:
            raise ValueError

        session.add(new_pessoa)
        await session.commit()
        await session.refresh(new_pessoa)
        res.headers["Location"] = f"/pessoas/{new_pessoa.id}"
        return new_pessoa
    except ValueError:
        raise HTTPException(status_code=400)


@app.get("/pessoas/{id}")
async def find_by_id(id: str, session: AsyncSession = Depends(get_database)):
    try:
        pessoa_existe = (
            (await session.execute(select(Pessoa).where(Pessoa.id == id)))
            .mappings()
            .first()
        )
        if pessoa_existe:
            return pessoa_existe
        else:
            raise HTTPException(status_code=400)
    except:
        raise HTTPException(status_code=400)


@app.get("/pessoas", response_model=list[Pessoa])
async def find_by_term(
    term: str = Query(..., alias="t"), session: AsyncSession = Depends(get_database)
):
    pessoas = []
    try:
        raw_query = "SELECT id, nome,apelido,stack,nascimento FROM pessoa WHERE search_text ilike :term"
        result = (
            await session.execute(text(raw_query), {"term": "%" + term + "%"})
        ).fetchmany(30)
        if not result:
            raise HTTPException(status_code=400)

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
async def count_pessoas(session: AsyncSession = Depends(get_database)):
    query = select(func.count(Pessoa.id))
    result = await session.execute(query)
    count = result.scalar_one()
    return count


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9999)
