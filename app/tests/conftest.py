import pytest
from httpx import AsyncClient
from ..api import app


@pytest.fixture
async def httpx_test_client():
    async with AsyncClient(app=app, base_url="http://localhost:8080") as client:
        yield client
