from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database.connection import SessionLocal
from app.models.user import User
from app.services.auth import get_current_user

templates = Jinja2Templates(directory="app/templates")
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/admin/dashboard")
def dashboard(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        return templates.TemplateResponse("unauthorized.html", {"request": request})

    # Exemple de stats
    user_count = db.query(User).count()
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user_count": user_count,
        "admin_name": current_user.username
    })