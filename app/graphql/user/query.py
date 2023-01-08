import graphene

from app.core.dependencies import get_user_service
from app.graphql.user.model import UserObject
from app.services.user import UserService


class UserQuery(graphene.ObjectType):
    users = graphene.List(UserObject, offset=graphene.Int(), limit=graphene.Int())

    async def resolve_users(self, info, offset=0, limit=None, user_service: UserService = next(get_user_service())):
        return await user_service.get_users(offset, limit)
