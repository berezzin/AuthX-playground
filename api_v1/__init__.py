from fastapi import APIRouter
from .auth import router as auth_router
from .health_check import router as health_check_router
from .protected import router as protected_router

main_router = APIRouter()

main_router.include_router(auth_router)
main_router.include_router(health_check_router)
main_router.include_router(protected_router)
