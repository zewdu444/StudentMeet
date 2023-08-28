from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
import datetime
class Sessions(Base):
    __tablename__ = "sessions"
    session_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_by_teacher = Column(Integer, ForeignKey("users.university_id"))
    session_start = Column(DateTime)
    session_end = Column(DateTime)
    session_description = Column(String)
    created_by=relationship("Users", back_populates="sessions_created", foreign_keys=[created_by_teacher])
    session_bookings = relationship("Session_bookings", back_populates="sessions")
