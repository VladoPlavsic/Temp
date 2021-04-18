from typing import List
from fastapi import HTTPException

from app.db.repositories.base import BaseDBRepository

from app.db.repositories.news.select.queries import *

from app.models.news import NewsImagesAllModel
from app.models.news import NewsAllModel

import logging

logger = logging.getLogger(__name__)

class NewsDBSelectRepository(BaseDBRepository):

    async def select_all_news(self) -> List[NewsAllModel]:
        """
        Returns list of keys for all news preview images in database
        """
        records = await self.__select_many(query=select_all_news_query())

        response = [NewsAllModel(**record) for record in records]
        return response

    async def select_all_news_images(self) -> List[NewsImagesAllModel]:
        """
        Returns list of keys for all news images in database
        """
        records = await self.__select_many(query=select_all_news_images_query())

        response = [NewsImagesAllModel(**record) for record in records] 
        return response


    async def __select_many(self, *, query):
        try:
            response = await self.db.fetch_all(query=query)
        except Exception as e:
            logger.error("--- ERROR SELECTING NEWS ---")                
            logger.error(e)
            logger.error("--- ERROR SELECTING NEWS ---")                
            raise HTTPException(status_code=400, detail=f"Unhandled error. Exiter with {e}")

        return response