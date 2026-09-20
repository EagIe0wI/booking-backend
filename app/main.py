from fastapi import FastAPI

app = FastAPI(title="Mise Restaurant Booking API")

@app.get("/")
async def root():
    return {"status": "working", "message": "Hello World from FastAPI"}
