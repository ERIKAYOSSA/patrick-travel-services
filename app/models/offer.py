from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database.connection import Base
from datetime import datetime

class Offer(Base):
    __tablename__ = "offers"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    type = Column(String, nullable=False)  # "bourse", "logement", "admission"
    description = Column(Text)
    conditions = Column(Text)
    partner_id = Column(Integer, ForeignKey("partners.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    partner = relationship("Partner")