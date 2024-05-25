from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app2.crud.pessoa import (
    create_Pessoa,
    get_Pessoa_by_term,
    Pessoa,
    count_Pessoas,
    get_Pessoa,
)
from app2.db.session import get_session
from app2.models.Pessoa import PessoaCreate, PessoaResponse

router = APIRouter(
    prefix="/Pessoas",
    tags=["Pessoas"],
)


@router.post(
    "/",
    summary="Create a new Pessoa.",
    status_code=status.HTTP_201_CREATED,
    response_model=PessoaResponse,
)
async def create_Pessoa_route(
    data: PessoaCreate,
    db: AsyncSession = Depends(get_session),
):
    return await create_Pessoa(session=db, Pessoa=data)


@router.get(
    "/{id}",
    summary="Get a Pessoa.",
    status_code=status.HTTP_200_OK,
    response_model=Pessoa,
)
async def get_Pessoa_route(id: UUID, db: AsyncSession = Depends(get_session)):
    return await get_Pessoa(session=db, id=id)


@router.get(
    "/term",
    summary="Search Pessoa by term",
    status_code=status.HTTP_200_OK,
    response_model=list[Pessoa],
)
async def find_by_term(term: str, db: AsyncSession = Depends(get_session)):
    return await get_Pessoa_by_term(session=db, term=term)


@router.get("/contagem-Pessoas")
async def count(session: AsyncSession = Depends(get_session)):
    return count_Pessoas(session)
