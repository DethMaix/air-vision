from fastapi import APIRouter

from .reg import router as reg_router
from .point import router as point_router

# Router initialization
router = APIRouter(prefix="/flights", tags=["flights"])

# Routers include
router.include_router(reg_router, prefix="/reg")
router.include_router(point_router, prefix="/point")