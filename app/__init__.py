from fastapi import FastAPI

app = FastAPI()

from .routers import users, items  # import and include all your routers
app.include_router(users.router)
app.include_router(items.router)

# You can also add any app-wide configurations here