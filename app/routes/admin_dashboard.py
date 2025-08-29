from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database.connection import SessionLocal
from app.services.auth import get_current_user
from app.models.user import User
from app.models.assistance_visa import AssistanceVisa
from app.models.school_admission import SchoolAdmission
from app.models.flight import FlightBooking
from app.models.accommodation import Accommodation
from app.models.message import Message
from app.models.document import Document
from app.models.offer import Offer
from app.models.notification import Notification

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/admin/dashboard")
def get_dashboard_stats(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Accès réservé à l'administration")

    stats = {
        "users_total": db.query(func.count(User.id)).scalar(),
        "messages_total": db.query(func.count(Message.id)).scalar(),
        "notifications_total": db.query(func.count(Notification.id)).scalar(),

        "bourse_requests": {
            "total": db.query(func.count(SchoolAdmission.id)).filter(SchoolAdmission.program == "bourse").scalar(),
            "validated": db.query(func.count()).filter(SchoolAdmission.program == "bourse", SchoolAdmission.status == "validated").scalar(),
            "pending": db.query(func.count()).filter(SchoolAdmission.program == "bourse", SchoolAdmission.status == "pending").scalar(),
            "rejected": db.query(func.count()).filter(SchoolAdmission.program == "bourse", SchoolAdmission.status == "rejected").scalar(),
        },
        "bourse_documents": {
            "total": db.query(func.count(Document.id)).filter(Document.request_type == "bourse").scalar(),
            "validated": db.query(func.count()).filter(Document.request_type == "bourse", Document.status == "validated").scalar(),
            "pending": db.query(func.count()).filter(Document.request_type == "bourse", Document.status == "pending").scalar(),
        },
        "housing": {
            "offers": db.query(func.count(Offer.id)).filter(Offer.type == "logement").scalar(),
            "reservations": db.query(func.count(Accommodation.id)).scalar(),
            "pending": db.query(func.count()).filter(Accommodation.status == "pending").scalar(),
        },
        "visa_followup": {
            "linked_to_bourse": db.query(func.count(AssistanceVisa.id)).filter(AssistanceVisa.visa_type == "étudiant").scalar(),
            "transmitted_to_embassy": db.query(func.count()).filter(AssistanceVisa.status == "transmis").scalar(),
        },
        "notifications_type": {
            "message": db.query(func.count(Notification.id)).filter(Notification.type == "message").scalar(),
            "account": db.query(func.count(Notification.id)).filter(Notification.type == "account").scalar(),
            "update": db.query(func.count(Notification.id)).filter(Notification.type == "update").scalar(),
            "reminder": db.query(func.count(Notification.id)).filter(Notification.type == "reminder").scalar(),
        }
    }

    return stats