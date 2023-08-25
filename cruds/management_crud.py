from typing import Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import management_config as models_management
from schemas import management as schemas_management


def get_management_by_user(db: Session, user_id: int) -> Optional[models_management.ManagementConfig]:
    management = db.query(models_management.ManagementConfig).filter(
        models_management.ManagementConfig.user_id == user_id).first()
    return management


def update_management(db: Session, management: schemas_management.ManagementUpdate, user_id: int):
    db_management = get_management_by_user(db=db, user_id=user_id)
    if db_management is None:
        raise HTTPException(status_code=404, detail="Management não encontrado")
    db_management.entry = management.entry
    db_management.stop_loss = management.stop_loss
    db_management.stop_win = management.stop_win
    db.commit()
    db.refresh(db_management)
    return db_management


def create_management(db, management: schemas_management.ManagementCreate, user_id: int):
    db_management = models_management.ManagementConfig(user_id=user_id, entry=management.entry,
                                                       stop_loss=management.stop_loss, stop_win=management.stop_win)
    db.add(db_management)
    db.commit()
    db.refresh(db_management)
    return db_management


def update_management_values(db: Session, management: schemas_management.ManagementConfigUpdate, user_id: int):
    db_management = get_management_by_user(db=db, user_id=user_id)
    if db_management is None:
        raise HTTPException(status_code=404, detail="Management não encontrado")
    if management.balance:
        db_management.balance = management.balance
    if management.value_gain:
        db_management.value_gain = management.value_gain
    if management.value_loss:
        db_management.value_loss = management.value_loss
    db.commit()
    db.refresh(db_management)
    return db_management


def reset_management_values(db: Session, user_id: int):
    db_management = get_management_by_user(db=db, user_id=user_id)
    if db_management is None:
        raise HTTPException(status_code=404, detail="Management não encontrado")
    db_management.balance = 0
    db_management.value_gain = 0
    db_management.value_loss = 0
    db.commit()
    db.refresh(db_management)
    return db_management


def get_management_values(db: Session, user_id: int):
    db_management = db.query(models_management.ManagementConfig.balance, models_management.ManagementConfig.value_gain,
                             models_management.ManagementConfig.value_loss,
                             models_management.ManagementConfig.id).filter(
        models_management.ManagementConfig.user_id == user_id).first()
    if db_management is None:
        raise HTTPException(status_code=404, detail="Management não encontrado")
    return db_management
