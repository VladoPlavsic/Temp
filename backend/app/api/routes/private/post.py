import re
import json

from fastapi import APIRouter
from fastapi import Depends, Body
from starlette.status import HTTP_201_CREATED, HTTP_200_OK

from app.db.repositories.private.private import PrivateDBRepository
from app.cdn.repositories.private.private import PrivateYandexCDNRepository

from app.api.dependencies.database import get_db_repository
from app.api.dependencies.cdn import get_cdn_repository

from app.api.dependencies.auth import allowed_or_denied, get_user_from_cookie_token

from app.cdn.types import DefaultFormats

# ###
# Request models
# ###
# material
from app.models.private import PresentationCreateModel, PresentationCreateModelCheck
from app.models.private import BookPostModel, BookCreateModel, BookPostModelCheck, RuModel
from app.models.private import VideoPostModelYT, VideoPostModelCDN, VideoCreateModel, VideoPostModelCDNCheck
from app.models.private import GamePostModel, GameCreateModel, GamePostModelCheck
from app.models.private import QuizPostModel, QuizCreateModel, QuizGetResultsModel, QuizPostModelCheck
# structure
from app.models.private import BranchPostModel, BranchCreateModel, BranchPostModelCheck
from app.models.private import LecturePostModel, LectureCreateModel, LecturePostModelCheck

# ###
# Response models
# ###
from app.models.core import AllowCreate
# material
from app.models.private import PresentationInDB
from app.models.private import BookInDB
from app.models.private import VideoInDB
from app.models.private import GameInDB
from app.models.private import QuizQuestionInDB, QuizResults, QuizResponse
# structure
from app.models.private import BranchInDB
from app.models.private import LectureInDB

router = APIRouter()


# STRUCTURE
@router.post("/branch/check", response_model=AllowCreate, name="private:post-practice-check", status_code=HTTP_200_OK)
async def check_create_private_branch(
    branch: BranchPostModelCheck = Body(...),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
) -> AllowCreate:
    """Try creating branch. If OK is returned {OK: True}, practice can be created, else there is something wrong with it."""
    response = await db_repo.insert_branch_check(**branch.dict())

    return AllowCreate(OK=response)

@router.post("/branch", response_model=BranchInDB, name="private:post-branch", status_code=HTTP_201_CREATED)
async def create_private_branch(
    branch: BranchPostModel = Body(...),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    cdn_repo: PrivateYandexCDNRepository = Depends(get_cdn_repository(PrivateYandexCDNRepository)),
    allowed: bool = Depends(allowed_or_denied),
) -> BranchInDB:
    background = cdn_repo.get_background_url(object_key=branch.object_key)
    response  = await db_repo.insert_branch(branch=BranchCreateModel(**branch.dict(), background=background))

    return response

@router.post("/lecture/check", response_model=AllowCreate, name="private:post-practice-check", status_code=HTTP_200_OK)
async def check_create_private_lecture(
    lecture: LecturePostModelCheck = Body(...),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
) -> AllowCreate:
    """Try creating lecture. If OK is returned {OK: True}, practice can be created, else there is something wrong with it."""
    response = await db_repo.insert_lecture_check(**lecture.dict())

    return AllowCreate(OK=response)

@router.post("/lecture", response_model=LectureInDB, name="private:post-lecture", status_code=HTTP_201_CREATED)
async def create_private_lecture(
    lecture: LecturePostModel = Body(...),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    # cdn_repo: PrivateYandexCDNRepository = Depends(get_cdn_repository(PrivateYandexCDNRepository)),
    allowed: bool = Depends(allowed_or_denied),
) -> LectureInDB:
    response  = await db_repo.insert_lecture(lecture=LectureCreateModel(**lecture.dict()))

    return response

# CONTENT
@router.post("/practice/check", response_model=AllowCreate, name="private:post-practice-check", status_code=HTTP_200_OK)
async def check_create_private_practice(
    presentation: PresentationCreateModelCheck = Body(...),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
) -> AllowCreate:
    """Try creating practice. If OK is returned {OK: True}, practice can be created, else there is something wrong with it."""
    response = await db_repo.insert_practice_check(fk=presentation.fk)

    return AllowCreate(OK=response)

@router.post("/practice", response_model=PresentationInDB, name="private:post-practice", status_code=HTTP_201_CREATED)
async def create_private_practice(
    presentation: PresentationCreateModel = Body(...),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    cdn_repo: PrivateYandexCDNRepository = Depends(get_cdn_repository(PrivateYandexCDNRepository)),
    allowed: bool = Depends(allowed_or_denied),
) -> PresentationInDB:
    images = cdn_repo.format_presentation_content(folder=presentation.object_key, fk=presentation.fk, type_=DefaultFormats.IMAGES)
    audio = cdn_repo.format_presentation_content(folder=presentation.object_key, fk=presentation.fk, type_=DefaultFormats.AUDIO)

    response = await db_repo.insert_practice(presentation=presentation, images=images, audio=audio)

    return response

@router.post("/theory/check", response_model=AllowCreate, name="private:post-practice-check", status_code=HTTP_200_OK)
async def check_create_private_theory(
    presentation: PresentationCreateModelCheck = Body(...),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
) -> AllowCreate:
    """Try creating theory. If OK is returned {OK: True}, practice can be created, else there is something wrong with it."""
    response = await db_repo.insert_theory_check(fk=presentation.fk)
    return AllowCreate(OK=response)

@router.post("/theory", response_model=PresentationInDB, name="private:post-theory", status_code=HTTP_201_CREATED)
async def create_private_theory(
    presentation: PresentationCreateModel = Body(...),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    cdn_repo: PrivateYandexCDNRepository = Depends(get_cdn_repository(PrivateYandexCDNRepository)),
    allowed: bool = Depends(allowed_or_denied),
) -> PresentationInDB:
    images = cdn_repo.format_presentation_content(folder=presentation.object_key, fk=presentation.fk, type_=DefaultFormats.IMAGES)
    audio = cdn_repo.format_presentation_content(folder=presentation.object_key, fk=presentation.fk, type_=DefaultFormats.AUDIO)

    response = await db_repo.insert_theory(presentation=presentation, images=images, audio=audio)

    return response

@router.post("/book/check", response_model=AllowCreate, name="private:post-practice-check", status_code=HTTP_200_OK)
async def check_create_private_book(
    book: BookPostModelCheck = Body(...),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
) -> AllowCreate:
    """Try creating book. If OK is returned {OK: True}, practice can be created, else there is something wrong with it."""
    response = await db_repo.insert_book_check(fk=book.fk)
    return AllowCreate(OK=response)

@router.post("/book", response_model=BookInDB, name="private:post-book", status_code=HTTP_201_CREATED)
async def create_private_book(
    book: BookPostModel = Body(...),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    cdn_repo: PrivateYandexCDNRepository = Depends(get_cdn_repository(PrivateYandexCDNRepository)),
    allowed: bool = Depends(allowed_or_denied),
) -> BookInDB:
    shared = cdn_repo.form_book_insert_data(folder=book.object_key)
    object_key = list(shared[0].keys())[0]
    url = shared[0][object_key]
    if url:
        url = re.sub(r'\?.*', '', url)
    book.object_key = object_key
    book = BookCreateModel(**book.dict(), url=url)
    response = await db_repo.insert_book(book=book)

    return response

@router.post("/video", response_model=VideoInDB, name="private:post-video", status_code=HTTP_201_CREATED)
async def create_private_video(
    video: VideoPostModelYT = Body(...),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    allowed: bool = Depends(allowed_or_denied),
) -> VideoInDB:
    video = VideoCreateModel(**video.dict(), object_key=None)
    response = await db_repo.insert_video(video=video)

    return response

@router.post("/game/check", response_model=AllowCreate, name="private:post-practice-check", status_code=HTTP_200_OK)
async def check_create_private_game(
    game: GamePostModelCheck = Body(...),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
) -> AllowCreate:
    """Try creating game. If OK is returned {OK: True}, practice can be created, else there is something wrong with it."""
    response = await db_repo.insert_game_check(fk=game.fk)
    return AllowCreate(OK=response)

@router.post("/game", response_model=GameInDB, name="private:post-game", status_code=HTTP_201_CREATED)
async def create_private_game(
    game: GamePostModel = Body(...),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    cdn_repo: PrivateYandexCDNRepository = Depends(get_cdn_repository(PrivateYandexCDNRepository)),
    allowed: bool = Depends(allowed_or_denied),
) -> GameInDB:
    shared = cdn_repo.form_game_insert_data(folder=game.object_key)
    object_key = list(shared[0].keys())[0]
    url = shared[0][object_key]
    if url:
        url = re.sub(r'\?.*', '', url)
    game.object_key = object_key
    response = await db_repo.insert_game(game=GameCreateModel(**game.dict(), url=url))

    return response

@router.post("/quiz/check", response_model=AllowCreate, name="private:post-practice-check", status_code=HTTP_200_OK)
async def check_create_private_quiz(
    quiz: QuizPostModelCheck = Body(...),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
) -> AllowCreate:
    """Try creating quiz. If OK is returned {OK: True}, practice can be created, else there is something wrong with it."""
    response = await db_repo.insert_quiz_check(fk=quiz.fk, order_number=quiz.order_number)
    return AllowCreate(OK=response)

@router.post("/quiz", response_model=QuizResponse, name="private:post-quiz", status_code=HTTP_201_CREATED)
async def create_private_quiz(
    quiz: QuizPostModel = Body(...),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    cdn_repo: PrivateYandexCDNRepository = Depends(get_cdn_repository(PrivateYandexCDNRepository)),
    allowed: bool = Depends(allowed_or_denied),
) -> QuizQuestionInDB:
    if quiz.object_key:
        shared = cdn_repo.form_quiz_insert_data(folder=quiz.object_key)
        object_key = list(shared[0].keys())[0]
        url = shared[0][object_key]
        if url:
            url = re.sub(r'\?.*', '', url)
        quiz.object_key = object_key
        quiz = QuizCreateModel(**quiz.dict(), image_url=url)
    else:
        quiz = QuizCreateModel(**quiz.dict(), image_url=None)

    res = await db_repo.insert_quiz_question(quiz_question=quiz)

    el = dict(res)
    el['answers'] = json.loads(res['answers']) if res.get('answers') else []
    el['options'] = json.loads(res['options']) if res.get('options') else []
    return QuizResponse(**el)

@router.post("/quiz/done", response_model=None, name="private:quiz-done", status_code=HTTP_200_OK)
async def get_quiz_results(
    quiz_results: QuizGetResultsModel = Body(...),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    user = Depends(get_user_from_cookie_token),
):
    return await db_repo.check_quiz_results(quiz_results=quiz_results, user=user.id)

# @router.post("/quiz/results", response_model=QuizResults, name="private:get-quiz-results", status_code=HTTP_200_OK)
# async def get_quiz_results(
#     quiz_results: QuizGetResultsModel = Body(...),
#     db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
#     allowed: bool = Depends(get_user_from_cookie_token),
# ) -> QuizResults:
#     return await db_repo.check_quiz_results(quiz_results=quiz_results)

@router.post("/block", response_model=RuModel, name="private:post-block", status_code=HTTP_201_CREATED)
async def create_private_block(
    block: RuModel = Body(...),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    cdn_repo: PrivateYandexCDNRepository = Depends(get_cdn_repository(PrivateYandexCDNRepository)),
    allowed: bool = Depends(allowed_or_denied),
) -> RuModel:
    block = RuModel(**block.dict())
    res = await db_repo.insert_block_question(block=block)
    el = dict(res)
    el['questions'] = json.loads(res['questions']) if res.get('questions') else []
    return RuModel(**el)
