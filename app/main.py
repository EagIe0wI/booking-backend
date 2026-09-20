from fastapi import FastAPI
from app.schemas.booking import BookingCreate

app = FastAPI(title="Mise Restaurant Booking API")

@app.get("/")
async def root():
    return {"status": "working", "message": "Hello World from FastAPI"}

@app.post("/test-validation")
async def test_validation(booking: BookingCreate):
    return {"message": "Данные успешно прошли валидацию Pydantic!", "data": booking}
