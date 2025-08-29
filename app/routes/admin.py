from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/admin/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
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
    return templates.TemplateResponse("dashboard.html", {"request": request, **stats})