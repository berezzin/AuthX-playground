import uvicorn
from authx import AuthX, AuthXConfig
from fastapi import FastAPI, HTTPException, Depends
from fastapi import Response

app = FastAPI()

authx_config = AuthXConfig()
authx_config.JWT_ALGORITHM = "HS256"
authx_config.JWT_SECRET_KEY = "SECRET_KEY"
authx_config.JWT_ACCESS_COOKIE_NAME = "Authorization"
authx_config.JWT_TOKEN_LOCATION = ["cookies"]

security = AuthX(config=authx_config)
security.handle_errors(app)


@app.get("/ping")
async def ping():
    return "pong"


@app.get('/login')
async def login(username: str, password: str, response: Response):
    if username == "test" and password == "test":
        token = security.create_access_token(uid=username)
        response.set_cookie(key=authx_config.JWT_ACCESS_COOKIE_NAME, value=token, httponly=True)
        return
    raise HTTPException(401, detail={"message": "Bad credentials"})


@app.get("/protected", dependencies=[Depends(security.access_token_required)])
async def protected():
    return {"status": "ok"}


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
