from sqlalchemy.orm import Session
from app.models.user import User
from app.db import get_db  # ou database.py selon ta config

def get_admin_count():
    db: Session = next(get_db())
    return db.query(User).filter(User.statut == "admin").count()