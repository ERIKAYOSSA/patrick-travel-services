from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.services.user_service import get_admin_count, get_user_by_email, verify_password
from app.schemas.user_schema import UserCreate
from app.services.user_service import create_user

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# ✅ Liste des emails admin
ADMIN_EMAILS = [
    "admin@patricktravel.com",
    "yossa@patricktravel.com",
    "erikayossa0507@gmail.com"
]

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
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
                "error": "Email ou mot de passe incorrect."
            })

        # ✅ Redirection selon l’email
        if email in ADMIN_EMAILS:
            return RedirectResponse(url="/admin/dashboard", status_code=303)
        else:
            return RedirectResponse(url="/dashboard", status_code=303)

    except Exception as e:
        print("Erreur lors de la connexion:", e)
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Une erreur est survenue lors de la connexion."
        })

@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    try:
        admin_count = get_admin_count()
        show_statut = admin_count < 3
    except Exception as e:
        print("Erreur dans get_admin_count:", e)
        show_statut = True  # fallback
    return templates.TemplateResponse("register.html", {"request": request, "show_statut": show_statut})

@router.post("/register")
async def register_user(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    statut: str = Form(...)
):
    try:
        user_data = UserCreate(
            username=name,
            email=email,
            password=password,
            statut=statut
        )
        create_user(user_data)
        return RedirectResponse(url="/login", status_code=303)
    except Exception as e:
        print("Erreur lors de l'inscription:", e)
        return templates.TemplateResponse("register.html", {
            "request": request,
            "show_statut": True,
            "error": "Une erreur est survenue lors de la création du compte."
        })