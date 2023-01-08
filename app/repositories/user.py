from typing import Union

from sqlmodel import select, update

from app.repositories.base import BaseRepository
from app.orm_models.user import User


class UserRepository(BaseRepository):
    async def get_users(self, offset: int, limit: Union[int, None]) -> list[User]:
        statement = select(User).offset(offset)
        if limit:
            statement.limit(limit)

        async with self.session() as session:
            users = await session.execute(statement)

            return users.scalars()

    async def create_user(self, email: str, first_name: str, last_name: str, phone: str) -> User:
        user = User(email=email, first_name=first_name, last_name=last_name, phone=phone)
        self.session.add(user)
        await self.session.commit()
        return user

    async def update_user(
            self,
            user_id: int,
            **kwargs
    ) -> bool:
        statement = update(User).filter(User.id == user_id).values(
            **{key: value for key, value in kwargs.items() if value}
        )
        async with self.session() as session:
            cursor = await session.execute(statement)
            return bool(cursor.rowcount)
