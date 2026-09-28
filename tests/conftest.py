import pytest
import pytest_asyncio
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from app.main import app
import app.services.booking_service as service

@pytest.fixture(autouse=True)
def clean_database():
    service.db_bookings.clear()
    service._id_counter = 1

@pytest_asyncio.fixture(loop_scope="function")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app), 
        base_url="http://testserver"
    ) as client:
        yield client
