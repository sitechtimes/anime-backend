import graphene
from graphene import Date
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from anime.models import Anime, Genre, Awards, AnimeAwards, AllWinners, Studio, Character
from users.models import UserProfile
# from users.models import CustomUser
from django.conf import settings

class GenreNode(DjangoObjectType):
    class Meta:
        model = Genre
        filter_fields = "__all__"
        interfaces = (graphene.relay.Node,)


class AwardsNode(DjangoObjectType):
    class Meta:
        model = Awards
        fields = "__all__"
        filter_fields = "__all__"
        interfaces = (graphene.relay.Node,)


class AnimeAwardsNode(DjangoObjectType):
    class Meta:
        model = AnimeAwards
        fields = "__all__"
        filter_fields = "__all__"
        interfaces = (graphene.relay.Node,)



class AnimeNode(DjangoObjectType):
    class Meta:
        model = Anime
        fields = "__all__"
        filter_fields = "__all__"
        interfaces = (graphene.relay.Node,)

class CharacterNode(DjangoObjectType):
    class Meta:
        model = Character
        fields = "__all__"
        filter_fields = "__all__"
        interfaces = (graphene.relay.Node,)


# class VoteNode(DjangoObjectType):
#     class Meta:
#         model = Vote
#         fields = "__all__"
#         filter_fields = "__all__"
#         interfaces = (graphene.relay.Node,)

class Query(object):
    genre = graphene.relay.Node.Field(GenreNode)
    all_genres = DjangoFilterConnectionField(GenreNode)

    awards = graphene.relay.Node.Field(AwardsNode)
    all_awards = DjangoFilterConnectionField(AwardsNode)

    anime_awards = graphene.relay.Node.Field(AnimeAwardsNode)
    all_anime_awards = DjangoFilterConnectionField(AnimeAwardsNode)

    anime = graphene.relay.Node.Field(AnimeNode)
    all_anime = DjangoFilterConnectionField(AnimeNode)
    
    winner = graphene.relay.Node.Field(AllWinnersNode)
    all_winners = DjangoFilterConnectionField(AllWinnersNode)
    
    character = graphene.relay.Node.Field(CharacterNode)
    all_characters = DjangoFilterConnectionField(CharacterNode)
    # def resolve_winners(self, info):
    # def resolve_characters()
        

    # vote = graphene.relay.Node.Field(VoteNode)
    # all_vote = DjangoFilterConnectionField(VoteNode)
    
    
    
class userInput(graphene.InputObjectType):
    # email = graphene.String(required = True)
    user_id = graphene.ID()
    # username = graphene.String(required = True)


class animeInput(graphene.InputObjectType):
    anime_name = graphene.String()
    rating = graphene.Int()
    anime_id = graphene.ID()
    watch_status = graphene.String()

# class awardInput(graphene.InputObjectType):
#     award_name = graphene.String()

class addVote(graphene.Mutation):
    pass





