from typing import Optional
import jwt
import bcrypt
from datetime import datetime, timedelta
from passlib.context import CryptContext

from fastapi import HTTPException, status
from pydantic import ValidationError

from app.core.config import SECRET_KEY, JWT_ALGORITHM, JWT_AUDIENCE, JWT_TOKEN_PREFIX, ACCESS_TOKEN_EXPIRE_MINUTES
from app.models.token import JWTMeta, JWTCreds, JWTPayload, JWTUserMeta, JWTEmailConfirmation
from app.models.user import UserPasswordUpdate, UserInDB

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class AuthException(BaseException):
    """
    Custom auth exception that can be modified later on.
    """
    pass

class AuthService:
    def create_salt_and_hash_password(self, *, plaintext_password: str) -> UserPasswordUpdate:
        salt = self.generate_salt()

        hashed_password = self.hash_password(password=plaintext_password, salt=salt)

        return UserPasswordUpdate(salt=salt, password=hashed_password)

    def generate_salt(self) -> str:
        return bcrypt.gensalt().decode()

    def hash_password(self, password: str, salt: str) -> str:
        return pwd_context.hash(password + salt)

    def verify_password(self, *, password: str, salt: str, hashed_password: str) -> bool:
        return pwd_context.verify(password + salt, hashed_password)

    def create_email_confirmation_token(self, *, user: UserInDB, secret_key: str = str(SECRET_KEY)) -> str:
        if not user or not isinstance(user, UserInDB):
            return None

        token_payload = JWTEmailConfirmation(user_id=user.id)

        confirmation_token = jwt.encode(token_payload.dict(), secret_key, algorithm=JWT_ALGORITHM)
        return confirmation_token

    def create_access_token_for_user(
        self,
        *,
        user: UserInDB,
        shold_be_session: bool = True,
        secret_key: str = str(SECRET_KEY),
        audience: str = JWT_AUDIENCE,
        expires_in: int = ACCESS_TOKEN_EXPIRE_MINUTES,
        ) -> str:
        
        return self.__create_token(
            user=user,
            shold_be_session=shold_be_session,
            secret_key=secret_key,
            audience=audience,
            expires_in=expires_in,
            ref=False
        )


    def create_refresh_token_for_user(self,
        *,
        user: UserInDB,
        shold_be_session: bool = True,
        secret_key: str = str(SECRET_KEY),
        audience: str = JWT_AUDIENCE,
        expires_in: int = 60 * 24 * 365, # refresh token expires in a year
        ) -> str:

        return self.__create_token(
            user=user,
            shold_be_session=shold_be_session,
            secret_key=secret_key,
            audience=audience,
            expires_in=expires_in,
            ref=True
        )

    def __create_token(self,
        *,
        user: UserInDB,
        shold_be_session: bool = True,
        secret_key: str = str(SECRET_KEY),
        audience: str = JWT_AUDIENCE,
        expires_in: int = 60 * 24 * 365, # refresh token expires in a year
        ref=True
        ) -> str:
        if not user or not isinstance(user, UserInDB):
            return None

        jwt_meta = JWTMeta(
            aud=audience,
            iat=datetime.timestamp(datetime.utcnow()),
            exp=datetime.timestamp(datetime.utcnow() + timedelta(minutes=expires_in)),
            ses=shold_be_session,
            ref=ref,
        )
        jwt_creds = JWTCreds(email=user.email, phone_number=user.phone_number)
        jwt_user_meta = JWTUserMeta(**user.dict())

        token_payload = JWTPayload(
            **jwt_meta.dict(),
            **jwt_creds.dict(),
            **jwt_user_meta.dict(),
        )

        token = jwt.encode(token_payload.dict(), secret_key, algorithm=JWT_ALGORITHM)
        return token


    def get_payload_from_confirmation_token(self, *, token: str, secret_key: str) -> Optional[JWTEmailConfirmation]:
        """Takes in JWT token. Returns payload || 401"""
        try:
            decoded_token = jwt.decode(token, str(secret_key), audience=JWT_AUDIENCE, algorithms=[JWT_ALGORITHM])
            payload = JWTEmailConfirmation(**decoded_token)
        except (jwt.PyJWTError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate token credientals",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return payload

    def get_payload_from_access_token(self, *, token: str, secret_key: str) -> Optional[JWTPayload]:
        """Takes in JWT token. Returns payload || 401"""
        try:
            decoded_token = jwt.decode(token, str(secret_key), audience=JWT_AUDIENCE, algorithms=[JWT_ALGORITHM])
            payload = JWTPayload(**decoded_token)
        except (jwt.PyJWTError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate token credientals",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return payload
