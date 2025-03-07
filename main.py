from fastapi import FastAPI, Query, HTTPException
from typing import Optional, List
from datetime import date, timedelta
from pydantic import BaseModel, Field
from uuid import uuid4, UUID
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешает все источники, в продакшене лучше указать конкретные домены
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


@app.get("/hotels", response_model=list[SHotel])
def get_hotels(
        location: str,
        date_from: date,
        date_to: date,
        quantity: int,
        stars: Optional[int] = Query(None, ge=1, le=5),
        has_spa: Optional[bool] = None
):
    """
    Получить список отелей по заданным параметрам.
    """
    # 1. Проверка корректности дат
    if date_from >= date_to:
        raise HTTPException(
            status_code=400, 
            detail="Дата выезда должна быть позже даты заезда"
        )
    
    # 2. Проверка наличия данных
    if not hotels:  # Если список отелей пуст
        return []
    
    # 3. Добавьте print для отладки
    print(f"Поиск отелей: {location}, {date_from} - {date_to}, гостей: {quantity}")
    
    # 4. Простая реализация без фильтрации (для тестирования)
    return hotels
    
    # 5. Полная версия с фильтрацией (раскомментируйте, когда базовая версия заработает)
    # filtered_hotels = []
    # for hotel in hotels:
    #     # Проверка локации (регистр не важен)
    #     if location.lower() not in hotel.location.lower():
    #         continue
    #     
    #     # Проверка количества звезд
    #     if stars is not None and hotel.stars != stars:
    #         continue
    #     
    #     # Проверка наличия спа
    #     if has_spa is not None and hotel.has_spa != has_spa:
    #         continue
    #     
    #     filtered_hotels.append(hotel)
    # 
    # return filtered_hotels


class SBooking(BaseModel):
    room_id: int
    date_from: date
    date_to: date


@app.post("/bookings")
def add_booking(booking: SBooking):
    return {"status": "success", "booking": booking.model_dump()}

bookings = [
    # После создания бронирования появится такая структура
    SBooking(
        id=uuid4(),           # ID бронирования
        hotel_id=1,    # ID отеля
        room_id=101,          # номер комнаты
        date_from=date.today(),
        date_to=date.today() + timedelta(days=1),
        price=5000,           # цена за ночь
        total_days=1,         # общее количество дней
        total_cost=5000       # общая стоимость
    )
]

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
