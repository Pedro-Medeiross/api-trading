from pydantic import BaseModel
from typing import Optional


class ManagementBase(BaseModel):
    user_id: Optional[int]
    entry: Optional[float]
    stop_loss: Optional[float]
    stop_win: Optional[float]
    balance: Optional[float]
    value_gain: Optional[float]
    value_loss: Optional[float]


class ManagementCreate(ManagementBase):
    pass


class ManagementUpdate(ManagementBase):
    pass


class Management(ManagementBase):
    id: int

    class Config:
        orm_mode = True


class ManagementConfigBase(BaseModel):
    balance: Optional[float]
    value_gain: Optional[float]
    value_loss: Optional[float]


class ManagementConfigUpdate(ManagementConfigBase):
    pass


class ManagementConfig(ManagementConfigBase):
    id: int

    class Config:
        orm_mode = True