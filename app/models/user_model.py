from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    telegram_uid = Column(Integer, unique=True, nullable=False)
    coins = Column(Integer, default=0)
    rating = Column(Integer, default=0)
    last_login = Column(DateTime, nullable=True, default=func.now())
    last_logout = Column(DateTime, nullable=True)
