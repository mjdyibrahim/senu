from fastapi import APIRouter                                                                                                 
                                                                                                                        
from .chat import router as chat_router                                                                                       
from .dashboard import router as dashboard_router                                                                             
from .gamification import router as gamification_router                                                                       
from .roadmap import router as roadmap_router                                                                                 
from .debug_routes import router as debug_router                                                                                     
                                                                                                                        
router = APIRouter()                                                                                                          
router.include_router(chat_router, prefix="/chat", tags=["chat"])                                                             
router.include_router(dashboard_router, prefix="/dashboard", tags=["dashboard"])                                              
router.include_router(gamification_router, prefix="/gamification", tags=["gamification"])                                     
router.include_router(roadmap_router, prefix="/roadmap", tags=["roadmap"])                                                    
router.include_router(debug_router, prefix="/debug", tags=["debug"])         