import graphene
from graphene import Date
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from.models import Anime, Genre, Awards, AnimeAwards
from graphql import GraphQLError

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


class Query(object):
    genre = graphene.relay.Node.Field(GenreNode)
    all_genres = DjangoFilterConnectionField(GenreNode)

    awards = graphene.relay.Node.Field(AwardsNode)
    all_awards = DjangoFilterConnectionField(AwardsNode)

    anime_awards = graphene.relay.Node.Field(AnimeAwardsNode)
    all_anime_awards = DjangoFilterConnectionField(AnimeAwardsNode)

    anime = graphene.relay.Node.Field(AnimeNode)
    all_anime = DjangoFilterConnectionField(AnimeNode)


class CreateAward(graphene.Mutation):

    award = graphene.Field(AwardsNode)

    class Arguments:
        name = graphene.String(required=True)

    def mutate(self, info, name):
        try:
            # if it can find an award with the given name, it will move on to the next line
            # if not, it will jump to except
            Awards.objects.get(award_name=name)

            return GraphQLError("an award with this name already exists")

        except Awards.DoesNotExist:
            award = Awards(award_name=name)
            award.save()

        return CreateAward(award=award)

class CreateAnimeAwardsObj(graphene.Mutation):
    anime_awards = graphene.Field(AnimeAwardsNode)

    class Arguments:
        nom = graphene.Boolean(required=True)
        nom_date = Date()
        got = graphene.Boolean(required=True)
        got_date = Date()
        award_name = graphene.String(required=True)

    def mutate(self, info, nom, nom_date, got, got_date, award_name):
        anime_awards = AnimeAwards(
            nominated_for_award=nom,
            nominated_date=nom_date,
            has_award=got,
            received_date=got_date,
            anime_award_name=Awards.objects.get(award_name=award_name),
        )
        # print(anime_awards.nominated_for_award)
        # # print(anime_awards.nominated_date)
        # # print(anime_awards.has_award)
        # # print(anime_awards.received_date)
        # # print(anime_awards.anime_award_name)
        # print(anime_awards)

        anime_awards.save()
        return CreateAnimeAwardsObj(anime_awards=anime_awards)



# class CreateAnimeAwardsObj(graphene.Mutation):
#     anime_awards = graphene.Field(AnimeAwardsNode)
#
#     class Arguments:
#         nom = graphene.Boolean()
#         has = graphene.Boolean()
#
#     def mutate(self, info, nom, has):
#         anime_awards_obj = AnimeAwards(nominated_for_award=nom, has_award=has)
#         anime_awards_obj.save()
#         print(anime_awards_obj)
#         print("sdc")
#         return CreateAnimeAwardsObj(anime_awards=anime_awards_obj)

class AssignAnimeAwardsToAnime(graphene.Mutation):
    anime = graphene.Field(AnimeNode)

    class Arguments:
        anime_name = graphene.String()
        award_name = graphene.String()

    def mutate(self, info, anime_name, award_name):

        my_anime = Anime.objects.get(anime_name=anime_name)
        my_anime_awards = AnimeAwards.objects.get(anime_award_name__award_name=award_name)
        my_anime.anime_awards.add(my_anime_awards)
        my_anime.save()

        return AssignAnimeAwardsToAnime(anime=my_anime)



class Mutation(graphene.ObjectType):
    create_award = CreateAward.Field()
    create_anime_awards_obj = CreateAnimeAwardsObj.Field()
    assign_anime_awards_to_anime = AssignAnimeAwardsToAnime.Field()





