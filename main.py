from fastapi import FastAPI, Request

from routes.users import router as users_router
from routes.posts import router as posts_router
from loguru import logger

# Log to a file, with automatic rotation and retention
logger.add(
    "logs/mini-blog-fastapi-{time:YYYY-MM-DD}.log",
    rotation="1 week",
    retention="1 month",
    compression="zip"
)

app = FastAPI()


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(users_router)
app.include_router(posts_router)
