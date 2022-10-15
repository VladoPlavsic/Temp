from typing import Optional

from fastapi import APIRouter, Request
from fastapi import Body, Cookie, BackgroundTasks, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm

from starlette.status import HTTP_200_OK

from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES

from app.models.email import QuestionEmail

from app.api.dependencies.email import send_message, create_confirm_code_msg, create_confirm_link, create_reactivate_profile_email

from app.db.repositories.users.users import UsersDBRepository
from app.api.dependencies.database import get_db_repository
from app.api.dependencies.auth import get_user_from_cookie_token, auth_service, get_user_from_query_token_refresh

from app.api.dependencies.auth import generate_confirmation_code
from app.api.dependencies.crons import handle_deactivated_profiles

from app.models.token import AccessToken, RefreshToken

# request models
from app.models.user import UserCreate

# response models
from app.models.user import PublicUserInDB, UserInDB

router = APIRouter()

@router.post("/email/contact")
async def send_user_question_via_email(
    background_tasks: BackgroundTasks,
    email: QuestionEmail = Body(..., embed=True),
    ) -> None:

    background_tasks.add_task(send_message, subject=email.user_email, message_text=email.email_body)

    return None

@router.post("/register")
async def register_new_user(
    background_tasks: BackgroundTasks,
    new_user: UserCreate = Body(...),
    db_repo: UsersDBRepository = Depends(get_db_repository(UsersDBRepository)),
    ) -> PublicUserInDB:
    registred = await db_repo.register_new_user(new_user=new_user)

    if registred and not isinstance(registred, UserInDB):
        # TODO: If user is registered how do we guarantee that he will confirm email before JWT has expired?
        # If we enter here, we need to check if we can get user from JWT if the error sais expired -> create new JWT for user, and update in db!

        # if email is taken but not confirmed, resend confirmation email
        background_tasks.add_task(send_message, subject="Email confirmation. MPEI kids", message_text=create_confirm_link(token=registred, username=new_user.full_name), to=new_user.email)
        raise HTTPException(
                status_code=409,
                detail="This email is already taken but email not confirmed. Confirmation email resent!"
            )
    elif not registred:
        raise HTTPException(
                status_code=409,
                detail="This email is already taken. Login whith that email or register with new one!"
            )

    access_token = AccessToken(
        access_token=auth_service.create_email_confirmation_token(user=registred), token_type='Bearer'
    )

    await db_repo.set_jwt_token(user_id=registred.id, token=access_token.access_token)

    background_tasks.add_task(send_message, subject="Подтверждение электронной почты", message_text=create_confirm_link(token=access_token.access_token, username=new_user.full_name), to=registred.email)

    return PublicUserInDB(**registred.dict())

@router.post("/login/code", status_code=HTTP_200_OK)
async def user_login_with_email_and_password_send_code(
    background_tasks: BackgroundTasks,
    user_repo: UsersDBRepository = Depends(get_db_repository(UsersDBRepository)),
    form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm),
    ):
    user = await user_repo.authenticate_user(email=form_data.username, password=form_data.password)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Authentication was unsuccessful.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.email_verified:
        raise HTTPException(
            status_code=403,
            detail="Email not verified. Please verify and try again.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=406,
            detail="This account has been deactivated.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    confirmation_code = generate_confirmation_code()
    confirmation_code = await user_repo.set_confirmation_code(user_id=user.id, confirmation_code=confirmation_code)

    background_tasks.add_task(send_message, subject="Код подтверждения", message_text=create_confirm_code_msg(confirmation_code=confirmation_code), to=user.email)

    return {"Detail": "Confirmation code email sent!"}

@router.post("/login/token/", response_model=PublicUserInDB)
async def user_login_with_email_and_password(
    confirmation_code: str,
    remember: bool,
    user_repo: UsersDBRepository = Depends(get_db_repository(UsersDBRepository)),
    form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm),
    ) -> PublicUserInDB:
    user = await user_repo.authenticate_user(email=form_data.username, password=form_data.password)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Authentication was unsuccessful.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not await user_repo.check_code(user_id=user.id, code=confirmation_code) or not confirmation_code:
        raise HTTPException(
            status_code=401,
            detail="Authentication was unsuccessful.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = AccessToken(access_token=auth_service.create_access_token_for_user(user=user), shold_be_session=not remember, token_type="Bearer")
    refresh_token = RefreshToken(refresh_token=auth_service.create_refresh_token_for_user(user=user, shold_be_session=not remember))

    await user_repo.set_jwt_token(user_id=user.id, token=refresh_token.refresh_token)
    response_content = jsonable_encoder(PublicUserInDB(**user.dict()))
    response = JSONResponse(content=response_content)
    if remember:
        response.set_cookie(key="_shkembridge_tok", expires=60 * ACCESS_TOKEN_EXPIRE_MINUTES, value=access_token.access_token)
        response.set_cookie(key="_shkembridge_ref", expires=60 * 60 * 24 * 365, value=refresh_token.refresh_token)
    else:
        response.set_cookie(key="_shkembridge_tok", value=access_token.access_token)
        response.set_cookie(key="_shkembridge_ref", value=refresh_token.refresh_token)
    return response

@router.post("/refresh/token", response_model=PublicUserInDB)
async def refresh_jw_token(
    user_repo: UsersDBRepository = Depends(get_db_repository(UsersDBRepository)),
    _shkembridge_ref: Optional[str] = Cookie(None),
    ) -> PublicUserInDB:
    payload = await get_user_from_query_token_refresh(token=_shkembridge_ref)
    user = await user_repo.check_refresh_token(user=payload, refresh_token=_shkembridge_ref)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Could not refresh jwt. Refresh token not valid. Try logging in again",
            headers={
                "WWW-Authenticate": "Bearer",
                "set-cookie": "_shkembridge_ref=""; expires=0; Max-Age=0; Path=/",
            },
        )

    access_token = AccessToken(access_token=auth_service.create_access_token_for_user(user=user), shold_be_session=payload.ses, token_type="Bearer")
    refresh_token = RefreshToken(refresh_token=auth_service.create_refresh_token_for_user(user=user, shold_be_session=payload.ses))

    await user_repo.set_jwt_token(user_id=user.id, token=refresh_token.refresh_token)

    response_content = jsonable_encoder(PublicUserInDB(**user.dict()))
    response = JSONResponse(content=response_content)
    if not payload.ses:
        response.set_cookie(key="_shkembridge_tok", expires=60 * ACCESS_TOKEN_EXPIRE_MINUTES, value=access_token.access_token)
        response.set_cookie(key="_shkembridge_ref", expires=60 * 60 * 24 * 365, value=refresh_token.refresh_token)
    else:
        response.set_cookie(key="_shkembridge_tok", value=access_token.access_token)
        response.set_cookie(key="_shkembridge_ref", value=refresh_token.refresh_token)

    return response

@router.post("/logout", response_model=PublicUserInDB)
async def logout(
    user_repo: UsersDBRepository = Depends(get_db_repository(UsersDBRepository)),
    user: UserInDB = Depends(get_user_from_cookie_token),
    ) -> PublicUserInDB:
    await user_repo.remove_jwt(user_id=user.id)

    response_content = jsonable_encoder({"Data": "OK"})
    response = JSONResponse(content=response_content)
    response.delete_cookie("_shkembridge_tok")
    response.delete_cookie("_shkembridge_ref")
    return response

@router.post("/deactivated/check")
async def users_check_deactivated_profiles(
    background_task: BackgroundTasks,
    user_repo: UsersDBRepository = Depends(get_db_repository(UsersDBRepository)),
    ) -> None:

    one_month_warning = await user_repo.select_deactivated_profiles_for_warning_month()
    one_week_warning = await user_repo.select_deactivated_profiles_for_warning_week()
    deletion_profiles = await user_repo.select_deactivated_profiles_for_deletion()

    background_task.add_task(handle_deactivated_profiles, one_month_warning=one_month_warning, one_week_warning=one_week_warning, deletion_profiles=deletion_profiles)

    for profile in deletion_profiles:
        await user_repo.delete_profile(user_id=profile.id)
    return None


@router.post("/request/profile/reactivate", status_code=HTTP_200_OK)
async def reactivate_profile_request(
    email: str,
    background_task: BackgroundTasks,
    user_repo: UsersDBRepository = Depends(get_db_repository(UsersDBRepository)),
    ) -> None:

    user = await user_repo.get_user_by_email(email=email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found with given email!",
            headers={"WWW-Authenticate": "Bearer"},
        )

    reactivate_hash = await user_repo.create_confirmation_hash_for_reactivation(user_id=user.id)
    if not reactivate_hash:
        raise HTTPException(
            status_code=404,
            detail="Profile not deactivated!",
            headers={"WWW-Authenticate": "Bearer"},
        )

    reactivate_url = create_reactivate_profile_email(reactivate_hash=reactivate_hash)
    background_task.add_task(send_message, subject="Reactivate profile request", message_text=f"To reactivate your profile visit this url: {reactivate_url}", to=user.email)
    return None

@router.post("/profile/reactivate", status_code=HTTP_200_OK)
async def reactivate_profile(
    reactivate_hash: str,
    user_repo: UsersDBRepository = Depends(get_db_repository(UsersDBRepository)),
    ) -> None:

    response = await user_repo.activate_profile(reactivation_hash=reactivate_hash)
    if not response:
        raise HTTPException(
            status_code=403,
            detail="Reactivation failed!",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return None
