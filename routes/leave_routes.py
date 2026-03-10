from fastapi import APIRouter, Depends, HTTPException
from models import LeaveRequest, LeaveUpdate
from database import leave_collection
from auth import verify_token
from datetime import datetime
from bson import ObjectId

router = APIRouter()


# Employee requests leave
@router.post("/request")
def request_leave(request: LeaveRequest, user=Depends(verify_token)):

    if user["role"] != "employee":
        raise HTTPException(status_code=403, detail="Only employees can request leave")

    leave = {
        "employee_id": user["user_id"],
        "employee_name": user["email"],
        "leave_date": request.leave_date,
        "reason": request.reason,
        "status": "pending",
        "created_at": datetime.now()
    }

    result = leave_collection.insert_one(leave)

    return {
        "message": "Leave request submitted",
        "leave_id": str(result.inserted_id)
    }


# Admin approves or rejects leave
@router.put("/update")
def update_leave(request: LeaveUpdate, user=Depends(verify_token)):

    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    leave = leave_collection.find_one({"_id": ObjectId(request.leave_id)})

    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")

    leave_collection.update_one(
        {"_id": ObjectId(request.leave_id)},
        {"$set": {"status": request.status}}
    )

    return {"message": f"Leave {request.status}"}


# Admin can see all leave requests
@router.get("/all")
def get_all_leaves(user=Depends(verify_token)):

    if user["role"] != "admin":
        raise HTTPException(status_code=403)

    leaves = leave_collection.find()

    data = []

    for leave in leaves:
        data.append({
            "id": str(leave["_id"]),
            "employee_id": leave["employee_id"],
            "employee_name": leave["employee_name"],
            "leave_date": leave["leave_date"],
            "reason": leave.get("reason"),
            "status": leave["status"],
            "created_at": leave["created_at"]
        })

    return {"leave_requests": data}


# Get leave requests for specific employee
@router.get("/user/{employee_id}")
def get_user_leaves(employee_id: str, user=Depends(verify_token)):

    # employees can only see their own leave
    if user["role"] == "employee" and user["user_id"] != employee_id:
        raise HTTPException(status_code=403)

    leaves = leave_collection.find({"employee_id": employee_id})

    data = []

    for leave in leaves:
        data.append({
            "id": str(leave["_id"]),
            "employee_id": leave["employee_id"],
            "employee_name": leave["employee_name"],
            "leave_date": leave["leave_date"],
            "reason": leave.get("reason"),
            "status": leave["status"],
            "created_at": leave["created_at"]
        })

    return {"leave_requests": data}