from pydantic import BaseModel
from typing import Optional


class BotOptionsBase(BaseModel):
    user_id: Optional[int]
    management: Optional[bool]
    status: Optional[int]
    soros: Optional[bool]
    news: Optional[bool]
    automatic: Optional[bool]


class BotOptionsCreate(BotOptionsBase):
    pass


class BotOptionsUpdate(BotOptionsBase):
    pass


class BotOptions(BotOptionsBase):
    id: int

    class Config:
        orm_mode = True


class BotStatusUpdate(BaseModel):
    status: int

    class Config:
        orm_mode = True
