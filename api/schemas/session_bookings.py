from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from enum import Enum
import datetime
from .user import User
from .session import Session

class Session_bookingsCreate(BaseModel):
    session_id: int = Field(..., example=1)
    booked_by_student: int = Field(..., example=1)

class  Session_bookingsUpdate(BaseModel):
    session_id: Optional[int] = Field(None, example=1)
    booked_by_student: Optional[int] = Field(None, example=1)

class Session_bookings(BaseModel):
    booking_id: int = Field(..., example=1)
    session_id:  Session
    booked_by_student: User
