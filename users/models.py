from django.db import models
from anime.models import Anime
from django.contrib.auth.models import AbstractUser

class UserAnime(models.Model):
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
    currently_watching = models.BooleanField()
    watchlist = models.BooleanField()
    finished_anime = models.BooleanField()
    rating = models.IntegerField(null=True)

    # def __str__(self):
    #     return self.rating


class CustomUser(AbstractUser):
    # username = models.CharField(max_length=100)
    # grade = models.IntegerField()
    email = models.EmailField()



class UserProfile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    grade = models.IntegerField()
    user_anime = models.ManyToManyField( UserAnime,related_name='taken', blank=True)
    # profile_img = models.ImageField()     # need to add a media root for it to work(just search it)

