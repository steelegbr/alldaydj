from pydantic import BaseModel
from typing import Optional


class OAuthDeviceCodeRequest(BaseModel):
    audience: Optional[str]
    scope: Optional[str]
    client_id: str


class OAutheDeviceCodeResponse(BaseModel):
    device_code: str
    user_code: str
    verification_uri: str
    verification_uri_complete: str
    expires_in: int
    interval: int
