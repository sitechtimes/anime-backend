from rest_framework import serializers
from anime.models import Anime

class AnimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anime
        fields = [
            "mal_id",
            "anime_name",
            "media_type",
            "image_url",
            "small_image_url",
            "large_image_url",
            "trailer_youtube_url",
            "episodes",
            "status",
            "aired_from",
            "aired_to",
            "summary",
            "anime_studio",
            "anime_genre",
            "anime_awards",
            "number_rating"
        ]
    