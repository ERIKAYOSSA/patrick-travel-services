from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import SessionLocal
from app.models.message import Message
from app.models.user import User
from app.models.notification import Notification
from app.services.auth import get_current_user
from app.services.email import send_notification_email
import shutil
import os
import asyncio

router = APIRouter()

MESSAGE_UPLOAD_DIR = "app/message_files"
os.makedirs(MESSAGE_UPLOAD_DIR, exist_ok=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/send-message")
def send_message(
    receiver_id: int,
    content: str | None = None,
    file: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Vérifier que le destinataire existe
    receiver = db.query(User).filter(User.id == receiver_id).first()
    if not receiver:
        raise HTTPException(status_code=404, detail="Destinataire introuvable")

    filename = None
    file_path = None

    if file:
        filename = f"{current_user.id}_{file.filename}"
        file_path = os.path.join(MESSAGE_UPLOAD_DIR, filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    # Enregistrer le message
    msg = Message(
        sender_id=current_user.id,
        receiver_id=receiver_id,
        content=content,
        filename=filename,
        file_url=file_path
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)

    # Créer une notification pour le destinataire
    note = Notification(
        user_id=receiver_id,
        type="message",
        content=f"Nouveau message de {current_user.username}"
    )
    db.add(note)
    db.commit()

    # Envoi d’un email de notification
    if receiver.email:
        asyncio.create_task(send_notification_email(
            to_email=receiver.email,
            subject="📩 Nouveau message reçu",
            content=f"Bonjour {receiver.username},\n\nVous avez reçu un nouveau message de {current_user.username} sur Patrick Travel Services.\n\nConnectez-vous pour le consulter."
        ))

    return {
        "message": "Message envoyé",
        "id": msg.id,
        "filename": filename,
        "file_url": file_path
    }