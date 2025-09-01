from sqlalchemy.orm import Session
from app.models.user import User
from app.db import SessionLocal  # Assure-toi que SessionLocal est bien défini dans db.py
from passlib.hash import bcrypt
from app.db import get_db
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

async def get_user_by_email(email: str):
    db: Session = next(get_db())
    return db.query(User).filter(User.email == email).first()

def get_admin_count():
    db: Session = SessionLocal()
    try:
        return db.query(User).filter(User.statut == "admin").count()
    except Exception as e:
        print("Erreur dans get_admin_count:", e)
        return 0
    finally:
        db.close()

def create_user(username: str, email: str, password: str, statut: str):
    db: Session = SessionLocal()
    try:
        hashed_password = bcrypt.hash(password)

        new_user = User(
            username=username,
            email=email,
            password=hashed_password,
            statut=statut,
            is_admin=(statut == "admin")
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

    except Exception as e:
        print("Erreur dans create_user:", e)
        raise

    finally:
        db.close()
