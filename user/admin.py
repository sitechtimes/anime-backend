from django.contrib import admin
from user.models import UserAnime, User, AllUserAnime

admin.site.register(UserAnime)
admin.site.register(User)
admin.site.register(AllUserAnime)