from fastapi import HTTPException

from app.db.repositories.news.update.queries import *

from app.db.repositories.base import BaseDBRepository

import logging

logger = logging.getLogger(__name__)

class NewsDBUpdateRepository(BaseDBRepository):

    async def update_news_links(self, *, news) -> None:
        """
        Accepts dict with keys = 'image key' and value = 'sharing link'
        Updates table news.news_images by keys
        """
        keys = list(news.keys())
        links = list(news.values())

        await self.__update(query=update_news_links_query(keys=keys, links=links))

    async def update_images_links(self, *, images) -> None:
        """
        Accepts dict with keys = 'image key' and value = 'sharing link'
        Updates table news.news_images by keys
        """
        keys = list(images.keys())
        links = list(images.values())
        await self.__update(query=update_news_images_links_query(keys=keys, links=links))

    async def __update(self, *, query):
        try:
            await self.db.fetch_one(query=query)
        except Exception as e:
            logger.error("--- ERROR UPDATING NEWS ---")                
            logger.error(e)
            logger.error("--- ERROR UPDATING NEWS ---")                
            raise HTTPException(status_code=400, detail=f"Unhandled error. Exiter with {e}")