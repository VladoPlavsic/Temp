from typing import List, Optional
from datetime import datetime
from app.models.core import DBCoreModel

# ###
# Presentation models
# ###

class PresentationModelCore(DBCoreModel):
    pass

class PresentationCreateModelCheck(DBCoreModel):
    fk: int

class PresentationCreateModel(PresentationModelCore):
    fk: int
    object_key: str

class PresentationMediaCore(DBCoreModel):
    order: int
    url: str
    object_key: str

class PresentationMediaInDB(PresentationMediaCore):
    pass

class PresentationMediaCreate(PresentationMediaCore):
    fk: int

class PresentationMasterInDB(PresentationModelCore):
    id: int

class PresentationInDB(PresentationMasterInDB):
    images: List[PresentationMediaInDB]
    audio: List[PresentationMediaInDB]

# ###
# Book models
# ###

class BookModelCore(DBCoreModel):
    name_ru: str
    description: str

class BookPostModelCheck(DBCoreModel):
    fk: int

class BookPostModel(BookModelCore):
    fk: int
    object_key: str

class BookCreateModel(BookPostModel):
    url: str

class BookInDB(BookModelCore):
    id: int
    url: str
    object_key: str

# ###
# Video models
# ###

class VideoModelCore(DBCoreModel):
    pass

class VideoPostModelYT(VideoModelCore):
    fk: int
    url: str

class VideoPostModelCDNCheck(DBCoreModel):
    fk: int

class VideoPostModelCDN(VideoModelCore):
    fk: int
    object_key: str

class VideoCreateModel(VideoModelCore):
    fk: int
    url: str
    object_key: Optional[str]

class VideoInDB(VideoModelCore):
    id: int
    url: str
    object_key: Optional[str]

# ###
# Game models
# ###

class GameModelCore(DBCoreModel):
    name_ru: str
    description: str
    object_key: str

class GamePostModelCheck(DBCoreModel):
    fk: int

class GamePostModel(GameModelCore):
    fk: int

class GameCreateModel(GameModelCore):
    fk: int
    url: str

class GameInDB(GameModelCore):
    id: int
    url: str

# ###
# Quiz models
# ###
class AnswerCoreModel(DBCoreModel):
    answer: str
    is_true: Optional[bool]
class OptionCoreModel(DBCoreModel):
    question: str
    answer: str

class AnswersInDB(AnswerCoreModel):
    question_id: int
    answer_id: int

class QuizModelCore(DBCoreModel):
    lecture_id: int
    order_number: Optional[int]
    question_type: str
    question: Optional[str]
    object_key: Optional[str]
    answers: Optional[List[AnswerCoreModel]]
    options: Optional[List[OptionCoreModel]]
    image_size: Optional[str]

class QuizPostModelCheck(DBCoreModel):
    fk: int
    order_number: int

class QuizPostModel(QuizModelCore):
    pass

class QuizCreateModel(QuizModelCore):
    image_url: Optional[str]

class QuestionInDB(DBCoreModel):
    id: int
    fk: int
    order_number: int
    question: Optional[str]
    object_key: Optional[str]
    image_url: Optional[str]

class QuizQuestionInDB(QuestionInDB):
    answers: List[AnswersInDB]

class QuizInDB(DBCoreModel):
    questions: List[QuizQuestionInDB]
class QuizResponse(DBCoreModel):
    id: int
    fk: int
    order_number: Optional[int]
    question_type: str
    question: Optional[str]
    object_key: Optional[str]
    image_url: Optional[str]
    answers: Optional[List[AnswerCoreModel]]
    options: Optional[List[OptionCoreModel]]
    image_size: Optional[str]

class QuizQuestionAnswerPair(DBCoreModel):
    question: int
    answer: int

class QuizGetResultsModel(DBCoreModel):
    id: int
    # results: List[QuizQuestionAnswerPair]
    # lecture_id: int

class QuizQuestionAnswerCorrectPair(DBCoreModel):
    question_id: int
    answer_id: int
    question_number: int
    answer: str
    correct: bool
    correct_answer: str
    correct_answer_id: int

class QuizResults(DBCoreModel):
    results: List[QuizQuestionAnswerCorrectPair]
    lecture_id: int

# ###
# Structure models
# ###
class GradeCoreModel(DBCoreModel):
    name_en: str
    name_ru: str
    object_key: str
    order_number: int

class GradeInDB(GradeCoreModel):
    id: int
    background: str

# subjects
class SubjectGetModel(DBCoreModel):
    grade_name_en: str

class SubjectCoreModel(DBCoreModel):
    name_ru: str
    object_key: str

class SubejctPostModelCheck(DBCoreModel):
    name_ru: str

class SubejctPostModel(SubjectCoreModel):
    pass

class SubjectCreateModel(SubjectCoreModel):
    background: str

class SubjectInDB(SubjectCoreModel):
    id: int
    background: str

# subject response
class SubjectResponse(DBCoreModel):
    subjects: List[SubjectInDB]

# branches
class BranchGetModel(DBCoreModel):
    grade_name_en: str
    subject_name_en: str

class BranchCoreModel(DBCoreModel):
    name_ru: str
    object_key: str
    # order_number: int

class BranchPostModelCheck(DBCoreModel):
    name_ru: str

class BranchPostModel(BranchCoreModel):
    pass

class BranchCreateModel(BranchCoreModel):
    background: str

class BranchInDB(BranchCoreModel):
    id: int
    background: str

class BranchPreResponse(BranchInDB):
    complete: int

# branch response
class BranchResponse(DBCoreModel):
    branches: List[BranchPreResponse]

# lectures
class LectureGetModel(DBCoreModel):
    subject_name_en: str
    branch_name_en: str

class LectureCoreModel(DBCoreModel):
    fk: int
    name_ru: str
    description: str
    order_number: int

class LecturePostModelCheck(DBCoreModel):
    fk: int
    name_ru: str

class LecturePostModel(LectureCoreModel):
    pass

class LectureCreateModel(LectureCoreModel):
    pass

class LectureInDB(LectureCoreModel):
    id: int
    background: str

class LecturePreResponse(LectureInDB):
    complete: bool

# lecture response
class LectureResponse(DBCoreModel):
    fk: int
    lectures: List[LecturePreResponse]


class Ru1Question(DBCoreModel):
    word: str
    video: str
    audio: str
class Ru1(DBCoreModel):
    id: int
    type: str = 'text_audio'
    heading: str
    description: str
    questions: List[dict]
    object_key: str = None
    order_number: int = None

class Ru2Question(DBCoreModel):
    russian_word: str
    english_word: str
    image: str
class Ru2(DBCoreModel):
    id: int
    type: str = 'translation'
    heading: str
    description: str
    questions: List[dict]
    object_key: str = None
    order_number: int = None

class Ru3Answer(DBCoreModel):
    answer: str
    is_true: bool
class Ru3Question(DBCoreModel):
    audio: str
    answers: List[Ru3Answer]
class Ru3(DBCoreModel):
    id: int
    type: str = 'phrase_playback_test'
    heading: str
    description: str
    questions: List[dict]
    object_key: str = None
    order_number: int = None

class Ru4Question(DBCoreModel):
    audio: str
    answer: str
class Ru4(DBCoreModel):
    id: int
    type: str = 'phrase_playback_self'
    heading: str
    description: str
    questions: List[dict]
    object_key: str = None
    order_number: int = None

class Ru5(DBCoreModel):
    id: int
    type: str = 'video'
    heading: str
    description: str
    video: str
    object_key: str = None
    order_number: int = None

class Ru6Question(DBCoreModel):
    words: str
    audio: str
    transcriptions: str
class Ru6(DBCoreModel):
    id: int
    type: str = 'transcription'
    heading: str
    description: str
    questions: List[dict]
    object_key: str = None
    order_number: int = None

class Ru7Question(DBCoreModel):
    video: str
    letters: List[str]
class Ru7(DBCoreModel):
    id: int
    type: str = 'articulation'
    heading: str
    description: str
    questions: List[dict]
    object_key: str = None
    order_number: int = None

class Ru8Question(DBCoreModel):
    question: str
    answer: str
class Ru8(DBCoreModel):
    id: int
    type: str = 'matching'
    heading: str
    description: str
    questions: List[dict]
    object_key: str = None
    order_number: int = None

class Ru9Question(DBCoreModel):
    question: str
    answer: str
class Ru9(DBCoreModel):
    id: int
    type: str = 'text_answer'
    heading: str
    description: str
    questions: List[dict]
    object_key: str = None
    order_number: int = None

class Ru10Question(DBCoreModel):
    audio: str
    texts: List[str]
    answer: str
class Ru10(DBCoreModel):
    id: int
    type: str = 'right_order'
    heading: str
    description: str
    questions: List[dict]
    object_key: str = None
    order_number: int = None

class Ru11(DBCoreModel):
    id: int
    type: str = 'theory'
    heading: str
    items: List[str]
    object_key: str = None
    order_number: int = None

class RuModel(DBCoreModel):
    id: int = None
    fk: int
    type: str
    heading: str = None
    description: str = None
    video: str = None
    items: List[str] = None
    questions: List[dict] = None
    object_key: str = None
    order_number: int = None

# material response
class MaterialResponseModel(DBCoreModel):
    video: Optional[VideoInDB]
    game: Optional[GameInDB]
    book: Optional[BookInDB]
    quiz: Optional[List[QuizResponse]]
    practice: Optional[PresentationInDB]
    theory: Optional[PresentationInDB]
    blocks: Optional[List[Ru1 or Ru2 or Ru3 or Ru4 or Ru5 or Ru6 or Ru7 or Ru8 or Ru9 or Ru10 or Ru11]]

class MaterialBulk(DBCoreModel):
    # video
    video_url: str
    video_name_ru: str
    video_description: str
    video_key: Optional[str]
    # game
    game_url: str
    game_name_ru: str
    game_description: str
    # theory
    theory_name_ru: str
    theory_description: str
    theory_key: str
    # practice
    practice_name_ru: str
    practice_description: str
    practice_key: str
    # book
    book_url: str
    book_name_ru: str
    book_key: str
    book_description: str

class MaterialResponse(DBCoreModel):
    fk: int
    material: MaterialResponseModel

# ###
# select all
# ###
class StructureAllModel(DBCoreModel):
    id: int
    object_key: str

class MaterialAllModel(DBCoreModel):
    id: int
    object_key: str

class AudioImagesAllModel(DBCoreModel):
    order: int
    object_key: str

# Update models
class UpdateBaseModel(DBCoreModel):
    id: int
    name_ru: Optional[str]

class UpdateVideoModel(UpdateBaseModel):
    description: Optional[str]
    url: Optional[str]

class UpdateGameModel(UpdateBaseModel):
    description: Optional[str]
    url: Optional[str]

class UpdateLectureModel(UpdateBaseModel):
    description: Optional[str]
    order_number: Optional[int]

class UpdateStructureModel(UpdateBaseModel):
    object_key: Optional[str]

class UpdateBookModel(UpdateBaseModel):
    description: Optional[str]

class UpdatePresentationModel(UpdateBaseModel):
    description: Optional[str]

# ###
# Subscriptions
# ###
class SubscriptionsBase(DBCoreModel):
    name: str
    price: float
    month_count: int

class OfferDetails(DBCoreModel):
    id: int
    product_fk: int
    subscription_fk: int

class CreateSubjectSubscriptionPlan(SubscriptionsBase):
    pass

class AvailableSubjectSubscriptionPlans(SubscriptionsBase):
    id: int

class AvailableSubjectSubscriptionOffers(SubscriptionsBase):
    id: int
    plan_id: int
    subject_id: int
    grade_id: int
    name_en: str
    name_ru: str

class PaymentRequestDetails(DBCoreModel):
    user_fk: int
    offer_fk: int
    payment_id: str
    level: bool
    confirmation_token: str
