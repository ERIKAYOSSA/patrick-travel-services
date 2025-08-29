from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.database.connection import Base
from datetime import datetime

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    request_type = Column(String, nullable=False)  # "visa", "bourse", "admission", etc.
    request_id = Column(Integer, nullable=True)    # ID de la demande liée
    filename = Column(String, nullable=False)
    file_url = Column(String, nullable=False)
    status = Column(String, default="pending")     # "pending", "validated", "rejected"
    is_conform = Column(Boolean, default=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")