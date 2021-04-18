from typing import List, Dict

from app.models.core import BaseModel

class NewsCoreModel(BaseModel):
    date: str
    title: str
    short_desc: str
    content: str
    url: str
    cloud_key: str

class NewsImagesCore(BaseModel):
    order: int
    url: str
    cloud_key: str

class NewsImagesInDB(NewsImagesCore):
    pass

class NewsImagesCreate(NewsImagesCore):
    pass

class NewsPostModel(NewsCoreModel):
    folder: str

class NewsCreateModel(NewsCoreModel):
    preview_image_url: str
    images: List[NewsImagesCreate]

class NewsInDBModel(NewsCoreModel):
    id: int
    preview_image_url: str
    images: List[NewsImagesCore]

class NewsUpdateModel(NewsCoreModel):
    pass

class NewsImagesAllModel(BaseModel):
    cloud_key: str

class NewsAllModel(BaseModel):
    cloud_key: str