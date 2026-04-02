import hashlib
import uuid
from fastapi import APIRouter, Depends, HTTPException, Header
from database import db
import models, schemas
from bson import ObjectId

router = APIRouter()
token_store = {}

def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

@router.post("/signup", response_model=schemas.UserResponse)
async def signup(payload: schemas.AuthRequest):
    if len(payload.password) < 4:
        raise HTTPException(status_code=400, detail="Password too short")
    existing = await db.users.find_one({"username": payload.username})
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")
    user_dict = {
        "username": payload.username,
        "password": _hash_password(payload.password)
    }
    result = await db.users.insert_one(user_dict)
    user_id = str(result.inserted_id)
    token = str(uuid.uuid4())
    token_store[token] = user_id
    return schemas.UserResponse(id=user_id, username=payload.username, token=token)

@router.post("/login", response_model=schemas.UserResponse)
async def login(payload: schemas.AuthRequest):
    user = await db.users.find_one({"username": payload.username})
    if not user or user["password"] != _hash_password(payload.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    user_id = str(user["_id"])
    token = str(uuid.uuid4())
    token_store[token] = user_id
    return schemas.UserResponse(id=user_id, username=user["username"], token=token)

@router.post("/google-auth", response_model=schemas.UserResponse)
async def google_auth(payload: schemas.GoogleAuthRequest):
    email = payload.email.strip().lower()
    if not email or "@" not in email:
        raise HTTPException(status_code=400, detail="Invalid Google email")
    user = await db.users.find_one({"username": email})
    if not user:
        user_dict = {
            "username": email,
            "password": _hash_password(f"google-{email}")
        }
        result = await db.users.insert_one(user_dict)
        user_id = str(result.inserted_id)
    else:
        user_id = str(user["_id"])
    token = str(uuid.uuid4())
    token_store[token] = user_id
    return schemas.UserResponse(id=user_id, username=email, token=token)

async def get_current_user_id(authorization: str | None = Header(default=None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")
    token = authorization.replace("Bearer ", "")
    user_id = token_store.get(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user_id
