from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.database.connection import Base
from datetime import datetime

class Partner(Base):
    __tablename__ = "partners"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)  # "school", "hotel", "institution"
    contact_email = Column(String)
    contact_phone = Column(String)
    address = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)