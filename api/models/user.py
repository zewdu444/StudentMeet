from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import datetime

class Users(Base):
    __tablename__ = "users"
    university_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    role  = Column(String)
    hashed_password = Column(String)
    sessions = relationship("Sessions", back_populates="users", foreign_keys=["Sessions.created_by_teacher"])
    session_bookings = relationship("Session_bookings", back_populates="users", foreign_keys=["Session_bookings.booked_by_student"])
