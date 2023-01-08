from app.db.base import async_session
from app.repositories.post import PostRepository
from app.services.post import PostService
from app.repositories.user import UserRepository
from app.services.user import UserService


def get_post_repository():
    yield PostRepository(async_session)


def get_post_service(repository: PostRepository = next(get_post_repository())):
    yield PostService(repository)


def get_user_repository():
    yield UserRepository(async_session)


def get_user_service(repository: UserRepository = next(get_user_repository())):
    yield UserService(repository)
