from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import SessionLocal
from app.models.user import User
from app.services.security import hash_password
from fastapi import HTTPException
from app.services.security import verify_password
from app.services.auth import create_access_token
from app.schemas.user_schema import UserCreate  # ✅

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(
    username=user.username,
    email=user.email,
    password=hash_password(user.password)  # 🔒 mot de passe chiffré
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Utilisateur enregistré", "id": new_user.id}


@router.post("/login")
def login_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Email incorrect")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Mot de passe incorrect")

    token = create_access_token({"sub": db_user.email})
    return {"access_token": token, "token_type": "bearer"}