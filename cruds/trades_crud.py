from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.orm import aliased
from sqlalchemy import Date, and_, cast
from models import trades as models_trade
from schemas import trade as schemas_trade
from schemas import trade_status as schemas_trade_status
from cruds import user_crud as crud_user
from cruds import bot_crud as crud_bot
from cruds import management_crud as crud_management
from datetime import datetime
import pytz


def get_trade_by_id(db: Session, trade_id: int):
    trade = db.query(models_trade.Trade).filter(models_trade.Trade.id == trade_id).first()
    return trade


def create_trade(db: Session, trade: schemas_trade.TradeCreate):
    tz = pytz.timezone('America/Sao_Paulo')
    date_trade_created = datetime.now(tz).replace(microsecond=0)
    db_trade = models_trade.Trade(pair=trade.pair, type=trade.type, method=trade.method, price=trade.price,
                                  timeframe=trade.timeframe, created_at=date_trade_created)
    db.add(db_trade)
    db.commit()
    db.refresh(db_trade)
    users = crud_user.get_users(db=db)
    for user in users:
        db_trade_status = models_trade.TradeStatus(trade_id=db_trade.id, user_id=user.id, status_trade=0,
                                                   created_at=date_trade_created)
        db.add(db_trade_status)
        db.commit()
        db.refresh(db_trade_status)
        db_autotrade = crud_bot.get_bot_options_by_user(db=db, user_id=user.id)
        if db_autotrade.automatic:
            amount = crud_management.get_management_by_user(db=db, user_id=user.id).entry
            if amount is not None or amount != 0:
                trade_status_accept(db=db, status=2, user_id=user.id, trade_id=db_trade.id, entry=amount)
    return db_trade


def update_trade(db: Session, trade: schemas_trade.TradeUpdate, trade_id: int):
    db_trade = get_trade_by_id(db, trade_id)
    if db_trade is None:
        raise HTTPException(status_code=404, detail="Trade não encontrado")
    db_trade.pair = trade.pair
    db_trade.type = trade.type
    db_trade.method = trade.method
    db_trade.price = trade.price
    db_trade.timeframe = trade.timeframe
    db.commit()
    db.refresh(db_trade)
    return db_trade


def get_trades_not_scheduled(db: Session, user_id: int):
    today = datetime.now(pytz.timezone('America/Sao_Paulo')).date()

    # Cria um alias para a tabela "Trade"
    t = aliased(models_trade.Trade)
    sts = aliased(models_trade.TradeStatus)

    # Consulta as trades que não foram agendadas pelo usuário e são do dia atual
    trades_not_scheduled = db.query(t).join(sts, and_(
        t.id == sts.trade_id, sts.user_id == user_id)).filter(sts.status_trade == 0).filter(
        cast(t.created_at, Date) == today).all()
    return trades_not_scheduled


def trade_status_accept(db: Session, status: int, user_id: int, trade_id: int, entry: float):
    db_trade_status = get_trade_status_by_trade_id_and_user_id(db, trade_id, user_id=user_id)
    if db_trade_status is None:
        raise HTTPException(status_code=404, detail="Trade associada não encontrada")
    db_trade_status.status_trade = status
    db_trade_status.scheduled = True
    db_trade_status.amount = entry
    db.commit()
    db.refresh(db_trade_status)
    return db_trade_status


def get_trade_ids_by_user_id(db: Session, user_id: int):
    today = datetime.now(pytz.timezone('America/Sao_Paulo'))
    trade_ids = db.query(models_trade.Trade.id).join(models_trade.TradeStatus,
                                                     models_trade.Trade.id == models_trade.TradeStatus.trade_id).filter(
        models_trade.TradeStatus.user_id == user_id).filter(models_trade.TradeStatus.status_trade == 2).all()
    return [schemas_trade_status.TradeStatusId(trade_id=trade_id) for trade_id, in trade_ids]


def get_trades_by_user_id(db: Session, user_id: int):
    trade_ids = db.query(models_trade.TradeStatus.trade_id).filter(
        models_trade.TradeStatus.user_id == user_id).all()
    return [trade_id for trade_id, in trade_ids]


def get_trades_pairs_schedule_with_user(db: Session, user_id: int):
    trade_ids = get_trades_by_user_id(db, user_id)
    today = datetime.now(pytz.timezone('America/Sao_Paulo'))
    trades = db.query(models_trade.Trade.pair).join(models_trade.TradeStatus,
                                                    models_trade.Trade.id == models_trade.TradeStatus.trade_id).filter(
        models_trade.Trade.id.in_(trade_ids)).filter(models_trade.TradeStatus.status_trade == 2).filter(
        models_trade.TradeStatus.user_id == user_id).all()
    return [schemas_trade_status.TradeStatusPair(pair=trade[0]) for trade in trades]


def get_trade_status_by_trade_id_and_user_id(db: Session, trade_id: int, user_id: int):
    trade_status = db.query(models_trade.TradeStatus).filter(models_trade.TradeStatus.trade_id == trade_id).filter(
        models_trade.TradeStatus.user_id == user_id).first()
    return trade_status


def update_status_trade(db: Session, trade_status: int, trade_id: int, user_id: int):
    db_trade_status = get_trade_status_by_trade_id_and_user_id(db, trade_id, user_id=user_id)
    if db_trade_status is None:
        raise HTTPException(status_code=404, detail="Trade associada não encontrada")
    db_trade_status.status_trade = trade_status
    db.commit()
    db.refresh(db_trade_status)
    return db_trade_status


def accept_associated_trade_for_all_users_not_accepted(db: Session, trade_id: int):
    users = crud_user.get_users(db=db)
    for user in users:
        trade_status = db.query(models_trade.TradeStatus).filter(
            models_trade.TradeStatus.trade_id == trade_id).filter(
            models_trade.TradeStatus.user_id == user.id).first()
        if trade_status.status_trade == 0:
            trade_status.status_trade = 3
            db.commit()
            db.refresh(trade_status)


def get_accepted_trades_by_user_and_status(db: Session, user_id: int):
    pending_trades = db.query(models_trade.TradeStatus).filter(models_trade.TradeStatus.user_id == user_id).filter(
        models_trade.TradeStatus.status_trade == 2).all()
    return pending_trades


def get_refused_trades_by_user_and_status(db: Session, user_id: int):
    recused_trades = db.query(models_trade.TradeStatus).filter(
        models_trade.TradeStatus.user_id == user_id).filter(
        models_trade.TradeStatus.status_trade == 1).all()
    return recused_trades


def trade_schedule_refuse(db: Session, trade_id: int, user_id: int):
    db_trade_status = get_trade_status_by_trade_id_and_user_id(db, trade_id, user_id=user_id)
    if db_trade_status is None:
        raise HTTPException(status_code=404, detail="Trade associada não encontrada")
    db_trade_status.scheduled = False
    db_trade_status.status_trade = 1
    db.commit()
    db.refresh(db_trade_status)
    return db_trade_status


def trade_schedule_accept(db: Session, trade_id: int, user_id: int):
    db_trade_status = get_trade_status_by_trade_id_and_user_id(db, trade_id, user_id=user_id)
    if db_trade_status is None:
        raise HTTPException(status_code=404, detail="Trade associada não encontrada")
    db_trade_status.scheduled = True
    db_trade_status.status_trade = 2
    db.commit()
    db.refresh(db_trade_status)
    return db_trade_status