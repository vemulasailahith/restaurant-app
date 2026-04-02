from pydantic import BaseModel, Field
from typing import List, Optional

class AuthRequest(BaseModel):
    username: str
    password: str

class GoogleAuthRequest(BaseModel):
    email: str
    name: str | None = None

class UserResponse(BaseModel):
    id: str
    username: str
    token: str

class RestaurantResponse(BaseModel):
    id: str
    name: str
    rating: float
    location: str
    price_range: str
    description: str
    student_friendly: bool
    distance_km: float
    image_url: str
    categories: List[str]
    time_slots: List[str]

class BookingRequest(BaseModel):
    restaurant_id: str
    date: str
    time: str
    people: int

class BookingResponse(BaseModel):
    id: str
    restaurant_id: str
    restaurant_name: str
    date: str
    time: str
    people: int
