from datetime import date
from fastapi import FastAPI
from app.schemas.booking import BookingCreate
from app.services.booking_service import BookingService

app = FastAPI(title="Mise Restaurant Booking API")

@app.get("/")
async def root():
    return {"status": "working", "message": "Hello World from FastAPI"}

# Тест создания брони (POST)
@app.post("/test/bookings")
async def test_create(booking: BookingCreate):
    return BookingService.create_booking(booking)

# Тест получения списка с фильтром (GET)
@app.get("/test/bookings")
async def test_get_all(date: date | None = None):
    return BookingService.get_bookings(date)

# Тест получения одной брони по ID (GET)
@app.get("/test/bookings/{booking_id}")
async def test_get_one(booking_id: int):
    return BookingService.get_booking_by_id(booking_id)

# Тест отмены брони (DELETE)
@app.delete("/test/bookings/{booking_id}")
async def test_cancel(booking_id: int):
    return BookingService.cancel_booking(booking_id)