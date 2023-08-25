from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from connection import Base
from .user_roles import UserRoles


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    username = Column(String(100), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    password = Column(String(100))
    phone = Column(String(50))
    last_login = Column(DateTime, nullable=True)
    email_activated = Column(Boolean(), default=False)
    phone_activated = Column(Boolean(), default=False)
    brokerage_email = Column(String(100), nullable=True)
    brokerage_password = Column(String(100), nullable=True)
    account_type = Column(String(100), nullable=True, default="PRACTICE")
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    is_active = Column(Boolean(), default=False)
    date_activation = Column(DateTime, nullable=True)

    roles = relationship("Role", secondary=UserRoles, back_populates="users")
    token = relationship("Tokens", back_populates="user")
