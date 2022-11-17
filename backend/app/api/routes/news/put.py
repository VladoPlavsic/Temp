from fastapi import APIRouter
from fastapi import Depends, Body
from starlette.status import HTTP_200_OK

from app.api.dependencies.cdn import get_cdn_repository
from app.cdn.repositories.news.news import NewsYandexCDNRepository

from app.api.dependencies.database import get_db_repository
from app.db.repositories.news.news import NewsDBRepository

from app.api.dependencies.auth import allowed_or_denied

# request models
from app.models.news import NewsUpdateModel

# response models
from app.models.news import NewsInDBModel

router = APIRouter()

@router.put("/update", response_model=NewsInDBModel, name="news:uodate", status_code=HTTP_200_OK)
async def create_news(
    updated: NewsUpdateModel = Body(...),
    db_repo: NewsDBRepository = Depends(get_db_repository(NewsDBRepository)),
    allowed: bool = Depends(allowed_or_denied),
) -> NewsInDBModel:
    response = await db_repo.update_news_metadata(updated=updated)
    return response
