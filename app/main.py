from fastapi import FastAPI

from app.services.llm_service import get_response
from app.routes.weather import router as weather_router

app = FastAPI(
    title="Weather AI API",
    version="1.0.0"
)

app.include_router(weather_router)


@app.get("/")
def home():
    return {
        "message": get_response()
    }