from django.db import models

# Create your models here.

class Genre(models.Model):
    genre = models.CharField(max_length=255)

class Anime(models.Model):
    anime_name = models.CharField(max_length=255)
    # picture = models.ImageField() #search for more parameters
    episodes = models.IntegerField()
    studio_name = models.CharField(max_length=255)
    aired = models.BooleanField(null=True)
    status = models.DateField()
    season = models.IntegerField()
    summary = models.TextField()
    anime_genre = models.ManyToManyField(Genre)

