from fastapi import APIRouter
from fastapi import Body, Depends, BackgroundTasks, HTTPException

from app.api.dependencies.email import send_message, create_reset_password_email

from app.db.repositories.users.users import UsersDBRepository
from app.api.dependencies.database import get_db_repository

from app.api.dependencies.auth import get_user_from_cookie_token
from app.models.user import UserUpdate, PublicUserInDB

# YooMoney
import uuid
from yookassa import Configuration, Payment

from app.core.config import YOOMONEY_ACCOUNT_ID, YOOMONEY_SECRET_KEY

router = APIRouter()

# password recovery
@router.put("/request/password/recovery")
async def request_password_recovery(
    background_task: BackgroundTasks,
    email: str = Body(..., embed=True),
    user_repo: UsersDBRepository = Depends(get_db_repository(UsersDBRepository)),
    ) -> None:

    # Create password recovery request and send recovery key to email
    # or return bad request (if email is not valid)
    response = await user_repo.request_reset_password(email=email)
    if not response:
        raise HTTPException(status_code=404, detail="User not found for given email")

    # send recovery email
    background_task.add_task(send_message, subject="Восстановление пароля", message_text=create_reset_password_email(recovery_hash=response), to=email)
    return None

@router.put("/confirm/password/recovery")
async def confirm_password_recovery(
    recovery_key: str,
    user_repo: UsersDBRepository = Depends(get_db_repository(UsersDBRepository)),
    ) -> None:

    response = await user_repo.confirm_reset_password(recovery_key=recovery_key)

    if not response:
        raise HTTPException(status_code=400, detail="Ooops! Something went wrong. Please try creating new recovery request!")

    return response

@router.put("/recover/password")
async def recover_password(
    recovery_hash: str,
    password: str = Body(..., embed=True),
    user_repo: UsersDBRepository = Depends(get_db_repository(UsersDBRepository)),
    ) -> None:

    response = await user_repo.reset_password(recovery_hash=recovery_hash, password=password)

    if not response:
        raise HTTPException(status_code=400, detail="Ooops! Something went wrong. Please try creating new recovery request!")

    return response

@router.put("/deactivate/profile")
async def deactivate_profile(
    password: str = Body(..., embed=True),
    user = Depends(get_user_from_cookie_token),
    user_repo: UsersDBRepository = Depends(get_db_repository(UsersDBRepository)),
    ) -> None:

    user = await user_repo.authenticate_user(email=user.email, password=password)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Authentication was unsuccessful.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    await user_repo.deactivate_profile(user_id=user.id)
    return None


@router.put("/delete/profile")
async def delete_profile(
    password: str = Body(..., embed=True),
    user = Depends(get_user_from_cookie_token),
    user_repo: UsersDBRepository = Depends(get_db_repository(UsersDBRepository)),
    ) -> None:

    user = await user_repo.authenticate_user(email=user.email, password=password)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Authentication was unsuccessful.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    await user_repo.delete_profile(user_id=user.id)
    return None

@router.put("/update")
async def update_profile(
    updated: UserUpdate = Body(...),
    user = Depends(get_user_from_cookie_token),
    user_repo: UsersDBRepository = Depends(get_db_repository(UsersDBRepository)),
    ) -> PublicUserInDB:

    response = await user_repo.update_user_information(id_=user.id, updated=updated)
    return response
