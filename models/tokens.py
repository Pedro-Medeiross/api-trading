from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from connection import Base
from models import user as models_user


class Tokens(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(250))
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship(models_user.User, back_populates="token")
