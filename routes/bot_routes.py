import aiohttp
import os
from typing import List
from fastapi import APIRouter
from schemas import bot_options as schemas_bot
from schemas import trade as schemas_trade
from schemas import user as schemas_user
from schemas import management as schemas_management
from schemas import trade_status as schemas_trade_status
from sqlalchemy.orm import Session
from connection import SessionLocal
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasicCredentials
from cruds import security_crud as security
from cruds import bot_crud as bot_crud
from cruds import user_crud as crud_user
from cruds import trades_crud as crud_trades
from cruds import management_crud as management_crud
from dotenv import load_dotenv

bot_router = APIRouter()
load_dotenv()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@bot_router.get("/botoptions/user", response_model=schemas_bot.BotOptions, dependencies=[Depends(security.get_current_user)])
async def get_bot_options(db: Session = Depends(get_db), current_user: schemas_user.User = Depends(security.get_current_user)):
    """Retorna as opções do bot"""
    db_user = crud_user.get_user_by_id(db, user_id=current_user.id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return bot_crud.get_bot_options_by_user(db, user_id=current_user.id)


@bot_router.get("/botoptions/id/{user_id}", response_model=schemas_bot.BotOptions)
async def get_bot_options(user_id: int, db: Session = Depends(get_db),
                          credentials: HTTPBasicCredentials = Depends(security.get_basic_credentials)):
    """Retorna as opções do bot"""
    db_user = crud_user.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return bot_crud.get_bot_options_by_user(db, user_id=user_id)


@bot_router.put("/botoptions/user", response_model=schemas_bot.BotOptions, dependencies=[Depends(security.get_current_user)])
async def update_bot_options(bot_options: schemas_bot.BotOptionsUpdate, db: Session = Depends(get_db), current_user: schemas_user.User = Depends(security.get_current_user)):
    """Atualiza as opções do bot"""
    db_user = crud_user.get_user_by_id(db, user_id=current_user.id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return bot_crud.update_bot_options(db, bot_options, user_id=current_user.id)


@bot_router.put("/botoptions/id/{user_id}", response_model=schemas_bot.BotOptions)
async def update_bot_options(user_id: int, bot_options: schemas_bot.BotOptionsUpdate, db: Session = Depends(get_db),
                             credentials: HTTPBasicCredentials = Depends(security.get_basic_credentials)):
    """Atualiza as opções do bot"""
    db_user = crud_user.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return bot_crud.update_bot_options(db, bot_options, user_id=user_id)


@bot_router.put("/botoptions/status/{user_id}/{bot_status}", response_model=schemas_bot.BotOptions)
async def update_bot_status(user_id: int, bot_status: int, db: Session = Depends(get_db),
                            credentials: HTTPBasicCredentials = Depends(security.get_basic_credentials)):
    """Atualiza o status do bot"""
    db_user = crud_user.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return bot_crud.update_bot_status(db, bot_status=bot_status, user_id=user_id)


# Users
@bot_router.get("/user/{user_id}", response_model=schemas_user.User)
async def get_user_by_id(user_id: int, db: Session = Depends(get_db),
                         credentials: HTTPBasicCredentials = Depends(security.get_basic_credentials)):
    """Retorna um usuário pelo seu id"""
    db_user = crud_user.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return db_user


# Trades
@bot_router.get("/trades/user/id/{user_id}", response_model=List[schemas_trade_status.TradeStatusId])
async def get_trades_ids_with_user(user_id: int, db: Session = Depends(get_db),
                                            credentials: HTTPBasicCredentials = Depends(
                                                security.get_basic_credentials)):
    """Retorna todos os trades que estão agendados para o dia atual e que o usuário logado está associado"""
    return crud_trades.get_trade_ids_by_user_id(db=db, user_id=user_id)


@bot_router.get("/trades/pairs/users/id/{user_id}", response_model=List[schemas_trade_status.TradeStatusPair])
async def get_trades_pairs_schedule_with_user(user_id: int, db: Session = Depends(get_db),
                                              credentials: HTTPBasicCredentials = Depends(
                                                  security.get_basic_credentials)):
    """retorna os pares de trades agendados para o usuário logado"""
    return crud_trades.get_trades_pairs_schedule_with_user(db=db, user_id=user_id)


@bot_router.get("/trades/id/{trade_id}", response_model=schemas_trade.Trade)
async def get_trade_by_id(trade_id: int, db: Session = Depends(get_db),
                          credentials: HTTPBasicCredentials = Depends(security.get_basic_credentials)):
    """Retorna um trade pelo id"""
    db_trade = crud_trades.get_trade_by_id(db, trade_id=trade_id)
    if db_trade is None:
        raise HTTPException(status_code=404, detail="Trade não encontrado")
    return db_trade


@bot_router.get("/trades/status/id/{user_id}/{trade_id}", response_model=schemas_trade_status.TradeStatus)
async def get_trade_status_by_id(user_id: int, trade_id: int, db: Session = Depends(get_db),
                                 credentials: HTTPBasicCredentials = Depends(security.get_basic_credentials)):
    """Retorna o status de um trade pelo id"""
    db_trade_status = crud_trades.get_trade_status_by_trade_id_and_user_id(db, trade_id=trade_id, user_id=user_id)
    if db_trade_status is None:
        raise HTTPException(status_code=404, detail="Trade não encontrado")
    return db_trade_status


@bot_router.post("/trades/accept/all/id/{trade_id}")
async def change_trade_status_for_all_users_not_accepted(trade_id: int, db: Session = Depends(get_db),
                                                         credentials: HTTPBasicCredentials = Depends(
                                                             security.get_basic_credentials)):
    """Altera o status de um trade para aceito para todos os usuários que não aceitaram"""
    crud_trades.accept_associated_trade_for_all_users_not_accepted(db=db, trade_id=trade_id)
    return 'Trade aceito para todos os usuários'


@bot_router.put("/trades/update/status/{trade_id}/{user_id}", response_model=schemas_trade_status.TradeStatus)
async def update_trade_status(trade_id: int, user_id: int, status_trade: schemas_trade_status.GetTradeStatus, db: Session = Depends(get_db),
                              credentials: HTTPBasicCredentials = Depends(security.get_basic_credentials)):
    """Altera o status de um trade"""
    return crud_trades.update_status_trade(db=db, trade_id=trade_id, user_id=user_id,
                                           trade_status=status_trade.status_trade)


# Management
@bot_router.get("/management/reset/id/{user_id}", response_model=schemas_management.ManagementConfig)
async def reset_management_values(user_id: int, db: Session = Depends(get_db),
                                  credentials: HTTPBasicCredentials = Depends(security.get_basic_credentials)):
    """Reseta os valores de gerenciamento de um usuário"""
    db_user = crud_user.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return management_crud.reset_management_values(db=db, user_id=user_id)


@bot_router.get("/management/id/{user_id}", response_model=schemas_management.Management)
async def get_management(user_id: int, db: Session = Depends(get_db),
                         credentials: HTTPBasicCredentials = Depends(security.get_basic_credentials)):
    """Retorna o gerenciamento de um usuário"""
    db_user = crud_user.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return management_crud.get_management_by_user(db, user_id=user_id)


@bot_router.put("/management/update/values/id/{user_id}", response_model=schemas_management.ManagementConfig)
async def update_management_values(user_id: int,
                                   management: schemas_management.ManagementConfigUpdate,
                                   db: Session = Depends(get_db),
                                   credentials: HTTPBasicCredentials = Depends(security.get_basic_credentials)):
    """Atualiza os valores de gerenciamento de um usuário"""
    db_user = crud_user.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return management_crud.update_management_values(db=db, management=management, user_id=user_id)


@bot_router.get("/start/user", dependencies=[Depends(security.get_current_user)])
async def start_bot(current_user: schemas_user.User = Depends(security.get_current_user)):
    """Inicia o bot para o usuário logado"""
    async with aiohttp.ClientSession() as session:
        auth = aiohttp.BasicAuth(os.getenv('API_USER'), os.getenv('API_PASS'))
        headers = {'Authorization': auth.encode()}
        try:
            async with session.get(f"https://bot.investingbrazil.online/start/{current_user.id}",
                                   headers=headers) as response:
                r = await response.text()
                return r
        except:
            if response.status != 200:
                new_attempt = await session.get(f"https://bot.investingbrazil.online/start/{current_user.id}",
                                                headers=headers)
                r = await new_attempt.text()
                return r


@bot_router.get("/status/user", dependencies=[Depends(security.get_current_user)])
async def get_bot_status(current_user: schemas_user.User = Depends(security.get_current_user)):
    """Retorna o status do bot para o usuário logado"""
    async with aiohttp.ClientSession() as session:
        auth = aiohttp.BasicAuth(os.getenv('API_USER'), os.getenv('API_PASS'))
        headers = {'Authorization': auth.encode()}
        try:
            async with session.get(f"https://bot.investingbrazil.online/status/{current_user.id}",
                                   headers=headers) as response:
                r = await response.text()
                return r
        except:
            if response.status != 200:
                new_attempt = await session.get(f"https://bot.investingbrazil.online/status/{current_user.id}",
                                                headers=headers)
                r = await new_attempt.text()
                return r


@bot_router.get("/stop/user", dependencies=[Depends(security.get_current_user)])
async def stop_bot(current_user: schemas_user.User = Depends(security.get_current_user)):
    """Para o bot para o usuário logado"""
    async with aiohttp.ClientSession() as session:
        auth = aiohttp.BasicAuth(os.getenv('API_USER'), os.getenv('API_PASS'))
        headers = {'Authorization': auth.encode()}
        try:
            async with session.get(f"https://bot.investingbrazil.online/stop/{current_user.id}",
                                   headers=headers) as response:
                r = await response.text()
                return r
        except:
            if response.status != 200:
                new_attempt = await session.get(f"https://bot.investingbrazil.online/stop/{current_user.id}",
                                                headers=headers)
                r = await new_attempt.text()
                return r