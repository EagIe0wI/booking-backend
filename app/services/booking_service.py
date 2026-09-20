from datetime import date, time
from app.models.booking import Booking, BookingStatus
from app.schemas.booking import BookingCreate
from fastapi import HTTPException

db_bookings: list[Booking] = []
_id_counter = 1

class BookingService:
    @classmethod
    def create_booking(cls, booking_data: BookingCreate) -> Booking:
        global _id_counter
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
            status=BookingStatus.ACTIVE
        )
        
        db_bookings.append(new_booking)
        _id_counter += 1
        return new_booking
