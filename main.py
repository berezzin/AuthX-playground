import uvicorn
from fastapi import FastAPI

from helpers.auth_helper import security
from api_v1 import main_router

app = FastAPI(docs_url="/", title="Authorization sandbox")
security.handle_errors(app)

app.include_router(main_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
