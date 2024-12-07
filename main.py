import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/ping")
async def ping():
    return "pong"


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)