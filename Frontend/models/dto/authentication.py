from enum import StrEnum
from pydantic import BaseModel
from typing import Generic, Optional, TypeVar

T = TypeVar("T")


class OAuthScope(StrEnum):
    OpenIdProfile = "openid profile"
    OpenIdOfflineAccess = "openid offline_access"
    OpenIdProfileWithOfflineAccess = "openid profile offline_access"


class OAuthGrant(StrEnum):
    DeviceCode = "urn:ietf:params:oauth:grant-type:device_code"


class OAuthTokenError(StrEnum):
    AuthorizationPending = "authorization_pending"
    SlowDown = "slow_down"
    ExpiredToken = "expired_token"
    AccessDenied = "access_denied"


class OAuthTokenResponseError(StrEnum):
    AuthorizationPending = "authorization_pending"
    SlowDown = "slow_down"
    ExpiredToken = "expired_token"
    AccessDenied = "access_denied"


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


class OAuthTokenRequest(BaseModel):
    grant_type: OAuthGrant
    device_code: str
    client_id: str


class OAuthTokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int


class OAuthError(BaseModel, Generic[T]):
    error: T
    error_description: str
