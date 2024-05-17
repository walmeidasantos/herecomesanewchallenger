import pytest
from app.database import init_db, delete_pessoas


@pytest.fixture(scope="session", autouse=True)
async def setup_db():
    await init_db()
    await delete_pessoas()
