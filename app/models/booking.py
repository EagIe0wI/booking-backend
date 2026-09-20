from datetime import date, time
from dataclasses import dataclass
from enum import Enum

class BookingStatus(str, Enum):
    ACTIVE = "active"
    CANCELLED = "cancelled"

@dataclass
class Booking:
    id: int
    name: str
    phone: str
    booking_date: date
    booking_time: time
    guests: int
    status: BookingStatus = BookingStatus.ACTIVE
