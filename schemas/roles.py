from pydantic import BaseModel


class RoleBase(BaseModel):
    name: str
    description: str


class RoleCreate(RoleBase):
    pass


class GetRoleName(BaseModel):
    name: str


class Role(RoleBase):
    id: int

    class Config:
        orm_mode = True
