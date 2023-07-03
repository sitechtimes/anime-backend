from rest_framework import serializers
from anime.models import Anime, Genre, Studio, AllWinners, CharacterAwardsWinner, AnimeAwards, CharacterAwards,  Character

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = [
            "genre"
        ]
class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = [
            "character_name"
        ]
        
        
class StudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Studio
        fields = [
            "studio"
        ]
    
class AnimeSerializer(serializers.ModelSerializer):
    anime_genre = GenreSerializer(many = True, read_only = True)
    anime_studio = StudioSerializer(many = True, read_only = True)
    anime_characters = CharacterSerializer(many = True, read_only = True)
    
    class Meta:
        model = Anime
        fields = "__all__"
        # fields = [
        #     "mal_id",
        #     "anime_name",
        #     "media_type",
        #     "image_url",
        #     "small_image_url",
        #     "large_image_url",
        #     "trailer_youtube_url",
        #     "episodes",
        #     "status",
        #     "aired_from",
        #     "aired_to",
        #     "summary",
        #     "anime_studio",
        #     "anime_genre",
        #     "anime_awards",
        #     "number_rating"
        # ]
     

# class AnimeWinnersSerializer(serializers.ModelSerializer):
#     # winner = AnimeAwardsSerializer(many = True)
#     winner = serializers.PrimaryKeyRelatedField(queryset=AnimeAwards.objects.all(), many = True, read_only = False)
#     class Meta:
#         model = AllWinners
#         fields = [
#             "date",
#             "season",
#             "year",
#             # "winner"
#         ]     
   
# class AnimeAwardsSerializer(serializers.ModelSerializer):
#     # anime = AnimeSerializer(many = True, read_only = True)
#     # allWinners = AnimeWinnersSerializer(many = True, read_only = True)
#     class Meta:
#         model = AnimeAwards
#         fields = [
#             "vote_count",
#             "award",
#         ]
# class CharacterAwardsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CharacterAwards
#         fields = "__all__"
        

        
# class CharacterWinnersSerializer(serializers.ModelSerializer):
#     # character_winner = CharacterAwardsSerializer(many = True, read_only = True)
#     class Meta:
#         model = CharacterAwardsWinner
#         fields = "__all__"

