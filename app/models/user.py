from sqlalchemy import Column, Integer, String
from app.database.connection import Base
from sqlalchemy import Column, Integer, String, Boolean
from app.db import Base

is_admin = Column(Boolean, default=False)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)  # ✅ champ admin
    statut = Column(String, default="client")  # ✅ admin ou client
    
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    statut : str
    

