from pydantic import BaseModel
from pydantic.schema import datetime


class TradeBase(BaseModel):
    pair: str
    type: str
    method: str
    price: str
    timeframe: float    


class TradeCreate(TradeBase):
    pass


class TradeUpdate(TradeBase):
    user_id: int
    updated_at: datetime


class Trade(TradeBase):
    id: int

    class Config:
        orm_mode = True
