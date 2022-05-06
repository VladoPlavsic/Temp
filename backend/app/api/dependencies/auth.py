from typing import Optional

from fastapi import Cookie, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from starlette.status import HTTP_403_FORBIDDEN

from app.core.config import SECRET_KEY, API_PREFIX
from app.models.user import UserInDB
from app.models.token import JWTPayload
from app.api.dependencies.database import get_db_repository
from app.db.repositories.users.users import UsersDBRepository
from app.services import auth_service


import logging

logger = logging.getLogger(__name__)

async def __validate_token_payload(payload, should_be_refresh: bool = False):
    if not payload:
        raise HTTPException(status_code=404, detail="No user found!")

    if payload.ref != should_be_refresh or payload.typ != "access":
        raise HTTPException(status_code=403, detail="Invalid token!")

    if not payload.is_active:
        raise HTTPException(status_code=406, detail="Account deactivated")

    return payload

async def __validate_token_payload_access(payload):
    return await __validate_token_payload(payload=payload, should_be_refresh=False)

async def __validate_token_payload_refresh(payload):
    return await __validate_token_payload(payload=payload, should_be_refresh=True)

async def get_user_from_query_token(
    token: str
    ) -> Optional[JWTPayload]:
    """Takes in JWT token as query parameter. Returns JWTPayload or raises 401 if token expired or not valid, 403 if token is wrong type and 406 if account is deactivated"""
    try:
        payload = auth_service.get_payload_from_access_token(token=token, secret_key=str(SECRET_KEY))
    except Exception as e:
        raise e
    
    return await __validate_token_payload_access(payload)

async def get_user_from_cookie_token(
    *,
    _shkembridge_tok: Optional[str] = Cookie(None)
    ) -> Optional[JWTPayload]:
    """Takes in JWT token as cookie. Returns JWTPayload or raises 401 if token expired or not valid, 403 if token is wrong type and 406 if account is deactivated"""
    try:
        payload = auth_service.get_payload_from_access_token(token=_shkembridge_tok, secret_key=str(SECRET_KEY))
    except Exception as e:
        raise e

    return await __validate_token_payload_access(payload)

async def get_user_from_cookie_token_refresh(
    *,
    _shkembridge_ref: Optional[str] = Cookie(None)
    ) -> Optional[JWTPayload]:
    """Takes in JWT token as cookie. Returns JWTPayload or raises 401 if token expired or not valid, 403 if token is wrong type and 406 if account is deactivated"""
    try:
        payload = auth_service.get_payload_from_access_token(token=_shkembridge_ref, secret_key=str(SECRET_KEY))
    except Exception as e:
        raise e

    return await __validate_token_payload_refresh(payload)

async def get_user_from_query_token_refresh(
    token: str
    ) -> Optional[JWTPayload]:
    """Takes in JWT token as query parameter. Returns JWTPayload or raises 401 if token expired or not valid, 403 if token is wrong type and 406 if account is deactivated"""
    try:
        payload = auth_service.get_payload_from_access_token(token=token, secret_key=str(SECRET_KEY))
    except Exception as e:
        raise e
    
    return await __validate_token_payload_refresh(payload)

async def is_superuser(
    *,
    user: UserInDB = Depends(get_user_from_cookie_token),
    ) -> bool:

    return user.is_superuser

async def is_verified(
    *,
    user: UserInDB = Depends(get_user_from_cookie_token),
    ) -> bool:

    if not user.email_verified:
        raise HTTPException(status_code=401, detail="Email not verified!")

    return user.email_verified

async def is_valid_confirmation_token(
    *,
    token: str
    ) -> Optional[JWTPayload]:
    """Takes in confirmation JWT token as query parameter. Returns JWTPayload if token is valid or raises 403 if token is wrong type"""
    try:
        payload = auth_service.get_payload_from_confirmation_token(token=token, secret_key=str(SECRET_KEY))
    except Exception as e:
        raise e

    if payload.typ != "confirmation":
        raise HTTPException(status_code=403, detail="Invalid token!")
    
    return payload

async def allowed_or_denied(
    is_superuser = Depends(is_superuser),
    is_verified = Depends(is_verified),
    ) -> bool:
    """If user is not superuser, or his email is not verified raise Exception, otherwise return True"""
    if not is_superuser:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not superuser!")
    
    return True

def generate_confirmation_code() -> str:
    from random import randint
    return str(randint(100000, 999999))
