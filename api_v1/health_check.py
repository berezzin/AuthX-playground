from fastapi import APIRouter

router = APIRouter(prefix="/health-check", tags=["Health metrics"])


@router.get("/ping")
async def ping():
    return "pong"
