from pydantic import BaseModel, HttpUrl
from typing import Optional


class Settings(BaseModel):
    base_url: HttpUrl = HttpUrl("http://localhost:8000")
    refresh_token: Optional[str] = None
    sound_device_preview: str = ""
