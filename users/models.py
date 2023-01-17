from django.db import models
from anime.models import Anime
from django.contrib.auth.models import AbstractUser, User
from django.core.validators import MaxValueValidator, MinValueValidator


from django.db.models.signals import post_save
from django.dispatch import receiver

watching_status = [
    ("NOT_WATCHING", "Not Watching"),
    ("CURRENTLY_WATCHING",  "Currently watching"),
    ("WATCHLIST", "Watchlist"),
    ("FINISHED_ANIME", "Finished Anime")
]

class UserAnime(models.Model):
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
    # currently_watching = models.BooleanField()
    # watchlist = models.BooleanField()
    # finished_anime = models.BooleanField()
    rating = models.IntegerField(null=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])
    watching_status = models.CharField(max_length=20, choices=watching_status, default="NOT_WATCHING")

    # def __str__(self):
    #     return self.rating


class CustomUser(AbstractUser):
    # username = models.CharField(max_length=100)
    # grade = models.IntegerField()
    email = models.EmailField()



class UserProfile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    # grade = models.IntegerField()
    user_anime = models.ManyToManyField(UserAnime,related_name='taken', blank=True)
    # profile_img = models.ImageField()     # need to add a media root for it to work(just search it)
    # def __str__(self) -> str:
    #     return user
    def __str__(self):
        return f"{self.user.username}"

@receiver(post_save, sender=CustomUser)
def create_user_customer(sender, instance, created, **kwargs):
    if created:
        try:
            print(instance.email)
            index = instance.email.index("@")
            print(index)
            account = instance.email[index + 1:]
            print(account)
            if account != ("nycstudents.net" or "schools.nyc.gov"):
                user = User.objects.get(email = instance.email)
                print(user)
                print("wassup")
                # user.remove()
                return 
            else:
                user = UserProfile.objects.get_or_create(user=instance)
        except Exception:
            return

post_save.connect(create_user_customer, sender=CustomUser)
