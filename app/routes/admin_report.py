from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from app.database.connection import SessionLocal
from app.services.auth import get_current_user
from app.models.user import User
from app.models.assistance_visa import AssistanceVisa
from app.models.school_admission import SchoolAdmission
from app.models.accommodation import Accommodation
from app.models.flight import FlightBooking
from app.models.partner import Partner

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/admin/reports")
def generate_report(
    start: datetime = Query(None),
    end: datetime = Query(None),
    partner_id: int = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Accès réservé à l'administration")

    report = {}

    # Requêtes de base
    visa_query = db.query(AssistanceVisa)
    admission_query = db.query(SchoolAdmission)
    flight_query = db.query(FlightBooking)
    accommodation_query = db.query(Accommodation)

    # Filtrage par période
    if start and end:
        visa_query = visa_query.filter(AssistanceVisa.submitted_at.between(start, end))
        admission_query = admission_query.filter(SchoolAdmission.submitted_at.between(start, end))
        flight_query = flight_query.filter(FlightBooking.travel_date.between(start, end))
        accommodation_query = accommodation_query.filter(Accommodation.check_in.between(start, end))

    # Filtrage par partenaire
    if partner_id:
        admission_query = admission_query.filter(SchoolAdmission.partner_id == partner_id)
        accommodation_query = accommodation_query.filter(Accommodation.partner_id == partner_id)

    # Statistiques générales
    report["visa_requests"] = visa_query.count()
    report["admission_requests"] = admission_query.count()
    report["flight_bookings"] = flight_query.count()
    report["accommodation_requests"] = accommodation_query.count()

    # Scénario étudiant : demandes de bourse
    bourse_query = admission_query.filter(SchoolAdmission.program == "bourse")
    report["bourse_requests"] = {
        "total": bourse_query.count(),
        "validated": bourse_query.filter(SchoolAdmission.status == "validated").count(),
        "pending": bourse_query.filter(SchoolAdmission.status == "pending").count(),
        "rejected": bourse_query.filter(SchoolAdmission.status == "rejected").count()
    }

    # Documents liés à la bourse
    from app.models.document import Document
    bourse_docs = db.query(Document).filter(Document.request_type == "bourse")
    if start and end:
        bourse_docs = bourse_docs.filter(Document.uploaded_at.between(start, end))

    report["bourse_documents"] = {
        "total": bourse_docs.count(),
        "validated": bourse_docs.filter(Document.status == "validated").count(),
        "pending": bourse_docs.filter(Document.status == "pending").count()
    }

    # Logements proposés et réservés
    from app.models.offer import Offer
    housing_offers = db.query(Offer).filter(Offer.type == "logement").count()
    housing_reservations = accommodation_query.count()
    housing_pending = accommodation_query.filter(Accommodation.status == "pending").count()

    report["housing"] = {
        "offers": housing_offers,
        "reservations": housing_reservations,
        "pending": housing_pending
    }

    # Visa lié à la bourse
    visa_bourse = visa_query.filter(AssistanceVisa.visa_type == "étudiant").count()
    visa_transmitted = visa_query.filter(AssistanceVisa.status == "transmis").count()

    report["visa_followup"] = {
        "linked_to_bourse": visa_bourse,
        "transmitted_to_embassy": visa_transmitted
    }

    # Notifications envoyées
    from app.models.notification import Notification
    notifications = db.query(Notification)
    if start and end:
        notifications = notifications.filter(Notification.created_at.between(start, end))

    report["notifications"] = {
        "total": notifications.count(),
        "by_type": {
            "message": notifications.filter(Notification.type == "message").count(),
            "account": notifications.filter(Notification.type == "account").count(),
            "update": notifications.filter(Notification.type == "update").count(),
            "reminder": notifications.filter(Notification.type == "reminder").count()
        }
    }

    # Info partenaire
    if partner_id:
        partner = db.query(Partner).filter(Partner.id == partner_id).first()
        report["partner"] = {
            "id": partner.id,
            "name": partner.name,
            "type": partner.type
        }

    report["generated_at"] = datetime.utcnow()
    return report

@router.get("/admin/reports/export")
def export_report(
    start: datetime = Query(None),
    end: datetime = Query(None),
    partner_id: int = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Accès réservé à l'administration")

    # Reprise des stats du dashboard enrichi
    from app.models.notification import Notification
    from app.models.document import Document
    from app.models.offer import Offer

    visa_query = db.query(AssistanceVisa)
    admission_query = db.query(SchoolAdmission)
    flight_query = db.query(FlightBooking)
    accommodation_query = db.query(Accommodation)
    notifications = db.query(Notification)
    documents = db.query(Document)
    offers = db.query(Offer)

    if start and end:
        visa_query = visa_query.filter(AssistanceVisa.submitted_at.between(start, end))
        admission_query = admission_query.filter(SchoolAdmission.submitted_at.between(start, end))
        flight_query = flight_query.filter(FlightBooking.travel_date.between(start, end))
        accommodation_query = accommodation_query.filter(Accommodation.check_in.between(start, end))
        notifications = notifications.filter(Notification.created_at.between(start, end))
        documents = documents.filter(Document.uploaded_at.between(start, end))

    if partner_id:
        admission_query = admission_query.filter(SchoolAdmission.partner_id == partner_id)
        accommodation_query = accommodation_query.filter(Accommodation.partner_id == partner_id)

    export_data = {
        "summary": {
            "visa_requests": visa_query.count(),
            "admission_requests": admission_query.count(),
            "flight_bookings": flight_query.count(),
            "accommodation_requests": accommodation_query.count(),
            "notifications_sent": notifications.count(),
            "documents_submitted": documents.count(),
            "offers_available": offers.count()
        },
        "details": {
            "bourse_validated": admission_query.filter(SchoolAdmission.program == "bourse", SchoolAdmission.status == "validated").count(),
            "housing_pending": accommodation_query.filter(Accommodation.status == "pending").count(),
            "visa_transmitted": visa_query.filter(AssistanceVisa.status == "transmis").count(),
            "messages_notifications": notifications.filter(Notification.type == "message").count()
        },
        "generated_at": datetime.utcnow()
    }

    if partner_id:
        partner = db.query(Partner).filter(Partner.id == partner_id).first()
        export_data["partner"] = {
            "id": partner.id,
            "name": partner.name,
            "type": partner.type
        }

    return export_data