from datetime import date, time, datetime
from app.models.booking import Booking, BookingStatus
from app.schemas.booking import BookingCreate
from fastapi import HTTPException

db_bookings: list[Booking] = []
_id_counter = 1

class BookingService:
    @classmethod
    def create_booking(cls, booking_data: BookingCreate) -> Booking:
        global _id_counter

        today = date.today()
        if booking_data.booking_date == today:
            current_time = datetime.now().time()
            if booking_data.booking_time < current_time:
                raise HTTPException(
                    status_code=400, 
                    detail="Нельзя забронировать столик на прошедшее время сегодняшнего дня"
                )

        for existing_booking in db_bookings:
            if existing_booking.status == BookingStatus.ACTIVE:
                if (existing_booking.booking_date == booking_data.booking_date and 
                    existing_booking.booking_time == booking_data.booking_time):
                    raise HTTPException(
                        status_code=409, 
                        detail="Слот на выбранные дату и время уже занят"
                    )
        
        new_booking = Booking(
            id=_id_counter,
            name=booking_data.name,
            phone=booking_data.phone,
            booking_date=booking_data.booking_date,
            booking_time=booking_data.booking_time,
            guests=booking_data.guests,
            status=BookingStatus.ACTIVE.value
        )
        
        db_bookings.append(new_booking)
        _id_counter += 1
        return new_booking

    @classmethod
    def get_bookings(cls, booking_date: date | None = None) -> list[Booking]:
        if booking_date is None:
            return db_bookings
            
        filtered_bookings = []
        for b in db_bookings:
            if b.booking_date == booking_date:
                filtered_bookings.append(b)
        return filtered_bookings

    @classmethod
    def get_booking_by_id(cls, booking_id: int) -> Booking:
        for b in db_bookings:
            if b.id == booking_id:
                return b
        raise HTTPException(status_code=404, detail="Booking not found")

    @classmethod
    def cancel_booking(cls, booking_id: int) -> Booking:
        booking = cls.get_booking_by_id(booking_id)
        
        booking.status = BookingStatus.CANCELLED.value
        return booking

