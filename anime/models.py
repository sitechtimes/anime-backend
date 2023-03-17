from django.db import models

# Create your models here.


class Genre(models.Model):
    genre = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.genre


class Studio(models.Model):
    studio = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.studio

class Awards(models.Model):
    award_name = models.CharField(max_length=255)
    # award_img = models.ImageField() #search for more parameters

    def __str__(self):

        return self.award_name


class AnimeAwards(models.Model):
    nominated_for_award = models.BooleanField()
    nominated_date = models.DateField(null=True)
    has_award = models.BooleanField()
    received_date = models.DateField(null=True)
    anime_award_name = models.OneToOneField(Awards, on_delete=models.CASCADE, )


    def __str__(self):
        return self.anime_award_name.award_name


class Character(models.Model):
    mal_id = models.IntegerField(null=True)
    character_name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    image_url = models.URLField(max_length=255, null=True)

    def __str__(self):
        return self.character_name

class Anime(models.Model):
    mal_id = models.IntegerField(null=True)
    anime_name = models.CharField(max_length=255)
    media_type = models.CharField(max_length=255, null=True)
    image_url = models.URLField(max_length=255, null=True)
    small_image_url = models.URLField(max_length=255, null=True)
    large_image_url = models.URLField(max_length=255, null=True)
    trailer_youtube_url = models.URLField(max_length=255, null=True)
    episodes = models.IntegerField(null=True)
    status = models.CharField(max_length=255, null=True)
    aired_from = models.DateField(null=True)
    aired_to = models.DateField(null=True)
    summary = models.TextField(null=True)
    season = models.CharField(max_length=255,null=True)
    anime_studio = models.ManyToManyField(Studio)
    anime_genre = models.ManyToManyField(Genre)
    anime_characters = models.ManyToManyField(Character)
    anime_awards = models.ManyToManyField(AnimeAwards)


    def __str__(self):
        return self.anime_name




