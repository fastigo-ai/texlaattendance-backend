import hashlib
from fastapi import APIRouter, HTTPException,Depends
from models import LoginRequest
from database import users_collection
from auth import create_token
from bson import ObjectId
from auth import verify_token

router = APIRouter()

@router.post("/login")
def login(request: LoginRequest):

    user = users_collection.find_one({
        "email": request.email
    })

    if not user:
        print("User not found")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    hashed_password = hashlib.sha256(request.password.encode()).hexdigest()

    print("Entered password:", request.password)
    print("Generated hash:", hashed_password)
    print("DB password:", user["password"])

    if user["password"] != hashed_password:
        print("Password mismatch")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token(str(user["_id"]), user["email"], user["role"])

    return {
        "token": token,
        "user": {
            "id": str(user["_id"]),
            "email": user["email"],
            "name": user["name"],
            "role": user["role"]
        }
    }
@router.get("/me")
def get_current_user(user=Depends(verify_token)):

    from bson import ObjectId

    db_user = users_collection.find_one({
        "_id": ObjectId(user["user_id"])
    })

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": str(db_user["_id"]),
        "email": db_user["email"],
        "name": db_user["name"],
        "role": db_user["role"]
    }