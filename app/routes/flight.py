from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import SessionLocal
from app.models.flight import FlightBooking
from app.schemas.flight import FlightBookingCreate  # à créer ensuite


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/book-flight")
def book_flight(request: FlightBookingCreate, db: Session = Depends(get_db)):
    booking = FlightBooking(
        user_id=request.user_id,
        departure=request.departure,
        arrival=request.arrival,
        travel_date=request.travel_date
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return {"message": "Réservation enregistrée", "id": booking.id}


