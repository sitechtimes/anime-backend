from rest_framework import serializers
from .models import AnimeAwards

class WinnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimeAwards
        fields = [
            ""
        ]