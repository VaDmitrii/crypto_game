import logging
import random
from datetime import datetime, timedelta
from typing import Tuple

from faker import Faker
from sqlalchemy.exc import PendingRollbackError, IntegrityError

from database import get_db
from models.user_model import User
from pydantic_schema.base_schemes import UserBase, UserUpdate
from services.user_service import UserService


async def get_statistics() -> Tuple[int, int, int]:
    async for session in get_db():
        user_service = UserService(session=session)
        users = await user_service.get_all()

    async for session in get_db():
        user_service = UserService(session=session)
        users_online = await user_service.get_online_users()

    async for session in get_db():
        user_service = UserService(session=session)
        unique_users = await user_service.get_unique_users()
    total_users = len(users.all())
    return total_users, users_online, unique_users


async def create_user() -> str:
    faker = Faker('ru')
    async for session in get_db():
        user = User(
            username=faker.unique.user_name(),
            telegram_uid=random.randint(11111, 99999),
            coins=random.randint(0, 10000000),
            rating=random.randint(0, 10000),
            last_login=faker.date_time_this_year(),
            last_logout=datetime.now() - timedelta(seconds=random.randint(10, 120))
        )
        session.add(user)
        try:
            await session.commit()
            await session.refresh(user)
            return user.username
        except (PendingRollbackError, IntegrityError):
            await session.rollback()


async def get_user_by_username(username: str) -> UserBase:
    async for session in get_db():
        user_service = UserService(session=session)
        user = await user_service.get_by_username(username=username)
        logging.error(user)
        return user


async def update_user(uid: int, new_coins: int = -1, new_rating: int = -1) -> None:
    update_values = UserUpdate(
        coins=new_coins if new_coins >= 0 else None,
        rating=new_rating if new_rating >= 0 else None
    )
    async for session in get_db():
        user_service = UserService(session=session)
        await user_service.update_user(uid=uid, update_user=update_values)
    return
