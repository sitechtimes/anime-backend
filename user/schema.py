import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from.models import UserAnime, User


class UserAnimeNode(DjangoObjectType):
    class Meta:
        model = UserAnime
        fields = ("__all__", )
        interfaces = (graphene.relay.Node,)


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        fields = ("__all__", )
        interfaces = (graphene.relay.Node,)



class Query(object):
    user_anime = graphene.relay.Node.Field(UserAnimeNode)
    all_user_anime = DjangoFilterConnectionField(UserAnimeNode)

    user = graphene.relay.Node.Field(UserNode)
    all_users = DjangoFilterConnectionField(UserNode)

