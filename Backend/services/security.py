from errors.exceptions import UnauthenticatedException, UnauthorizedException
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, SecurityScopes
from jwt import decode, PyJWKClient
from jwt.exceptions import DecodeError, PyJWKClientError
from logging import getLogger, Logger
from services.settings import get_settings, Settings
from typing import List, Optional

token_auth_scheme = HTTPBearer()


class TokenVerifier:
    __client: PyJWKClient
    __logger: Logger
    __settings: Settings

    def __init__(self, logger: Logger = getLogger("uvicorn.error")):
        self.__logger = logger

        self.__settings = get_settings()
        jwks_url = f"https://{self.__settings.jwt_domain}/.well-known/jwks.json"
        self.__logger.info("Set JWKS URL to %s", jwks_url)

        self.__client = PyJWKClient(jwks_url)

    @staticmethod
    def __check_claims(payload, claim_name: str, expected_values: List[str]):
        if claim_name not in payload:
            raise UnauthorizedException(detail=f"Claim {claim_name} not found in token")

        payload_claim = payload[claim_name]

        if claim_name == "scope":
            payload_claim = payload[claim_name].split(" ")

        for expected_value in expected_values:
            if expected_value not in payload_claim:
                raise UnauthorizedException(detail=f"Missing {claim_name} scope")

    async def verify(
        self,
        security_scopes: SecurityScopes,
        token: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer()),
    ):
        if not token:
            raise UnauthenticatedException()

        try:
            signing_key = self.__client.get_signing_key_from_jwt(token.credentials).key
        except DecodeError as error:
            raise UnauthorizedException(str(error))
        except PyJWKClientError as error:
            raise UnauthorizedException(str(error))

        try:
            payload = decode(
                token.credentials,
                signing_key,
                algorithms=[self.__settings.jwt_algorithm],
                audience=self.__settings.jwt_audience,
                issuer=self.__settings.jwt_issuer,
            )
        except Exception as error:
            raise UnauthorizedException(str(error))

        if len(security_scopes.scopes) > 0:
            self.__check_claims(payload, "scope", security_scopes.scopes)

        return payload
