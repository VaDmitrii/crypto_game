import logging

from config import settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.user_router import router as user_router

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


app = FastAPI(
    title="Welcome to Admin bot API",
    summary="API для получения и изменения данных о пользователях из Unity",
    docs_url="/docs",
    redoc_url=None,
    openapi_url="/openapi.json"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
