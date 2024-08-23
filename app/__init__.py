from fastapi import FastAPI
from app.routers import router as api_router
from app.dependencies import get_db

def create_app() -> FastAPI:
    app =FastAPI()
    app.include_router(api_router)
    return app

app = create_app()