import json
from typing import List

from app.models.private import PresentationMediaCreate
from app.db.repositories.parsers import string_or_null, list_to_string

import logging

logger = logging.getLogger(__name__)

# STRUCTURE queries
def insert_grade_check_query(name_en) -> str:
    return \
        f"SELECT private.grade_can_be_created({string_or_null(name_en)}) AS yes"

def insert_grades_query(name_en, name_ru, object_key, background, order_number) -> str:
    return \
        f"SELECT (private.insert_grade({string_or_null(name_en, name_ru, object_key, background)}, {order_number})).*"

def insert_subject_check_query(fk=1, name_en=None) -> str:
    return \
        f"SELECT private.subject_can_be_created({fk}, {string_or_null(name_en)}) AS yes"

def insert_subject_query(fk=1, name_en='-', name_ru='-', object_key='-', background='-', order_number=1) -> str:
    return \
        f"SELECT (private.insert_subject({fk}, {string_or_null(name_ru, name_ru, object_key, background)}, {order_number})).*"

def insert_branch_check_query(fk=1, name_en=None) -> str:
    return \
        f"SELECT private.branch_can_be_created({fk}, {string_or_null(name_en)}) AS yes"

def insert_branch_query(fk=1, name_en='-', name_ru='-', object_key='-', background='-', order_number=1) -> str:
    return \
        f"SELECT (private.insert_branch({fk}, {string_or_null(name_ru, name_ru, object_key, background)}, {order_number})).*"

def insert_lecture_check_query(fk, name_en) -> str:
    return \
        f"SELECT private.lecture_can_be_created({fk}, {string_or_null(name_en)}) AS yes"

def insert_lecture_query(fk, name_en='-', name_ru='-', description='-', object_key='-', background='-', order_number=1) -> str:
    return \
        f"SELECT (private.insert_lecture({fk}, {string_or_null(name_ru, name_ru, description, object_key, background)}, {order_number})).*"

# MATERIAL queries
def insert_video_check_query(fk) -> str:
    return \
        f"SELECT private.video_can_be_created({fk}) AS yes"

def insert_video_query(fk, name_ru='-', description='-', object_key=None, url=None) -> str:
    return \
        f"SELECT (private.insert_video({fk}, {string_or_null(name_ru, description, object_key, url)})).*"

def insert_game_check_query(fk) -> str:
    return \
        f"SELECT private.game_can_be_created({fk}) AS yes"

def insert_game_query(fk, name_ru, description, url, object_key) -> str:
    return \
        f"SELECT (private.insert_game({fk}, {string_or_null(name_ru, description, url, object_key)})).*"

def insert_quiz_query(lecture_id, question_type, order_number=None, image_url=None, question=None, object_key=None, answers=None, options=None, image_size=None) -> str:
    if not image_size:
        image_size = 'null'
    else:
        image_size = f"'{image_size}'"

    js1 = json.dumps(answers or []).replace("'", "''")
    js2 = json.dumps(options or []).replace("'", "''")

    return \
        f"INSERT INTO private.quiz (fk, order_number, question_type, question, object_key, image_url, answers, options, image_size) VALUES ({string_or_null(lecture_id, order_number or 1, question_type, question, object_key, image_url)}, '{js1}'::JSONB, '{js2}'::JSONB, {image_size}) RETURNING *"

def insert_block_pre_query(id, fk, type, heading=None, description=None, video=None, items=None, questions=None, object_key=None, order_number=None) -> str:
    js1 = json.dumps(questions or []).replace("'", "''")
    return \
        f"INSERT INTO private.blocks (fk, type, heading, description, video, items, questions, object_key, order_number) VALUES ({string_or_null(fk, type, heading, description, video or '-', items or '{}')}, '{js1}'::JSONB, {string_or_null(object_key, order_number)}) RETURNING *"

def insert_book_check_query(fk) -> str:
    return \
        f"SELECT private.book_can_be_created({fk}) AS yes"

def insert_book_query(fk, name_ru, description, object_key, url) -> str:
    return \
        f"SELECT (private.insert_book({fk}, {string_or_null(name_ru, description, object_key, url)})).*"

def insert_practice_check_query(fk) -> str:
    return \
        f"SELECT private.practice_can_be_created({fk}) AS yes"

def insert_theory_check_query(fk) -> str:
    return \
        f"SELECT private.theory_can_be_created({fk}) AS yes"

def insert_presentation_query(table, fk, name_ru='-', description='-', object_key=None) -> str:
    """Creates insert query for presentation.

    Keyword arguments:
    table       -- table we are trying to insert into. (practice || theory)
    fk          -- lecture id (id of lecture we are adding material to)
    name_ru     -- presentation name
    description -- presentation description
    object_key  -- presentation object_key in cdn
    """

    return \
        f"SELECT (private.insert_{table}({fk}, {string_or_null(name_ru, description, object_key)})).*"

def insert_presentation_media_query(table, media_type , medium: List[PresentationMediaCreate]) -> str:
    """Creates insert query for presentation data.

    table      -- table we are trying to insert into. (practice || theory)
    media_type -- presentation content type (image || audio)
    medium     -- List of PresentationMediaCreate
    """
    foreign_keys, order_numbers, urls, keys = map(list, zip( *((media.fk, media.order, media.url, media.object_key) for media in medium)))

    foreign_keys = ','.join(map(str,foreign_keys))
    order_numbers = ','.join(map(str,order_numbers))
    urls = ','.join(map(str,urls))
    keys = ','.join(map(str,keys))

    return \
        f"SELECT (private.insert_{table}_{media_type}('{{{foreign_keys}}}'::int[], '{{{order_numbers}}}'::int[], '{{{urls}}}', '{{{keys}}}')).*"

def insert_quiz_check_query(fk, order_number) -> str:
    return \
        f"SELECT private.quiz_can_be_created({fk}, {order_number}) AS yes"

def insert_quiz_question_query(lecture_id: int, order_number: int, question: str, object_key: str, image_url: str, answers: List[str], is_true: List[bool]) -> str:
    answers = list_to_string(answers)
    is_true = list_to_string(is_true)
    return \
        f"SELECT (private.insert_quiz_question({lecture_id}, {order_number}, {string_or_null(question, object_key, image_url)}, '{{{answers}}}', '{{{is_true}}}')).*"

def insert_quiz_question_answers_query(question_id: int, answers: List[str], is_true: List[bool]) -> str:
    answers = list_to_string(answers)
    is_true = list_to_string(is_true)
    return \
        f"SELECT (private.insert_quiz_answers({question_id}, '{{{answers}}}', '{{{is_true}}}')).*"
