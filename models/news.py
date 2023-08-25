from connection import Base
from sqlalchemy import Column, Integer, String, DateTime, Text


class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    pair = Column(String(100), index=True)
    stars = Column(Integer)
    hours = Column(String)


class FilterNews(Base):
    __tablename__ = "filter_news"

    id = Column(Integer, primary_key=True, index=True)
    pair = Column(String(100), index=True)
    range_hours = Column(Text)
