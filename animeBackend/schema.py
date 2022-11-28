import graphene
import users.schema
import anime.schema


class Query(
    anime.schema.Query, # Add your Query objects here
    users.schema.Query,
    graphene.ObjectType
):
    pass


class Mutation(
    users.schema.Mutation,
    graphene.ObjectType
):

    pass


schema = graphene.Schema(query=Query, mutation= Mutation )
# schema = graphene.Schema(query=Query, mutation=Mutation)



