from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_200_OK

from app.db.repositories.private.private import PrivateDBRepository

from app.api.dependencies.database import get_db_repository
from app.api.dependencies.auth import get_user_from_cookie_token, is_superuser, is_verified

# ###
# response models
# ###
# structure
from app.models.private import SubjectResponse
from app.models.private import BranchResponse
from app.models.private import LectureResponse
# material
from app.models.private import MaterialResponse

router = APIRouter()

# ###
# SUBJECTS
# ###
@router.get("/subject",
    response_model=SubjectResponse,
    name="private:get-subjects",
    status_code=HTTP_200_OK,
)
async def get_subjects(
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
) -> SubjectResponse:
    response = await db_repo.select_subjects()
    return SubjectResponse(subjects=response)

# ###
# BRANCHES
# ###
# @router.get("/branch/available", response_model=BranchResponse, name="private:get-branches", status_code=HTTP_200_OK)
# async def get_private_branches(
#     subject_name_en: str,
#     db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
#     ) -> BranchResponse:

#     subject = await db_repo.get_subject_by_name(subject_name=subject_name_en)
#     response = await db_repo.select_branches(fk=subject.id)

#     return BranchResponse(branches=response, fk=subject.id)

@router.get("/branch", response_model=BranchResponse, name="private:get-branches", status_code=HTTP_200_OK)
async def get_private_branches(
    subject_id: int,
    # subject_name_en: str,
    # user = Depends(get_user_from_cookie_token),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    # is_superuser = Depends(is_superuser),
    # is_verified = Depends(is_verified),
) -> BranchResponse:

    """We decide what content to provide based on JWT.

    If JWT contains user who has not confirmed their email  -- Raise 401
    If JWT contains superuser                               -- Grant access to all content
    If JWT contains any other use but superuser             -- Grant access based on user available subjects
                                                            or grades if specific subject is not available
    """
    # if is_superuser:
    #     subject = await db_repo.get_subject_by_name(subject_name=subject_name_en)
    #     response = await db_repo.select_branches(fk=subject.id)
    # else:
    #     if await db_repo.check_if_content_available(user_id=user.id, subject_name=subject_name_en):
    #         subject = await db_repo.get_subject_by_name(subject_name=subject_name_en)
    response = await db_repo.select_branches(fk=subject_id)
    #     else:
    #         raise HTTPException(status_code=402, detail="Ooops! Looks like you don't have access to this content. Check our offers to gain access!")

    return BranchResponse(branches=response, fk=subject_id)

# ###
# LECTURES
# ###
# @router.get("/lecture/available", response_model=LectureResponse, name="private:get-lectures", status_code=HTTP_200_OK)
# async def get_private_lectures(
#     subject_name_en: str,
#     branch_name_en: str,
#     db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
#     ) -> LectureResponse:

#     (branch, path) = await db_repo.get_branch_by_name(subject_name=subject_name_en, branch_name=branch_name_en)
#     response = await db_repo.select_lectures(fk=branch.id)
#     return LectureResponse(lectures=response, fk=branch.id, path=path + '/' + branch.name_ru)

@router.get("/lecture", response_model=LectureResponse, name="private:get-lectures", status_code=HTTP_200_OK)
async def get_private_lectures(
    branch_id: int,
    # subject_name_en: str,
    # branch_name_en: str,
    # user = Depends(get_user_from_cookie_token),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    # is_superuser = Depends(is_superuser),
    # is_verified = Depends(is_verified),
) -> LectureResponse:
    """We decide what content to provide based on JWT.

    If JWT contains user who has not confirmed their email  -- Raise 401
    If JWT contains superuser                               -- Grant access to all content
    If JWT contains any other use but superuser             -- Grant access based on user available subjects
                                                            or grades if specific subject is not available
    """
    # if is_superuser:
    #     (branch, path) = await db_repo.get_branch_by_name(subject_name=subject_name_en, branch_name=branch_name_en)
    #     response = await db_repo.select_material(fk=branch.id)
    # else:
    #     if await db_repo.check_if_content_available(user_id=user.id, subject_name=subject_name_en):
    #         (branch, path) = await db_repo.get_branch_by_name(subject_name=subject_name_en, branch_name=branch_name_en)
    response = await db_repo.select_lectures(fk=branch_id)
    #     else:
    #         raise HTTPException(status_code=402, detail="Ooops! Looks like you don't have access to this content. Check our offers to gain access!")

    return LectureResponse(lectures=response, fk=branch_id) # path=path + '/' + branch.name_ru

@router.get("/material", response_model=MaterialResponse, name="private:get-material", status_code=HTTP_200_OK)
async def get_private_material(
    lecture_id: int,
    # grade_name_en: str,
    # subject_name_en: str,
    # branch_name_en: str,
    # lecture_name_en: str,
    # user = Depends(get_user_from_cookie_token),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    # is_superuser = Depends(is_superuser),
    # is_verified = Depends(is_verified),
    ) -> MaterialResponse:
    """We decide what content to provide based on JWT.

    If JWT contains user who has not confirmed their email  -- Raise 401
    If JWT contains superuser                               -- Grant access to all content
    If JWT contains any other use but superuser             -- Grant access based on user available subjects
                                                            or grades if specific subject is not available
    """
    # if is_superuser:
    #     (lecture, path) = await db_repo.get_lecture_by_name(grade_name=grade_name_en, subject_name=subject_name_en, branch_name=branch_name_en, lecture_name=lecture_name_en)
    #     response = await db_repo.select_material(fk=lecture.id)
    # else:
    #     if await db_repo.check_if_content_available(user_id=user.id, subject_name=subject_name_en):
    #         (lecture, path) = await db_repo.get_lecture_by_name(grade_name=grade_name_en, subject_name=subject_name_en, branch_name=branch_name_en, lecture_name=lecture_name_en)
    response = await db_repo.select_material(fk=lecture_id)
    #     else:
    #         raise HTTPException(status_code=402, detail="Ooops! Looks like you don't have access to this content. Check our offers to gain access!")

    return MaterialResponse(material=response, fk=lecture_id) # path=path
