import pytest
import asyncio
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.services.booking_service import db_bookings, _id_counter

@pytest.fixture(autouse=True)
def clean_database():
    global _id_counter
    db_bookings.clear()
    _id_counter = 1

@pytest.fixture
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app), 
        base_url="http://testserver"
    ) as client:
        yield client
