from fastapi import APIRouter

router = APIRouter()


@router.get("/weather")
def get_weather(city: str):
    return {
        "city": city,
        "temperature": 30,
        "condition": "Sunny"
    }