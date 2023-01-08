from typing import Union

from app.orm_models.user import User
from app.repositories.user import UserRepository


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def get_users(self, offset: int, limit: Union[int, None]) -> list[User]:
        return await self.repository.get_users(offset, limit)

    async def create_user(self, email: str, first_name: str, last_name: str, phone: str) -> User:
        return await self.repository.create_user(email, first_name, last_name, phone)

    async def update_user(
            self,
            user_id: int,
            email: Union[str, None] = None,
            first_name: Union[str, None] = None,
            last_name: Union[str, None] = None,
            phone: Union[str, None] = None
    ) -> bool:
        return await self.repository.update_user(
            user_id,
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone=phone
        )
