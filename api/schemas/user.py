from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from enum import Enum
import datetime

class Role(str, Enum):
   student = "student"
   teacher = "teacher"

class UserCreate(BaseModel):
   first_name: str = Field(..., example="John")
   last_name:  str = Field(..., example="Doe")
   email: EmailStr = Field(..., example="zewdu444@gmail.com")
   role: Role = Field(..., example="student")
   hashed_password: str = Field(..., example="123456")

class UserUpdate(BaseModel):
  first_name: Optional[str] =Field(None,example="John")
  last_name: Optional[str] = Field(None, example="Doe")
  email: Optional[EmailStr] = Field(None, example="zewdu444@gmail.com")
  role: Optional[Role] = Field(None, example="student")

class User(BaseModel):
   university_id: int =Field(..., example=1)
   first_name: str = Field(..., example="John")
   last_name:  str = Field(..., example="Doe")
   email: EmailStr = Field(..., example="zewdu444@gmail.com")
   role: Role = Field(..., example="student")
