from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database.connection import Base
from datetime import datetime

class SchoolAdmission(Base):
    __tablename__ = "school_admissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    school_name = Column(String, nullable=False)
    program = Column(String, nullable=False)
    country = Column(String, nullable=False)
    status = Column(String, default="pending")
    submitted_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
    
partner_id = Column(Integer, ForeignKey("partners.id"), nullable=True)
partner = relationship("Partner")