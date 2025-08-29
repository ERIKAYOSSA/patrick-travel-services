from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import SessionLocal
from app.models.school_admission import SchoolAdmission
from app.schemas.school_admission import SchoolAdmissionCreate # à créer ensuite

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/school-admission")
def submit_school_admission(request: SchoolAdmissionCreate, db: Session = Depends(get_db)):
    new_admission = SchoolAdmission(
        user_id=request.user_id,
        school_name=request.school_name,
        program=request.program,
        country=request.country
    )
    db.add(new_admission)
    db.commit()
    db.refresh(new_admission)
    return {"message": "Demande d'admission scolaire enregistrée", "id": new_admission.id}