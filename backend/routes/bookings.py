from fastapi import APIRouter, Depends, HTTPException
from database import db
import models, schemas
from routes.auth import get_current_user_id
from bson import ObjectId

router = APIRouter()

@router.post("/book", response_model=schemas.BookingResponse)
async def create_booking(
    payload: schemas.BookingRequest,
    user_id: str = Depends(get_current_user_id),
):
    if payload.people < 1:
        raise HTTPException(status_code=400, detail="People must be at least 1")
    
    if not ObjectId.is_valid(payload.restaurant_id):
        raise HTTPException(status_code=400, detail="Invalid restaurant id")
        
    restaurant = await db.restaurants.find_one({"_id": ObjectId(payload.restaurant_id)})
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
        
    existing = await db.bookings.find_one({
        "restaurant_id": payload.restaurant_id,
        "date": payload.date,
        "time": payload.time,
    })
    
    if existing:
        raise HTTPException(status_code=400, detail="Time slot already booked")
        
    booking_dict = {
        "user_id": user_id,
        "restaurant_id": payload.restaurant_id,
        "date": payload.date,
        "time": payload.time,
        "people": payload.people,
    }
    
    result = await db.bookings.insert_one(booking_dict)
    booking_id = str(result.inserted_id)
    
    return schemas.BookingResponse(
        id=booking_id,
        restaurant_id=payload.restaurant_id,
        restaurant_name=restaurant["name"],
        date=payload.date,
        time=payload.time,
        people=payload.people,
    )

@router.get("/my-bookings", response_model=list[schemas.BookingResponse])
async def list_bookings(
    user_id: str = Depends(get_current_user_id),
):
    cursor = db.bookings.find({"user_id": user_id}).sort("_id", -1)
    bookings = await cursor.to_list(length=100)
    
    results = []
    for b in bookings:
        restaurant = await db.restaurants.find_one({"_id": ObjectId(b["restaurant_id"])})
        results.append(
            schemas.BookingResponse(
                id=str(b["_id"]),
                restaurant_id=b["restaurant_id"],
                restaurant_name=restaurant["name"] if restaurant else "Restaurant",
                date=b["date"],
                time=b["time"],
                people=b["people"],
            )
        )
    return results

@router.delete("/book/{booking_id}")
async def cancel_booking(
    booking_id: str,
    user_id: str = Depends(get_current_user_id),
):
    if not ObjectId.is_valid(booking_id):
        raise HTTPException(status_code=400, detail="Invalid booking id")
        
    result = await db.bookings.delete_one({
        "_id": ObjectId(booking_id),
        "user_id": user_id
    })
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Booking not found")
        
    return {"status": "cancelled"}
