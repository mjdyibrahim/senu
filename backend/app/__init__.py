from fastapi import FastAPI
from fastapi import APIRouter
from app.routers.chat import router as chat_router                                                                                       
from app.routers.dashboard import router as dashboard_router                                                                             
from app.routers.gamification import router as gamification_router                                                                       
from app.routers.roadmap import router as roadmap_router                                                                                 
from app.routers.debug_routes import router as debug_router   
from app.dependencies import get_db

router = APIRouter()                                                                                                          

def create_app() -> FastAPI:
    app =FastAPI()
    app.router.include_router(chat_router)                                                             
    app.router.include_router(dashboard_router)                                              
    app.router.include_router(gamification_router)                                     
    app.router.include_router(roadmap_router)                                                    
    app.router.include_router(debug_router)     
    return app

app = create_app()