from fastapi import APIRouter
from fastapi import Depends, Body
from starlette.status import HTTP_201_CREATED, HTTP_200_OK

from app.db.repositories.private.private import PrivateDBRepository
from app.cdn.repositories.private.private import PrivateYandexCDNRepository
from app.api.dependencies.database import get_db_repository
from app.api.dependencies.cdn import get_cdn_repository
from app.models.private import (
    SubejctPostModel, SubjectCreateModel, SubejctPostModelCheck,
)
from app.models.core import AllowCreate
from app.models.private import SubjectInDB


router = APIRouter()


@router.post("/check",
    response_model=AllowCreate,
    name="cources:check-create-cources",
    status_code=HTTP_200_OK,
)
async def check_create_cource(
    subject: SubejctPostModelCheck = Body(...),
    db_repo=Depends(get_db_repository(PrivateDBRepository)),
) -> AllowCreate:
    response = await db_repo.insert_subject_check(**subject.dict())
    return AllowCreate(OK=response)

@router.post("/",
    response_model=SubjectInDB,
    name="cources:post-subject",
    status_code=HTTP_201_CREATED,
)
async def create_private_subject(
    subject: SubejctPostModel = Body(...),
    db_repo=Depends(get_db_repository(PrivateDBRepository)),
    cdn_repo=Depends(get_cdn_repository(PrivateYandexCDNRepository)),
) -> SubjectInDB:
    background = cdn_repo.get_background_url(object_key=subject.object_key)
    return await db_repo.insert_subject(subject=SubjectCreateModel(
        **subject.dict(),
        background=background,
    ))
