from fastapi import APIRouter, Depends
from database import users_collection, visits_collection
from auth import verify_token
from datetime import datetime

router = APIRouter()


@router.get("/employees")
def get_employees(user=Depends(verify_token)):

    employees = users_collection.find({"role": "employee"})

    data = []

    for e in employees:
        data.append({

            "id": str(e["_id"]),
            "email": e["email"],
            "name": e["name"]
        })

    return {"employees": data}


@router.get("/dashboard")
def dashboard(user=Depends(verify_token)):

    today = datetime.now().strftime("%Y-%m-%d")

    total_visits_today = visits_collection.count_documents({"visit_date": today})

    total_employees = users_collection.count_documents({"role": "employee"})

    active_employees = len(visits_collection.distinct("employee_id", {"visit_date": today}))

    attendance = 0

    if total_employees > 0:
        attendance = (active_employees / total_employees) * 100

    return {

        "total_visits_today": total_visits_today,
        "total_employees": total_employees,
        "active_employees": active_employees,
        "attendance_percentage": round(attendance, 2)
    }