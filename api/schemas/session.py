from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from enum import Enum
import datetime
from .user import User

class Status(str, Enum):
     created = "created"
     pending = "pending"
     cancel = "cancel"
     closed = "closed"

class SessionCreate(BaseModel):
    session_start: datetime.datetime = Field(..., example="2021-08-01 12:00:00")
    session_end: datetime.datetime = Field(..., example="2021-08-01 13:00:00")
    session_description: str = Field(..., example="This is a session")

class SessionUpdate(BaseModel):
    session_start: Optional[datetime.datetime] = Field(None, example="2021-08-01 12:00:00")
    session_end: Optional[datetime.datetime] = Field(None, example="2021-08-01 13:00:00")
    session_description: Optional[str] = Field(None, example="This is a session")
    status: Optional[Status] = Field(None, example="created")

class Session(BaseModel):
    session_id: int = Field(..., example=1)
    created_by_teacher: User
    session_start: datetime.datetime = Field(..., example="2021-08-01 12:00:00")
    session_end: datetime.datetime = Field(..., example="2021-08-01 13:00:00")
    session_description: str = Field(..., example="This is a session")
    status: Status = Field(..., example="created")
