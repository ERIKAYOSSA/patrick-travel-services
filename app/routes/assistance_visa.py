from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import SessionLocal
from app.models.assistance_visa import AssistanceVisa
from app.models.user import User  # si tu veux lier à l'utilisateur
from app.schemas.assistance_visa import AssistanceVisaCreate # à créer ensuite
from app.services.auth import get_current_user


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/assistance-visa")
def submit_assistance_visa(request: AssistanceVisaCreate, db: Session = Depends(get_db)):
    new_request = AssistanceVisa(
        user_id=request.user_id,
        country=request.country,
        visa_type=request.visa_type
    )
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    return {"message": "Demande d'assistance visa enregistrée", "id": new_request.id}


