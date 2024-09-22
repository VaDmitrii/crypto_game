from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    id: int
    username: str
    telegram_uid: int
    coins: Optional[int] = 0
    rating: Optional[int] = 0

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    username: str
    telegram_uid: int

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    username: Optional[str] = None
    coins: Optional[int] = None
    rating: Optional[int] = None

    class Config:
        from_attributes = True


class UserOut(UserBase):
    last_login: Optional[datetime]
    last_logout: Optional[datetime]

    class Config:
        from_attributes = True
