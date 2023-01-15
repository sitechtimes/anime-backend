from graphene_django import DjangoObjectType
import graphene
from graphene_django.filter import DjangoFilterConnectionField
from django.contrib.auth import get_user_model
from .models import UserAnime, CustomUser, UserProfile, Anime
from anime.schema import AnimeNode


class UserAnimeNode(DjangoObjectType):
    class Meta:
        model = UserAnime
        fields = "__all__"
        filter_fields = "__all__"
        interfaces = (graphene.relay.Node,)


class UserNode(DjangoObjectType):
    class Meta:
        model = CustomUser
        fields = "__all__"
        filter_fields = "__all__"
        interfaces = (graphene.relay.Node,)

class UserProfileNode(DjangoObjectType):
    class Meta:
        model = UserProfile
        fields = "__all__"
        filter_fields = "__all__"
        interfaces = (graphene.relay.Node,)



class Query(object):
    user_anime = graphene.relay.Node.Field(UserAnimeNode)
    all_user_anime = DjangoFilterConnectionField(UserAnimeNode)

    # user = graphene.relay.Node.Field(UserNode)
    # all_users = DjangoFilterConnectionField(UserNode)

    user_profile = graphene.relay.Node.Field(UserProfileNode)
    all_users = DjangoFilterConnectionField(UserProfileNode)








class userInput(graphene.InputObjectType):
    email = graphene.String(required = True)
    # user_id = graphene.ID()
    # username = graphene.String(required = True)
    
class animeInput(graphene.InputObjectType):
    anime_name = graphene.String(required = True)
    rating = graphene.Int(required = True)
    
class addRating(graphene.Mutation):
    class Arguments:
        user_data = userInput(required = True)
        anime_data = animeInput(required = True)
    
    anime = graphene.Field(UserAnimeNode)
    user = graphene.Field(UserProfileNode)
    
    @staticmethod
    def get_anime(name):
        return Anime.objects.get(anime_name = name)
    
    @staticmethod
    def get_user(email):
        return UserProfile.objects.get(email = email)
    
    def mutate(self, info, user_data=None, anime_data=None):
        anime = addRating.get_anime(anime_data.anime_name)
        user = addRating.get_user(user_data.user_id)
        if anime_data.rating:
            user_anime = UserAnime(
                anime = anime,
                rating = anime_data.rating
            )
            user_anime.save()
            user.user_anime.add(user_anime)
            user.save()
            return addRating(user=user, anime=user_anime)
# class addUserAnime(graphene.Mutation):
#     class Arguments:
#         user_data = userInput(required = True)
#         anime_data = animeInput(required = True)
        
#     user = graphene.Field(UserProfileNode)
    
#     def mutate(self, info, user_data=None, anime_data=None):
        
    

class CreateUser(graphene.Mutation):

    user = graphene.Field(UserNode)

    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        user = get_user_model()(
            username= username,
            email=email,
            password=password
        )
        user.set_password(password)
        user.save()

        return CreateUser(user=user)

# class CreateUserProfile(graphene.Mutation):
#
#     user_profile = graphene.Field( UserProfileNode)
#
#     class Arguments:
#         username = graphene.String(required=True)
#         email = graphene.String(required=True)
#         password = graphene.String(required=True)
#
#     def mutate(self, info, username, password, email):
#         user = get_user_model()(
#             username= username,
#             email=email,
#             password=password
#         )
#         user.set_password(password)
#         user.save()
#
#         return CreateUser(user=user)



class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    add_rating = addRating.Field()
