from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/gamification", response_class=HTMLResponse)
async def show_gamification(request: Request):
    challenges = "here is your first challenge"
    return templates.TemplateResponse("gamification.html", {"request": request, "challenges": challenges})