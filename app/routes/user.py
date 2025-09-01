from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database.connection import SessionLocal
from app.models.user import User
from app.services.security import hash_password, verify_password
from app.services.auth import create_access_token

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {
        "request": request,
        "show_statut": True
    })

@router.post("/register", response_class=HTMLResponse)
def register_user(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    statut: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            return templates.TemplateResponse("register.html", {
                "request": request,
                "error": "Cet email est déjà utilisé.",
                "show_statut": True
            })

        hashed_pw = hash_password(password)

        new_user = User(
            username=username,
            email=email,
            password=hashed_pw,
            statut=statut,
            is_admin=(statut == "admin")
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return templates.TemplateResponse("register.html", {
            "request": request,
            "success": f"✅ Compte créé avec succès pour {username} !",
            "redirect_url": "/login",
            "show_statut": False
        })

    except Exception as e:
        print("Erreur lors de l'enregistrement:", e)
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "Une erreur est survenue lors de la création du compte.",
            "show_statut": True
        })

@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login", response_class=HTMLResponse)
def login_user(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        db_user = db.query(User).filter(User.email == email).first()
        if not db_user or not verify_password(password, db_user.password):
            return templates.TemplateResponse("login.html", {
                "request": request,
                "error": "Email ou mot de passe incorrect.",
                "email": email
            })

        redirect_url = "/admin/dashboard" if db_user.statut == "admin" else f"/dashboard?name={db_user.username}"
        return templates.TemplateResponse("login.html", {
            "request": request,
            "success": f"Connexion réussie. Bienvenue {db_user.username} !",
            "redirect_url": redirect_url
        })

    except Exception as e:
        print("Erreur lors de la connexion:", e)
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Erreur interne lors de la connexion.",
            "email": email
        })