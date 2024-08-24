from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app import templates

router = APIRouter()

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, scorecard: str = ""):
    return templates.TemplateResponse("dashboard.html", {"request": request, "scorecard": scorecard})