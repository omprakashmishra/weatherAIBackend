from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.llm_service import fact_check

router = APIRouter()


class FactCheckRequest(BaseModel):
    claim: str = Field(..., min_length=3, description="Statement to fact-check")


@router.get("/weather")
def get_weather(city: str):
    return {
        "city": city,
        "temperature": 30,
        "condition": "Sunny"
    }


@router.post("/fact-check")
def fact_check_endpoint(claim: str):
    try:
        result = fact_check(claim)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))