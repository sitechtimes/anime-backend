from django.contrib import admin
from history.models import RatedAnime, MostSearchedAnime, History

admin.site.register(RatedAnime)
admin.site.register(MostSearchedAnime)
# admin.site.register(SeasonalAnimeAwards)
admin.site.register(History)
