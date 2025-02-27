import json
from typing import List, Tuple, Union
from fastapi import HTTPException
from app.db.repositories.base import BaseDBRepository

# queries
from app.db.repositories.private.select.queries import *

# response models
from app.models.private import GradeInDB
from app.models.private import SubjectInDB
from app.models.private import BranchInDB, BranchPreResponse
from app.models.private import LectureInDB, LecturePreResponse
from app.models.private import MaterialResponseModel

from app.models.user import UserAvailableGrades
from app.models.user import UserAvailableSubjects

from app.models.private import VideoInDB
from app.models.private import GameInDB
from app.models.private import BookInDB
from app.models.private import QuizInDB, QuizQuestionInDB, AnswersInDB, QuizGetResultsModel, QuizResults, QuizQuestionAnswerCorrectPair, QuizResponse, RuModel
from app.models.private import PresentationInDB
from app.models.private import PresentationMediaInDB

from app.models.private import StructureAllModel
from app.models.private import MaterialAllModel
from app.models.private import AudioImagesAllModel

from app.db.repositories.types import ContentType

import logging


logger = logging.getLogger(__name__)


async def get_branch_progress(self, id, user):
    try:
        res = await self._fetch_many(
            query=(
                f"SELECT id FROM private.lecture"
                f" WHERE fk = {id}"
            ),
        )
        lectures = [i['id'] for i in res]
        complete = 0
        for lecture in lectures:
            if await get_lecture_progress(self, lecture, user):
                complete += 1
        return round(complete * 100 / len(lectures))
    except:
        return 100

async def get_lecture_progress(self, id, user):
    try:
        res = await self._fetch_one(
            query=(
                f"SELECT true FROM private.users_quiz"
                f" WHERE quiz_id = {id} AND user_id = {user}"
            ),
        )
        return bool(res)
        # res = await self._fetch_many(
        #     query=(
        #         f"SELECT id FROM private.quiz"
        #         f" WHERE fk = {id}"
        #     ),
        # )
        # quizes = [i['id'] for i in res]
        # complete = await self._fetch_many(
        #     query=(
        #         f"SELECT quiz_id FROM private.users_quiz"
        #         f" WHERE quiz_id IN ({','.join(map(str, quizes))}) AND user_id = {user}"
        #     ),
        # )
        # complete = [i['quiz_id'] for i in complete]
        # return all(i in complete for i in quizes)
    except:
        return True


class PrivateDBSelectRepository(BaseDBRepository):
    """Connector allowing select data from private database schema"""
    # STRUCTURE
    async def get_grade_by_name(self, *, grade_name) -> GradeInDB:
        """Returns GradeInDB based on grades name_en."""
        response = await self._fetch_one(query=get_grade_by_name_query(grade_name=grade_name))
        if not response:
            raise HTTPException(status_code=404, detail="Didn't find any grades with given name.")
        return GradeInDB(**response)

    async def get_subject_by_name(self, *, subject_name) -> Tuple[SubjectInDB, str]:
        response = await self._fetch_one(query=get_subject_by_name_query(subject_name=subject_name))
        if not response:
            raise HTTPException(status_code=404, detail="Didn't find any subjects with given name.")
        return SubjectInDB(**response)

    async def get_branch_by_name(self, *, subject_name, branch_name) -> Tuple[BranchInDB, str]:
        """Returns (BranchInDB, grades name_ru concatinated with subjects name_ru via / [path])"""
        (subject, path) = await self.get_subject_by_name(subject_name=subject_name)

        response = await self._fetch_one(query=get_branch_by_name_query(fk=subject.id, branch_name=branch_name))
        if not response:
            raise HTTPException(status_code=404, detail="Didn't find any branches with given name.")
        return BranchInDB(**response), path + '/' + subject.name_ru

    async def get_lecture_by_name(self, *, grade_name, subject_name, branch_name, lecture_name) -> Tuple[LectureInDB, str]:
        """Returns (LetureInDB, grades name_ru concatinated with subjects name_ru and branches name_ru via / [path])"""
        (branch, path) = await self.get_branch_by_name(grade_name=grade_name, subject_name=subject_name, branch_name=branch_name)

        response = await self._fetch_one(query=get_lecture_by_name_query(fk=branch.id, lecture_name=lecture_name))
        if not response:
            HTTPException(status_code=404, detail="Didn't find any lectures with given name.")
        return LectureInDB(**response), path + '/' + branch.name_ru

    async def select_grades(self, *, identifications=None) -> List[GradeInDB]:
        """Returns list of grades available to customer based on grade ID's"""
        response_data = await self._fetch_many(query=select_grades_query(identifications=identifications))
        return [GradeInDB(**data) for data in response_data]

    async def select_all_grades(self) -> List[StructureAllModel]:
        """Returns list of id, object_keys for all grades in database"""
        records = await self._fetch_many(query=select_all_grade_keys_query())
        return [StructureAllModel(**record) for record in records]

    async def select_subjects(self, *, fk=1, identifications=None) -> List[SubjectInDB]:
        """Returns list of subjects available to customer based on subject ID's"""
        response_data = await self._fetch_many(query=select_subject_query(fk=fk, identifications=identifications))
        return [SubjectInDB(**data) for data in response_data]

    async def select_all_subjects(self) -> List[StructureAllModel]:
        """Returns list of id, object_keys for all subjects in database"""
        records = await self._fetch_many(query=select_all_subject_keys_query())
        return [StructureAllModel(**record) for record in records]

    async def select_branches(self, *, fk=1, user=None) -> List[BranchInDB]:
        """Returns all branches based on fk they refer to"""
        response_data = await self._fetch_many(query=select_branch_query(fk=fk))
        return [BranchPreResponse(**data, complete=await get_branch_progress(self, data['id'], user.id)) for data in response_data]

    async def select_all_branches(self) -> List[StructureAllModel]:
        """Returns list of id, object_keys for all branches in database"""
        records = await self._fetch_many(query=select_all_branch_keys_query())
        return [StructureAllModel(**record) for record in records]

    async def select_lectures(self, *, fk, user) -> List[LectureInDB]:
        """Returns all lectures based on fk they refer to"""
        response_data = await self._fetch_many(query=select_lecture_query(fk=fk))
        return [LecturePreResponse(**data, complete=await get_lecture_progress(self, data['id'], user.id)) for data in response_data]

    async def select_all_lectures(self) -> List[StructureAllModel]:
        """Returns list of id, object_keys for all lectures in database"""
        records = await self._fetch_many(query=select_all_lecture_keys_query())
        return [StructureAllModel(**record) for record in records]

    # MATERIAL
    async def select_material(self, *, fk) -> MaterialResponseModel:
        """Returns all material from a lecture they belong to. Lecture is determined by fk."""
        video = await self.select_video(fk=fk)
        book = await self.select_book(fk=fk)
        game = await self.select_game(fk=fk)
        quiz = await self.select_quiz(fk=fk)
        theory = await self.select_presentation(fk=fk, presentation=ContentType.THEORY)
        practice = await self.select_presentation(fk=fk, presentation=ContentType.PRACTICE)
        blocks = await self.select_blocks(fk=fk)

        return MaterialResponseModel(
            video=video,
            book=book,
            game=game,
            quiz=quiz,
            theory=theory,
            practice=practice,
            blocks=blocks,
        )

    async def select_video(self, *, fk) -> VideoInDB:
        """Returns VideoInDB for a given lecture. Or None if there is none."""
        response = await self._fetch_one(query=select_one_material_query(fk=fk, table=ContentType.VIDEO.value))
        return VideoInDB(**response) if response else None

    async def select_all_video(self) -> List[MaterialAllModel]:
        """Returns list of id, object_keys for all video in database"""
        records = await self._fetch_many(query=select_all_material_keys_query(table=ContentType.VIDEO.value))
        return [MaterialAllModel(**record) for record in records if record["object_key"]]

    async def select_all_game(self) -> List[MaterialAllModel]:
        """Returns list of id, object_keys for all games in database"""
        records = await self._fetch_many(query=select_all_material_keys_query(table=ContentType.GAME.value))
        return [MaterialAllModel(**record) for record in records if record["object_key"]]

    async def select_quiz(self, *, fk) -> QuizInDB:
        """Returns QuizInDB based on lecture fk. If there is no quiz for given lecture, return None."""
        responses = await self._fetch_many(query=select_quiz_questions_query(fk=fk))

        # questions = [QuizQuestionInDB(**response, answers=[]) for response in responses]
        # for question in questions:
        #     responses = await self._fetch_many(query=select_quiz_answers_query(fk=question.id))
        #     question.answers = [AnswersInDB(**response) for response in responses]

        for i, el in enumerate(responses):
            ele = dict(el)
            ele['answers'] = json.loads(el['answers']) if el.get('answers') else []
            ele['options'] = json.loads(el['options']) if el.get('options') else []
            responses[i] = ele

        return [QuizResponse(**res) for res in responses]

    async def select_blocks(self, *, fk):
        """Returns QuizInDB based on lecture fk. If there is no quiz for given lecture, return None."""
        responses = await self._fetch_many(query=select_blocks_query(fk=fk))

        for i, el in enumerate(responses):
            ele = dict(el)
            ele['questions'] = json.loads(el['questions']) if el.get('questions') else []
            responses[i] = ele

        return [RuModel(**res) for res in responses]

    async def select_all_quiz(self) -> List[MaterialAllModel]:
        """Returns list of id, object_keys for all quizes in database"""
        records = await self._fetch_many(query=select_all_material_keys_query(table='quiz_question'))
        return [MaterialAllModel(**record) for record in records if record["object_key"]]

    async def select_book(self, *, fk) -> BookInDB:
        """Returns BookInDB for a given lecture. Or None if there is none."""
        response = await self._fetch_one(query=select_one_material_query(fk=fk, table=ContentType.BOOK.value))
        return BookInDB(**response) if response else None

    async def select_all_books(self) -> List[MaterialAllModel]:
        """Returns list of id, object_keys for all books in database"""
        records = await self._fetch_many(query=select_all_material_keys_query(table=ContentType.BOOK.value))
        return [MaterialAllModel(**record) for record in records]

    async def select_game(self, *, fk) -> GameInDB:
        """Returns GameInDB for a given lecture. Or None if there is none."""
        response = await self._fetch_one(query=select_one_material_query(fk=fk, table=ContentType.GAME.value))
        return GameInDB(**response) if response else None

    async def select_presentation(self, *, fk, presentation: ContentType) -> PresentationInDB:
        """Return presentation data - PresentationInDB based on presentation type and lecture they belong to."""
        master = await self._fetch_one(query=select_one_material_query(fk=fk, table=presentation.value))
        images = await self.__select_presentation_parts(fk=fk, presentation=presentation, media_type=ContentType.IMAGE)
        audio = await self.__select_presentation_parts(fk=fk, presentation=presentation, media_type=ContentType.AUDIO)
        return PresentationInDB(**master, images=images, audio=audio,) if master else None

    async def __select_presentation_parts(self, *, fk, presentation: ContentType, media_type: ContentType) -> List[PresentationMediaInDB]:
        """Return PresentationMediaInDB based on presentation and media type as well as lecture they belong to."""
        medium = await self._fetch_many(query=select_material_parts_query(fk=fk, presentation=presentation.value, media_type=media_type.value))
        return [PresentationMediaInDB(**media) for media in medium]

    async def select_all_presentation_parts(self, presentation: ContentType, media_type: ContentType) -> List[AudioImagesAllModel]:
        """Returns list of order, object_keys for all presentation (theory || practice) parts (images|| audio) in database"""
        records = await self._fetch_many(query=select_all_material_part_keys_query(presentation=presentation.value, media_type=media_type.value))
        return [AudioImagesAllModel(**record) for record in records]

    # USERS AVAILABLE CONTENT
    async def select_user_available_grades(self, *, user_id: int) -> List[UserAvailableGrades]:
        """Return all user available grades - UserAvaialableGrades - based on user_id."""
        records = await self._fetch_many(query=select_all_user_available_grades_query(user_id=user_id))
        return [UserAvailableGrades(**record) for record in records]

    async def select_user_available_subjects(self, *, user_id: int) -> List[UserAvailableSubjects]:
        """Return all user available subjects - UserAvaialableSubjects - based on user_id."""
        records = await self._fetch_many(query=select_all_user_available_subjects_query(user_id=user_id))
        return [UserAvailableSubjects(**record) for record in records]

    # QUIZ RESULTS
    async def check_quiz_results(self, *, quiz_results: QuizGetResultsModel, user) -> QuizResults:
        records = await self._fetch_one(query=check_quiz_results_query(quiz=quiz_results.id, user=user))
        # """Checks quiz results, and returns QuizResults object."""
        # questions = []
        # answers = []
        # for result in quiz_results.results:
        #     questions.append(result.question)
        #     answers.append(result.answer)

        # records = await self._fetch_one(query=check_quiz_results_query(questions=questions, answers=answers))
        # response = []

        # for index in range(0, len(records['question_ids'])):
        #     response.append(QuizQuestionAnswerCorrectPair(
        #         question_id=records['question_ids'][index],
        #         answer_id=records['answer_ids'][index],
        #         question_number=records['question_numbers'][index],
        #         answer=records['answers'][index],
        #         correct=records['correct'][index],
        #         correct_answer=records['correct_answers'][index],
        #         correct_answer_id=records['correct_answers_id'][index],
        #     ))

        return None

    async def check_if_content_available(self, *, user_id: int, subject_name: str) -> bool:
        """Checks if requested content is available to user requesting it.

        Keyword arguments:
        user_id      -- ID of user requesting given content
        grade_name   -- english name of a grade content belongs to
        subject_name -- english name of a subject content belongs to
        """
        available = await self._fetch_one(query=check_if_content_available_query(user_id=user_id, subject_name=subject_name))
        return available['available']
