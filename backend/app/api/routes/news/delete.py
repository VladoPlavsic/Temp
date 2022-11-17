from fastapi import APIRouter
from fastapi import Depends
from starlette.status import HTTP_200_OK

from app.api.dependencies.database import get_db_repository
from app.db.repositories.news.news import NewsDBRepository

from app.api.dependencies.cdn import get_cdn_repository
from app.cdn.repositories.news.news import NewsYandexCDNRepository

from app.api.dependencies.auth import allowed_or_denied

router = APIRouter()

@router.delete("/delete", response_model=None, name="news:delete", status_code=HTTP_200_OK)
async def create_news(
    id: int,
    db_repo: NewsDBRepository = Depends(get_db_repository(NewsDBRepository)),
    allowed: bool = Depends(allowed_or_denied),
) -> None:
    await db_repo.delete_news(id=id)
    return None
