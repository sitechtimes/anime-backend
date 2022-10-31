from django.db import models

# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
class Anime(models.Model):
    name = models.CharField(max_length=255)
    picture = models.ImageField() #search for more parameters
    episodes = models.IntegerField()
    studio_name = models.CharField(max_length=255)
    aired = models.BooleanField(null=True)
    completed = models.BooleanField(null=True)
    season = models.IntegerField()
    summary = models.TextField()
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    #need to add userrated and awards

