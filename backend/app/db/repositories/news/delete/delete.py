from app.db.repositories.base import BaseDBRepository

from app.db.repositories.news.delete.queires import *

class NewsDBDeleteRepository(BaseDBRepository):

    async def delete_news(self, *, id: int) -> None:
        await self.__execute(query=delete_news_query(id=id))

    async def __execute(self, *, query):
        try:
            response = await self.db.fetch_one(query=query)
        except Exception as e:
            logger.error("--- ERROR DELETING NEWS ---")                
            logger.error(e)
            logger.error("--- ERROR DELETING NEWS ---")                
            raise HTTPException(status_code=400, detail=f"Unhandled error. Exiter with {e}")

        return response
