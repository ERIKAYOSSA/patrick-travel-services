from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import os

# Chargement des variables d'environnement
load_dotenv()
db_url = os.getenv("DATABASE_URL")
email_user = os.getenv("EMAIL_USER")
email_pass = os.getenv("EMAIL_PASS")

# Initialisation de l'app
app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

# Route racine
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Inclusion des routeurs
from app.routes import (
    status, user, assistance_visa, school_admission, flight, accommodation,
    message, admin_partner, admin_offer, public_offer, document, admin_document,
    admin_notification, notification, admin_dashboard, admin_report, admin, auth
)

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
app.include_router(auth.router)  # ✅ routes /login et /register
app.mount("/static", StaticFiles(directory="app/static"), name="static")