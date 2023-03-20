import graphene
import user.schema
import anime.schema

class Query(
    anime.schema.Query, # Add your Query objects here
    user.schema.Query,
    graphene.ObjectType
):
    pass

class Mutation(
    anime.schema.Mutation, # Add your Mutation objects here
    graphene.ObjectType
):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)



