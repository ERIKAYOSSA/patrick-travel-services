from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.services.user_service import (
    get_admin_count,
    get_user_by_email,
    verify_password,
    create_user
)

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

ADMIN_EMAILS = [
    "admin@patricktravel.com",
    "yossa@patricktravel.com",
    "erikayossa0507@gmail.com"
]

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login", response_class=HTMLResponse)
async def login_user(
    request: Request,
    email: str = Form(...),
    password: str = Form(...)
):
    try:
        user = await get_user_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            return templates.TemplateResponse("login.html", {
                "request": request,
                "error": "Email ou mot de passe incorrect.",
                "email": email
            })

        redirect_url = "/admin/dashboard" if email in ADMIN_EMAILS else f"/dashboard?name={user.username}"
        return templates.TemplateResponse("login.html", {
            "request": request,
            "success": f"Connexion réussie. Bienvenue {user.username} !",
            "redirect_url": redirect_url
        })

    except Exception as e:
        print("Erreur lors de la connexion:", e)
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Erreur interne lors de la connexion.",
            "email": email
        })

@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    try:
        admin_count = get_admin_count()
        show_statut = admin_count < 3
    except Exception as e:
        print("Erreur dans get_admin_count:", e)
        show_statut = True
    return templates.TemplateResponse("register.html", {
        "request": request,
        "show_statut": show_statut
    })

@router.post("/register", response_class=HTMLResponse)
async def register_user(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    statut: str = Form(...)
):
    try:
        existing_user = await get_user_by_email(email)
        if existing_user:
            return templates.TemplateResponse("register.html", {
                "request": request,
                "error": "Cet email est déjà utilisé.",
                "show_statut": True
            })

        create_user(
            username=username,
            email=email,
            password=password,
            statut=statut
        )

        return templates.TemplateResponse("register.html", {
            "request": request,
            "success": f"✅ Compte créé avec succès pour {username} !",
            "redirect_url": "/login",
            "show_statut": False
        })

    except Exception as e:
        print("Erreur lors de l'inscription:", e)
        admin_count = get_admin_count()
        show_statut = admin_count < 3
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "Une erreur est survenue lors de la création du compte.",
            "show_statut": show_statut
        })