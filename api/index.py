from fastapi import FastAPI, Query, HTTPException
from typing import Optional, List
from datetime import date, timedelta
from pydantic import BaseModel, Field
from uuid import uuid4, UUID
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SHotel(BaseModel):
    id: UUID
    name: str
    location: str
    stars: int = Field(ge=1, le=5)
    rooms: List[int]
    has_spa: bool

# Тестовые данные
hotels = [
    SHotel(
        id=uuid4(),
        name="Cosmos Hotel",
        location="Москва",
        stars=5,
        rooms=[1, 2, 3, 4],
        has_spa=True
    ),
    SHotel(
        id=uuid4(),
        name="Grand Hotel",
        location="Санкт-Петербург",
        stars=4,
        rooms=[10, 11, 12],
        has_spa=False
    ),
    SHotel(
        id=uuid4(),
        name="Hilton Moscow",
        location="Москва",
        stars=5,
        rooms=[20, 21, 22, 23],
        has_spa=True
    )
]

@app.get("/api")
async def root():
    return {"message": "API работает!"}

@app.get("/api/hotels", response_model=list[SHotel])
async def get_hotels(
        location: str,
        date_from: date,
        date_to: date,
        quantity: int,
        stars: Optional[int] = Query(None, ge=1, le=5),
        has_spa: Optional[bool] = None
):
    if date_from >= date_to:
        raise HTTPException(
            status_code=400,
            detail="Дата выезда должна быть позже даты заезда"
        )
    
    filtered_hotels = []
    for hotel in hotels:
        if location.lower() in hotel.location.lower():
            if stars is None or hotel.stars == stars:
                if has_spa is None or hotel.has_spa == has_spa:
                    filtered_hotels.append(hotel)
    
    return filtered_hotels 