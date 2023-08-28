from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
import datetime

class Session_bookings(Base):
    __tablename__ = "session_bookings"
    booking_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey("sessions.session_id"))
    booked_by_student = Column(Integer, ForeignKey("users.university_id"))
    users = relationship("Users", back_populates="session_bookings")
    sessions = relationship("Sessions", back_populates="session_bookings")
