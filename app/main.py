from fastapi import FastAPI
from app.api.bookings import router as bookings_router

app = FastAPI(title="Mise Restaurant Booking API", version="1.0.0")

app.include_router(bookings_router)

@app.get("/")
async def root():
    return {
        "status": "working", 
        "message": "Mise Restaurant Booking API ис успешно запущено и готово к работе."
    }
