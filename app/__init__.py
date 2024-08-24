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
    router.include_router(chat_router, prefix="/chat", tags=["chat"])                                                             
    router.include_router(dashboard_router, prefix="/dashboard", tags=["dashboard"])                                              
    router.include_router(gamification_router, prefix="/gamification", tags=["gamification"])                                     
    router.include_router(roadmap_router, prefix="/roadmap", tags=["roadmap"])                                                    
    router.include_router(debug_router, prefix="/debug", tags=["debug"])     
    return app

app = create_app()