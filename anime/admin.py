from django.contrib import admin
from anime.models import Anime, Genre, Awards, AnimeAwards, Studio, Character
import requests
import datetime
# Register your models here.


admin.site.register(Genre)
admin.site.register(Anime)
admin.site.register(Awards)
admin.site.register(AnimeAwards)

admin.site.register(Character)

admin.site.register(AllWinners)
admin.site.register(Studio)

