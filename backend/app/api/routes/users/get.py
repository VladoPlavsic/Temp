from fastapi import APIRouter
from fastapi import Depends

from starlette.status import HTTP_200_OK
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from app.api.dependencies.auth import get_user_from_cookie_token, get_user_from_query_token, is_superuser, is_valid_confirmation_token

from app.db.repositories.users.users import UsersDBRepository
from app.api.dependencies.database import get_db_repository

from app.models.user import PublicUserInDB, UserInDB, AdminAvailableData

from app.models.token import AccessToken, RefreshToken
from app.core.config import AWS_SECRET_ACCESS_KEY, AWS_SECRET_KEY_ID, BUCKET

from app.services import auth_service

router = APIRouter()

@router.get("/admin", name="users:check-if-admin", status_code=HTTP_200_OK)
async def admin(
    is_superuser = Depends(is_superuser),
) -> bool:
    return AdminAvailableData(
        is_superuser=is_superuser,
        AWS_SECRET_ACCESS_KEY=AWS_SECRET_ACCESS_KEY if is_superuser else None,
        AWS_SECRET_KEY_ID=AWS_SECRET_KEY_ID if is_superuser else None,
        BUCKET=BUCKET if is_superuser else None,
    )

@router.get("/email/confirm")
async def confirm_email(
    user: UserInDB = Depends(is_valid_confirmation_token),
    db_repo: UsersDBRepository = Depends(get_db_repository(UsersDBRepository)),
    ) -> PublicUserInDB:
    try:
        user = await db_repo.get_user_by_id(user_id=user.user_id)

        if user.email_verified:
            return None

        if not user.is_active:
            return None

        await db_repo.verify_email(user_id=user.id)

        access_token = AccessToken(access_token=auth_service.create_access_token_for_user(user=user), shold_be_session=True, token_type="Bearer")
        refresh_token = RefreshToken(refresh_token=auth_service.create_refresh_token_for_user(user=user, shold_be_session=True))

        await db_repo.set_jwt_token(user_id=user.id, token=refresh_token.refresh_token)

        response_content = jsonable_encoder(PublicUserInDB(**user.dict()))
        response = JSONResponse(content=response_content)
        response.set_cookie(key="_shkembridge_tok", value=access_token.access_token)
        response.set_cookie(key="_shkembridge_ref", value=refresh_token.refresh_token)

        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Unhandled exception raised in user. Exited with {e}")

@router.get("/profile")
async def get_user_information(
    user: UserInDB = Depends(get_user_from_cookie_token),
    db_repo: UsersDBRepository = Depends(get_db_repository(UsersDBRepository)),
    ) -> PublicUserInDB:

    response = await db_repo.get_user_by_id(user_id=user.id)
    return PublicUserInDB(**response.dict())
