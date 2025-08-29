from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import SessionLocal
from app.models.notification import Notification
from app.services.auth import get_current_user
from app.models.user import User

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/notifications")
def get_user_notifications(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    notes = db.query(Notification).filter(Notification.user_id == current_user.id).order_by(Notification.created_at.desc()).all()
    return notes

from fastapi import HTTPException

@router.patch("/notifications/{notification_id}/read")
def mark_notification_as_read(notification_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    note = db.query(Notification).filter(Notification.id == notification_id, Notification.user_id == current_user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Notification introuvable")

    note.is_read = True
    db.commit()
    return {"message": "Notification marquée comme lue"}