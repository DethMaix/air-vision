from fastapi import APIRouter

# Router initialization
router = APIRouter(tags=["health"])

# Basic health check endpoint
@router.get("")
def health_check() -> dict:
    return {"status": "ok"}