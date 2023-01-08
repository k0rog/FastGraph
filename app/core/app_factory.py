import graphene
from fastapi import FastAPI
from starlette_graphene3 import GraphQLApp

from app.graphql.user.query import UserQuery
from app.graphql.user.mutation import UserMutation


def create_app():
    app = FastAPI()

    app.add_route("/graphql", GraphQLApp(schema=graphene.Schema(query=UserQuery, mutation=UserMutation)))

    return app
