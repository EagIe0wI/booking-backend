import pytest
from httpx import AsyncClient
from datetime import date, timedelta

pytestmark = pytest.mark.asyncio

TODAY = date.today()
VALID_FUTURE_DATE = (TODAY + timedelta(days=5)).isoformat()
TOO_LATE_DATE = (TODAY + timedelta(days=95)).isoformat()
PAST_DATE = (TODAY - timedelta(days=1)).isoformat()

async def test_create_booking_success(ac: AsyncClient):
    payload = {
        "name": "Игорь",
        "phone": "+79991234567",
        "booking_date": VALID_FUTURE_DATE,
        "booking_time": "18:00",
        "guests": 4
    }
    
    response = await ac.post("/bookings", json=payload)
    assert response.status_code == 201
    
    data = response.json()
    assert data["id"] == 1
    assert data["status"] == "active"
    assert data["name"] == "Игорь"

async def test_get_bookings_success(ac: AsyncClient):
    payload = {
        "name": "Анна",
        "phone": "89997654321",
        "booking_date": VALID_FUTURE_DATE,
        "booking_time": "19:00",
        "guests": 2
    }
    await ac.post("/bookings", json=payload)
    
    response = await ac.get("/bookings")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == "Анна"

async def test_get_one_booking_success(ac: AsyncClient):
    payload = {
        "name": "Игорь",
        "phone": "+79991234567",
        "booking_date": VALID_FUTURE_DATE,
        "booking_time": "18:00",
        "guests": 4
    }
    await ac.post("/bookings", json=payload)
    
    response = await ac.get("/bookings/1")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Игорь"

async def test_cancel_booking_success(ac: AsyncClient):
    payload = {
        "name": "Игорь",
        "phone": "+79991234567",
        "booking_date": VALID_FUTURE_DATE,
        "booking_time": "18:00",
        "guests": 4
    }
    await ac.post("/bookings", json=payload)
    
    response = await ac.delete("/bookings/1")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == 1
    assert data["status"] == "cancelled"
