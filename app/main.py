from fastapi import FastAPI
from app.routes.request import router as api_router

app = FastAPI(
    title="Weather AI API",
    version="1.0.0",
    description="Weather data + LLM-powered fact checking",
)

# Register all API routes
app.include_router(api_router)


@app.get("/", tags=["Health"])
def home() -> dict:
    """Root endpoint — health check."""
    return {"message": "Weather AI Backend is running!"}