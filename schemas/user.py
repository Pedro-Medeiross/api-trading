from pydantic import BaseModel
from pydantic.schema import datetime
from typing import Optional
from .roles import Role


class UserBase(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
    phone: str


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    pass

class UserUpdateBrokerage(BaseModel):
    brokerage_email: str
    brokerage_password: str
    account_type: str


class UserUpdateAccountType(BaseModel):
    account_type: str


class DeleteUser(UserBase):
    deleted_at: datetime


class UserUpdatePassword(BaseModel):
    password: str

    orm_mode = True


class User(UserBase):
    id: int
    account_type: str
    email_activated: Optional[bool]
    phone_activated: Optional[bool]
    brokerage_email: Optional[str]
    brokerage_password: Optional[str]
    last_login: Optional[datetime]
    date_activation: Optional[datetime]
    is_active: Optional[bool]
    roles: list[Role] = []

    class Config:
        orm_mode = True
