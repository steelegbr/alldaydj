from fastapi import APIRouter, Depends, Security
from services.security import TokenVerifier

router = APIRouter(prefix="/tag", tags=["tag"])

token_verifier = TokenVerifier()


@router.get("/")
def auth_test(auth_result: str = Security(token_verifier.verify)):
    return {"result": auth_result}
