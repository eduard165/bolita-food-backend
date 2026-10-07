from fastapi import FastAPI
from workers import asgi

from api.health import router as health_router
from api.menu import router as menu_router

app = FastAPI(
    title="Bolita Food API",
    version="0.1.0",
)

app.include_router(health_router)
app.include_router(menu_router)

Default = asgi.entrypoint(app)