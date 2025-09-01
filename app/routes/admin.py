from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.services.auth import get_current_user
from app.models.user import User

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/admin/dashboard", response_class=HTMLResponse)
async def dashboard(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin:
        return RedirectResponse(url="/login", status_code=303)

    stats = {
        "total_clients": 128,
        "total_revenue": 4500000,
        "total_destinations": 12,
        "recent_bookings": [
            {"client": "Alice", "destination": "Paris", "date": "2025-08-28", "amount": 350000},
            {"client": "Jean", "destination": "Dubaï", "date": "2025-08-27", "amount": 420000},
            {"client": "Fatou", "destination": "Zanzibar", "date": "2025-08-26", "amount": 310000},
        ],
        "chart_labels": ["Jan", "Fév", "Mar", "Avr", "Mai", "Juin", "Juil", "Août"],
        "chart_data": [500000, 650000, 700000, 800000, 900000, 750000, 820000, 950000]
    }

    return templates.TemplateResponse("admin_dashboard.html", {
        "request": request,
        "user": current_user,
        **stats
    })