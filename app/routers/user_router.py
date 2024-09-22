from typing import List

from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from exceptions_custom import UserNotFoundException, IntegrityDataException
from pydantic_schema.base_schemes import UserBase, UserOut, UserCreate, UserUpdate
from security import check_token
from services.user_service import UserService

router = APIRouter(
    prefix='/user',
)


@router.get("", response_model=List[UserOut])
async def get_all(db: AsyncSession = Depends(get_db), api_key: str = Security(check_token)):
    """ Get a list of all users registered

    :param:

        db: AsyncSession within database (Dependency injections)

    :returns:

        List[UserOut]: a list of User models
    """
    return await UserService(session=db).get_all()


@router.get("/{username}", response_model=UserOut)
async def get_by_username(username: str, db: AsyncSession = Depends(get_db), api_key: str = Security(check_token)):
    """ Retrieve a User by username

    :param:

        username: User's username to search for
        db: AsyncSession within database (Dependency injections)

    :raise:

        HTTPException(404): If the user with username provided is not found

    :returns:

        UserOut: a User model
    """
    try:
        return await UserService(session=db).get_by_username(username=username)
    except UserNotFoundException:
        raise HTTPException(status_code=404, detail="User not found")


@router.post("", response_model=UserBase)
async def create_user(user_data: UserCreate, db: AsyncSession = Depends(get_db),
                      api_key: str = Security(check_token)):
    """ Create new User

    :param:

        user_data:
            username: new User's username
            telegram_uid: new User's telegram_id
            coins: a number of a new User's coins. Then initial number is 0 by default
            rating: a number of a new User's rating. Then initial number is 0 by default

        db: AsyncSession within database (Dependency injections)

    :raise:

        HTTPException(409): If there was a DB data violation

    :returns:

        UserBase: a User model
    """
    try:
        return await UserService(session=db).create_user(user_data=user_data)
    except IntegrityDataException as exc:
        raise HTTPException(status_code=409, detail=f"Data integrity error: {exc.args[0]}")


@router.put("/{uid}", response_model=UserOut)
async def update_user(uid: int, updates: UserUpdate, db: AsyncSession = Depends(get_db),
                      api_key: str = Security(check_token)):
    """ Update an existing User

    :param:

        uid: an ID of a User to be updated

        updates (all fields are optional):
            username: new User's username
            coins: a number of a new User's coins. Then initial number is 0 by default
            rating: a number of a new User's rating. Then initial number is 0 by default

        db: AsyncSession within database (Dependency injections)

    :raise:

        HTTPException(404): If the user with ID provided is not found
        HTTPException(409): If there was a DB data violation
        HTTPException(422): If there were no params provided for update

    :returns:

        UserOut: a User model
    """
    print(updates)
    try:
        return await UserService(
            session=db
        ).update_user(
            uid=uid, update_user=updates
        )
    except UserNotFoundException:
        raise HTTPException(status_code=404, detail="User not found")
    except ValueError:
        raise HTTPException(status_code=422, detail="At least one field must be provided for update.")
    except IntegrityDataException as exc:
        raise HTTPException(status_code=409, detail=f"Data integrity error: {exc.args[0]}")
