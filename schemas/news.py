from pydantic import BaseModel


class NewsBase(BaseModel):
    pair: str
    stars: int
    hours: str


class NewsCreate(NewsBase):
    pass


class News(NewsBase):
    id: int

    class Config:
        orm_mode = True


class FilterNewsBase(BaseModel):
    pair: str
    range_hours: str


class FilterNewsCreate(FilterNewsBase):
    pass


class FilterNews(FilterNewsBase):
    id: int

    class Config:
        orm_mode = True
