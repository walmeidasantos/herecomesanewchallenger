from httpx import AsyncClient
from app.main import app
from uuid import UUID
import pytest
import asyncio

URL = "http://localhost:9999"


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@pytest.mark.asyncio(scope="session")
async def test_create_person():
    data = {
        "apelido": "test_person",
        "nome": "test_person",
        "nascimento": "1992-05-23",
        "stack": ["Python", "FastAPI"],
    }
    async with AsyncClient(app=app, base_url=URL) as ac:
        response = await ac.post("/pessoas", json=data)
    assert response.status_code == 201
    location = response.headers.get("Location")
    assert location is not None
    id_str = location.split("/")[-1]
    assert UUID(id_str)  # Validate it's a UUID


@pytest.mark.asyncio(scope="session")
async def test_find_by_term():
    term = "Python"
    async with AsyncClient(app=app, base_url=URL) as ac:
        response = await ac.get(f"/pessoas?t={term}")
    assert response.status_code == 200
    people = response.json()
    assert isinstance(people, list)


@pytest.mark.asyncio(scope="session")
async def test_get_count():
    async with AsyncClient(app=app, base_url=URL) as ac:
        response = await ac.get("/contagem-pessoas")
    assert response.status_code == 200
    count = response.text
    assert len(count) >= 1
