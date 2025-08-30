from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.services.user_service import get_admin_count
from app.schemas.user_schema import UserCreate
from app.services.user_service import create_user

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

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