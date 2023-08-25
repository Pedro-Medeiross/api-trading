from connection import Base
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship


class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)
    pair = Column(String(100))
    type = Column(String(100))
    method = Column(String(100))
    price = Column(String(100))
    timeframe = Column(Float)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    
    statuses = relationship("TradeStatus", back_populates="trade")


"""
Status das Trades :
0 - Aguardando ou Pendente
1 - Recusado
2 - Agendado
3 - Executado mas não agendado
4 - Executado
5 - Cancelado por noticia
"""


class TradeStatus(Base):
    __tablename__ = "trade_status"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    trade_id = Column(Integer, ForeignKey('trades.id'))
    status_trade = Column(Integer, nullable=True)
    created_at = Column(DateTime)
    scheduled = Column(Boolean, nullable=True)
    executed_at = Column(DateTime, nullable=True)
    amount = Column(Integer, nullable=True)

    trade = relationship("Trade", back_populates="statuses")
