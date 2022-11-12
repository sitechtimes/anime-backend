from django.db import models

# Create your models here.


class Genre(models.Model):
    genre = models.CharField(max_length=255)


class Awards(models.Model):
    award_name = models.CharField(max_length=255)
    # award_img = models.ImageField() #search for more parameters
    award_description = models.CharField(max_length=300)


class AnimeAwards(models.Model):
    nominated_for_award = models.BooleanField()
    has_award = models.BooleanField()
    anime_award_name = models.OneToOneField(Awards, on_delete=models.CASCADE, )


class Anime(models.Model):
    anime_name = models.CharField(max_length=255)
    # picture = models.ImageField() #search for more parameters
    episodes = models.IntegerField()
    studio_name = models.CharField(max_length=255)
    aired = models.BooleanField(null=True)
    status = models.DateField()
    seasons = models.IntegerField()
    summary = models.TextField()
    anime_genre = models.ManyToManyField(Genre)
    anime_awards = models.ManyToManyField(AnimeAwards)

