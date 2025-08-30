from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.services.user_service import get_admin_count

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