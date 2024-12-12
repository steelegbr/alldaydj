from enum import StrEnum
from pydantic import BaseModel
from typing import Optional


class OAuthScope(StrEnum):
    OpenIdProfile = "openid profile"


class OAuthDeviceCodeRequest(BaseModel):
    audience: Optional[str]
    scope: Optional[str]
    client_id: str


class OAuthDeviceCodeResponse(BaseModel):
    device_code: str
    user_code: str
    verification_uri: str
    verification_uri_complete: str
    expires_in: int
    interval: int
