import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from anime.models import Anime, Genre, Awards, AnimeAwards
from users.models import UserProfile
# from users.models import CustomUser
from django.conf import settings

# from users.schema import animeInput, userInput


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
    class Arguments:
        user_data = userInput(required = True)
        anime_data = animeInput(required = True)
        award_name = graphene.String(required = True)
    
    anime_award = graphene.Field(AnimeAwardsNode)
    
    @staticmethod
    def get_user(id):
        return UserProfile.objects.get(user_id = id)
    
    @staticmethod
    def get_anime(name):
        return Anime.objects.get(anime_name = name)
    
    @staticmethod
    def get_award(name):
        return Awards.objects.get(award_name = name)
    
    def mutate(self, info, user_data=None, anime_data=None, award_name=None):
        user = addVote.get_user(user_data.user_id)
        anime = addVote.get_anime(anime_data.anime_name)
        award = addVote.get_award(award_name)
        print(user, anime, award)
        print("hi")
        try:
            print("dfg")
            anime_award = AnimeAwards.objects.get(anime__anime_name = anime_data.anime_name, award__award_name = award_name)
            print("This is the award:", anime_award)
            if anime_award:
                print("Anime exists")
                anime_award.vote_count += 1
                anime_award.save()
            
        except AnimeAwards.DoesNotExist:
            print("Anime Award does not exist and will now be created")
            anime_award = AnimeAwards(
                vote_count = 1,
                anime = anime,
                award = award,
            )
            # anime_award.allUsers.add(user)
            anime_award.save()
            print(anime_award)
        return addVote(anime_award = anime_award) 
    

# class addVote(graphene.Mutation):
#     class Arguments:
#         user_data = userInput(required = True)
#         anime_data = animeInput(required = True)
#         award_name = graphene.String(required = True)
    
#     vote = graphene.Field(VoteNode)
#     # user = graphene.Field(UserProfileNode)
#     # anime = graphene.Field(AnimeNode)
    
#     # @staticmethod
#     # def get_user_anime(id):
#     #     return UserAnime.objects.get(id = id)
    
#     @staticmethod
#     def get_user(id):
#         return settings.AUTH_USER_MODEL.objects.get(user_id = id)
    
#     def mutate(self, info, user_data=None, anime_data=None, award_name=None):
#         # anime = addRating.get_anime(anime_data.anime_id)
#         user = addVote.get_user(user_data.user_id)
#         anime = Anime.objects.get(anime_name = anime_data.anime_name)

#         vote = Vote(
#             user = user,
#             anime = anime,
#             award = award_name
#         )

#         vote.save()

        
#         # if user_anime == "":
#         #     return GraphQLError("User anime does not exit")
#         # user_anime = UserAnime.objects.filter(user_set__name = "johnson")
#         # print(UserAnime.objects.filter(anime_id = 1))
 
#         return addVote(vote=vote) 
    
class Mutation(graphene.ObjectType):
    add_vote = addVote.Field()