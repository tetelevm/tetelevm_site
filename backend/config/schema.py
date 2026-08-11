import graphene


class Query(graphene.ObjectType):
    status = graphene.String(default_value="ok")


schema = graphene.Schema(query=Query)
