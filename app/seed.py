import asyncio
import random
from datetime import datetime, timedelta
from faker import Faker
from sqlalchemy.exc import PendingRollbackError, IntegrityError
from database import AsyncSessionLocal
from models.user_model import User

faker = Faker('ru')


async def seed_fake_user(user_amount: int):
    async with AsyncSessionLocal() as session:
        for _ in range(user_amount):
            username = faker.unique.user_name()
            telegram_uid = random.randint(11111, 99999)
            last_login = faker.date_time_this_year()

            user = User(
                username=username,
                telegram_uid=telegram_uid,
                coins=random.randint(0, 10000000),
                rating=random.randint(0, 10000),
                last_login=last_login,
                last_logout=datetime.now() - timedelta(seconds=random.randint(10, 1200))
            )

            session.add(user)
            try:
                await session.commit()
            except (PendingRollbackError, IntegrityError):
                await session.rollback()

        await session.commit()

asyncio.run(seed_fake_user(user_amount=100))
