from fastapi import HTTPException

from app.db.repositories.base import BaseDBRepository

from app.db.repositories.private.delete.queries import *

import logging

logger = logging.getLogger(__name__)

class PrivateDBDeleteRepository(BaseDBRepository):
    async def delete_grade(self, *, id) -> str:
        return await self.__delete(query=delete_grade_query(id=id))

    async def delete_subject(self, *, id) -> str:
        return await self.__delete(query=delete_subject_query(id=id))

    async def delete_branch(self, *, id) -> str:
        return await self.__delete(query=delete_branch_query(id=id))

    async def delete_lecture(self, *, id) -> str:
        return await self.__delete(query=delete_lecture_query(id=id))

    async def delete_theory(self, *, id) -> str:
        return await self.__delete(query=delete_theory_query(id=id))

    async def delete_practice(self, *, id) -> str:
        return await self.__delete(query=delete_practice_query(id=id))

    async def delete_book(self, *, id) -> str:
        return await self.__delete(query=delete_book_query(id=id))

    async def delete_game(self, *, id) -> str:
        return await self.__delete(query=delete_game_query(id=id))

    async def delete_video(self, *, id) -> str:
        """Deletes video. Video does not have to have object_key!"""
        response = await self._fetch_one(query=delete_video_query(id=id))
        return response['object_key'] if response else None

    async def delete_quiz(self, *, fk) -> str:
        """Deletes quiz entirely and returns list of deleted object_keys."""
        records = await self._fetch_many(query=delete_quiz_query(fk=fk))
        return [record['object_key'] for record in records if record['object_key']]

    async def delete_quiz_question(self, *, id) -> str:
        """Deletes quiz. Quiz does not have to have object_key!"""
        response = await self._fetch_one(query=delete_quiz_question_query(id=id))
        return response['object_key'] if response else None

    async def delete_block_question(self, *, id) -> str:
        response = await self._fetch_one(query=delete_block_question_query(id=id))
        return None

    async def __delete(self, *, query):
        """Executes query and tries to return deleted object_key or raise HTTPException"""
        response = await self._fetch_one(query=query)
        if not response['object_key']:
            raise HTTPException(status_code=404, detail="Trying to delete returned nothing.")
        return response['object_key']
