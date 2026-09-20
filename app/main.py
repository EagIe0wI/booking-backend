from datetime import date
from fastapi import FastAPI, Query
from pydantic import BaseModel, Field
from app.schemas.booking import BookingCreate, BookingOut
from app.services.booking_service import BookingService

app = FastAPI(title="Mise Restaurant Booking API")

class ErrorResponse(BaseModel):
    detail: str = Field(..., examples=["Описание ошибки со стороны сервера"])

# Создание брони (POST)
@app.post(
    "/test/bookings", 
    response_model=BookingOut, 
    status_code=201,
    responses={
        409: {"model": ErrorResponse, "description": "Слот на выбранные дату/время уже занят"}
    }
)
async def test_create(booking: BookingCreate):
    return BookingService.create_booking(booking)

# Получение списка с фильтром (GET)
@app.get(
    "/test/bookings", 
    response_model=list[BookingOut],
    responses={
        422: {"description": "Невалидный формат переданной даты"}
    }
)
async def test_get_all(date: date | None = Query(None, description="Фильтр по дате в формате YYYY-MM-DD")):
    return BookingService.get_bookings(date)

# Получение одной брони по ID (GET)
@app.get(
    "/test/bookings/{booking_id}", 
    response_model=BookingOut,
    responses={
        404: {"model": ErrorResponse, "description": "Бронь с указанным ID не найдена"}
    }
)
async def test_get_one(booking_id: int):
    return BookingService.get_booking_by_id(booking_id)

# Отмена брони (DELETE)
@app.delete(
    "/test/bookings/{booking_id}", 
    response_model=BookingOut,
    responses={
        404: {"model": ErrorResponse, "description": "Бронь с указанным ID не найдена для отмены"}
    }
)
async def test_cancel(booking_id: int):
    return BookingService.cancel_booking(booking_id)
