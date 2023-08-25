from pydantic import BaseModel
from typing import Optional


class TradeStatusBase(BaseModel):
    user_id: int
    trade_id: int
    status_trade: int
    scheduled: Optional[bool]
    amount: Optional[int]


class TradeStatusCreate(TradeStatusBase):
    pass


class TradeStatusUpdate(TradeStatusBase):
    pass


class GetTradeStatus(TradeStatusBase):
    status_trade: int


class UpdateStatusTrade(BaseModel):
    trade_id: int
    status_trade: int

    class Config:
        orm_mode = True


class TradeStatusPair(BaseModel):
    pair: str

    class Config:
        orm_mode = True


class TradeStatusId(BaseModel):
    trade_id: int

    class Config:
        orm_mode = True


class TradeStatus(TradeStatusBase):
    id: int

    class Config:
        orm_mode = True
