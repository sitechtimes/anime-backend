from django.db import models
from anime.models import Anime


class UserAnime(models.Model):
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
    currently_watching = models.BooleanField()
    watchlist = models.BooleanField()
    finished_anime = models.BooleanField()
    rating = models.IntegerField()
    # user = models.ForeignKey(
    #    User, related_name="ingredients", on_delete=models.CASCADE
    # )

class User(models.Model):
    user_name = models.CharField(max_length=100)
    grade = models.IntegerField()
    email = models.EmailField()
    # profile_img = models.ImageField()     # need to add a media root for it to work(just search it)
    user_anime = models.ManyToManyField(
        UserAnime
    )

