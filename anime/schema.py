import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from anime.models import Anime, Genre, Awards, AnimeAwards, AllWinners
from users.models import UserProfile
# from users.models import CustomUser
from django.conf import settings
from graphql import GraphQLError

# from scripts.winner import FindAwardWinner

# from users.schema import animeInput, userInput
from datetime import date
today = date.today()

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

class AllWinnersNode(DjangoObjectType):
    class Meta:
        model = AllWinners
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
    
    winner = graphene.relay.Node.Field(AllWinnersNode)
    all_winners = DjangoFilterConnectionField(AllWinnersNode)
    # def resolve_winners(self, info):

        

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
    def get_anime(id):
        return Anime.objects.get(mal_id = id)
    
    @staticmethod
    def get_award(name):
        return Awards.objects.get(award_name = name)
    
    def mutate(self, info, user_data=None, anime_data=None, award_name=None):
        user = addVote.get_user(user_data.user_id)
        anime = addVote.get_anime(anime_data.anime_id)
        award = addVote.get_award(award_name)
        print(user, anime, award)
        print("hi")
        try:
            try:
                all_anime_awards = AnimeAwards.objects.filter(award__award_name = award_name)
                print(all_anime_awards)
                user_exist = all_anime_awards.filter(allUsers = user)
                print(user_exist)
                if user_exist:
                    print("user already voted for this award")
                    return GraphQLError("user already voted for this award")
                
            except Exception:
                print("there was an error ")
                ["award1", "blue lock"]
            anime_award = AnimeAwards.objects.get(anime__mal_id = anime_data.anime_id, award__award_name = award_name)
            print("This is the award:", anime_award)
            if anime_award:
                print("Anime exists")
                # if user in anime_award.allUsers.all():
                #     print("user already voted for this anime for this award")
                #     return GraphQLError("user already voted for this anime for this award")
                anime_award.vote_count += 1
                anime_award.allUsers.add(user)
                anime_award.save()
                user.user_voted_animes.add(anime_award)
                user.save()
            
        except AnimeAwards.DoesNotExist:
            print("Anime Award does not exist and will now be created")
            anime_award = AnimeAwards(
                vote_count = 1,
                anime = anime,
                award = award,
            )
            # anime_award.allUsers.add(user)
            anime_award.save()
            anime_award.allUsers.add(user)
            anime_award.save()
            user.user_voted_animes.add(anime_award)
            user.save()
            print(anime_award)
        return addVote(anime_award = anime_award) 
    
class winner(graphene.Mutation):
    anime_awards = graphene.List(AllWinnersNode)
    # anime = graphene.Field(AnimeNode)
    
    def mutate(self, info):
        date = today
        anime_awards = []
        
        all_awards = Awards.objects.all()
        
        for award in all_awards:
            anime_awards.append(award)
        
        for anime_award in anime_awards:
            try:
                all_anime_awards = AnimeAwards.objects.filter(award__award_name = anime_award)
                highest_vote_count = max(all_anime_awards, key=lambda y: y.vote_count).vote_count
                print(highest_vote_count)
                
                filtered_anime_awards = all_anime_awards.filter(vote_count = highest_vote_count)
                print(len(filtered_anime_awards))
                for filtered_anime_award in filtered_anime_awards:
                    # if filtered_anime_award in AllWinners.objects.all():
                    #     return GraphQLError(f"{filtered_anime_award.anime.anime_name} has already won the {filtered_anime_award.award.award_name} award")
                    
                    filtered_anime_name = filtered_anime_award.anime.anime_name
                    filtered_award_name = filtered_anime_award.award.award_name
                    filtered_anime = Anime.objects.get(anime_name = filtered_anime_name)
                    filtered_award = Awards.objects.get(award_name = filtered_award_name)
                    filtered_award.date = date
                    filtered_award.save()
                    print(date)
                    filtered_anime.anime_awards.add(filtered_award)
                    filtered_anime.save()
                    # return filtered_anime
    
                    AllWinners.objects.create(winner = filtered_anime_award)
                    # print(self.all_winners)
                    # print(filtered_anime_award, filtered_anime_name)
                    print(f"The {filtered_award_name} Award goes to {filtered_anime_name}")

            except:
                print("there is an error")
        print(AllWinners.objects.all())
        # FindAwardWinner = FindAwardWinner()
        # # FindAwardWinner.determine_winner()
        # anime_awards = FindAwardWinner.determine_winner()
        return winner(anime_awards = AllWinners.objects.all())
        
    
class Mutation(graphene.ObjectType):
    add_vote = addVote.Field()
    winner = winner.Field()