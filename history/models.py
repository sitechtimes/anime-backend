from django.db import models
from anime.models import Anime

from django.utils import timezone
# Create your models here.
class RatedAnime(models.Model):
    time = models.DateTimeField(default=timezone.now)
    anime_rated = models.ForeignKey(Anime,  on_delete=models.CASCADE)
    #mostwatched will be the one with the most ratings

class MostSearchedAnime(models.Model):
    daily = models.ManyToManyField(Anime, related_name='daily2Anime')
    weekly = models.ManyToManyField(Anime, related_name='weekly2Anime')
    monthly = models.ManyToManyField(Anime, related_name='monthly2Anime')
    yearly_searched = models.ManyToManyField(Anime, related_name='yearly2Anime')
#
# class SeasonalAnimeAwards(models.Model):
#     fall = models.ManyToManyField(Anime,related_name='fall2Anime')
#     winter = models.ManyToManyField(Anime,related_name='winter2Anime')
#     spring = models.ManyToManyField(Anime,related_name='spring2Anime')
#     summer = models.ManyToManyField(Anime,related_name='summer2Anime')
#     yearly_awards = models.ManyToManyField(Anime,related_name='yearly2Anime')


class History(models.Model):
    rated_anime = models.ManyToManyField(RatedAnime)
    most_searched_anime = models.OneToOneField(MostSearchedAnime, on_delete=models.CASCADE)
    # seasonal_anime_awards = models.OneToOneField(SeasonalAnimeAwards, on_delete=models.CASCADE)



