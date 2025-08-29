from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database.connection import Base
from datetime import datetime

class FlightBooking(Base):
    __tablename__ = "flight_bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    departure = Column(String, nullable=False)
    arrival = Column(String, nullable=False)
    travel_date = Column(DateTime)
    status = Column(String, default="pending")

    user = relationship("User")
    
    
    