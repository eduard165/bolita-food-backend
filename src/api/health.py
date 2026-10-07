from fastapi import APIRouter

router = APIRouter(tags=["Sistema"])


@router.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "bolita-food-backend",
        "version": "0.1.0",
    }