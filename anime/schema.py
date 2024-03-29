import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from anime.models import Anime, Genre, Awards, AnimeAwards, AllWinners, Studio, Character, CharacterAwards, CharacterAwardsWinner
from users.models import UserProfile
# from users.models import CustomUser
from django.conf import settings
from graphql import GraphQLError

# from scripts.winner import FindAwardWinner

# from users.schema import animeInput, userInput
from datetime import date
import datetime
# month = datetime.datetime.month()


today = date.today()
month = date.today().month
year = date.today().year
season = ""

match month:
    case 1|2|3:
        season = "Winter"
    case 4|5|6:
        season = "Spring"
    case 7|8|9:
        season = "Summer"
    case 10|11|12:
        season = "Fall"
    case None:
        season = ""





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
class CharacterAwardsNode(DjangoObjectType):
    class Meta:
        model = CharacterAwards
        fields = "__all__"
        filter_fields = "__all__"
        interfaces = (graphene.relay.Node,)


class AnimeStudioNode(DjangoObjectType):
    class Meta:
        model =  Studio
        fields = "__all__"
        filter_fields = "__all__"
        interfaces = (graphene.relay.Node,)

class AllWinnersNode(DjangoObjectType):
    class Meta:
        model = AllWinners
        fields = "__all__"
        filter_fields = "__all__"
        interfaces = (graphene.relay.Node,)
        
class CharacterAwardsWinnerNode(DjangoObjectType):
    class Meta:
        model = CharacterAwardsWinner
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

# class CombWinners(graphene.Union):
#     class Meta:
#         types = (AllWinnersNode, CharacterAwardsWinnerNode)
        
#     def resolve_type(self, info):
#         if isinstance(self, AllWinners):
#             return AllWinnersNode
#         elif isinstance(self, CharacterAwardsWinner):
#             return CharacterAwardsWinnerNode
#         else:
#             raise Exception('Unknown type of winner')

# class VoteNode(DjangoObjectType):
#     class Meta:
#         model = Vote
#         fields = "__all__"
#         filter_fields = "__all__"
#         interfaces = (graphene.relay.Node,)

class Query(object):
    genre = graphene.relay.Node.Field(GenreNode)
    all_genres = DjangoFilterConnectionField(GenreNode)

    studio = graphene.relay.Node.Field(AnimeStudioNode)
    all_studios = DjangoFilterConnectionField(AnimeStudioNode)

    awards = graphene.relay.Node.Field(AwardsNode)
    all_awards = DjangoFilterConnectionField(AwardsNode)

    anime_awards = graphene.relay.Node.Field(AnimeAwardsNode)
    all_anime_awards = DjangoFilterConnectionField(AnimeAwardsNode)
    
    character_awards = graphene.relay.Node.Field(AnimeAwardsNode)
    all_character_awards = DjangoFilterConnectionField(AnimeAwardsNode)

    anime = graphene.relay.Node.Field(AnimeNode)
    all_anime = DjangoFilterConnectionField(AnimeNode)
    
    character_winner = graphene.relay.Node.Field(CharacterAwardsWinnerNode)
    all_character_winners = DjangoFilterConnectionField(CharacterAwardsWinnerNode)
    
    winner = graphene.relay.Node.Field(AllWinnersNode)
    all_winners = DjangoFilterConnectionField(AllWinnersNode)
    
    character = graphene.relay.Node.Field(CharacterNode)
    all_characters = graphene.List(CharacterNode)
    
    sorted_currently_watching = graphene.List(AnimeNode)
    
    all_anime_winners = graphene.List(AllWinnersNode)
    all_character_winners = graphene.List(CharacterAwardsWinnerNode)
    
    def resolve_all_anime_winners(root, info):
        all_winners = AllWinners.objects.all()
        return all_winners  
    
    def resolve_all_character_winners(root, info):
        all_character_winners = CharacterAwardsWinner.objects.all()
        return all_character_winners
    
    # comb_winners = graphene.List(CombWinners)
    
    def resolve_comb_winners(root, info):
        all_winners = AllWinners.objects.all()
        all_character_winners = CharacterAwardsWinner.objects.all()
        return all_winners, all_character_winners
    
    
    # def resolve_winners(self, info):
    def resolve_all_characters(root, info):
        return Character.objects.all()
        
    def resolve_sorted_currently_watching(root, info) :
        allAnimes = Anime.objects.all()
        sorted_anime = sorted(allAnimes, key=lambda x: x.currently_watching, reverse=True)
        return sorted_anime[:10]
    
    # def resolve_anime_and_character_winners(root, info):
    #     all_winners = AllWinners.objects.all()
    #     all_character_winners = CharacterAwardsWinner.objects.all()
    #     return chain(all_winners, all_character_winners)

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

class addAnimeVote(graphene.Mutation):
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
        return Anime.objects.get( anime_name = id)
        
    
    @staticmethod
    def get_award(name):
        return Awards.objects.get(award_name = name)
    
    def mutate(self, info, user_data=None, anime_data=None, award_name=None):
        user = addAnimeVote.get_user(user_data.user_id)
        anime = addAnimeVote.get_anime(anime_data.anime_name)
        award = addAnimeVote.get_award(award_name)
        print(user, anime, award)
        print("the year and season is:", year, season)
        try:
            try:
                all_anime_awards = AnimeAwards.objects.filter(award__award_name = award_name, season = season, year = year)
                print(all_anime_awards)
                user_exist = all_anime_awards.filter(allUsers = user)
                print(user_exist)
                if user_exist:
                    print("user already voted for this award")
                    return GraphQLError(f"user already voted for this award {season} {year}")
                
            except Exception:
                print("there was an error ")
                ["award1", "blue lock"]
            anime_award = AnimeAwards.objects.get(anime__anime_name = anime_data.anime_name, award__award_name = award_name, season = season, year = year)
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
                # date = today
                season = season,
                year = year
            )
            # anime_award.allUsers.add(user)
            anime_award.save()
            anime_award.allUsers.add(user)
            anime_award.save()
            user.user_voted_animes.add(anime_award)
            user.save()
            print(anime_award)
        return addAnimeVote(anime_award = anime_award) 
    
class addCharacterVote(graphene.Mutation):
    class Arguments:
        user_data = userInput(required = True)
        # anime_data = animeInput(required = True)
        award_name = graphene.String(required = True)
        character_name = graphene.String(required = True)
    
    character_award = graphene.Field(CharacterAwardsNode)
    
    @staticmethod
    def get_user(id):
        return UserProfile.objects.get(user_id = id)
    
    @staticmethod
    def get_character(id):
        return Character.objects.get(character_name = id)
        
    
    @staticmethod
    def get_award(name):
        return Awards.objects.get(award_name = name)
    
    def mutate(self, info, user_data=None, character_name=None, award_name=None):
        user = addCharacterVote.get_user(user_data.user_id)
        character = addCharacterVote.get_character(character_name)
        award = addCharacterVote.get_award(award_name)
        print(user, character, award)
        print("hi")
        try:
            try:
                all_character_awards = CharacterAwards.objects.filter(award__award_name = award_name, season = season, year = year)
                print(all_character_awards)
                user_exist = all_character_awards.filter(allUsers = user)
                print(user_exist)
                if user_exist:
                    print("user already voted for this award")
                    return GraphQLError(f"user already voted for this award {season} {year}")
                
            except Exception:
                print("there was an error ")
                ["award1", "blue lock"]
            character_award = CharacterAwards.objects.get(character__character_name = character_name, award__award_name = award_name, season = season, year = year)
            print("This is the award:", character_award)
            if character_award:
                print("Character exists")
                # if user in anime_award.allUsers.all():
                #     print("user already voted for this anime for this award")
                #     return GraphQLError("user already voted for this anime for this award")
                character_award.vote_count += 1
                character_award.allUsers.add(user)
                character_award.save()
                user.user_voted_characters.add(character_award)
                user.save()
            
        except CharacterAwards.DoesNotExist:
            print("Anime Award does not exist and will now be created")
            character_award = CharacterAwards(
                vote_count = 1,
                character = character,
                award = award,
                # date = today
                season = season,
                year = year
            )
            # anime_award.allUsers.add(user)
            character_award.save()
            character_award.allUsers.add(user)
            character_award.save()
            user.user_voted_characters.add(character_award)
            user.save()
            print(character_award)
        return addCharacterVote(character_award = character_award) 
    
class winner(graphene.Mutation):
    anime_awards = graphene.List(AllWinnersNode)
    character_awards = graphene.List(CharacterAwardsWinnerNode)
    # anime = graphene.Field(AnimeNode)
    

    
    def mutate(self, info):
        date = today
        anime_awards = []
        season = ""
        

        match month:
            case 1 | 2 | 3:
                season = "Winter"
            case 4 | 5 | 6:
                season = "Spring"
            case 7 | 8 | 9:
                season = "Summer"
            case 10 | 11 | 12:
                season = "Fall"
                
                
        def filterWinner(winner):
            print("sdcdscds", season, year)
            if winner.season == season and winner.year == year:
                return True
            else: 
                return False
        
        # # filtered_all_anime_winners = filter(filterWinner, AllWinners.objects.all())
        # filtered_all_winners = 
        
        # print(list(filtered_all_anime_winners))

        
        all_awards = Awards.objects.all()
        all_winners = list(AllWinners.objects.all()) + list(CharacterAwardsWinner.objects.all())
        # print(all_winners)
        filtered_all_winners = filter(filterWinner, all_winners)
        if len(list(filtered_all_winners)) > 0:
            return GraphQLError(f"You have already ran the winner mutation for {season}, {year}")
        
        print(list(filtered_all_winners))
        
        # all_winners.filter
        
        for award in all_awards:
            anime_awards.append(award)
        
        for anime_award in anime_awards:
            try:
                if "Character" in str(anime_award):
                     all_character_awards = CharacterAwards.objects.filter(award__award_name = anime_award, season = season, year = year)
                     highest_vote_count = max(all_character_awards, key=lambda y: y.vote_count).vote_count
                    #  print(highest_vote_count)
                    
                     filtered_character_awards = all_character_awards.filter(vote_count = highest_vote_count)
                    #  print(len(filtered_anime_awards))
                     for filtered_character_award in filtered_character_awards:
                        # if filtered_anime_award in AllWinners.objects.all():
                        #     return GraphQLError(f"{filtered_anime_award.anime.anime_name} has already won the {filtered_anime_award.award.award_name} award")
                        
                        filtered_character_name = filtered_character_award.character.character_name
                        filtered_award_name = filtered_character_award.award.award_name
                        filtered_character = Character.objects.get(character_name = filtered_character_name)
                        filtered_award = Awards.objects.get(award_name = filtered_award_name)
                        # filtered_award.date = date
                        filtered_award.save()
                        # print(date)
                        filtered_character.character_awards.add(filtered_award)
                        filtered_character.save()
                        # return filtered_anime
        
                        CharacterAwardsWinner.objects.create(character_winner = filtered_character_award, date = date, season = season, year = year)
                        # print(self.all_winners)
                        # print(filtered_anime_award, filtered_anime_name)
                        # print(f"The {filtered_award_name} Award goes to {filtered_anime_name}")
                    
                        # print(anime_award, "character award")
                else:
                    print(anime_award, "anime award")
                    all_anime_awards = AnimeAwards.objects.filter(award__award_name = anime_award, season = season, year = year)
                    highest_vote_count = max(all_anime_awards, key=lambda y: y.vote_count).vote_count
                    # print(highest_vote_count)
                    
                    filtered_anime_awards = all_anime_awards.filter(vote_count = highest_vote_count)
                    # print(len(filtered_anime_awards))
                    for filtered_anime_award in filtered_anime_awards:
                        # if filtered_anime_award in AllWinners.objects.all():
                        #     return GraphQLError(f"{filtered_anime_award.anime.anime_name} has already won the {filtered_anime_award.award.award_name} award")
                        
                        filtered_anime_name = filtered_anime_award.anime.anime_name
                        filtered_award_name = filtered_anime_award.award.award_name
                        filtered_anime = Anime.objects.get(anime_name = filtered_anime_name)
                        filtered_award = Awards.objects.get(award_name = filtered_award_name)
                        # filtered_award.date = date
                        filtered_award.save()
                        # print(date)
                        filtered_anime.anime_awards.add(filtered_award)
                        filtered_anime.save()
                        # return filtered_anime
        
                        AllWinners.objects.create(winner = filtered_anime_award, date = date, season = season, year = year)
                        # print(self.all_winners)
                        # print(filtered_anime_award, filtered_anime_name)
                        print(f"The {filtered_award_name} Award goes to {filtered_anime_name}")

            except:
                print("there is an error")
        # print(AllWinners.objects.all())
        # FindAwardWinner = FindAwardWinner()
        # # FindAwardWinner.determine_winner()
        # anime_awards = FindAwardWinner.determine_winner()
        # AnimeAwards.objects.all().delete()
        # CharacterAwards.objects.all().delete()
        return winner(anime_awards = AllWinners.objects.all(), character_awards = CharacterAwardsWinner.objects.all())
        
    
class Mutation(graphene.ObjectType):
    add_anime_vote = addAnimeVote.Field()
    add_character_vote = addCharacterVote.Field()
    winner = winner.Field()