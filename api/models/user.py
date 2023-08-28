from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import datetime
from .session import Sessions
from .session_booking import Session_bookings
class Users(Base):
    __tablename__ = "users"
    university_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    role  = Column(String)
    hashed_password = Column(String)
    sessions_created = relationship("Sessions", back_populates="created_by")
    session_bookings = relationship("Session_bookings", back_populates="booked_by")
