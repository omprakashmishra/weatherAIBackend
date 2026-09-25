from fastapi import FastAPI
from app.routes.request import router as api_router
from app.services.llm_service import fact_check

app = FastAPI(
    title="Weather AI API",
    version="1.0.0",
    description="Weather data + LLM-powered fact checking",
)

# Register all API routes (weather, fact-check, etc.)
app.include_router(api_router)


@app.get("/", tags=["Health"])
def home() -> dict:
    """Root endpoint — quick LLM sanity check."""
    return {"message": get_response()}