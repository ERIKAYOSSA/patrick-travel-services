from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import SessionLocal
from app.models.document import Document
from app.schemas.document import DocumentCreate
from app.services.auth import get_current_user
from app.models.user import User
from fastapi import File, UploadFile
import shutil
import os
router = APIRouter()

UPLOAD_DIR = "app/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upload-document")
def upload_document(
    request_type: str,
    request_id: int | None = None,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    filename = f"{current_user.id}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    new_doc = Document(
        user_id=current_user.id,
        request_type=request_type,
        request_id=request_id,
        filename=filename,
        file_url=file_path
    )
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)

    return {"message": "Document uploadé", "filename": filename}



