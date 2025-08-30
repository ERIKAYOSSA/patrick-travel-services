from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.services.user_service import get_admin_count, create_user

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    admin_count = get_admin_count()
    show_statut = admin_count < 3
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
        create_user(name, email, password, statut)
        return RedirectResponse(url="/login", status_code=303)
    except Exception as e:
        print("Erreur lors de l'inscription:", e)
        return templates.TemplateResponse("register.html", {
            "request": request,
            "show_statut": True,
            "error": "Une erreur est survenue lors de la création du compte."
        })





