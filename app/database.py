from app.models import User
from sqlalchemy.orm import Session
from app.db import get_db

async def get_admin_count():
    db: Session = get_db()
    return db.query(User).filter(User.statut == "admin").count()

from sqlalchemy.orm import Session
from app.models import User
from app.db import get_db  # Assure-toi que get_db() est bien défini

def get_admin_count():
    db: Session = next(get_db())
    return db.query(User).filter(User.statut == "admin").count()

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()