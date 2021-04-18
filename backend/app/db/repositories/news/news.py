from app.db.repositories.news.insert.insert import NewsDBInsertRepository
from app.db.repositories.news.insert.delete import NewsDBDeletetRepository
from app.db.repositories.news.insert.update import NewsDBUpdateRepository
from app.db.repositories.news.insert.select import NewsDBSelectRepository

class NewsDBRepository(
    NewsDBInsertRepository,
    NewsDBSelectRepository,
    NewsDBUpdateRepository,
    NewsDBDeletetRepository,
    ):
    pass
