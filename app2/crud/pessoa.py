from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, text, func

from app2.models.pessoa import Pessoa, PessoaCreate


async def create_Pessoa(session: AsyncSession, Pessoa: PessoaCreate) -> Pessoa:
    db_Pessoa = Pessoa(**Pessoa.dict())
    try:
        session.add(db_Pessoa)
        await session.commit()
        await session.refresh(db_Pessoa)

        return db_Pessoa
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=409,
            detail="Pessoa already exists",
        )


async def get_Pessoa(session: AsyncSession, id: UUID) -> Pessoa:
    query = select(Pessoa).where(Pessoa.id == id)
    response = await session.execute(query)
    return response.scalar_one_or_none()


async def get_Pessoa_by_term(session: AsyncSession, term: str) -> list[Pessoa]:

    Pessoas = []

    raw_query = "SELECT id, nome,apelido,stack,nascimento FROM pessoa WHERE search_text ilike :term"
    result = (
        await session.execute(text(raw_query), {"term": "%" + term + "%"})
    ).fetchmany(30)
    if not result:
        raise HTTPException(status_code=400, detail="termo not found")

    for row in result:
        Pessoa = Pessoa(
            id=row.id,
            nome=row.nome,
            apelido=row.apelido,
            stack=row.stack,
            nascimento=row.nascimento,
        )
        Pessoas.append(Pessoa.model_dump())

    return Pessoas


async def count_Pessoas(session: AsyncSession):

    query = select(func.count(Pessoa.id))
    result = await session.execute(query)
    count = result.scalar_one()
    return count
