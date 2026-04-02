import sqlite3
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME", "tablenow")
SQLITE_DB = "tablenow.db"

async def migrate():
    if not MONGODB_URI:
        print("Error: MONGODB_URI not found in .env")
        return

    print(f"Connecting to MongoDB Atlas...")
    client = AsyncIOMotorClient(MONGODB_URI)
    db = client[DATABASE_NAME]

    print(f"Connecting to SQLite: {SQLITE_DB}...")
    try:
        sqlite_conn = sqlite3.connect(SQLITE_DB)
        sqlite_conn.row_factory = sqlite3.Row
        cursor = sqlite_conn.cursor()
    except Exception as e:
        print(f"Error opening SQLite DB: {e}")
        return

    # 1. Migrate Users
    print("Migrating Users...")
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    user_id_map = {} # Map SQLite ID to Mongo ID string
    for r in users:
        user_doc = {"username": r["username"], "password": r["password"]}
        result = await db.users.insert_one(user_doc)
        user_id_map[r["id"]] = str(result.inserted_id)
    print(f"Migrated {len(users)} users.")

    # 2. Migrate Restaurants
    print("Migrating Restaurants...")
    cursor.execute("SELECT * FROM restaurants")
    restaurants = cursor.fetchall()
    restaurant_id_map = {}
    
    # Pre-defined metadata to enrich the migration
    restaurant_meta = {
        "Campus Brew": {
            "description": "Cozy cafe with quick bites and study-friendly seating.",
            "image_url": "https://images.unsplash.com/photo-1504753793650-d4a2b783c15e",
            "categories": ["Cafe", "Veg"],
            "time_slots": ["12:00", "13:00", "15:00", "17:00", "19:00"],
            "distance_km": 1.2,
        },
        "Spice Route": {
            "description": "Affordable Indian meals with student combos.",
            "image_url": "https://images.unsplash.com/photo-1540189549336-e6e99c3679fe",
            "categories": ["Indian"],
            "time_slots": ["11:30", "13:30", "18:00", "20:00"],
            "distance_km": 2.4,
        },
        "Quick Bites": {
            "description": "Fast food spot with quick service and budget options.",
            "image_url": "https://images.unsplash.com/photo-1550547660-d9450f859349",
            "categories": ["Fast Food"],
            "time_slots": ["12:30", "14:00", "16:30", "19:30"],
            "distance_km": 0.9,
        },
        "Green Bowl": {
            "description": "Healthy veg bowls and fresh juices.",
            "image_url": "https://images.unsplash.com/photo-1498837167922-ddd27525d352",
            "categories": ["Veg"],
            "time_slots": ["10:30", "12:00", "14:00", "18:30"],
            "distance_km": 3.1,
        },
    }

    for r in restaurants:
        meta = restaurant_meta.get(r["name"], {})
        res_doc = {
            "name": r["name"],
            "rating": r["rating"],
            "location": r["location"],
            "price_range": r["price_range"],
            "description": meta.get("description", ""),
            "image_url": meta.get("image_url", ""),
            "categories": meta.get("categories", []),
            "time_slots": meta.get("time_slots", []),
            "distance_km": meta.get("distance_km", 2.0)
        }
        result = await db.restaurants.insert_one(res_doc)
        restaurant_id_map[r["id"]] = str(result.inserted_id)
    print(f"Migrated {len(restaurants)} restaurants.")

    # 3. Migrate Bookings
    print("Migrating Bookings...")
    cursor.execute("SELECT * FROM bookings")
    bookings = cursor.fetchall()
    for r in bookings:
        booking_doc = {
            "user_id": user_id_map.get(r["user_id"]),
            "restaurant_id": restaurant_id_map.get(r["restaurant_id"]),
            "date": r["date"],
            "time": r["time"],
            "people": r["people"]
        }
        if booking_doc["user_id"] and booking_doc["restaurant_id"]:
            await db.bookings.insert_one(booking_doc)
    print(f"Migrated {len(bookings)} bookings.")

    sqlite_conn.close()
    print("Migration finished successfully!")

if __name__ == "__main__":
    asyncio.run(migrate())
