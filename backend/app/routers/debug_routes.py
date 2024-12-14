from fastapi import APIRouter, Request
from fastapi.routing import APIRoute

router = APIRouter()

@router.get("/debug-routes")
async def debug_routes(request: Request):
    routes = request.app.routes
    route_data = [
        {
            "name": route.name,
            "path": route.path,
            "methods": route.methods if hasattr(route, "methods") else None,
        }
        for route in routes
    ]
    return {"routes": route_data}