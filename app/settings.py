import os
from dotenv import load_dotenv

load_dotenv()  # Charge les variables depuis .env

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL")
    EMAIL_USER = os.getenv("EMAIL_USER")
    EMAIL_PASS = os.getenv("EMAIL_PASS")
    SECRET_KEY = os.getenv("SECRET_KEY")
    SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 587))

settings = Settings()