from fastapi import APIRouter, FastAPI
from routers.settings import router as settings_router
from routers.tag import router as tag_router

app = FastAPI(title="AllDay DJ")
base_router = APIRouter(prefix="/api")

base_router.include_router(settings_router)
base_router.include_router(tag_router)

app.include_router(base_router)
