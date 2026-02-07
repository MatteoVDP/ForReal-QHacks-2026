"""API route handlers."""
from app.routers.fact_check import router as fact_check_router
from app.routers.media import router as media_router

__all__ = [
    "fact_check_router",
    "media_router"
]
