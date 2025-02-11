from fastapi import APIRouter, FastAPI
from fastapi_pagination import add_pagination
from routers.settings import router as settings_router
from routers.genre import router as genre_router
from routers.tag import router as tag_router
from routers.type import router as type_router

app = FastAPI(title="AllDay DJ")
base_router = APIRouter(prefix="/api")

base_router.include_router(genre_router)
base_router.include_router(settings_router)
base_router.include_router(tag_router)
base_router.include_router(type_router)

app.include_router(base_router)

add_pagination(app)
