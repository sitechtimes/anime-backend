from graphene_django import DjangoObjectType
import graphene
from graphene_django.filter import DjangoFilterConnectionField
from django.contrib.auth import get_user_model
from .models import UserAnime, CustomUser, UserProfile
from anime.schema import AnimeNode, Anime
from graphql import GraphQLError


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
    # email = graphene.String(required = True)
    user_id = graphene.ID()
    # username = graphene.String(required = True)


class animeInput(graphene.InputObjectType):
    anime_name = graphene.String()
    rating = graphene.Int()
    anime_id = graphene.ID(required=True)
    watch_status = graphene.String()


class userAnimeInput(graphene.InputObjectType):
    # user_anime_id = graphene.ID(required = True)
    rating = graphene.Int()
    watch_status = graphene.String()
    anime_name = graphene.String(required=True)


class addRating(graphene.Mutation):
    class Arguments:
        user_data = userInput(required=True)
        anime_data = animeInput(required=True)

    user_anime = graphene.Field(UserAnimeNode)
    user = graphene.Field(UserProfileNode)
    # anime = graphene.Field(AnimeNode)

    @staticmethod
    def get_anime(id):
        return Anime.objects.get(pk=id)

    @staticmethod
    def get_user(id):
        return UserProfile.objects.get(user_id=id)

    def mutate(self, info, user_data=None, anime_data=None):
        anime = addRating.get_anime(anime_data.anime_id)
        user = addRating.get_user(user_data.user_id)

        # user = UserProfile.objects.create(
        #     user = CustomUser.objects.create(email = "ps@pls.com", username = "sdcfgdfgwerdfs")
        # )
        # user.save()

        if anime_data.rating and anime_data.watch_status:
            if anime_data.rating > 10 or anime_data.rating < 0:
                    return GraphQLError("rating needs to be between 0-10")
            print(anime_data.rating)
            user_anime = UserAnime(
                    anime = anime,
                    rating = anime_data.rating,
                    watching_status = anime_data.watch_status
                )
            user_anime.save()
            user.user_anime.add(user_anime)
            user.save()
            initial_rating = anime.number_rating
            rating_number = initial_rating + 1
            anime.number_rating = rating_number
            anime.save()
            print(anime.number_rating)
        elif anime_data.rating:
            if anime_data.rating > 10 or anime_data.rating < 0:
                    return GraphQLError("rating needs to be between 0-10")
            user_anime = UserAnime(
                    anime = anime,
                    rating = anime_data.rating,
                    # watching_status = anime_data.watch_status
                )
            user_anime.save()
            user.user_anime.add(user_anime)
            user.save()
            initial_rating = anime.number_rating
            rating_number = initial_rating + 1
            anime.number_rating = rating_number
            anime.save()
            print(anime.number_rating)
        elif anime_data.watch_status:
            user_anime = UserAnime(
                    anime = anime,
                    # rating = null,
                    watching_status = anime_data.watch_status
                )
            user_anime.save()
            user.user_anime.add(user_anime)
            user.save()
        return addRating(user=user, user_anime=user_anime)




class updateUserAnime(graphene.Mutation):
    class Arguments:
        user_data = userInput(required = True)
        user_anime_data = userAnimeInput(required = True)
    
    user_anime = graphene.Field(UserAnimeNode)
    user = graphene.Field(UserProfileNode)
    # anime = graphene.Field(AnimeNode)
    
    # @staticmethod
    # def get_user_anime(id):
    #     return UserAnime.objects.get(id = id)
    
    @staticmethod
    def get_user(id):
        return UserProfile.objects.get(user_id = id)
    
    def mutate(self, info, user_data=None, user_anime_data=None):
        # anime = addRating.get_anime(anime_data.anime_id)
        user = updateUserAnime.get_user(user_data.user_id)
        user_anime = user.user_anime.get(anime__anime_name = user_anime_data.anime_name)
        
        if user_anime_data.rating:
            user_anime.rating = user_anime_data.rating
        
        if user_anime_data.watch_status:
            user_anime.watching_status = user_anime_data.watch_status
            
        user_anime.save()
        
        # if user_anime == "":
        #     return GraphQLError("User anime does not exit")
        # user_anime = UserAnime.objects.filter(user_set__name = "johnson")
        print(user_anime)
        # print(UserAnime.objects.filter(anime_id = 1))
 
        return updateUserAnime(user=user, user_anime=user_anime) 
    
# class updateUserAnime(graphene.Mutation):
#     class Arguments:
#         user_data = userInput(required = True)
#         user_anime_data = userAnimeInput(required = True)
        
#     user = graphene.Field(UserProfileNode)
#     user_anime = graphene.Field(UserAnimeNode)
    
#     # @staticmethod
#     # def get_user_anime(id):
#     #     return UserAnime.objects.get(pk = id)
    
#     @staticmethod
#     def get_user(id):
#         return UserProfile.objects.get(user_id = id)
    
    
#     def mutate(self, info, user_data=None, anime_data=None):
#         # user_anime = updateUserAnime.get_user_anime(1)
#         # user = updateUserAnime.get_user(user_data.user_id)
        
#         user = UserProfile.objects.get(user_id=60)


#         return updateUserAnime(user=user)
    

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
    update_user_anime = updateUserAnime.Field()
