from fastapi import FastAPI
from app.routes.weather import router as weather_router

app = FastAPI(
    title="Weather AI API",
    version="1.0.0"
)

app.include_router(weather_router)


@app.get("/")
def home():
    return {
        "message": "Weather AI Backend is running!"
    }