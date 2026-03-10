from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from datetime import datetime
from database import visits_collection, end_day_collection
from auth import verify_token
from utils import upload_to_cloudinary

router = APIRouter()


# ================= START VISIT =================

@router.post("/start")
async def start_visit(
        shop_name: str = Form(...),
        latitude: float = Form(...),
        longitude: float = Form(...),
        photo: UploadFile = File(...),
        user=Depends(verify_token)
):

    if user["role"] != "employee":
        raise HTTPException(status_code=403)

    # photo_content = await photo.read()
    photo_url = await upload_to_cloudinary(photo,
    user["user_id"],
    "visits")

    now = datetime.now()

    visit = {
        "employee_id": user["user_id"],
        "employee_name": user["email"],
        "shop_name": shop_name,
        "visit_photo": photo_url,
        "latitude": latitude,
        "longitude": longitude,
        "visit_date": now.strftime("%Y-%m-%d"),
        "visit_time": now.strftime("%H:%M:%S"),
        "created_at": now
    }

    result = visits_collection.insert_one(visit)

    return {
        "message": "Visit started",
        "visit_id": str(result.inserted_id)
    }


# ================= END DAY =================

@router.post("/end-day")
async def end_day(photo: UploadFile = File(...), user=Depends(verify_token)):

    # photo_content = await photo.read()
    photo_url = await upload_to_cloudinary(photo,
    user["user_id"],
    "end_day")

    now = datetime.now()

    end_day_collection.insert_one({
        "employee_id": user["user_id"],
        "employee_name": user["email"],
        "photo": photo_url,
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S")
    })

    return {"message": "Day ended successfully"}


# ================= GET VISITS =================

@router.get("/")
def get_visits(user=Depends(verify_token)):

    query = {}

    # employees can only see their own visits
    if user["role"] == "employee":
        query["employee_id"] = user["user_id"]

    visits = visits_collection.find(query).sort("created_at", -1)

    data = []

    for v in visits:
        data.append({
            "id": str(v["_id"]),
            "employee_id": v["employee_id"],
            "employee_name": v["employee_name"],
            "shop_name": v["shop_name"],
            "visit_photo": v["visit_photo"],
            "latitude": v["latitude"],
            "longitude": v["longitude"],
            "visit_date": v["visit_date"],
            "visit_time": v["visit_time"]
        })

    return {"visits": data}


# ================= GET END DAY PHOTOS (ADMIN) =================

@router.get("/end-day-photos")
def get_end_day_photos(user=Depends(verify_token)):

    if user["role"] != "admin":
        raise HTTPException(status_code=403)

    end_day_records = end_day_collection.find().sort("date", -1).sort("time", -1)

    data = []

    for r in end_day_records:
        data.append({
            "id": str(r["_id"]),
            "employee_id": r["employee_id"],
            "employee_name": r["employee_name"],
            "photo": r["photo"],
            "date": r["date"],
            "time": r["time"]
        })

    return {"end_day_records": data}
