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
    
    user_anime_data = graphene.Field(UserProfileNode, id = graphene.ID())
    
    specific_user_anime = graphene.List(UserAnimeNode, id = graphene.ID())
    
    def resolve_user_anime_data(root, info, id):
        user = UserProfile.objects.get(user_id=id)
        # user_anime = user.filter(user_anime__anime__anime_name = anime_name)
        return user
    def resolve_specific_user_anime(root, info, id):
        user_anime = UserAnime.objects.filter(anime__mal_id = id)
        return user_anime


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
    # anime_name = graphene.String(required=True)


class addUserAnime(graphene.Mutation):
    class Arguments:
        user_data = userInput(required=True)
        anime_data = animeInput(required=True)

    user_anime = graphene.Field(UserAnimeNode)
    user = graphene.Field(UserProfileNode)
    # anime = graphene.Field(AnimeNode)

    @staticmethod
    def get_anime(id):
        return Anime.objects.get(mal_id=id)


    @staticmethod
    def get_user(id):
        return UserProfile.objects.get(user_id=id)

    def mutate(self, info, user_data=None, anime_data=None):
        anime = addUserAnime.get_anime(anime_data.anime_id)
        user = addUserAnime.get_user(user_data.user_id)

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
            user.user_anime.add(user_anime)
            user.save()

            total_num_rated = anime.num_rated + 1
            anime.num_rated =  total_num_rated 
            new_avg_rated = (anime.avg_rating +  anime_data.rating) / total_num_rated
            anime.avg_rating = new_avg_rated
            anime.save()


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
            total_num_rated = anime.num_rated + 1
            anime.num_rated =  total_num_rated 
            new_avg_rated = (anime.avg_rating +  anime_data.rating) / total_num_rated
            anime.avg_rating = new_avg_rated
            anime.save()

            print(anime.avg_rating)
        elif anime_data.watch_status:
            user_anime = UserAnime(
                    anime = anime,
                    # rating = null,
                    watching_status = anime_data.watch_status
                )
            user_anime.save()
            user.user_anime.add(user_anime)
            user.save()
        return addUserAnime(user=user, user_anime=user_anime)




class updateUserAnime(graphene.Mutation):
    @staticmethod
    def get_anime(name):
        return Anime.objects.get(anime_name=name)


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
        anime =  addUserAnime.get_anime( user_anime_data.anime_name)
        print(user_anime_data.anime_name)

        
        if user_anime_data.rating:
            anime.avg_rating =((anime.avg_rating -  user_anime.rating) + user_anime_data.rating)/anime.num_rated          
            anime.save()
            user_anime.rating = user_anime_data.rating
           
            
        
        if user_anime_data.watch_status:
            user_anime.watching_status = user_anime_data.watch_status
            
        user_anime.save()
        
        # if user_anime == "":
        #     return GraphQLError("User anime does not exit")
        # user_anime = UserAnime.objects.filter(user_set__name = "johnson")

        # print(UserAnime.objects.filter(anime_id = 1))
 
        return updateUserAnime(user=user, user_anime=user_anime, anime=anime) 
    



class UserAnimeMutation(graphene.Mutation):
    class Arguments:
        user_data = userInput(required=True)
        anime_data = animeInput(required=True)
        user_anime_data = userAnimeInput(required = True)
    

    user_anime = graphene.Field(UserAnimeNode)
    user = graphene.Field(UserProfileNode)
    anime = graphene.Field(AnimeNode)

    @staticmethod
    def get_anime(id):
        return Anime.objects.get(mal_id=id)


    @staticmethod
    def get_user(id):
        return UserProfile.objects.get(user_id=id)

    def mutate(self, info, user_data=None, anime_data=None, user_anime_data=None):
        anime = addUserAnime.get_anime(anime_data.anime_id)
        user = addUserAnime.get_user(user_data.user_id)
        
        
        try:
 
            user_anime = user.user_anime.get(anime__mal_id = anime.mal_id)
            print("user anime exists")
                
            if user_anime_data.rating:
                anime.avg_rating =((anime.avg_rating * anime.num_rated - user_anime.rating) + user_anime_data.rating)/anime.num_rated          
                anime.save()
                user_anime.rating = user_anime_data.rating
                user_anime.save()
            
            
        
            if user_anime_data.watch_status:
                user_anime.watching_status = user_anime_data.watch_status
            
                user_anime.save()
        
        # if user_anime == "":
        #     return GraphQLError("User anime does not exit")
        # user_anime = UserAnime.objects.filter(user_set__name = "johnson")

        # print(UserAnime.objects.filter(anime_id = 1))
 
            return UserAnimeMutation(user=user, user_anime=user_anime, anime=anime) 
        except Exception:
            print("anime does not exist and will be created")
            #i feel likle you can cut this down to only if-statements
            if user_anime_data.rating and user_anime_data.watch_status:
                if user_anime_data.rating > 10 or user_anime_data.rating < 0:
                    return GraphQLError("rating needs to be between 0-10")
                print(user_anime_data.watch_status)
                user_anime = UserAnime(
                        anime = anime,
                        rating = user_anime_data.rating,
                        watching_status = user_anime_data.watch_status
                    )
                user_anime.save()
                user.user_anime.add(user_anime)
                user.save()
                user.user_anime.add(user_anime)
                user.save()

                total_num_rated = anime.num_rated + 1
                anime.num_rated =  total_num_rated 
                new_avg_rated = (anime.avg_rating +  user_anime_data.rating) / total_num_rated
                anime.avg_rating = new_avg_rated
                anime.save()


            elif user_anime_data.rating:
                if user_anime_data.rating > 10 or user_anime_data.rating < 0:
                        return GraphQLError("rating needs to be between 0-10")
                user_anime = UserAnime(
                        anime = anime,
                        rating = user_anime_data.rating,
                        # watching_status = anime_data.watch_status
                    )
                
                user_anime.save()
                user.user_anime.add(user_anime)
                user.save()
                total_num_rated = anime.num_rated + 1
                anime.num_rated =  total_num_rated 
                new_avg_rated = (anime.avg_rating +  user_anime_data.rating) / total_num_rated
                anime.avg_rating = new_avg_rated
                anime.save()

                print(anime.avg_rating)
            elif user_anime_data.watch_status:
                user_anime = UserAnime(
                        anime = anime,
                        # rating = null,
                        watching_status = user_anime_data.watch_status
                    )
                user_anime.save()
                user.user_anime.add(user_anime)
                user.save()
            return UserAnimeMutation(user=user, user_anime=user_anime, anime=anime)
            

        
      





class Mutation(graphene.ObjectType):
    # add_user_anime = addUserAnime.Field()
    # update_user_anime = updateUserAnime.Field()
    user_anime_mutation = UserAnimeMutation.Field()
