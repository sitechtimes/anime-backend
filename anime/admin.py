from django.contrib import admin
from.models import Anime, Genre, Awards, AnimeAwards, AllWinners
# Register your models here.


admin.site.register(Genre)
admin.site.register(Anime)
admin.site.register(Awards)
admin.site.register(AnimeAwards)
admin.site.register(AllWinners)