from fastapi import FastAPI
from app.routes.request import router as api_router

app = FastAPI(
    title="Weather AI API",
    version="1.0.0",
    description="Weather data + LLM-powered fact checking",
)

app.include_router(api_router)


@app.get("/", tags=["Health"])
def home() -> dict:
    return {"message": "Weather AI API is running"}