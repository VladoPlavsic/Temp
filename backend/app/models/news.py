from typing import List, Dict, Optional

from app.models.core import BaseModel

class NewsCoreModel(BaseModel):
    date: str
    title: str
    short_desc: str
    object_key: str
    preview_image_url: str

class NewsImagesCore(BaseModel):
    order: int
    url: str
    object_key: str

class NewsImagesInDB(NewsImagesCore):
    pass

class NewsImagesCreate(NewsImagesCore):
    pass

class NewsPostModel(NewsCoreModel):
    images: list
    content: str

class NewsCreateModel(NewsCoreModel):
    content: str
    images: list

class NewsPreviewInDBModel(NewsCoreModel):
    id: int

class NewsInDBModel(NewsCoreModel):
    id: int
    content: str
    images: list

class NewsResponseModel(BaseModel):
    count: int
    news: List[NewsPreviewInDBModel]

class NewsUpdateModel(BaseModel):
    id: int
    date: Optional[str]
    title: Optional[str]
    short_desc: Optional[str]
    content: Optional[str]
    images: Optional[list]
    object_key: Optional[str]
    preview_image_url: Optional[str]

class NewsImagesAllModel(BaseModel):
    object_key: str

class NewsAllModel(BaseModel):
    object_key: str
