from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, scorecard: str = ""):
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "scorecard": scorecard,
            "burn_rate_data": [],  # Replace with actual data
            "clv_data": [],        # Replace with actual data
            "cac_data": [],        # Replace with actual data
            "valuation_data": [],  # Replace with actual data
            "exit_potential_data": []  # Replace with actual data
        }
    )
