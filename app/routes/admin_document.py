from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import SessionLocal
from app.models.document import Document
from app.services.auth import get_current_user
from app.models.user import User

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/admin/documents")
def list_documents(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Accès réservé à l'administration")
    return db.query(Document).all()

@router.patch("/admin/documents/{doc_id}/validate")
def validate_document(doc_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Accès réservé à l'administration")

    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document introuvable")

    doc.status = "validated"
    doc.is_conform = True
    db.commit()
    return {"message": "Document validé"}

@router.patch("/admin/documents/{doc_id}/reject")
def reject_document(doc_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Accès réservé à l'administration")

    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document introuvable")

    doc.status = "rejected"
    doc.is_conform = False
    db.commit()
    return {"message": "Document refusé"}