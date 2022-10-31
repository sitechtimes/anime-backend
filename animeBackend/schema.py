import graphene
import user.schema

class Query(
    user.schema.Query, # Add your Query objects here
    graphene.ObjectType
):
    pass

# class Mutation(
#     my_app.schema.Mutation, # Add your Mutation objects here
#     graphene.ObjectType
# ):
#     pass

schema = graphene.Schema(query=Query)



