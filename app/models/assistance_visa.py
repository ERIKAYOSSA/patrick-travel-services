from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database.connection import Base
from datetime import datetime

class AssistanceVisa(Base):
    __tablename__ = "assistance_visas"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    country = Column(String, nullable=False)
    visa_type = Column(String, nullable=False)
    status = Column(String, default="pending")
    submitted_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")