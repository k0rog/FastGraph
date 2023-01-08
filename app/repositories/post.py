from sqlmodel import select
from sqlalchemy import func

from app.repositories.base import BaseRepository
from app.orm_models.post import Post


class PostRepository(BaseRepository):
    async def get_user_posts(self, user_id: int, offset: int, limit: int) -> list[Post]:
        async with self.session() as session:
            statement = select(Post).where(Post.user_id == user_id).offset(offset)
            if limit:
                statement.limit(limit)

            user = await session.execute(statement)
            return user.scalars()

    async def get_user_post_count(self, user_id: int) -> list[Post]:
        async with self.session() as session:
            user = await session.execute(
                select([func.count(Post.id)]).where(Post.user_id == user_id)
            )
            return user.scalars().first()
