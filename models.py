from pydantic import BaseModel, EmailStr
from typing import Optional

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    token: str
    user: dict


class VisitCreate(BaseModel):
    shop_name: str
    latitude: float
    longitude: float


class LeaveRequest(BaseModel):
    leave_date: str
    reason: Optional[str] = None


class LeaveUpdate(BaseModel):
    leave_id: str
    status: str