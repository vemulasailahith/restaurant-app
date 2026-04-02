from fastapi import APIRouter, Depends, Query, HTTPException
from database import db
import models, schemas
from bson import ObjectId

router = APIRouter()

def _to_response(restaurant: dict) -> schemas.RestaurantResponse:
    return schemas.RestaurantResponse(
        id=str(restaurant["_id"]),
        name=restaurant["name"],
        rating=restaurant["rating"],
        location=restaurant["location"],
        price_range=restaurant["price_range"],
        description=restaurant.get("description", "Popular student-friendly restaurant."),
        student_friendly=restaurant.get("price_range") == "₹",
        distance_km=restaurant.get("distance_km", 2.0),
        image_url=restaurant.get(
            "image_url",
            "https://images.unsplash.com/photo-1498654896293-37aacf113fd9",
        ),
        categories=restaurant.get("categories", ["Cafe"]),
        time_slots=restaurant.get("time_slots", ["12:00", "14:00", "18:00"]),
    )

@router.get("/restaurants", response_model=list[schemas.RestaurantResponse])
async def list_restaurants(
    search: str | None = Query(default=None),
    category: str | None = Query(default=None),
    budget: bool = Query(default=False),
):
    query = {}
    if search:
        query["name"] = {"$regex": search, "$options": "i"}
    if budget:
        query["price_range"] = "₹"
    if category:
        query["categories"] = category

    cursor = db.restaurants.find(query)
    restaurants = await cursor.to_list(length=100)
    return [_to_response(r) for r in restaurants]

@router.get("/restaurants/{restaurant_id}", response_model=schemas.RestaurantResponse)
async def get_restaurant(restaurant_id: str):
    if not ObjectId.is_valid(restaurant_id):
        raise HTTPException(status_code=400, detail="Invalid restaurant id format")
    
    restaurant = await db.restaurants.find_one({"_id": ObjectId(restaurant_id)})
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return _to_response(restaurant)
