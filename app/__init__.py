from fastapi import FastAPI
from .routers import chat_router, dashboard_router, gamification_router, roadmap_router, debug_router
from .dependencies import get_db

app = FastAPI()

# Include routers
app.include_router(chat_router)
app.include_router(dashboard_router)
app.include_router(gamification_router)
app.include_router(roadmap_router)
app.include_router(debug_router)

# You can also add any app-wide configurations here
# You can also add any app-wide configurations here