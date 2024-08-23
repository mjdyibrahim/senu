from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/result", response_class=HTMLResponse)
async def show_result(request: Request, scorecard: str = ""):
    return templates.TemplateResponse("result.html", {"request": request, "scorecard": scorecard})