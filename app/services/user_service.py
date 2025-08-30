from sqlalchemy.orm import Session
from app.models.user import User
from app.db import SessionLocal
from passlib.hash import bcrypt

def get_admin_count():
    db: Session = SessionLocal()
    try:
        return db.query(User).filter(User.statut == "admin").count()
    except Exception as e:
        print("Erreur dans get_admin_count:", e)
        return 0
    finally:
        db.close()

def create_user(name, email, password, statut):
    db: Session = SessionLocal()
    try:
        hashed_password = bcrypt.hash(password)
        new_user = User(
            username=name,
            email=email,
            password=hashed_password,
            statut=statut,
            is_admin=(statut == "admin")
        )
        db.add(new_user)
        db.commit()
    finally:
        db.close()