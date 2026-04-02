from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import db
import models
from routes import auth, restaurants, bookings
import asyncio

app = FastAPI(title="TableNow API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def seed_restaurants():
    try:
        count = await db.restaurants.count_documents({})
        if count == 0:
            restaurants_data = [
                {
                    "name": "Campus Brew",
                    "rating": 4.5,
                    "location": "North Campus",
                    "price_range": "₹",
                    "description": "Cozy cafe with quick bites and study-friendly seating.",
                    "image_url": "https://images.unsplash.com/photo-1504753793650-d4a2b783c15e",
                    "categories": ["Cafe", "Veg"],
                    "time_slots": ["12:00", "13:00", "15:00", "17:00", "19:00"],
                    "distance_km": 1.2,
                },
                {
                    "name": "Spice Route",
                    "rating": 4.2,
                    "location": "Main Street",
                    "price_range": "₹₹",
                    "description": "Affordable Indian meals with student combos.",
                    "image_url": "https://images.unsplash.com/photo-1540189549336-e6e99c3679fe",
                    "categories": ["Indian"],
                    "time_slots": ["11:30", "13:30", "18:00", "20:00"],
                    "distance_km": 2.4,
                },
                {
                    "name": "Quick Bites",
                    "rating": 4.0,
                    "location": "Student Hub",
                    "price_range": "₹",
                    "description": "Fast food spot with quick service and budget options.",
                    "image_url": "https://images.unsplash.com/photo-1550547660-d9450f859349",
                    "categories": ["Fast Food"],
                    "time_slots": ["12:30", "14:00", "16:30", "19:30"],
                    "distance_km": 0.9,
                },
                {
                    "name": "Green Bowl",
                    "rating": 4.4,
                    "location": "City Center",
                    "price_range": "₹₹",
                    "description": "Healthy veg bowls and fresh juices.",
                    "image_url": "https://images.unsplash.com/photo-1498837167922-ddd27525d352",
                    "categories": ["Veg"],
                    "time_slots": ["10:30", "12:00", "14:00", "18:30"],
                    "distance_km": 3.1,
                },
            ]
            await db.restaurants.insert_many(restaurants_data)
    except Exception as e:
        print(f"Seeding error: {e}")

@app.on_event("startup")
async def on_startup():
    await seed_restaurants()

app.include_router(auth.router)
app.include_router(restaurants.router)
app.include_router(bookings.router)
