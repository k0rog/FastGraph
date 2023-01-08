import graphene

from app.core.dependencies import get_post_service
from app.graphql.post.model import PostObject
from app.services.post import PostService


class UserObject(graphene.ObjectType):
    id = graphene.Int()
    email = graphene.String()
    first_name = graphene.String()
    last_name = graphene.String()
    phone = graphene.String()
    posts = graphene.List(PostObject, offset=graphene.Int(), limit=graphene.Int())
    post_count = graphene.Int()

    def resolve_id(self, info):
        return self.id

    def resolve_email(self, info):
        return self.email

    def resolve_first_name(self, info):
        return self.first_name

    def resolve_last_name(self, info):
        return self.last_name

    def resolve_phone(self, info):
        return self.phone

    async def resolve_posts(self, info, offset=0, limit=None, service: PostService = next(get_post_service())):
        return await service.get_user_posts(self.id, offset, limit)

    async def resolve_post_count(self, info, service: PostService = next(get_post_service())):
        return await service.get_user_post_count(self.id)
