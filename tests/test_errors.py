import pytest
from httpx import AsyncClient
from datetime import date, timedelta, datetime

pytestmark = pytest.mark.asyncio

TODAY = date.today()
VALID_FUTURE_DATE = (TODAY + timedelta(days=5)).isoformat()
TOO_LATE_DATE = (TODAY + timedelta(days=95)).isoformat()
PAST_DATE = (TODAY - timedelta(days=1)).isoformat()

# --- 1. ТЕСТЫ НА ВАЛИДАЦИЮ ДАТ И ВРЕМЕНИ (422 и 400) ---

async def test_create_booking_date_past_error(ac: AsyncClient):
    """Ошибка 422: Попытка забронировать вчерашний день"""
    payload = {
        "name": "Игорь",
        "phone": "+79991234567",
        "booking_date": PAST_DATE,
        "booking_time": "18:00",
        "guests": 4
    }
    response = await ac.post("/bookings", json=payload)
    assert response.status_code == 422

async def test_create_booking_date_too_late_error(ac: AsyncClient):
    """Ошибка 422: Попытка забронировать дату дальше +90 дней"""
    payload = {
        "name": "Игорь",
        "phone": "+79991234567",
        "booking_date": TOO_LATE_DATE,
        "booking_time": "18:00",
        "guests": 4
    }
    response = await ac.post("/bookings", json=payload)
    assert response.status_code == 422

async def test_create_booking_past_time_today_error(ac: AsyncClient):
    """Ошибка 400: Попытка забронировать прошедший час внутри сегодняшнего дня"""
    current_hour = datetime.now().hour
    
    past_time = "12:00"
    if current_hour >= 13: 
        payload = {
            "name": "Игорь",
            "phone": "+79991234567",
            "booking_date": TODAY.isoformat(),
            "booking_time": past_time,
            "guests": 4
        }
        response = await ac.post("/bookings", json=payload)
        assert response.status_code == 400
        assert response.json()["detail"] == "Нельзя забронировать столик на прошедшее время сегодняшнего дня"

# --- 2. ТЕСТ НА БЛОКИРОВКУ СЛОТА (409 Conflict) ---

async def test_create_booking_conflict_409(ac: AsyncClient):
    """Ошибка 409: Попытка занять уже забронированное время"""
    payload = {
        "name": "Игорь",
        "phone": "+79991234567",
        "booking_date": VALID_FUTURE_DATE,
        "booking_time": "18:00",
        "guests": 4
    }
    
    res1 = await ac.post("/bookings", json=payload)
    assert res1.status_code == 201
    
    res2 = await ac.post("/bookings", json=payload)
    assert res2.status_code == 409
    assert res2.json()["detail"] == "Слот на выбранные дату и время уже занят"

# --- 3. ТЕСТ НА ОТСУТСТВИЕ РЕСУРСА (404 Not Found) ---

async def test_get_booking_not_found(ac: AsyncClient):
    """Ошибка 404: Запрос несуществующей брони"""
    response = await ac.get("/bookings/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Booking not found"

# --- 4. ТЕСТЫ НА ОГРАНИЧЕНИЯ PYDANTIC (422 Unprocessable Entity) ---

async def test_create_booking_name_too_short_error(ac: AsyncClient):
    """Ошибка 422: Имя слишком короткое (1 символ вместо минимум 2)"""
    payload = {
        "name": "И",  # Слишком короткое
        "phone": "+79991234567",
        "booking_date": VALID_FUTURE_DATE,
        "booking_time": "18:00",
        "guests": 4
    }
    response = await ac.post("/bookings", json=payload)
    assert response.status_code == 422

async def test_create_booking_invalid_phone_error(ac: AsyncClient):
    """Ошибка 422: В телефоне есть запрещенные буквы"""
    payload = {
        "name": "Игорь",
        "phone": "+79991234567abc",  # Буквы в телефоне
        "booking_date": VALID_FUTURE_DATE,
        "booking_time": "18:00",
        "guests": 4
    }
    response = await ac.post("/bookings", json=payload)
    assert response.status_code == 422

async def test_create_booking_too_many_guests_error(ac: AsyncClient):
    """Ошибка 422: Превышен лимит гостей (15 вместо максимум 12)"""
    payload = {
        "name": "Игорь",
        "phone": "+79991234567",
        "booking_date": VALID_FUTURE_DATE,
        "booking_time": "18:00",
        "guests": 15  # Больше 12
    }
    response = await ac.post("/bookings", json=payload)
    assert response.status_code == 422
