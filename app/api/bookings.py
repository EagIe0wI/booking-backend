from datetime import date
from fastapi import APIRouter, Query
from pydantic import BaseModel, Field
from app.schemas.booking import BookingCreate, BookingOut
from app.services.booking_service import BookingService

router = APIRouter(prefix="/bookings", tags=["Bookings"])

class NotFoundResponse(BaseModel):
    detail: str = Field(..., examples=["Booking not found"])

class ConflictResponse(BaseModel):
    detail: str = Field(..., examples=["Slot is already booked"])

@router.post(
    "", 
    response_model=BookingOut, 
    status_code=201,
    responses={
        409: {"model": ConflictResponse, "description": "Слот на выбранные дату/время уже занят"}
    }
)
async def create_booking(booking: BookingCreate):
    return BookingService.create_booking(booking)

@router.get(
    "", 
    response_model=list[BookingOut],
    responses={
        422: {"description": "Невалидный формат переданной даты"}
    }
)
async def get_all_bookings(date: date | None = Query(None, description="Фильтр по дате в формате YYYY-MM-DD")):
    return BookingService.get_bookings(date)

@router.get(
    "/{booking_id}",
    response_model=BookingOut,
    responses={
        404: {"model": NotFoundResponse, "description": "Бронь с указанным ID не найдена"}
    }
)
async def get_one_booking(booking_id: int):
    return BookingService.get_booking_by_id(booking_id)

@router.delete(
    "/{booking_id}", 
    response_model=BookingOut,
    responses={
        404: {"model": NotFoundResponse, "description": "Бронь с указанным ID не найдена для отмены"}
    }
)
async def cancel_booking(booking_id: int):
    return BookingService.cancel_booking(booking_id)
