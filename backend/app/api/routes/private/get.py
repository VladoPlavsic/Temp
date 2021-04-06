from typing import List
from fastapi import APIRouter, Depends, Path
from starlette.status import HTTP_200_OK

from app.db.repositories.private.private import PrivateDBRepository
from app.cdn.repositories.private.private import PrivateYandexCDNRepository

from app.api.dependencies.database import get_db_repository
from app.api.dependencies.cdn import get_cdn_repository

# request models
from app.models.private import SubjectGetModel
from app.models.private import BranchGetModel
from app.models.private import LectureGetModel

# ###
# response models
# ###
# structure
from app.models.private import GradeResponse
from app.models.private import SubjectResponse
from app.models.private import BranchResponse
from app.models.private import LectureResponse
# content
from app.models.private import VideoInDB
from app.models.private import BookInDB
from app.models.private import PresentationInDB
from app.models.private import GameInDB
# material
from app.models.private import MaterialResponse


# security
from app.api.dependencies.auth import get_user_from_token

router = APIRouter()

@router.get("/grade", response_model=GradeResponse, name="private:get-grades", status_code=HTTP_200_OK)
async def get_private_grades(
    token: str,
    user = Depends(get_user_from_token),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    ) -> GradeResponse:

    # we will accept token for validating user and available grade id's
    # available grade id's for a user will be returned to him when he logs in, same time as token
    # super user (admin) will skip process id validation

    if not user.is_superuser:
        user_grades = await db_repo.select_user_available_grades(user_id=user.id)
        ids = [grade.grade_id for grade in user_grades]
        if not ids:
            return GradeResponse(grades=[])
        else:
            response = await db_repo.select_grades(ids=ids)
            return GradeResponse(grades=response)
    else:
        response = await db_repo.select_grades()
        return GradeResponse(grades=response)


@router.get("/subject", response_model=SubjectResponse, name="private:get-subjects", status_code=HTTP_200_OK)
async def get_private_subjects(
    token: str,
    grade_name_en: str,
    user = Depends(get_user_from_token),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    ) -> SubjectResponse:
    
    # we will accept token for validating user and available grade id's as well as available subject id's
    # available grade id's for a user will be returned to him when he logs in, same time as token
    # we get grade ID by subject.grade_name_en
    # we check if grade ID is in available grade id's sent to us
    # if yes:
    #     select_subject (ids=subject id's, fk=grade ID)
    #     return subjects
    # no:
    #     return 402 Payment required
    # super user (admin) will skip process id validation

    fk = await db_repo.get_grade_by_name(grade_name=grade_name_en)
    response = await db_repo.select_subjects(fk=fk.id)

    return SubjectResponse(subjects=response, fk=fk.id, path=fk.name_ru)

@router.get("/branch", response_model=BranchResponse, name="private:get-branches", status_code=HTTP_200_OK)
async def get_private_branches(
    token: str,
    grade_name_en: str,
    subject_name_en: str,
    user = Depends(get_user_from_token),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    ) -> BranchResponse:

    # we will accept token for validating user and available grade id's as well as available subject id's
    # available grade id's for a user will be returned to him when he logs in, same time as token
    # we get grade ID by branch.grade_name_en
    # we check if grade ID is in available grade id's sent to us
    # if yes:
    #     we get ID by branch.subject_name_en
    #     we check if subject ID is in available subject id's sent to us 
    #     if yes:
    #         select_branches (fk = subject ID)
    #         return branches
    #     no:
    #         return 402 Payment required
    # no:
    #     return 402 Payment required
    # super user (admin) will skip process id validation
    (fk, path) = await db_repo.get_subject_by_name(grade_name=grade_name_en, subject_name=subject_name_en)
    response = await db_repo.select_branches(fk=fk.id)

    return BranchResponse(branches=response, fk=fk.id, path=path + '/' + fk.name_ru)

@router.get("/lecture", response_model=LectureResponse, name="private:get-lectures", status_code=HTTP_200_OK)
async def get_private_lectures(
    token: str,
    grade_name_en: str,
    subject_name_en: str,
    branch_name_en: str,
    user = Depends(get_user_from_token),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    ) -> LectureResponse:
    # we will accept token for validating user and available grade id's as well as available subject id's
    # available grade id's for a user will be returned to him when he logs in, same time as token
    # we get grade ID by branch.grade_name_en
    # we check if grade ID is in available grade id's sent to us
    # if yes:
    #     we get ID by branch.subject_name_en
    #     we check if subject ID is in available subject id's sent to us 
    #     if yes:
    #         get_branch_fk_by_name
    #         select_lecture (fk = branch ID)
    #         return lecture
    #     no:
    #         return 402 Payment required
    # no:
    #     return 402 Payment required
    # super user (admin) will skip process id validation
    (fk, path) = await db_repo.get_branch_by_name(grade_name=grade_name_en, subject_name=subject_name_en, branch_name=branch_name_en)
    response = await db_repo.select_lectures(fk=fk.id)


    return LectureResponse(lectures=response, fk=fk.id, path=path + '/' + fk.name_ru)

@router.get("/lecture/id", name="private:get-lecture-id", status_code=HTTP_200_OK)
async def get_private_lectures_id(
    grade_name_en: str,
    subject_name_en: str,
    branch_name_en: str,
    lecture_name_en: str,
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    ):

    (fk, path) = await db_repo.get_lecture_by_name(grade_name=grade_name_en, subject_name=subject_name_en, branch_name=branch_name_en, lecture_name=lecture_name_en)

    return {"Lecture id": fk.id}

@router.get("/material", response_model=MaterialResponse, name="private:get-material", status_code=HTTP_200_OK)
async def get_private_material(
    token: str,
    grade_name_en: str,
    subject_name_en: str,
    branch_name_en: str,
    lecture_name_en: str,
    user = Depends(get_user_from_token),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    ) -> MaterialResponse:
    # we will accept token for validating user and available grade id's as well as available subject id's
    # available grade id's for a user will be returned to him when he logs in, same time as token
    # we get grade ID by branch.grade_name_en
    # we check if grade ID is in available grade id's sent to us
    # if yes:
    #     we get ID by branch.subject_name_en
    #     we check if subject ID is in available subject id's sent to us 
    #     if yes:
    #         get_lecture_fk_by_name
    #         
    #         select_material (fk = lecture ID)
    #         return material
    #     no:
    #         return 402 Payment required
    # no:
    #     return 402 Payment required
    # super user (admin) will skip process id validation

    grade_id = await db_repo.get_grade_by_name(grade_name=grade_name_en)
    subject_id = await db_repo.get_subject_by_name(subject_name=subject_name_en)
    (fk, path) = await db_repo.get_lecture_by_name(grade_name=grade_name_en, subject_name=subject_name_en, branch_name=branch_name_en, lecture_name=lecture_name_en)

    response = await db_repo.select_material(fk=fk.id)

    return MaterialResponse(material=response, path=path, fk=fk.id)