from rest_framework import serializers
from anime.models import Anime, Genre, Studio

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = [
            "genre"
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
    