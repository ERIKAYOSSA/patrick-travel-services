from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import SessionLocal
from app.models.user import User
from app.services.security import hash_password, verify_password
from app.services.auth import create_access_token

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register_user(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    statut: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        hashed_pw = hash_password(password)

        new_user = User(
            username=username,
            email=email,
            password=hashed_pw,
            statut=statut,
            is_admin=(statut == "admin")
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {"message": "Utilisateur enregistré", "id": new_user.id}

    except Exception as e:
        print("Erreur lors de l'enregistrement:", e)
        raise HTTPException(status_code=500, detail="Erreur interne")

@router.post("/login")
def login_user(
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.email == email).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Email incorrect")

    if not verify_password(password, db_user.password):
        raise HTTPException(status_code=400, detail="Mot de passe incorrect")

    token = create_access_token({"sub": db_user.email})
    return {"access_token": token, "token_type": "bearer"}