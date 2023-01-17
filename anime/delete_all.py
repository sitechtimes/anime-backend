from anime.models import Anime, Genre, Studio

Anime.objects.all().delete()
Genre.objects.all().delete()
Studio.objects.all().delete()