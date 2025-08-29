from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import SessionLocal
from app.models.notification import Notification
from app.schemas.notification import NotificationCreate
from app.services.auth import get_current_user
from app.models.user import User

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/admin/notifications")
def create_notification(notification: NotificationCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Accès réservé à l'administration")

    new_note = Notification(**notification.dict())
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return {"message": "Notification envoyée", "id": new_note.id}

@router.get("/admin/notifications")
def list_notifications(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Accès réservé à l'administration")

    return db.query(Notification).order_by(Notification.created_at.desc()).all()