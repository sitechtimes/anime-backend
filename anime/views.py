from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from anime.models import Anime
from anime.serializers import AnimeSerializer


# Create your views here.
class AnimeView(APIView):
    def get(self, request, format = None):
        animes = Anime.objects.all()
        serializer = AnimeSerializer(animes, many = True)
        return Response(serializer.data)
