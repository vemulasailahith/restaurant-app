from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Annotated
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")

class MongoBaseModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}

class User(MongoBaseModel):
    username: str
    password: str

class Restaurant(MongoBaseModel):
    name: str
    rating: float
    location: str
    price_range: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    categories: List[str] = []
    time_slots: List[str] = []
    distance_km: Optional[float] = None

class Booking(MongoBaseModel):
    user_id: str  # Store as string for easier matching
    restaurant_id: str
    date: str
    time: str
    people: int
