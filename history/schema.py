from graphene_django import DjangoObjectType
import graphene
from graphene_django.filter import DjangoFilterConnectionField
from history.models import RatedAnime, MostSearchedAnime, History


class RatedAnimeNode(DjangoObjectType):
    class Meta:
        model = RatedAnime
        fields = "__all__"
        filter_fields = "__all__"
        interfaces = (graphene.relay.Node,)


class  MostSearchedAnimeNode(DjangoObjectType):
    class Meta:
        model =  MostSearchedAnime
        fields = "__all__"
        filter_fields = "__all__"
        interfaces = (graphene.relay.Node,)

# class SeasonalAnimeAwardsNode(DjangoObjectType):
#     class Meta:
#         model = SeasonalAnimeAwards
#         fields = "__all__"
#         filter_fields = "__all__"
#         interfaces = (graphene.relay.Node,)

class HistoryNode(DjangoObjectType):
    class Meta:
        model =History
        fields = "__all__"
        filter_fields = "__all__"
        interfaces = (graphene.relay.Node,)



class Query(object):
    rated_anime = graphene.relay.Node.Field(RatedAnimeNode)
    all_rated_anime  = DjangoFilterConnectionField(RatedAnimeNode)

    most_searched_anime = graphene.relay.Node.Field(MostSearchedAnimeNode)
    all_most_searched_anime = DjangoFilterConnectionField(MostSearchedAnimeNode)

    # seasonal_anime_awards = graphene.relay.Node.Field(SeasonalAnimeAwardsNode)
    # all_seasonal_anime_awards = DjangoFilterConnectionField(SeasonalAnimeAwardsNode)

    history = graphene.relay.Node.Field(HistoryNode)
    all_history = DjangoFilterConnectionField(HistoryNode)

