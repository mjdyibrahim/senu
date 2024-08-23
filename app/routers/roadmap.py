from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/roadmap", response_class=HTMLResponse)
async def show_milestones(request: Request):
    milestones = "Here you go this is your next Milestone"
    return templates.TemplateResponse("roadmap.html", {"request": request, "milestones": milestones})