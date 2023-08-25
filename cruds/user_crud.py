import pytz
import base64
from typing import Optional
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import user as models_user
from models import bot_options as models_bot_options
from models import management_config as models_management
from models import tokens as models_tokens
from schemas import user as schemas_user
from cruds import security_crud as crud_security
from cruds import role_crud as crud_role
from cruds import email_crud as crud_email


def get_user_by_id(db: Session, user_id: int):
    return db.query(models_user.User).filter(models_user.User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 1000000):
    return db.query(models_user.User).offset(skip).limit(limit).all()


def get_user_by_username(db: Session, username: str) -> Optional[models_user.User]:
    user = db.query(models_user.User).filter(models_user.User.username == username).first()
    return user


def get_user_by_email(db: Session, email: str) -> Optional[models_user.User]:
    user = db.query(models_user.User).filter(models_user.User.email == email).first()
    return user


def create_user(db: Session, user: schemas_user.UserCreate):
    hashed_password = crud_security.get_password_hash(user.password)
    tz = pytz.timezone('America/Sao_Paulo')
    date_trade_created = datetime.now(tz).replace(microsecond=0)
    db_user = models_user.User(first_name=user.first_name, last_name=user.last_name,
                               username=user.username, email=user.email, password=hashed_password,
                               phone=user.phone, created_at=date_trade_created, is_active=False,
                               account_type='PRACTICE')
    role = crud_role.get_role_by_name(db, 'cliente')
    db_user.roles.append(role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db_botoptions = models_bot_options.BotOptions(user_id=db_user.id, management=False, status=0, soros=False,
                                                  news=False,
                                                  automatic=False)
    db.add(db_botoptions)
    db.commit()
    db.refresh(db_botoptions)
    db_management = models_management.ManagementConfig(user_id=db_user.id, entry=0, stop_loss=0, stop_win=0, balance=0,
                                                       value_gain=0, value_loss=0)
    db.add(db_management)
    db.commit()
    db.refresh(db_management)
    # token = crud_security.generate_confirm_email_token(db_user.email)
    # db_token = models_tokens.Tokens(token=token, user_id=db_user.id)
    # db.add(db_token)
    # db.commit()
    # db.refresh(db_token)
    # crud_email.send_confirm_email(db=db, user_email=db_user.email, token=token)
    return db_user


def update_user(db: Session, user: schemas_user.UserUpdate, user_id: int):
    tz = pytz.timezone('America/Sao_Paulo')
    date_updated = datetime.now(tz).replace(microsecond=0)
    db_user = get_user_by_id(db, user_id)
    db_user.first_name = user.first_name
    db_user.last_name = user.last_name
    db_user.username = user.username
    db_user.email = user.email
    db_user.phone = user.phone
    db_user.updated_at = date_updated
    db.commit()
    db.refresh(db_user)
    return db_user


def update_brokerage_credentials(db: Session, user: schemas_user.UserUpdateBrokerage, user_id: int):
    tz = pytz.timezone('America/Sao_Paulo')
    date_updated = datetime.now(tz).replace(microsecond=0)
    db_user = get_user_by_id(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    db_user.brokerage_email = user.brokerage_email
    db_user.brokerage_password = base64.b64encode(user.brokerage_password.encode()).decode()
    db_user.updated_at = date_updated
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user_password(db: Session, user: schemas_user.UserUpdatePassword, user_id: int):
    db_user = get_user_by_id(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    hashed_password = crud_security.get_password_hash(user.password)
    db_user.password = hashed_password
    db_user.updated_at = datetime.now(pytz.timezone('America/Sao_Paulo'))
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user_account_type(db: Session, user_id: int, account_type: schemas_user.UserUpdateAccountType):
    db_user = get_user_by_id(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    db_user.account_type = account_type.account_type
    db_user.updated_at = datetime.now(pytz.timezone('America/Sao_Paulo'))
    db.commit()
    db.refresh(db_user)
    return db_user
