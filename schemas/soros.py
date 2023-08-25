from pydantic import BaseModel
from typing import Optional


class SorosBase(BaseModel):
    user_id: Optional[int]
    soros_quantity: Optional[int]
    soros_percent: Optional[float]


class SorosCreate(SorosBase):
    pass


class SorosUpdate(SorosBase):
    pass


class Soros(SorosBase):
    id: int

    class Config:
        orm_mode = True
