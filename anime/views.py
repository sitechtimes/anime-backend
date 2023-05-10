from django.shortcuts import render
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from anime.models import Anime, Genre
from anime.serializers import AnimeSerializer, GenreSerializer


# Create your views here.
class AnimeView(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, format = None):
        animes = Anime.objects.all()
        serializer = AnimeSerializer(animes, many = True)
        return Response(serializer.data)
    
class GenreView(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, format = None):
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many = True)
        return Response(serializer.data)
