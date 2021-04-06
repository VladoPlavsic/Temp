from fastapi import APIRouter
from fastapi import Depends, Path

from starlette.status import HTTP_200_OK

from app.api.dependencies.database import get_db_repository

from app.db.repositories.about.about import AboutDBRepository


router = APIRouter()

@router.delete("/team/{order}", response_model=None, name="delete:about-team", status_code=HTTP_200_OK)
async def delete_team_member(
    order: int = Path(...),
    db_repo: AboutDBRepository = Depends(get_db_repository(AboutDBRepository)),
    ) -> None:
    
    await db_repo.delete_team_member(id=order)


@router.delete("/contacts/{order}", response_model=None, name="delete:about-contact", status_code=HTTP_200_OK)
async def delete_contact(
    order: int = Path(...),
    db_repo: AboutDBRepository = Depends(get_db_repository(AboutDBRepository)),
    ) -> None:

    await db_repo.delete_contact(id=order)

@router.delete("/about_project/{order}", response_model=None, name="delete:about-about_project", status_code=HTTP_200_OK)
async def delete_about_project(
    order: int = Path(...),
    db_repo: AboutDBRepository = Depends(get_db_repository(AboutDBRepository)),
    ) -> None:

    await db_repo.delete_about_project(id=order)

