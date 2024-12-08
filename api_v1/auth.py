from fastapi import APIRouter, Depends
import httpx
from fastapi import HTTPException, Request, Response
from fastapi.responses import RedirectResponse
from google.auth.transport import requests
from google.oauth2 import id_token

from config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET
from helpers.auth_helper import security

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
async def login(request: Request):
    redirect_uri = request.url_for("auth_callback")
    google_auth_url = f"https://accounts.google.com/o/oauth2/auth?client_id={GOOGLE_CLIENT_ID}&redirect_uri={redirect_uri}&response_type=code&scope=openid email profile"

    return RedirectResponse(url=google_auth_url)


@router.get("/callback")
async def auth_callback(code: str, request: Request, response: Response):
    token_request_uri = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": request.url_for("auth_callback"),
        "grant_type": "authorization_code",
    }

    async with httpx.AsyncClient() as client:
        response_ouath = await client.post(token_request_uri, data=data)
        response_ouath.raise_for_status()
        token_response = response_ouath.json()

    id_token_value = token_response.get("id_token")
    if not id_token_value:
        raise HTTPException(status_code=400, detail="Missing id_token in response.")

    try:
        id_info = id_token.verify_oauth2_token(
            id_token_value, requests.Request(), GOOGLE_CLIENT_ID
        )

        user_name = id_info.get("name")

        access_token = security.create_access_token(uid=user_name)
        refresh_token = security.create_refresh_token(uid=user_name)

        security.set_access_cookies(token=access_token, response=response)
        security.set_refresh_cookies(token=refresh_token, response=response)
        return {"status": "ok", "name": user_name}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid id_token: {str(e)}")

    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/logout", dependencies=[Depends(security.access_token_required)])
async def logout(response: Response):
    security.unset_cookies(response=response)
    return {"status": "ok", "detail": "You are logged out!"}
