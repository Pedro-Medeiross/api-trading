from sqlalchemy.orm import Session
from models import bot_options as models_bot
from schemas import bot_options as schemas_bot
from fastapi import HTTPException


def get_bot_options_by_user(db: Session, user_id: int):
    bot_options = db.query(models_bot.BotOptions).filter(models_bot.BotOptions.user_id == user_id).first()
    return bot_options


def update_bot_options(db: Session, bot_options: schemas_bot.BotOptionsUpdate, user_id: int):
    db_bot_options = get_bot_options_by_user(db, user_id)
    if db_bot_options is None:
        raise HTTPException(status_code=404, detail="Bot options não encontrado")
    db_bot_options.management = bot_options.management
    db_bot_options.status = bot_options.status
    db_bot_options.soros = bot_options.soros
    db_bot_options.news = bot_options.news
    db_bot_options.automatic = bot_options.automatic
    db.commit()
    db.refresh(db_bot_options)
    return db_bot_options


def update_bot_status(db: Session, bot_status: int, user_id: int):
    db_bot_options = get_bot_options_by_user(db, user_id)
    if db_bot_options is None:
        raise HTTPException(status_code=404, detail="Bot options não encontrado")
    db_bot_options.status = bot_status
    db.commit()
    db.refresh(db_bot_options)
    return db_bot_options
