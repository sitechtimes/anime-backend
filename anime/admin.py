from django.contrib import admin

from.models import Anime, Genre, Awards, AnimeAwards, AllWinners, Studio, Character
# Register your models here.

admin.site.register(Studio)
admin.site.register(Genre)
admin.site.register(Character)
admin.site.register(Anime)
admin.site.register(Awards)
admin.site.register(AnimeAwards)
admin.site.register(Character)
