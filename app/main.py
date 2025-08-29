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


import os
from dotenv import load_dotenv

load_dotenv()  # charge les variables depuis .env

# Exemple d'utilisation
db_url = os.getenv("DATABASE_URL")
email_user = os.getenv("EMAIL_USER")
email_pass = os.getenv("EMAIL_PASS")