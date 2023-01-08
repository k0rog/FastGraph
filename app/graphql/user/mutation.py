import graphene

from app.core.dependencies import get_user_service
from app.graphql.user.model import UserObject
from app.services.user import UserService


class UserMutationInput(graphene.InputObjectType):
    email = graphene.String()
    first_name = graphene.String()
    last_name = graphene.String()
    phone = graphene.String()


class CreateUserMutation(graphene.Mutation):
    class Arguments:
        user_input = UserMutationInput()

    user = graphene.Field(UserObject)

    async def mutate(
            self, info, email, first_name, last_name, phone, user_service: UserService = next(get_user_service())
    ):
        user = await user_service.create_user(email, first_name, last_name, phone)
        return CreateUserMutation(user=user)


class UpdateUserMutation(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int()
        user_input = UserMutationInput(required=False)

    is_successful = graphene.Boolean()

    async def mutate(
            self,
            info,
            user_id,
            user_input=None,
            user_service: UserService = next(get_user_service())
    ):
        is_successful = await user_service.update_user(user_id, **user_input)
        return UpdateUserMutation(is_successful=is_successful)


class UserMutation(graphene.ObjectType):
    create_user = CreateUserMutation.Field()
    update_user = UpdateUserMutation.Field()
