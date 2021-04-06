from fastapi import APIRouter
from fastapi import Body, Depends
from starlette.status import HTTP_200_OK

from app.api.dependencies.database import get_db_repository
from app.db.repositories.about.about import AboutDBRepository

# request models
from app.models.about import UpdateTeamMemberModel
from app.models.about import UpdateAboutProjectModel
from app.models.about import UpdateContactsModel

# respoonse models
from app.models.about import TeamMemberInDBModel
from app.models.about import AboutProjectInDBModel
from app.models.about import ContactsInDBModel

router = APIRouter()

@router.put("/team", response_model=TeamMemberInDBModel, name="put:about-team", status_code=HTTP_200_OK)
async def update_team_member(
    updated: UpdateTeamMemberModel = Body(...),
    db_repo: AboutDBRepository = Depends(get_db_repository(AboutDBRepository)),
    ) -> TeamMemberInDBModel:

    response = await db_repo.update_team_member(updated=updated)
    return response

@router.put("/contacts", response_model=ContactsInDBModel, name="put:about-contact", status_code=HTTP_200_OK)
async def update_contact(
    updated: UpdateContactsModel = Body(...),
    db_repo: AboutDBRepository = Depends(get_db_repository(AboutDBRepository)),
    ) -> ContactsInDBModel:

    response = await db_repo.update_contact(updated=updated)
    return response

@router.put("/about_project", response_model=AboutProjectInDBModel, name="put:about-about_contact", status_code=HTTP_200_OK)
async def update_about_project(
    updated: UpdateAboutProjectModel = Body(...),
    db_repo: AboutDBRepository = Depends(get_db_repository(AboutDBRepository)),
    ) -> AboutProjectInDBModel:

    response = await db_repo.update_about_project(updated=updated)
    return response

