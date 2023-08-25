from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from connection import Base
from .user_roles import UserRoles


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)
    description = Column(String(100))

    users = relationship("User", secondary=UserRoles, back_populates="roles")
