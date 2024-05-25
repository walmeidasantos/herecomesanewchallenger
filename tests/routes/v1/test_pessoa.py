from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid_extensions import uuid7

from app2.crud.pessoa import (
    create_pessoa,
    delete_pessoa,
    get_pessoa,
    get_pessoa_by_email,
    update_pessoa,
)
from app2.models.pessoa import pessoaCreate, pessoaUpdate


async def test_create_pessoa(session: AsyncSession):
    pessoa = pessoaCreate(email="test@example.com")
    created_pessoa = await create_pessoa(session, pessoa)
    assert created_pessoa.id is not None
    assert created_pessoa.email == pessoa.email
    assert created_pessoa.created_at is not None
    assert created_pessoa.updated_at is not None


async def test_create_duplicate_pessoa(session: AsyncSession):
    pessoa = pessoaCreate(email="test@example.com")
    await create_pessoa(session, pessoa)
    try:
        await create_pessoa(session, pessoa)
    except HTTPException as e:
        assert e.status_code == 409
        assert e.detail == "pessoa already exists"


async def test_get_pessoa(session: AsyncSession):
    pessoa = pessoaCreate(email="test@example.com")
    created_pessoa = await create_pessoa(session, pessoa)
    retrieved_pessoa = await get_pessoa(session, created_pessoa.id)
    assert retrieved_pessoa == created_pessoa


async def test_get_nonexistent_pessoa(session: AsyncSession):
    retrieved_pessoa = await get_pessoa(session, uuid7())
    assert retrieved_pessoa is None


async def test_get_pessoa_by_email(session: AsyncSession):
    pessoa = pessoaCreate(email="test@example.com")
    created_pessoa = await create_pessoa(session, pessoa)
    retrieved_pessoa = await get_pessoa_by_email(session, pessoa.email)
    assert retrieved_pessoa == created_pessoa


async def test_get_nonexistent_pessoa_by_email(session: AsyncSession):
    retrieved_pessoa = await get_pessoa_by_email(session, "nonexistent@example.com")
    assert retrieved_pessoa is None


async def test_update_pessoa(session: AsyncSession):
    created_pessoa = await create_pessoa(
        session, pessoaCreate(first_name="alice", email="test@example.com")
    )
    updated_pessoa = await update_pessoa(
        session, created_pessoa.id, pessoaUpdate(first_name="bob")
    )
    assert updated_pessoa.id == created_pessoa.id
    assert updated_pessoa.email == "test@example.com"
    assert updated_pessoa.first_name == "bob"


async def test_update_nonexistent_pessoa(session: AsyncSession):
    try:
        await update_pessoa(session, uuid7(), pessoaUpdate(first_name="alice"))
    except HTTPException as e:
        assert e.status_code == 404
        assert e.detail == "pessoa not found"


async def test_delete_pessoa(session: AsyncSession):
    created_pessoa = await create_pessoa(session, pessoaCreate(email="test@example.com"))
    deleted_count = await delete_pessoa(session, created_pessoa.id)
    assert deleted_count == 1
    retrieved_pessoa = await get_pessoa(session, created_pessoa.id)
    assert retrieved_pessoa is None


async def test_delete_nonexistent_pessoa(session: AsyncSession):
    deleted_count = await delete_pessoa(session, uuid7())
    assert deleted_count == 0
