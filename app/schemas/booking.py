import re
from datetime import date, time
from pydantic import BaseModel, Field, field_validator
from typing import Literal

class BookingCreate(BaseModel):
    name: str = Field(
        ..., 
        min_length=2, 
        examples=["Игорь"],
        description="Имя гостя. Минимум 2 символа, только буквы, пробелы, дефис."
    )
    phone: str = Field(
        ..., 
        examples=["+79991234567"],
        description="Российский формат: +7XXXXXXXXXX или 8XXXXXXXXXX"
    )
    booking_date: date = Field(
        ..., 
        examples=["2026-09-30"],
        description="Дата бронирования. Не раньше сегодняшнего дня и не позднее +90 дней."
    )
    booking_time: time = Field(
        ..., 
        examples=["18:00"],
        description="Время бронирования. Только слоты с шагом в 1 час (12:00-22:00)."
    )
    guests: int = Field(
        ..., 
        ge=1, 
        le=12, 
        examples=[4],
        description="Количество гостей от 1 до 12."
    )

    @field_validator('name')
    @classmethod
    def validate_name(cls, value: str) -> str:
        if not re.match(r"^[а-яа-яa-z\s-]+$", value, re.IGNORECASE):
            raise ValueError("Имя должно содержать только буквы, пробелы или дефис")
        return value

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, value: str) -> str:
        digits = re.sub(r'\D', '', value)
        
        if len(digits) == 11 and digits[0] in ('7', '8'):
            return value
            
        raise ValueError('Введите корректный номер: +7 или 8, 10 цифр после кода')

    @field_validator('booking_date')
    @classmethod
    def validate_booking_date(cls, value: date) -> date:
        today = date.today()
        from datetime import timedelta
        max_date = today + timedelta(days=90)
        
        if value < today:
            raise ValueError("Дата бронирования не может быть в прошлом")
        if value > max_date:
            raise ValueError("Бронирование возможно максимум на 90 дней вперед")
            
        return value

    @field_validator('booking_time')
    @classmethod
    def validate_booking_time(cls, value: time) -> time:
        from datetime import time as dt_time
        if value < dt_time(12, 0) or value > dt_time(22, 0):
            raise ValueError("Бронирование возможно только с 12:00 до 22:00")
        
        if value.minute != 0 or value.second != 0 or value.microsecond != 0:
            raise ValueError("Время бронирования должно быть кратно часу (например, 13:00, 18:00)")
            
        return value

class BookingOut(BookingCreate):
    id: int = Field(..., examples=[1], description="Уникальный ID брони")
    status: Literal['active', 'cancelled'] = Field(
        ..., 
        examples=["active"], 
        description="Текущий статус бронирования: active (активно) или cancelled (отменено)"
    )
