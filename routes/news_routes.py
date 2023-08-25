from typing import List
from fastapi import APIRouter
from sqlalchemy.orm import Session
from connection import SessionLocal
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasicCredentials
from cruds import security_crud as security
from cruds import news_crud as news_crud
from schemas import news as news_schema

news_router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@news_router.get("/get_news", response_model=List[news_schema.News])
def read_news(skip: int = 0, limit: int = 1000000, db: Session = Depends(get_db),
              credentials: HTTPBasicCredentials = Depends(security.get_basic_credentials)):
    """Retorna todas as notícias cadastradas no banco de dados"""
    news = news_crud.get_news(db, skip=skip, limit=limit)
    return news


@news_router.get("/get_filter_news", response_model=List[news_schema.FilterNews])
def read_filter_news(skip: int = 0, limit: int = 1000000, db: Session = Depends(get_db),
                     credentials: HTTPBasicCredentials = Depends(security.get_basic_credentials)):
    """Retorna todos os filtros de notícias cadastrados no banco de dados"""
    news = news_crud.get_filter_news(db, skip=skip, limit=limit)
    return news


@news_router.post("/create", response_model=news_schema.News)
def create_news(news: news_schema.NewsCreate, db: Session = Depends(get_db),
                credentials: HTTPBasicCredentials = Depends(security.get_basic_credentials)):
    """Cria uma nova notícia no banco de dados"""
    return news_crud.create_news(db=db, news=news)


@news_router.post("/filter_news", response_model=news_schema.FilterNews)
def create_filter_news(filter_news: news_schema.FilterNewsCreate, db: Session = Depends(get_db),
                       credentials: HTTPBasicCredentials = Depends(security.get_basic_credentials)):
    """Cria um novo filtro de notícias no banco de dados"""
    return news_crud.create_filter_news(db=db, filter_news=filter_news)
