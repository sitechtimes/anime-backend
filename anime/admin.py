from django.contrib import admin
from django.shortcuts import render
from.models import Anime, Genre, Awards, AnimeAwards, Studio
import requests
import datetime

# Register your models here.

admin.site.register(Studio)
admin.site.register(Genre)
admin.site.register(Anime)
admin.site.register(Awards)
admin.site.register(AnimeAwards)
