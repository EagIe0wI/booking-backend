from fastapi import FastAPI, Request
from app.api.bookings import router as bookings_router

app = FastAPI(title="Mise Restaurant Booking API", version="1.0.0")

app.include_router(bookings_router)

@app.get("/")
async def root(request: Request):
    base_url = str(request.base_url)
    return {
        "status": "working", 
        "message": "Mise Restaurant Booking API успешно запущено и готово к работе.",
        "documentation": f"{base_url}docs"
    }