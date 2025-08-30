from fastapi import FastAPI
from app.routes import status
from app.routes import status, user
from app.routes import assistance_visa, school_admission
from app.routes import flight, accommodation, message
from app.routes import admin_partner
from app.routes import admin_offer
from app.routes import public_offer
from app.routes import document, admin_document
from app.routes import admin_notification
from app.routes import notification
from app.routes import admin_dashboard
from app.routes import admin_report
from app.routes import admin
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.services.user_service import get_admin_count
from app.routes import auth

app = FastAPI()

app.include_router(status.router)
app.include_router(user.router)
app.include_router(assistance_visa.router)
app.include_router(school_admission.router)
app.include_router(flight.router)
app.include_router(accommodation.router)
app.include_router(message.router)
app.include_router(admin_partner.router)
app.include_router(admin_offer.router)
app.include_router(public_offer.router)
app.include_router(document.router)
app.include_router(admin_document.router)
app.include_router(admin_notification.router)
app.include_router(notification.router)
app.include_router(admin_dashboard.router)
app.include_router(admin_report.router)
app.include_router(admin.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "Bienvenue sur Patrick Travel Services 🚀"}

import os
from dotenv import load_dotenv

load_dotenv()  # charge les variables depuis .env

# Exemple d'utilisation
db_url = os.getenv("DATABASE_URL")
email_user = os.getenv("EMAIL_USER")
email_pass = os.getenv("EMAIL_PASS")




app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")  # ✅ si ton dossier est dans app/

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    admin_count = await get_admin_count()  # à définir dans ton backend
    show_statut = admin_count < 3
    return templates.TemplateResponse("register.html", {"request": request, "show_statut": show_statut})