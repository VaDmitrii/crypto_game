import logging
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from exceptions_custom import UserNotFoundException
from pydantic_schema.base_schemes import UserBase, UserCreate, UserUpdate, UserOut
from repositories.user_repository import UserRepository


class UserService:
    _session: AsyncSession

    def __init__(self, session: AsyncSession):
        self._session = session
        self._repository = UserRepository(session=self._session)

    async def get_all(self) -> List[UserOut]:
        """ Get a list of all users """
        return await self._repository.get_all()

    async def get_by_uid(self, uid: int) -> UserBase:
        """ Retrieve user by ID """
        return await self._repository.get_by_uid(uid=uid)

    async def get_online_users(self, last_n_seconds: int = 60) -> int:
        """ Get a number of users who are online """
        return await self._repository.get_online_users(last_n_seconds=last_n_seconds)

    async def get_unique_users(self, min_rating: int = 1800, min_coins: int = 1000000) -> int:
        """ Get a number of users with extraordinary stats """
        return await self._repository.get_unique_users(min_rating=min_rating, min_coins=min_coins)

    async def get_by_username(self, username: str) -> UserBase:
        """ Retrieve user by username """
        return await self._repository.get_user(username=username)

    async def create_user(self, user_data: UserCreate) -> UserBase:
        """ Create new User with credentials provided """
        return await self._repository.create_user(user_data=user_data)

    async def update_user(self, uid: int, update_user: UserUpdate) -> UserOut:
        """ Update the User with credentials provided """
        if all(value is None for value in update_user.__dict__.values()):
            raise ValueError("At least one field must be provided for update.")
        if not await self.get_by_uid(uid=uid):
            logging.error(f"User with ID {uid} was not found")
            raise UserNotFoundException
        return await self._repository.update_user(uid=uid, update_user=update_user)
