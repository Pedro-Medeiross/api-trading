from fastapi import APIRouter
from schemas import trade as schemas_trade
from schemas import trade_status as schemas_trade_status
from schemas import user as schemas_user
from sqlalchemy.orm import Session
from connection import SessionLocal
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasicCredentials
from cruds import security_crud as security
from cruds import trades_crud as crud_trades
from typing import List

trades_router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@trades_router.get("/pending", response_model=List[schemas_trade.Trade],
                   dependencies=[Depends(security.get_current_user)])
async def get_trades_not_scheduled(db: Session = Depends(get_db),
                                   current_user: schemas_user.User = Depends(security.get_current_user)):
    """Retorna todos os trades que não estão agendados para o dia atual"""
    user = current_user
    return crud_trades.get_trades_not_scheduled(db=db, user_id=user.id)


@trades_router.get("/accepted", response_model=List[schemas_trade.Trade])
async def get_accepted_trades_by_user(db: Session = Depends(get_db),
                                      current_user: schemas_user.User = Depends(security.get_current_user)):
    """Retorna todos os trades aceitos para o usuário logado"""
    user = current_user
    return crud_trades.get_accepted_trades_by_user_and_status(db=db, user_id=user.id)


@trades_router.get("/refused", response_model=List[schemas_trade_status.TradeStatus])
async def get_refused_trades_by_user(db: Session = Depends(get_db),
                                     current_user: schemas_user.User = Depends(security.get_current_user)):
    """Retorna todos os trades recusados para o usuário logado"""
    user = current_user
    return crud_trades.get_refused_trades_by_user_and_status(db=db, user_id=user.id)


@trades_router.post("/create", response_model=schemas_trade.Trade, dependencies=[Depends(security.get_current_user)])
async def create_trade(trade: schemas_trade.TradeCreate, db: Session = Depends(get_db)):
    """Cria um novo trade"""
    return crud_trades.create_trade(db=db, trade=trade)


@trades_router.post("/status/accept", response_model=schemas_trade_status.TradeStatus,
                    dependencies=[Depends(security.get_current_user)])
async def trade_status_accept(trade_status: schemas_trade_status.UpdateStatusTrade, db: Session = Depends(get_db),
                              current_user: schemas_user.User = Depends(security.get_current_user)):
    """Altera o status de um trade para aceito"""
    return crud_trades.trade_status_accept(db=db, status=trade_status.status_trade, trade_id=trade_status.trade_id,
                                           user_id=current_user.id)


@trades_router.post("/schedule/refuse", response_model=schemas_trade_status.TradeStatus,
                    dependencies=[Depends(security.get_current_user)])
async def trade_schedule_refuse(trade_status: schemas_trade_status.UpdateStatusTrade, db: Session = Depends(get_db),
                                current_user: schemas_user.User = Depends(security.get_current_user)):
    """Altera o status de um trade para recusado"""
    return crud_trades.trade_schedule_refuse(db=db, trade_id=trade_status.trade_id,
                                           user_id=current_user.id)


@trades_router.post("/schedule/accept", response_model=schemas_trade_status.TradeStatus,
                    dependencies=[Depends(security.get_current_user)])
async def trade_schedule_accept(trade_status: schemas_trade_status.UpdateStatusTrade, db: Session = Depends(get_db),
                                current_user: schemas_user.User = Depends(security.get_current_user)):
    """Altera o status de um trade para agendado"""
    return crud_trades.trade_schedule_accept(db=db, trade_id=trade_status.trade_id,
                                             user_id=current_user.id)


@trades_router.put("/status/update", response_model=schemas_trade_status.TradeStatus)
async def update_trade_associate(trade: schemas_trade_status.UpdateStatusTrade,
                                 db: Session = Depends(get_db),
                                 credentials: HTTPBasicCredentials = Depends(security.get_basic_credentials)):
    """Altera o status de um trade"""
    return crud_trades.update_status_trade(db=db, trade_id=trade.trade_id, user_id=trade.user_id,
                                           trade_status=trade.status_trade)
