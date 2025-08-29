from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import SessionLocal
from app.models.accommodation import Accommodation
from app.schemas.accommodation import AccommodationCreate  # à créer ensuite

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/accommodation-request")
def request_accommodation(request: AccommodationCreate, db: Session = Depends(get_db)):
    lodging = Accommodation(
        user_id=request.user_id,
        location=request.location,
        check_in=request.check_in,
        check_out=request.check_out
    )
    db.add(lodging)
    db.commit()
    db.refresh(lodging)
    return {"message": "Demande de logement enregistrée", "id": lodging.id}