from sqlalchemy import Column, Integer, ForeignKey, Float
from connection import Base


class ManagementConfig(Base):
    __tablename__ = "manegement_config"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    entry = Column(Float)
    stop_loss = Column(Float)
    stop_win = Column(Float)
    balance = Column(Float)
    value_gain = Column(Float)
    value_loss = Column(Float)