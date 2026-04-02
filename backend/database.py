import os
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    mongodb_uri: str = "mongodb://localhost:27017"
    database_name: str = "tablenow"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()

client = AsyncIOMotorClient(settings.mongodb_uri)
db = client[settings.database_name]

async def get_db():
    # In MongoDB with Motor, we don't need a generator like SQLAlchemy's get_db
    # But we can provide it for consistency if needed, or just import 'db' directly.
    return db
