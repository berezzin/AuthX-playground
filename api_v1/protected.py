from fastapi import APIRouter, Depends

from helpers.auth_helper import security

router = APIRouter(prefix="/secret", tags=["Top secret"])


@router.get("/protected", dependencies=[Depends(security.access_token_required)])
async def protected():
    return {"status": "ok"}
