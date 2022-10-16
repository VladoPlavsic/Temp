from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK

from app.db.repositories.public.public import PublicDBRepository
from app.api.dependencies.database import get_db_repository
from app.models.public import CourceResponse


router = APIRouter()


@router.get("/",
    response_model=CourceResponse,
    name="cources:get-cources",
    status_code=HTTP_200_OK,
)
async def get_subjects(
    db_repo=Depends(get_db_repository(PublicDBRepository)),
) -> CourceResponse:
    return CourceResponse(cources=await db_repo.get_cources())
