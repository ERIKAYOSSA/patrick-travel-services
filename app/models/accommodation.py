from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database.connection import Base
from datetime import datetime

class Accommodation(Base):
    __tablename__ = "accommodations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    location = Column(String, nullable=False)
    check_in = Column(DateTime)
    check_out = Column(DateTime)
    status = Column(String, default="pending")

    user = relationship("User")
    
partner_id = Column(Integer, ForeignKey("partners.id"), nullable=True)
partner = relationship("Partner")