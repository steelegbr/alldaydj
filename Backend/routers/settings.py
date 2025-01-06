from fastapi import APIRouter, Depends
from models.settings import AppSettings
from services.settings import get_settings
from typing import Annotated, Dict

router = APIRouter(prefix="/settings", tags=["settings"])

SettingsDep = Annotated[Dict, Depends(get_settings)]


@router.get("/")
async def application_settings(settings: SettingsDep) -> AppSettings:
    return AppSettings(
        auth_audience=settings.jwt_audience,
        auth_domain=settings.jwt_domain,
        auth_client_id=settings.jwt_client_id,
    )
