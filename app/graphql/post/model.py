import graphene


class PostObject(graphene.ObjectType):
    id = graphene.Int()
    text = graphene.String()
    date = graphene.DateTime()

    def resolve_id(self, info):
        return self.id

    def resolve_text(self, info):
        return self.text

    def resolve_date(self, info):
        return self.date
