import logging
from datetime import datetime, timedelta
from typing import List

from sqlalchemy import insert, update, func, or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from exceptions_custom import IntegrityDataException
from models.user_model import User
from pydantic_schema.base_schemes import UserCreate, UserUpdate, UserBase, UserOut


class UserRepository:
    _session: AsyncSession

    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_all(self) -> List[UserOut]:
        """ Retrieve all users """
        result = await self._session.execute(select(User))
        return result.scalars()  # type:ignore

    async def get_user(self, username: str) -> UserBase:
        """ Retrieve user by username """
        result = await self._session.execute(
            select(User)
            .filter(User.username == username)
        )
        return result.scalar()

    async def get_by_uid(self, uid: int) -> UserBase:
        """ Retrieve user by ID """
        result = await self._session.execute(
            select(User)
            .filter(User.telegram_uid == uid)
        )
        return result.scalars().first()

    async def get_online_users(self, last_n_seconds: int) -> int:
        """ Get a number of users who are online """
        last_login_timedelta = datetime.utcnow() - timedelta(seconds=last_n_seconds)
        query = (
            select(func.count(User.id))
            .where(User.last_login > last_login_timedelta)
        )
        result = await self._session.execute(query)
        return result.scalar()

    async def get_unique_users(self, min_rating: int, min_coins: int) -> int:
        """ Get a number of users with extraordinary stats """
        query = (
            select(func.count(User.id))
            .where(or_(
                User.rating > min_rating,
                User.coins > min_coins)
            )
        )
        result = await self._session.execute(query)
        return result.scalar()

    async def create_user(self, user_data: UserCreate) -> UserBase:
        """ Create new User with credentials provided """
        stmt = (
            insert(User)
            .values(
                username=user_data.username,
                telegram_uid=user_data.telegram_uid
            )
        )
        await self._session.execute(stmt)

        user = await self._session.execute(
            select(User)
            .filter(User.telegram_uid == user_data.telegram_uid)
        )
        try:
            await self._session.commit()
        except IntegrityError as exc:
            logging.error(f"Data integrity exception: {exc.args[0]}")
            raise IntegrityDataException(message=exc.args[0]) from exc
        return user.scalar_one()

    async def update_user(self, uid: int, update_user: UserUpdate) -> UserOut:
        """ Update the User with credentials provided """
        stmt = (
            update(User)
            .where(User.telegram_uid == uid)
            .values({key: value for key, value in update_user if value is not None})
        )
        await self._session.execute(stmt)

        updated_user_stmt = select(User).where(User.telegram_uid == uid)
        user_updated = await self._session.execute(updated_user_stmt)
        try:
            await self._session.commit()
        except IntegrityError as exc:
            logging.error(f"Data integrity exception: {exc.args[0]}")
            raise IntegrityDataException(message=exc.args[0]) from exc
        return user_updated.scalar_one()
