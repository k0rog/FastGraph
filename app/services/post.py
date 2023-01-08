from app.orm_models.post import Post
from app.repositories.post import PostRepository


class PostService:
    def __init__(self, repository: PostRepository):
        self.repository = repository

    async def get_user_posts(self, user_id, offset: int, limit: int) -> list[Post]:
        return await self.repository.get_user_posts(user_id, offset, limit)

    async def get_user_post_count(self, user_id) -> list[Post]:
        return await self.repository.get_user_post_count(user_id)
