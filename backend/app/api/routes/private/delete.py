from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK

from app.db.repositories.private.private import PrivateDBRepository
from app.cdn.repositories.private.private import PrivateYandexCDNRepository

from app.api.dependencies.database import get_db_repository
from app.api.dependencies.cdn import get_cdn_repository

from app.api.dependencies.auth import allowed_or_denied


router = APIRouter()


@router.delete('/branch', response_model=None, name="private:delete-branch", status_code=HTTP_200_OK)
async def delete_private_branch(
    id: int,
    cdn_repo: PrivateYandexCDNRepository = Depends(get_cdn_repository(PrivateYandexCDNRepository)),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    allowed: bool = Depends(allowed_or_denied),
) -> None:

    deleted_key = await db_repo.delete_branch(id=id)
    try:
        if deleted_key:
            cdn_repo.delete_folder_by_inner_key(inner_key=deleted_key)
    except:
        pass

    return None

@router.delete('/lecture', response_model=None, name="private:delete-lecture", status_code=HTTP_200_OK)
async def delete_private_lecture(
    id: int,
    cdn_repo: PrivateYandexCDNRepository = Depends(get_cdn_repository(PrivateYandexCDNRepository)),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    allowed: bool = Depends(allowed_or_denied),
) -> None:
    deleted_key = await db_repo.delete_lecture(id=id)
    try:
        if deleted_key:
            cdn_repo.delete_folder_by_inner_key(inner_key=deleted_key)
    except:
        pass

    return None

@router.delete('/theory', response_model=None, name="private:delete-theory", status_code=HTTP_200_OK)
async def delete_private_theory(
    id: int,
    cdn_repo: PrivateYandexCDNRepository = Depends(get_cdn_repository(PrivateYandexCDNRepository)),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    allowed: bool = Depends(allowed_or_denied),
) -> None:

    deleted_key = await db_repo.delete_theory(id=id)
    try:
        if deleted_key:
            cdn_repo.delete_folder(folder=deleted_key)
    except:
        pass

    return None

@router.delete('/practice', response_model=None, name="private:delete-practice", status_code=HTTP_200_OK)
async def delete_private_practice(
    id: int,
    cdn_repo: PrivateYandexCDNRepository = Depends(get_cdn_repository(PrivateYandexCDNRepository)),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    allowed: bool = Depends(allowed_or_denied),
) -> None:

    deleted_key = await db_repo.delete_practice(id=id)
    try:
        if deleted_key:
            cdn_repo.delete_folder(folder=deleted_key)
    except:
        pass

    return None

@router.delete('/book', response_model=None, name="private:delete-book", status_code=HTTP_200_OK)
async def delete_private_book(
    id: int,
    cdn_repo: PrivateYandexCDNRepository = Depends(get_cdn_repository(PrivateYandexCDNRepository)),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    allowed: bool = Depends(allowed_or_denied),
) -> None:

    deleted_key = await db_repo.delete_book(id=id)
    try:
        if deleted_key:
            cdn_repo.delete_folder_by_inner_key(inner_key=deleted_key)
    except:
        pass

    return None

@router.delete('/video', response_model=None, name="private:delete-video", status_code=HTTP_200_OK)
async def delete_private_video(
    id: int,
    cdn_repo: PrivateYandexCDNRepository = Depends(get_cdn_repository(PrivateYandexCDNRepository)),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    allowed: bool = Depends(allowed_or_denied),
) -> None:

    deleted_key = await db_repo.delete_video(id=id)
    try:
        if deleted_key:
            cdn_repo.delete_folder_by_inner_key(inner_key=deleted_key)
    except:
        pass

    return None

@router.delete("/quiz", response_model=None, name="private:delete-quiz", status_code=HTTP_200_OK)
async def delete_private_quiz(
    fk: int,
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    cdn_repo: PrivateYandexCDNRepository = Depends(get_cdn_repository(PrivateYandexCDNRepository)),
    allowed: bool = Depends(allowed_or_denied),
) -> None:
    deleted_keys = await db_repo.delete_quiz(fk=fk)
    try:
        if deleted_keys:
            cdn_repo.delete_keys(list_of_keys=deleted_keys)
    except:
        pass

    return None

@router.delete("/quiz/question", response_model=None, name="private:delete-quiz", status_code=HTTP_200_OK)
async def delete_private_quiz_questions(
    id: int,
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    cdn_repo: PrivateYandexCDNRepository = Depends(get_cdn_repository(PrivateYandexCDNRepository)),
    allowed: bool = Depends(allowed_or_denied),
) -> None:

    deleted_key = await db_repo.delete_quiz_question(id=id)
    try:
        if deleted_key:
            cdn_repo.delete_folder_by_inner_key(inner_key=deleted_key)
    except:
        pass

    return None

@router.delete('/game', response_model=None, name="private:delete-game", status_code=HTTP_200_OK)
async def delete_private_game(
    id: int,
    cdn_repo: PrivateYandexCDNRepository = Depends(get_cdn_repository(PrivateYandexCDNRepository)),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    allowed: bool = Depends(allowed_or_denied),
) -> None:

    deleted_key = await db_repo.delete_game(id=id)
    try:
        if deleted_key:
            cdn_repo.delete_folder_by_inner_key(inner_key=deleted_key)
    except:
        pass

    return None

@router.delete("/block", response_model=None, name="private:delete-block", status_code=HTTP_200_OK)
async def delete_private_block_questions(
    id: int,
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    cdn_repo: PrivateYandexCDNRepository = Depends(get_cdn_repository(PrivateYandexCDNRepository)),
    allowed: bool = Depends(allowed_or_denied),
) -> None:
    deleted_key = await db_repo.delete_block_question(id=id)
    try:
        if deleted_key:
            cdn_repo.delete_folder_by_inner_key(inner_key=deleted_key)
    except:
        pass

    return None
