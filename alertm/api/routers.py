from api import health, matching
from fastapi import APIRouter

router = APIRouter()

router.include_router(matching.router, tags=["matching"], prefix="/alert-matching")
router.include_router(health.router, tags=["health"], prefix="/health")
