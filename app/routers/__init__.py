from .chat import router as chat_router
from .dashboard import router as dashboard_router
from .gamification import router as gamification_router
from .roadmap import router as roadmap_router
from .debug_routes import router as debug_router

# You can also create a list of all routers if needed
all_routers = [chat_router, dashboard_router, gamification_router, roadmap_router, debug_router]