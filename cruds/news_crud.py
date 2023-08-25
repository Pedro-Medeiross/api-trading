from typing import Optional
from sqlalchemy.orm import Session
from models import news as news_model
from schemas import news as news_schema


def get_news(db: Session, skip: int = 0, limit: int = 1000000):
    return db.query(news_model.News).offset(skip).limit(limit).all()


def create_news(db: Session, news: news_schema.NewsCreate):
    db_news = news_model.News(**news.dict())
    db.add(db_news)
    db.commit()
    db.refresh(db_news)
    return db_news


def create_filter_news(db: Session, filter_news: news_schema.FilterNewsCreate):
    db_filter_news = news_model.FilterNews(**filter_news.dict())
    db.add(db_filter_news)
    db.commit()
    db.refresh(db_filter_news)
    return db_filter_news


def get_filter_news(db: Session, skip: int = 0, limit: int = 1000000):
    return db.query(news_model.FilterNews).offset(skip).limit(limit).all()
