from sqlalchemy import Boolean, Column, Integer, ForeignKey
from connection import Base


class BotOptions(Base):
    __tablename__ = "bot_options"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    management = Column(Boolean(), default=False)
    status = Column(Integer, default=0)
    soros = Column(Boolean(), default=False)
    news = Column(Boolean(), default=False)
    automatic = Column(Boolean(), default=False)
