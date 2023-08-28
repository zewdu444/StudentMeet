from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from enum import Enum
import datetime
from .user import User

class status(str, Enum):
     created  = "created"
     pending  = "pending"
     closed  = "closed"

class SessionCreate(BaseModel):
    created_by_teacher: int = Field(..., example=1)
    session_start: datetime.datetime = Field(..., example="2021-08-01 12:00:00")
    session_end: datetime.datetime = Field(..., example="2021-08-01 13:00:00")
    session_description: str = Field(..., example="This is a session")

class SessionUpdate(BaseModel):
    created_by_teacher: Optional[int] = Field(None, example=1)
    session_start: Optional[datetime.datetime] = Field(None, example="2021-08-01 12:00:00")
    session_end: Optional[datetime.datetime] = Field(None, example="2021-08-01 13:00:00")
    session_description: Optional[str] = Field(None, example="This is a session")

class Session(BaseModel):
    session_id: int = Field(..., example=1)
    created_by_teacher: User
    session_start: datetime.datetime = Field(..., example="2021-08-01 12:00:00")
    session_end: datetime.datetime = Field(..., example="2021-08-01 13:00:00")
    session_description: str = Field(..., example="This is a session")
    status: status = Field(..., example="created")
